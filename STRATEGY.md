# STRATEGY — How TripWire wins ₹3,00,000

Internal document. Not for submission.

## The rubric (what we are actually being scored on)

| Criterion | Weight | What it really tests |
| --- | --- | --- |
| AI Integration & Intelligence Design | 25% | Are you using AI deeply, not as a wrapper? Multi-model, evals, prompting craft, agents? |
| System Architecture & Engineering Quality | 25% | Is the system real? Distributed, observable, deployable, secure, scalable? |
| Communication, Presentation & UX | 15% | Can a non-technical judge follow it? Is the demo crisp? Does the UI not look like a hackathon? |
| Prototype Readiness & Scalability | 15% | Does it actually run? Live URL? Doesn't crash? Could it handle real load? |
| Problem Depth & Product Clarity | 10% | Do you understand the threat model precisely, with sources? |
| Market Understanding & Product Fit | 10% | Who buys this, why, and how big is the market? |

**50% of the score is technical depth.** This is where most of the 12,970 registrants will be weak. We weaponize that.

## Why we win each criterion

### AI Integration & Intelligence Design — 25%
Most teams will call `gpt-4o` once and call it done. We use:
- **GPT-4.1** for the Glass Box explainer (reasoning trace generation, low call volume, high quality)
- **o4-mini** for hot-path classification at L1 (cheap, fast, high accuracy on injection detection)
- **Azure Prompt Shields** as a baseline L1 layer we extend
- **Azure AI Content Safety Groundedness** as part of L4 anomaly detection
- **A fine-tuned distil-class model** for L5 — trained on our growing corpus, deployed as an Azure ML endpoint
- **Azure AI Foundry Evaluation SDK** to produce a benchmark report against published attack corpora (HackAPrompt, OWASP LLM Top 10 examples, Anthropic-published patterns)

This is multi-model orchestration with a real evaluation harness. Almost no team will go this deep.

### System Architecture & Engineering Quality — 25%
A real distributed system, not a notebook:
- FastAPI defense engine on Container Apps (autoscale)
- Next.js arena UI on Static Web Apps
- Postgres + pgvector on Cosmos for corpus + embedding search
- SignalR for the real-time leaderboard
- Bicep IaC for one-command provisioning (`azd up`)
- OpenTelemetry traces flowing into Application Insights
- Containerized, GitHub Actions CI, security scanning enabled
- Architecture diagram in [ARCHITECTURE.md](ARCHITECTURE.md) using Mermaid

The pitch slide reads: "TripWire is production-grade Azure-native from day one — not a Streamlit demo in a trench coat."

### Communication, Presentation & UX — 15%
- The arena UI is Tailwind + shadcn + Framer Motion. Looks like a SaaS product, not a hackathon.
- The Glass Box is the killer UX element — every blocked attack opens a trace card that animates the layer-by-layer defense.
- Pitch video: 3 minutes, exactly. Opens with a live attack getting blocked. No talking-head intro.
- Pitch deck: 8 slides max. Problem → Stakes → Demo → Architecture → Benchmark → Moat → Market → Ask.

### Prototype Readiness & Scalability — 15%
- Public live URL by June 7.
- Load tested to 100 RPS (Azure Load Testing).
- Zero secrets in the repo (per the rules — they will check).
- Health checks, readiness probes, graceful degradation if Prompt Shields rate-limits.

### Problem Depth & Product Clarity — 10%
- Threat model document citing: OWASP LLM Top 10 (LLM01: Prompt Injection, LLM02: Insecure Output Handling, LLM07: Insecure Plugin Design), Anthropic's red-team research, Microsoft's own Prompt Shields paper, Lakera's published taxonomies.
- Specific attack scenarios mapped to specific TripWire layers in a matrix.
- We do not say "TripWire stops prompt injection" — we say "TripWire stops these 14 named attack classes via these 5 mechanisms, with these measured block rates."

### Market Understanding & Product Fit — 10%
- TAM: agent security is a new sub-segment of API security ($14B in 2025, growing 30% YoY). Gartner predicts agent identity will be a top-3 security investment by 2027.
- Buyer: Director of AppSec or CISO at any company shipping agentic features (SaaS, fintech, healthcare).
- Wedge: open-source the L1-L3 layers (Apache-2.0), license the L4-L5 enterprise tier.
- This is how Snyk, Lakera, and Promptfoo were built. Defensible playbook.

## What we are NOT doing (and why)

- **Not Streamlit.** Production-quality UI is part of the moat.
- **Not single-model.** Multi-model orchestration scores higher on AI Integration.
- **Not "AI inbox triage" or any AI at Work product.** ~60% of teams will pick that theme. We pick Security because (a) fewest teams will, and (b) it lets judges interact with the live demo.
- **Not a slide-heavy pitch.** First 30s of the pitch is the live attack arena. Everything else is footnotes.

## The contrarian moves (the 9X gap)

| What every other team does | What TripWire does |
| --- | --- |
| One LLM call | 3-model orchestration with role-specialized models |
| Pattern matching | 5-layer defense in depth with a learning loop |
| Slides claim "secure" | Live benchmark numbers from Azure AI Foundry evals |
| "Try this prompt" demo | Live red-team arena with leaderboard via SignalR |
| Streamlit | Bicep + Container Apps + Static Web Apps + IaC |
| No real corpus | Curated 2000+ attack corpus with provenance to public sources |
| Hand-waved market | Named buyer, named comparable companies, named TAM |

## The risks we accept

- **IP assignment to Microsoft.** Per rules, we lose ownership at submission. Acceptable — prize + resume value + open-source community matters more.
- **Azure cost.** Manageable if we stay on standard tiers + use o4-mini for hot path. See [AZURE_SETUP.md](AZURE_SETUP.md) cost ceiling.
- **Live demo risk.** Mitigated by (a) controlled-interactive demo style, (b) pre-recorded backup loop on a hidden tab.

## How we beat the field

We are not the cleverest idea in the room. We are the most **executed** idea in the room. The team that ships a real, deployed, multi-layered, observable, IaC-provisioned, benchmarked product with a Tailwind UI and a live attack arena beats the team with the more "interesting" idea every time at Microsoft-judged hackathons. Microsoft engineers respect engineering.

We are betting on craft, not novelty. The novelty is in the architecture, not the pitch.
