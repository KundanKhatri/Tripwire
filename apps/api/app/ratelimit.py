"""Lightweight in-memory rate limiting for the public endpoints.

A fixed-window limiter keyed on client IP. Protects the paid Azure path
(/assess fans out to embeddings + Prompt Shields) and the /lead sink from abuse.

Note: state is per-replica. With min-replicas 1 that's effectively global; at
higher scale move to a shared store (Redis) — the dependency surface stays the same.
"""

from __future__ import annotations

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status


def client_ip(request: Request) -> str:
    """Real client IP behind the Container Apps ingress proxy."""
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class FixedWindowLimiter:
    def __init__(self, limit: int, window_s: float, max_keys: int = 10_000) -> None:
        self.limit = limit
        self.window = window_s
        self.max_keys = max_keys
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        dq = self._hits[key]
        while dq and now - dq[0] > self.window:
            dq.popleft()
        if len(dq) >= self.limit:
            retry = max(1, int(self.window - (now - dq[0])))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in ~{retry}s.",
                headers={"Retry-After": str(retry)},
            )
        dq.append(now)
        if len(self._hits) > self.max_keys:
            self._prune(now)

    def _prune(self, now: float) -> None:
        stale = [k for k, dq in self._hits.items() if not dq or now - dq[-1] > self.window]
        for k in stale:
            del self._hits[k]


def make_dependency(limit: int, window_s: float):
    limiter = FixedWindowLimiter(limit, window_s)

    async def _dep(request: Request) -> None:
        limiter.check(client_ip(request))

    return _dep
