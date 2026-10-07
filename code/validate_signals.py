"""Signal validation — which signals actually have edge? (Information Coefficient.)

Runs every numeric signal over the universe and reports mean IC and the fraction of names
where the edge is statistically significant (|t|>2). This is how a quant desk decides
whether to trust a signal at all — and it keeps us honest about weak signals.

  python3 validate_signals.py --limit 10
"""
import argparse
import json

import numpy as np

from src.core.policy import load_policy
from src.data.market import fetch_ohlcv, add_indicators
from src.backtest.signals import SIGNALS
from src.backtest.engine import run_backtest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", default="long_term")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--period", default="3y")
    args = ap.parse_args()

    policy = load_policy(f"config/policies/{args.policy}.json")
    uni = json.load(open("config/universe.json"))
    tickers = (uni["US"] + uni["NSE"])[:args.limit]
    dfs = []
    for t in tickers:
        try:
            dfs.append((t, add_indicators(fetch_ohlcv(t, period=args.period))))
        except Exception as e:
            print(f"  {t}: skipped ({repr(e)[:45]})")

    print(f"=== signal IC validation over {len(dfs)} names ===\n")
    print(f"{'signal':<16}{'mean IC':>10}{'mean rank-IC':>14}{'|t|>2 names':>13}")
    for name, fn in SIGNALS.items():
        ics, rics, sig = [], [], []
        for _, df in dfs:
            r = run_backtest(df, policy, fn, signal_name=name)
            if np.isfinite(r.ic["IC"]):
                ics.append(r.ic["IC"]); rics.append(r.ic["rank_IC"])
                sig.append(abs(r.ic["t_stat"]) > 2 if np.isfinite(r.ic["t_stat"]) else False)
        if ics:
            print(f"{name:<16}{np.mean(ics):>+10.3f}{np.mean(rics):>+14.3f}{np.mean(sig):>12.0%}")
    print("\n(IC near 0 = noise. This is why the LLM agents — reading news/fundamentals — must")
    print(" beat these numeric baselines to justify their cost. Same engine measures them.)")


if __name__ == "__main__":
    main()
