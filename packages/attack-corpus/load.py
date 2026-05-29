"""Load the seed attack corpus into Cosmos for Postgres with pgvector embeddings.

Run after provisioning Azure resources and setting POSTGRES_URL +
AZURE_OPENAI_ENDPOINT.

Usage:
    python load.py [--dry-run]

This script:
  1. Reads seeds.jsonl
  2. Generates embeddings via Azure OpenAI text-embedding-3-large
  3. Upserts rows into attack_patterns table
  4. Reports inserted/updated counts
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
from uuid import uuid4

import httpx

SEED_PATH = Path(__file__).parent / "seeds.jsonl"


async def get_embedding(text: str, endpoint: str, deployment: str, token: str) -> list[float]:
    url = f"{endpoint}/openai/deployments/{deployment}/embeddings?api-version=2024-10-21"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"input": text},
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]


async def main(dry_run: bool) -> None:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_EMBED", "text-embedding-3-large")
    pg_url = os.environ.get("POSTGRES_URL", "")

    if dry_run:
        print("[dry-run] would load:", SEED_PATH)

    seeds: list[dict] = []
    with SEED_PATH.open() as f:
        for line in f:
            line = line.strip()
            if line:
                seeds.append(json.loads(line))

    print(f"Loaded {len(seeds)} seed patterns")
    if dry_run:
        for s in seeds[:3]:
            print(f"  {s['id']} [{s['attack_type']}] {s['payload'][:60]}...")
        return

    if not endpoint or not pg_url:
        raise SystemExit("Set AZURE_OPENAI_ENDPOINT and POSTGRES_URL before running without --dry-run")

    # Get a token via managed identity (or az login locally)
    from azure.identity.aio import DefaultAzureCredential

    cred = DefaultAzureCredential()
    token = (await cred.get_token("https://cognitiveservices.azure.com/.default")).token

    import psycopg

    inserted = 0
    async with await psycopg.AsyncConnection.connect(pg_url) as conn:
        async with conn.cursor() as cur:
            for s in seeds:
                emb = await get_embedding(s["payload"], endpoint, deployment, token)
                await cur.execute(
                    """
                    INSERT INTO attack_patterns
                      (id, attack_type, owasp_category, payload, source_ref, embedding, severity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                      payload = EXCLUDED.payload,
                      embedding = EXCLUDED.embedding,
                      severity = EXCLUDED.severity
                    """,
                    (
                        str(uuid4()),
                        s["attack_type"],
                        s["owasp_category"],
                        s["payload"],
                        s.get("source", ""),
                        emb,
                        s.get("severity", 5),
                    ),
                )
                inserted += 1
            await conn.commit()
    print(f"Inserted/updated {inserted} patterns")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    asyncio.run(main(dry_run=args.dry_run))
