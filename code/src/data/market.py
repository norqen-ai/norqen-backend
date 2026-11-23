"""Market data pipeline (MALHAR). Requires: pip install yfinance pandas.

Design rule: every function returns plain pandas DataFrames with UTC timestamps,
and every derived indicator column is prefixed 'ind_'. NSE tickers use the
Yahoo suffix '.NS' for now; a jugaad-data/nsepy source can be added later
behind the same interface.
"""
from __future__ import annotations

try:
    import pandas as pd
    import yfinance as yf
    _HAS_DEPS = True
except ImportError:                     # keep the repo importable pre-venv
    _HAS_DEPS = False


def fetch_ohlcv(ticker: str, period: str = "2y", interval: str = "1d"):
    """Daily OHLCV for a US ('AAPL') or NSE ('RELIANCE.NS') ticker."""
    if not _HAS_DEPS:
        raise ImportError("run: pip install -r requirements.txt")
    df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
    if df.empty:
        raise ValueError(f"no data for {ticker}")
    df.index = df.index.tz_convert("UTC") if df.index.tz else df.index.tz_localize("UTC")
    return df[["Open", "High", "Low", "Close", "Volume"]]


def add_indicators(df):
    """Standard indicator set. Add new ones here; keep the 'ind_' prefix."""
    out = df.copy()
    close = out["Close"]
    out["ind_sma20"] = close.rolling(20).mean()
    out["ind_sma50"] = close.rolling(50).mean()
    out["ind_ema12"] = close.ewm(span=12).mean()
    out["ind_ret1"] = close.pct_change()
    out["ind_vol20"] = out["ind_ret1"].rolling(20).std()
    # RSI(14)
    delta = close.diff()
    up = delta.clip(lower=0).rolling(14).mean()
    down = (-delta.clip(upper=0)).rolling(14).mean()
    rs = up / down.replace(0, float("nan"))
    out["ind_rsi14"] = 100 - 100 / (1 + rs)
    return out
