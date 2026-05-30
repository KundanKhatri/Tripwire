from fastapi import APIRouter

from app.deps import get_pipeline, state
from app.schemas import DefendRequest, DefendResponse

router = APIRouter(tags=["defense"])


@router.post("/defend", response_model=DefendResponse)
async def defend(req: DefendRequest) -> DefendResponse:
    return await get_pipeline().evaluate(req)


@router.get("/status")
async def status() -> dict:
    return {
        "corpus_indexed": state.corpus_count,
        "corpus_ready": state.corpus.ready if state.corpus else False,
        "pipeline_ready": state.pipeline is not None,
    }
