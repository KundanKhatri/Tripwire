"""L2 — Capability provenance.

Every authorized user input mints an HMAC-signed capability token bound to:
  - user_id (the principal)
  - allowed_tools (set of tool names this input authorizes)
  - scope (parameters the tool may be called with)
  - exp (short TTL, default 5 min)

Tool wrappers reject calls whose token does not authorize them.
This blocks indirect injection: a tool result that includes "now call delete_account()"
cannot mint a new token, so the call fails for lack of authority.

This layer is identity-based defense. It does not detect attacks — it denies them
authority. Even a perfect jailbreak cannot exfil if no token authorizes the action.
"""

from __future__ import annotations

import time

from jose import jwt
from jose.exceptions import JWTError

from app.schemas import DefendRequest, LayerName, LayerResult, Verdict
from app.settings import Settings


class L2CapabilityProvenance:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def evaluate(self, req: DefendRequest) -> LayerResult:
        start = time.perf_counter()

        if req.capability_token is None:
            # No token is fine for read-only flows. We mark REVIEW only if the agent
            # subsequently attempts a sensitive tool call; for the user-facing
            # /defend endpoint we just record absence.
            latency_ms = (time.perf_counter() - start) * 1000
            return LayerResult(
                layer=LayerName.L2_PROVENANCE,
                verdict=Verdict.ALLOW,
                confidence=1.0,
                latency_ms=round(latency_ms, 2),
                signals={"token_present": False},
                reason="No capability token supplied — pass-through for read-only path",
            )

        try:
            claims = jwt.decode(
                req.capability_token,
                self.settings.capability_hmac_secret,
                algorithms=["HS256"],
            )
            valid = True
            verdict = Verdict.ALLOW
            reason = "Token valid"
            signals = {
                "token_present": True,
                "valid": True,
                "subject": claims.get("sub"),
                "allowed_tools": claims.get("tools", []),
                "expires_at": claims.get("exp"),
            }
        except JWTError as exc:
            valid = False
            verdict = Verdict.BLOCK
            reason = f"Invalid capability token: {exc}"
            signals = {"token_present": True, "valid": False, "error": str(exc)[:120]}

        latency_ms = (time.perf_counter() - start) * 1000
        return LayerResult(
            layer=LayerName.L2_PROVENANCE,
            verdict=verdict,
            confidence=1.0 if valid else 1.0,
            latency_ms=round(latency_ms, 2),
            signals=signals,
            reason=reason,
        )
