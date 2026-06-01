#!/usr/bin/env python3
"""Generate docs/TripWire_Deck.pdf — the 10-slide submission pitch deck.

Widescreen 16:9. Built for the Microsoft Build AI 2026 submission (HackerEarth):
problem, solution, the differentiating insight, architecture, AI integration,
live proof, honest benchmarks, market, business, roadmap + team.

Shares the TripWire brand system (dark ink + accent blue) with the Bible PDF.
Embeds charts from docs/assets/ (run make_bible_charts.py first).

Run: source .azcli-venv/bin/activate && python scripts/make_deck_pdf.py
"""
from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "..", "docs", "assets")
OUT = os.path.join(HERE, "..", "docs", "TripWire_Deck.pdf")

# 16:9 widescreen (PowerPoint standard, 13.333 x 7.5 in)
W, H = 338.67 * mm, 190.5 * mm

INK = HexColor("#0a0c16")
INK2 = HexColor("#11141f")
CARD_DK = HexColor("#161a28")
ACCENT = HexColor("#5b8cff")
ACCENT2 = HexColor("#7aa2ff")
BLOCK = HexColor("#ff5470")
REVIEW = HexColor("#ffb454")
ALLOW = HexColor("#3ddc97")
PURPLE = HexColor("#b57bff")
TEAL = HexColor("#39c5cf")
PAPER = HexColor("#f7f9ff")
MUTED = HexColor("#5b6478")
MUTED_DK = HexColor("#8b95b0")
BORDER = HexColor("#dbe2f5")
BORDER_DK = HexColor("#2a3047")
ACCENT_SOFT = HexColor("#e8eeff")

MARGIN = 26 * mm
_pg = [0]


# ---------- primitives ----------
def bg(c, color=PAPER):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def dotgrid(c, color=INK2, step=28):
    c.setFillColor(color)
    for gx in range(0, int(W), step):
        for gy in range(0, int(H), step):
            c.circle(gx, gy, 0.5, fill=1, stroke=0)


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


def kicker(c, text, color=ACCENT, dark=False):
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(color)
    c.drawString(MARGIN, H - 24 * mm, text.upper())


def title(c, text, color=None, y=None):
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(color or INK)
    y = y if y is not None else H - 38 * mm
    c.drawString(MARGIN, y, text)
    return y - 14 * mm


def footer(c, dark=False):
    _pg[0] += 1
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED_DK if dark else MUTED)
    c.drawString(MARGIN, 11 * mm, "TripWire  ·  The control plane for AI agent actions")
    c.drawRightString(W - MARGIN, 11 * mm, f"Microsoft Build AI 2026  ·  {_pg[0]} / 10")


def pagenum_only(c):
    _pg[0] += 1


