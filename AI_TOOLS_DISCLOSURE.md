# AI Tools Disclosure

Per Microsoft Build AI 2026 hackathon guidelines, all AI tools used in the development of this project are disclosed below. This document is updated as new tools are introduced.

## Development-time AI tools (used to build the codebase)

| Tool | Use | Where it touched the code |
| --- | --- | --- |
| **Claude Code (Anthropic)** | Architecture design, scaffolding, refactoring, code review. Used as a pair-programming assistant. | Across the repo — initial scaffold, defense layer logic outlines, documentation. All code reviewed, modified, and accepted by the human author. |
| **GitHub Copilot** | Inline code completions in VS Code. | Across the repo. Suggestions accepted only after review. |

## Runtime AI dependencies (the product itself uses these)

These are not development tools — they are services TripWire calls in production. Listed here for completeness.

| Service | Use |
| --- | --- |
| Azure OpenAI Service — `gpt-4.1` | Glass Box trace explainer (generates human-readable reasoning for blocked attacks) |
| Azure OpenAI Service — `o4-mini` | L1 hot-path classification |
| Azure OpenAI Service — `text-embedding-3-large` | Embedding generation for L1 similarity search and L4 trajectory analysis |
| Azure AI Content Safety — Prompt Shields | L1 baseline attack detection |
| Azure AI Content Safety — Groundedness | L4 anomaly cross-check |
| Azure AI Foundry — agent runtime | Hosts the protected demo agent (the target of arena attacks) |
| Custom fine-tuned classifier (DistilBERT-class) | L5 learning classifier. Trained on the attack corpus, deployed on Azure ML managed online endpoint. |

## Statement of human contribution

Per the guideline that "the final solution must clearly demonstrate meaningful human creativity, judgment, and engineering — AI-generated boilerplate alone does not constitute a good submission":

The architecture of TripWire — the 5-layer defense model, the canary token mechanism, the capability provenance design, the live red-team arena loop — is original to the author. AI tools were used to accelerate implementation of decisions the author made and to surface options for the author to evaluate. Every commit was authored, reviewed, and accepted by a human.

The novel contributions of this project that AI tools did not invent:
- The 5-layer defense-in-depth model as applied to agentic systems
- The capability provenance design (HMAC-signed authorization scoping)
- The decision to extend Azure Prompt Shields rather than replace it
- The arena leaderboard as a learning-loop input
- The Glass Box trace UI for explainability
- The overall product positioning and market thesis

## Audit trail

Public commit history on GitHub is the primary audit trail. Commits are signed and timestamped. For any commit where an AI tool produced more than a trivial amount of the diff, the commit body notes it (`AI-assisted: claude-code` or similar).
