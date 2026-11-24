"""Generate every number in the FinFM paper (../paper_finfm/) from the logs. Never hand-edit a number.

  python make_finfm_tables.py        # writes ../paper_finfm/tables/{enforcement,confidence,macros}.tex

Table 1 (enforcement): October scored decisions, text-persona proposals, primary window, pooled models.
Table 2 (confidence under feedback): logs/finfm_2027/revise_*_confset.jsonl and their _hideconf controls.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

SCORED = Path("logs/exp_pit_20261012/analysis/scored.pkl")
ARMS = Path("logs/finfm_2027")
PAPER = Path("../paper_finfm")
RNG = np.random.default_rng(20261117)
MODEL_NAMES = {"gpt-4o-mini": "gpt-4o-mini", "gpt-4.1-mini": "gpt-4.1-mini", "gpt-5-mini": "gpt-5-mini",
               "llama-3.3-70b": "Llama-3.3-70B", "llama-4-scout": "Llama-4-Scout",
               "gpt-oss-120b": "gpt-oss-120b", "gpt-oss-20b": "gpt-oss-20b"}   # rows appear only when files exist
# Table 1 and the pooled headline macros use only these models, so adding an open-weight model never
# silently changes the abstract's numbers. To pool more models, add them here AND update "three models"
# in the abstract, Setup and captions.
MAIN_MODELS = {"gpt-4o-mini", "gpt-4.1-mini", "gpt-5-mini"}


def boot(df: pd.DataFrame, col: str, B: int = 2000):
    g = df.groupby("month")[col].agg(["sum", "count"])
    s, c = g["sum"].to_numpy(), g["count"].to_numpy()
    idx = RNG.integers(0, len(g), size=(B, len(g)))
    bs = s[idx].sum(1) / c[idx].sum(1)
    return float(df[col].mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)


def enforcement(macros: dict) -> str:
    df = pd.read_pickle(SCORED)
    df = df[df["model"].isin(MAIN_MODELS)]
    nl, ex = df[df["style"] == "nl"], df[df["style"] == "explicit"]
    u_tr = nl["u_trade"]
    rows = [("Raw persona proposal", nl, "raw"), ("Block (veto $\\to$ WAIT)", nl, "block"),
            ("LLM risk manager", nl, "agent"), ("Deterministic repair", nl, "repair"),
            ("Limits stated in prompt", ex, "raw"), ("Code only", nl, "code")]
    out = []
    for name, d, c in rows:
        viol = 100 * (d[f"size_{c}"] > d["cap"] + 1e-9).mean()
        trade = 100 * d[f"trade_{c}"].mean()
        kept = 100 * d.loc[d["u_trade"], f"trade_{c}"].mean() if c in ("block", "agent", "repair") else np.nan
        util = (d[f"size_{c}"] / d["cap"]).mean()
        x = d[f"pnl_{c}"]
        cvar = x[x <= x.quantile(0.05)].mean()
        piv = d.pivot_table(index=["ticker", "date", "model"], columns="policy", values=f"size_{c}")
        ratio = piv["aggressive_growth"].mean() / piv["conservative"].mean() if piv["conservative"].mean() > 0 else np.nan
        m, lo, hi = boot(d, f"pnl_{c}")
        out.append(f"{name} & {viol:.1f} & {trade:.1f} & {'--' if np.isnan(kept) else f'{kept:.1f}'} & "
                   f"{util:.2f} & {'--' if np.isnan(ratio) else f'{ratio:.1f}'} & {x.std():.1f} & {cvar:.1f} & "
                   f"{m:+.2f} [{lo:+.2f}, {hi:+.2f}] \\\\")
    macros["NPersona"] = f"{len(nl):,}"
    macros["NBundles"] = f"{nl.groupby(['ticker', 'date']).ngroups:,}"
    macros["PersonaViol"] = f"{100 * (nl['size_raw'] > nl['cap'] + 1e-9).mean():.1f}"
    macros["VetoRate"] = f"{100 * (nl.loc[u_tr, 'verdict'] == 'VETOED').mean():.0f}"
    for c, k in (("block", "Block"), ("agent", "Agent"), ("repair", "Repair")):
        macros[f"Kept{k}"] = f"{100 * nl.loc[u_tr, f'trade_{c}'].mean():.1f}"
    return "\n".join(out) + "\n"


def confidence(macros: dict) -> str:
    out = []
    pooled = {"shown": [0, 0], "hidden": [0, 0]}
    found = {f.name[len("revise_"):].split("_r3")[0] for f in ARMS.glob("revise_*_r3_confset.jsonl")}
    for m in list(MODEL_NAMES) + sorted(found - set(MODEL_NAMES)):   # any newly run model gets a row
        cells = []
        for tag in ("", "_hideconf"):
            f = ARMS / f"revise_{m}_r3{tag}_confset.jsonl"
            if not f.exists():
                cells.append(None)
                continue
            rows = [json.loads(l) for l in f.open() if l.strip()]
            # Like-for-like: keep proposals that ALSO broke a size/stop clause, so both arms get a revision
            # round; the only difference is whether the feedback mentions the confidence bar.
            rows = [r for r in rows if any("below policy threshold" not in s for s in r["U_reasons"])]
            n = len(rows)
            raised = kept = 0
            for r in rows:
                h = [x for x in r.get("history", []) if x.get("D")]
                bar = r["U_reasons"] and float(next(s for s in r["U_reasons"] if "below policy threshold" in s)
                                               .split("threshold")[1].strip())
                if h and h[-1]["D"]["conf"] >= bar - 1e-9:
                    raised += 1
                kept += r["final"]["action"] in ("BUY", "SELL") and r["final"]["size"] > 0
            cells.append((n, raised, kept))
            if m in MAIN_MODELS:
                pooled["hidden" if tag else "shown"][0] += raised
                pooled["hidden" if tag else "shown"][1] += n
        if cells[0] is None:
            continue
        (n, r1, k1), c2 = cells[0], cells[1]
        lo, hi = wilson(r1, n)
        s = f"{MODEL_NAMES.get(m, m)} & {n} & {100 * r1 / n:.1f} [{np.floor(lo):.0f}, {np.ceil(hi):.0f}] & "
        if c2:
            lo2, hi2 = wilson(c2[1], c2[0])
            s += f"{100 * c2[1] / c2[0]:.1f} [{np.floor(lo2):.0f}, {np.ceil(hi2):.0f}] & "
        else:
            s += "-- & "
        s += f"{100 * k1 / n:.1f} \\\\"
        out.append(s)
    # LLM risk manager under two prompts (keep rate of proposed trades), per proposer model
    for f in sorted(ARMS.glob("riskmgr_*_by_*.jsonl")):
        rows = [json.loads(l) for l in f.open() if l.strip()]
        kept = sum(1 for r in rows if r.get("A") and r["A"]["action"] in ("BUY", "SELL") and r["A"]["size"] > 0)
        m, rest = f.stem[len("riskmgr_"):].split("_by_")
        variant = "RepairFirst" if rest.endswith("repair_first") else "Orig"
        tag = {"gpt-4o-mini": "FourO", "gpt-4.1-mini": "FourOne", "gpt-5-mini": "Five",
               "llama-3.3-70b": "Llama", "llama-4-scout": "Scout",
               "gpt-oss-120b": "OssBig", "gpt-oss-20b": "OssSmall"}.get(m, m)
        macros[f"RiskMgrKept{variant}{tag}"] = f"{100 * kept / len(rows):.1f}"
    for k, (r, n) in pooled.items():
        if n:
            macros[f"ConfRaised{k.capitalize()}"] = f"{100 * r / n:.0f}"
            macros[f"ConfN{k.capitalize()}"] = f"{n:,}"
    return "\n".join(out) + "\n" if out else "\\multicolumn{6}{c}{(run run\\_finfm\\_arms.py first)} \\\\\n"


def matched_table():
    source = ARMS / "matched_confidence.json"
    if not source.exists():
        return
    results = json.loads(source.read_text())
    rows = []
    for model, result in results.items():
        if "hit" not in result:
            continue
        cells = []
        for metric, scale in (("hit", 100), ("pnl", 1)):
            d = result[metric]
            lo, hi = d["ci95"]
            cells.append(f"{scale*d['difference']:+.2f} [{scale*lo:+.2f}, {scale*hi:+.2f}]")
        rows.append(f"{model} & {result['n_raised']} & {result['n_above']} & " + " & ".join(cells) + r" \\")
    (PAPER / "tables" / "matched.tex").write_text(
        r"\begin{tabular}{lrrll}" + "\n" + r"\toprule" + "\n" +
        r"Model & Raised & Above & Hit difference (pp) & P\&L difference (bp) \\" + "\n" +
        r"\midrule" + "\n" + "\n".join(rows) + "\n" + r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")


def main():
    (PAPER / "tables").mkdir(parents=True, exist_ok=True)
    from src.core.policy import load_all_policies
    from src.pit.outcomes import HORIZON
    profiles = []
    for name, policy in load_all_policies("config/policies").items():
        profiles.append(f"{name.replace('_', ' ')} & {policy.max_position_pct:g} & {policy.stop_loss_pct:g} & {policy.confidence_to_act:g} & {HORIZON[name]}" + r" \\")
    (PAPER / "tables" / "profiles.tex").write_text(
        r"\begin{tabular}{lrrrr}" + "\n" + r"\toprule" + "\n" +
        r"Profile & Cap & Stop & Bar & Horizon \\" + "\n" + r"\midrule" + "\n" +
        "\n".join(profiles) + "\n" + r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")
    matched_table()
    macros: dict = {}
    (PAPER / "tables" / "enforcement.tex").write_text(
        "\\begin{tabular}{lrrrrrrrl}\n\\toprule\n"
        "Pipeline & Viol.\\,\\% & Trades\\,\\% & Kept\\,\\% & Exp./cap & Aggr./Cons. & SD & CVaR$_5$ & "
        "Mean P\\&L [95\\% CI] \\\\\n\\midrule\n" + enforcement(macros) + "\\bottomrule\n\\end{tabular}\n")
    (PAPER / "tables" / "confidence.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\n"
        " & & \\multicolumn{2}{c}{Raised to bar (\\%)} & Kept (\\%) \\\\\n"
        "Model & $n$ & bar shown & bar hidden & bar shown \\\\\n\\midrule\n"
        + confidence(macros) + "\\bottomrule\n\\end{tabular}\n")
    (PAPER / "tables" / "macros.tex").write_text(
        "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in sorted(macros.items())))
    print(json.dumps(macros, indent=1))


if __name__ == "__main__":
    main()
