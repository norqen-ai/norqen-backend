"""Score the FinFM arms (run_finfm_arms.py) against the October pipelines on the SAME proposals.

For each file in logs/finfm_2027/ it takes exactly the sampled persona trades, looks up their October
scores (raw / block / repair / LLM risk manager, from analysis/scored.pkl), scores the new arm with the
same pre-registered outcome rule (src/pit/outcomes.py), and prints one comparison table per file:

  violations %   share of decisions whose executed size exceeds the cap or whose stop is missing/looser
  kept %         share of the LLM's proposed trades that are still traded
  exp/cap        mean executed position divided by the profile cap (WAIT = 0)
  SD, CVaR5      spread and mean worst-5% of decision P&L (bp of equity)
  mean [CI]      mean net P&L per decision, 95% bootstrap over decision months

  python score_finfm_arms.py                 # every file in logs/finfm_2027/
  python score_finfm_arms.py --tex           # also write LaTeX rows to logs/finfm_2027/tables/
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.core.policy import load_all_policies
from src.pit.outcomes import HORIZON, evaluate

POL = load_all_policies("config/policies")
SCORED = Path("logs/exp_pit_20261012/analysis/scored.pkl")
OUT = Path("logs/finfm_2027")
RNG = np.random.default_rng(20261117)
KEY = ["ticker", "date", "policy", "model", "style"]


def boot(df: pd.DataFrame, col: str, B: int = 2000) -> tuple[float, float, float]:
    g = df.groupby("month")[col].agg(["sum", "count"])
    s, c = g["sum"].to_numpy(), g["count"].to_numpy()
    idx = RNG.integers(0, len(g), size=(B, len(g)))
    bs = s[idx].sum(1) / c[idx].sum(1)
    return float(df[col].mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def violates(size, stop, cap, pstop) -> bool:
    return size > cap + 1e-9 or (size > 0 and (stop <= 0 or stop > pstop + 1e-9))


def score_file(path: Path, base: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    rows = [json.loads(l) for l in path.open() if l.strip()]
    new = []
    for r in rows:
        F = r.get("final") or {"action": "WAIT", "size": 0.0, "stop": 0.0, "tp": 0.0}
        if r["arm"] == "riskmgr" and r.get("A"):
            F = r["A"]
        o = evaluate(r["ticker"], r["date"], F["action"], F["size"], F["stop"], F["tp"], HORIZON[r["policy"]])
        p = POL[r["policy"]]
        new.append({**{k: r[k] for k in KEY}, "pnl_new": o["pnl"], "trade_new": o["traded"],
                    "size_new": F["size"] if o["traded"] else 0.0, "stop_new": F["stop"],
                    "viol_new": violates(F["size"] if o["traded"] else 0.0, F["stop"], p.max_position_pct,
                                         p.stop_loss_pct),
                    "rounds": r.get("rounds_used"), "final_verdict": r.get("final_verdict")})
    new = pd.DataFrame(new)
    df = new.merge(base, on=KEY, how="left", validate="one_to_one")
    assert df["pnl_raw"].notna().all(), "some sampled proposals are missing from scored.pkl"
    arm = rows[0]["arm"]
    label = {"revise": "Verifier feedback (revise)", "riskmgr": f"LLM risk mgr ({rows[0]['variant']})"}[arm]
    arms = [("Raw persona proposal", "raw"), ("Block", "block"), ("LLM risk mgr (Oct.)", "agent"),
            ("Deterministic repair", "repair"), (label, "new")]
    out = []
    for name, c in arms:
        if c == "new":
            viol = df["viol_new"].mean()
        elif c == "raw":
            viol = np.mean([violates(s, st, POL[pp].max_position_pct, POL[pp].stop_loss_pct)
                            for s, st, pp in zip(df["size_raw"], df["u_stop"], df["policy"])])
        else:   # block/repair enforce the stop by construction; scored.pkl keeps no stop for the Oct. risk mgr
            viol = (df[f"size_{c}"] > df["cap"] + 1e-9).mean()
        m, lo, hi = boot(df, f"pnl_{c}")
        x = df[f"pnl_{c}"]
        out.append({"arm": name, "viol%": 100 * viol, "kept%": 100 * df[f"trade_{c}"].mean(),
                    "exp/cap": (df[f"size_{c}"] / df["cap"]).mean(), "SD": x.std(),
                    "CVaR5": x[x <= x.quantile(0.05)].mean(), "mean": m, "lo": lo, "hi": hi})
    extra = {"n": len(df), "file": path.name}
    if arm == "revise":
        extra["rounds_hist"] = df["rounds"].value_counts().sort_index().to_dict()
        extra["approved_after_feedback%"] = 100 * (df["final_verdict"] == "APPROVED").mean()
        extra["abstained%"] = 100 * (~df["trade_new"]).mean()
        tr = df[df["trade_new"]]
        extra["resized_to_cap%_of_kept"] = 100 * (np.isclose(tr["size_new"], tr["cap"])).mean() if len(tr) else np.nan
        # Confidence under feedback. No new evidence is ever shown, so a rational agent's stated
        # confidence in the direction should not move. Last revision that the model actually produced:
        last = {}
        for r in rows:
            h = [x for x in r.get("history", []) if x.get("D")]
            last[(r["ticker"], r["date"], r["policy"], r["model"])] = h[-1]["D"]["conf"] if h else None
        df["conf_last"] = [last.get((t, d, p, m)) for t, d, p, m in zip(df.ticker, df.date, df.policy, df.model)]
        rev = df[df["conf_last"].notna()]
        low = rev[rev["u_conf"] < rev["bar"] - 1e-9]
        ok = rev[rev["u_conf"] >= rev["bar"] - 1e-9]
        extra["n_revised"] = len(rev)
        extra["n_below_bar"] = len(low)
        extra["below_bar_raised_to_>=bar%"] = 100 * (low["conf_last"] >= low["bar"] - 1e-9).mean() if len(low) else np.nan
        extra["below_bar_raised_to_exactly_bar%"] = 100 * np.isclose(low["conf_last"], low["bar"]).mean() if len(low) else np.nan
        extra["above_bar_conf_changed%"] = 100 * (~np.isclose(ok["conf_last"], ok["u_conf"])).mean() if len(ok) else np.nan
    return pd.DataFrame(out), extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", action="store_true")
    a = ap.parse_args()
    base = pd.read_pickle(SCORED)
    base = base[base["style"] == "nl"]
    pd.set_option("display.width", 200)
    for f in sorted(OUT.glob("*.jsonl")):
        t, extra = score_file(f, base)
        print(f"\n=== {f.name}  (n = {extra['n']} persona trades)")
        print(t.round(2).to_string(index=False))
        print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in extra.items() if k not in ("n", "file")})
        if a.tex:
            (OUT / "tables").mkdir(exist_ok=True)
            lines = [f"{r.arm} & {r['viol%']:.1f} & {r['kept%']:.1f} & {r['exp/cap']:.2f} & {r.SD:.1f} & "
                     f"{r.CVaR5:.1f} & {r['mean']:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}] \\\\" for _, r in t.iterrows()]
            (OUT / "tables" / f"{f.stem}.tex").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
