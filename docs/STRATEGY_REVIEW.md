# STRATEGY_REVIEW — honest red-team of TripWire + all-themes analysis

Internal. Not for submission. Written to be the opposite of a pitch: find what's
wrong before a judge does, then decide with evidence.

---

## PART 1 — Red-team of TripWire (what's actually wrong)

Ranked by severity. Each flaw has a fix. If we can't fix it, we say so.

### FLAW 1 (critical) — Our monetization logic is backwards
The current plan: "open-source L1–L3, license L4–L5."
- L1 is mostly **Microsoft's Prompt Shields** — not ours to monetize, and commoditized.
- L4 (behavioral anomaly) and L5 (learning classifier) are our **weakest, least-proven** layers.
- So the plan gives away the valuable, defensible parts (L2 provenance, L3 canary) and charges for the shaky parts. That's upside-down.

**Fix:** flip it. The defensible IP is the **action-layer control plane** — L2 (capability provenance) + L3 (canary/exfil tripwire) operating on *tool calls and outputs*. That's the paid core. L1 prompt-filtering is table-stakes we inherit and open-source as a funnel. See Part 2.

### FLAW 2 (critical) — We benchmark the least-novel layer
Our headline numbers measure **L1 only** (prompt in → verdict). L2/L3/L4 act on the agent's *actions/outputs*, which needs the agent in the loop — and we haven't benchmarked those. So we're proving the commodity part and asserting the novel part.

**Fix before June 30:** build the agent-in-the-loop harness and benchmark L2+L3 — *"of N exfiltration attempts, L3 caught X with 0 false positives; of M unauthorized tool calls, L2 denied Y."* That's the number that actually differentiates us.

### FLAW 3 (high) — The "novel" layer (L2) is the thinnest implementation
We *claim* capability provenance is the differentiator, but in code it's a JWT verify stub. A sharp judge will ask to see it stop a real indirect-injection tool call. Right now we can't fully demo that.

**Fix:** wire a real victim agent with 2–3 tools, mint scoped tokens on the genuine user turn, and show an injected tool-call get denied for lack of provenance. This is the single highest-leverage build task left.

### FLAW 4 (high) — We oversell L3 canaries
We wrote "catches any stolen secret." False. Canaries catch exfiltration of the *specific decoy*, probabilistically. An attacker exfiltrating real data that isn't a canary isn't caught by L3 alone.

**Fix (honesty + substance):** reframe L3 precisely — "a zero-false-positive *tripwire* that detects exfiltration attempts; paired with output taint-tracking for coverage." Add a lightweight taint check (does the output contain any value that originated from a sensitive source?) as L3b. Never claim a guarantee we don't have.

### FLAW 5 (high) — L4 is technically weak and will false-positive
Cosine(goal, action) divergence sounds smart but legit multi-step agent tasks routinely diverge from the literal goal. In production this generates noise, and noise gets the security layer turned off.

**Fix:** demote L4 from "blocker" to "risk-scorer that gates L2 strictness." Don't let it hard-block. Be honest it's heuristic. Or cut it for the prototype and list as roadmap — a smaller honest system beats a bigger hand-wavy one.

### FLAW 6 (high) — L5's learning loop is a data-poisoning hole
A security product that retrains nightly on attacker-submitted arena data can be **poisoned** by attackers to mislabel future attacks as benign. Ironic and real.

**Fix:** never auto-train on unverified arena labels. Human-in-the-loop or consensus labeling only. Frame L5 as "curated continual learning," and call out poisoning resistance as a *feature* — judges in a security theme will respect that we thought of it.

### FLAW 7 (medium) — 500ms inline latency is a real product tax
p95 ~500ms on every request (from the benchmark) is high for an inline gateway. Most teams shipping agents won't accept half a second of added latency per call.

**Fix:** tier the path. L1 patterns + L2 provenance + L3 canary are all <10ms, in-process, no network. Only call Prompt Shields / embeddings on the **fast-path miss** or by sampling. Target: p95 < 30ms for the 95% of traffic that's clearly clean. This is also a better architecture story.

### FLAW 8 (medium) — The market is crowded, not white space
Lakera, Prompt Security, HiddenLayer, Protect AI (Palo Alto), Robust Intelligence (Cisco) all play here, well-funded. "Agent security startup" is not a clean wedge.

