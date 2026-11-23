"""Symbol resolver — 'Apple'->AAPL, 'Reliance'->RELIANCE.NS, 'infy'->INFY.NS.

Lets a user type a company name or loose ticker instead of the exact symbol, so the
product works for ANY listed stock. Uses Yahoo's public search endpoint; falls back
to the uppercased input if search is unavailable. No API key.
"""
from __future__ import annotations


def resolve_ticker(query: str, prefer_nse: bool = True) -> dict:
    """Resolve a name/loose ticker to a symbol. This product is India-first, so when
    the query already carries a US hint we respect it, otherwise an NSE (.NS) match is
    preferred over a foreign dual-listing (e.g. 'Reliance' -> RELIANCE.NS, not EZRA).
    Full `candidates` are always returned so the UI can let the user disambiguate."""
    q = (query or "").strip()
    if not q:
        return {"ticker": None, "name": None, "exchange": None, "candidates": []}
    try:
        import requests
        r = requests.get(
            "https://query2.finance.yahoo.com/v1/finance/search",
            params={"q": q, "quotesCount": 6, "newsCount": 0},
            headers={"User-Agent": "Mozilla/5.0"}, timeout=8,
        )
        quotes = [x for x in r.json().get("quotes", [])
                  if x.get("quoteType") == "EQUITY" and x.get("symbol")]
        if quotes:
            top = quotes[0]
            if prefer_nse and not q.upper().endswith((".US", "-US")):
                nse = next((x for x in quotes if x["symbol"].upper().endswith(".NS")), None)
                if nse:
                    top = nse
            return {
                "ticker": top["symbol"],
                "name": top.get("shortname") or top.get("longname"),
                "exchange": top.get("exchange"),
                "candidates": [x["symbol"] for x in quotes[:6]],
            }
    except Exception:
        pass
    return {"ticker": q.upper(), "name": None, "exchange": None, "candidates": [q.upper()]}
