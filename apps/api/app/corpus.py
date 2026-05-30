"""In-memory attack-corpus similarity index.

For the prototype we avoid standing up Cosmos for PostgreSQL (cost + setup) by
embedding the seed corpus once at startup and doing cosine search in-process.
The interface matches what a pgvector-backed searcher would expose, so swapping
to Cosmos later is a drop-in change (see ARCHITECTURE.md).
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any

from app.azure_clients import EmbeddingsClient

# Look for the seed corpus in multiple locations so it works both in local dev
# (repo layout) and inside the container (bundled copy under app/data/).
_HERE = Path(__file__).resolve()
_CANDIDATE_PATHS = [
    _HERE.parent / "data" / "seeds.jsonl",  # bundled in container build context
    _HERE.parents[3] / "packages" / "attack-corpus" / "seeds.jsonl",  # repo root
]


def _resolve_corpus_path() -> Path | None:
    for p in _CANDIDATE_PATHS:
        if p.exists():
            return p
    return None


_CORPUS_PATH = _resolve_corpus_path() or _CANDIDATE_PATHS[0]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class CorpusSearcher:
    def __init__(self, embeddings: EmbeddingsClient) -> None:
        self.embeddings = embeddings
        self._index: list[dict[str, Any]] = []
        self._ready = False

    @property
    def ready(self) -> bool:
        return self._ready

    async def build(self) -> int:
        """Embed every seed pattern once. Returns count indexed."""
        if not self.embeddings.available or not _CORPUS_PATH.exists():
            return 0
        rows: list[dict[str, Any]] = []
        with _CORPUS_PATH.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        for r in rows:
            vec = await self.embeddings.embed(r["payload"])
            if vec is not None:
                self._index.append(
                    {"id": r["id"], "attack_type": r["attack_type"], "embedding": vec}
                )
        self._ready = len(self._index) > 0
        return len(self._index)

    async def search(self, payload: str, k: int = 3) -> list[dict[str, Any]]:
        if not self._ready:
            return []
        q = await self.embeddings.embed(payload)
        if q is None:
            return []
        scored = [
            {"id": e["id"], "attack_type": e["attack_type"], "score": _cosine(q, e["embedding"])}
            for e in self._index
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:k]
