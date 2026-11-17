"""Paper tables, figures and numbers for the PIT decision-component study.

Reads <exp>/analysis/scored.pkl (written by analyze_components.py) and writes LaTeX tables,
PDF figures and numbers.json into the paper folder.

  python make_paper_results.py --exp logs/exp_pit_20261012 --paper ../07_ICAIF_AI4F_2026/paper
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binomtest, spearmanr

from analyze_components import B, EPS, RNG, auc, boot_mean

MODELS = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"]
PROF = ["conservative", "long_term", "intraday", "aggressive_growth"]
PNAME = {"conservative": "Conservative", "long_term": "Long-term", "intraday": "Intraday",
         "aggressive_growth": "Aggressive"}
PIPES = ["raw", "block", "repair", "judge", "code"]
PIPE_LABEL = {"raw": "Raw LLM", "block": "Block", "repair": "Repair", "judge": "Judgment-only",
              "code": "Code", "agent": "LLM risk agent"}
from matplotlib import font_manager as _fm
for _f in ("/System/Library/Fonts/Supplemental/STIXTwoText.ttf", "/System/Library/Fonts/Supplemental/STIXTwoText-Italic.ttf"):
    try:
        _fm.fontManager.addfont(_f)
    except Exception:
        pass
plt.rcParams.update({"font.family": "STIX Two Text", "mathtext.fontset": "stix", "font.size": 7.5,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
                     "axes.edgecolor": "#5b6070", "axes.labelcolor": "#1f2433", "xtick.color": "#3b4050",
                     "ytick.color": "#3b4050", "xtick.major.width": 0.6, "ytick.major.width": 0.6,
                     "axes.grid": True, "grid.color": "#e7e3dc", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "legend.frameon": False, "savefig.dpi": 300})
COL = {"gpt-4o-mini": "#6d55a3", "gpt-4.1-mini": "#3f6fb0", "gpt-5-mini": "#b07a3f", "code": "#5b6070"}


def fmt(x, d=1):
    return "--" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}"


def ci(m, lo, hi, d=1):
    return f"{fmt(m, d)} [{fmt(lo, d)}, {fmt(hi, d)}]"


def interventions(df: pd.DataFrame, guard: str, util: str) -> dict:
    x = df.copy()
    x["delta"] = x[f"{util}_{guard}"] - x[f"{util}_raw"]
    x["int"] = (x[f"size_{guard}"] != x["size_raw"]) | (x[f"trade_{guard}"] != x["trade_raw"]) | (x["delta"].abs() > 1e-9)
    gi = x[x["int"]]
    h, k = int((gi["delta"] > EPS).sum()), int((gi["delta"] < -EPS).sum())
    m, lo, hi = boot_mean(x, "delta")
    mi, loi, hii = boot_mean(gi, "delta") if len(gi) else (np.nan,) * 3
    return {"n": len(x), "int": len(gi), "rate": len(gi) / max(len(x), 1), "helpful": h, "harmful": k,
            "neutral": len(gi) - h - k, "p": binomtest(h, h + k).pvalue if h + k else np.nan,
            "mean": m, "lo": lo, "hi": hi, "mean_int": mi, "lo_int": loi, "hi_int": hii,
            "help_share": h / max(h + k, 1)}


def components(df: pd.DataFrame, util: str) -> dict:
    """Pooled component estimates for one slice (date-cluster bootstrap)."""
    xs = "" if util == "pnl" else "x"
    rc = "ret" if util == "pnl" else "retx"
    g = df.copy()
    g["d_sel"] = g[f"unit{xs}_u"] - g[f"unit{xs}_c"]
    tr = g[g["u_trade"]].copy()
    tr["z_llm"] = tr["u_size"] / 100 * tr[f"{rc}_pol"] * 1e4
    tr["z_eq"] = tr.groupby(["model", "style", "policy"])["u_size"].transform("mean") / 100 * tr[f"{rc}_pol"] * 1e4
    tr["d_size"] = tr["z_llm"] - tr["z_eq"]
    tr["x_llm"], tr["x_pol"], tr["x_none"] = (tr[f"{rc}_llmexit"] * 100, tr[f"{rc}_pol"] * 100, tr[f"{rc}_noexit"] * 100)
    tr["d_exit"] = tr["x_llm"] - tr["x_pol"]
    tr["d_exit_none"] = tr["x_llm"] - tr["x_none"]
    out = {"n": len(g), "n_trades": len(tr), "u_trade_rate": g["u_trade"].mean(), "c_trade_rate": g["c_trade"].mean()}
    for c, fr in (("d_sel", g), (f"unit{xs}_u", g), (f"unit{xs}_c", g), ("d_size", tr), ("d_exit", tr),
                  ("d_exit_none", tr), ("x_llm", tr), ("x_pol", tr), ("x_none", tr), ("z_llm", tr), ("z_eq", tr)):
        out[c.replace(f"unit{xs}_", "unit_")] = boot_mean(fr, c)
    # per-trade selection quality at unit size (bp of equity per 1% position)
    out["llm_per_trade"] = boot_mean(tr, f"unit{xs}_u")
    ct = g[g["c_trade"]]
    out["code_per_trade"] = boot_mean(ct, f"unit{xs}_c")
    out["hit_llm"] = float((tr[f"{rc}_pol"] > 0).mean()) if len(tr) else np.nan
    out["hit_code"] = float((ct[f"unit{xs}_c"] > 0).mean()) if len(ct) else np.nan
    # confidence (K): AUC with a date-cluster bootstrap CI
    a = auc(tr["u_conf"], tr[f"{rc}_pol"] > 0)
    dates = tr["month"].unique()
    by = {d: tr[tr["month"] == d] for d in dates}
    bs = []
    for _ in range(300):
        s = pd.concat([by[d] for d in RNG.choice(dates, len(dates))])
        bs.append(auc(s["u_conf"], s[f"{rc}_pol"] > 0))
    out["auc"] = (a, float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5)))
    out["size_rho"] = float(spearmanr(tr["u_size"], tr[f"{rc}_pol"])[0]) if tr["u_size"].nunique() > 1 else np.nan
    out["conf_sd"] = float(tr["u_conf"].std())
    out["conf_mean"] = float(tr["u_conf"].mean())
    out["conf_unique"] = int(tr["u_conf"].round(3).nunique())
    return out


def pipeline_stats(df: pd.DataFrame, util: str, name: str) -> dict:
    col = f"{util}_{name}"
    m = boot_mean(df, col)
    per_date = df.groupby("month")[col].mean()
    sr = per_date.mean() / per_date.std() * np.sqrt(12) if per_date.std() > 0 else np.nan
    traded = df[f"trade_{name}"]
    return {"mean": m, "trade_rate": float(traded.mean()),
            "exposure": float(df[f"size_{name}"].mean()),
            "sd": float(df[col].std()), "cvar5": float(df[col][df[col] <= df[col].quantile(0.05)].mean()),
            "worst": float(df[col].min()), "sharpe": float(sr)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="logs/exp_pit_20261012")
    ap.add_argument("--paper", default="../07_ICAIF_AI4F_2026/paper")
    ap.add_argument("--analysis", default="analysis")
    ap.add_argument("--macros-only", action="store_true")
    a = ap.parse_args()
    if a.macros_only:
        write_macros(json.loads((Path(a.paper) / "numbers.json").read_text()), Path(a.paper))
        return
    df = pd.read_pickle(Path(a.exp) / a.analysis / "scored.pkl")
    paper = Path(a.paper)
    (paper / "figures").mkdir(parents=True, exist_ok=True)
    (paper / "tables").mkdir(parents=True, exist_ok=True)
    models = [m for m in MODELS if m in set(df["model"])]
    N = {"rows": len(df), "bundles": int(df[["ticker", "date"]].drop_duplicates().shape[0]),
         "models": models, "per_model": {m: int((df["model"] == m).sum()) for m in models}}

    # ---------------- violations (replication of the obedience result)
    viol = {}
    for (m, s), g in df.groupby(["model", "style"]):
        tr = g[g["u_trade"]]
        viol[f"{m}|{s}"] = {"trade_rate": float(g["u_trade"].mean()),
                            "veto_rate": float((g["verdict"] == "VETOED").mean()),
                            "veto_of_trades": float((tr["verdict"] == "VETOED").mean()) if len(tr) else np.nan,
                            "oversize_of_trades": float((tr["u_size"] > tr["cap"]).mean()) if len(tr) else np.nan,
                            "mean_size_over_cap": float((tr["u_size"] / tr["cap"]).mean()) if len(tr) else np.nan}
    N["violations"] = viol
    by_prof_size = df[(df["style"] == "nl") & df["u_trade"]].groupby(["model", "policy"])["u_size"].mean().unstack()
    N["nl_mean_size_by_profile"] = by_prof_size.round(2).to_dict()
    tr_all = df[df["u_trade"]]
    N["exit_medians"] = {f"{s}|{p}": {"stop": float(g["u_stop"].median()), "tp": float(g["u_tp"].median())}
                         for (s, p), g in tr_all.groupby(["style", "policy"])}

    # ---------------- components (pooled over profiles) per model x style, both utilities
    comp = {}
    for util in ("pnl", "pnlx"):
        for (m, s), g in df.groupby(["model", "style"]):
            comp[f"{util}|{m}|{s}"] = components(g, util)
        for s, g in df.groupby("style"):
            comp[f"{util}|pooled|{s}"] = components(g, util)
    N["components"] = comp

    # ---------------- pipelines per style x profile (pooled models) + per model
    pip = {}
    for util in ("pnl", "pnlx"):
        for (s, p), g in df.groupby(["style", "policy"]):
            for name in PIPES + (["agent"] if s == "nl" else []):
                pip[f"{util}|pooled|{s}|{p}|{name}"] = pipeline_stats(g, util, name)
        for (m, s), g in df.groupby(["model", "style"]):
            for name in PIPES + (["agent"] if s == "nl" else []):
                pip[f"{util}|{m}|{s}|all|{name}"] = pipeline_stats(g, util, name)
        for s, g in df.groupby("style"):
            for name in PIPES + (["agent"] if s == "nl" else []):
                pip[f"{util}|pooled|{s}|all|{name}"] = pipeline_stats(g, util, name)
    N["pipelines"] = pip

    # ---------------- interventions (nl style; explicit has ~none)
    inter = {}
    for util in ("pnl", "pnlx"):
        for s, gs in df.groupby("style"):
            for guard in ("block", "repair") + (("agent",) if s == "nl" else ()):
                inter[f"{util}|{s}|{guard}|all|all"] = interventions(gs, guard, util)
                for p, g in gs.groupby("policy"):
                    inter[f"{util}|{s}|{guard}|policy|{p}"] = interventions(g, guard, util)
                for r, g in gs.groupby("region"):
                    inter[f"{util}|{s}|{guard}|region|{r}"] = interventions(g, guard, util)
                for m, g in gs.groupby("model"):
                    inter[f"{util}|{s}|{guard}|model|{m}"] = interventions(g, guard, util)
            vet = gs[gs["verdict"] == "VETOED"]
            for c, g in vet.groupby("clause"):
                inter[f"{util}|{s}|block|clause|{c}"] = interventions(g, "block", util)
    N["interventions"] = inter

    # risk agent leakage
    rv = df[(df["style"] == "nl") & df["reviewed"]]
    if len(rv):
        N["agent"] = {"reviewed": int(len(rv)), "residual_veto": float((rv["a_verdict"] == "VETOED").mean()),
                      "to_wait": float((rv["trade_agent"] == False).mean())}  # noqa: E712

    # subset / region robustness for the main component numbers
    rob = {}
    for util in ("pnl", "pnlx"):
        for r, g in df.groupby("region"):
            rob[f"{util}|region|{r}"] = components(g[g["style"] == "nl"], util)
        rob[f"{util}|core40"] = components(df[df["core40"] & (df["style"] == "nl")], util)
    N["robust"] = rob

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return None if np.isnan(o) else round(float(o), 5)
        if isinstance(o, (np.integer,)):
            return int(o)
        return o
    (paper / "numbers.json").write_text(json.dumps(clean(N), indent=1))
    print("numbers.json written:", len(json.dumps(clean(N))) // 1024, "KB")
    figures(df, comp, pip, inter, models, paper)
    tables(df, comp, pip, inter, models, paper)
    write_macros(json.loads((paper / "numbers.json").read_text()), paper)


# =============================================================================== figures
def figures(df, comp, pip, inter, models, paper):
    # Figure: component forest plot (T, Z, X, K) per model x style, raw P&L
    fig, axes = plt.subplots(1, 4, figsize=(7.0, 1.9), sharey=True)
    rows = [(m, s) for m in models for s in ("nl", "explicit")]
    ylab = [f"{m}\n{'persona' if s == 'nl' else 'rules'}" for m, s in rows]
    panels = [("d_sel", "T  Selection: LLM $-$ code\n(bp per decision, 1% size)"),
              ("d_size", "Z  Sizing: LLM $-$ equal size\n(bp per trade)"),
              ("d_exit", "X  Exits: LLM $-$ policy\n(bp per trade, 1% size)"),
              ("auc", "K  Confidence AUC\n(profitable trade)")]
    for ax, (key, title) in zip(axes, panels):
        for i, (m, s) in enumerate(rows):
            v = comp[f"pnl|{m}|{s}"][key]
            y = len(rows) - 1 - i
            ax.errorbar(v[0], y, xerr=[[v[0] - v[1]], [v[2] - v[0]]], fmt="o" if s == "nl" else "s",
                        color=COL[m], ms=3.2, lw=0.9, capsize=1.5, mfc="white" if s == "explicit" else COL[m])
        ax.axvline(0.5 if key == "auc" else 0, color="#999", lw=0.6, ls="--")
        ax.set_title(title, fontsize=6.6, loc="left")
        ax.tick_params(labelsize=6)
    axes[0].set_yticks(range(len(rows)))
    axes[0].set_yticklabels(ylab[::-1], fontsize=5.8)
    fig.tight_layout(w_pad=0.6)
    fig.savefig(paper / "figures" / "fig_components.pdf", bbox_inches="tight")
    plt.close(fig)

    # Figure: risk-return of pipelines by profile (nl, pooled models)
    fig, axes = plt.subplots(1, 4, figsize=(7.0, 1.85))
    mk = {"raw": "o", "block": "X", "repair": "D", "judge": "^", "code": "s", "agent": "P"}
    pc = {"raw": "#a35b5b", "block": "#5576a8", "repair": "#4f8a63", "judge": "#6d55a3", "code": "#5b6070",
          "agent": "#a7864a"}
    for ax, p in zip(axes, PROF):
        for name in PIPES + ["agent"]:
            k = f"pnl|pooled|nl|{p}|{name}"
            if k not in pip:
                continue
            st = pip[k]
            ax.errorbar(-st["cvar5"], st["mean"][0], yerr=[[st["mean"][0] - st["mean"][1]], [st["mean"][2] - st["mean"][0]]],
                        fmt=mk[name], color=pc[name], ms=4, lw=0.8, capsize=1.5, label=PIPE_LABEL[name])
        ax.axhline(0, color="#999", lw=0.6, ls="--")
        ax.set_title(PNAME[p], fontsize=7)
        ax.set_xlabel("tail loss: $-$CVaR$_{5\\%}$ (bp)", fontsize=6)
        ax.tick_params(labelsize=6)
    axes[0].set_ylabel("mean P&L (bp / decision)", fontsize=6)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=6, fontsize=6, frameon=False, bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout(w_pad=0.8)
    fig.savefig(paper / "figures" / "fig_pipelines.pdf", bbox_inches="tight")
    plt.close(fig)

    # Figure: helpful / harmful / neutral of BLOCK by profile, raw vs index-excess
    fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.7), sharey=True)
    for ax, util, ttl in zip(axes, ("pnl", "pnlx"), ("raw P&L", "index-excess P&L")):
        for i, p in enumerate(PROF):
            v = inter[f"{util}|nl|block|policy|{p}"]
            tot = max(v["int"], 1)
            ax.barh(i, v["helpful"] / tot, color="#4f8a63", height=0.62)
            ax.barh(i, v["neutral"] / tot, left=v["helpful"] / tot, color="#d9d4cc", height=0.62)
            ax.barh(i, v["harmful"] / tot, left=(v["helpful"] + v["neutral"]) / tot, color="#a35b5b", height=0.62)
            ax.text(1.02, i, f"n={v['int']}", va="center", fontsize=5.5)
        ax.set_yticks(range(len(PROF)))
        ax.set_yticklabels([PNAME[p] for p in PROF], fontsize=6)
        ax.set_xlim(0, 1)
        ax.axvline(0.5, color="#555", lw=0.5, ls=":")
        ax.set_title(f"Vetoes, {ttl}", fontsize=6.6)
        ax.tick_params(labelsize=6)
    axes[0].invert_yaxis()
    fig.tight_layout(w_pad=2.2)
    fig.savefig(paper / "figures" / "fig_vetoes.pdf", bbox_inches="tight")
    plt.close(fig)


# =============================================================================== tables
def tables(df, comp, pip, inter, models, paper):
    # Table: pipelines pooled over models, by profile (nl) — mean bp [CI], trade rate, exposure, CVaR, Sharpe
    L = [r"\begin{tabular}{llrrrr}", r"\toprule",
         r"Profile & Pipeline & Mean P\&L (bp) [95\% CI] & Trade & Exp. & CVaR$_5$ \\", r"\midrule"]
    for p in PROF:
        first = True
        for name in PIPES + ["agent"]:
            k = f"pnl|pooled|nl|{p}|{name}"
            if k not in pip:
                continue
            st = pip[k]
            L.append(f"{PNAME[p] if first else ''} & {PIPE_LABEL[name]} & {ci(*st['mean'])} & "
                     f"{st['trade_rate'] * 100:.0f}\\% & {st['exposure']:.1f} & {st['cvar5']:.0f} \\\\")
            first = False
        L.append(r"\midrule" if p != PROF[-1] else r"\bottomrule")
    L.append(r"\end{tabular}")
    (paper / "tables" / "pipelines.tex").write_text("\n".join(L))

    # Table: intervention transitions (nl), block and repair, by clause / profile / market
    def row(lbl, v):
        per_dec = v["mean"]
        return (f"{lbl} & {v['int']} & {v['helpful']} & {v['harmful']} & {v['neutral']} & "
                f"{ci(v['mean'], v['lo'], v['hi'])} \\\\")
    L = [r"\begin{tabular}{lrrrrr}", r"\toprule",
         r"Stratum & Int. & Help & Harm & Neut. & $\Delta u$ per decision (bp) \\", r"\midrule",
         r"\multicolumn{6}{l}{\emph{Block (veto $\rightarrow$ WAIT), by clause}}\\"]
    clause_lbl = {"size": "size only", "stop": "stop only", "size+stop": "size + stop", "conf": "confidence only",
                  "conf+size": "conf. + size", "conf+stop": "conf. + stop", "conf+size+stop": "all three"}
    for c in ("size", "size+stop", "stop", "conf", "conf+size", "conf+stop", "conf+size+stop"):
        k = f"pnl|nl|block|clause|{c}"
        if k in inter and inter[k]["int"] >= 10:
            L.append(row(clause_lbl[c], inter[k]))
    L.append(r"\midrule \multicolumn{6}{l}{\emph{Block, by profile}}\\")
    for p in PROF:
        L.append(row(PNAME[p], inter[f"pnl|nl|block|policy|{p}"]))
    L.append(r"\midrule \multicolumn{6}{l}{\emph{Repair (gate, clip size, tighten stop), by profile}}\\")
    for p in PROF:
        L.append(row(PNAME[p], inter[f"pnl|nl|repair|policy|{p}"]))
    L.append(r"\midrule \multicolumn{6}{l}{\emph{By market (block / repair)}}\\")
    for r, nm in (("US", "US"), ("IN", "NSE")):
        L.append(row(f"{nm}, block", inter[f"pnl|nl|block|region|{r}"]))
        L.append(row(f"{nm}, repair", inter[f"pnl|nl|repair|region|{r}"]))
    L += [r"\bottomrule", r"\end{tabular}"]
    (paper / "tables" / "interventions.tex").write_text("\n".join(L))
    print("tables written")



# =============================================================================== macros
def write_macros(N: dict, paper: Path) -> None:
    """Every number quoted in the prose comes from here (tables/macros.tex), never typed by hand."""
    M = {}
    pct = lambda x: f"{100 * x:.0f}\\%"
    f1 = lambda x: f"{x:+.1f}" if x is not None else "--"
    f2 = lambda x: f"{x:.2f}" if x is not None else "--"
    cir = lambda t, d=1: f"{t[0]:+.{d}f} [{t[1]:+.{d}f}, {t[2]:+.{d}f}]"
    M["NRows"] = f"{N['rows']:,}".replace(",", "{,}")
    M["NBundles"] = f"{N['bundles']:,}".replace(",", "{,}")
    tag = {"gpt-4o-mini": "Fo", "gpt-4.1-mini": "Fone", "gpt-5-mini": "Five"}
    for m in N["models"]:
        for s, st in (("nl", "Nl"), ("explicit", "Ex")):
            v = N["violations"][f"{m}|{s}"]
            M[f"trade{tag[m]}{st}"] = pct(v["trade_rate"])
            M[f"vetoTr{tag[m]}{st}"] = pct(v["veto_of_trades"]) if v["veto_of_trades"] is not None else "--"
            M[f"overcap{tag[m]}{st}"] = f"{v['mean_size_over_cap']:.1f}" if v["mean_size_over_cap"] else "--"
        M[f"consSize{tag[m]}"] = f"{N['nl_mean_size_by_profile']['conservative'][m]:.1f}"
    for util, u in (("pnl", ""), ("pnlx", "X")):
        for s, st in (("nl", "Nl"), ("explicit", "Ex")):
            c = N["components"][f"{util}|pooled|{s}"]
            M[f"sel{st}{u}"] = cir(c["d_sel"], 2)
            M[f"llmPT{st}{u}"] = cir(c["llm_per_trade"], 2)
            M[f"codePT{st}{u}"] = cir(c["code_per_trade"], 2)
            M[f"size{st}{u}"] = cir(c["d_size"], 2)
            M[f"rho{st}{u}"] = f"{c['size_rho']:+.3f}"
            M[f"exit{st}{u}"] = cir(c["d_exit"], 2)
            M[f"exitNone{st}{u}"] = cir(c["d_exit_none"], 2)
            M[f"auc{st}{u}"] = f"{c['auc'][0]:.3f} [{c['auc'][1]:.3f}, {c['auc'][2]:.3f}]"
            M[f"hitLlm{st}{u}"] = pct(c["hit_llm"])
            M[f"hitCode{st}{u}"] = pct(c["hit_code"])
            M[f"uTrade{st}"] = pct(c["u_trade_rate"])
            M[f"cTrade{st}"] = pct(c["c_trade_rate"])
            M[f"confSd{st}"] = f"{c['conf_sd']:.3f}"
        aucs = [N["components"][f"{util}|{m}|{s}"]["auc"][0] for m in N["models"] for s in ("nl", "explicit")]
        rhos = [N["components"][f"{util}|{m}|{s}"]["size_rho"] for m in N["models"] for s in ("nl", "explicit")]
        M[f"aucMin{u}"], M[f"aucMax{u}"] = f"{min(aucs):.2f}", f"{max(aucs):.2f}"
        M[f"rhoMin{u}"], M[f"rhoMax{u}"] = f"{min(rhos):+.2f}", f"{max(rhos):+.2f}"
        for s, st in (("nl", "Nl"), ("explicit", "Ex")):
            for name, nm in (("raw", "Raw"), ("block", "Block"), ("repair", "Repair"), ("judge", "Judge"), ("code", "Code")):
                v = N["pipelines"][f"{util}|pooled|{s}|all|{name}"]
                M[f"pipe{nm}{st}{u}"] = cir(v["mean"], 2)
                M[f"cvar{nm}{st}{u}"] = f"{v['cvar5']:.0f}"
                M[f"trd{nm}{st}"] = pct(v["trade_rate"])
                M[f"exp{nm}{st}"] = f"{v['exposure']:.1f}"
        for guard, g in (("block", "Block"), ("repair", "Repair")):
            v = N["interventions"][f"{util}|nl|{guard}|all|all"]
            M[f"int{g}{u}"] = f"{v['int']:,}".replace(",", "{,}")
            M[f"help{g}{u}"] = f"{v['helpful']:,}".replace(",", "{,}")
            M[f"harm{g}{u}"] = f"{v['harmful']:,}".replace(",", "{,}")
            M[f"helpShare{g}{u}"] = pct(v["help_share"])
            M[f"dAll{g}{u}"] = cir((v["mean"], v["lo"], v["hi"]), 2)
            M[f"dInt{g}{u}"] = cir((v["mean_int"], v["lo_int"], v["hi_int"]), 2)
            for p, pn in (("conservative", "Cons"), ("long_term", "Long"), ("intraday", "Intra"), ("aggressive_growth", "Aggr")):
                w = N["interventions"][f"{util}|nl|{guard}|policy|{p}"]
                M[f"d{g}{pn}{u}"] = cir((w["mean"], w["lo"], w["hi"]), 2)
                M[f"hs{g}{pn}{u}"] = pct(w["help_share"])
            for r, rn in (("US", "Us"), ("IN", "In")):
                w = N["interventions"][f"{util}|nl|{guard}|region|{r}"]
                M[f"d{g}{rn}{u}"] = cir((w["mean"], w["lo"], w["hi"]), 2)
        for c, cn in (("stop", "Stop"), ("conf", "Conf"), ("size", "Size"), ("size+stop", "SizeStop")):
            k = f"{util}|nl|block|clause|{c}"
            if k in N["interventions"]:
                w = N["interventions"][k]
                M[f"cl{cn}{u}"] = cir((w["mean"], w["lo"], w["hi"]), 2)
                M[f"clN{cn}{u}"] = f"{w['int']:,}".replace(",", "{,}")
                M[f"clH{cn}{u}"] = f"{w['helpful']:,}".replace(",", "{,}")
                M[f"clX{cn}{u}"] = f"{w['harmful']:,}".replace(",", "{,}")
                M[f"clP{cn}{u}"] = "$<$0.001" if w["p"] is not None and w["p"] < 1e-3 else (f"{w['p']:.2f}" if w["p"] is not None else "--")
    for p, pn in (("conservative", "Cons"), ("long_term", "Long"), ("intraday", "Intra"), ("aggressive_growth", "Aggr")):
        e = N["exit_medians"].get(f"nl|{p}")
        if e:
            M[f"stopMed{pn}"], M[f"tpMed{pn}"] = f"{e['stop']:g}", f"{e['tp']:g}"
    for r, rn in (("IN", "In"), ("US", "Us")):
        c = N["robust"][f"pnl|region|{r}"]
        M[f"auc{rn}"] = f"{c['auc'][0]:.2f} [{c['auc'][1]:.2f}, {c['auc'][2]:.2f}]"
        M[f"sel{rn}"] = cir(c["d_sel"], 2)
        M[f"exit{rn}"] = cir(c["d_exit"], 2)
        M[f"rho{rn}"] = f"{c['size_rho']:+.3f}"
    c = N["robust"]["pnl|core40"]
    M["selCore"], M["aucCore"], M["exitCore"] = cir(c["d_sel"], 2), f"{c['auc'][0]:.2f}", cir(c["d_exit"], 2)
    for util, u in (("pnl", ""), ("pnlx", "X")):
        for m, mt in (("gpt-4o-mini", "Fo"), ("gpt-4.1-mini", "Fone"), ("gpt-5-mini", "Five")):
            for guard, g in (("block", "Block"), ("repair", "Repair")):
                w = N["interventions"].get(f"{util}|nl|{guard}|model|{m}")
                if w:
                    M[f"d{g}{mt}{u}"] = cir((w["mean"], w["lo"], w["hi"]), 2)
        w = N["interventions"].get(f"{util}|nl|agent|all|all")
        if w:
            M[f"dAllAgent{u}"] = cir((w["mean"], w["lo"], w["hi"]), 2)
    nf = Path("logs/exp_pit_20261012/analysis/noise_floor.json")
    if nf.exists():
        z = json.loads(nf.read_text())
        for s_, st in (("nl", "Nl"), ("explicit", "Ex")):
            M[f"nfAction{st}"] = pct(z[s_]["same_action"])
            M[f"nfSize{st}"] = pct(z[s_]["same_size_if_both_trade"])
            M[f"nfVerdict{st}"] = pct(z[s_]["same_verdict"])
            M[f"nfRawOne{st}"], M[f"nfRawTwo{st}"] = f"{z[s_]['raw_run1']:+.2f}", f"{z[s_]['raw_run2']:+.2f}"
            M[f"nfRepOne{st}"], M[f"nfRepTwo{st}"] = f"{z[s_]['repair_run1']:+.2f}", f"{z[s_]['repair_run2']:+.2f}"
    if "agent" in N:
        M["agentN"] = f"{N['agent']['reviewed']:,}".replace(",", "{,}")
        M["agentResid"] = pct(N["agent"]["residual_veto"])
        M["agentWait"] = pct(N["agent"]["to_wait"])
    lines = [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in M.items()]
    (paper / "tables" / "macros.tex").write_text("\n".join(lines) + "\n")
    print(f"{len(M)} macros written")


if __name__ == "__main__":
    main()
