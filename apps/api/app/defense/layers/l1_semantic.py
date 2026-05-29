"""L1 — Semantic firewall.

Three sub-checks, evaluated concurrently:
  (a) Pattern bank — fast regex/structural rules for known injection forms
  (b) Azure AI Content Safety Prompt Shields — Microsoft's published baseline
  (c) Embedding similarity — pgvector cosine search vs. curated attack corpus

The layer returns:
  - BLOCK if any sub-check returns high-confidence detection
  - REVIEW if a soft signal fires (e.g., similarity 0.65-0.78)
  - ALLOW otherwise

Latency target: p95 ≤ 200ms (gated by Prompt Shields round-trip).
"""

from __future__ import annotations

import asyncio
import re
import time
from typing import Any

import httpx
from azure.ai.contentsafety.aio import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.identity.aio import DefaultAzureCredential

from app.schemas import DefendRequest, LayerName, LayerResult, Verdict
from app.settings import Settings

# Threshold for embedding similarity to known attacks (cosine).
SIM_BLOCK_THRESHOLD = 0.82
SIM_REVIEW_THRESHOLD = 0.70


# Pattern bank — rules drawn from OWASP LLM Top 10 examples + public injection corpora.
# Each rule is (id, owasp_class, compiled_regex, severity).
PATTERN_RULES: list[tuple[str, str, re.Pattern[str], int]] = [
    # Role override / system prompt leak attempts
    ("role_override_ignore", "LLM01", re.compile(r"\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?)", re.I), 9),
    ("role_override_disregard", "LLM01", re.compile(r"\b(disregard|forget|override)\s+(your|the)\s+(instructions?|system\s+prompt|guidelines?)", re.I), 9),
    ("role_override_assistant", "LLM01", re.compile(r"\byou\s+are\s+(now\s+)?(a\s+)?(different|new)\s+(assistant|ai|model)\b", re.I), 8),
    # System prompt extraction
    ("system_prompt_leak", "LLM01", re.compile(r"\b(reveal|show|print|repeat|tell\s+me)\s+(your|the)\s+(system\s+prompt|initial\s+instructions|hidden\s+instructions)", re.I), 9),
    ("verbatim_request", "LLM01", re.compile(r"\bverbatim\b.{0,40}\b(prompt|instructions|system\s+message)", re.I), 8),
    # Delimiter / injection markers
    ("delimiter_escape", "LLM01", re.compile(r"(\"\"\"|'''|<\|im_(end|start)\|>|<\/?system>|<\/?assistant>|<\/?user>)", re.I), 7),
    ("markdown_inject", "LLM01", re.compile(r"^\s*```\s*system\s*$", re.I | re.M), 7),
    # Encoded / obfuscated commands
    ("base64_hidden", "LLM01", re.compile(r"\b(decode|base64).{0,40}(execute|run|follow)", re.I), 8),
    # Tool / function abuse
    ("tool_force", "LLM07", re.compile(r"\b(call|invoke|execute)\s+(the\s+)?(tool|function|api)\s+\w+\s+(with|using)", re.I), 6),
    # Exfiltration cues
    ("exfil_external", "LLM02", re.compile(r"\b(send|post|GET|fetch)\b.{0,40}\bhttps?://", re.I), 7),
    ("exfil_image_md", "LLM02", re.compile(r"!\[[^\]]*\]\(https?://[^)]+\?[^)]*=[^)]*\)", re.I), 8),
    # Jailbreak personas
    ("jailbreak_dan", "LLM01", re.compile(r"\b(DAN|do\s+anything\s+now|developer\s+mode\s+enabled)\b", re.I), 9),
    ("jailbreak_hypothetical", "LLM01", re.compile(r"\bhypothetically\b.{0,40}\b(unrestricted|no\s+rules|no\s+filter)", re.I), 7),
    # Excessive agency
    ("agency_grant", "LLM08", re.compile(r"\byou\s+(have|are\s+given)\s+(full|admin|root|sudo)\s+(access|permissions?)", re.I), 8),
]


