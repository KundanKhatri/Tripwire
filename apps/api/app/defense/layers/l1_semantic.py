"""L1 — Semantic firewall.

Three sub-checks, evaluated concurrently:
  (a) Pattern bank — fast regex/structural rules for known injection forms
  (b) Azure AI Content Safety Prompt Shields — Microsoft's published baseline
  (c) Embedding similarity — cosine search vs. the curated attack corpus

Returns:
  - BLOCK if any sub-check returns high-confidence detection
  - REVIEW if a soft signal fires (e.g. similarity 0.70-0.82)
  - ALLOW otherwise

Latency target: p95 <= 200ms (gated by Prompt Shields round-trip).
"""

from __future__ import annotations

import asyncio
import re
import time
from typing import Any

from app.azure_clients import PromptShieldsClient
from app.corpus import CorpusSearcher
from app.schemas import DefendRequest, LayerName, LayerResult, Verdict

SIM_BLOCK_THRESHOLD = 0.82
SIM_REVIEW_THRESHOLD = 0.70

PATTERN_RULES: list[tuple[str, str, re.Pattern[str], int]] = [
    ("role_override_ignore", "LLM01", re.compile(r"\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?)", re.I), 9),
    ("role_override_disregard", "LLM01", re.compile(r"\b(disregard|forget|override)\s+(your|the)\s+(instructions?|system\s+prompt|guidelines?)", re.I), 9),
    ("role_override_assistant", "LLM01", re.compile(r"\byou\s+are\s+(now\s+)?(a\s+)?(different|new)\s+(assistant|ai|model)\b", re.I), 8),
    ("system_prompt_leak", "LLM01", re.compile(r"\b(reveal|show|print|repeat|tell\s+me)\s+(your|the)\s+(system\s+prompt|initial\s+instructions|hidden\s+instructions)", re.I), 9),
    ("verbatim_request", "LLM01", re.compile(r"\bverbatim\b.{0,40}\b(prompt|instructions|system\s+message)", re.I), 8),
    ("delimiter_escape", "LLM01", re.compile(r"(\"\"\"|'''|<\|im_(end|start)\|>|<\/?system>|<\/?assistant>|<\/?user>)", re.I), 7),
    ("markdown_inject", "LLM01", re.compile(r"^\s*```\s*system\s*$", re.I | re.M), 7),
    ("base64_hidden", "LLM01", re.compile(r"\b(decode|base64).{0,40}(execute|run|follow)", re.I), 8),
    ("tool_force", "LLM07", re.compile(r"\b(call|invoke|execute)\s+(the\s+)?(tool|function|api)\s+\w+\s+(with|using)", re.I), 6),
    ("exfil_external", "LLM02", re.compile(r"\b(send|post|GET|fetch)\b.{0,40}\bhttps?://", re.I), 7),
    ("exfil_image_md", "LLM02", re.compile(r"!\[[^\]]*\]\(https?://[^)]+\?[^)]*=[^)]*\)", re.I), 8),
    ("jailbreak_dan", "LLM01", re.compile(r"\b(DAN|do\s+anything\s+now|developer\s+mode\s+enabled)\b", re.I), 9),
    ("jailbreak_hypothetical", "LLM01", re.compile(r"\bhypothetically\b.{0,40}\b(unrestricted|no\s+rules|no\s+filter)", re.I), 7),
    ("agency_grant", "LLM08", re.compile(r"\byou\s+(have|are\s+given)\s+(full|admin|root|sudo)\s+(access|permissions?)", re.I), 8),
    ("indirect_inject", "LLM01", re.compile(r"(###\s*system\s*###|\[note from admin\]|new instruction:)", re.I), 9),
]


class L1SemanticFirewall:
    def __init__(self, shields: PromptShieldsClient, corpus: CorpusSearcher) -> None:
        self.shields = shields
        self.corpus = corpus

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        pattern_task = asyncio.create_task(self._check_patterns(req.payload))
        shields_task = asyncio.create_task(self.shields.detect(req.payload))
        sim_task = asyncio.create_task(self._check_similarity(req.payload))
        pattern_hits, shields_signal, sim_signal = await asyncio.gather(
            pattern_task, shields_task, sim_task
        )

        signals: dict[str, Any] = {
            "pattern_hits": pattern_hits,
            "prompt_shields": shields_signal,
            "embedding_similarity": sim_signal,
        }

        verdict = Verdict.ALLOW
        confidence = 0.0
        reason: str | None = None

        if shields_signal.get("attack_detected"):
            verdict = Verdict.BLOCK
            confidence = max(confidence, 0.95)
            reason = "Azure Prompt Shields detected attack"

        high_sev = [h for h in pattern_hits if h["severity"] >= 8]
        if high_sev:
            verdict = Verdict.BLOCK
            confidence = max(confidence, 0.9)
            reason = reason or f"High-severity pattern match: {high_sev[0]['id']}"
        elif pattern_hits and verdict == Verdict.ALLOW:
            verdict = Verdict.REVIEW
            confidence = max(confidence, 0.6)
            reason = reason or f"Pattern match: {pattern_hits[0]['id']}"

        top_sim = sim_signal.get("top_score", 0.0)
        if top_sim >= SIM_BLOCK_THRESHOLD:
            verdict = Verdict.BLOCK
            confidence = max(confidence, top_sim)
            reason = reason or f"High similarity to known attack ({top_sim:.2f})"
        elif top_sim >= SIM_REVIEW_THRESHOLD and verdict == Verdict.ALLOW:
            verdict = Verdict.REVIEW
            confidence = max(confidence, top_sim * 0.8)
            reason = reason or f"Moderate similarity to known attack ({top_sim:.2f})"

        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L1_SEMANTIC,
            verdict=verdict,
            confidence=round(confidence, 3),
            latency_ms=round(latency_ms, 2),
            signals=signals,
            reason=reason,
        )

    @staticmethod
    async def _check_patterns(payload: str) -> list[dict[str, Any]]:
        hits: list[dict[str, Any]] = []
        for rule_id, owasp, regex, severity in PATTERN_RULES:
            m = regex.search(payload)
            if m:
                hits.append({"id": rule_id, "owasp_class": owasp, "severity": severity, "matched": m.group(0)[:80]})
        return hits

    async def _check_similarity(self, payload: str) -> dict[str, Any]:
        try:
            neighbors = await self.corpus.search(payload, k=3)
            top = neighbors[0]["score"] if neighbors else 0.0
            return {
                "available": self.corpus.ready,
                "top_score": round(top, 4),
                "neighbors": [{"id": n["id"], "attack_type": n["attack_type"], "score": round(n["score"], 4)} for n in neighbors],
            }
        except Exception as exc:  # noqa: BLE001
            return {"available": False, "top_score": 0.0, "error": str(exc)[:120]}
