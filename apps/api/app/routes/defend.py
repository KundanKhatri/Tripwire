from fastapi import APIRouter, Depends

from app.defense import DefensePipeline
from app.defense.layers.l1_semantic import L1SemanticFirewall
from app.defense.layers.l2_provenance import L2CapabilityProvenance
from app.defense.layers.l3_canary import L3CanaryTokens
from app.defense.layers.l4_anomaly import L4BehavioralAnomaly
from app.defense.layers.l5_classifier import L5LearningClassifier
from app.schemas import DefendRequest, DefendResponse
from app.settings import Settings, get_settings

router = APIRouter(tags=["defense"])


def _pipeline(settings: Settings) -> DefensePipeline:
    # Singleton-per-process is fine for now; revisit if state grows.
    return DefensePipeline(
        l1=L1SemanticFirewall(settings=settings, corpus_searcher=None),
        l2=L2CapabilityProvenance(settings=settings),
        l3=L3CanaryTokens(),
        l4=L4BehavioralAnomaly(),
        l5=L5LearningClassifier(),
    )


@router.post("/defend", response_model=DefendResponse)
async def defend(req: DefendRequest, settings: Settings = Depends(get_settings)) -> DefendResponse:
    pipeline = _pipeline(settings)
    return await pipeline.evaluate(req)
