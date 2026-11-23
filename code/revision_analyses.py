"""Revision analyses (13 Oct 2026; exploratory, no new LLM calls) answering the revision plan:

  1.1  information content of the evidence layer (per-agent and pooled IC) + naive selection baselines
       (always long, 20-day momentum, SMA20/50, random trades at matched frequency) through the same simulator
  1.3  confidence: AUC by profile x market, gross vs net, reference AUCs, distinct values, calibration table,
       unit P&L above vs below each profile's bar
  1.4  exposure control: uniform down-scaling to Repair's exposure, risk per unit exposure, cap-only baseline
  1.5  stop-only repair arm (only the stop changes), per-decision denominators
  2.3  headline numbers without the intraday profile

  python revision_analyses.py --analysis analysis          # primary window (A1)
  python revision_analyses.py --analysis analysis_ext      # 25-month extension (A2)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from analyze_components import auc
from src.core.policy import load_all_policies
from src.pit import data
from src.pit.outcomes import COST_RT, HORIZON, evaluate

EXP = Path("logs/exp_pit_20261012")
PAPER = Path("../07_ICAIF_AI4F_2026/paper")
POL = load_all_policies("config/policies")
PROF = ["conservative", "long_term", "intraday", "aggressive_growth"]
PN = {"conservative": "Cons.", "long_term": "Long", "intraday": "Intra.", "aggressive_growth": "Aggr."}


def mboot(df, col, unit="month", block=2, B=2000, seed=7):
    """Mean with a moving-block (consecutive months) bootstrap CI."""
    x = df[[unit, col]].dropna()
    g = x.groupby(unit)[col].agg(["sum", "count"]).sort_index()
    s, n, k = g["sum"].to_numpy(), g["count"].to_numpy(), len(g)
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(k / block))
    st = rng.integers(0, k - block + 1, size=(B, nb))
    idx = (st[:, :, None] + np.arange(block)[None, None, :]).reshape(B, -1)[:, :k]
    bs = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(s.sum() / n.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def series_boot(vals, B=2000, seed=3):
    v = np.asarray([x for x in vals if np.isfinite(x)])
    rng = np.random.default_rng(seed)
    bs = rng.choice(v, size=(B, len(v))).mean(1)
    return float(v.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def fwd_ret(ticker, t, H):
    df = data.prices()[ticker]
    fut = df[df.index > pd.Timestamp(t)].iloc[:H]
    if len(fut) == 0:
        return np.nan
    return float(fut["Close"].iloc[-1] / fut["Open"].iloc[0] - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default="analysis")
    a = ap.parse_args()
    ext = a.analysis.endswith("_ext")
    pre = "x" if ext else ""                     # macro prefix for the extended window
    M, out = {}, {}
    c = lambda t, d=2: f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"
    df = pd.read_pickle(EXP / a.analysis / "scored.pkl")
    keys = set(zip(df["ticker"], df["date"]))
    # decisions metadata (pooled evidence, vol) per (bundle, policy)
    meta = {}
    for f in sorted(EXP.glob("decisions_*.jsonl")):
        for l in f.open():
            r = json.loads(l)
            meta[(r["ticker"], r["date"], r["policy"])] = (r["agg_dir"], r["agg_conf"], r["ann_vol"])
        break  # identical across models (same code decision)
    df["agg_dir"] = [meta.get((t, d, p), (np.nan,) * 3)[0] for t, d, p in zip(df.ticker, df.date, df.policy)]
    df["agg_conf"] = [meta.get((t, d, p), (np.nan,) * 3)[1] for t, d, p in zip(df.ticker, df.date, df.policy)]
    df["ann_vol"] = [meta.get((t, d, p), (np.nan,) * 3)[2] for t, d, p in zip(df.ticker, df.date, df.policy)]
    nl = df[df["style"] == "nl"].copy()
    tr = nl[nl["u_trade"]].copy()
    tr["cost"] = tr["region"].map(COST_RT)
    tr["ret_gross"] = tr["ret_pol"] + tr["cost"]
    M[pre + "Bundles"] = f"{len(keys):,}".replace(",", "{,}")
    M[pre + "Months"] = str(df["month"].nunique())
    M[pre + "Rows"] = f"{len(df):,}".replace(",", "{,}")

    # ================================================================= 1.1 evidence information (IC)
    bundles = {}
    for (tk, d) in keys:
        p = EXP / "bundles" / f"{tk}_{d}.json"
        if p.exists():
            bundles[(tk, d)] = {e["tool"]: e["direction"] for e in json.loads(p.read_text())["evidence"]}
    rows = []
    for (tk, d), ev in bundles.items():
        r = {"ticker": tk, "date": d, "month": d[:7], "region": "IN" if tk.endswith(".NS") else "US"}
        r.update({f"d_{k}": v for k, v in ev.items()})
        for H in (1, 5, 20, 40):
            r[f"r{H}"] = fwd_ret(tk, d, H)
        rows.append(r)
    ev = pd.DataFrame(rows)
    ic = {}
    agents = ["technical", "price_predictor", "news", "fundamental"]   # macro is constant within market-date
    for ag in agents:
        for H in (5, 20):
            monthly = [spearmanr(g[f"d_{ag}"], g[f"r{H}"])[0] for _, g in ev.groupby("month")
                       if g[f"d_{ag}"].nunique() > 2]
            ic[(ag, H)] = series_boot(monthly)
    # pooled direction per profile at its own horizon, gross; and per market
    pooled = {}
    base = nl[nl["model"] == nl["model"].iloc[0]]
    for p in PROF:
        g0 = base[base["policy"] == p].copy()
        g0["r"] = [fwd_ret(t, d, HORIZON[p]) for t, d in zip(g0.ticker, g0.date)]
        monthly = [spearmanr(g["agg_dir"], g["r"])[0] for _, g in g0.groupby("month") if g["agg_dir"].nunique() > 2]
        pooled[p] = series_boot(monthly)
        for reg in ("US", "IN"):
            gm = g0[g0["region"] == reg]
            mm = [spearmanr(g["agg_dir"], g["r"])[0] for _, g in gm.groupby("month") if g["agg_dir"].nunique() > 2]
            pooled[(p, reg)] = series_boot(mm)
    L = [r"\begin{tabular}{lrr}", r"\toprule", r"Signal & IC, $H{=}5$ & IC, $H{=}20$ \\", r"\midrule"]
    nm = {"technical": "Technical (LLM)", "price_predictor": "Price model (LR)", "news": "News (LLM)", "fundamental": "Fundamental (LLM)"}
    for ag in agents:
        L.append(f"{nm[ag]} & {c(ic[(ag, 5)], 3)} & {c(ic[(ag, 20)], 3)} \\\\")
    L.append(r"\midrule \multicolumn{3}{l}{\emph{Pooled direction, profile's own horizon}} \\")
    for p in PROF:
        L.append(f"{PN[p]} ($H{{=}}{HORIZON[p]}$) & \\multicolumn{{2}}{{r}}{{{c(pooled[p], 3)}}} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "tables" / f"ic{'_ext' if ext else ''}.tex").write_text("\n".join(L))
    allic = [ic[k][0] for k in ic] + [pooled[p][0] for p in PROF]
    M[pre + "icMin"], M[pre + "icMax"] = f"{min(allic):+.3f}", f"{max(allic):+.3f}"
    sig = [k for k in list(ic) if ic[k][1] > 0 or ic[k][2] < 0] + [p for p in PROF if pooled[p][1] > 0 or pooled[p][2] < 0]
    M[pre + "icSig"] = str(len(sig))
    M[pre + "icPooledLong"] = c(pooled["long_term"], 3)
    M[pre + "icNewsTwenty"] = c(ic[("news", 20)], 3)
    out["ic"] = {f"{k[0]}|{k[1]}": v for k, v in ic.items()}
    out["ic_pooled"] = {str(k): v for k, v in pooled.items()}
    print("IC", {k: round(v[0], 3) for k, v in out["ic"].items()}, {k: round(v[0], 3) for k, v in out["ic_pooled"].items()})

    # ---------------- naive selection baselines at unit size (1%), policy exits, same simulator
    b = base[["ticker", "date", "month", "region", "policy"]].copy()
    sides = {}
    for r in b.itertuples():
        px = data.asof(r.ticker, r.date)
        cl = px["Close"]
        mom = cl.iloc[-1] / cl.iloc[-21] - 1 if len(cl) > 21 else 0.0
        sma = cl.iloc[-20:].mean() - cl.iloc[-50:].mean()
        sides[(r.ticker, r.date, r.policy)] = (1 if mom > 0 else -1, 1 if sma > 0 else -1)
    def unit(row, action):
        p = POL[row.policy]
        return evaluate(row.ticker, row.date, action, 1.0, p.stop_loss_pct, p.take_profit_pct, HORIZON[row.policy])["pnl"]
    b["long"] = [unit(r, "BUY") for r in b.itertuples()]
    b["short"] = [unit(r, "SELL") for r in b.itertuples()]
    b["mom"] = [r.long if sides[(r.ticker, r.date, r.policy)][0] > 0 else r.short for r in b.itertuples()]
    b["sma"] = [r.long if sides[(r.ticker, r.date, r.policy)][1] > 0 else r.short for r in b.itertuples()]
    f_llm = nl.groupby("policy")["u_trade"].mean().to_dict()
    f_code = base.groupby("policy")["c_trade"].mean().to_dict()
    rng = np.random.default_rng(0)
    rand_llm, rand_code = [], []
    for s in range(50):
        for f, acc in ((f_llm, rand_llm), (f_code, rand_code)):
            tr_mask = rng.random(len(b)) < b["policy"].map(f).to_numpy()
            side = rng.random(len(b)) < 0.5
            pnl = np.where(tr_mask, np.where(side, b["long"], b["short"]), 0.0)
            acc.append(pnl.mean())
    rules = nl[nl["style"] == "nl"]
    ex = df[df["style"] == "explicit"]
    brows = [("LLM, persona", mboot(nl, "unit_u")), ("LLM, rules", mboot(ex, "unit_u")), ("Code", mboot(base, "unit_c")),
             ("Always long", mboot(b, "long")), ("20-day momentum", mboot(b, "mom")), ("SMA20/50 trend", mboot(b, "sma"))]
    L = [r"\begin{tabular}{lr}", r"\toprule", r"Selection rule (1\% size, policy exits) & bp per decision [95\% CI] \\", r"\midrule"]
    for nm_, t in brows:
        L.append(f"{nm_} & {c(t)} \\\\")
    rl, rc = np.array(rand_llm), np.array(rand_code)
    L.append(f"Random, LLM trade rate (50 seeds) & {rl.mean():+.2f} [{np.percentile(rl, 2.5):+.2f}, {np.percentile(rl, 97.5):+.2f}] \\\\")
    L.append(f"Random, code trade rate (50 seeds) & {rc.mean():+.2f} [{np.percentile(rc, 2.5):+.2f}, {np.percentile(rc, 97.5):+.2f}] \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "tables" / f"selection_baselines{'_ext' if ext else ''}.tex").write_text("\n".join(L))
    M[pre + "selLong"], M[pre + "selMom"], M[pre + "selSma"] = c(brows[3][1]), c(brows[4][1]), c(brows[5][1])
    M[pre + "selRandLlm"] = f"{rl.mean():+.2f}"
    M[pre + "selLlmPersona"], M[pre + "selCode"] = c(brows[0][1]), c(brows[2][1])
    out["selection_baselines"] = {k: v for k, v in brows}
    out["random"] = {"llm_rate": [rl.mean(), np.percentile(rl, 2.5), np.percentile(rl, 97.5)],
                     "code_rate": [rc.mean(), np.percentile(rc, 2.5), np.percentile(rc, 97.5)]}
    print("baselines", {k: round(v[0], 2) for k, v in brows}, "random", round(rl.mean(), 2), round(rc.mean(), 2))

    # ================================================================= 1.3 confidence
    conf_rows = []
    for p in PROF:
        for reg in ("US", "IN"):
            g = tr[(tr["policy"] == p) & (tr["region"] == reg)]
            conf_rows.append((p, reg, len(g), auc(g["u_conf"], g["ret_pol"] > 0), auc(g["u_conf"], g["ret_gross"] > 0)))
    out["auc_cells"] = conf_rows
    vals = [x for r in conf_rows for x in (r[3], r[4]) if np.isfinite(x)]
    M[pre + "aucCellMin"], M[pre + "aucCellMax"] = f"{min(vals):.2f}", f"{max(vals):.2f}"
    lt = tr[tr["policy"] == "long_term"]
    M[pre + "aucLongGross"] = f"{auc(lt['u_conf'], lt['ret_gross'] > 0):.3f}"
    # references on the same trades
    ref = {"stated conf.": auc(tr["u_conf"], tr["ret_pol"] > 0),
           "pooled evidence |d|": auc(tr["agg_dir"].abs(), tr["ret_pol"] > 0),
           "code's pooled conf.": auc(tr["agg_conf"], tr["ret_pol"] > 0),
           "low realised vol": auc(-tr["ann_vol"], tr["ret_pol"] > 0)}
    out["auc_ref"] = ref
    M[pre + "aucRefEvid"] = f"{ref['pooled evidence |d|']:.3f}"
    M[pre + "aucRefCode"] = f"{ref['code' + chr(39) + 's pooled conf.']:.3f}"
    M[pre + "aucRefVol"] = f"{ref['low realised vol']:.3f}"
    # discreteness
    dv = {}
    for (m, s_), g in df[df["u_trade"]].groupby(["model", "style"]):
        vc = g["u_conf"].round(3).value_counts(normalize=True)
        dv[f"{m}|{s_}"] = (int(len(vc)), float(vc.iloc[:3].sum()))
    out["distinct"] = dv
    M[pre + "distinctMin"] = str(min(v[0] for v in dv.values()))
    M[pre + "distinctMax"] = str(max(v[0] for v in dv.values()))
    M[pre + "topThreeShare"] = f"{100 * np.mean([v[1] for v in dv.values()]):.0f}\\%"
    # calibration by stated-confidence bin (pooled persona) and for long-term
    bins = [0, 0.6, 0.65, 0.7, 0.75, 0.8, 1.01]
    tr["cbin"] = pd.cut(tr["u_conf"], bins, right=False)
    cal = tr.groupby("cbin", observed=True).agg(n=("ret_pol", "size"), hit=("ret_pol", lambda v: (v > 0).mean()),
                                                ret=("ret_pol", lambda v: v.mean() * 100))
    out["calibration"] = {str(k): v for k, v in cal.to_dict("index").items()}
    L = [r"\begin{tabular}{lrrr}", r"\toprule", r"Stated conf. & $n$ & Hit rate & Mean ret.\ (\%) \\", r"\midrule"]
    for k_, r_ in cal.iterrows():
        lo, hi = k_.left, min(k_.right, 1.0)
        L.append(f"[{lo:.2f}, {hi:.2f}) & {int(r_['n']):,} & {100 * r_['hit']:.0f}\\% & {r_['ret']:+.2f} \\\\".replace(",", "{,}"))
    L += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "tables" / f"calibration{'_ext' if ext else ''}.tex").write_text("\n".join(L))
    # above vs below bar (unit size, policy exits)
    tr["unit_pol"] = tr["ret_pol"] * 100
    ab = {}
    for p in PROF:
        g = tr[tr["policy"] == p]
        hi_, lo_ = g[g["u_conf"] >= g["bar"]], g[g["u_conf"] < g["bar"]]
        ab[p] = (mboot(hi_, "unit_pol") if len(hi_) > 30 else (np.nan,) * 3,
                 mboot(lo_, "unit_pol") if len(lo_) > 30 else (np.nan,) * 3, len(hi_), len(lo_))
    out["above_below"] = {p: v for p, v in ab.items()}
    hi_all = tr[tr["u_conf"] >= tr["bar"]]
    lo_all = tr[tr["u_conf"] < tr["bar"]]
    M[pre + "aboveBar"], M[pre + "belowBar"] = c(mboot(hi_all, "unit_pol")), c(mboot(lo_all, "unit_pol"))
    print("AUC ref", {k: round(v, 3) for k, v in ref.items()}, "distinct", dv)

    # ================================================================= 1.4 exposure control
    g = nl.groupby(["model", "policy"])
    nl["k"] = g["size_repair"].transform("sum") / g["size_raw"].transform("sum")
    nl["pnl_scaled"] = nl["k"] * nl["pnl_raw"]
    # cap-only: clip size to cap, keep LLM exits, no confidence gate
    def caponly(r):
        if not r.u_trade:
            return 0.0, 0.0
        s = min(r.u_size, r.cap)
        o = evaluate(r.ticker, r.date, r.u_action, s, r.u_stop, r.u_tp, HORIZON[r.policy])
        return o["pnl"], (s if o["traded"] else 0.0)
    cp = [caponly(r) for r in nl.itertuples()]
    nl["pnl_cap"], nl["size_cap"] = [x[0] for x in cp], [x[1] for x in cp]
    # stop-only repair: replace only a missing/looser stop with the policy stop
    def stoponly(r):
        if not r.u_trade:
            return 0.0, False
        ps = POL[r.policy].stop_loss_pct
        if r.u_stop > 0 and r.u_stop <= ps:
            return r.pnl_raw, False
        return evaluate(r.ticker, r.date, r.u_action, r.u_size, ps, r.u_tp, HORIZON[r.policy])["pnl"], True
    so = [stoponly(r) for r in nl.itertuples()]
    nl["pnl_stoprep"], nl["stop_changed"] = [x[0] for x in so], [x[1] for x in so]
    nl["d_stoprep"] = nl["pnl_stoprep"] - nl["pnl_raw"]
    cv = lambda v: float(v[v <= v.quantile(0.05)].mean())
    risk = {}
    for nm_, col, scol in [("Raw", "pnl_raw", "size_raw"), ("Block", "pnl_block", "size_block"),
                           ("Repair", "pnl_repair", "size_repair"), ("Code", "pnl_code", "size_code"),
                           ("Uniform scaling", "pnl_scaled", None), ("Cap only", "pnl_cap", "size_cap")]:
        expo = nl[scol].mean() if scol else (nl["k"] * nl["size_raw"]).mean()
        risk[nm_] = {"mean": mboot(nl, col), "sd": float(nl[col].std()), "cvar": cv(nl[col]), "exposure": float(expo),
                     "sd_per_exposure": float(nl[col].std() / expo) if expo > 0 else np.nan}
    out["risk"] = risk
    L = [r"\begin{tabular}{lrrrrr}", r"\toprule", r"Pipeline & Mean (bp) [95\% CI] & SD & CVaR$_5$ & Exp.\ & SD/Exp. \\", r"\midrule"]
    for nm_, v in risk.items():
        L.append(f"{nm_} & {c(v['mean'])} & {v['sd']:.1f} & {v['cvar']:.0f} & {v['exposure']:.2f} & {v['sd_per_exposure']:.1f} \\\\")
    L += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "tables" / f"exposure{'_ext' if ext else ''}.tex").write_text("\n".join(L))
    for nm_, key in [("Raw", "Raw"), ("Repair", "Repair"), ("Scaled", "Uniform scaling"), ("Cap", "Cap only"), ("Code", "Code"), ("Block", "Block")]:
        M[pre + f"spe{nm_}"] = f"{risk[key]['sd_per_exposure']:.1f}"
    M[pre + "capSd"], M[pre + "capCvar"] = f"{risk['Cap only']['sd']:.1f}", f"{risk['Cap only']['cvar']:.0f}"
    M[pre + "capMean"] = c(risk["Cap only"]["mean"])
    M[pre + "repSd"] = f"{risk['Repair']['sd']:.1f}"
    M[pre + "scaledSd"] = f"{risk['Uniform scaling']['sd']:.1f}"
    # ================================================================= 1.5 stop-only repair, per decision
    sr = mboot(nl, "d_stoprep")
    ch = nl[nl["stop_changed"]]
    sr_int = mboot(ch, "d_stoprep")
    M[pre + "stopRepDec"], M[pre + "stopRepInt"] = c(sr), c(sr_int)
    M[pre + "stopRepN"] = f"{len(ch):,}".replace(",", "{,}")
    nl["d_block"] = nl["pnl_block"] - nl["pnl_raw"]
    stopveto = nl[(nl["verdict"] == "VETOED") & (nl["clause"] == "stop")]
    tot = nl["d_block"].sum()
    M[pre + "stopVetoShare"] = f"{100 * stopveto['d_block'].sum() / tot:.0f}\\%" if tot else "--"
    M[pre + "stopVetoPerDec"] = f"{stopveto['d_block'].sum() / len(nl):+.2f}"
    out["stop_only"] = {"per_decision": sr, "per_changed": sr_int, "n_changed": int(len(ch)),
                        "veto_stop_only_per_decision": float(stopveto["d_block"].sum() / len(nl))}
    print("stop-only repair", sr, sr_int, len(ch), "risk", {k: (round(v['sd'], 1), round(v['sd_per_exposure'], 1)) for k, v in risk.items()})

    # ================================================================= 2.3 without intraday
    ni = nl[nl["policy"] != "intraday"].copy()
    ni["d_repair"] = ni["pnl_repair"] - ni["pnl_raw"]
    ni["d_block"] = ni["pnl_block"] - ni["pnl_raw"]
    tri = ni[ni["u_trade"]]
    M[pre + "noIntraBlock"], M[pre + "noIntraRepair"] = c(mboot(ni, "d_block")), c(mboot(ni, "d_repair"))
    M[pre + "noIntraSdRaw"], M[pre + "noIntraSdRep"] = f"{ni['pnl_raw'].std():.1f}", f"{ni['pnl_repair'].std():.1f}"
    M[pre + "noIntraAuc"] = f"{auc(tri['u_conf'], tri['ret_pol'] > 0):.3f}"
    out["no_intraday"] = {k: M[pre + k] for k in ("noIntraBlock", "noIntraRepair", "noIntraSdRaw", "noIntraSdRep", "noIntraAuc")}
    print("no intraday", out["no_intraday"])

    # ================================================================= core headline estimates (2-month blocks)
    nl["d_sel"] = nl["unit_u"] - nl["unit_c"]
    nl["d_repair"] = nl["pnl_repair"] - nl["pnl_raw"]
    t2 = nl[nl["u_trade"]].copy()
    t2["z_llm"] = t2["u_size"] / 100 * t2["ret_pol"] * 1e4
    t2["z_eq"] = t2.groupby(["model", "policy"])["u_size"].transform("mean") / 100 * t2["ret_pol"] * 1e4
    t2["d_size_eq_minus_llm"] = t2["z_eq"] - t2["z_llm"]
    t2["d_exit"] = (t2["ret_llmexit"] - t2["ret_pol"]) * 100
    M[pre + "coreAuc"] = f"{auc(t2['u_conf'], t2['ret_pol'] > 0):.3f}"
    M[pre + "coreRho"] = f"{spearmanr(t2['u_size'], t2['ret_pol'])[0]:+.3f}"
    M[pre + "coreSel"] = c(mboot(nl, "d_sel"))
    M[pre + "coreSize"] = c(mboot(t2, "d_size_eq_minus_llm"))
    M[pre + "coreExit"] = c(mboot(t2, "d_exit"))
    M[pre + "coreBlock"] = c(mboot(nl, "d_block"))
    M[pre + "coreRepair"] = c(mboot(nl, "d_repair"))
    M[pre + "coreSdRaw"], M[pre + "coreSdRep"] = f"{nl['pnl_raw'].std():.1f}", f"{nl['pnl_repair'].std():.1f}"
    M[pre + "coreRepVsScaled"] = c(mboot(nl.assign(dd=nl["pnl_repair"] - nl["pnl_scaled"]), "dd"))
    M[pre + "coreTradeLlm"] = f"{100 * nl['u_trade'].mean():.0f}\\%"
    M[pre + "coreTradeCode"] = f"{100 * base['c_trade'].mean():.0f}\\%"
    ex2 = df[df["style"] == "explicit"].copy()
    ex2["d_sel"] = ex2["unit_u"] - ex2["unit_c"]
    M[pre + "coreSelRules"] = c(mboot(ex2, "d_sel"))
    te = ex2[ex2["u_trade"]].copy()
    te["z_llm"] = te["u_size"] / 100 * te["ret_pol"] * 1e4
    te["z_eq"] = te.groupby(["model", "policy"])["u_size"].transform("mean") / 100 * te["ret_pol"] * 1e4
    te["d"] = te["z_llm"] - te["z_eq"]
    M[pre + "coreSizeRulesLlmMinusEq"] = c(mboot(te, "d"))
    (EXP / a.analysis / "revision_analyses.json").write_text(json.dumps(out, indent=1, default=lambda o: list(o) if isinstance(o, tuple) else (float(o) if isinstance(o, (np.floating,)) else str(o))))
    (PAPER / "tables" / f"macros_rev2{'_ext' if ext else ''}.tex").write_text("\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in M.items()) + "\n")
    print(len(M), "macros")


if __name__ == "__main__":
    main()
