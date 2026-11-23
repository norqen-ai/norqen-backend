"""Result figures + numbers for the paper/deck (300 dpi). Run from the code/ directory:
   cd code && .venv/bin/python ../06_Assessment_Oct2026/figures/make_results_figs.py
Uses only the project's own modules and real market data."""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, ".")
from src.core.policy import load_policy, load_all_policies
from src.data.market import fetch_ohlcv, add_indicators
from src.backtest.signals import SIGNALS
from src.backtest.engine import run_backtest
from src.eval.calibration import reliability, brier, temperature_scale
from src.eval.cost_quality import frontier

FIG = Path("../06_Assessment_Oct2026/figures")
RUN = Path("logs/exp_obedience_20261004")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
NAVY, GREEN, GOLD, GREY = "#14243A", "#006633", "#B9820F", "#9AA7B2"
out = {}

# ---- 1. obedience figures from the analysed run + proposed size vs cap
for f in ["fig_violations_by_profile.png", "fig_violations_by_clause.png"]:
    shutil.copy(RUN / f, FIG / f)
pols = load_all_policies("config/policies")
order = ["conservative", "long_term", "intraday", "aggressive_growth"]
label = {"conservative": "Conservative", "long_term": "Long-term", "intraday": "Day-trader", "aggressive_growth": "Aggressive"}
cards = [json.loads(l) for l in open(next(RUN.glob("decisions_*.jsonl")))]
def mode(c): return next(x.split(":", 1)[1] for x in c["policy_clauses_applied"] if x.startswith("mode:"))
sizes = {m: {p: [c["position_size_pct"] for c in cards if mode(c) == m and c["policy_name"] == p
                 and c["action"] in ("BUY", "SELL")] for p in order}
         for m in ["guarded", "unguarded_explicit", "unguarded_nl"]}
out["mean_size_acted"] = {m: {p: (float(np.mean(v)) if v else 0.0) for p, v in d.items()} for m, d in sizes.items()}
fig, ax = plt.subplots(figsize=(7.2, 3.6))
x = np.arange(len(order)); w = 0.26
for i, (m, lab, col) in enumerate([("guarded", "Guarded (code)", GREY), ("unguarded_explicit", "LLM + numeric rules", GREEN),
                                   ("unguarded_nl", "LLM + text profile", GOLD)]):
    vals = [out["mean_size_acted"][m][p] for p in order]
    b = ax.bar(x + (i - 1) * w, vals, w, label=lab, color=col)
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.2, f"{v:.1f}", ha="center", fontsize=7.5)
for j, p in enumerate(order):
    cap = pols[p].max_position_pct
    ax.plot([j - 0.45, j + 0.45], [cap, cap], color="#B03A2E", lw=1.6, ls="--")
ax.plot([], [], color="#B03A2E", ls="--", label="Policy cap")
ax.set_xticks(x, [label[p] for p in order]); ax.set_ylabel("Mean position size when trading (%)")
ax.set_title("Proposed position size vs. the investor's cap")
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, fontsize=8, ncol=2)
fig.tight_layout(); fig.savefig(FIG / "fig_size_vs_cap.png", dpi=300); plt.close(fig)
print("obedience figures done", flush=True)

# ---- 2. numeric baselines over the frozen universe (real 3-year daily data)
uni = json.load(open("config/universe.json"))
tickers = (uni["US"] + uni["NSE"])[:10]
pol = load_policy("config/policies/long_term.json")
dfs = {}
for t in tickers:
    try:
        dfs[t] = add_indicators(fetch_ohlcv(t, period="3y"))
    except Exception as e:
        print("skip", t, e)
out["baseline_tickers"] = list(dfs)

ic = {}
for name, fn in SIGNALS.items():
    vals = [run_backtest(df, pol, fn, signal_name=name).ic for df in dfs.values()]
    vals = [v for v in vals if np.isfinite(v["IC"])]
    ic[name] = {"mean_IC": float(np.mean([v["IC"] for v in vals])),
                "sig_frac": float(np.mean([abs(v["t_stat"]) > 2 for v in vals]))}
out["ic"] = ic
print("IC done", ic, flush=True)

conf, corr = [], []
for df in dfs.values():
    for d in run_backtest(df, pol, SIGNALS["combo"], signal_name="combo").decisions:
        if abs(d["direction"]) >= 0.15:
            conf.append(d["confidence"]); corr.append(int(np.sign(d["direction"]) == np.sign(d["fwd_return"])))
rows, ece, mce = reliability(conf, corr)
T, ece_after = temperature_scale(conf, corr)
c = np.clip(np.array(conf), 1e-4, 1 - 1e-4)
scaled = 1 / (1 + np.exp(-np.log(c / (1 - c)) / T))
rows_s, _, _ = reliability(scaled, corr)
out["calibration"] = {"n": len(conf), "base_acc": float(np.mean(corr)), "ECE": ece, "MCE": mce,
                      "Brier": brier(conf, corr), "T": T, "ECE_after": ece_after,
                      "Brier_after": brier(scaled, corr)}
fig, ax = plt.subplots(figsize=(5.4, 4.0))
ax.plot([0, 1], [0, 1], color=GREY, ls="--", lw=1, label="Perfect calibration")
ax.plot([r["conf"] for r in rows], [r["acc"] for r in rows], "o-", color=GOLD, lw=1.8,
        label=f"Raw confidence (ECE {ece:.3f})")
ax.plot([r["conf"] for r in rows_s], [r["acc"] for r in rows_s], "s-", color=GREEN, lw=1.8,
        label=f"After temperature scaling (ECE {ece_after:.3f})")
ax.set_xlabel("Stated confidence"); ax.set_ylabel("Observed accuracy"); ax.set_xlim(0.2, 0.85); ax.set_ylim(0.2, 0.85)
ax.set_title("Is the stated confidence accurate?")
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(FIG / "fig_reliability.png", dpi=300); plt.close(fig)
print("calibration done", out["calibration"], flush=True)

fr = frontier(list(dfs.values())[:8], thresholds=[0.30, 0.40, 0.50, 0.60, 0.65])
out["cost_quality"] = fr
fig, ax1 = plt.subplots(figsize=(5.4, 3.6))
th = [r["threshold"] for r in fr]
ax1.plot(th, [r["mean_cost"] for r in fr], "o-", color=NAVY, lw=1.8, label="Evidence used (sources)")
ax1.set_xlabel("Stopping threshold (confidence needed to stop)"); ax1.set_ylabel("Mean evidence sources used", color=NAVY)
ax2 = ax1.twinx()
ax2.plot(th, [r["accuracy"] * 100 for r in fr], "s-", color=GOLD, lw=1.8, label="Directional accuracy (%)")
ax2.set_ylabel("Directional accuracy (%)", color=GOLD); ax2.set_ylim(40, 60)
ax1.set_title("More evidence, same accuracy")
for a in (ax1, ax2):
    a.spines[["top"]].set_visible(False)
fig.legend(frameon=False, fontsize=8, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(FIG / "fig_cost_quality.png", dpi=300); plt.close(fig)
print("cost-quality done", fr, flush=True)

(FIG / "results_numbers.json").write_text(json.dumps(out, indent=2))
print("ALL DONE")
