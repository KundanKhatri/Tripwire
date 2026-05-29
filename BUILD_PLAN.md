# BUILD_PLAN — Solo sprint to June 7 prototype, then to June 30 final

Today: **2026-05-29**. Prototype deadline: **2026-06-07 18:29 UTC (June 7, 11:59 PM IST)**. Net build window: **9 days**.

## Operating rules

- One in-progress task at a time. Mark complete the moment it ships.
- Public commit history from day 1 — every meaningful change is a commit with a clear message.
- No new feature on day N if day N-1 didn't ship its target.
- Cut scope before extending the day. Sleep is part of the plan, not a slack variable.
- Slack day built in (Day 8). Do not eat it early.

## Day 0 — Today (May 29) — Foundations
**Goal:** repo live, Azure credits claimed, scaffolds runnable.
- [x] Strategy locked, all top-level docs written
- [ ] Create GitHub repo `tripwire`, push initial scaffold, make public
- [ ] Claim Azure credits — Microsoft for Startups Founders Hub OR Azure for Students OR Azure free tier (whichever applies — see [AZURE_SETUP.md](AZURE_SETUP.md))
- [ ] `apps/api` runs locally with health endpoint
- [ ] `apps/web` runs locally with home page
- [ ] CI: lint + typecheck on PR

## Day 1 — May 30 — L1 Semantic Firewall + corpus seed
**Goal:** first real defense layer working end-to-end.
- [ ] Provision Azure OpenAI (`gpt-4.1` + `o4-mini` deployments) + Azure AI Content Safety
- [ ] `packages/attack-corpus`: seed 200 attack patterns across 6 OWASP LLM Top 10 categories
- [ ] L1 layer: Prompt Shields API integrated + pattern rules + embedding similarity check
- [ ] Unit tests for L1 against 50 corpus samples
- [ ] API: `POST /defend` returns layer-by-layer trace

## Day 2 — May 31 — L2 Provenance + L3 Canary tokens
**Goal:** the layers that nobody else builds.
- [ ] L2 capability provenance: HMAC-signed trace tokens, tool-call wrapper that validates before execution
- [ ] L3 canary token engine: inject decoys into agent context, monitor outbound channels (response + tool args + simulated outbound HTTP)
- [ ] Integration test: a "leaky agent" with a canary in its system prompt — show L3 catches exfil
- [ ] Trace JSON schema finalized

## Day 3 — June 1 — L4 Behavioral Anomaly
**Goal:** the layer that scores us on AI Integration.
- [ ] Goal embedding + trajectory embedding (Azure OpenAI embeddings)
- [ ] Divergence scoring + threshold tuning
- [ ] Azure AI Content Safety Groundedness API integrated as a cross-check
- [ ] 30 anomaly test cases from corpus

## Day 4 — June 2 — L5 Classifier + Foundry evaluation
**Goal:** the benchmark slide.
- [ ] Fine-tune a small classifier (DistilBERT or similar) on corpus + augmentations (train locally, deploy to Azure ML endpoint)
- [ ] Azure AI Foundry evaluation run: TripWire vs. vanilla GPT-4.1 (no defense) on a held-out injection set
- [ ] Benchmark report: % blocked, % FPR, latency by layer — markdown + chart
- [ ] If classifier underperforms vs. rules-only, ship rules-only and document the choice

## Day 5 — June 3 — Arena UI + SignalR
**Goal:** the demo loop judges will see.
- [ ] Next.js `/arena` page: textarea, submit, animated trace card on response
- [ ] `/leaderboard` with SignalR real-time push
- [ ] `/trace/[id]` Glass Box: layer cards with confidence + GPT-4.1 explainer
- [ ] Tailwind + shadcn polish pass. No raw HTML buttons.

## Day 6 — June 4 — Deploy + harden
**Goal:** judges can hit a live URL right now.
- [ ] Bicep `azd up` provisions everything from scratch in <15 min
- [ ] Container Apps deployment of API
- [ ] Static Web Apps deployment of UI
- [ ] App Insights traces flowing
- [ ] Load test to 100 RPS (Azure Load Testing) — record numbers for pitch
- [ ] Run `gitleaks` — zero secrets in repo

## Day 7 — June 5 — Threat model doc + market doc + glass-box polish
**Goal:** lock the 20% non-technical scoring (Problem Depth + Market).
- [ ] `docs/THREAT_MODEL.md` — attack class × defense layer matrix with citations to OWASP, Anthropic, Microsoft research
- [ ] `docs/MARKET.md` — TAM, buyer persona, GTM, comparable companies, named segments
- [ ] Glass Box visual polish — make the trace UI screenshot-worthy

## Day 8 — June 6 — SLACK + pitch artifacts
**Goal:** absorb any spillover, ship pitch artifacts.
- [ ] Pitch video — 3 minutes, opens with a live attack getting blocked. Recorded with Loom or OBS. Uploaded YouTube unlisted, linked in README.
- [ ] Pitch deck — 8 slides PDF. Problem → Stakes → Demo screenshot → Architecture → Benchmark → Moat → Market → Ask.
- [ ] Pre-submission checklist run from `RULES_DIGEST.md`

## Day 9 — June 7 — Submit
**Goal:** hit the deadline at T-6 hours, not T-30 minutes.
- [ ] HackerEarth submission form completed
- [ ] GitHub tag `v0.1-prototype`
- [ ] Demo URL verified up
- [ ] All checkbox items in `RULES_DIGEST.md` ✅

---

## June 8–30 — Final-stage polish window (if we advance)

If we make it past prototype, we get 23 days to:
- Expand corpus to 5000+ patterns
- Ship the learning loop: arena attacks feed nightly classifier retraining
- Add a second "victim agent" so judges can pick the agent they attack
- Publish a Substack post on the threat model — drives traffic to live URL by submission day
- Get one design partner quote ("we'd buy this") for the pitch
- Re-record pitch video with the new state of the product
- Run a final ultrareview pass on the entire codebase

## Scope cuts if behind schedule

Drop in this order:
1. L5 classifier (rules-only fallback acceptable)
2. SignalR realtime leaderboard (replace with polling, document as future work)
3. Second victim agent (single one is fine)
4. Pitch deck polish beyond 8 raw slides

Do NOT cut:
- The Glass Box trace UI (this is the differentiator)
- L3 canary tokens (this is the most novel layer)
- Live demo URL (without this we score zero on Prototype Readiness)
- Benchmark numbers (without these we are hand-waving)
