# TripWire — Product Requirements Document (PRD)

Status: living document. Scope: the control plane for AI agent actions.

## 1. Vision & goals

Make it safe to give an AI agent real power. TripWire sits inline between an agent
and the world (prompts in, tools/MCP, memory, outputs) and enforces who the agent
is, what it may do, and proves nothing harmful happens — with a full audit trail.

**Success metrics (product):**
- Attack block rate on a held-out injection set, reported with false-positive rate.
- Zero false positives on the provenance + canary layers (hard guarantee).
- Added p95 latency on clean traffic < 30ms (fast path).
- Time-to-first-value: a dev protects one agent in < 15 minutes.

## 2. Users & personas

| Persona | Need | TripWire value |
| --- | --- | --- |
| **AI/platform engineer** (champion) | ship an agent without it getting jailbroken or looping | drop-in SDK; arena to prove it |
| **AppSec / CISO** (buyer) | governance, audit, risk reduction for autonomous systems | policy, identity ledger, audit module |
| **FinOps / eng lead** | stop runaway agent bills | cost/loop governor with hard budgets |
| **Compliance officer** | EU AI Act / SOC2 evidence | one-click audit exports |

## 3. User stories (prioritized)

**P0 — must have (now):**
- As an engineer, I send a user prompt + agent context to `/defend` and get a
  layered verdict (allow/review/block) with a reason, in < 250ms.
- As an engineer, my agent's tool calls require a capability token scoped to the
  user's actual request; injected tool calls are denied (L2).
- As a security lead, any decoy secret (canary) that tries to leave the boundary
  is blocked with certainty and logged (L3).
- As anyone, I can attack a live agent in the arena and watch every layer decide
  (the Glass Box).

**P1 — next:**
- As a platform owner, every tool/MCP server is scanned + hash-pinned; a changed
  tool forces re-approval (F2).
- As a FinOps owner, I set a per-task/per-agent token budget; loops auto-pause
  before overspend (F3).

**P2 — enterprise:**
- As a security admin, every agent has a managed identity with lifecycle + kill
  switch (F1).
- As a compliance officer, I export a signed, timestamped audit trail for any
  incident (F5).
- As an admin, writes to agent long-term memory are provenance-checked and
  quarantined if untrusted (F4).

## 4. Functional requirements (current build)

| ID | Requirement | Status |
| --- | --- | --- |
| FR-1 | `POST /defend` runs the 5-layer pipeline, returns layered trace | ✅ |
| FR-2 | L1 = pattern rules + Azure Prompt Shields + embedding similarity | ✅ live |
| FR-3 | L2 = HMAC capability tokens; tools deny calls lacking scope | ✅ tested |
| FR-4 | L3 = canary mint + scan on tool args and outputs | ✅ tested |
| FR-5 | Victim-agent demo: indirect injection blocked end-to-end | ✅ tested |
| FR-6 | Glass Box trace UI (per-layer verdict, latency, reason) | ✅ live |
| FR-7 | Arena works with zero backend (local mirror) for demo resilience | ✅ live |
| FR-8 | L4 behavioral anomaly (risk-scorer, non-blocking) | ⏳ heuristic |
| FR-9 | L5 learning classifier (curated, human-in-loop) | ⏳ roadmap |

## 5. Non-functional requirements

- **Latency:** clean-traffic fast path (patterns + provenance + canary) < 30ms p95;
  full path (Azure calls) < 250ms p95.
- **Reliability:** graceful degradation — if an Azure dependency is down, the
  pipeline continues on local layers and marks the trace accordingly.
- **Security:** no secrets in repo; keys in Key Vault / managed identity; signing
  keys never leave the provenance authority.
- **Privacy:** synthetic demo data only; customer data never used to train without
  explicit, verified consent.
- **Observability:** OpenTelemetry traces; every decision is reconstructable.

## 6. Out of scope (for now)

- Acting as the agent framework itself (we secure agents, not build them).
- Model hosting (we're provider-agnostic).
- Network-layer firewalling (we operate at the agent action layer).

## 7. Release criteria (prototype → GA)

- Prototype (done): live arena, live Azure L1, tested L2/L3, honest benchmark.
- Beta: F2 + F3 shipped, 3 design partners in production, SOC2 in progress.
- GA: F1 + F5, SLA, marketplace listing, reference customers.
