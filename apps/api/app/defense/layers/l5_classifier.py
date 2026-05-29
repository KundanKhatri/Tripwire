"""L5 — Learning classifier.

Calls a fine-tuned classifier (Azure ML managed online endpoint) to score the
payload as benign / suspicious / malicious. The model is retrained nightly
on the growing attack corpus + arena attempts.

Skeleton lands Day 0; real model deployment lands Day 4. Until then this
returns ALLOW with low confidence so the trace shape is preserved.
"""

from __future__ import annotations

import time

from app.schemas import DefendRequest, LayerName, LayerResult, Verdict


class L5LearningClassifier:
    def __init__(self, endpoint_url: str | None = None) -> None:
        self.endpoint_url = endpoint_url

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()
        # TODO Day 4: HTTP call to Azure ML endpoint with managed-identity auth.
        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L5_CLASSIFIER,
            verdict=Verdict.ALLOW,
            confidence=0.3,
            latency_ms=round(latency_ms, 2),
            signals={"model_deployed": False, "skeleton": True},
            reason="Classifier endpoint not yet deployed (Day 4 target)",
        )
