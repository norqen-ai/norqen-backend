"""Point-in-time data caches: daily OHLCV, annual fundamentals, dated news headlines.

Leakage rules (PREREGISTRATION.md, amendment 2026-10-12):
  * prices/indicators at decision date t use rows with date <= t (the close of t);
  * annual statements are usable only if fiscal-year end + 90 days <= t;
  * headlines must be published in [t-7d, t+1d 00:00 UTC), i.e. before the next session opens;
  * the trade is entered at the OPEN of the next session (t+1), never at t.
Everything is cached under code/data/pit/ so runs are reproducible and resumable.
"""
from __future__ import annotations

import calendar
import json
import pickle
import re
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from src.data.market import add_indicators
from src.pit.universe import INDEX, all_tickers, region

ROOT = Path(__file__).resolve().parents[2] / "data" / "pit"
ROOT.mkdir(parents=True, exist_ok=True)
PRICE_START, PRICE_END = "2022-06-01", "2026-10-11"


# --------------------------------------------------------------------------- prices
def download_prices(tickers: list[str] | None = None) -> dict[str, pd.DataFrame]:
    import yfinance as yf
    path = ROOT / "prices.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    tickers = (tickers or all_tickers()) + list(INDEX.values())
    raw = yf.download(tickers, start=PRICE_START, end=PRICE_END, auto_adjust=True,
                      progress=False, group_by="ticker", threads=True)
    out = {}
    for t in tickers:
        try:
            df = raw[t][["Open", "High", "Low", "Close", "Volume"]].dropna()
        except KeyError:
            continue
        if len(df) > 300:
            df.index = pd.to_datetime(df.index).tz_localize(None)
            out[t] = df
    path.write_bytes(pickle.dumps(out))
    return out


_PRICES: dict | None = None


def prices() -> dict[str, pd.DataFrame]:
    global _PRICES
    if _PRICES is None:
        _PRICES = download_prices()
    return _PRICES


def asof(ticker: str, t: str | pd.Timestamp) -> pd.DataFrame:
    """OHLCV rows with date <= t (inclusive of t's close)."""
    df = prices()[ticker]
    return df[df.index <= pd.Timestamp(t)]


def asof_indicators(ticker: str, t, lookback_days: int = 130) -> pd.DataFrame:
    """Same indicator set as the live system (src/data/market.add_indicators) on a ~6-month
    window ending at t, mirroring MARKET.get_indicators(period='6mo')."""
    df = asof(ticker, t)
    return add_indicators(df.iloc[-lookback_days:])


def trading_days(ticker_or_index: str) -> pd.DatetimeIndex:
    return prices()[ticker_or_index].index


def decision_dates(start="2025-01-15", end="2026-07-15", region_code="US") -> list[pd.Timestamp]:
    """First trading session on/after the 15th of each month, using the index calendar of
    the region (NSE and NYSE holidays differ)."""
    cal = trading_days(INDEX[region_code])
    out, d = [], pd.Timestamp(start)
    while d <= pd.Timestamp(end):
        nxt = cal[cal >= d]
        if len(nxt):
            out.append(nxt[0])
        d = (d + pd.offsets.MonthBegin(1)).replace(day=15)
    return out


# --------------------------------------------------------------------------- fundamentals
def _row(df: pd.DataFrame, names: list[str]):
    for n in names:
        if n in df.index:
            return df.loc[n]
    return None


def download_fundamentals(tickers: list[str] | None = None) -> dict:
    """Annual income statement + balance sheet per ticker (yfinance gives ~4 fiscal years)."""
    import yfinance as yf
    path = ROOT / "fundamentals.pkl"
    cache = pickle.loads(path.read_bytes()) if path.exists() else {}
    for t in tickers or all_tickers():
        if t in cache:
            continue
        try:
            tk = yf.Ticker(t)
            cache[t] = {"income": tk.income_stmt, "balance": tk.balance_sheet,
                        "name": (tk.info or {}).get("shortName") or (tk.info or {}).get("longName")}
        except Exception as e:
            cache[t] = {"error": repr(e)[:120]}
        path.write_bytes(pickle.dumps(cache))
    return cache


_FUND: dict | None = None


