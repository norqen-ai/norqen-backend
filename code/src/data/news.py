"""Real news headlines for a ticker — free sources only, no API key.

Sources (best-effort, deduped, newest-first):
  1. yfinance Ticker.news  (Yahoo Finance)
  2. Google News RSS via feedparser

Returns list[{"ts": float|None, "title": str, "source": str}]. The News Agent
(LLM) reads these; this module does NOT score sentiment — that is the agent's job.
"""
from __future__ import annotations

import time
import urllib.parse


def _company_query(ticker: str) -> str:
    root = ticker.split(".")[0]
    suffix = " share price NSE" if ticker.upper().endswith(".NS") else " stock"
    return f"{root}{suffix}"


def _from_yfinance(ticker: str) -> list[dict]:
    out: list[dict] = []
    try:
        import yfinance as yf
        for n in (yf.Ticker(ticker).news or []):
            c = n.get("content") or n          # yfinance schema changed; handle both
            title = c.get("title") or n.get("title")
            if not title:
                continue
            prov = (c.get("provider") or {}).get("displayName") if isinstance(c.get("provider"), dict) else n.get("publisher")
            out.append({"ts": n.get("providerPublishTime"), "title": title.strip(), "source": prov or "Yahoo"})
    except Exception:
        pass
    return out


def _from_google_rss(ticker: str, limit: int) -> list[dict]:
    out: list[dict] = []
    try:
        import feedparser
        q = urllib.parse.quote(_company_query(ticker))
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en")
        for e in feed.entries[:limit]:
            ts = time.mktime(e.published_parsed) if getattr(e, "published_parsed", None) else None
            src = e.get("source", {}).get("title") if isinstance(e.get("source"), dict) else "GoogleNews"
            out.append({"ts": ts, "title": e.title.strip(), "source": src or "GoogleNews"})
    except Exception:
        pass
    return out


def fetch_headlines(ticker: str, limit: int = 8) -> list[dict]:
    items = _from_yfinance(ticker) + _from_google_rss(ticker, limit)
    seen, deduped = set(), []
    for it in items:
        key = it["title"].lower()[:80]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    deduped.sort(key=lambda x: x["ts"] or 0, reverse=True)
    return deduped[:limit]
