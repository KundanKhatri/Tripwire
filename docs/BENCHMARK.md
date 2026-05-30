# BENCHMARK — TripWire defense effectiveness

Measured against a **held-out eval set** of 20 attacks + 20 benign prompts
(`packages/attack-corpus/eval_set.jsonl`) — none of these exact strings are in
the corpus the system was indexed on (30 seed patterns). Run against
**live Azure** (Prompt Shields + text-embedding-3-large).

Reproduce: `cd apps/api && set -a && source .env.local && set +a && python ../../scripts/benchmark.py`

## Representative run

| Config | Attack block | Attack caught¹ | Benign blocked² | Benign flagged³ | Latency p50 (ms) | p95 (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| No defense (baseline) | 0% | 0% | 0% | 0% | 0 | 0 |
| Azure Prompt Shields only | 75% | 75% | 0% | 0% | 504 | 613 |
| Full TripWire (L1) | 80% | 90% | 0% | 0% | 512 | 708 |

¹ *Attack caught* = blocked **or** held for review (review routes to a human / stricter model).
² *Benign blocked* = false positive (hard block on a safe prompt) — lower is better.
³ *Benign flagged* = blocked or sent to review — the soft false-positive rate.

## On run-to-run variance (read this)

Azure Prompt Shields is a hosted model and is **not perfectly deterministic** on
borderline inputs (subtle obfuscation, social-engineering framing). Across repeated
runs of this eval set we observe:

- Prompt Shields only: attack-block in the **65–75%** range
- Full TripWire (L1): attack-block **75–80%**, attack-caught **80–90%**
- Benign false-positive rate: **0% in every run observed**

So we do not claim a single hero number. The **robust, always-observed result** is:

> **Full TripWire catches strictly more attacks than Azure Prompt Shields alone, at 0% measured false-positive cost.**

The lift comes from the layers Shields doesn't have: pattern rules catch known
structural attacks instantly, and embedding similarity catches novel phrasings
that have no keyword match and that Shields rates as borderline. The gap between
"block" and "caught" (the review band) is where embedding similarity flags
suspicious-but-not-certain inputs for a human or a stricter model.

## How to read this

- **Attack block** is the headline: fraction of real attacks stopped outright.
- **Benign blocked** is the cost: a defense that blocks safe traffic is useless. We report it next to the block rate, always — a high block rate with a high false-positive rate is not a win.
- We deliberately report **both** "block" and "caught" so the review-band is visible, not hidden inside an inflated block number.

## Methodology notes

- Baseline is definitionally 0% block / 0% FP (no defense applied) — it anchors the comparison.
- This measures **L1** only (the layers acting on the inbound prompt). L2 (provenance), L3 (canary), and L4 (behavioral) act on the agent's *actions/outputs* and are evaluated separately with the agent in the loop.
- Latency is wall-clock per call **including the Azure round-trip from a dev machine in a different region** (the API resource is in Southeast/Korea while the caller is in India). In-region production p95 is materially lower; the relative comparison between configs is what matters here.
- The eval set is small by hackathon necessity. The methodology scales unchanged to the full corpus for the June 30 final round.
