#!/usr/bin/env python3
"""Generate docs/TripWire_Bible.pdf — the master business + product doc.

Serves three audiences in one doc: investor (market, moat, financials, ask),
hackathon judge (product depth, rubric fit), and founder (roadmap, workflows).
Embeds charts from docs/assets/ (run make_bible_charts.py first).

Run: python scripts/make_bible_pdf.py
"""
from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "..", "docs", "assets")
OUT = os.path.join(HERE, "..", "docs", "TripWire_Bible.pdf")

W, H = A4
INK = HexColor("#0a0c16")
INK2 = HexColor("#11141f")
ACCENT = HexColor("#5b8cff")
BLOCK = HexColor("#ff5470")
REVIEW = HexColor("#ffb454")
ALLOW = HexColor("#3ddc97")
PURPLE = HexColor("#b57bff")
TEAL = HexColor("#39c5cf")
PAPER = HexColor("#f7f9ff")
MUTED = HexColor("#5b6478")
CARD = white
BORDER = HexColor("#dbe2f5")
ACCENT_SOFT = HexColor("#e8eeff")

_pg = [0]


def wrap(c, text, x, y, w, font, size, lead, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in simpleSplit(text, font, size, w):
        c.drawString(x, y, ln)
        y -= lead
    return y


def rounded(c, x, y, w, h, r, fill, stroke=None, lw=1.1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1 if stroke else 0)


def bg(c, color=PAPER):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def footer(c, dark=False):
    _pg[0] += 1
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#8b95b0") if dark else MUTED)
    c.drawCentredString(W / 2, 11 * mm, f"TripWire Bible  -  Confidential business + product overview  -  {_pg[0]}")


def kicker(c, text, color=ACCENT, y=H - 18 * mm):
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(color)
    c.drawString(22 * mm, y, text.upper())


def h2(c, text, y=H - 29 * mm):
    c.setFont("Helvetica-Bold", 21)
    c.setFillColor(INK)
    c.drawString(22 * mm, y, text)
    return y - 12 * mm


def shield(c, cx, cy, s, color):
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy + s); p.lineTo(cx + s * 0.8, cy + s * 0.55); p.lineTo(cx + s * 0.8, cy - s * 0.2)
    p.curveTo(cx + s * 0.8, cy - s * 0.7, cx + s * 0.4, cy - s, cx, cy - s)
    p.curveTo(cx - s * 0.4, cy - s, cx - s * 0.8, cy - s * 0.7, cx - s * 0.8, cy - s * 0.2)
    p.lineTo(cx - s * 0.8, cy + s * 0.55); p.close()
    c.drawPath(p, fill=1, stroke=0)


def image(c, name, x, y, w):
    path = os.path.join(ASSETS, name)
    if not os.path.exists(path):
        return y
    img = ImageReader(path)
    iw, ih = img.getSize()
    h = w * ih / iw
    c.drawImage(img, x, y - h, width=w, height=h, mask="auto")
    return y - h


def callout(c, x, y, w, title, body, accent, soft):
    bl = simpleSplit(body, "Helvetica", 10.5, w - 16 * mm)
    h = 13 * mm + len(bl) * 5.2 * mm
    rounded(c, x, y - h, w, h, 8, soft, accent)
    rounded(c, x, y - h, 4.5 * mm, h, 2, accent)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(x + 10 * mm, y - 8.5 * mm, title)
    wrap(c, body, x + 10 * mm, y - 14.5 * mm, w - 18 * mm, "Helvetica", 10.5, 5.2 * mm, HexColor("#34406a"))
    return y - h - 4 * mm


