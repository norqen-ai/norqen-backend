"""Decision-component and guardrail analysis for the PIT study (PREREGISTRATION.md, amendment A1).

Reads logs/exp_pit_20261012/decisions_<model>.jsonl, labels every decision with its realised
outcome (src/pit/outcomes.py) and writes tables + figures + numbers.json to <exp>/analysis/.

  python analyze_components.py                    # primary analysis
  python analyze_components.py --horizon 20       # robustness: common H for every profile
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, spearmanr

from src.core.policy import load_all_policies
from src.pit.outcomes import HORIZON, evaluate
from src.pit.universe import CORE_40

POL = load_all_policies("config/policies")
EPS = 0.5          # bp of equity: |delta| <= EPS is a neutral intervention
RNG = np.random.default_rng(20261012)
B = 2000


# --------------------------------------------------------------------------- scoring
def pipelines(r: dict) -> dict:
    """The five pre-registered pipelines, all derived from ONE proposal U and ONE code decision C."""
    p, U, C = POL[r["policy"]], r["U"], r["C"]
    trade = U["action"] in ("BUY", "SELL") and U["size"] > 0
    raw = (U["action"], U["size"], U["stop"], U["tp"])
    block = ("WAIT", 0, 0, 0) if r["verdict"] == "VETOED" else raw
    if not trade:
        repair, judge = raw, raw
    elif U["conf"] < p.confidence_to_act:
        repair, judge = ("WAIT", 0, 0, 0), (U["action"], r["code_size_ungated"], p.stop_loss_pct, p.take_profit_pct)
    else:
        stop = p.stop_loss_pct if (U["stop"] <= 0 or U["stop"] > p.stop_loss_pct) else U["stop"]
        repair = (U["action"], min(U["size"], p.max_position_pct), stop, U["tp"])
        judge = (U["action"], r["code_size_ungated"], p.stop_loss_pct, p.take_profit_pct)
    code = (C["action"], C["size"], C["stop"], C["tp"])
    A = r.get("A")      # exploratory LLM risk-manager review (nl trades only); otherwise unchanged
    agent = (A["action"], A["size"], A["stop"], A["tp"]) if A else raw
    return {"raw": raw, "block": block, "repair": repair, "judge": judge, "code": code, "agent": agent}


def clause_label(reasons: list[str]) -> str:
    c = set()
    for s in reasons or []:
        if "exceeds policy cap" in s:
            c.add("size")
        elif "stop-loss" in s:
            c.add("stop")
        elif "below policy threshold" in s:
            c.add("conf")
    return "+".join(sorted(c)) or "none"


def score(rows: list[dict], H_override: int | None = None) -> pd.DataFrame:
    out = []
    for r in rows:
        if r["U"] is None:
            continue
        p = POL[r["policy"]]
        H = H_override or HORIZON[r["policy"]]
        tk, t = r["ticker"], r["date"]
        ev = lambda a, s, k, g: evaluate(tk, t, a, s, k, g, H)
        d = {k: r[k] for k in ("ticker", "date", "region", "policy", "model", "style")}
        d["month"] = r["date"][:7]          # bootstrap cluster: one decision month (US and NSE together)
        d["core40"] = tk in CORE_40
        U, C = r["U"], r["C"]
        d.update(u_action=U["action"], u_size=U["size"], u_stop=U["stop"], u_tp=U["tp"], u_conf=U["conf"],
                 c_action=C["action"], c_size=C["size"], verdict=r["verdict"], clause=clause_label(r.get("reasons")),
                 cap=p.max_position_pct, bar=p.confidence_to_act, code_size_ungated=r["code_size_ungated"])
        d["u_trade"] = U["action"] in ("BUY", "SELL") and U["size"] > 0
        d["reviewed"] = bool(r.get("A"))
        d["a_verdict"] = r.get("A_verdict")
        d["c_trade"] = C["action"] in ("BUY", "SELL") and C["size"] > 0
        for name, (a, s, k, g) in pipelines(r).items():
            o = ev(a, s, k, g)
            d[f"pnl_{name}"], d[f"pnlx_{name}"], d[f"trade_{name}"] = o["pnl"], o["pnl_x"], o["traded"]
            d[f"size_{name}"] = s if o["traded"] else 0.0
        # component probes (unit size = 1% of equity)
        pol_x = (p.stop_loss_pct, p.take_profit_pct)
        for who, act in (("u", U["action"]), ("c", C["action"])):
            o = ev(act, 1.0, *pol_x)
            d[f"unit_{who}"], d[f"unitx_{who}"] = o["pnl"], o["pnl_x"]
        if d["u_trade"]:
            o_pol = ev(U["action"], 1.0, *pol_x)
            o_llm = ev(U["action"], 1.0, U["stop"], U["tp"])
            o_none = ev(U["action"], 1.0, 0, 0)
            d.update(ret_pol=o_pol["ret"], retx_pol=o_pol["ret_x"], ret_llmexit=o_llm["ret"],
                     retx_llmexit=o_llm["ret_x"], ret_noexit=o_none["ret"], retx_noexit=o_none["ret_x"],
                     exit_llm=o_llm["exit"], exit_pol=o_pol["exit"])
        out.append(d)
    return pd.DataFrame(out)


# --------------------------------------------------------------------------- stats
def boot_mean(df: pd.DataFrame, col: str, cluster: str = "month") -> tuple[float, float, float]:
    """Mean of col with a cluster bootstrap 95% CI, resampling whole decision months (US and NSE
    decisions of the same month move together, so they are resampled together)."""
    g = df.groupby(cluster)[col].agg(["sum", "count"])
    if g["count"].sum() == 0:
        return (np.nan, np.nan, np.nan)
    s, n = g["sum"].to_numpy(), g["count"].to_numpy()
    idx = np.random.default_rng(20261012).integers(0, len(g), size=(B, len(g)))   # same draws every call
    bs = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(s.sum() / n.sum()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def intervention_table(df: pd.DataFrame, guard: str, util: str = "pnl", by: list[str] | None = None) -> pd.DataFrame:
    """Policy-as-Skill-style transition analysis of guardrail `guard` vs RAW on identical proposals."""
    x = df.copy()
    x["delta"] = x[f"{util}_{guard}"] - x[f"{util}_raw"]
    x["intervened"] = (x[f"size_{guard}"] != x["size_raw"]) | (x[f"trade_{guard}"] != x["trade_raw"]) | \
                      (x["delta"].abs() > 1e-9)
    rows = []
    for key, g in ([("all", x)] if not by else x.groupby(by)):
        gi = g[g["intervened"]]
        help_, harm = int((gi["delta"] > EPS).sum()), int((gi["delta"] < -EPS).sum())
        neut = len(gi) - help_ - harm
        m, lo, hi = boot_mean(g, "delta")
        mi, loi, hii = boot_mean(gi, "delta") if len(gi) else (np.nan,) * 3
        p = binomtest(help_, help_ + harm, 0.5).pvalue if help_ + harm else np.nan
        rows.append({"stratum": key if isinstance(key, str) else "/".join(map(str, key)), "n": len(g),
                     "interventions": len(gi), "rate": len(gi) / max(len(g), 1), "helpful": help_,
                     "harmful": harm, "neutral": neut, "sign_p": p,
                     "mean_delta_bp": m, "ci_lo": lo, "ci_hi": hi,
                     "mean_delta_if_int": mi, "ci_lo_int": loi, "ci_hi_int": hii})
    return pd.DataFrame(rows)


def auc(score_, label) -> float:
    s, y = np.asarray(score_, float), np.asarray(label, int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    gt = (pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()
    return float(gt / (len(pos) * len(neg)))


def summarize(df: pd.DataFrame, util: str = "pnl") -> dict:
    res = {"n_rows": len(df)}
    keys = ["model", "style"]
    # 1. pipelines
    pip = []
    for k, g in df.groupby(keys + ["policy"]):
        for name in ("raw", "block", "repair", "judge", "code", "agent"):
            m, lo, hi = boot_mean(g, f"{util}_{name}")
            per_date = g.groupby("month")[f"{util}_{name}"].mean()
            sr = per_date.mean() / per_date.std() * np.sqrt(12) if per_date.std() > 0 else np.nan
            tr = g[f"{util}_{name}"][g[f"trade_{name}"]]
            pip.append({"model": k[0], "style": k[1], "policy": k[2], "pipeline": name,
                        "mean_bp": m, "lo": lo, "hi": hi, "trade_rate": g[f"trade_{name}"].mean(),
                        "mean_size": g.loc[g[f"trade_{name}"], f"size_{name}"].mean(),
                        "hit": (tr > 0).mean() if len(tr) else np.nan,
                        "cvar5_bp": g[f"{util}_{name}"].quantile(0.05) if len(g) else np.nan,
                        "worst_bp": g[f"{util}_{name}"].min(), "sharpe_dates": sr})
    res["pipelines"] = pd.DataFrame(pip)
    # 2. components
    comp = []
    rcol, xsuffix = ("ret", "") if util == "pnl" else ("retx", "x")
    for k, g in df.groupby(keys + ["policy"]):
        tr = g[g["u_trade"]]
        row = {"model": k[0], "style": k[1], "policy": k[2], "n": len(g), "u_trade_rate": g["u_trade"].mean(),
               "c_trade_rate": g["c_trade"].mean()}
        # T: selection at unit size with policy exits (bp per decision, WAIT = 0)
        row["sel_llm_bp"] = g[f"unit{xsuffix}_u"].mean()
        row["sel_code_bp"] = g[f"unit{xsuffix}_c"].mean()
        row["sel_llm_per_trade_bp"] = tr[f"unit{xsuffix}_u"].mean() if len(tr) else np.nan
        ct = g[g["c_trade"]]
        row["sel_code_per_trade_bp"] = ct[f"unit{xsuffix}_c"].mean() if len(ct) else np.nan
        if len(tr) > 5:
            r_pol = tr[f"{rcol}_pol"].to_numpy()
            # Z: sizing on LLM trades with policy exits
            eq = tr["u_size"].mean()
            row["size_llm_bp"] = float((tr["u_size"] / 100 * r_pol * 1e4).mean())
            row["size_equal_bp"] = float((eq / 100 * r_pol * 1e4).mean())
            row["size_code_bp"] = float((tr["code_size_ungated"] / 100 * r_pol * 1e4).mean())
            row["size_rho"], row["size_rho_p"] = spearmanr(tr["u_size"], r_pol) if tr["u_size"].nunique() > 1 else (np.nan, np.nan)
            # X: exits at unit size
            row["exit_llm_bp"] = float(tr[f"{rcol}_llmexit"].mean() * 100)
            row["exit_pol_bp"] = float(tr[f"{rcol}_pol"].mean() * 100)
            row["exit_none_bp"] = float(tr[f"{rcol}_noexit"].mean() * 100)
            row["llm_stop_med"], row["pol_stop"] = float(tr["u_stop"].median()), POL[k[2]].stop_loss_pct
            # K: confidence
            row["conf_auc"] = auc(tr["u_conf"], r_pol > 0)
            hi_, lo_ = tr[tr["u_conf"] >= tr["bar"]], tr[tr["u_conf"] < tr["bar"]]
            row["conf_above_bp"] = float(hi_[f"{rcol}_pol"].mean() * 100) if len(hi_) else np.nan
            row["conf_below_bp"] = float(lo_[f"{rcol}_pol"].mean() * 100) if len(lo_) else np.nan
            row["n_above"], row["n_below"] = len(hi_), len(lo_)
            row["hit_llm"] = float((r_pol > 0).mean())
        comp.append(row)
    res["components"] = pd.DataFrame(comp)
    # 3. guardrail interventions
    res["block_by_policy"] = intervention_table(df, "block", util, keys + ["policy"])
    res["repair_by_policy"] = intervention_table(df, "repair", util, keys + ["policy"])
    res["block_by_clause"] = intervention_table(df[df["verdict"] == "VETOED"], "block", util, keys + ["clause"])
    res["repair_by_region"] = intervention_table(df, "repair", util, keys + ["region"])
    res["block_by_region"] = intervention_table(df, "block", util, keys + ["region"])
    res["block_overall"] = intervention_table(df, "block", util, keys)
    nl = df[df["style"] == "nl"]
    res["agent_overall"] = intervention_table(nl, "agent", util, keys)
    res["agent_by_policy"] = intervention_table(nl, "agent", util, keys + ["policy"])
    res["repair_overall"] = intervention_table(df, "repair", util, keys)
    return res


def pooled_components(df: pd.DataFrame, util: str = "pnl") -> pd.DataFrame:
    """Component estimates pooled over profiles, with date-cluster bootstrap CIs."""
    rows = []
    xs = "" if util == "pnl" else "x"
    rcol = "ret" if util == "pnl" else "retx"
    for k, g in df.groupby(["model", "style"]):
        tr = g[g["u_trade"]].copy()
        tr["z_llm"] = tr["u_size"] / 100 * tr[f"{rcol}_pol"] * 1e4
        tr["z_eq"] = tr.groupby("policy")["u_size"].transform("mean") / 100 * tr[f"{rcol}_pol"] * 1e4
        tr["z_code"] = tr["code_size_ungated"] / 100 * tr[f"{rcol}_pol"] * 1e4
        tr["x_llm"], tr["x_pol"], tr["x_none"] = tr[f"{rcol}_llmexit"] * 100, tr[f"{rcol}_pol"] * 100, tr[f"{rcol}_noexit"] * 100
        tr["d_size"] = tr["z_llm"] - tr["z_eq"]
        tr["d_exit"] = tr["x_llm"] - tr["x_pol"]
        g = g.copy()
        g["d_sel"] = g[f"unit{xs}_u"] - g[f"unit{xs}_c"]
        row = {"model": k[0], "style": k[1], "n": len(g), "n_trades": len(tr)}
        for c, frame in (("d_sel", g), ("d_size", tr), ("d_exit", tr), (f"unit{xs}_u", g), (f"unit{xs}_c", g),
                         ("z_llm", tr), ("z_eq", tr), ("z_code", tr), ("x_llm", tr), ("x_pol", tr), ("x_none", tr)):
            m, lo, hi = boot_mean(frame, c)
            row[c], row[c + "_lo"], row[c + "_hi"] = m, lo, hi
        row["conf_auc"] = auc(tr["u_conf"], tr[f"{rcol}_pol"] > 0)
        row["size_rho"] = spearmanr(tr["u_size"], tr[f"{rcol}_pol"])[0] if tr["u_size"].nunique() > 1 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="logs/exp_pit_20261012")
    ap.add_argument("--horizon", type=int, default=None)
    ap.add_argument("--subset", default=None, choices=[None, "core40"])
    ap.add_argument("--window", default="primary", choices=["primary", "extended"],
                    help="primary = Jan 2025-Jul 2026 (A1); extended = Jul 2024-Jul 2026 (A2)")
    ap.add_argument("--costs", default="prereg", choices=["prereg", "zero", "low_nse"],
                    help="robustness only (exploratory): zero costs, or NSE at 15 bp round trip")
    a = ap.parse_args()
    if a.costs != "prereg":
        import src.pit.outcomes as oc
        oc.COST_RT.update({"US": 0.0, "IN": 0.0} if a.costs == "zero" else {"IN": 0.0015})
        oc.trade_return.cache_clear()
    exp = Path(a.exp)
    rows = []
    for f in sorted(exp.glob("decisions_*.jsonl")):
        rows += [json.loads(l) for l in f.open() if l.strip()]
    # keep only the pre-registered schedule (drops one smoke-test bundle dated off-schedule)
    from src.pit.data import decision_dates
    start = "2024-07-15" if a.window == "extended" else "2025-01-15"
    sched = {r_: {str(d.date()) for d in decision_dates(start=start, region_code=r_)} for r_ in ("US", "IN")}
    n0 = len(rows)
    rows = [r for r in rows if r["date"] in sched[r["region"]]]
    print(f"dropped {n0 - len(rows)} off-schedule rows")
    reviews = {}
    for f in sorted(exp.glob("riskagent_*.jsonl")):
        m = f.stem.split("_", 1)[1]
        for l in f.open():
            v = json.loads(l)
            if v.get("A"):
                reviews[(m, v["bundle"], v["policy"], v["style"])] = v
    for r in rows:
        v = reviews.get((r["model"], r["bundle"], r["policy"], r["style"]))
        if v:
            r["A"], r["A_verdict"] = v["A"], v["A_verdict"]
    tag = ("_ext" if a.window == "extended" else "") + (f"_H{a.horizon}" if a.horizon else "") + (f"_{a.subset}" if a.subset else "") + \
          (f"_cost_{a.costs}" if a.costs != "prereg" else "")
    outd = exp / f"analysis{tag}"
    outd.mkdir(exist_ok=True)
    df = score(rows, a.horizon)
    if a.subset == "core40":
        df = df[df["core40"]]
    df.to_pickle(outd / "scored.pkl")
    print(f"scored {len(df)} decisions ({df['model'].nunique()} models) -> {outd}")
    for util in ("pnl", "pnlx"):
        res = summarize(df, util)
        for name, t in res.items():
            if isinstance(t, pd.DataFrame):
                t.to_csv(outd / f"{util}_{name}.csv", index=False)
        pooled_components(df, util).to_csv(outd / f"{util}_components_pooled.csv", index=False)
    print("tables written:", sorted(p.name for p in outd.glob("*.csv"))[:6], "...")


if __name__ == "__main__":
    main()