def fundamentals_asof(ticker: str, t, lag_days: int = 90) -> dict:
    """Fundamentals usable at t: the latest fiscal year whose end + lag_days <= t.
    Returns the same fields the live fundamental agent reads (trailing P/E, profit margin,
    revenue growth, ROE) plus the fiscal-year end used, or {} if nothing is usable."""
    global _FUND
    if _FUND is None:
        _FUND = pickle.loads((ROOT / "fundamentals.pkl").read_bytes())
    f = _FUND.get(ticker, {})
    inc, bal = f.get("income"), f.get("balance")
    if inc is None or getattr(inc, "empty", True):
        return {}
    t = pd.Timestamp(t)
    cols = sorted([c for c in inc.columns if pd.Timestamp(c) + timedelta(days=lag_days) <= t], reverse=True)
    if not cols:
        return {}
    fy = cols[0]
    rev = _row(inc, ["Total Revenue", "Operating Revenue"])
    ni = _row(inc, ["Net Income", "Net Income Common Stockholders"])
    eps = _row(inc, ["Diluted EPS", "Basic EPS"])
    eq = _row(bal, ["Stockholders Equity", "Common Stock Equity", "Total Equity Gross Minority Interest"]) \
        if bal is not None and not bal.empty else None

    def val(s, c):
        try:
            v = float(s[c])
            return None if pd.isna(v) else v
        except Exception:
            return None

    r0, n0 = val(rev, fy) if rev is not None else None, val(ni, fy) if ni is not None else None
    prev = [c for c in inc.columns if pd.Timestamp(c) < pd.Timestamp(fy)]
    r1 = val(rev, max(prev)) if (rev is not None and prev) else None
    e0 = val(eps, fy) if eps is not None else None
    q0 = val(eq, fy) if (eq is not None and fy in getattr(eq, "index", [])) else None
    px = float(asof(ticker, t)["Close"].iloc[-1])
    return {
        "trailingPE": round(px / e0, 1) if e0 and e0 > 0 else None,
        "profitMargins": round(n0 / r0, 4) if (n0 is not None and r0) else None,
        "revenueGrowth": round(r0 / r1 - 1, 4) if (r0 and r1) else None,
        "returnOnEquity": round(n0 / q0, 4) if (n0 is not None and q0) else None,
        "fiscal_year_end": str(pd.Timestamp(fy).date()),
    }


# --------------------------------------------------------------------------- news
_SUFFIX = re.compile(r"\b(inc|corp|corporation|company|co|ltd|limited|plc|holdings?|group|the|class [ab]|"
                     r"incorporated|n\.?a\.?|& co)\b\.?", re.I)


# Yahoo truncates some NSE short names ("TATA CONSULTANCY SERV LT"); use the common market name.
NAME_OVERRIDE = {"TCS.NS": "TCS", "SUNPHARMA.NS": "Sun Pharma", "APOLLOHOSP.NS": "Apollo Hospitals",
                 "DRREDDY.NS": "Dr Reddy's", "DIVISLAB.NS": "Divi's Laboratories", "BPCL.NS": "BPCL",
                 "HDFCLIFE.NS": "HDFC Life", "ADANIPORTS.NS": "Adani Ports", "ONGC.NS": "ONGC",
                 "POWERGRID.NS": "Power Grid", "TATACONSUM.NS": "Tata Consumer"}


def company_query(ticker: str, name: str | None) -> str:
    base = ticker.split(".")[0]
    name = NAME_OVERRIDE.get(ticker, name)
    if name:
        clean = _SUFFIX.sub("", name).replace(",", " ").strip(" .")
        clean = re.sub(r"\(\s*\)", "", clean)
        clean = re.sub(r"\s+", " ", clean).strip(" .")
        if len(clean) >= 3:
            base = clean
    return f"{base} share price" if region(ticker) == "IN" else f"{base} stock"


def news_asof(ticker: str, t, name: str | None = None, limit: int = 8, window_days: int = 7) -> list[dict]:
    """Headlines published in [t - window_days, t + 1 day) via Google News RSS date operators,
    cached per (ticker, date). Same feed the live news module uses, but date-bounded."""
    import feedparser
    t = pd.Timestamp(t)
    d = ROOT / "news"
    d.mkdir(exist_ok=True)
    path = d / f"{ticker}_{t.date()}.json"
    if path.exists():
        return json.loads(path.read_text())
    after = (t - timedelta(days=window_days)).date()
    before = (t + timedelta(days=1)).date()
    q = f"{company_query(ticker, name)} after:{after} before:{before}"
    hl = "en-IN&gl=IN&ceid=IN:en" if region(ticker) == "IN" else "en-US&gl=US&ceid=US:en"
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl={hl}"
    entries, ok = [], False
    for attempt in range(5):
        feed = feedparser.parse(url)
        if getattr(feed, "status", None) == 200:
            entries, ok = feed.entries, True
            break
        time.sleep(3 + 5 * attempt)
    if not ok:                             # throttled/unreachable: do NOT cache as "no news"
        raise RuntimeError(f"news fetch failed for {ticker} {t.date()}")
    cutoff = datetime(before.year, before.month, before.day, tzinfo=timezone.utc).timestamp()
    out, seen = [], set()
    for e in entries:
        ts = calendar.timegm(e.published_parsed) if getattr(e, "published_parsed", None) else None
        if ts is None or ts >= cutoff:
            continue                       # drop undated or post-decision headlines (leakage guard)
        title = e.title.strip()
        key = title.lower()[:80]
        if key in seen:
            continue
        seen.add(key)
        src = e.get("source", {}).get("title") if isinstance(e.get("source"), dict) else "GoogleNews"
        out.append({"ts": ts, "title": title, "source": src or "GoogleNews"})
    out.sort(key=lambda x: x["ts"], reverse=True)
    out = out[:limit]
    path.write_text(json.dumps(out))
    return out