# ---------- slides ----------
def s1_cover(c):
    bg(c, INK)
    dotgrid(c)
    # left brand block
    shield(c, MARGIN + 12 * mm, H - 50 * mm, 13 * mm, ACCENT)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(MARGIN + 12 * mm, H - 51.5 * mm, "TW")

    c.setFillColor(white); c.setFont("Helvetica-Bold", 72)
    c.drawString(MARGIN, H - 100 * mm, "TripWire")
    c.setFont("Helvetica", 22); c.setFillColor(ACCENT)
    c.drawString(MARGIN + 1 * mm, H - 114 * mm, "The control plane for AI agent actions")

    y = H - 130 * mm
    for ln in simpleSplit("Stop prompt injection, tool poisoning, data exfiltration, and runaway "
                          "agents — at the action layer, on Azure.", "Helvetica", 14, 116 * mm):
        c.setFillColor(HexColor("#aab3cc")); c.drawString(MARGIN, y, ln); y -= 8 * mm

    # bottom strip
    c.setFillColor(HexColor("#6b7590")); c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, 24 * mm, "MICROSOFT BUILD AI 2026  ·  SECURITY IN THE AGENTIC FUTURE")
    c.setFillColor(white); c.setFont("Helvetica", 11)
    c.drawString(MARGIN, 16 * mm, "Kundan Khatri  ·  kundanlm10@gmail.com  ·  github.com/KundanKhatri/Tripwire")

    # right pipeline glyph
    rx = W - 96 * mm
    layers = [("L1", ALLOW), ("L2", ACCENT), ("L3", REVIEW), ("L4", PURPLE), ("L5", TEAL)]
    ly = H - 58 * mm
    c.setFont("Helvetica-Bold", 9.5)
    for tag, col in layers:
        rounded(c, rx, ly - 12 * mm, 64 * mm, 12 * mm, 4, CARD_DK, BORDER_DK)
        rounded(c, rx + 3 * mm, ly - 9.5 * mm, 9 * mm, 7 * mm, 2, col)
        c.setFillColor(white); c.drawCentredString(rx + 7.5 * mm, ly - 7.2 * mm, tag)
        c.setFillColor(HexColor("#c2cbe0")); c.setFont("Helvetica", 9.5)
        names = {"L1": "Semantic Firewall", "L2": "Capability Provenance", "L3": "Canary Tripwires",
                 "L4": "Behavioral Anomaly", "L5": "Learning Classifier"}
        c.drawString(rx + 16 * mm, ly - 7.2 * mm, names[tag]); c.setFont("Helvetica-Bold", 9.5)
        ly -= 15 * mm
    c.setFillColor(MUTED_DK); c.setFont("Helvetica", 9)
    c.drawCentredString(rx + 32 * mm, ly - 1 * mm, "5-layer defense pipeline")
    c.showPage(); pagenum_only(c)


