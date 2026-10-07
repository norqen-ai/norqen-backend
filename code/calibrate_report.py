"""RQ2 read-out — is the confidence honest?

Runs leakage-safe backtests over the universe, pools every DIRECTIONAL call's
(confidence, was-it-right) pair, and reports the reliability curve + ECE/Brier +
temperature scaling.

  python3 calibrate_report.py --signal combo --policy long_term --limit 10

This measures the numeric signal's calibration (cheap, no LLM). The identical code
scores the LLM agent's confidence once we log live outcomes — that is RQ2 for the paper.
"""
import argparse
import json

import numpy as np

from src.core.policy import load_policy
from src.data.market import fetch_ohlcv, add_indicators
from src.backtest.signals import SIGNALS
from src.backtest.engine import run_backtest
from src.eval.calibration import calibration_report

DIRECTIONAL = 0.15


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signal", default="combo", choices=list(SIGNALS))
    ap.add_argument("--policy", default="long_term")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--period", default="3y")
    args = ap.parse_args()

    policy = load_policy(f"config/policies/{args.policy}.json")
    sig = SIGNALS[args.signal]
    uni = json.load(open("config/universe.json"))
    tickers = (uni["US"] + uni["NSE"])[:args.limit]

    conf, correct = [], []
    used = 0
    for t in tickers:
        try:
            df = add_indicators(fetch_ohlcv(t, period=args.period))
            res = run_backtest(df, policy, sig, ticker=t, signal_name=args.signal)
            used += 1
            for d in res.decisions:
                if abs(d["direction"]) >= DIRECTIONAL:
                    conf.append(d["confidence"])
                    correct.append(int(np.sign(d["direction"]) == np.sign(d["fwd_return"])))
        except Exception as e:
            print(f"  {t}: skipped ({repr(e)[:45]})")

    print(f"=== RQ2 calibration: signal='{args.signal}', {used} names, {len(conf)} directional calls ===\n")
    print(calibration_report(conf, correct))


if __name__ == "__main__":
    main()
