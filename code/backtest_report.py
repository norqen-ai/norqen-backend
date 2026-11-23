"""Run the leakage-safe backtester and report the quant metrics.

  python3 backtest_report.py --ticker NVDA --signal combo --policy long_term
  python3 backtest_report.py --universe --limit 8 --signal combo --policy long_term

Aggregates Sharpe / IC across names — the honest quant read-out for a signal. No LLM.
"""
import argparse
import json

import numpy as np

from src.core.policy import load_policy
from src.data.market import fetch_ohlcv, add_indicators
from src.backtest.signals import SIGNALS
from src.backtest.engine import run_backtest


def one(ticker, policy, signal_fn, signal_name, period="3y"):
    df = add_indicators(fetch_ohlcv(ticker, period=period))
    return run_backtest(df, policy, signal_fn, ticker=ticker, signal_name=signal_name)


def line(res):
    p = res.performance
    return (f"  {res.ticker:<13} Sharpe={p['Sharpe']:>5.2f}  Sortino={p['Sortino']:>5.2f}  "
            f"maxDD={p['max_drawdown']:>6.1%}  CAGR={p['CAGR']:>7.1%}  "
            f"IC={res.ic['IC']:+.3f}(t={res.ic['t_stat']:+.1f})  trades={res.n_trades}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="NVDA")
    ap.add_argument("--signal", default="combo", choices=list(SIGNALS))
    ap.add_argument("--policy", default="long_term")
    ap.add_argument("--universe", action="store_true")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--period", default="3y")
    args = ap.parse_args()

    policy = load_policy(f"config/policies/{args.policy}.json")
    sig = SIGNALS[args.signal]
    print(f"=== backtest: signal='{args.signal}'  policy='{args.policy}'  period={args.period} ===")

    if args.universe:
        uni = json.load(open("config/universe.json"))
        tickers = (uni["US"] + uni["NSE"])[:args.limit]
        results = []
        for t in tickers:
            try:
                r = one(t, policy, sig, args.signal, args.period)
                results.append(r)
                print(line(r))
            except Exception as e:
                print(f"  {t:<13} skipped ({repr(e)[:50]})")
        if results:
            ics = np.array([r.ic["IC"] for r in results])
            shp = np.array([r.performance["Sharpe"] for r in results])
            sig_frac = np.mean([abs(r.ic["t_stat"]) > 2 for r in results if np.isfinite(r.ic["t_stat"])])
            print("\n  " + "-" * 60)
            print(f"  UNIVERSE ({len(results)} names): mean IC={ics.mean():+.3f}  "
                  f"mean Sharpe={np.nanmean(shp):+.2f}  |t|>2 in {sig_frac:.0%} of names")
            print("  (mean IC near 0 => these simple signals are ~noise — the honest quant reality.)")
    else:
        print(line(one(args.ticker, policy, sig, args.signal, args.period)))


if __name__ == "__main__":
    main()
