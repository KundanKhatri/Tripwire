# TripWire — Web (Arena UI)

Next.js 14 + Tailwind + Framer Motion. The live red-team arena where anyone can attack a protected
agent and watch the 5-layer defense pipeline decide, layer by layer.

## Key design choice

The arena ships with a **local defense mirror** (`src/lib/localEngine.ts`) — a faithful TS port of
the L1 pattern bank. This means the site is fully interactive **with zero backend**, so the live
demo can never break on stage. When `NEXT_PUBLIC_API_BASE` points at the deployed FastAPI engine,
requests route through the real Azure-backed pipeline (Prompt Shields + embeddings + classifier).

## Run

```bash
pnpm install   # or npm install
pnpm dev       # http://localhost:3000
```

## Deploy

- Azure Static Web Apps (primary, for the Microsoft-stack requirement)
- Any Node host as fallback

Set `NEXT_PUBLIC_API_BASE` in the host's env to the Container Apps URL of the API.
