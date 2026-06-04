"""L5 — Learning classifier.

An embedding nearest-centroid classifier over the *live* corpus. It builds two
class centroids from Azure OpenAI embeddings:
  - malicious — the mean of the seeded attack corpus (reused from L1's index, so
    we don't re-embed it)
  - benign — the mean of a benign-anchor set

At request time it embeds the payload and compares cosine similarity to each
centroid. A payload that leans malicious (and clears a floor, to avoid flagging
random out-of-distribution text) is routed to REVIEW. It never hard-BLOCKs on
its own — L5 is the soft, advisory tier, protecting the zero-false-positive
posture; L1 already hard-blocks the certain cases.

It *learns*: `learn(text, malicious=...)` adds a labeled example and updates the
relevant centroid, so the boundary improves as the arena is attacked. This is a
real, honest learning loop — not a fine-tuned model endpoint (that's the
roadmap); we don't overclaim.

When embeddings are unavailable (offline / local mirror) it returns ALLOW with
low confidence so the trace shape is preserved.
"""

from __future__ import annotations

import time
from typing import Any

from app.corpus import CorpusSearcher, _cosine
from app.schemas import DefendRequest, LayerName, LayerResult, Verdict

BENIGN_ANCHORS = [
    "Please summarize the attached quarterly report.",
    "What are the key risks mentioned in this document?",
    "Translate this paragraph into French.",
    "Help me draft a friendly reply to this customer email.",
    "Explain what this code function does.",
    "What time is the meeting scheduled for?",
    "Give me three bullet points on the main findings.",
    "Can you proofread this paragraph for grammar?",
    "What is the capital of Australia?",
    "Recommend a good book on data structures.",
]

# Decision boundary on (sim_to_malicious - sim_to_benign). Conservative to
# protect 0% FP; tune against the live eval set.
MAL_REVIEW_MARGIN = 0.08
MAL_FLOOR = 0.30  # payload must be at least this close to the malicious centroid


def _centroid(vectors: list[list[float]]) -> list[float] | None:
    if not vectors:
        return None
    dim = len(vectors[0])
    acc = [0.0] * dim
    for v in vectors:
        for i, x in enumerate(v):
            acc[i] += x
    n = len(vectors)
    return [x / n for x in acc]


class L5LearningClassifier:
    def __init__(
        self, embeddings: Any | None = None, corpus: CorpusSearcher | None = None
    ) -> None:
        self.embeddings = embeddings
        self.corpus = corpus
        self._mal_vecs: list[list[float]] = []
        self._ben_vecs: list[list[float]] = []
        self._mal_centroid: list[float] | None = None
        self._ben_centroid: list[float] | None = None
        self._trained = False
        self._learned_count = 0

    @property
    def _embeddings_available(self) -> bool:
        return bool(self.embeddings is not None and getattr(self.embeddings, "available", False))

    async def warmup(self) -> int:
        """Build class centroids once. Returns total examples used (0 if offline)."""
        if self._trained or not self._embeddings_available:
            return 0
        # Reuse the corpus's already-embedded attack vectors (no re-embedding).
        if self.corpus is not None:
            self._mal_vecs = [e["embedding"] for e in getattr(self.corpus, "_index", [])]
        for text in BENIGN_ANCHORS:
            vec = await self.embeddings.embed(text)
            if vec is not None:
                self._ben_vecs.append(vec)
        self._recompute()
        return len(self._mal_vecs) + len(self._ben_vecs)

    def _recompute(self) -> None:
        self._mal_centroid = _centroid(self._mal_vecs)
        self._ben_centroid = _centroid(self._ben_vecs)
        self._trained = self._mal_centroid is not None and self._ben_centroid is not None

    async def learn(self, text: str, malicious: bool) -> bool:
        """Add a labeled example and update the boundary — the learning hook."""
        if not self._embeddings_available:
            return False
        vec = await self.embeddings.embed(text)
        if vec is None:
            return False
        (self._mal_vecs if malicious else self._ben_vecs).append(vec)
        self._learned_count += 1
        self._recompute()
        return True

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        if self._trained and self._embeddings_available:
            vec = await self.embeddings.embed(req.payload)
            if vec is not None and self._mal_centroid is not None and self._ben_centroid is not None:
                sim_mal = _cosine(vec, self._mal_centroid)
                sim_ben = _cosine(vec, self._ben_centroid)
                margin = sim_mal - sim_ben
                malicious = margin >= MAL_REVIEW_MARGIN and sim_mal >= MAL_FLOOR
                label = "malicious" if malicious else ("suspicious" if margin > 0 else "benign")
                signals: dict[str, Any] = {
                    "model": "embedding-nearest-centroid",
                    "label": label,
                    "sim_malicious": round(sim_mal, 4),
                    "sim_benign": round(sim_ben, 4),
                    "margin": round(margin, 4),
                    "corpus_size": len(self._mal_vecs),
                    "learned_examples": self._learned_count,
                }
                if malicious:
                    return self._finish(
                        start, Verdict.REVIEW, round(min(0.5 + margin, 0.95), 3),
                        f"Classifier: payload leans malicious "
                        f"(sim={sim_mal:.2f}, margin={margin:.2f})", signals,
                    )
                return self._finish(start, Verdict.ALLOW, round(max(sim_ben, 0.1), 3), None, signals)

        # Offline / untrained fallback — preserve trace shape.
        return self._finish(
            start, Verdict.ALLOW, 0.3, None,
            {"model": "unavailable", "trained": self._trained},
        )

    @staticmethod
    def _finish(
        start: float,
        verdict: Verdict,
        confidence: float,
        reason: str | None,
        signals: dict[str, Any],
    ) -> LayerResult:
        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L5_CLASSIFIER,
            verdict=verdict,
            confidence=confidence,
            latency_ms=round(latency_ms, 2),
            signals=signals,
            reason=reason,
        )
