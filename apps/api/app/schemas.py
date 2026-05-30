from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


class LayerName(str, Enum):
    L1_SEMANTIC = "L1_semantic_firewall"
    L2_PROVENANCE = "L2_capability_provenance"
    L3_CANARY = "L3_canary_tokens"
    L4_ANOMALY = "L4_behavioral_anomaly"
    L5_CLASSIFIER = "L5_learning_classifier"


class LayerResult(BaseModel):
    layer: LayerName
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    latency_ms: float
    signals: dict[str, Any] = Field(default_factory=dict)
    reason: str | None = None


class DefendRequest(BaseModel):
    payload: str = Field(..., description="The user input to evaluate")
    agent_id: str = Field(default="demo-agent")
    conversation_id: UUID | None = None
    capability_token: str | None = None
    inject_canaries: bool = True


class DefendResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    verdict: Verdict
    layers: list[LayerResult]
    explanation: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