# ---------- pages ----------
def cover(c):
    bg(c, INK)
    c.setFillColor(INK2)
    for gx in range(0, int(W), 26):
        for gy in range(0, int(H), 26):
            c.circle(gx, gy, 0.5, fill=1, stroke=0)
    shield(c, W / 2, H - 70 * mm, 24 * mm, ACCENT)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W / 2, H - 72.5 * mm, "TW")
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W / 2, H - 104 * mm, "The TripWire Bible")
    c.setFont("Helvetica", 15); c.setFillColor(ACCENT)
    c.drawCentredString(W / 2, H - 116 * mm, "The control plane for AI agent actions")
    y = H - 134 * mm
    for ln in simpleSplit("Product, market, business model, and three-year plan. "
                          "One document for investors, judges, and the founding team.",
                          "Helvetica", 12, 130 * mm):
        c.setFillColor(HexColor("#aab3cc")); c.drawCentredString(W / 2, y, ln); y -= 7 * mm
    rounded(c, W / 2 - 58 * mm, 36 * mm, 116 * mm, 20 * mm, 8, INK2)
    c.setFont("Helvetica", 9.5); c.setFillColor(HexColor("#8b95b0"))
    c.drawCentredString(W / 2, 47 * mm, "Microsoft Build AI 2026  -  Security in the Agentic Future")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(white)
    c.drawCentredString(W / 2, 42 * mm, "Kundan Khatri  -  github.com/KundanKhatri/Tripwire")
    c.setFont("Helvetica", 8); c.setFillColor(HexColor("#6b7590"))
    c.drawCentredString(W / 2, 38 * mm, "Figures marked [verify] are directional; confirm before external/financial use.")
    c.showPage(); _pg[0] += 1


def execsummary(c):
    bg(c); kicker(c, "Executive summary"); y = h2(c, "Make it safe to give an AI agent power")
    y = wrap(c,
        "Enterprises are handing AI agents real authority - to read data, call tools, spend money, "
        "and act on their own. The security model has not caught up. 88% of organizations have "
        "already had an agent security incident, yet only ~6% of security budget covers agent risk. "
        "TripWire closes that gap.", 22 * mm, y, 166 * mm, "Helvetica", 12, 6.6 * mm)
    y -= 2 * mm
    y = image(c, "c1_gap.png", 30 * mm, y, 150 * mm) - 4 * mm
    y = wrap(c,
        "LLM firewalls inspect the text going in. TripWire governs what the agent is allowed to do - "
        "across the three boundaries every agent exposes (prompt, tools/MCP, memory) - and proves "
        "nothing harmful leaves, with a full audit trail. It is the action-layer control plane "
        "incumbents under-serve.", 22 * mm, y, 166 * mm, "Helvetica", 12, 6.6 * mm)
    y = callout(c, 22 * mm, y - 1 * mm, 166 * mm, "The one-line",
        "TripWire is the runtime security, identity, and governance layer enterprises install "
        "before they let agents touch production systems. Open-core, provider-agnostic, built on Azure.",
        ACCENT, ACCENT_SOFT)
    footer(c); c.showPage()


