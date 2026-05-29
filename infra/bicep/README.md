# Infra — Bicep

One-command provisioning of the TripWire Azure stack.

## What it creates

| Resource | SKU (Student-credit friendly) | Purpose |
| --- | --- | --- |
| Azure OpenAI + 3 deployments | S0 | gpt-4o, gpt-4o-mini, text-embedding-3-large |
| Azure AI Content Safety | S0 | Prompt Shields (L1), Groundedness (L4) |
| Cosmos for PostgreSQL | Burstable B1ms | attack corpus + pgvector |
| Container Apps env | Consumption | API host |
| SignalR | Free F1 | real-time leaderboard |
| Log Analytics + App Insights | PerGB / first 1GB free | telemetry |

## Deploy

```bash
export PG_ADMIN_PASSWORD=$(openssl rand -base64 24)
az group create -n rg-tripwire -l eastus
az deployment group create \
  -g rg-tripwire \
  -f main.bicep \
  -p main.bicepparam \
  -p pgAdminPassword=$PG_ADMIN_PASSWORD
```

Outputs (OpenAI endpoint, Content Safety endpoint, Postgres host, App Insights
connection string) print at the end — copy them into `apps/api/.env.local`.

## Teardown

```bash
az group delete -n rg-tripwire --yes --no-wait
```

## Note on the quick path

For the prototype we provision Azure OpenAI directly via `az cognitiveservices`
(see AZURE_SETUP.md) because it is faster to iterate. This Bicep file is the
reproducible, reviewable IaC that judges can read and run — it provisions the
*entire* stack in one command and is what the "production-grade from day one"
architecture story rests on.
