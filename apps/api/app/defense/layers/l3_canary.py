"""L3 — Canary tokens.

Decoy strings are injected into the agent's context before each run. If any
canary ever appears outside the agent boundary (response, tool args, would-be
outbound HTTP), it is a 100% confidence exfiltration signal — no model
judgment required.

For the /defend endpoint this layer scans the incoming payload for any active
canary the requester would have no legitimate reason to know. A hit means the
user is replaying exfiltrated context (a "canary echo" attack indicator).
"""

from __future__ import annotations

import secrets
import time

from app.schemas import DefendRequest, LayerName, LayerResult, Verdict

CANARY_PREFIX = "tw-canary-"


def mint_canary() -> str:
    return f"{CANARY_PREFIX}{secrets.token_hex(8)}"


class L3CanaryTokens:
    def __init__(self) -> None:
        # In-memory active set; in prod backed by Cosmos `canaries` table.
        self._active: set[str] = set()

    def register(self, canary: str) -> None:
        self._active.add(canary)

    def revoke(self, canary: str) -> None:
        self._active.discard(canary)

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        hits: list[str] = []
        payload_lower = req.payload.lower()
        for canary in self._active:
            if canary.lower() in payload_lower:
                hits.append(canary)

        # Also flag obvious canary-shaped tokens that aren't ours — strong sign
        # someone is probing the system or replaying exfiltrated decoys.
        suspicious_unknown = []
        if CANARY_PREFIX in payload_lower:
            suspicious_unknown.append("payload contains canary-prefix pattern")

        if hits:
            verdict = Verdict.BLOCK
            reason = f"Active canary token observed in payload ({len(hits)} matches)"
            confidence = 1.0
        elif suspicious_unknown:
            verdict = Verdict.REVIEW
            reason = "Canary-prefix pattern in payload but no active canary match"
            confidence = 0.7
        else:
            verdict = Verdict.ALLOW
            reason = None
            confidence = 1.0

        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L3_CANARY,
            verdict=verdict,
            confidence=confidence,
            latency_ms=round(latency_ms, 2),
            signals={
                "active_canaries": len(self._active),
                "matched": hits,
                "suspicious": suspicious_unknown,
            },
            reason=reason,
        )
