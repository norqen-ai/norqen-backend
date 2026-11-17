"""Build point-in-time evidence bundles: every stock x every monthly decision date.

Each bundle freezes all five agents' evidence AS OF date t (src/pit/agents.py) plus the
realised volatility used for sizing, so decisions can be replayed later under any profile
and any decision model.

  python build_pit_bundles.py                      # all 100 stocks x 19 dates
  python build_pit_bundles.py --tickers AAPL,TCS.NS --dates 2025-01-15
"""
from __future__ import annotations

import argparse
import json
import pickle
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from src.audit.log import EvidenceBundle
from src.core.sizing import realized_ann_vol
from src.pit import agents, data
from src.pit.universe import all_tickers, region

OUT = Path("logs/exp_pit_20261012")


def build_one(ticker: str, t: pd.Timestamp, name: str | None, out: Path) -> str:
    path = out / "bundles" / f"{ticker}_{t.date()}.json"
    if path.exists():
        return "cached"
    closes = data.asof(ticker, t)["Close"].values[-63:]          # ~3 months, as the live runner
    ctx = {"ann_vol": realized_ann_vol(closes), "date": str(t.date()), "region": region(ticker)}
    ev = agents.gather(ticker, t, name)
    b = EvidenceBundle(ticker, ev, ts=t.timestamp(), context=ctx)
    path.write_text(json.dumps({"ticker": ticker, "ts": b.ts, "context": ctx,
                                "evidence": [e.to_dict() for e in ev]}, indent=1))
    return "built"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default=None)
    ap.add_argument("--dates", default=None)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--start", default="2025-01-15", help="first decision month (A2 extension: 2024-07-15)")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out)
    (out / "bundles").mkdir(parents=True, exist_ok=True)
    names = {t: v.get("name") for t, v in pickle.loads((data.ROOT / "fundamentals.pkl").read_bytes()).items()}
    tickers = a.tickers.split(",") if a.tickers else all_tickers()
    jobs = []
    for tk in tickers:
        dates = [pd.Timestamp(d) for d in a.dates.split(",")] if a.dates else data.decision_dates(start=a.start, region_code=region(tk))
        jobs += [(tk, d) for d in dates]
    print(f"{len(jobs)} bundles -> {out}/bundles", flush=True)
    t0, n, fails = time.time(), 0, []
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(build_one, tk, d, names.get(tk), out): (tk, d) for tk, d in jobs}
        for f in as_completed(futs):
            n += 1
            try:
                f.result()
            except Exception as e:
                fails.append((futs[f][0], str(futs[f][1].date()), repr(e)[:100]))
            if n % 100 == 0:
                print(f"{n}/{len(jobs)}  {time.time() - t0:.0f}s  fails={len(fails)}", flush=True)
    print(f"done {n} in {time.time() - t0:.0f}s; failures: {len(fails)}", fails[:10], flush=True)


if __name__ == "__main__":
    main()
