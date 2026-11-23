"""Modular market-data provider layer.

The one architectural point GPT got right: agents/tools must NOT import yfinance
directly. They call `MARKET.get_*(ticker)`, so providers are swappable (Yahoo today;
Finnhub / Alpha Vantage / FRED tomorrow) without touching any agent code. This also
keeps the research reproducible — ONE place controls where data comes from.

Add a provider by subclassing YahooProvider and overriding the methods you improve.
Set FINNHUB_API_KEY in .env to route news+fundamentals through Finnhub automatically.
"""
from __future__ import annotations

import os

from src.data.market import fetch_ohlcv, add_indicators
from src.data import news as news_mod


class YahooProvider:
    """Default provider — free, no key, US + NSE (.NS). Unofficial but fine for
    daily/event-level research."""
    name = "yahoo"

    def get_ohlcv(self, ticker: str, period: str = "6mo"):
        return fetch_ohlcv(ticker, period=period)

    def get_indicators(self, ticker: str, period: str = "6mo"):
        return add_indicators(fetch_ohlcv(ticker, period=period))

    def get_fundamentals(self, ticker: str) -> dict:
        import yfinance as yf
        info = yf.Ticker(ticker).info or {}
        return {
            "trailingPE": info.get("trailingPE"),
            "profitMargins": info.get("profitMargins"),
            "revenueGrowth": info.get("revenueGrowth"),
            "returnOnEquity": info.get("returnOnEquity"),
            "longName": info.get("longName"),
            "sector": info.get("sector"),
        }

    def get_news(self, ticker: str, limit: int = 8) -> list[dict]:
        return news_mod.fetch_headlines(ticker, limit)

    def get_macro(self, region: str = "US") -> dict:
        idx = "^NSEI" if region == "IN" else "^GSPC"
        df = add_indicators(fetch_ohlcv(idx, period="6mo")).dropna()
        row = df.iloc[-1]
        return {"index": idx, "sma20": float(row["ind_sma20"]), "sma50": float(row["ind_sma50"])}


class FinnhubProvider(YahooProvider):
    """News + fundamentals via Finnhub when FINNHUB_API_KEY is set; everything
    else (OHLCV, macro) stays on Yahoo. Any Finnhub error falls back to Yahoo,
    so the pipeline never breaks. (Activates automatically; test with your key.)"""
    name = "finnhub"

    def _key(self):
        return os.environ.get("FINNHUB_API_KEY")

    def get_fundamentals(self, ticker: str) -> dict:
        try:
            import requests
            k = self._key()
            m = requests.get("https://finnhub.io/api/v1/stock/metric",
                             params={"symbol": ticker, "metric": "all", "token": k}, timeout=8).json().get("metric", {})
            if m:
                return {
                    "trailingPE": m.get("peBasicExclExtraTTM"),
                    "profitMargins": (m.get("netProfitMarginTTM") or 0) / 100 if m.get("netProfitMarginTTM") else None,
                    "revenueGrowth": (m.get("revenueGrowthTTMYoy") or 0) / 100 if m.get("revenueGrowthTTMYoy") else None,
                    "returnOnEquity": (m.get("roeTTM") or 0) / 100 if m.get("roeTTM") else None,
                    "longName": None, "sector": None,
                }
        except Exception:
            pass
        return super().get_fundamentals(ticker)

    def get_news(self, ticker: str, limit: int = 8) -> list[dict]:
        try:
            import requests, time
            k = self._key()
            today = time.strftime("%Y-%m-%d")
            weekago = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 7 * 86400))
            arr = requests.get("https://finnhub.io/api/v1/company-news",
                               params={"symbol": ticker.split(".")[0], "from": weekago, "to": today, "token": k},
                               timeout=8).json()
            out = [{"ts": n.get("datetime"), "title": n.get("headline"), "source": n.get("source")}
                   for n in arr[:limit] if n.get("headline")]
            if out:
                return out
        except Exception:
            pass
        return super().get_news(ticker, limit)


def get_market():
    """Pick the provider. Finnhub for news+fundamentals if a key is present, else Yahoo."""
    return FinnhubProvider() if os.environ.get("FINNHUB_API_KEY") else YahooProvider()


MARKET = get_market()
