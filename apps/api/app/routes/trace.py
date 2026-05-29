from uuid import UUID

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["trace"])


@router.get("/trace/{request_id}")
async def get_trace(request_id: UUID) -> dict:
    # TODO Day 2: read from Cosmos `defense_traces` table once DB layer lands.
    raise HTTPException(status_code=404, detail="Trace store not yet implemented (Day 2 target)")