def s2_problem(c):
    bg(c); kicker(c, "The problem", BLOCK)
    title(c, "We're handing agents real power — and not guarding it")
    wrap(c, "Enterprises let AI agents read data, call tools, spend money, and act autonomously. "
            "The security model hasn't caught up.", MARGIN, H - 50 * mm, W - 2 * MARGIN,
         "Helvetica", 13.5, 7 * mm)

    # three big stats
    stats = [("88%", "of organizations have already had an agent-related security incident", BLOCK),
             ("~6%", "of security budget covers agent risk", REVIEW),
             ("$47K", "documented cost of a single runaway agent loop (11 days)", PURPLE)]
    sw = (W - 2 * MARGIN - 16 * mm) / 3
    sx = MARGIN
    for big, lab, col in stats:
        rounded(c, sx, H - 100 * mm, sw, 32 * mm, 8, white, BORDER)
        rounded(c, sx, H - 100 * mm, 4 * mm, 32 * mm, 2, col)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 34)
        c.drawString(sx + 11 * mm, H - 82 * mm, big)
        wrap(c, lab, sx + 11 * mm, H - 88 * mm, sw - 16 * mm, "Helvetica", 10.5, 5 * mm, MUTED)
        sx += sw + 8 * mm

    # attack list (two columns)
    rows = [
        ("Indirect prompt injection", "Hidden instructions in a doc/email/page the agent reads — #1 OWASP agent risk."),
        ("Tool poisoning via MCP", "Malicious instructions in tool metadata; first malicious MCP package, Sep 2025."),
        ("Memory poisoning", "False facts implanted into long-term memory persist across sessions."),
        ("No audit trail", "EU AI Act penalties begin Aug 2026; few teams can show what their agents did."),
    ]
    colw = (W - 2 * MARGIN - 10 * mm) / 2
    y0 = H - 106 * mm
    for i, (t, b) in enumerate(rows):
        cx = MARGIN + (i % 2) * (colw + 10 * mm)
        cy = y0 - (i // 2) * 26 * mm
        rounded(c, cx, cy - 22 * mm, colw, 22 * mm, 7, white, BORDER)
        c.setFillColor(BLOCK); c.circle(cx + 8 * mm, cy - 7.5 * mm, 1.8 * mm, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 12.5)
        c.drawString(cx + 14 * mm, cy - 8.5 * mm, t)
        wrap(c, b, cx + 14 * mm, cy - 14.5 * mm, colw - 20 * mm, "Helvetica", 10.5, 5 * mm, MUTED)

    rounded(c, MARGIN, 18 * mm, W - 2 * MARGIN, 14 * mm, 7, ACCENT_SOFT, ACCENT)
    c.setFillColor(HexColor("#22305c")); c.setFont("Helvetica-Bold", 12.5)
    c.drawString(MARGIN + 8 * mm, 23 * mm,
                 "LLM firewalls inspect the text going IN. Nobody governs what the agent is allowed to DO — and proves nothing harmful leaves. That's TripWire.")
    footer(c); c.showPage()


def s3_solution(c):
    bg(c); kicker(c, "The solution")
    title(c, "One control plane. Three boundaries. Five layers.")
    wrap(c, "TripWire sits inline between your agent and the world, across the three boundaries "
            "every agent exposes — the prompt, the tools/MCP, and the memory — enforcing a 5-layer "
            "defense pipeline on every action.", MARGIN, H - 50 * mm, W - 2 * MARGIN,
         "Helvetica", 13.5, 7 * mm)

    layers = [
        ("L1", "Semantic Firewall", ALLOW, "Pattern rules + Azure Prompt Shields + embedding similarity to a known-attack corpus."),
        ("L2", "Capability Provenance", ACCENT, "Every tool call must carry a signed token scoped to the real user request. Injected calls have no authority — denied."),
        ("L3", "Canary Tripwires", REVIEW, "Decoy secrets seeded into context; if one ever leaves, it is proof of exfiltration. Zero false positives."),
        ("L4", "Behavioral Anomaly", PURPLE, "Scores when the agent's actions diverge from the user's goal (goal hijack)."),
        ("L5", "Learning Classifier", TEAL, "Curated, human-in-the-loop model that improves from real attacks."),
    ]
    y = H - 66 * mm
    rh = 17 * mm
    for tag, name, col, desc in layers:
        rounded(c, MARGIN, y - rh, W - 2 * MARGIN, rh, 7, white, BORDER)
        rounded(c, MARGIN + 5 * mm, y - rh + (rh - 11 * mm) / 2, 18 * mm, 11 * mm, 3, col)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(MARGIN + 14 * mm, y - rh + (rh - 11 * mm) / 2 + 3 * mm, tag)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGIN + 28 * mm, y - 8.5 * mm, name)
        wrap(c, desc, MARGIN + 95 * mm, y - 8 * mm, W - 2 * MARGIN - 100 * mm, "Helvetica", 11, 5.2 * mm, MUTED)
        y -= rh + 3 * mm
    footer(c); c.showPage()