class L1SemanticFirewall:
    def __init__(self, settings: Settings, corpus_searcher: "CorpusSearcher | None" = None) -> None:
        self.settings = settings
        self.corpus = corpus_searcher
        self._cs_client: ContentSafetyClient | None = None

    async def _content_safety_client(self) -> ContentSafetyClient | None:
        if not self.settings.azure_content_safety_endpoint:
            return None
        if self._cs_client is None:
            self._cs_client = ContentSafetyClient(
                endpoint=self.settings.azure_content_safety_endpoint,
                credential=DefaultAzureCredential(),  # managed identity in prod
            )
        return self._cs_client

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        pattern_task = asyncio.create_task(self._check_patterns(req.payload))
        shields_task = asyncio.create_task(self._check_prompt_shields(req.payload))
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

        high_sev_hits = [h for h in pattern_hits if h["severity"] >= 8]
        if high_sev_hits:
            verdict = Verdict.BLOCK
            confidence = max(confidence, 0.9)
            reason = reason or f"High-severity pattern match: {high_sev_hits[0]['id']}"
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
            confidence=confidence,
            latency_ms=round(latency_ms, 2),
            signals=signals,
            reason=reason,
        )

    @staticmethod
    async def _check_patterns(payload: str) -> list[dict[str, Any]]:
        hits: list[dict[str, Any]] = []
        for rule_id, owasp, regex, severity in PATTERN_RULES:
            match = regex.search(payload)
            if match:
                hits.append(
                    {
                        "id": rule_id,
                        "owasp_class": owasp,
                        "severity": severity,
                        "matched": match.group(0)[:80],
                    }
                )
        return hits

    async def _check_prompt_shields(self, payload: str) -> dict[str, Any]:
        client = await self._content_safety_client()
        if client is None:
            return {"available": False, "attack_detected": False}
        try:
            # Prompt Shields detects user-prompt injection and indirect injection via documents.
            # The SDK exposes `analyze_text` for content harm; Prompt Shields uses a separate
            # endpoint we hit directly via httpx for now (SDK convergence pending).
            url = f"{self.settings.azure_content_safety_endpoint}/contentsafety/text:shieldPrompt?api-version=2024-09-01"
            async with httpx.AsyncClient(timeout=5.0) as http:
                # Auth: managed identity in prod (token); key for local dev (set via env).
                cred = DefaultAzureCredential()
                token = await cred.get_token("https://cognitiveservices.azure.com/.default")
                resp = await http.post(
                    url,
                    headers={"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"},
                    json={"userPrompt": payload, "documents": []},
                )
                if resp.status_code >= 400:
                    return {"available": True, "attack_detected": False, "error": resp.status_code}
                body = resp.json()
                attack = body.get("userPromptAnalysis", {}).get("attackDetected", False)
                return {"available": True, "attack_detected": attack, "raw": body}
        except Exception as exc:  # noqa: BLE001 — degrade gracefully if Shields unavailable
            return {"available": True, "attack_detected": False, "error": str(exc)[:120]}

    async def _check_similarity(self, payload: str) -> dict[str, Any]:
        if self.corpus is None:
            return {"available": False, "top_score": 0.0, "neighbors": []}
        try:
            neighbors = await self.corpus.search(payload, k=3)
            top_score = neighbors[0]["score"] if neighbors else 0.0
            return {
                "available": True,
                "top_score": top_score,
                "neighbors": [
                    {"id": n["id"], "attack_type": n["attack_type"], "score": n["score"]}
                    for n in neighbors
                ],
            }
        except Exception as exc:  # noqa: BLE001
            return {"available": True, "top_score": 0.0, "error": str(exc)[:120]}


class CorpusSearcher:
    """Embedding-similarity search over the attack corpus.

    Implementation note: in prod, this hits pgvector. For local dev without DB,
    a JSONL-backed in-memory fallback is provided so the layer is testable solo.
    """

    async def search(self, payload: str, k: int = 3) -> list[dict[str, Any]]:
        raise NotImplementedError
