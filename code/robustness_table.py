"""Robustness table for the paper: re-computes the headline estimates under each analysis variant.

Variants (each produced by analyze_components.py):
  analysis            primary (pre-registered)
  analysis_H20        common 20-day horizon for every profile      (pre-registered robustness)
  analysis_core40     original 40-stock universe only               (pre-registered robustness)
  analysis_cost_zero  no trading costs                              (exploratory)
  analysis_cost_low_nse  NSE round trip 15 bp instead of 36 bp      (exploratory)
Writes <paper>/tables/robustness.tex and <paper>/tables/macros_rob.tex.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analyze_components import auc, boot_mean

VARIANTS = [("analysis", "Primary (19 mo.)", "Prim"), ("analysis_ext", "Extended (25 mo.)", "Ext"), ("analysis_H20", "Common $H=20$", "Hh"),
            ("analysis_core40", "Original 40 stocks", "Core"), ("analysis_cost_low_nse", "NSE cost 15\\,bp", "Low"),
            ("analysis_cost_zero", "Zero costs", "Zero")]


def estimates(df: pd.DataFrame) -> dict:
    nl = df[df["style"] == "nl"].copy()
    tr = nl[nl["u_trade"]].copy()
    nl["d_sel"] = nl["unit_u"] - nl["unit_c"]
    tr["d_exit"] = (tr["ret_llmexit"] - tr["ret_pol"]) * 100
    out = {"auc": auc(tr["u_conf"], tr["ret_pol"] > 0),
           "rho": spearmanr(tr["u_size"], tr["ret_pol"])[0],
           "sel": boot_mean(nl, "d_sel"), "exit": boot_mean(tr, "d_exit"),
           "llm_trade": boot_mean(tr, "unit_u")}
    for g in ("block", "repair"):
        nl[f"d_{g}"] = nl[f"pnl_{g}"] - nl["pnl_raw"]
        out[g] = boot_mean(nl, f"d_{g}")
    cons = nl[nl["policy"] == "conservative"]
    out["block_cons"] = boot_mean(cons, "d_block")
    aggr = nl[nl["policy"] == "aggressive_growth"]
    out["block_aggr"] = boot_mean(aggr, "d_block")
    cv = lambda c: float(nl[c][nl[c] <= nl[c].quantile(0.05)].mean())
    for nm in ("raw", "repair", "code", "block"):
        out[f"cvar_{nm}"] = cv(f"pnl_{nm}")
        out[f"sd_{nm}"] = float(nl[f"pnl_{nm}"].std())
        out[f"mean_{nm}"] = float(nl[f"pnl_{nm}"].mean())
    for g in ("block", "repair"):
        nl[f"dx_{g}"] = nl[f"pnlx_{g}"] - nl["pnlx_raw"]
        out[f"x_{g}"] = boot_mean(nl, f"dx_{g}")
    stop = nl[(nl["verdict"] == "VETOED") & (nl["clause"] == "stop")]
    out["stop_only"] = boot_mean(stop, "d_block") if len(stop) else (np.nan,) * 3
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="logs/exp_pit_20261012")
    ap.add_argument("--paper", default="../07_ICAIF_AI4F_2026/paper")
    a = ap.parse_args()
    exp, paper = Path(a.exp), Path(a.paper)
    c = lambda t: f"{t[0]:+.2f} [{t[1]:+.2f}, {t[2]:+.2f}]"
    rows, macros = [], []
    for d, label, tag in VARIANTS:
        p = exp / d / "scored.pkl"
        if not p.exists():
            print("missing", p)
            continue
        e = estimates(pd.read_pickle(p))
        rows.append(f"{label} & {e['auc']:.3f} & {e['rho']:+.3f} & {c(e['sel'])} & {c(e['block'])} & "
                    f"{c(e['block_cons'])} & {c(e['stop_only'])} \\\\")
        for k in ("cvar_raw", "cvar_repair", "cvar_code", "sd_raw", "sd_repair", "sd_code", "mean_raw", "mean_repair", "mean_code"):
            macros.append(f"\\newcommand{{\\rob{tag}{k.replace('_', '').capitalize()}}}{{{e[k]:.{0 if 'cvar' in k else (1 if 'sd' in k else 2)}f}}}")
        for k in ("block", "repair", "block_cons", "block_aggr", "stop_only", "sel", "exit", "llm_trade", "x_block", "x_repair"):
            macros.append(f"\\newcommand{{\\rob{tag}{k.replace('_', '').capitalize()}}}{{{c(e[k])}}}")
        macros.append(f"\\newcommand{{\\rob{tag}Auc}}{{{e['auc']:.3f}}}")
        macros.append(f"\\newcommand{{\\rob{tag}Rho}}{{{e['rho']:+.3f}}}")
        print(label, {k: (round(float(v), 3) if not isinstance(v, tuple) else tuple(round(x, 2) for x in v)) for k, v in e.items()})
    tex = ["\\begin{tabular}{lrrrrrr}", "\\toprule",
           "Variant & AUC & $\\rho$ & T: LLM$-$code & Block $\\Delta u$ & Block, cons. & Stop-only veto \\\\",
           "\\midrule", *rows, "\\bottomrule", "\\end{tabular}"]
    (paper / "tables" / "robustness.tex").write_text("\n".join(tex))
    (paper / "tables" / "macros_rob.tex").write_text("\n".join(macros) + "\n")
    print("written robustness.tex,", len(macros), "macros")


if __name__ == "__main__":
    main()