def s4_insight(c):
    bg(c, INK); dotgrid(c)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(ACCENT)
    c.drawString(MARGIN, H - 24 * mm, "THE INSIGHT — WHY TRIPWIRE WINS")
    c.setFont("Helvetica-Bold", 30); c.setFillColor(white)
    c.drawString(MARGIN, H - 38 * mm, "Don't try to recognize every attack.")
    c.setFont("Helvetica-Bold", 30); c.setFillColor(ACCENT2)
    c.drawString(MARGIN, H - 52 * mm, "Deny it authority. Catch the theft.")

    wrap(c, "Indirect injection is unsolvable by text inspection: the user's request is benign and "
            "the attack hides in tool-returned content. So we stopped playing whack-a-mole with "
            "payloads and changed the model of trust.", MARGIN, H - 66 * mm, W - 2 * MARGIN,
         "Helvetica", 13.5, 7 * mm, HexColor("#aab3cc"))

    cards = [
        ("L2 · Capability Provenance", ACCENT,
         "Every tool call carries a signed token scoped to the real user request. "
         "An injected call — even a perfectly-worded one — has no token for that scope, "
         "so it is denied. The attack never gets authority to act."),
        ("L3 · Canary Tripwires", REVIEW,
         "Decoy secrets are seeded into the agent's context. They have no legitimate reason "
         "to leave the boundary. If one ever does, that is hard proof of exfiltration — "
         "zero false positives, by construction."),
    ]
    cw = (W - 2 * MARGIN - 12 * mm) / 2
    cx = MARGIN
    for t, col, b in cards:
        rounded(c, cx, 40 * mm, cw, 56 * mm, 9, CARD_DK, BORDER_DK)
        rounded(c, cx, 40 * mm, 4 * mm, 56 * mm, 2, col)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 16)
        c.drawString(cx + 12 * mm, 88 * mm, t)
        wrap(c, b, cx + 12 * mm, 78 * mm, cw - 20 * mm, "Helvetica", 12, 6.4 * mm, HexColor("#c2cbe0"))
        cx += cw + 12 * mm

    rounded(c, MARGIN, 20 * mm, W - 2 * MARGIN, 14 * mm, 7, INK2, ACCENT)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 8 * mm, 25 * mm,
                 "These are the two layers an LLM firewall structurally cannot have. That's the moat.")
    footer(c, dark=True); c.showPage()


