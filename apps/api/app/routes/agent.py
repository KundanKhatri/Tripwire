from __future__ import annotations

from fastapi import APIRouter

from app.agent.runner import run_poisoned_scenario
from app.defense.layers.l3_canary import mint_canary

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/demo/indirect-injection")
async def demo_indirect_injection() -> dict:
    """Run the headline scenario: an indirect prompt injection that tries to
    exfiltrate a secret, defeated by L2 capability provenance + L3 canary.

    Returns the full step-by-step trace the Glass Box renders.
    """
    canary = mint_canary()
    run = run_poisoned_scenario(secret_canary=canary)
    return {
        "scenario": "indirect_prompt_injection_exfiltration",
        "user_request": run.user_request,
        "granted_tools": run.granted_tools,
        "breached": run.breached,
        "summary": run.summary,
        "steps": [{"kind": s.kind, "detail": s.detail, "data": s.data} for s in run.steps],
    }
