"""Block diagram + flowchart for the paper (300 dpi). Drawn from the actual architecture."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

OUT = __file__.rsplit("/", 1)[0]
NAVY, GREEN, GOLD, RED, GREY = "#14243A", "#006633", "#B9820F", "#B03A2E", "#5C6B7A"
FILL = {"in": "#EAF2FB", "proc": "#EEF6F1", "out": "#FFF6E5", "risk": "#FBECEA", "eval": "#F1EEF8"}
plt.rcParams.update({"font.family": "DejaVu Sans"})


def box(ax, x, y, w, h, title, sub="", kind="proc", edge=NAVY, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=FILL[kind], ec=edge, lw=1.3))
    ax.text(x + w / 2, y + h / 2 + (0.13 if sub else 0), title, ha="center", va="center",
            fontsize=fs, weight="bold", color=NAVY)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.2, sub, ha="center", va="center", fontsize=7.4, color=GREY)


def arrow(ax, x1, y1, x2, y2, text="", color=NAVY, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2, linestyle=ls, mutation_scale=11))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.1, text, ha="center", fontsize=7, color=GREY,
                bbox=dict(fc="white", ec="none", pad=0.5))


# ------------------------------------------------------------------ block diagram
fig, ax = plt.subplots(figsize=(10, 5.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
for x, lab in [(0.25, "INPUT"), (3.15, "PROCESSING"), (7.55, "OUTPUT")]:
    ax.text(x, 5.35, lab, fontsize=8.5, weight="bold", color=GOLD)

box(ax, 0.2, 3.75, 2.4, 1.2, "Market data", "prices · news · company\nnumbers · index trend", "in")
box(ax, 0.2, 2.15, 2.4, 1.2, "Investor policy (JSON)", "limits · tool order ·\nconfidence bar · budget", "in")
box(ax, 0.2, 0.55, 2.4, 1.2, "Provider layer", "Yahoo Finance · Finnhub\n(any US / NSE ticker)", "in")

box(ax, 3.1, 3.75, 3.6, 1.2, "Policy-conditioned planner", "LangGraph: gather evidence in policy order,\nstop when confident or budget spent")
box(ax, 3.1, 2.15, 3.6, 1.2, "Evidence agents", "LLM: technical · news · fundamental · macro\nML: logistic-regression predictor")
box(ax, 3.1, 0.55, 1.7, 1.2, "Decision", "guarded (code)\nor LLM-proposed", fs=9)
box(ax, 5.0, 0.55, 1.7, 1.2, "Risk engine", "deterministic\nveto, no AI", "risk", RED, fs=9)

box(ax, 7.5, 3.75, 2.3, 1.2, "Decision card", "action · size · stop ·\nconfidence · reasons", "out")
box(ax, 7.5, 2.15, 2.3, 1.2, "Audit log + bundle", "JSONL record, frozen\nevidence for replay", "out")
box(ax, 7.5, 0.55, 2.3, 1.2, "Evaluation suite", "obedience · calibration ·\ncost · quant metrics", "eval", "#5B4B8A")

arrow(ax, 2.6, 4.35, 3.1, 4.35)
arrow(ax, 2.6, 2.75, 3.1, 4.1, "governs")
arrow(ax, 2.6, 1.15, 3.1, 2.55)
arrow(ax, 4.9, 3.75, 4.9, 3.35, "consult")
arrow(ax, 4.1, 2.15, 4.0, 1.75)
arrow(ax, 4.8, 1.15, 5.0, 1.15)
arrow(ax, 6.7, 1.15, 7.5, 4.2, "approved / vetoed")
arrow(ax, 8.65, 3.75, 8.65, 3.35)
arrow(ax, 8.65, 2.15, 8.65, 1.75)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_block_diagram.png", dpi=300)
plt.close(fig)


# ------------------------------------------------------------------ flowchart
def term(ax, cx, cy, text):
    ax.add_patch(FancyBboxPatch((cx - 1.4, cy - 0.22), 2.8, 0.44, boxstyle="round,pad=0.02,rounding_size=0.22",
                                fc=NAVY, ec=NAVY))
    ax.text(cx, cy, text, ha="center", va="center", color="white", fontsize=8.5, weight="bold")


def step(ax, cx, cy, text, w=2.9, h=0.5, kind="proc", edge=NAVY):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=FILL[kind], ec=edge, lw=1.1))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=7.8, color=NAVY)


def diamond(ax, cx, cy, text, w=2.9, h=0.85):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)],
                         closed=True, fc="#FFF6E5", ec=GOLD, lw=1.2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=7.4, color=NAVY)


fig, ax = plt.subplots(figsize=(6.4, 9.6))
ax.set_xlim(0, 6.4); ax.set_ylim(0, 9.6); ax.axis("off")
cx = 2.3
term(ax, cx, 9.25, "Start: ticker + investor policy")
step(ax, cx, 8.55, "Fetch data; build tool queue in policy order\n(skip forbidden tools)")
step(ax, cx, 7.75, "Call next evidence agent → direction, confidence")
step(ax, cx, 6.95, "Aggregate evidence (reliability-weighted);\nadd cost")
diamond(ax, cx, 5.95, "confidence ≥ bar and ≥2 items,\nor budget spent, or queue empty?")
diamond(ax, cx, 4.7, "Decision mode?")
step(ax, 0.95, 3.6, "Guarded: code sets\naction + vol-target size", w=1.75, h=0.62)
step(ax, 3.65, 3.6, "Unguarded: LLM proposes\naction, size, stop", w=1.85, h=0.62)
step(ax, cx, 2.55, "Risk engine: size cap · stop-loss · confidence ·\ndaily loss · forbidden evidence", kind="risk", edge=RED)
diamond(ax, cx, 1.55, "All checks pass?", h=0.7)
step(ax, 5.15, 1.55, "VETO + reasons", w=1.6, h=0.46, kind="risk", edge=RED)
step(ax, cx, 0.75, "Log decision card + evidence (JSONL)", kind="out")
term(ax, cx, 0.2, "End")

arrow(ax, cx, 9.03, cx, 8.8); arrow(ax, cx, 8.3, cx, 8.0); arrow(ax, cx, 7.5, cx, 7.2)
arrow(ax, cx, 6.7, cx, 6.38)
ax.annotate("", xy=(cx + 1.45, 7.75), xytext=(cx + 1.45, 5.95),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.1, connectionstyle="angle,angleA=0,angleB=90,rad=0"))
ax.text(cx + 1.6, 6.85, "no", fontsize=7.5, color=GREY)
arrow(ax, cx, 5.52, cx, 5.12); ax.text(cx + 0.1, 5.3, "yes", fontsize=7.5, color=GREY)
arrow(ax, cx - 0.5, 4.45, 0.95, 3.92); arrow(ax, cx + 0.5, 4.45, 3.65, 3.92)
arrow(ax, 0.95, 3.29, cx - 0.4, 2.8); arrow(ax, 3.65, 3.29, cx + 0.4, 2.8)
arrow(ax, cx, 2.3, cx, 1.9); arrow(ax, cx + 1.45, 1.55, 4.35, 1.55); ax.text(3.95, 1.65, "no", fontsize=7.5, color=GREY)
arrow(ax, cx, 1.2, cx, 1.0); ax.text(cx + 0.1, 1.07, "yes", fontsize=7.5, color=GREY)
ax.annotate("", xy=(cx + 1.45, 0.75), xytext=(5.15, 1.32),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.1, connectionstyle="angle,angleA=-90,angleB=0,rad=0"))
arrow(ax, cx, 0.5, cx, 0.42)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_flowchart.png", dpi=300)
plt.close(fig)
print("wrote fig_block_diagram.png, fig_flowchart.png")