def s5_arch(c):
    bg(c); kicker(c, "Architecture", TEAL)
    title(c, "Azure-native, provider-agnostic core")

    # flow diagram: User -> Agent -> [TripWire] -> World, with Azure services under TripWire
    cy = H - 78 * mm
    bw, bh = 44 * mm, 22 * mm
    gap = 16 * mm
    x0 = MARGIN + 4 * mm

    def node(x, label, sub, fill, txt=INK, stroke=BORDER):
        rounded(c, x, cy - bh, bw, bh, 7, fill, stroke)
        c.setFillColor(txt); c.setFont("Helvetica-Bold", 12.5)
        c.drawCentredString(x + bw / 2, cy - 9 * mm, label)
        c.setFillColor(MUTED if fill == white else HexColor("#c2cbe0")); c.setFont("Helvetica", 9)
        c.drawCentredString(x + bw / 2, cy - 15 * mm, sub)

    def arrow(x1, x2):
        c.setStrokeColor(ACCENT); c.setLineWidth(2)
        c.line(x1, cy - bh / 2, x2, cy - bh / 2)
        c.setFillColor(ACCENT)
        p = c.beginPath(); p.moveTo(x2, cy - bh / 2); p.lineTo(x2 - 3 * mm, cy - bh / 2 + 2 * mm)
        p.lineTo(x2 - 3 * mm, cy - bh / 2 - 2 * mm); p.close(); c.drawPath(p, fill=1, stroke=0)

    node(x0, "User", "real request", white)
    arrow(x0 + bw, x0 + bw + gap)
    node(x0 + bw + gap, "AI Agent", "any framework", white)
    tx = x0 + 2 * (bw + gap)
    arrow(x0 + 2 * bw + gap, tx)
    # TripWire emphasized
    rounded(c, tx, cy - bh - 3 * mm, bw + 6 * mm, bh + 6 * mm, 8, INK, ACCENT, 2)
    shield(c, tx + (bw + 6 * mm) / 2, cy - 7 * mm, 5 * mm, ACCENT)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(tx + (bw + 6 * mm) / 2, cy - 14 * mm, "TripWire")
    c.setFillColor(MUTED_DK); c.setFont("Helvetica", 8.5)
    c.drawCentredString(tx + (bw + 6 * mm) / 2, cy - 19 * mm, "L1–L5 inline")
    arrow(tx + bw + 6 * mm, tx + bw + 6 * mm + gap)
    node(tx + bw + 6 * mm + gap, "World", "tools · data · $", white)

    # Azure services row under TripWire
    c.setFont("Helvetica-Bold", 11); c.setFillColor(TEAL)
    c.drawString(MARGIN, cy - 38 * mm, "RUNS ON AZURE")
    svc = [
        ("Azure OpenAI", "text-embedding-3-large · similarity + anomaly"),
        ("Azure AI Content Safety", "Prompt Shields — L1 baseline (verified live)"),
        ("Azure Container Apps", "FastAPI defense engine"),
        ("Cosmos DB for PostgreSQL", "pgvector corpus + immutable traces"),
        ("Static Web Apps / SignalR", "arena UI + live leaderboard"),
        ("Bicep + azd", "one-command provisioning (IaC)"),
    ]
    colw = (W - 2 * MARGIN - 10 * mm) / 3
    sy = cy - 46 * mm
    for i, (name, sub) in enumerate(svc):
        sx = MARGIN + (i % 3) * (colw + 5 * mm)
        scy = sy - (i // 3) * 24 * mm
        rounded(c, sx, scy - 20 * mm, colw, 20 * mm, 6, white, BORDER)
        rounded(c, sx, scy - 20 * mm, 3.5 * mm, 20 * mm, 2, TEAL)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(sx + 8 * mm, scy - 8 * mm, name)
        wrap(c, sub, sx + 8 * mm, scy - 13.5 * mm, colw - 12 * mm, "Helvetica", 9.5, 4.6 * mm, MUTED)
    footer(c); c.showPage()


def s6_ai(c):
    bg(c); kicker(c, "AI integration", PURPLE)
    title(c, "Where the intelligence lives")
    wrap(c, "TripWire uses AI on both sides of the boundary — Azure models to detect attacks, and "
            "a real victim agent to prove the defense under live attack.", MARGIN, H - 50 * mm,
         W - 2 * MARGIN, "Helvetica", 13.5, 7 * mm)

    items = [
        ("Embedding similarity", ACCENT,
         "Azure OpenAI text-embedding-3-large embeds every inbound prompt and scores cosine "
         "similarity to a known-attack corpus in pgvector. Catches novel phrasings with no keyword match."),
        ("Azure Prompt Shields", ALLOW,
         "Azure AI Content Safety Prompt Shields runs as the L1 baseline — a hosted jailbreak/"
         "injection classifier, verified live against the deployment."),
        ("Behavioral anomaly (L4)", PURPLE,
         "Embeds the agent's actions and scores divergence from the user's stated goal — surfacing "
         "goal-hijack even when each individual step looks innocent."),
        ("Victim agent (the proof)", REVIEW,
         "A real tool-calling agent (gpt-oss-120b on Azure) runs the attack end-to-end so every "
         "layer's decision is observable — not a mock. Provenance denies injected calls in the loop."),
        ("Learning classifier (L5)", TEAL,
         "Human-in-the-loop curation turns every real attack into training signal — the data moat "
         "that compounds as the corpus grows."),
        ("Honest by design", BLOCK,
         "We report block rate WITH false-positive rate, always, against a held-out eval set on "
         "live Azure. No cherry-picked hero number."),
    ]
    colw = (W - 2 * MARGIN - 10 * mm) / 3
    y0 = H - 64 * mm
    for i, (t, col, b) in enumerate(items):
        cx = MARGIN + (i % 3) * (colw + 5 * mm)
        cyy = y0 - (i // 3) * 44 * mm
        rounded(c, cx, cyy - 40 * mm, colw, 40 * mm, 7, white, BORDER)
        c.setFillColor(col); c.circle(cx + 7 * mm, cyy - 8 * mm, 2 * mm, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont("Helvetica-Bold", 12.5)
        c.drawString(cx + 12 * mm, cyy - 9 * mm, t)
        wrap(c, b, cx + 6 * mm, cyy - 16 * mm, colw - 11 * mm, "Helvetica", 10, 4.9 * mm, MUTED)
    footer(c); c.showPage()


def s7_proof(c):
    bg(c, INK); dotgrid(c)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(ALLOW)
    c.drawString(MARGIN, H - 24 * mm, "PROOF — WATCH AN ATTACK GET BLOCKED")
    c.setFont("Helvetica-Bold", 30); c.setFillColor(white)
    c.drawString(MARGIN, H - 38 * mm, "Indirect injection, defeated in the loop")

    wrap(c, "The victim agent is asked only to summarize a document. The document is poisoned with a "
            "hidden instruction to read a secret file and email it to an attacker. The user authorized "
            "only 'read_document' — so every malicious tool call is denied for lack of provenance.",
         MARGIN, H - 50 * mm, W - 2 * MARGIN, "Helvetica", 12.5, 6.6 * mm, HexColor("#aab3cc"))

    # terminal card
    tw = W - 2 * MARGIN
    rounded(c, MARGIN, 30 * mm, tw, 70 * mm, 9, HexColor("#05060c"), BORDER_DK)
    c.setFillColor(BLOCK); c.circle(MARGIN + 8 * mm, 95 * mm, 1.6 * mm, fill=1, stroke=0)
    c.setFillColor(REVIEW); c.circle(MARGIN + 13 * mm, 95 * mm, 1.6 * mm, fill=1, stroke=0)
    c.setFillColor(ALLOW); c.circle(MARGIN + 18 * mm, 95 * mm, 1.6 * mm, fill=1, stroke=0)
    c.setFillColor(MUTED_DK); c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 26 * mm, 94 * mm, "victim_agent.py — live trace")

    lines = [
        ("[plan]   ", "User asked to summarize a document.", HexColor("#c2cbe0")),
        ("[tool]   ", "Agent reads the document (authorized).", ALLOW),
        ("[blocked]", "Injection -> read_file.   L2: not in granted scope [read_document]", BLOCK),
        ("[blocked]", "Injection -> send_email.  L2: not in granted scope [read_document]", BLOCK),
        ("[final]  ", "Attack neutralized. Nothing sensitive left the boundary.", ALLOW),
    ]
    ty = 84 * mm
    for tag, txt, col in lines:
        c.setFont("Courier-Bold", 12); c.setFillColor(col)
        c.drawString(MARGIN + 8 * mm, ty, tag)
        c.setFont("Courier", 12); c.setFillColor(HexColor("#dfe5f2"))
        c.drawString(MARGIN + 36 * mm, ty, txt)
        ty -= 8.5 * mm

    c.setFillColor(MUTED_DK); c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN, 22 * mm,
                 "Try it yourself in the live arena → kundankhatri.github.io/Tripwire  ·  the Glass Box shows each layer's decision.")
    footer(c, dark=True); c.showPage()


def s8_benchmark(c):
    bg(c); kicker(c, "Benchmarks — honest by design")
    title(c, "Strictly more attacks caught, at 0% false-positive cost")
    wrap(c, "Measured against a held-out eval set (20 attacks + 20 benign) on live Azure — none of "
            "these exact strings were in the indexed corpus. We report block rate WITH false-positive "
            "rate, always.", MARGIN, H - 50 * mm, W - 2 * MARGIN, "Helvetica", 13, 6.8 * mm)

    # table
    cols = ["Config", "Attack block", "Attack caught", "Benign blocked (FP)", "Latency p95"]
    rows = [
        ["No defense (baseline)", "0%", "0%", "0%", "0 ms"],
        ["Azure Prompt Shields only", "75%", "75%", "0%", "613 ms"],
        ["Full TripWire (L1)", "80%", "90%", "0%", "708 ms"],
    ]
    tx, ty = MARGIN, H - 64 * mm
    tw = W - 2 * MARGIN
    cws = [tw * 0.30, tw * 0.16, tw * 0.16, tw * 0.22, tw * 0.16]
    # header
    rounded(c, tx, ty - 12 * mm, tw, 12 * mm, 6, INK)
    cxp = tx
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11.5)
    for i, h in enumerate(cols):
        c.drawString(cxp + 5 * mm, ty - 8 * mm, h)
        cxp += cws[i]
    ry = ty - 12 * mm
    for ri, row in enumerate(rows):
        rh = 14 * mm
        hi = ri == len(rows) - 1
        rounded(c, tx, ry - rh, tw, rh, 0, ACCENT_SOFT if hi else white, BORDER)
        cxp = tx
        for i, cell in enumerate(row):
            if i == 0:
                c.setFont("Helvetica-Bold", 11.5); c.setFillColor(ACCENT if hi else INK)
            else:
                c.setFont("Helvetica-Bold" if hi else "Helvetica", 11.5); c.setFillColor(INK)
            c.drawString(cxp + 5 * mm, ry - 9 * mm, cell)
            cxp += cws[i]
        ry -= rh

    # variance note + insight callouts
    notes = [
        ("Run-to-run honesty", ACCENT,
         "Prompt Shields is a hosted model, not perfectly deterministic. Across runs: Shields 65–75%, "
         "Full TripWire 75–80% block / 80–90% caught. So we claim a range, not a hero number."),
        ("Why the lift is real", ALLOW,
         "Pattern rules catch known structural attacks instantly; embedding similarity catches novel "
         "phrasings Shields rates as borderline. L2/L3 are zero-false-positive by construction."),
    ]
    cw = (W - 2 * MARGIN - 10 * mm) / 2
    cx = MARGIN
    for t, col, b in notes:
        rounded(c, cx, 22 * mm, cw, 36 * mm, 8, white, BORDER)
        rounded(c, cx, 22 * mm, 4 * mm, 36 * mm, 2, col)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 13)
        c.drawString(cx + 11 * mm, 51 * mm, t)
        wrap(c, b, cx + 11 * mm, 44 * mm, cw - 18 * mm, "Helvetica", 10.5, 5.2 * mm, MUTED)
        cx += cw + 10 * mm
    footer(c); c.showPage()


