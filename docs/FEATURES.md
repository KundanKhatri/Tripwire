# TripWire — Feature Roadmap

TripWire is the **control plane for AI agent actions**. Today it ships a 5-layer
defense pipeline (semantic firewall, capability provenance, canary tripwires,
behavioral anomaly, learning classifier). This document describes where the
product goes next — each feature anchored to a real, documented 2025–2026 problem.

> Market context: enterprise spend on agentic AI is projected at ~$200B for 2026,
> yet **88% of organizations have already experienced an agent-related security
> incident while only ~6% of security budget is allocated to agent risk.** That gap
> is the company. (Figures from public industry reporting — see _Sources_; verify
> before external/investor use.)

---

## Part A — Buildable now / near-future

### F1 · Agent Identity Ledger (Non-Human Identity for agents)
**The problem.** Agents are a new class of identity — they authenticate, hold
credentials, and act — but enterprise IAM was built for humans and service
accounts. Only ~18% of security leaders are confident their IAM can manage agent
identities; ~69% say identity management must fundamentally change.

**What we build.** Every agent gets a cryptographic identity with:
- a signed birth certificate (who created it, when, for what purpose),
- scoped capabilities (which tools, which data, which budget) — a direct
  extension of TripWire's L2 capability provenance,
- a full lifecycle: issue → rotate → suspend → revoke, with instant kill-switch,
- a tamper-evident ledger of everything the identity ever did.

**Why us.** L2 already mints scoped capability tokens. The Identity Ledger is the
system of record those tokens hang off. This turns "we check tool calls" into "we
are the identity provider for your agents."

---

### F2 · MCP Tool Firewall (tool-poisoning & supply-chain defense)
**The problem.** The Model Context Protocol (MCP) is how agents connect to tools,
and it's now a live attack surface. The first malicious MCP package hit public
registries in September 2025. **Tool poisoning** hides instructions inside tool
descriptions the model reads but the user never sees; **rug-pull** attacks
silently swap a trusted tool's behavior after approval — with no re-prompt.

**What we build.**
- Scan every tool description/metadata for hidden instructions before the agent
  is allowed to see it (reuse L1's semantic firewall on the tool surface).
- **Hash-pin** approved tools; any change forces re-approval (kills rug-pulls).
- Provenance + reputation on MCP servers (which publisher, since when, change
  history).
- Sandbox + rate-limit tool execution; canary-tag tool outputs (L3) so a poisoned
  tool can't exfiltrate.

**Why us.** Same defense primitives (semantic scan + provenance + canary), pointed
at the tool/MCP boundary instead of the user prompt. Few incumbents cover this
boundary yet.

---

### F3 · Runaway-Cost & Loop Governor (the "excessive agency" + FinOps layer)
**The problem.** Agents loop. A documented multi-agent tool ran a recursive loop
for **11 days before anyone noticed — a $47,000 API bill.** Agent paths can cost
3x at 5 steps and **30x+ at 50 steps** versus a single call. ~40% of agentic
projects are forecast to be cancelled by 2027, with runaway cost a top reason.

**What we build.**
- Real-time trajectory analysis to detect loops, oscillation, and stagnation
  (two agents ping-ponging, no net progress).
- Hard token/cost **budgets per task and per agent identity**, enforced inline.
- Circuit breaker: auto-pause + alert a human when an agent exceeds budget or
  trips a loop signal — before the bill, not after.
- Cost attribution per agent identity (ties to F1) for FinOps + chargeback.

**Why us.** This reframes "excessive agency" (OWASP LLM08) as both a security AND
a cost problem — the rare security feature with a hard-dollar ROI a CFO signs off
on. It rides on L4 (behavioral trajectory) we already model.

---

### F4 · Memory-Poisoning Shield
**The problem.** Unlike a one-shot prompt injection, **memory poisoning persists**:
an adversary implants false/malicious facts into an agent's long-term memory and
the agent recalls them in future sessions. It is one of the most insidious 2026
agent threats.

**What we build.**
- Validate and provenance-tag every write to long-term memory (who/what caused it).
- Taint-tracking: facts derived from untrusted sources are marked and cannot
  silently become "trusted."
- Quarantine + review for high-impact memory writes; staleness/conflict detection
  when a new fact contradicts a trusted one.

**Why us.** Provenance and taint are the same machinery as L2/L3, applied to the
memory boundary — the third boundary (after prompt and tool) an agent exposes.

---

### F5 · Compliance Audit Ledger (EU AI Act / governance-ready)
**The problem.** The EU AI Act's penalty phase begins August 2026; Annex III
high-risk obligations land December 2027. They require timestamped, traceable logs
of agent inputs, outputs, tool use, and full execution paths. Most teams have no
audit trail for what their agents did.

**What we build.**
- Immutable, timestamped, signed ledger of every agent action with full provenance
  (built on F1's identity ledger).
- Pre-built evidence exports for EU AI Act, SOC 2, ISO 42001.
- "Replay" any incident: exactly what the agent saw, decided, and did.

**Why us.** We already sit inline on every action — capturing the audit trail is
nearly free for us and a greenfield requirement for buyers. Compliance is the
budget line that gets approved.

---

## Part B — Visionary (2–3 year bets)

### V1 · Agent Trust Fabric (cross-org agent-to-agent trust)
As agents from different companies start transacting with each other, each needs
to verify the other is legitimate, scoped, and reputable — before acting. TripWire
becomes the **PKI + reputation bureau for non-human identities**: an agent can
present a TripWire-signed credential and trust score, and a counterparty agent can
verify it in milliseconds. Network effects: every protected agent strengthens the
fabric.

### V2 · Agent Risk Score & Insurance
TripWire's telemetry across millions of agent actions becomes an actuarial dataset.
From it we derive an **agent risk score** (like a credit score for autonomous
systems) and, with an insurance partner, **underwrite agent-caused-loss coverage**.
The data moat (Part A) becomes a financial product — the highest-margin, most
defensible endgame.

---

## How the features compound

```
            prompt boundary      tool/MCP boundary       memory boundary
                  │                     │                      │
   L1 firewall ───┤      F2 MCP firewall┤   F4 memory shield───┤
   L2 provenance ─┼── F1 Identity Ledger (system of record) ───┤
   L3 canary ─────┤                     │                      │
   L4 behavioral ─┴── F3 Cost/Loop Governor                    │
                                                               │
        Everything writes to ▶ F5 Compliance Audit Ledger
        Aggregate telemetry ▶ V2 Risk Score ▶ V1 Trust Fabric
```

Each feature reuses the same three primitives — **provenance, taint/canary, and
inline policy** — applied to the three boundaries every agent exposes (prompt,
tool, memory). That's the architectural thesis: one control plane, three
boundaries, compounding data.

---

## Sources (verify figures before external use)

- Enterprise agentic spend, market size & CAGR — industry market reports, 2026.
- 88% incident / 6% budget; 18% IAM confidence; 69% identity-change — agent
  security industry surveys, 2026.
- $47K / 11-day runaway loop; 3x–30x cost multiplier; ~40% project cancellation —
  agentic-failure analyses, 2025–2026.
- First malicious MCP package (Sep 2025); tool poisoning / rug-pull — MCP security
  research, 2025–2026.
- Memory poisoning persistence — agentic threat surveys, 2026.
- EU AI Act timeline (penalties Aug 2026; Annex III Dec 2027) & logging duties —
  EU AI Act guidance, 2025–2026.

These are real, widely-reported figures gathered from current web sources; treat
the exact numbers as directional and re-confirm primary citations before putting
them in an investor deck.
