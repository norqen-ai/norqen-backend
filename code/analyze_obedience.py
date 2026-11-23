"""Analyse an obedience run (see run_obedience.py).

  python3 analyze_obedience.py logs/exp_obedience_20261004

Writes report.md, summary.csv and 300-dpi figures into the run folder. Violation clauses
use the pre-registered definitions in src/eval/adherence.py::check_card.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.core.policy import load_all_policies
from src.eval.adherence import check_card, ACTED

CLAUSES = ["oversize", "bad_stop", "under_confidence"]
MODES = ["guarded", "unguarded_explicit", "unguarded_nl"]
MODE_LABEL = {"guarded": "Guarded (code)", "unguarded_explicit": "LLM + numeric rules",
              "unguarded_nl": "LLM + text profile"}
POL_ORDER = ["conservative", "long_term", "intraday", "aggressive_growth"]
POL_LABEL = {"conservative": "Conservative", "long_term": "Long-term",
             "intraday": "Day-trader", "aggressive_growth": "Aggressive"}


def mode_of(card):
    m = [x for x in card.get("policy_clauses_applied", []) if x.startswith("mode:")]
    return m[0].split(":", 1)[1] if m else "guarded"


def boot_ci(x, n=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def main(run_dir: str):
    run = Path(run_dir)
    cards = [json.loads(l) for f in sorted(run.glob("decisions_*.jsonl")) for l in open(f) if l.strip()]
    policies = load_all_policies("config/policies")
    rows = []
    for c in cards:
        pol = policies[c["policy_name"]]
        v, acted = check_card(c, pol)
        rows.append({"mode": mode_of(c), "policy": c["policy_name"], "ticker": c["ticker"],
                     "market": "NSE" if c["ticker"].upper().endswith(".NS") else "US",
                     "action": c["action"], "acted": acted, "size": c["position_size_pct"],
                     "stop": c["stop_loss_pct"], "conf": c["confidence"],
                     "vetoed": c["risk_verdict"] == "VETOED",
                     **{k: bool(v[k]) for k in CLAUSES}, "any": any(v[k] for k in CLAUSES)})

    out, csv_rows = [], []
    out.append(f"# Obedience run — {run.name}\n\n{len(rows)} decisions · "
               f"{len({r['ticker'] for r in rows})} stocks · modes: {', '.join(sorted({r['mode'] for r in rows}))}\n")

    # ---- per mode x policy
    out.append("## Violation rates by mode and investor profile\n")
    out.append("| Mode | Profile | N | Acted | Mean size (acted) | Oversize | Loose/missing stop | Acted below conf. bar | Any violation | Vetoed |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for m in MODES:
        for p in POL_ORDER:
            g = [r for r in rows if r["mode"] == m and r["policy"] == p]
            if not g:
                continue
            acted = [r for r in g if r["acted"]]
            rec = {"mode": m, "policy": p, "N": len(g),
                   "acted_rate": np.mean([r["acted"] for r in g]),
                   "mean_size_acted": np.mean([r["size"] for r in acted]) if acted else 0.0,
                   **{k: np.mean([r[k] for r in g]) for k in CLAUSES},
                   "any": np.mean([r["any"] for r in g]), "veto": np.mean([r["vetoed"] for r in g])}
            csv_rows.append(rec)
            out.append(f"| {MODE_LABEL[m]} | {POL_LABEL[p]} | {rec['N']} | {rec['acted_rate']:.0%} | "
                       f"{rec['mean_size_acted']:.2f}% | {rec['oversize']:.0%} | {rec['bad_stop']:.0%} | "
                       f"{rec['under_confidence']:.0%} | **{rec['any']:.0%}** | {rec['veto']:.0%} |")

    # ---- per mode overall with CI, and by market
    out.append("\n## Overall, with 95% bootstrap CI, and by market\n")
    out.append("| Mode | N | Any violation [95% CI] | Violation among ACTED | US | NSE | Act rate |")
    out.append("|---|---|---|---|---|---|---|")
    overall = {}
    for m in MODES:
        g = [r for r in rows if r["mode"] == m]
        if not g:
            continue
        lo, hi = boot_ci([r["any"] for r in g])
        acted = [r for r in g if r["acted"]]
        us = [r["any"] for r in g if r["market"] == "US"]
        ns = [r["any"] for r in g if r["market"] == "NSE"]
        overall[m] = {"any": np.mean([r["any"] for r in g]), "lo": lo, "hi": hi}
        out.append(f"| {MODE_LABEL[m]} | {len(g)} | {overall[m]['any']:.1%} [{lo:.1%}, {hi:.1%}] | "
                   f"{(np.mean([r['any'] for r in acted]) if acted else 0):.1%} (n={len(acted)}) | "
                   f"{(np.mean(us) if us else float('nan')):.1%} | {(np.mean(ns) if ns else float('nan')):.1%} | "
                   f"{np.mean([r['acted'] for r in g]):.0%} |")

    # ---- divergence on identical evidence
    out.append("\n## Do profiles behave differently on identical evidence?\n")
    out.append("| Mode | Stock moments | Action labels differ | Full decision differs (action+size+stop) | Mean size spread when ≥2 act |")
    out.append("|---|---|---|---|---|")
    for m in MODES:
        by_t = defaultdict(dict)
        for r in rows:
            if r["mode"] == m:
                by_t[r["ticker"]][r["policy"]] = (r["action"], r["size"], r["stop"])
        moments = [d for d in by_t.values() if len(d) >= 2]
        if not moments:
            continue
        act = np.mean([len({v[0] for v in d.values()}) > 1 for d in moments])
        full = np.mean([len(set(d.values())) > 1 for d in moments])
        spreads = [max(s) - min(s) for d in moments
                   for s in [[v[1] for v in d.values() if v[0] in ACTED]] if len(s) >= 2]
        out.append(f"| {MODE_LABEL[m]} | {len(moments)} | {act:.0%} | {full:.0%} | "
                   f"{(np.mean(spreads) if spreads else 0):.2f}% |")

    # ---- what the risk engine caught
    vet = [r for r in rows if r["vetoed"] and r["mode"] != "guarded"]
    out.append(f"\n## Deterministic-layer interventions\n\nThe risk engine vetoed **{len(vet)}** unguarded "
               f"proposals. By clause: " + ", ".join(f"{k} {sum(r[k] for r in vet)}" for k in CLAUSES) + ".\n")

    (run / "report.md").write_text("\n".join(out))
    with open(run / "summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)
    make_figures(run, csv_rows, overall)
    print("\n".join(out))


def make_figures(run, csv_rows, overall):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    colors = {"guarded": "#9AA7B2", "unguarded_explicit": "#006633", "unguarded_nl": "#B9820F"}

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    w = 0.26
    x = np.arange(len(POL_ORDER))
    for i, m in enumerate(MODES):
        vals = [next((r["any"] * 100 for r in csv_rows if r["mode"] == m and r["policy"] == p), 0) for p in POL_ORDER]
        b = ax.bar(x + (i - 1) * w, vals, w, label=MODE_LABEL[m], color=colors[m])
        for rect, v in zip(b, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 1, f"{v:.0f}", ha="center", fontsize=8)
    ax.set_xticks(x, [POL_LABEL[p] for p in POL_ORDER])
    ax.set_ylabel("Decisions breaking the mandate (%)")
    ax.set_title("Mandate violations on identical evidence, by investor profile")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_ylim(0, max(10, ax.get_ylim()[1] * 1.15))
    fig.tight_layout()
    fig.savefig(run / "fig_violations_by_profile.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    labels = {"oversize": "Position above cap", "bad_stop": "Stop-loss missing/too loose",
              "under_confidence": "Acted below confidence bar"}
    x = np.arange(len(CLAUSES))
    for i, m in enumerate(MODES):
        g = [r for r in csv_rows if r["mode"] == m]
        if not g:
            continue
        tot = sum(r["N"] for r in g)
        vals = [sum(r[k] * r["N"] for r in g) / tot * 100 for k in CLAUSES]
        b = ax.bar(x + (i - 1) * w, vals, w, label=MODE_LABEL[m], color=colors[m])
        for rect, v in zip(b, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
    ax.set_xticks(x, [labels[k] for k in CLAUSES])
    ax.set_ylabel("Share of decisions (%)")
    ax.set_title("Which rule gets broken?")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(run / "fig_violations_by_clause.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "logs/exp_obedience_20261004")
