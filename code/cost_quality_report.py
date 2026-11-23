"""RQ3 read-out — the cost vs quality frontier of adaptive evidence gathering.
  python3 cost_quality_report.py --limit 8
No LLM: uses the cheap numeric signals as stand-in evidence sources.
"""
import argparse
import json

from src.data.market import fetch_ohlcv, add_indicators
from src.eval.cost_quality import frontier, format_frontier


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--period", default="3y")
    args = ap.parse_args()

    uni = json.load(open("config/universe.json"))
    tickers = (uni["US"] + uni["NSE"])[:args.limit]
    dfs = []
    for t in tickers:
        try:
            dfs.append(add_indicators(fetch_ohlcv(t, period=args.period)))
        except Exception as e:
            print(f"  {t}: skipped ({repr(e)[:45]})")
    print(f"=== RQ3 over {len(dfs)} names ===\n")
    rows = frontier(dfs, thresholds=[0.30, 0.40, 0.50, 0.60, 0.65])
    print(format_frontier(rows))


if __name__ == "__main__":
    main()