def s9_market(c):
    bg(c); kicker(c, "Market & business", REVIEW)
    title(c, "A control plane built to be a company")

    # left: chart, right: model + roadmap
    image(c, "c2_market.png", MARGIN, H - 56 * mm, 150 * mm)

    rx = MARGIN + 162 * mm
    rw = W - MARGIN - rx
    blocks = [
        ("Model — open-core", ACCENT,
         "Free OSS engine drives adoption; enterprise tier sells identity, compliance audit ledger, "
         "and the cross-org trust fabric. Bottom-up, developer-led GTM."),
        ("The moat — compounding data", ALLOW,
         "Every blocked attack feeds the L5 classifier and the corpus. Data → identity → compliance "
         "→ network: each layer is harder to copy than the last."),
        ("Why now", REVIEW,
         "Agent deployments are exploding; EU AI Act penalties begin Aug 2026; incumbents guard the "
         "prompt, not the action. The window is open."),
    ]
    by = H - 48 * mm
    for t, col, b in blocks:
        bl = simpleSplit(b, "Helvetica", 11, rw - 14 * mm)
        bh = 14 * mm + len(bl) * 5.4 * mm
        rounded(c, rx, by - bh, rw, bh, 8, white, BORDER)
        rounded(c, rx, by - bh, 4 * mm, bh, 2, col)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 13)
        c.drawString(rx + 11 * mm, by - 9 * mm, t)
        wrap(c, b, rx + 11 * mm, by - 15.5 * mm, rw - 16 * mm, "Helvetica", 11, 5.4 * mm, MUTED)
        by -= bh + 5 * mm
    footer(c); c.showPage()


