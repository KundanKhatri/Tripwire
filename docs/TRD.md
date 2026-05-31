# TripWire — Technical Requirements Document (TRD)

Companion to [ARCHITECTURE.md](../ARCHITECTURE.md) (system design) and
[PRD.md](PRD.md) (product). This doc specifies the *how* at component level.

## 1. System overview

TripWire is an inline control plane. Requests flow:

```
client/agent ─▶ Edge (TLS) ─▶ Defense API (FastAPI, Azure Container Apps)
                                  │
              ┌───────────────────┼─────────────────────────────┐
              ▼                   ▼                              ▼
        L1 Semantic        L2 Provenance / L3 Canary       L4/L5 (async)
        (Prompt Shields,    (in-process, <10ms)            (anomaly, classifier)
         embeddings,                                         │
         pgvector)                                           ▼
                                                      Trace Composer
                                          (verdict + per-layer reasons + GPT explain)
                                                            │
                                          Cosmos pgvector (corpus, traces, canaries)
                                          App Insights (OTel)   SignalR (live arena)
```

## 2. Components & responsibilities

| Component | Tech | Responsibility |
| --- | --- | --- |
| Defense API | FastAPI / Python 3.11 | orchestrate pipeline, expose `/defend`, `/agent/*` |
| L1 Semantic Firewall | regex bank + Azure Content Safety Prompt Shields + Azure OpenAI embeddings | detect known/novel injection at the prompt boundary |
| Corpus index | pgvector (Cosmos for PostgreSQL); in-memory cosine for prototype | similarity search vs. attack corpus |
| L2 Provenance Authority | HMAC (python-jose); key in Key Vault | mint/verify scoped capability tokens |
| L3 Canary engine | in-process | mint decoys, scan tool args + outputs |
| Guarded Toolbox | Python | enforce L2+L3 on every tool invocation |
| L4 Behavioral | Azure OpenAI embeddings + Content Safety Groundedness | goal/action divergence risk score (non-blocking) |
| L5 Classifier | Azure ML endpoint (roadmap) | curated, human-in-loop continual learning |
| Trace store | Cosmos for PostgreSQL | immutable defense traces (audit basis, F5) |
| Arena UI | Next.js 14, Tailwind, Framer Motion; Azure Static Web Apps / GitHub Pages | live attack demo + Glass Box |
| Realtime | Azure SignalR | live leaderboard |
| Telemetry | OpenTelemetry → App Insights | traces, latency, decisions |
| IaC | Bicep + `azd` | one-command provisioning |

## 3. Key technical decisions

- **Dual auth** (API key for dev, managed identity for prod) on all Azure clients.
- **Graceful degradation:** any Azure call failure returns a safe partial result;
  the pipeline never hard-fails on a dependency.
- **Short-circuit + concurrency:** L1→L2→L3 sequential with early block; L4/L5 run
  concurrently. Most attacks die at L1, so median latency ≈ L1 only.
- **Fast path (target):** patterns + provenance + canary are all in-process; clean
  traffic that matches no pattern can skip network calls or sample them, holding
  p95 < 30ms. Azure calls reserved for suspicious/sampled traffic.
- **Provenance is identity-based, not detection-based:** an injected tool call is
  denied because it lacks a token chain to a real user turn — independent of
  whether we recognize the attack text.
- **Provider-agnostic core:** Azure today (hackathon requirement); the primitives
  (provenance, canary, policy) are cloud/model-neutral by design.

## 4. Data model (Postgres + pgvector)

```sql
attack_patterns(id, attack_type, owasp_category, payload, embedding vector(3072), severity)
defense_traces(id, request_id, payload, verdict, layers jsonb, explanation, created_at)  -- audit basis
canaries(id, token, request_id, expires_at)
arena_attempts(id, handle, payload, verdict, score, trace_id, created_at)
-- roadmap: agent_identities, capability_grants, audit_ledger (F1/F5)
```

## 5. APIs

```
POST /defend                       -> layered verdict + trace
POST /agent/demo/indirect-injection-> victim-agent scenario (L2/L3 in action)
GET  /status                       -> corpus/pipeline health
GET  /trace/{id}                   -> full trace (audit)
POST /arena/attempt, GET /arena/leaderboard
GET  /healthz /readyz
```

## 6. Security & compliance

- No secrets in repo; `.env.local` gitignored; CI secret scan.
- Signing keys isolated in the provenance authority / Key Vault.
- Audit trail (defense_traces) is the basis for the F5 compliance ledger
  (timestamped, signed, replayable) — EU AI Act / SOC2 aligned.
- Threat-model coverage mapped to OWASP LLM Top 10 in ARCHITECTURE.md.

## 7. Performance & scale targets

| Metric | Target |
| --- | --- |
| Clean-traffic p95 (fast path) | < 30 ms |
| Full-pipeline p95 | < 250 ms |
| Throughput (prototype) | 100 RPS on Container Apps consumption |
| Availability | 99.9% (prod), degrade-open on dependency loss |

## 8. Testing

- Unit: L1 pattern bank; L2 token scoping; L3 canary on args/outputs; full
  victim-agent scenario asserts no breach. (13 tests green.)
- Eval: held-out attack/benign set → block rate + FPR + latency (BENCHMARK.md).
- Live verification: `scripts/verify_azure.py` proves embeddings + Prompt Shields.

## 9. Roadmap (engineering)

1. Fast-path latency tiering (<30ms) + sampling of Azure calls.
2. F2 MCP Tool Firewall (scan + hash-pin + sandbox).
3. F3 Cost/Loop Governor (trajectory loop detection + budgets).
4. Persist traces to Cosmos; build F5 audit exports.
5. F1 Identity Ledger; F4 Memory Shield; L5 classifier (human-in-loop).
