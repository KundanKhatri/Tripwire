# Attack corpus sources and attribution

The TripWire attack corpus is a curated set of prompt-injection patterns drawn from publicly available research, taxonomies, and security disclosures. Every entry includes a `source` field. This document expands those references and provides license attribution where required.

Current corpus: 30 seed patterns across 14 attack types and 6 OWASP LLM Top 10 categories. Target by June 7: 200 patterns. Final target by June 30: 2,000+ patterns.

## Categories represented (OWASP LLM Top 10 2025)

- **LLM01 — Prompt Injection** (direct and indirect)
- **LLM02 — Insecure Output Handling** (exfiltration via markdown/links)
- **LLM06 — Sensitive Information Disclosure**
- **LLM07 — Insecure Plugin Design** (tool misuse)
- **LLM08 — Excessive Agency**

Full OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/

## Public sources referenced

| Source | License | Use in corpus |
| --- | --- | --- |
| OWASP LLM Top 10 (2025) | CC-BY-SA-4.0 | Threat taxonomy, attack class definitions |
| HackAPrompt 2023 dataset | CC-BY-4.0 | Pattern inspiration (not verbatim copy) |
| Anthropic published red-team research | Article-fair-use citation | Attack-class taxonomy |
| Microsoft Azure AI Content Safety — Prompt Shields documentation | Article-fair-use citation | Baseline detection benchmarks |
| Lakera Gandalf public writeups | Article-fair-use citation | Pattern inspiration |

## What is NOT in the corpus

- No payloads that target real people, real companies, or real systems
- No payloads containing actual API keys, credentials, or sensitive personal data
- No payloads copied verbatim from datasets whose licenses prohibit redistribution

All `payload` strings are either authored originally for TripWire or are paraphrases of widely-published attack classes. Where a payload is structurally similar to a published example, the `source` field cites the published taxonomy class, not a specific dataset row.

## Contribution guidelines (post-launch)

For future contributors adding to the corpus:
1. Cite a public source for each entry.
2. Tag with OWASP class and attack type.
3. Severity 1–10 scaled to (probability × impact).
4. No real PII. No real secrets. No targeted attacks.
