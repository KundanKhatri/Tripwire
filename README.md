<div align="center">

# 🛡️ TripWire

### The control plane for AI agent actions

**Live demo → [kundankhatri.github.io/Tripwire](https://kundankhatri.github.io/Tripwire/)**

Stop prompt injection, tool poisoning, data exfiltration, and runaway agents —
at the action layer, on Azure.

*Built for Microsoft Build AI 2026 · Theme: Security in the Agentic Future*

</div>

---

## The problem

Enterprises are giving AI agents real power — to read data, call tools, spend
money, and act autonomously. But **88% of organizations have already had an
agent-related security incident, while only ~6% of security budget covers agent
risk.** Agents get hijacked by hidden instructions, poisoned tools, and corrupted
memory; they loop and burn five-figure bills; and almost no one has an audit trail
of what their agents did.

LLM firewalls inspect the text going *in*. **Nobody governs what the agent is
allowed to *do* — and proves nothing harmful leaves.** That's TripWire.

## What it does

TripWire sits inline between your agent and the world, across the **three
boundaries every agent exposes** — the prompt, the tools/MCP, and the memory —
and enforces a 5-layer defense pipeline:

| Layer | Name | What it does |
| :---: | --- | --- |
| **L1** | Semantic Firewall | Pattern rules + Azure Prompt Shields + embedding similarity to a known-attack corpus |
| **L2** | Capability Provenance | Every tool call must carry a signed token scoped to the real user request. Injected calls have no authority — denied. |
| **L3** | Canary Tripwires | Decoy secrets seeded into context; if one ever leaves, it's proof of exfiltration. Zero false positives. |
| **L4** | Behavioral Anomaly | Scores when the agent's actions diverge from the user's goal (goal hijack). |
| **L5** | Learning Classifier | Curated, human-in-the-loop model that improves from real attacks. |

The standout: **L2 + L3 stop the attacks an LLM firewall can't** — like indirect
injection, where the user's request is benign and the attack hides in
tool-returned content. We don't try to *recognize* every attack; we deny it
*authority* and catch the *theft*.

## See it work

The repo includes a victim-agent demo where an indirect prompt injection tries to
read a secret file and email it to an attacker. The user only authorized
"summarize a document" — so every malicious tool call is denied for lack of
provenance:

```
[plan]    User asked to summarize a document.
[tool]    Agent reads the document (authorized).
[blocked] Injection → read_file.  L2 blocked: not in granted scope [read_document]
[blocked] Injection → send_email. L2 blocked: not in granted scope [read_document]
[final]   Attack neutralized. Nothing sensitive left the boundary.
```

Try attacks yourself in the **[live arena](https://kundankhatri.github.io/Tripwire/)** —
every payload runs the full pipeline and the Glass Box shows each layer's decision.

## Where it's going

A control plane, not a single feature. See **[docs/FEATURES.md](docs/FEATURES.md)**:

- **F1 · Agent Identity Ledger** — cryptographic identity + lifecycle for every agent (NHI).
- **F2 · MCP Tool Firewall** — defeat tool poisoning & rug-pulls (scan + hash-pin + sandbox).
- **F3 · Cost & Loop Governor** — kill runaway agents before the $47K bill.
- **F4 · Memory-Poisoning Shield** — provenance + taint for long-term agent memory.
- **F5 · Compliance Audit Ledger** — EU AI Act / SOC2-ready signed action trail.
- **V1/V2 · Trust Fabric & Agent Risk Score** — the cross-org network and data moat.

## Architecture

Azure-native, provider-agnostic core. See **[ARCHITECTURE.md](ARCHITECTURE.md)**
and **[docs/TRD.md](docs/TRD.md)**.

- **Azure OpenAI** (`text-embedding-3-large`) — similarity + anomaly
- **Azure AI Content Safety — Prompt Shields** — L1 baseline (verified live)
- **Azure Container Apps** — defense API (FastAPI)
- **Azure Cosmos DB for PostgreSQL (pgvector)** — corpus + immutable traces
- **Azure Static Web Apps / SignalR** — arena UI + live leaderboard
- **Bicep + `azd`** — one-command provisioning

## Benchmarks

Measured against a held-out eval set on live Azure. We report block rate **with**
false-positive rate, always — see **[docs/BENCHMARK.md](docs/BENCHMARK.md)**.
Headline: Full TripWire catches strictly more attacks than Prompt-Shields-only at
**0% measured false-positive cost**; the provenance and canary layers are
zero-false-positive by construction.

## Run it locally

```bash
# API (defense engine)
cd apps/api && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload          # http://localhost:8000/docs

# Web (arena UI)
cd apps/web && npm install && npm run dev   # http://localhost:3000
```

The arena runs with **zero backend** via a local defense mirror, so the demo
never breaks; point `NEXT_PUBLIC_API_BASE` at the API to use the live Azure
pipeline.

## Repo layout

```
apps/api        FastAPI defense engine (L1–L5, victim agent, provenance, canary)
apps/web        Next.js arena UI + Glass Box trace viewer
packages/        attack corpus (OWASP-mapped) + pgvector schema + loader
infra/bicep      one-command Azure provisioning
docs/            FEATURES, BUSINESS_PLAN, PRD, TRD, BENCHMARK, ARCHITECTURE
scripts/         live-Azure verification + benchmark
```

## Business

TripWire is built to be a company. Full plan in
**[docs/BUSINESS_PLAN.md](docs/BUSINESS_PLAN.md)**: open-core model, bottom-up
GTM, three-year roadmap, and the data → identity → compliance → network moat.

## AI tools used

Disclosed per hackathon rules in **[AI_TOOLS_DISCLOSURE.md](AI_TOOLS_DISCLOSURE.md)**.

## Team

| Name | Role | Contact |
| --- | --- | --- |
| Kundan Khatri | Solo — architecture, backend, frontend, demo | kundanlm10@gmail.com |

## License

MIT (code). Built for Microsoft Build AI 2026.
