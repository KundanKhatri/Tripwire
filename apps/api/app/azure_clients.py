"""Thin async clients for the live Azure AI services.

Supports BOTH auth modes:
  - API key (local dev / simple Container Apps): set AZURE_*_API_KEY / _KEY
  - Managed identity (production best practice): leave keys blank, role-assign

These wrap raw REST so we control versions and degrade gracefully when a service
is unavailable (the defense pipeline must never hard-fail on a dependency).
"""

from __future__ import annotations

import httpx

from app.settings import Settings


class EmbeddingsClient:
    def __init__(self, settings: Settings) -> None:
        self.s = settings

    @property
    def available(self) -> bool:
        return bool(self.s.azure_openai_endpoint and self.s.azure_openai_api_key)

    async def embed(self, text: str) -> list[float] | None:
        if not self.available:
            return None
        url = (
            f"{self.s.azure_openai_endpoint.rstrip('/')}/openai/deployments/"
            f"{self.s.azure_openai_deployment_embed}/embeddings"
            f"?api-version={self.s.azure_openai_api_version}"
        )
        try:
            async with httpx.AsyncClient(timeout=10.0) as http:
                resp = await http.post(
                    url,
                    headers={"api-key": self.s.azure_openai_api_key, "Content-Type": "application/json"},
                    json={"input": text},
                )
                resp.raise_for_status()
                return resp.json()["data"][0]["embedding"]
        except Exception:  # noqa: BLE001 — graceful degradation
            return None


class PromptShieldsClient:
    def __init__(self, settings: Settings) -> None:
        self.s = settings

    @property
    def available(self) -> bool:
        return bool(self.s.azure_content_safety_endpoint and self.s.azure_content_safety_key)

    async def detect(self, user_prompt: str, documents: list[str] | None = None) -> dict:
        if not self.available:
            return {"available": False, "attack_detected": False}
        url = (
            f"{self.s.azure_content_safety_endpoint.rstrip('/')}"
            f"/contentsafety/text:shieldPrompt?api-version=2024-09-01"
        )
        try:
            async with httpx.AsyncClient(timeout=6.0) as http:
                resp = await http.post(
                    url,
                    headers={
                        "Ocp-Apim-Subscription-Key": self.s.azure_content_safety_key,
                        "Content-Type": "application/json",
                    },
                    json={"userPrompt": user_prompt, "documents": documents or []},
                )
                if resp.status_code >= 400:
                    return {"available": True, "attack_detected": False, "error": resp.status_code}
                body = resp.json()
                attack = body.get("userPromptAnalysis", {}).get("attackDetected", False)
                return {"available": True, "attack_detected": bool(attack)}
        except Exception as exc:  # noqa: BLE001
            return {"available": True, "attack_detected": False, "error": str(exc)[:120]}
