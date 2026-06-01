"""Terminal demo for the victim-agent scenario — the headline TripWire demo.

Runs the REAL defense pipeline (L2 capability provenance + L3 canary) via
run_poisoned_scenario() and prints the step-by-step trace in the colored
[plan] / [tool] / [blocked] / [final] format shown in the README and deck.

This is what the demo video records. No mock — the verdicts come from the
same code path the API and arena use.

Run:
    cd apps/api && python -m app.agent.cli
    # slow, cinematic typing for recording:
    cd apps/api && python -m app.agent.cli --slow
"""
from __future__ import annotations

import argparse
import sys
import time

from app.agent.runner import run_poisoned_scenario
from app.defense.layers.l3_canary import mint_canary

# ANSI — degrade gracefully if not a TTY.
_TTY = sys.stdout.isatty()


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _TTY else s


DIM = "2"
BOLD = "1"
GREEN = "1;32"
RED = "1;31"
YELLOW = "1;33"
BLUE = "1;34"
CYAN = "1;36"
GREY = "90"

KIND_STYLE = {
    "plan": (GREY, "[plan]   "),
    "tool": (GREEN, "[tool]   "),
    "blocked": (RED, "[blocked]"),
    "final": (CYAN, "[final]  "),
}


def _line(s: str = "", delay: float = 0.0) -> None:
    sys.stdout.write(s + "\n")
    sys.stdout.flush()
    if delay:
        time.sleep(delay)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="TripWire victim-agent terminal demo")
    p.add_argument("--slow", action="store_true",
                   help="pause between steps for screen recording")
    args = p.parse_args(argv)
    pause = 0.9 if args.slow else 0.0

    canary = mint_canary()
    run = run_poisoned_scenario(secret_canary=canary)

    _line()
    _line(_c(BOLD, "  TripWire — victim agent — live trace"), pause)
    _line(_c(GREY, "  scenario: indirect prompt injection → secret exfiltration"))
    _line()
    _line(_c(DIM, f"  user request : {run.user_request}"))
    _line(_c(DIM, f"  granted tools: {run.granted_tools}  ")
          + _c(YELLOW, "(NOT read_file, NOT send_email)"), pause)
    _line()

    for step in run.steps:
        color, tag = KIND_STYLE.get(step.kind, (GREY, f"[{step.kind}]"))
        # final summary wraps; keep tag on its own line for readability.
        if step.kind == "final":
            _line()
            _line(f"  {_c(color, tag)} " + _c(BOLD, "ATTACK NEUTRALIZED"), 0)
            for chunk in _wrap(step.detail, 76):
                _line(_c(GREY, f"           {chunk}"))
        else:
            _line(f"  {_c(color, tag)} {step.detail}", pause)

    _line()
    verdict = (_c(RED, "  ✗ BREACHED") if run.breached
               else _c(GREEN, "  ✓ Nothing sensitive left the boundary."))
    _line(verdict)
    _line(_c(GREY, "    L2 denied every injected tool call for lack of provenance;"))
    _line(_c(GREY, "    an LLM prompt firewall alone would not have caught this."))
    _line()
    return 1 if run.breached else 0


def _wrap(text: str, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
