# RULES_DIGEST — Things that can disqualify us or surprise us

Sourced from `hackerearth.com/challenges/hackathon/microsoft-build-ai-2026/{rules,custom-tab/guidelines}`. Treat as authoritative. If anything in this document contradicts the live site, the live site wins — re-read.

## Hard disqualifiers (do not violate)

1. **Project must be built entirely during 3 May – 30 June 2026.** No pre-existing code. Public commit history on GitHub from day 1 is our proof.
2. **Microsoft AI stack is mandatory.** Failure to "use Microsoft AI stack as a component of the solution" = disqualification per guidelines. We use Azure AI Foundry, Azure OpenAI, Azure AI Content Safety, Cosmos for Postgres, Container Apps, Static Web Apps, SignalR — well past the bar.
3. **No third-party IP or pre-existing IP.** Open-source dependencies are fine when properly credited in the README with license details.
4. **Public GitHub repo accessible to judges.** From day 1.
5. **README must include**: project description, setup instructions, dependencies, team member details. ✅ implemented in `README.md`.
6. **Disclose every AI tool used in development** in the README. ✅ see `AI_TOOLS_DISCLOSURE.md`.
7. **No secrets in the repo.** Use `.env.example` only. CI secret scan enabled.
8. **No sensitive personal data in submitted materials.** Demo dataset is synthetic.
9. **Disclose open-source components and their licenses** at submission time. ✅ table in README, full list in `packages/attack-corpus/SOURCES.md`.
10. **One participant per team. Cannot be on multiple teams.** Solo here.
11. **Plagiarism = disqualification.** All code original to us + properly credited OSS.

## Soft surprises (know before signing)

### IP assignment — quoted verbatim
> "The Participant hereby irrevocably and perpetually assigns to Microsoft Corporation on a worldwide basis, without additional consideration, all worldwide rights, title, and interest, in and to any Materials."

Translation: on submission, Microsoft owns TripWire. We cannot independently commercialize the submitted code after. We can still:
- Use the experience and credentials publicly
- Build a separate product later using our own learnings (but not the submitted codebase verbatim)
- Reference the win on resume / portfolio

If this is a dealbreaker, we do not submit. We have decided it is not — prize value, resume signal, and the open-source ecosystem play (we will publicly release earlier checkpoints under MIT before submission, marking those as our own provenance) justify it.

**Action**: tag a public release `v0.1-prototype` on GitHub *before* the final submission. That earlier checkpoint stays MIT-ours.

### Liability cap
> Maximum liability capped at **Rs. 5000**.

Translation: if Microsoft makes a mistake that costs us money, recovery is capped. Not a meaningful risk for us.

### Multiple submissions
> "Last hack will be considered as the final submission."

Translation: we can iterate and re-submit until the deadline. Useful — we ship prototype version, then keep updating.

### Prize tax
> "Winners are responsible for all applicable taxes, withholding, and reporting requirements."

Translation: ₹3,00,000 will be net of TDS (likely ~31.2% under Section 194B for prize income in India). Net ≈ ₹2,06,400. Factor in if planning what to do with winnings.

### Documentation for additional disbursement
> Winners must sign documentation Microsoft requires "within such timelines as they specify. Failure to do so may result in disqualification."

Translation: respond to all post-win emails immediately. Set up a label/filter.

## Timeline (from hackerearth)

| Event | Date (Asia/Kolkata) |
| --- | --- |
| Build period opens | May 3, 2026 |
| Registration opens | May 5, 2026 |
| Prototype phase ends | June 7, 2026, 11:59 PM IST (06:29 PM UTC) |
| Final submission | June 30, 2026 |

**We anchor on June 7.** That's the gate to final-stage consideration.

## What is NOT documented (and how we handle it)

- No specified pitch video format → we make a 3-min MP4, 1080p, MP4/H.264, embedded in README and uploaded to YouTube unlisted.
- No specified pitch deck format → we make an 8-slide PDF. Embedded in `docs/PITCH.pdf`.
- No specified judging order between prototype and final → we treat prototype as the binary gate (pass/fail to advance) and final as the scoring round.

## Pre-submission checklist (run T-24h before each deadline)

- [ ] Repo public on GitHub
- [ ] README complete with all required sections
- [ ] AI_TOOLS_DISCLOSURE.md present and accurate
- [ ] All OSS dependencies credited with licenses
- [ ] No secrets in repo (run `gitleaks detect`)
- [ ] Live deployment URL up and tested
- [ ] Pitch video uploaded and linked
- [ ] Pitch deck PDF in repo
- [ ] Team details accurate in README
- [ ] Submission form on HackerEarth filled with correct URLs
- [ ] Tagged release on GitHub matching submission
