#!/usr/bin/env python3
"""Generate all charts for the TripWire Bible into docs/assets/ as PNGs.

Charts are stylistically consistent with the TripWire brand (dark ink + accent
blue). Run before make_bible_pdf.py.
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ASSETS = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
os.makedirs(ASSETS, exist_ok=True)

INK = "#0a0c16"
INK2 = "#11141f"
ACCENT = "#5b8cff"
ACCENT2 = "#7aa2ff"
BLOCK = "#ff5470"
REVIEW = "#ffb454"
ALLOW = "#3ddc97"
PURPLE = "#b57bff"
TEAL = "#39c5cf"
MUTED = "#8b95b0"
PAPER = "#f7f9ff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#cfd6ea",
    "axes.linewidth": 0.8,
    "text.color": "#1a2030",
    "axes.labelcolor": "#1a2030",
    "xtick.color": "#5b6478",
    "ytick.color": "#5b6478",
    "figure.dpi": 150,
})


def save(fig, name):
    fig.savefig(os.path.join(ASSETS, name), bbox_inches="tight", facecolor="white", dpi=150)
    plt.close(fig)
    print("wrote", name)


# C1 — the gap: 88% incidents vs 6% budget
def c1():
    fig, ax = plt.subplots(figsize=(7, 3.4))
    bars = ax.bar(["Orgs that had an\nagent security incident", "Security budget\nspent on agent risk"],
                  [88, 6], color=[BLOCK, ACCENT], width=0.55)
    for b, v in zip(bars, [88, 6]):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v}%", ha="center",
                fontsize=18, fontweight="bold", color=INK)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of organizations")
    ax.set_title("The gap TripWire sells into", fontsize=13, fontweight="bold", color=INK, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.5, -0.04, "Source: agent-security industry surveys, 2026  [verify]",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "c1_gap.png")


# C2 — market growth
def c2():
    years = ["2026", "2027", "2028", "2029", "2030"]
    agents = [10.8, 17, 26, 38, 50]      # AI agents market $B [verify]
    sec = [2.0, 3.6, 6.2, 10.5, 17]      # agent-security sub-segment $B [verify]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.fill_between(years, agents, color=ACCENT, alpha=0.18)
    ax.plot(years, agents, color=ACCENT, lw=2.5, marker="o", label="AI agents market")
    ax.plot(years, sec, color=BLOCK, lw=2.5, marker="o", label="Agent-security sub-segment")
    for x, y in zip(years, agents):
        ax.text(x, y + 1.5, f"${y:g}B", ha="center", fontsize=8, color=ACCENT)
    for x, y in zip(years, sec):
        ax.text(x, y + 1.5, f"${y:g}B", ha="center", fontsize=8, color=BLOCK)
    ax.set_ylabel("Market size ($B)")
    ax.set_title("Agent + agent-security market, 2026–2030 (~45–50% CAGR)",
                 fontsize=12.5, fontweight="bold", color=INK, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, 58)
    fig.text(0.5, -0.04, "Top-down market figures, public reporting 2026  [verify]",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "c2_market.png")


# C3 — cost runaway multiplier
def c3():
    steps = [1, 5, 10, 20, 35, 50]
    mult = [1, 3.2, 6, 12, 22, 32]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(steps, mult, color=REVIEW, lw=2.6, marker="o")
    ax.fill_between(steps, mult, color=REVIEW, alpha=0.15)
    ax.text(50, 32, "  30x+", color=REVIEW, fontsize=12, fontweight="bold", va="center")
    ax.set_xlabel("Agent steps in a task")
    ax.set_ylabel("Cost vs. a single call")
    ax.set_title("Why agents bankrupt you: cost compounds with steps",
                 fontsize=12.5, fontweight="bold", color=INK, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.5, -0.06, "Documented: an 11-day agent loop cost $47,000.  Source: agentic-failure analyses 2025 [verify]",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "c3_cost.png")


# C4 — revenue mix by tier (stacked) over 3 years
def c4():
    years = ["Year 1", "Year 2", "Year 3"]
    team = [0.36, 1.6, 4.3]
    ent = [0.0, 2.0, 11.0]
    platform = [0.0, 0.4, 3.0]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(years, team, color=ACCENT, label="Team subscriptions")
    ax.bar(years, ent, bottom=team, color=PURPLE, label="Enterprise")
    ax.bar(years, platform, bottom=[t + e for t, e in zip(team, ent)], color=TEAL,
           label="Platform / data (V1–V2)")
    totals = [t + e + p for t, e, p in zip(team, ent, platform)]
    for i, tot in enumerate(totals):
        ax.text(i, tot + 0.4, f"~${tot:.1f}M", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_ylabel("ARR ($M, modeled)")
    ax.set_title("Revenue mix shifts to enterprise + data over time",
                 fontsize=12.5, fontweight="bold", color=INK, pad=10)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, 22)
    fig.text(0.5, -0.04, "Illustrative model; assumptions in BUSINESS_PLAN.md  [verify]",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "c4_revenue.png")


# C5 — GTM funnel
def c5():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.axis("off")
    stages = [
        ("OSS / free SDK adoption", 1.0, ACCENT),
        ("Active dev teams", 0.74, ACCENT2),
        ("Team-tier customers", 0.5, PURPLE),
        ("Enterprise expansion", 0.28, TEAL),
        ("Platform / data + insurance", 0.14, ALLOW),
    ]
    y = 4.6
    for label, w, col in stages:
        x0 = (1 - w) / 2
        ax.add_patch(FancyBboxPatch((x0, y), w, 0.7, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    facecolor=col, edgecolor="none"))
        ax.text(0.5, y + 0.35, label, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white")
        y -= 0.95
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.3, 5.6)
    ax.set_title("Bottom-up GTM: land with developers, expand to enterprise",
                 fontsize=12.5, fontweight="bold", color=INK, pad=4)
    save(fig, "c5_funnel.png")


# C6 — competitive positioning 2x2
def c6():
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    ax.axhline(0, color="#cfd6ea", lw=1)
    ax.axvline(0, color="#cfd6ea", lw=1)
    # x: prompt-only -> full action layer ; y: single-cloud -> provider-agnostic
    pts = [
        ("Prompt/LLM\nfirewalls", -0.6, 0.1, MUTED),
        ("Cloud-native\nAI safety", -0.3, -0.6, MUTED),
        ("ML-security\nincumbents", 0.0, 0.3, MUTED),
        ("TripWire", 0.62, 0.6, ACCENT),
    ]
    for label, x, y, col in pts:
        ax.scatter([x], [y], s=320 if col == ACCENT else 180, color=col,
                   edgecolor="white", zorder=3, linewidth=1.5)
        ax.text(x, y - 0.16, label, ha="center", va="top", fontsize=9.5,
                fontweight="bold" if col == ACCENT else "normal",
                color=INK if col == ACCENT else "#3a4050")
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("Prompt filter  →  full action control plane", fontsize=9.5)
    ax.set_ylabel("Single-cloud  →  provider-agnostic", fontsize=9.5)
    ax.set_title("Positioning: the action-layer + neutral quadrant is open",
                 fontsize=12, fontweight="bold", color=INK, pad=10)
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(False)
    save(fig, "c6_position.png")


# C7 — ARR build line
def c7():
    years = ["Y1", "Y2", "Y3"]
    arr = [0.4, 4.0, 18.0]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    bars = ax.bar(years, arr, color=[ACCENT, PURPLE, TEAL], width=0.5)
    for b, v in zip(bars, arr):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, f"~${v:g}M", ha="center",
                fontsize=12, fontweight="bold", color=INK)
    ax.set_ylabel("ARR ($M, modeled)")
    ax.set_title("Three-year ARR build (illustrative)", fontsize=12.5,
                 fontweight="bold", color=INK, pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, 21)
    fig.text(0.5, -0.05, "Planning model, not a forecast. Assumptions in BUSINESS_PLAN.md  [verify]",
             ha="center", fontsize=8, color=MUTED)
    save(fig, "c7_arr.png")


if __name__ == "__main__":
    c1(); c2(); c3(); c4(); c5(); c6(); c7()
    print("all charts done")
