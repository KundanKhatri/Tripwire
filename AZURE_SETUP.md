# AZURE_SETUP — From zero to deployed, with credits, today

You have an Azure account but no credits. Here is the path of least resistance to get credits, provision everything, and stay under a sensible cost ceiling.

## ✅ Status (2026-05-29): Azure for Students, $100 credit secured

We will not pursue Founders Hub for this hackathon — $100 Student credit is enough if we stay disciplined. Cost plan revised to $25–40/month. See § Step 5.

**Known Student-sub constraints we will respect:**
- Azure OpenAI is supported but requires aka.ms/oai/access approval (~24h)
- Many regions blocked. Use **East US** first, then **Sweden Central** or **Switzerland North**. Avoid East US 2 on Student sub.
- Azure AI Foundry → Marketplace check often returns `RequestDisallowedByAzure`. Provision Azure OpenAI **directly** (skip Foundry initially). Add Foundry later only if it works.
- Claude / Anthropic / Mistral / Cohere models in the Foundry catalog go through Marketplace and will be blocked. **Use Microsoft-native models only: gpt-4o, gpt-4o-mini, text-embedding-3-large.** Better hackathon optics regardless.
- No premium Cosmos for Postgres tiers. Use **Burstable B1ms** ($12–20/mo).
- SignalR **Free tier** is sufficient (20 concurrent connections).

## Step 1 — Get credits (pick the first one you qualify for)

In rough order of how much they give you:

### Option A — Microsoft for Startups Founders Hub ($150,000 over 4 years, the big one)
- URL: https://startups.microsoft.com
- Eligibility: any individual building a startup. No incorporation required, no revenue minimum.
- Approval time: usually under a few hours, sometimes instant.
- This is the best one. Apply with a one-line pitch: "Building TripWire, a security layer for agentic AI systems, for Microsoft Build AI 2026."

### Option B — Azure for Students ($100/year, no card required)
- URL: https://azure.microsoft.com/en-us/free/students
- Requires a `.edu` / verifiable student email. If you have one, this is the easiest claim.

### Option C — Azure free trial ($200 for 30 days)
- URL: https://azure.microsoft.com/en-us/free
- Requires a credit card (no charge unless you upgrade). Universal fallback.

### Option D — Microsoft Build 2026 hackathon credits (check HackerEarth dashboard)
- HackerEarth sometimes distributes sponsor credits via the participant portal once registered. Worth checking under "Resources" or messaging support@hackerearth.com if not visible.

**Recommendation**: apply to Founders Hub (Option A) first — even if approval takes hours, while it processes use Option C ($200) so you're not blocked.

## Step 2 — Install tools

```bash
# Azure CLI
brew install azure-cli

# Azure Developer CLI (azd) — for one-shot deployments
brew tap azure/azd && brew install azd

# Bicep (auto-installs with azure-cli, but explicit:)
az bicep install

# Sign in
az login
azd auth login

# Verify subscription
az account show
```

## Step 3 — Request OpenAI access in your subscription

Azure OpenAI requires a one-time form approval. If your subscription doesn't yet have access:
- URL: https://aka.ms/oai/access
- Justification: "Hackathon project for Microsoft Build AI 2026 — prompt injection defense system requiring multi-model orchestration."
- Approval: usually under 24 hours.

Models we need deployed:
- `gpt-4.1` (or `gpt-4o` as fallback) — Standard deployment, 30K TPM is enough for hackathon
- `o4-mini` (or `gpt-4o-mini` as fallback) — Standard deployment, 60K TPM
- `text-embedding-3-large` — Standard deployment, 60K TPM

## Step 4 — Provision via Bicep (one command)

We will write the Bicep in `infra/bicep` over Day 0/1. Once written:

```bash
azd init  # already configured in our repo
azd up    # provisions everything end-to-end
```

This provisions:
- Resource group `rg-tripwire-prod`
- Azure OpenAI account + 3 model deployments
- Azure AI Content Safety resource
- Azure Cosmos DB for PostgreSQL cluster with pgvector
- Azure Container Apps environment + app for the API
- Azure Static Web App for the UI
- Azure SignalR Service (Free tier — 20 concurrent connections is enough for demo)
- Azure Key Vault
- Application Insights
- Managed identities + role assignments

## Step 5 — Cost ceiling for the $100 Student credit

Revised plan to fit $100 over the 33-day hackathon (today through June 30):

| Resource | SKU | Est. monthly cost | Notes |
| --- | --- | --- | --- |
| Azure OpenAI `gpt-4o` | Pay-as-you-go | $8–15 | Used only for Glass Box explainer (low volume) |
| Azure OpenAI `gpt-4o-mini` | Pay-as-you-go | $1–4 | Hot-path classification, very cheap |
| Azure OpenAI `text-embedding-3-large` | Pay-as-you-go | $1–3 | Corpus load is one-time; arena queries are bursty |
| Azure AI Content Safety | F0 (Free) → S0 | $0–10 | **Start on F0 free tier (5K calls/mo) — sufficient for prototype** |
| Cosmos for Postgres | Burstable B1ms (single node) | $12–18 | Pause overnight if idle to save |
| Container Apps | Consumption | $2–8 | Scale to zero on idle |
| Static Web Apps | Free | $0 | |
| SignalR | Free | $0 | 20 concurrent connections is fine |
| Key Vault | Standard | $0–1 | |
| App Insights | First 1GB/mo free | $0–2 | |
| **Total** | | **$25–40/month** | Comfortably fits $100 over 33 days |

Hard rules:
1. **Set a budget alert at $50 and $80** via Cost Management. Both as actual + forecasted.
2. **Pause Cosmos when not actively building** (`az postgres flexible-server stop`). Saves ~$15/mo.
3. **Use Content Safety Free tier (F0) until June 5.** Upgrade to S0 only for the load-test day if needed.
4. **Use `gpt-4o-mini` as the default in all code paths.** Only call `gpt-4o` from the Glass Box explainer.

### Emergency tear-down (when balance hits $20)
```bash
az group delete --name rg-tripwire --yes --no-wait
```

## Step 6 — Daily cost-watchdog

Add to your shell rc:
```bash
alias azcost="az consumption usage list --top 5 --query '[].{Date:date,Service:meterCategory,Cost:pretaxCost}' -o table"
```

Run before bed. Anything spiking, kill the resource.

## Step 7 — Emergency tear-down

If you blow the credit cap:
```bash
az group delete --name rg-tripwire-prod --yes --no-wait
```
Everything goes. Bicep re-provisions in 12-15 min.

## Step 8 — Authentication strategy

- **No keys in env files committed to git.** All secrets in Key Vault.
- **Local dev**: `az login` + DefaultAzureCredential resolves automatically.
- **Container Apps**: managed identity with role assignments to OpenAI, Content Safety, Cosmos, Key Vault.
- **CI**: federated OIDC credential to Azure (no client secret).

Verify with:
```bash
az role assignment list --assignee <managed-identity-objectid> --output table
```