def problempage(c):
    bg(c); kicker(c, "The problem", BLOCK); y = h2(c, "Agents are powerful - and unguarded")
    y = wrap(c,
        "The same autonomy that makes agents useful makes them dangerous when fooled. The damage is "
        "documented and concrete:", 22 * mm, y, 166 * mm, "Helvetica", 12, 6.6 * mm)
    rows = [
        ("Indirect prompt injection", "Hidden instructions in a document/email/web page the agent reads - the #1 OWASP agent risk."),
        ("Tool poisoning via MCP", "Malicious instructions in tool metadata; first malicious MCP package hit registries Sep 2025."),
        ("Memory poisoning", "False facts implanted into long-term memory persist across sessions."),
        ("Runaway cost loops", "A documented agent loop ran 11 days = $47,000; cost compounds 30x+ at 50 steps."),
        ("No audit trail", "EU AI Act penalties begin Aug 2026; few teams can show what their agents did."),
    ]
    y -= 1 * mm
    for t, b in rows:
        bl = simpleSplit(b, "Helvetica", 10.5, 120 * mm)
        h = 8.5 * mm + (len(bl) - 1) * 5 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 7, CARD, BORDER)
        c.setFillColor(BLOCK); c.circle(29 * mm, y - h / 2, 1.7 * mm, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(34 * mm, y - 6 * mm, t)
        wrap(c, b, 80 * mm, y - 6 * mm, 104 * mm, "Helvetica", 10.5, 5 * mm, MUTED)
        y -= h + 3.5 * mm
    y = image(c, "c3_cost.png", 30 * mm, y - 1 * mm, 150 * mm)
    footer(c); c.showPage()


def solutionpage(c):
    bg(c); kicker(c, "The solution"); y = h2(c, "One control plane, three boundaries")
    y = wrap(c,
        "TripWire runs inline as a 5-layer pipeline built on three reusable primitives - provenance, "
        "taint/canary, and inline policy - applied to the prompt, tool/MCP, and memory boundaries.",
        22 * mm, y, 166 * mm, "Helvetica", 12, 6.6 * mm)
    layers = [
        ("L1", "Semantic Firewall", ALLOW, "Patterns + Azure Prompt Shields + embedding similarity to a known-attack corpus."),
        ("L2", "Capability Provenance", ACCENT, "Tool calls need a signed token scoped to the real user request. Injected calls have no authority - denied."),
        ("L3", "Canary Tripwires", REVIEW, "Decoy secrets; if one ever leaves, it is proof of exfiltration. Zero false positives."),
        ("L4", "Behavioral Anomaly", PURPLE, "Scores when the agent's actions diverge from the user's goal."),
        ("L5", "Learning Classifier", TEAL, "Curated, human-in-the-loop model that improves from real attacks."),
    ]
    y -= 1 * mm
    for tag, name, col, desc in layers:
        bl = simpleSplit(desc, "Helvetica", 10.5, 120 * mm)
        h = 8.5 * mm + (len(bl) - 1) * 5 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 7, CARD, BORDER)
        rounded(c, 26 * mm, y - h + (h - 8 * mm) / 2, 13 * mm, 8 * mm, 3, col)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(32.5 * mm, y - h + (h - 8 * mm) / 2 + 2.4 * mm, tag)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(44 * mm, y - 6 * mm, name)
        wrap(c, desc, 80 * mm, y - 6 * mm, 104 * mm, "Helvetica", 10.5, 5 * mm, MUTED)
        y -= h + 3.5 * mm
    y = callout(c, 22 * mm, y, 166 * mm, "The standout",
        "L2 + L3 stop attacks an LLM firewall can't - like indirect injection, where the user "
        "request is benign and the attack hides in tool output. We don't recognize every attack; "
        "we deny it authority (L2) and catch the theft (L3).", ACCENT, ACCENT_SOFT)
    footer(c); c.showPage()


def proofpage(c):
    bg(c); kicker(c, "Proof"); y = h2(c, "It works - watch an attack get blocked")
    y = wrap(c,
        "A victim agent is asked only to summarize a document. The document is poisoned with a hidden "
        "instruction to read a secret file and email it to an attacker. The user authorized only "
        "'read_document', so every malicious tool call is denied for lack of provenance:",
        22 * mm, y, 166 * mm, "Helvetica", 12, 6.6 * mm)
    y -= 2 * mm
    code = [
        "[plan]    User asked to summarize a document.",
        "[tool]    Agent reads the document (authorized).",
        "[blocked] Injection -> read_file.  L2: not in granted scope [read_document]",
        "[blocked] Injection -> send_email. L2: not in granted scope [read_document]",
        "[final]   Attack neutralized. Nothing sensitive left the boundary.",
    ]
    ch = 6 * mm + len(code) * 5 * mm
    rounded(c, 22 * mm, y - ch, 166 * mm, ch, 6, INK)
    yy = y - 8 * mm
    for ln in code:
        col = BLOCK if "[blocked]" in ln else (ALLOW if "[final]" in ln else HexColor("#aab3cc"))
        c.setFont("Courier", 9.2); c.setFillColor(col)
        c.drawString(27 * mm, yy, ln); yy -= 5 * mm
    y = y - ch - 5 * mm
    y = callout(c, 22 * mm, y, 166 * mm, "Verified, not claimed",
        "13 automated tests green. Live Azure verified (embeddings + Prompt Shields). Benchmarks "
        "report block rate WITH false-positive rate; provenance + canary layers are zero-FP by "
        "construction. Try it: kundankhatri.github.io/Tripwire", ALLOW, HexColor("#eafaf3"))
    footer(c); c.showPage()


