# BENCHMARK — TripWire defense effectiveness

Measured against a **held-out eval set** of 20 attacks + 20 benign prompts
(`packages/attack-corpus/eval_set.jsonl`) — none of these exact strings are in
the corpus the system was indexed on (30 seed patterns). Run against
**live Azure** (Prompt Shields + text-embedding-3-large).

Reproduce: `cd apps/api && set -a && source .env.local && set +a && python ../../scripts/benchmark.py`

| Config | Attack block | Attack caught¹ | Benign blocked² | Benign flagged³ | Latency p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| No defense (baseline) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0 | 0.0 |
| Azure Prompt Shields only | 65.0% | 65.0% | 0.0% | 0.0% | 489.5 | 517.3 |
| Full TripWire (L1) | 65.0% | 75.0% | 0.0% | 0.0% | 496.2 | 609.8 |

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
