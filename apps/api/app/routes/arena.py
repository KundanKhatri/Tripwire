from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/arena", tags=["arena"])


class ArenaAttempt(BaseModel):
    handle: str
    payload: str


class ArenaAttemptResponse(BaseModel):
    attempt_id: str
    verdict: str
    score: int
    rank: int | None = None


@router.post("/attempt", response_model=ArenaAttemptResponse)
async def attempt(_body: ArenaAttempt) -> ArenaAttemptResponse:
    # TODO Day 5: persist + push to SignalR
    return ArenaAttemptResponse(attempt_id="stub", verdict="allow", score=0)


@router.get("/leaderboard")
async def leaderboard() -> list[dict]:
    # TODO Day 5: read top 100 from Cosmos
    return []
