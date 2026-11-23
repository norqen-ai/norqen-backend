"""Checks added in response to an internal review (13 Oct 2026). All exploratory unless noted.

  1. News point-in-time audit: every cached headline vs the next session's open.
  2. Dependence: moving-block bootstrap over consecutive months (overlapping holds) and a
     two-way (month x stock) cluster bootstrap, for the headline estimates.
  3. Naive baselines: always-WAIT and always-long at the profile cap with policy exits.
  4. Guardrail decomposition: Repair vs exposure-matched (de-levered) Raw.
  5. Helpful/harmful threshold sensitivity.
  6. Holm correction over the pre-registered primary family.
Writes <paper>/tables/macros_rev.tex, <paper>/tables/baselines.tex and <exp>/analysis/reviewer_checks.json.
"""
from __future__ import annotations

import glob
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analyze_components import auc
from src.core.policy import load_all_policies
from src.pit.data import ROOT, decision_dates
from src.pit.outcomes import HORIZON, evaluate

EXP = Path("logs/exp_pit_20261012")
PAPER = Path("../07_ICAIF_AI4F_2026/paper")
POL = load_all_policies("config/policies")
B = 2000
OPEN_UTC = {"US": 13.5, "IN": 3.75}       # session open, hours UTC (NYSE 09:30 ET in EDT ~13:30; NSE 09:15 IST)


