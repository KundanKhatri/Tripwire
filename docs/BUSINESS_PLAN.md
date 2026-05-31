# TripWire — Business Plan

> Numbers in this document are bottoms-up models with stated assumptions. Market
> figures are from current public reporting and are marked **[verify]** where they
> should be re-confirmed before investor or contractual use.

## 1. One-line

TripWire is the **control plane for AI agent actions** — the runtime security,
identity, and governance layer enterprises install before they let agents touch
production systems.

## 2. Problem

Enterprises are deploying autonomous agents fast, but **88% have already had an
agent security incident and only ~6% of security budget covers agent risk [verify]**.
The damage is concrete: indirect prompt injection, tool poisoning via MCP, memory
poisoning, runaway-cost loops (a documented **$47K, 11-day loop [verify]**), and no
audit trail for what agents did — right as the EU AI Act penalty phase begins
(Aug 2026 [verify]).

LLM firewalls inspect text going *in*. Nobody owns what the agent is *allowed to
do* and proves nothing sensitive leaves. That control plane is TripWire.

## 3. Solution & moat

A single inline control plane across the three boundaries every agent exposes —
**prompt, tool/MCP, and memory** — built on three reusable primitives:
provenance, taint/canary, and inline policy. (See [FEATURES.md](FEATURES.md).)

**Moat, in order of durability:**
1. **Data** — telemetry across millions of agent actions → detection models +
   an eventual agent risk score no one else has.
2. **Identity system-of-record** — once we issue agent identities, we're embedded
   in the customer's control plane (high switching cost).
3. **Audit/compliance lock-in** — we hold the legal record of agent behavior.
4. **Provider-agnostic position** — neutral across model/cloud vendors; defensible
   against any single platform "absorbing" us.

## 4. Why now

- Agent deployment crossed from pilots to production in 2025–2026.
- The attack surface (MCP, agent memory, agent identity) is brand new and growing.
- Regulation (EU AI Act) forces an audit trail on a deadline.
- Security spend is shifting toward agent risk from a near-zero base.

## 5. Market sizing (bottoms-up + top-down)

**Top-down [verify].** AI-agents market ~$10–11B (2026) → ~$47–53B (2030),
~45–50% CAGR. Agent-security is the fastest-growing sub-segment; ~$392M was funded
around RSAC 2026 alone.

**Bottoms-up (our reachable market).**
- Assume N companies run production agents and would pay for a control plane.
- 2026 design-partner phase: tens of logos.
- Serviceable target by Y3: ~3,000 companies × ~$40K average annual contract =
  ~$120M reachable ARR pool; we model capturing a low-single-digit slice (below).

| Layer | 2026 | 2030 |
| --- | --- | --- |
| TAM (all agent security) [verify] | ~$2B | ~$15–20B |
| SAM (mid-market+ running prod agents) | ~$0.5B | ~$5B |
| SOM (what we can realistically win) | ~$1–3M | ~$60–100M |

## 6. Business model — open-core

| Tier | Who | Price | What |
| --- | --- | --- | --- |
| **OSS / Free** | individual devs | $0 | SDK, L1 semantic firewall, single-agent provenance. Adoption funnel. |
| **Team** | startups, one agent team | ~$2–5K/mo | full 5-layer pipeline, MCP firewall (F2), cost governor (F3), dashboard, SSO. |
| **Enterprise** | regulated / many agents | ~$60K–250K/yr | Identity Ledger (F1), Memory Shield (F4), Compliance Audit (F5), policy, SLA, on-prem/VPC. |
| **Platform / data** | later | usage + % | Trust Fabric (V1), Risk Score & insurance (V2). |

**Revenue streams:** (1) seat/agent subscriptions, (2) usage (actions inspected),
(3) compliance/audit module, (4) later: risk-score API + insurance referral/share.

Pricing logic: priced per **protected agent**, not per seat — aligns our revenue
with the thing that's exploding (agent count), and with the value (each agent is a
risk we retire).

## 7. Go-to-market

**Motion: open-core, bottom-up → land → expand.** (The Snyk / Lakera / HashiCorp
playbook.)

1. **Developer adoption** — OSS SDK + L1 free. Win the dev who's wiring up an
   agent and just read an MCP-poisoning headline. Content + the live arena demo.
2. **Land** — one agent team adopts Team tier for a single production agent.
3. **Expand** — org-wide policy, identity ledger, audit module → Enterprise.
4. **Compliance pull** — EU AI Act deadline is the urgency lever for the audit
   module into regulated buyers (fintech, health, gov).

**Design partners (now → 2026):** 3–5 companies shipping production agents; free
in exchange for logos, feedback, and reference quotes.

**Channel (Y2+):** Microsoft / Azure marketplace; GitHub; cloud security ISV
ecosystems.

**Buyer & champion:** champion = platform/AI-eng lead feeling the pain; buyer =
Director of AppSec / CISO holding the budget and the EU AI Act risk.

## 8. Competition & positioning

Incumbents (Lakera, HiddenLayer, Noma, Prompt Security, Protect AI/Palo Alto,
Robust Intelligence/Cisco) are mostly **prompt/LLM-firewall first**. TripWire's
wedge is **agent *action* security — the control plane over tools, identity, and
memory** — the boundary they under-serve. We're provider-agnostic, which lock-in-
averse enterprises prefer over a single cloud's native feature.

## 9. Three-year roadmap

**Year 1 — Wedge & credibility.**
- Ship 5-layer pipeline + MCP Tool Firewall (F2) + Cost/Loop Governor (F3).
- OSS launch; 3–5 design partners; first 10 paying Team customers.
- Goal: prove the wedge, ~$250K–500K ARR [model].

**Year 2 — Platform & enterprise.**
- Agent Identity Ledger (F1) + Compliance Audit (F5) + Memory Shield (F4).
- First enterprise contracts; SOC2; Azure/GitHub marketplace.
- Goal: ~$3–5M ARR [model], Series A.

**Year 3 — Data moat & network.**
- Agent Risk Score (V2 alpha) + Trust Fabric (V1 pilot).
- Land-and-expand inside enterprise accounts; partner channel.
- Goal: ~$15–25M ARR [model].

## 10. Financial model (illustrative — assumptions stated)

Assumptions: Team ACV $36K, Enterprise ACV $90K; net revenue retention 120%;
sales-led for enterprise from Y2; gross margin ~80% (SaaS).

| | Y1 | Y2 | Y3 |
| --- | --- | --- | --- |
| Team customers | 10 | 45 | 120 |
| Enterprise customers | 0 | 8 | 30 |
| ARR (modeled) | ~$0.4M | ~$4M | ~$18M |
| Headcount | 5 | 18 | 45 |
| Gross margin | ~75% | ~80% | ~82% |

These are planning models, not forecasts; every input is a lever to test with
design partners. **[verify all before any external/financial use].**

## 11. The ask (template)

Raise a pre-seed/seed to fund the Year-1 wedge: ship F2+F3, land design partners,
prove the open-core funnel converts. Use of funds: ~70% engineering, ~20% GTM/dev-
rel, ~10% compliance/SOC2. (Fill amount + terms before use.)

## 12. Key risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Platform absorption (Azure/OpenAI ship native) | Provider-agnostic position; own identity + audit + cross-vendor data. |
| Crowded market | Wedge on action/tool/memory boundary, not prompt firewall. |
| Long enterprise sales cycles | OSS bottom-up land first; compliance deadline as urgency. |
| Detection false positives erode trust | Lead with zero-FP primitives (provenance, canary); ranges not hero numbers. |
| Learning-loop data poisoning | Human-in-loop labeling; never auto-train on unverified attacker data. |