def marketpage(c):
    bg(c); kicker(c, "Market"); y = h2(c, "Big, new, and growing fast")
    y = image(c, "c2_market.png", 24 * mm, y, 162 * mm) - 3 * mm
    y = wrap(c,
        "Enterprise spend on agentic AI is projected near $200B for 2026. The agent-security "
        "sub-segment is the fastest-growing slice - ~$392M was funded around RSAC 2026 alone "
        "(Noma $100M, HiddenLayer $50M). The attack surface (MCP, agent memory, agent identity) "
        "is brand new, and regulation (EU AI Act) forces spend on a deadline.",
        22 * mm, y, 166 * mm, "Helvetica", 11.5, 6.3 * mm)
    y = callout(c, 22 * mm, y - 1 * mm, 166 * mm, "Why now",
        "Agents crossed from pilots to production in 2025-26; the boundaries we secure didn't exist "
        "two years ago; and security budget is shifting to agent risk from a near-zero base.",
        ACCENT, ACCENT_SOFT)
    footer(c); c.showPage()


def positionpage(c):
    bg(c); kicker(c, "Positioning & moat"); y = h2(c, "The open quadrant")
    y = image(c, "c6_position.png", 38 * mm, y, 134 * mm) - 3 * mm
    y = wrap(c,
        "Incumbents (Lakera, HiddenLayer, Noma, Prompt Security, Protect AI, Robust Intelligence) "
        "are mostly prompt/LLM-firewall first and often single-cloud. TripWire's wedge is agent "
        "ACTION security - the control plane over tools, identity, and memory - and it is "
        "provider-agnostic.", 22 * mm, y, 166 * mm, "Helvetica", 11.5, 6.3 * mm)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(INK)
    c.drawString(22 * mm, y - 2 * mm, "Moat, most durable first:")
    y -= 9 * mm
    for t in ["Data - telemetry across millions of actions -> detection + an agent risk score.",
              "Identity system-of-record - once we issue agent identities, switching is costly.",
              "Audit/compliance lock-in - we hold the legal record of agent behavior.",
              "Provider-agnostic - defensible against any single platform absorbing us."]:
        c.setFillColor(ACCENT); c.circle(25 * mm, y - 1.3 * mm, 1.5 * mm, fill=1, stroke=0)
        y = wrap(c, t, 30 * mm, y, 158 * mm, "Helvetica", 11, 5.7 * mm, MUTED) - 2 * mm
    footer(c); c.showPage()


def featurespage(c):
    bg(c); kicker(c, "Product roadmap"); y = h2(c, "From defense pipeline to platform")
    feats = [
        ("F1", "Agent Identity Ledger", "Cryptographic identity + lifecycle + kill-switch for every agent (NHI).", ACCENT),
        ("F2", "MCP Tool Firewall", "Scan + hash-pin + sandbox tools; defeat poisoning & rug-pulls.", REVIEW),
        ("F3", "Cost & Loop Governor", "Detect loops, enforce budgets, circuit-break before the $47K bill.", ALLOW),
        ("F4", "Memory-Poisoning Shield", "Provenance + taint for long-term agent memory.", PURPLE),
        ("F5", "Compliance Audit Ledger", "Signed, replayable action trail; EU AI Act / SOC2-ready.", TEAL),
        ("V1", "Agent Trust Fabric", "Cross-org agent-to-agent trust: PKI + reputation for non-human identities.", ACCENT),
        ("V2", "Agent Risk Score + Insurance", "Telemetry becomes an actuarial dataset; underwrite agent-loss cover.", BLOCK),
    ]
    y -= 1 * mm
    for tag, name, desc, col in feats:
        h = 13 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 7, CARD, BORDER)
        rounded(c, 26 * mm, y - h + 2.5 * mm, 13 * mm, 8 * mm, 3, col)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(32.5 * mm, y - h + 5 * mm, tag)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11)
        c.drawString(44 * mm, y - 6 * mm, name)
        c.setFillColor(MUTED); c.setFont("Helvetica", 9.8)
        c.drawString(44 * mm, y - 10.5 * mm, desc)
        y -= h + 3 * mm
    footer(c); c.showPage()


