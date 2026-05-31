"""L2 provenance + L3 canary — the layers that actually differentiate TripWire."""

from __future__ import annotations

from app.agent.provenance import ProvenanceAuthority
from app.agent.runner import run_poisoned_scenario
from app.agent.tools import GuardedToolbox, ToolCall
from app.defense.layers.l3_canary import mint_canary


def test_token_authorizes_only_granted_tools() -> None:
    auth = ProvenanceAuthority(secret="k")
    tok = auth.mint("user:a", ["read_document"])
    ok, _ = auth.authorize(tok, "read_document")
    assert ok
    bad, reason = auth.authorize(tok, "send_email")
    assert not bad and "not in granted scope" in reason


def test_missing_token_denied() -> None:
    auth = ProvenanceAuthority(secret="k")
    ok, reason = auth.authorize(None, "send_email")
    assert not ok and "no capability token" in reason


def test_l2_blocks_unauthorized_tool_call() -> None:
    auth = ProvenanceAuthority(secret="k")
    box = GuardedToolbox(auth, canaries=set())
    tok = auth.mint("user:a", ["read_document"])  # not send_email
    res = box.invoke(ToolCall("send_email", {"to": "x@y.com", "body": "hi"}, tok))
    assert not res.executed
    assert "L2 blocked" in (res.denied_reason or "")


def test_l3_blocks_canary_in_args() -> None:
    auth = ProvenanceAuthority(secret="k")
    canary = mint_canary()
    box = GuardedToolbox(auth, canaries={canary})
    tok = auth.mint("user:a", ["send_email"])  # authorized this time
    res = box.invoke(ToolCall("send_email", {"to": "x@y.com", "body": f"key={canary}"}, tok))
    assert not res.executed
    assert "L3 blocked" in (res.denied_reason or "")


def test_full_scenario_not_breached() -> None:
    run = run_poisoned_scenario(secret_canary=mint_canary())
    assert run.breached is False
    # Both malicious tool calls must be blocked.
    blocked = [s for s in run.steps if s.kind == "blocked"]
    assert len(blocked) >= 2
