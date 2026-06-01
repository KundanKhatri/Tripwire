# HackerEarth Submission — copy-paste fields

Microsoft Build AI 2026 · Theme: Security in the Agentic Future · Solo: Kundan Khatri
Paste each block into the matching form field. Pause before the final irreversible submit.

---

## Project name
TripWire

## Tagline / one-liner (≤120 chars)
The control plane for AI agent actions — stop prompt injection, tool poisoning & data exfiltration at the action layer.

## Theme / track
Security in the Agentic Future

---

## Problem statement
Enterprises are giving AI agents real power — to read data, call tools, spend money, and act autonomously. The security model hasn't caught up. 88% of organizations have already had an agent-related security incident, yet only ~6% of security budget covers agent risk. Agents get hijacked by hidden instructions in the content they read (indirect prompt injection — the #1 OWASP agent risk), poisoned by malicious MCP tools, and looped into five-figure bills. LLM firewalls inspect the text going *in*, but nobody governs what the agent is allowed to *do* — or proves nothing harmful leaves.

## Solution / what it does
TripWire sits inline between an agent and the world, across the three boundaries every agent exposes — the prompt, the tools/MCP, and the memory — and enforces a 5-layer defense pipeline on every action:

- L1 Semantic Firewall — pattern rules + Azure AI Content Safety Prompt Shields + embedding similarity to a known-attack corpus.
- L2 Capability Provenance — every tool call must carry a signed token scoped to the real user request; injected calls have no authority and are denied.
- L3 Canary Tripwires — decoy secrets seeded into context; if one ever leaves, it's proof of exfiltration (zero false positives by construction).
- L4 Behavioral Anomaly — scores when the agent's actions diverge from the user's goal (goal hijack).
- L5 Learning Classifier — a human-in-the-loop model that improves from real attacks.

The standout: L2 + L3 stop the attacks an LLM firewall structurally can't — like indirect injection, where the user's request is benign and the attack hides in tool-returned content. We don't try to *recognize* every attack; we deny it *authority* and catch the *theft*.

---

## How AI is used / Azure AI integration
TripWire uses AI on both sides of the boundary:
- Azure OpenAI (text-embedding-3-large) embeds every inbound prompt and scores cosine similarity against a known-attack corpus in pgvector — catching novel phrasings with no keyword match.
- Azure AI Content Safety — Prompt Shields runs as the L1 baseline (a hosted jailbreak/injection classifier), verified live against the deployment.
- L4 behavioral anomaly embeds the agent's actions and scores divergence from the user's stated goal.
- A real tool-calling victim agent (gpt-oss-120b on Azure) runs the headline attack end-to-end so every layer's decision is observable — not a mock.
- L5 learning classifier: human-in-the-loop curation turns every real attack into training signal.

## Architecture / tech stack
Azure-native, provider-agnostic core. FastAPI defense engine (apps/api), Next.js 14 arena UI with a Glass Box trace viewer (apps/web), OWASP-mapped attack corpus + pgvector schema (packages/), one-command Bicep IaC (infra/).
- Azure OpenAI — embeddings (similarity + anomaly)
- Azure AI Content Safety — Prompt Shields (L1 baseline, verified live)
- Azure Container Apps — defense API
- Azure Cosmos DB for PostgreSQL (pgvector) — corpus + immutable traces
- Azure Static Web Apps / SignalR — arena UI + live leaderboard
- Bicep + azd — one-command provisioning

## Key features
- Inline 5-layer allow / review / block pipeline on every agent action, with a per-layer reason and latency.
- Capability provenance (HMAC-signed tokens) that denies injected tool calls for lack of scope.
- Canary tripwires that prove exfiltration with zero false positives.
- Live red-team arena: anyone can attack a real agent and watch every layer decide (the Glass Box).
- Honest, reproducible benchmark on a held-out eval set against live Azure.

## What makes it unique / innovation
Everyone else guards the prompt. TripWire governs the action. It's the only approach here that stops indirect prompt injection — by changing the model of trust (deny authority via provenance, catch theft via canaries) instead of trying to pattern-match every payload. Those are two layers an LLM firewall structurally cannot have, and they're the moat.

## Benchmark / results (honest)
Measured against a held-out eval set (20 attacks + 20 benign) on live Azure — none of these exact strings were in the indexed corpus. We report block rate WITH false-positive rate, always.
- Azure Prompt Shields only: ~75% attack block, 0% false positives.
- Full TripWire (L1): ~80% block / ~90% caught, 0% false positives.
Numbers vary run-to-run (Prompt Shields is a hosted, non-deterministic model). The robust, always-observed result: Full TripWire catches strictly more attacks than Prompt Shields alone, at 0% measured false-positive cost. L2/L3 are zero-FP by construction.

## What's next / roadmap
F1 Agent Identity Ledger (cryptographic NHI) · F2 MCP Tool Firewall (scan + hash-pin + sandbox) · F3 Cost & Loop Governor · F4 Memory-Poisoning Shield · F5 Compliance Audit Ledger (EU AI Act / SOC2) · V1/V2 cross-org Trust Fabric + Agent Risk Score (the data moat).

## Business potential / market
Open-core model: free OSS engine drives adoption; enterprise tier sells identity, the compliance audit ledger, and the cross-org trust fabric. The agent market is projected to grow from ~$10.8B (2026) toward ~$50B (2030); the agent-security sub-segment compounds at ~45–50%. Why now: agent deployments are exploding, EU AI Act penalties begin Aug 2026, and incumbents guard the prompt, not the action.

---

## Links
- GitHub repo: https://github.com/KundanKhatri/Tripwire
- Live demo: https://kundankhatri.github.io/Tripwire/
- Demo video (MP4): <PASTE YOUTUBE/DRIVE LINK AFTER RECORDING>
- Project deck (PDF, 10 slides): docs/TripWire_Deck.pdf (also attach the file directly)

## Team
Kundan Khatri — solo. Architecture, backend, frontend, infra, demo. kundanlm10@gmail.com

## AI tools used (disclosure, if asked)
Disclosed per hackathon rules in AI_TOOLS_DISCLOSURE.md in the repo.

---

### Submission checklist (4 required)
- [x] Public GitHub repo
- [x] Live link
- [x] Project Deck PDF (≤10 slides) — docs/TripWire_Deck.pdf
- [ ] Demo Video MP4 (≤3 min) — record using docs/DEMO_SCRIPT.md, upload, paste link above
