"""Victim-agent tools, each guarded by capability provenance (L2) and canary
exfil checks (L3).

These are deliberately the kinds of tools an attacker wants to hijack:
  - send_email   (exfiltration channel)
  - read_file    (sensitive-data source)
  - http_get     (data-exfil + SSRF channel)

A tool refuses to execute unless the caller presents a capability token that
authorizes *that* tool. Every tool's output and arguments are scanned for canary
tokens before anything leaves the boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.agent.provenance import ProvenanceAuthority


@dataclass
class ToolCall:
    tool: str
    args: dict
    capability_token: str | None = None


@dataclass
class ToolResult:
    tool: str
    executed: bool
    output: str
    denied_reason: str | None = None
    l2_signal: dict = field(default_factory=dict)
    l3_signal: dict = field(default_factory=dict)


# Simulated sensitive environment the agent operates in. The canary is a decoy
# secret seeded into the agent's context; if it ever appears in a tool argument
# or output, that is proof of exfiltration (L3).
SENSITIVE_FILES = {
    "/secrets/api_key.txt": "PROD_KEY=sk-live-9f3a2b7c1e8d4f6a",
}


class GuardedToolbox:
    def __init__(self, authority: ProvenanceAuthority, canaries: set[str]) -> None:
        self.authority = authority
        self.canaries = canaries

    def _canary_scan(self, text: str) -> list[str]:
        return [c for c in self.canaries if c.lower() in (text or "").lower()]

    def invoke(self, call: ToolCall) -> ToolResult:
        # L2 — capability provenance gate
        allowed, reason = self.authority.authorize(call.capability_token, call.tool)
        l2 = {"authorized": allowed, "reason": reason}
        if not allowed:
            return ToolResult(
                tool=call.tool, executed=False, output="",
                denied_reason=f"L2 blocked: {reason}", l2_signal=l2,
            )

        # L3 — canary scan on the *arguments* (catches "send the secret out" attempts)
        arg_text = " ".join(str(v) for v in call.args.values())
        arg_hits = self._canary_scan(arg_text)
        if arg_hits:
            return ToolResult(
                tool=call.tool, executed=False, output="",
                denied_reason=f"L3 blocked: canary token in tool arguments ({len(arg_hits)} hit)",
                l2_signal=l2, l3_signal={"arg_canary_hits": arg_hits},
            )

        # Execute the (simulated) tool
        out = self._run(call)

        # L3 — canary scan on the *output* before it leaves the boundary
        out_hits = self._canary_scan(out)
        if out_hits:
            return ToolResult(
                tool=call.tool, executed=False, output="[REDACTED]",
                denied_reason=f"L3 blocked: canary token in tool output ({len(out_hits)} hit)",
                l2_signal=l2, l3_signal={"output_canary_hits": out_hits},
            )

        return ToolResult(tool=call.tool, executed=True, output=out, l2_signal=l2,
                          l3_signal={"clean": True})

    def _run(self, call: ToolCall) -> str:
        if call.tool == "read_file":
            path = call.args.get("path", "")
            return SENSITIVE_FILES.get(path, f"(no such file: {path})")
        if call.tool == "send_email":
            to = call.args.get("to", "?")
            body = call.args.get("body", "")
            return f"email queued to {to} ({len(body)} chars)"
        if call.tool == "http_get":
            return f"fetched {call.args.get('url', '?')} (200, 1.2kb)"
        return f"(unknown tool: {call.tool})"
