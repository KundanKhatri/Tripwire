# PROVISIONING_LOG — real Azure state (Azure for Students)

Live record of what is actually provisioned, the constraints discovered, and the decisions taken. Updated as infrastructure changes.

## Subscription reality

- **Subscription:** Azure for Students (`aa680940-8dbe-495d-bcbd-169bb88a9958`), $100 credit
- **Region policy (hard constraint):** policy `b86dabb9...` (`Allowed resource deployment regions`) restricts deployments to: **austriaeast, koreacentral, southeastasia, uaenorth, malaysiawest**. East US / East US 2 are blocked → this is the real cause of the portal's `RequestDisallowedByAzure` and Foundry failures.
- **Chat-model quota:** gpt-4o and gpt-4o-mini have **0 real-time TPM quota** on this subscription in the allowed regions (regional `Standard` SKU not offered; `GlobalStandard` quota = 0). Mainstream GPT chat models are effectively unavailable.
- **What IS available (verified quota):**
  - `OpenAI.Standard.text-embedding-3-large` — 350 TPM (southeastasia & koreacentral)
  - `AIServices.GlobalStandard.gpt-oss-120b` — **5000 TPM** (koreacentral) ← open-weight OpenAI model via Azure AI Foundry MaaS
  - `AIServices.GlobalStandard.MaaS` — 600 TPM (koreacentral) ← serverless models (Llama, Mistral, etc.)
  - `OpenAI.GlobalBatch.gpt-35-turbo` — 50 (batch only)

## Provisioned resources

| Resource | Name | Region | Kind | Status |
| --- | --- | --- | --- | --- |
| Resource group | `rg-tripwire` | eastus (metadata) | — | ✅ |
| Azure OpenAI | `aoai-tripwire` | southeastasia | OpenAI | ✅ |
| └ deployment | `text-embedding-3-large` (Standard, 30) | — | — | ✅ **verified** |
| Azure OpenAI | `aoai-tripwire-kc` | koreacentral | OpenAI | ✅ (empty, reserved) |
| Content Safety | `cs-tripwire` | koreacentral | ContentSafety | ✅ **verified** |

## Verification (run `scripts/verify_azure.py`)

```
[EMBEDDINGS] OK dim=3072 model=text-embedding-3-large
[PROMPT SHIELDS] ATTACK: attackDetected=True
[PROMPT SHIELDS] BENIGN: attackDetected=False
RESULT: ALL CHECKS PASSED ✓
```

Both core defense AI services are live and behaving correctly. The Microsoft AI stack requirement is satisfied with working services, not mocks.

## Decision: chat / victim-agent model

Because gpt-4o* are quota-zero, the victim agent + Glass Box explainer will use **`gpt-oss-120b` via Azure AI Foundry (AIServices MaaS)** in koreacentral, where we have 5000 TPM. This is a *stronger* story than gpt-4o-mini: it is a current (2025) open-weight OpenAI model served natively on Microsoft's stack. Deployment is the next infra step (requires an `AIServices` kind resource + serverless/MaaS deployment).

Fallback if MaaS deployment is blocked: the template-based explainer in `apps/web/src/lib/localEngine.ts` already produces human-readable trace explanations, so the demo is never blocked on the chat model.

## Live arena + benchmark (2026-05-30)

- **Arena live:** https://kundankhatri.github.io/Tripwire/ (GitHub Actions CI/CD, auto-deploys on push). Static export, real client-side L1 blocking via the local mirror.
- **API verified on live Azure:** `/defend` blocks novel (no-pattern) attacks via Prompt Shields + embedding similarity; allows benign. See `scripts/verify_azure.py`.
- **Benchmark (`docs/BENCHMARK.md`):** Full TripWire 90% attack-block / 95% caught / 0% hard FP vs 70% for Prompt-Shields-only. Held-out eval set, live Azure.
- **Container Apps deploy:** attempted via `az containerapp up` (koreacentral). Interrupted mid ACR-build; core AI resources unaffected. Retry pending — next step is a clean ACA deploy so the live arena routes through the Azure pipeline.

## Cost posture

Embeddings + Content Safety are the only metered services running. At demo volumes this is a few dollars. gpt-oss-120b at 5000 TPM is generous headroom. Well within $100.
```
az consumption usage list --top 5 -o table   # check before bed
```
