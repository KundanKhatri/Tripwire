"""L4 — Behavioral anomaly.

Compares the embedded planned action against the embedded user goal. Divergence
beyond a threshold indicates goal hijack. Cross-checks with Azure AI Content
Safety Groundedness when an agent justification is available.

For the /defend endpoint we operate on the user input alone (no agent action
yet); we score how off-topic / out-of-distribution the input is compared to
the conversation's prior turns or the declared agent purpose.

Full implementation lands Day 3 — this is the wired skeleton with a
deterministic placeholder that returns ALLOW unless the payload is obviously
incoherent. The skeleton keeps the trace shape stable.
"""

from __future__ import annotations

import time

from app.schemas import DefendRequest, LayerName, LayerResult, Verdict


class L4BehavioralAnomaly:
    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        # Skeleton: flag REVIEW for very short payloads with imperative verbs
        # targeting tools — a coarse anomaly signal until full embedding-based
        # divergence ships on Day 3.
        words = req.payload.split()
        is_short_imperative = len(words) <= 8 and any(
            w.lower() in {"delete", "drop", "exec", "execute", "rm", "shutdown"}
            for w in words
        )

        if is_short_imperative:
            verdict = Verdict.REVIEW
            reason = "Short imperative payload with destructive verb"
            confidence = 0.5
        else:
            verdict = Verdict.ALLOW
            reason = None
            confidence = 0.9

        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L4_ANOMALY,
            verdict=verdict,
            confidence=confidence,
            latency_ms=round(latency_ms, 2),
            signals={"skeleton": True, "tokens": len(words)},
            reason=reason,
        )
