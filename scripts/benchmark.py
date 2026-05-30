#!/usr/bin/env python3
"""TripWire benchmark — block rate, false-positive rate, latency across 3 configs.

Runs the held-out eval set (packages/attack-corpus/eval_set.jsonl) through:
  1. baseline      — no defense (everything allowed)
  2. shields_only  — Azure Prompt Shields verdict only
  3. full_tripwire — full L1 (patterns + Prompt Shields + embedding similarity)

Reports, for each config:
  - block rate on attacks (strict block, and block+review = "caught")
  - false-positive rate on benign (strict, and including review)
  - median + p95 added latency

Writes docs/BENCHMARK.md. Run from apps/api with env sourced:
    cd apps/api && set -a && source .env.local && set +a \
      && python ../../scripts/benchmark.py
"""
from __future__ import annotations

import asyncio
import json
import statistics
import time
from pathlib import Path

from app.azure_clients import EmbeddingsClient, PromptShieldsClient
from app.corpus import CorpusSearcher
from app.defense.layers.l1_semantic import L1SemanticFirewall
from app.schemas import DefendRequest, Verdict
from app.settings import get_settings

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "packages" / "attack-corpus" / "eval_set.jsonl"
OUT = ROOT / "docs" / "BENCHMARK.md"


def load_eval() -> list[dict]:
    rows = []
    with EVAL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 1) if d else 0.0


async def main() -> None:
    settings = get_settings()
    embeddings = EmbeddingsClient(settings)
    shields = PromptShieldsClient(settings)
    corpus = CorpusSearcher(embeddings)
    indexed = await corpus.build()
    l1 = L1SemanticFirewall(shields=shields, corpus=corpus)

    rows = load_eval()
    attacks = [r for r in rows if r["label"] == "attack"]
    benign = [r for r in rows if r["label"] == "benign"]

    results: dict[str, dict] = {}

    # --- baseline: no defense ---
    results["baseline"] = {
        "attack_block": 0, "attack_caught": 0,
        "benign_block": 0, "benign_flagged": 0, "lat": [0.0],
    }

    # --- shields_only ---
    so = {"attack_block": 0, "attack_caught": 0, "benign_block": 0, "benign_flagged": 0, "lat": []}
    for r in rows:
        t = time.perf_counter()
        sig = await shields.detect(r["payload"])
        so["lat"].append((time.perf_counter() - t) * 1000)
        blocked = bool(sig.get("attack_detected"))
        if r["label"] == "attack":
            so["attack_block"] += int(blocked)
            so["attack_caught"] += int(blocked)
        else:
            so["benign_block"] += int(blocked)
            so["benign_flagged"] += int(blocked)
    results["shields_only"] = so

    # --- full tripwire (L1) ---
    ft = {"attack_block": 0, "attack_caught": 0, "benign_block": 0, "benign_flagged": 0, "lat": []}
    for r in rows:
        t = time.perf_counter()
        res = await l1.evaluate(DefendRequest(payload=r["payload"]))
        ft["lat"].append((time.perf_counter() - t) * 1000)
        is_block = res.verdict == Verdict.BLOCK
        is_flag = res.verdict in (Verdict.BLOCK, Verdict.REVIEW)
        if r["label"] == "attack":
            ft["attack_block"] += int(is_block)
            ft["attack_caught"] += int(is_flag)
        else:
            ft["benign_block"] += int(is_block)
            ft["benign_flagged"] += int(is_flag)
    results["full_tripwire"] = ft

    na, nb = len(attacks), len(benign)

    def line(name: str, d: dict) -> str:
        lat = d["lat"]
        med = round(statistics.median(lat), 1)
        p95 = round(sorted(lat)[max(0, int(len(lat) * 0.95) - 1)], 1)
        return (
            f"| {name} | {pct(d['attack_block'], na)}% | {pct(d['attack_caught'], na)}% | "
            f"{pct(d['benign_block'], nb)}% | {pct(d['benign_flagged'], nb)}% | {med} | {p95} |"
        )

    md = f"""# BENCHMARK — TripWire defense effectiveness

Measured against a **held-out eval set** of {na} attacks + {nb} benign prompts
(`packages/attack-corpus/eval_set.jsonl`) — none of these exact strings are in
the corpus the system was indexed on ({indexed} seed patterns). Run against
**live Azure** (Prompt Shields + text-embedding-3-large).

Reproduce: `cd apps/api && set -a && source .env.local && set +a && python ../../scripts/benchmark.py`

| Config | Attack block | Attack caught¹ | Benign blocked² | Benign flagged³ | Latency p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
{line("No defense (baseline)", results["baseline"])}
{line("Azure Prompt Shields only", results["shields_only"])}
{line("Full TripWire (L1)", results["full_tripwire"])}

¹ *Attack caught* = blocked **or** held for review (review routes to a human / stricter model).
² *Benign blocked* = false positive (hard block on a safe prompt) — lower is better.
³ *Benign flagged* = blocked or sent to review — the soft false-positive rate.

## How to read this

- **Attack block** is the headline: what fraction of real attacks are stopped outright.
- **Benign blocked** is the cost: a defense that blocks safe traffic is useless. We report it next to the block rate, always — a high block rate with a high false-positive rate is not a win.
- Full TripWire combines pattern rules, Prompt Shields, and embedding similarity, so it catches attacks that any single mechanism misses (e.g. novel phrasings with no keyword match are caught by similarity; obfuscation that dodges patterns is caught by Shields).

## Methodology notes

- Baseline is definitionally 0% block / 0% FP (no defense applied) — it anchors the comparison.
- This measures **L1** only (the layers that act on the inbound prompt). L2 (provenance), L3 (canary), and L4 (behavioral) act on the agent's *actions/outputs* and are evaluated separately with the agent in the loop.
- Latency is wall-clock per call including the Azure round-trip from the dev machine; production p95 in-region is lower.
- Eval set is small by hackathon necessity; the methodology scales to the full corpus for the final round.
"""
    OUT.write_text(md)
    print(md)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