def gtmpage(c):
    bg(c); kicker(c, "Go-to-market"); y = h2(c, "Land with developers, expand to enterprise")
    y = image(c, "c5_funnel.png", 30 * mm, y, 150 * mm) - 3 * mm
    steps = [
        ("1  Adopt", "OSS SDK + L1 free. Win the dev wiring up an agent who just read an MCP-poisoning headline."),
        ("2  Land", "One agent team buys Team tier for a single production agent."),
        ("3  Expand", "Org-wide policy, identity ledger, audit module -> Enterprise."),
        ("4  Pull", "EU AI Act deadline is the urgency lever into regulated buyers."),
    ]
    for t, b in steps:
        c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 11)
        c.drawString(22 * mm, y, t)
        wrap(c, b, 52 * mm, y, 136 * mm, "Helvetica", 10.5, 5 * mm, MUTED)
        y -= 9 * mm
    y = callout(c, 22 * mm, y, 166 * mm, "Buyer & champion",
        "Champion = platform/AI-eng lead feeling the pain. Buyer = Director of AppSec / CISO holding "
        "the budget and the EU AI Act risk. Pricing is per protected agent - aligned with what's "
        "exploding (agent count) and the value (each agent is a risk retired).", ACCENT, ACCENT_SOFT)
    footer(c); c.showPage()


def modelpage(c):
    bg(c); kicker(c, "Business model"); y = h2(c, "Open-core, four revenue streams")
    tiers = [
        ("OSS / Free", "$0", "SDK, L1 firewall, single-agent provenance. The adoption funnel."),
        ("Team", "~$2-5K/mo", "Full 5-layer pipeline, MCP firewall, cost governor, dashboard, SSO."),
        ("Enterprise", "~$60-250K/yr", "Identity ledger, memory shield, compliance audit, policy, SLA, VPC."),
        ("Platform / data", "usage + %", "Trust fabric + risk score + insurance (the data moat)."),
    ]
    y -= 1 * mm
    for t, price, desc in tiers:
        h = 13 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 7, CARD, BORDER)
        rounded(c, 22 * mm, y - h, 4.5 * mm, h, 2, ACCENT)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(30 * mm, y - 6 * mm, t)
        c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(30 * mm, y - 10.5 * mm, price)
        c.setFillColor(MUTED); c.setFont("Helvetica", 9.8)
        wrap(c, desc, 70 * mm, y - 7.5 * mm, 116 * mm, "Helvetica", 9.8, 4.8 * mm, MUTED)
        y -= h + 3 * mm
    c.setFont("Helvetica-Bold", 11); c.setFillColor(INK)
    c.drawString(22 * mm, y - 1 * mm, "Revenue streams:")
    y = wrap(c, "(1) seat/agent subscriptions  (2) usage (actions inspected)  "
                "(3) compliance/audit module  (4) risk-score API + insurance share (later).",
             22 * mm, y - 7 * mm, 166 * mm, "Helvetica", 10.5, 5.5 * mm, MUTED)
    y = image(c, "c4_revenue.png", 24 * mm, y - 2 * mm, 162 * mm)
    footer(c); c.showPage()


def financepage(c):
    bg(c); kicker(c, "Three-year plan"); y = h2(c, "Roadmap and modeled ARR")
    phases = [
        ("Year 1 - Wedge", "5-layer pipeline + MCP firewall (F2) + cost governor (F3). OSS launch, 3-5 design partners, first 10 Team customers.", "~$0.4M ARR"),
        ("Year 2 - Platform", "Identity ledger (F1) + compliance audit (F5) + memory shield (F4). First enterprise contracts, SOC2, marketplace.", "~$4M ARR"),
        ("Year 3 - Data moat", "Risk score (V2 alpha) + trust fabric (V1 pilot). Land-and-expand + partner channel.", "~$18M ARR"),
    ]
    y -= 1 * mm
    for t, b, arr in phases:
        bl = simpleSplit(b, "Helvetica", 10.2, 120 * mm)
        h = 13 * mm + (len(bl) - 1) * 4.8 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 7, CARD, BORDER)
        rounded(c, 22 * mm, y - h, 4.5 * mm, h, 2, ACCENT)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(30 * mm, y - 6.5 * mm, t)
        c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 11)
        c.drawRightString(184 * mm, y - 6.5 * mm, arr)
        wrap(c, b, 30 * mm, y - 11.5 * mm, 150 * mm, "Helvetica", 10.2, 4.8 * mm, MUTED)
        y -= h + 3.5 * mm
    y = image(c, "c7_arr.png", 26 * mm, y - 1 * mm, 158 * mm) - 2 * mm
    c.setFont("Helvetica-Oblique", 8.5); c.setFillColor(MUTED)
    c.drawCentredString(W / 2, y, "All financials are planning models with stated assumptions (see BUSINESS_PLAN.md). [verify before external use]")
    footer(c); c.showPage()