def s10_roadmap(c):
    bg(c, INK); dotgrid(c)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(ACCENT)
    c.drawString(MARGIN, H - 24 * mm, "ROADMAP, TEAM & THE ASK")
    c.setFont("Helvetica-Bold", 30); c.setFillColor(white)
    c.drawString(MARGIN, H - 38 * mm, "From hackathon prototype to the agent control plane")

    feats = [
        ("F1", "Agent Identity Ledger", "Cryptographic identity + lifecycle for every agent (NHI)."),
        ("F2", "MCP Tool Firewall", "Defeat tool poisoning & rug-pulls — scan + hash-pin + sandbox."),
        ("F3", "Cost & Loop Governor", "Kill runaway agents before the $47K bill."),
        ("F4", "Memory-Poisoning Shield", "Provenance + taint for long-term agent memory."),
        ("F5", "Compliance Audit Ledger", "EU AI Act / SOC2-ready signed action trail."),
        ("V1/V2", "Trust Fabric + Risk Score", "Cross-org network and the data moat."),
    ]
    colw = (W - 2 * MARGIN - 10 * mm) / 3
    y0 = H - 52 * mm
    for i, (tag, name, b) in enumerate(feats):
        cx = MARGIN + (i % 3) * (colw + 5 * mm)
        cyy = y0 - (i // 3) * 34 * mm
        rounded(c, cx, cyy - 30 * mm, colw, 30 * mm, 7, CARD_DK, BORDER_DK)
        rounded(c, cx + 6 * mm, cyy - 12 * mm, 16 * mm, 8 * mm, 3, ACCENT)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(cx + 14 * mm, cyy - 9.5 * mm, tag)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 11.5)
        c.drawString(cx + 25 * mm, cyy - 9.5 * mm, name)
        wrap(c, b, cx + 6 * mm, cyy - 18 * mm, colw - 11 * mm, "Helvetica", 10, 4.9 * mm, HexColor("#aab3cc"))

    # team + status + links
    rounded(c, MARGIN, 22 * mm, W - 2 * MARGIN, 32 * mm, 9, INK2, ACCENT)
    c.setFillColor(ACCENT); c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 10 * mm, 47 * mm, "TEAM")
    c.setFillColor(white); c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN + 10 * mm, 40 * mm, "Kundan Khatri — solo")
    c.setFillColor(HexColor("#aab3cc")); c.setFont("Helvetica", 10.5)
    c.drawString(MARGIN + 10 * mm, 33 * mm, "Architecture · backend · frontend · live demo")
    c.drawString(MARGIN + 10 * mm, 27 * mm, "kundanlm10@gmail.com")

    c.setFillColor(ALLOW); c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 120 * mm, 47 * mm, "SHIPPED")
    c.setFillColor(white); c.setFont("Helvetica", 10.5)
    for i, t in enumerate(["L1 live on Azure · L2/L3 tested · 13 tests green",
                            "Live arena UI + Glass Box trace viewer",
                            "Bicep IaC · honest benchmark · attack corpus"]):
        c.drawString(MARGIN + 120 * mm, 40 * mm - i * 6 * mm, "✓  " + t)

    c.setFillColor(ACCENT2); c.setFont("Helvetica-Bold", 11)
    c.drawRightString(W - MARGIN - 10 * mm, 47 * mm, "github.com/KundanKhatri/Tripwire")
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11)
    c.drawRightString(W - MARGIN - 10 * mm, 40 * mm, "kundankhatri.github.io/Tripwire")
    footer(c, dark=True); c.showPage()


def build():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle("TripWire — Microsoft Build AI 2026 Submission Deck")
    c.setAuthor("Kundan Khatri")
    for slide in (s1_cover, s2_problem, s3_solution, s4_insight, s5_arch,
                  s6_ai, s7_proof, s8_benchmark, s9_market, s10_roadmap):
        slide(c)
    c.save()
    print(f"Wrote {OUT}  ({_pg[0]} slides)")


if __name__ == "__main__":
    build()