**Fix:** our honest wedge is **agent *action* security (the control plane over tool calls), not prompt filtering** (commoditized + crowded). Most incumbents are prompt/LLM-firewall first. Provenance + canary on the tool boundary is a thinner, sharper, more defensible position. Pitch that, not "another LLM firewall."

### FLAW 9 (medium) — "We extend Prompt Shields" cuts both ways
Flatters Microsoft judges, but invites: "so isn't this a feature Microsoft absorbs in 2 releases?" (They're already shipping Entra Agent ID + Purview for AI.)

**Fix:** position as the **cross-model, cross-cloud action-control plane** that sits above any provider's prompt filter. The provenance/canary/audit layer is provider-agnostic and is where lock-in-averse enterprises want a neutral vendor. That's defensible against being absorbed.

### What's genuinely GOOD (keep, lead with these)
- **L3 canary tripwire** — zero-FP, live-demoable, judges can verify it on stage. Best demo asset.
- **L2 provenance** — the *idea* is the strongest in the project; identity-based defense that doesn't depend on detecting the attack. Just needs to be actually built.
- **The live arena + Glass Box** — genuinely differentiated demo theater; judges interact.
- **Real Azure wiring + honest benchmark + 0% FP** — credibility most teams won't have.
- **Defense-in-depth framing mapped to OWASP** — correct and well-argued.

### Verdict on TripWire
**Strong hackathon winner, flawed product — fixable.** Do NOT abandon it 8 days from prototype with a working build. **Sharpen it**: reposition around the action-layer control plane (L2+L3), build the real victim agent, benchmark the novel layers, fix the latency tiering, and tell an honest story about L4/L5. That turns it from "another LLM firewall demo" into "the neutral control plane for agent actions."

---

## PART 2 — The repositioning (one paragraph)

> **TripWire is the control plane for agent *actions*.** LLM firewalls (including
> Azure Prompt Shields) inspect text going *in*. TripWire governs what the agent is
> allowed to *do* and proves nothing sensitive leaves: every tool call must carry
> signed provenance tracing it to a real user instruction (L2), and every output is
> watched by zero-false-positive exfiltration tripwires (L3). Prompt filtering (L1)
> is table-stakes we inherit and open-source. The paid product is the action layer:
> provider-agnostic, audit-grade, and exactly what a CISO needs before letting an
> agent touch production tools.

This fixes Flaws 1, 8, 9 at once and makes the monetization, the moat, and the
anti-absorption story all consistent.

---

## PART 3 — All six themes: problem, solution, GTM, model, win-probability

Scored on the actual rubric (50% technical, 30% comms/readiness, 20% problem/market)
and on **competition density** (how many of 12,970 entrants pick it) and **Microsoft
strategic fit** (judges reward what their employer invests in).

### Theme 1 — AI at Work: Productivity & Teamwork
- **Real problem:** knowledge work drowns in context-switching; meetings/threads/docs don't connect.
- **Sharp solution:** a "decision memory" layer — captures decisions across Teams/email/docs and answers "why did we decide X, and what changed?" (not another summarizer).
- **GTM:** bottom-up, free for individuals, team plan when 3+ adopt. M365 Copilot ecosystem ride-along.
- **Model:** per-seat SaaS, $8–15/user/mo.
- **Verdict:** ❌ for *us*. Competition density is brutal (~55–65% pick this). You'd build something good and look identical to 5,000 others. Skip.

### Theme 2 — Security in the Agentic Future ← OURS
- **Problem:** agents with tools/memory are a breach waiting to happen; #1 OWASP risk; no neutral action-control plane.
- **Solution:** TripWire, repositioned per Part 2.
- **GTM:** open-source L1 + provenance SDK → developer adoption → land on one agent team → expand to org-wide policy + audit (Snyk/Lakera playbook). Design-partner 3 companies shipping agents.
- **Model:** open-core. Free: SDK + L1 + single-app. Paid: org policy, audit log, canary management, SSO — $2–5k/mo team, enterprise custom.
- **Verdict:** ✅ **Best fit for us.** Low competition density (<10% pick security), high Microsoft fit, the only theme where judges *attack the demo live*. Flaws are fixable. Stay.

### Theme 3 — Agentic Web
- **Problem:** agents that browse/transact for you are brittle and unsafe.
- **Sharp solution:** a "reliability harness" for web agents — checkpoint/rollback + verification so multi-step transactions don't half-complete.
- **GTM:** dev tool, usage-based.
- **Model:** per-action pricing.
- **Verdict:** ⚠️ Browserbase/Stagehand/OpenAI Operator have eaten the obvious version; novelty bar brutal. Skip unless you have a genuinely new reliability primitive.

### Theme 4 — AI Meets Data: From Noise to Insight
- **Real problem:** enterprises sit on messy unstructured data; "insight" needs cleaning + enrichment + a question-answering layer that's trustworthy.
- **Sharp solution:** a **trust-scored** analytics agent — every answer ships with a provenance + confidence trail (which rows, which transforms, how sure). Solves the "can I act on this AI answer?" blocker.
- **GTM:** land in one team's data stack (Fabric/Snowflake), expand by trust.
- **Model:** per-seat + compute.
- **Verdict:** ✅✅ **Strongest *business* theme** — this is where enterprise budgets actually are, and Microsoft Fabric pull is huge. Medium competition. **If we were starting fresh, this would be the #2 contender.** Interesting overlap: our "provenance + trust trail" muscle from TripWire transfers directly here.

### Theme 5 — Agent Swarms
- **Problem:** multi-agent systems are impressive in demos, chaotic in production.
- **Sharp solution:** an **orchestration observability + guardrail** layer for swarms (who called whom, cost, loops, deadlocks).
- **Verdict:** ⚠️ High technical-wow ceiling but high crash risk on stage; "5 agents talking" looks like chaos unless the control story is excellent. Adjacent to our security wedge though.

### Theme 6 — AI-Powered Production Function: Reinventing Work
- **Real problem:** software delivery (CI/CD, QA, PM) wasn't built for AI-led work.
- **Sharp solution:** an **AI-native quality gate** — an agent that reviews PRs *with* runtime/behavioral evidence, not just static diff.
- **GTM:** GitHub Marketplace, bottom-up dev adoption (huge Microsoft/GitHub fit).
- **Model:** per-repo / per-seat.
- **Verdict:** ✅ Strong Microsoft fit (GitHub), real budget, devs are the judges' peers. Medium-high competition. Solid #3 contender.

### Ranked for *winning this specific hackathon*
1. **Security (ours)** — lowest competition × highest live-demo leverage × Microsoft fit. **Stay.**
2. **AI Meets Data (trust-scored analytics)** — biggest business, strong Fabric fit, but more crowded and no live-attack theater.
3. **Production Function (AI-native quality gate)** — great GitHub fit, devs judge it well.
4. Agent Swarms / Agentic Web — higher risk, more crowded or more eaten.
5. AI at Work — do not; you vanish in the crowd.

---

## PART 4 — Decision & professional recommendation

**Do not switch themes.** 8 days to prototype, a working live demo, real Azure
wiring, and an honest benchmark already in hand. Switching throws away a
compounding lead for a theme that isn't strictly better for *winning*.

**Do sharpen TripWire** along Part 1's fixes, in this priority order (highest ROI first):
1. Build the **real victim agent + L2 provenance** demo (fixes Flaws 2,3 — the credibility core).
2. **Benchmark L2+L3 agent-in-the-loop** (the number that actually differentiates).
3. **Reposition** all collateral to "action-layer control plane" (fixes 1,8,9 — free, just messaging).
4. **Latency tiering** (fast-path <30ms; fixes 7 — better architecture story).
5. **Honest L4/L5 framing** (fixes 4,5,6 — turn limitations into "we thought about this").

**Carry-forward insight:** the "provenance + trust trail" capability we're building
for security is the *same muscle* Theme 4 (trust-scored analytics) needs. If TripWire
places well, the natural next product is "trust trails for AI answers." That's a
real company, not just a hackathon entry.

**Business-model one-liner (professional version):**
> Open-core. Free SDK + prompt filter drives developer adoption; the paid product is
> the agent action-control plane (provenance, exfil tripwires, audit, policy) —
> provider-agnostic, priced per protected agent, sold to AppSec/platform teams. The
> wedge incumbents leave open is *action* security, not prompt filtering.