def boot(df, col, unit="month", block=1, twoway=False, seed=20261012):
    """Mean of col with a bootstrap CI. unit-cluster bootstrap; block>1 = moving blocks of consecutive
    months; twoway = resample months and stocks independently (pigeonhole two-way bootstrap)."""
    rng = np.random.default_rng(seed)
    x = df[[unit, "ticker", col]].dropna()
    if twoway:
        months, stocks = x[unit].unique(), x["ticker"].unique()
        g = x.groupby([unit, "ticker"])[col].agg(["sum", "count"])
        bs = []
        for _ in range(500):
            mw = pd.Series(np.bincount(rng.integers(0, len(months), len(months)), minlength=len(months)), index=months)
            sw = pd.Series(np.bincount(rng.integers(0, len(stocks), len(stocks)), minlength=len(stocks)), index=stocks)
            w = mw.reindex(g.index.get_level_values(0)).to_numpy() * sw.reindex(g.index.get_level_values(1)).to_numpy()
            bs.append((g["sum"].to_numpy() * w).sum() / max((g["count"].to_numpy() * w).sum(), 1))
        m = x[col].mean()
        return m, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), np.array(bs)
    g = x.groupby(unit)[col].agg(["sum", "count"]).sort_index()
    s, n = g["sum"].to_numpy(), g["count"].to_numpy()
    k = len(g)
    nb = int(np.ceil(k / block))
    starts = rng.integers(0, k - block + 1, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(B, -1)[:, :k]
    bs = s[idx].sum(1) / n[idx].sum(1)
    return float(s.sum() / n.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), bs


def pval(bs, null=0.0):
    return float(min(1.0, 2 * min((bs <= null).mean(), (bs >= null).mean())))


def main():
    out, M = {}, {}
    c = lambda t, d=2: f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"

    # ------------------------------------------------------------------ 1. news audit
    n_items = n_bad = 0
    lead = []
    for f in glob.glob(str(ROOT / "news" / "*.json")):
        name = Path(f).stem
        tk, d = name.rsplit("_", 1)
        reg = "IN" if tk.endswith(".NS") else "US"
        items = json.loads(Path(f).read_text())
        t = pd.Timestamp(d)
        nxt = t + pd.Timedelta(days=1)
        open_ts = datetime(nxt.year, nxt.month, nxt.day, tzinfo=timezone.utc).timestamp() + OPEN_UTC[reg] * 3600
        for it in items:
            n_items += 1
            if it["ts"] >= open_ts:
                n_bad += 1
            lead.append((open_ts - it["ts"]) / 3600)
    lead = np.array(lead)
    out["news"] = {"headlines": n_items, "after_next_open": n_bad, "min_lead_h": float(lead.min()),
                   "median_lead_h": float(np.median(lead))}
    M["newsN"] = f"{n_items:,}".replace(",", "{,}")
    M["newsBad"] = str(n_bad)
    M["newsMinLead"] = f"{lead.min():.1f}"
    print("news audit", out["news"])

    # ------------------------------------------------------------------ load scored decisions
    df = pd.read_pickle(EXP / "analysis" / "scored.pkl")
    df["mi"] = df["month"].rank(method="dense").astype(int)
    nl = df[df["style"] == "nl"].copy()
    tr = nl[nl["u_trade"]].copy()
    nl["d_sel"] = nl["unit_u"] - nl["unit_c"]
    nl["d_block"] = nl["pnl_block"] - nl["pnl_raw"]
    nl["d_repair"] = nl["pnl_repair"] - nl["pnl_raw"]
    tr["d_exit"] = (tr["ret_llmexit"] - tr["ret_pol"]) * 100
    tr["z_llm"] = tr["u_size"] / 100 * tr["ret_pol"] * 1e4
    tr["z_eq"] = tr.groupby(["model", "policy"])["u_size"].transform("mean") / 100 * tr["ret_pol"] * 1e4
    tr["d_size"] = tr["z_llm"] - tr["z_eq"]

    # ------------------------------------------------------------------ 2. dependence-robust intervals
    rows = []
    for key, frame, col in [("sel", nl, "d_sel"), ("size", tr, "d_size"), ("exit", tr, "d_exit"),
                            ("block", nl, "d_block"), ("repair", nl, "d_repair")]:
        a = boot(frame, col, "mi")
        b2 = boot(frame, col, "mi", block=2)
        b3 = boot(frame, col, "mi", block=3)
        tw = boot(frame, col, "mi", twoway=True)
        rows.append({"est": key, "month": a[:3], "block2": b2[:3], "block3": b3[:3], "twoway": tw[:3],
                     "p_block2": pval(b2[3])})
        M[f"rev{key.capitalize()}Btwo"] = c(b2[:3])
        M[f"rev{key.capitalize()}Bthree"] = c(b3[:3])
        M[f"rev{key.capitalize()}Tw"] = c(tw[:3])
    out["dependence"] = rows
    # AUC with 2-month moving-block bootstrap
    rng = np.random.default_rng(1)
    months = sorted(tr["mi"].unique())
    by = {m: tr[tr["mi"] == m] for m in months}
    bs = []
    for _ in range(400):
        st = rng.integers(0, len(months) - 1, size=int(np.ceil(len(months) / 2)))
        sel = [months[min(s0 + j, len(months) - 1)] for s0 in st for j in (0, 1)][:len(months)]
        smp = pd.concat([by[m] for m in sel])
        bs.append(auc(smp["u_conf"], smp["ret_pol"] > 0))
    a0 = auc(tr["u_conf"], tr["ret_pol"] > 0)
    M["revAucBtwo"] = f"{a0:.3f} [{np.percentile(bs, 2.5):.3f}, {np.percentile(bs, 97.5):.3f}]"
    p_auc = float(min(1, 2 * min((np.array(bs) <= 0.5).mean(), (np.array(bs) >= 0.5).mean())))
    print("dependence", json.dumps(rows, default=lambda o: [round(v, 3) for v in o] if isinstance(o, tuple) else o)[:900])

    # ------------------------------------------------------------------ 3. naive baselines (per bundle x profile)
    base = df[(df["model"] == df["model"].iloc[0]) & (df["style"] == "nl")][["ticker", "date", "region", "policy", "month",
                                                                           "pnl_code"]].copy()
    longs = []
    for r in base.itertuples():
        p = POL[r.policy]
        o = evaluate(r.ticker, r.date, "BUY", p.max_position_pct, p.stop_loss_pct, p.take_profit_pct, HORIZON[r.policy])
        longs.append(o["pnl"])
    base["pnl_long"] = longs
    base["pnl_wait"] = 0.0
    cv = lambda v: float(v[v <= v.quantile(0.05)].mean())
    brows = []
    for nm, col in [("Always WAIT", "pnl_wait"), ("Always long at cap", "pnl_long"), ("Code", "pnl_code")]:
        m = boot(base, col, "month", block=2)
        brows.append((nm, m[:3], float(base[col].std()), cv(base[col])))
    for nm, col in [("Raw LLM (persona)", "pnl_raw"), ("Repair (persona)", "pnl_repair")]:
        m = boot(nl, col, "month", block=2)
        brows.append((nm, m[:3], float(nl[col].std()), cv(nl[col])))
    L = [r"\begin{tabular}{lrrr}", r"\toprule", r"Decision rule & Mean P\&L (bp) [95\% CI] & SD & CVaR$_5$ \\", r"\midrule"]
    for nm, m, sd, cvar in brows:
        L.append(f"{nm} & {c(m)} & {sd:.1f} & {cvar:.0f} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "tables" / "baselines.tex").write_text("\n".join(L))
    M["baseLong"] = c(brows[1][1])
    M["baseLongSd"] = f"{brows[1][2]:.1f}"
    out["baselines"] = [(nm, m, sd, cvar) for nm, m, sd, cvar in brows]
    print("baselines", brows)

    # ------------------------------------------------------------------ 4. guardrail decomposition: exposure-matched raw
    g = nl.groupby(["model", "policy"])
    nl["k"] = g["size_repair"].transform("sum") / g["size_raw"].transform("sum")
    nl["pnl_raw_scaled"] = nl["k"] * nl["pnl_raw"]
    nl["d_rep_vs_scaled"] = nl["pnl_repair"] - nl["pnl_raw_scaled"]
    k_all = nl["size_repair"].sum() / nl["size_raw"].sum()
    m_sc = boot(nl, "pnl_raw_scaled", "mi", block=2)
    d_sc = boot(nl, "d_rep_vs_scaled", "mi", block=2)
    out["decomp"] = {"exposure_ratio": float(k_all), "mean_scaled_raw": m_sc[:3], "sd_scaled_raw": float(nl["pnl_raw_scaled"].std()),
                     "sd_repair": float(nl["pnl_repair"].std()), "repair_minus_scaled": d_sc[:3],
                     "cvar_scaled_raw": cv(nl["pnl_raw_scaled"]), "cvar_repair": cv(nl["pnl_repair"])}
    M["decK"] = f"{k_all:.2f}"
    M["decScaledSd"] = f"{nl['pnl_raw_scaled'].std():.1f}"
    M["decScaledCvar"] = f"{cv(nl['pnl_raw_scaled']):.0f}"
    M["decRepMinusScaled"] = c(d_sc[:3])
    print("decomp", out["decomp"])

    # ------------------------------------------------------------------ 5. threshold sensitivity (block, nl)
    x = nl[(nl["size_block"] != nl["size_raw"]) | (nl["trade_block"] != nl["trade_raw"]) | (nl["d_block"].abs() > 1e-9)]
    sens = {}
    for eps in (0.0, 0.5, 2.0):
        h, k = int((x["d_block"] > eps).sum()), int((x["d_block"] < -eps).sum())
        sens[eps] = h / max(h + k, 1)
    out["eps"] = sens
    M["epsZero"], M["epsHalf"], M["epsTwo"] = (f"{100 * sens[e]:.0f}\\%" for e in (0.0, 0.5, 2.0))

    # ------------------------------------------------------------------ 6. Holm over the primary family
    prim = {"AUC = 0.5": p_auc}
    for r in rows:
        prim[r["est"]] = r["p_block2"]
    rho, p_rho = spearmanr(tr["u_size"], tr["ret_pol"])
    prim["rho = 0"] = float(p_rho)
    order = sorted(prim.items(), key=lambda kv: kv[1])
    holm, m_ = {}, len(order)
    running = 0.0
    for i, (k_, p_) in enumerate(order):
        running = max(running, min(1.0, (m_ - i) * p_))
        holm[k_] = running
    out["holm"] = {k_: {"p": prim[k_], "p_holm": holm[k_]} for k_ in prim}
    print("holm", out["holm"])
    for k_, nm in [("sel", "Sel"), ("size", "Size"), ("exit", "Exit"), ("block", "Block"), ("repair", "Repair")]:
        M[f"holm{nm}"] = f"{holm[k_]:.3f}" if holm[k_] >= 0.001 else "$<$0.001"
    M["holmAuc"] = f"{holm['AUC = 0.5']:.2f}"
    M["holmRho"] = f"{holm['rho = 0']:.2f}"

    (EXP / "analysis" / "reviewer_checks.json").write_text(json.dumps(out, indent=1, default=lambda o: list(o) if isinstance(o, tuple) else str(o)))
    (PAPER / "tables" / "macros_rev.tex").write_text("\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in M.items()) + "\n")
    print(len(M), "macros")


if __name__ == "__main__":
    main()
