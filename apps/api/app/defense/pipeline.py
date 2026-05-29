"""Defense pipeline — orchestrates the 5 layers."""

from __future__ import annotations

import asyncio
from uuid import uuid4

from app.defense.layers.l1_semantic import L1SemanticFirewall
from app.defense.layers.l2_provenance import L2CapabilityProvenance
from app.defense.layers.l3_canary import L3CanaryTokens
from app.defense.layers.l4_anomaly import L4BehavioralAnomaly
from app.defense.layers.l5_classifier import L5LearningClassifier
from app.schemas import DefendRequest, DefendResponse, LayerResult, Verdict


class DefensePipeline:
    """Runs all defense layers against an incoming payload.

    Strategy: L1-L3 are evaluated in order with short-circuit on hard block.
    L4-L5 run concurrently for the soft scoring tier.
    The final verdict is the worst across all enabled layers.
    """

    def __init__(
        self,
        l1: L1SemanticFirewall,
        l2: L2CapabilityProvenance,
        l3: L3CanaryTokens,
        l4: L4BehavioralAnomaly,
        l5: L5LearningClassifier,
    ) -> None:
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4
        self.l5 = l5

    async def evaluate(self, req: DefendRequest) -> DefendResponse:
        results: list[LayerResult] = []

        l1_result = await self.l1.evaluate(req)
        results.append(l1_result)
        if l1_result.verdict == Verdict.BLOCK:
            return DefendResponse(
                request_id=uuid4(),
                verdict=Verdict.BLOCK,
                layers=results,
                explanation=None,
            )

        l2_result = await self.l2.evaluate(req)
        results.append(l2_result)

        l3_result = await self.l3.evaluate(req)
        results.append(l3_result)

        l4_task = asyncio.create_task(self.l4.evaluate(req))
        l5_task = asyncio.create_task(self.l5.evaluate(req))
        l4_result, l5_result = await asyncio.gather(l4_task, l5_task)
        results.extend([l4_result, l5_result])

        verdict = self._aggregate(results)
        return DefendResponse(
            request_id=uuid4(),
            verdict=verdict,
            layers=results,
            explanation=None,
        )

    @staticmethod
    def _aggregate(results: list[LayerResult]) -> Verdict:
        if any(r.verdict == Verdict.BLOCK for r in results):
            return Verdict.BLOCK
        if any(r.verdict == Verdict.REVIEW for r in results):
            return Verdict.REVIEW
        return Verdict.ALLOW
