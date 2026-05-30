"""Shared singletons: Azure clients, corpus index, and the defense pipeline.

Built once at app startup (see main.lifespan) so the corpus is embedded a single
time and reused across requests.
"""

from __future__ import annotations

from app.azure_clients import EmbeddingsClient, PromptShieldsClient
from app.corpus import CorpusSearcher
from app.defense.layers.l1_semantic import L1SemanticFirewall
from app.defense.layers.l2_provenance import L2CapabilityProvenance
from app.defense.layers.l3_canary import L3CanaryTokens
from app.defense.layers.l4_anomaly import L4BehavioralAnomaly
from app.defense.layers.l5_classifier import L5LearningClassifier
from app.defense.pipeline import DefensePipeline
from app.settings import get_settings


class AppState:
    pipeline: DefensePipeline | None = None
    corpus: CorpusSearcher | None = None
    corpus_count: int = 0


state = AppState()


async def startup() -> None:
    settings = get_settings()
    embeddings = EmbeddingsClient(settings)
    shields = PromptShieldsClient(settings)
    corpus = CorpusSearcher(embeddings)
    state.corpus_count = await corpus.build()
    state.corpus = corpus
    state.pipeline = DefensePipeline(
        l1=L1SemanticFirewall(shields=shields, corpus=corpus),
        l2=L2CapabilityProvenance(settings=settings),
        l3=L3CanaryTokens(),
        l4=L4BehavioralAnomaly(),
        l5=L5LearningClassifier(),
    )


def get_pipeline() -> DefensePipeline:
    if state.pipeline is None:
        raise RuntimeError("Pipeline not initialized")
    return state.pipeline