def riskask(c):
    bg(c, INK); c.setFont("Helvetica-Bold", 21); c.setFillColor(white)
    c.drawString(22 * mm, H - 26 * mm, "Risks, mitigations & the ask")
    risks = [
        ("Platform absorption (Azure/OpenAI ship native)", "Provider-agnostic; own identity + audit + cross-vendor data."),
        ("Crowded market", "Wedge on action/tool/memory boundary, not prompt firewall."),
        ("Long enterprise sales cycles", "OSS bottom-up first; compliance deadline as urgency."),
        ("False positives erode trust", "Lead with zero-FP primitives; ranges, not hero numbers."),
        ("Learning-loop data poisoning", "Human-in-loop labeling; never auto-train on attacker data."),
    ]
    y = H - 40 * mm
    for t, m in risks:
        bl = simpleSplit(m, "Helvetica", 9.8, 150 * mm)
        h = 12 * mm + (len(bl) - 1) * 4.6 * mm
        rounded(c, 22 * mm, y - h, 166 * mm, h, 6, INK2, HexColor("#262b3d"))
        c.setFillColor(BLOCK); c.setFont("Helvetica-Bold", 10.5)
        c.drawString(28 * mm, y - 6 * mm, t)
        c.setFillColor(HexColor("#aab3cc")); c.setFont("Helvetica", 9.8)
        c.drawString(28 * mm, y - 10.5 * mm, "-> " + m)
        y -= h + 3 * mm
    rounded(c, 22 * mm, y - 26 * mm, 166 * mm, 23 * mm, 8, ACCENT)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 13)
    c.drawString(28 * mm, y - 9 * mm, "The ask")
    wrap(c, "Raise a pre-seed/seed to fund the Year-1 wedge: ship F2+F3, land design partners, prove "
            "the open-core funnel converts. Use of funds ~70% engineering, ~20% GTM/dev-rel, ~10% "
            "compliance/SOC2. (Fill amount + terms before use.)",
         28 * mm, y - 14 * mm, 154 * mm, "Helvetica", 9.8, 4.7 * mm, INK)
    footer(c, dark=True); c.showPage()


def closing(c):
    bg(c, INK)
    shield(c, W / 2, H / 2 + 24 * mm, 18 * mm, ACCENT)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W / 2, H / 2, "Make it safe to give an agent power.")
    c.setFont("Helvetica", 13); c.setFillColor(HexColor("#aab3cc"))
    c.drawCentredString(W / 2, H / 2 - 12 * mm, "TripWire - the control plane for AI agent actions.")
    c.setFont("Helvetica-Bold", 11); c.setFillColor(ACCENT)
    c.drawCentredString(W / 2, H / 2 - 28 * mm, "kundankhatri.github.io/Tripwire   -   github.com/KundanKhatri/Tripwire")
    c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("The TripWire Bible - product, market, business plan")
    c.setAuthor("Kundan Khatri")
    cover(c)
    execsummary(c)
    problempage(c)
    solutionpage(c)
    proofpage(c)
    marketpage(c)
    positionpage(c)
    featurespage(c)
    gtmpage(c)
    modelpage(c)
    financepage(c)
    riskask(c)
    closing(c)
    c.save()
    print("Wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
