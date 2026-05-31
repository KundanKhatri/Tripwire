"""Capability provenance — the heart of L2.

A *capability token* is minted ONLY from a genuine end-user instruction. It is an
HMAC-signed grant that scopes exactly which tools the agent may call, on whose
behalf, for how long. Every tool invocation must present a token that authorizes
*that specific tool*. A tool call that originates from injected text in a
document or tool-output has no token chain back to a real user turn — so it is
denied for lack of authority, regardless of how convincing the injection is.

This is identity-based defense: it does not try to *detect* the attack. It denies
the attack *authority*. Even a perfect, never-before-seen jailbreak cannot make
the agent act, because the malicious instruction cannot mint a token.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from jose import jwt
from jose.exceptions import JWTError


@dataclass
class Capability:
    subject: str  # the user principal the grant belongs to
    allowed_tools: list[str]  # tools this grant authorizes
    issued_at: int
    expires_at: int


class ProvenanceAuthority:
    """Mints and verifies capability tokens. The signing key never leaves here."""

    def __init__(self, secret: str, default_ttl_s: int = 300) -> None:
        self._secret = secret
        self._ttl = default_ttl_s

    def mint(self, subject: str, allowed_tools: list[str], ttl_s: int | None = None) -> str:
        now = int(time.time())
        exp = now + (ttl_s or self._ttl)
        claims = {
            "sub": subject,
            "tools": sorted(set(allowed_tools)),
            "iat": now,
            "exp": exp,
            "purpose": "tripwire-capability",
        }
        return jwt.encode(claims, self._secret, algorithm="HS256")

    def authorize(self, token: str | None, tool: str) -> tuple[bool, str]:
        """Return (allowed, reason). A missing/invalid token => denied."""
        if not token:
            return False, f"no capability token presented for tool '{tool}'"
        try:
            claims = jwt.decode(token, self._secret, algorithms=["HS256"])
        except JWTError as exc:
            return False, f"invalid capability token: {exc}"
        if claims.get("purpose") != "tripwire-capability":
            return False, "token is not a TripWire capability"
        allowed = claims.get("tools", [])
        if tool not in allowed:
            return False, f"tool '{tool}' not in granted scope {allowed}"
        return True, f"authorized for '{tool}' as {claims.get('sub')}"
