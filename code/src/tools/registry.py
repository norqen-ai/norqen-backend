"""The specialist tools/agents, backed by REAL market data via the provider layer.

Each entry in the registry is `callable(ticker) -> EvidenceItem`, keyed by the
exact names the policies use in `tool_priorities`:
    technical · price_predictor · news · fundamental · macro

Tools NEVER import yfinance directly — they call `MARKET.get_*()` so the data
source is swappable (Yahoo / Finnhub / ...). Pattern for every tool:
  1. Pull real data via MARKET.
  2. Compute a transparent DETERMINISTIC signal (always runs, no key needed).
  3. If an OpenAI key is set, ask the LLM agent to judge instead, given the real
     facts; on any failure keep the deterministic signal.
The LLM never invents numbers used for sizing — it only judges direction/confidence.
"""
from __future__ import annotations

from src.core.schemas import EvidenceItem
from src.agents.llm import judge, llm_available
from src.data.providers import MARKET


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def _neutral(tool, kind, ticker, why) -> EvidenceItem:
    return EvidenceItem(tool=tool, kind=kind, ticker=ticker,
                        summary=f"insufficient data: {why}", direction=0.0,
                        confidence=0.1, reliability=0.3, cost_units=1.0)


# --------------------------------------------------------------------------- #
def technical(ticker: str) -> EvidenceItem:
    try:
        df = MARKET.get_indicators(ticker, period="6mo")
        row = df.dropna().iloc[-1]
        ret5 = float(df["Close"].iloc[-1] / df["Close"].iloc[-6] - 1) if len(df) > 6 else 0.0
    except Exception as e:
        return _neutral("technical", "technical", ticker, repr(e)[:60])

    close, sma20, sma50, rsi = float(row["Close"]), float(row["ind_sma20"]), float(row["ind_sma50"]), float(row["ind_rsi14"])
    trend = _clamp((sma20 - sma50) / sma50 * 12, -1, 1)
    momentum = _clamp((rsi - 50) / 50, -1, 1)
    d_dir = _clamp(0.6 * trend + 0.4 * momentum, -1, 1)
    facts = (f"{ticker}: close={close:.2f}, SMA20={sma20:.2f}, SMA50={sma50:.2f} "
             f"({'above' if sma20 > sma50 else 'below'}), RSI14={rsi:.0f}, 5-day return={ret5:+.1%}.")
    j = judge("You are a technical analyst. From the indicators, judge next 1-5 day direction. "
              "RSI>70 overbought, <30 oversold; SMA20>SMA50 is an uptrend. Be calibrated, not bold.",
              facts) if llm_available() else None
    return EvidenceItem(tool="technical", kind="technical", ticker=ticker,
                        summary=j.summary if j else f"SMA20 {'>' if sma20 > sma50 else '<'} SMA50, RSI {rsi:.0f}, 5d {ret5:+.1%}",
                        direction=j.direction if j else d_dir,
                        confidence=j.confidence if j else _clamp(0.40 + 0.45 * abs(d_dir), 0, 0.9),
                        reliability=0.75, cost_units=2.0 if j else 1.0)


# --------------------------------------------------------------------------- #
def price_predictor(ticker: str) -> EvidenceItem:
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
        df = MARKET.get_indicators(ticker, period="2y").dropna()
        feats = ["ind_sma20", "ind_sma50", "ind_ema12", "ind_ret1", "ind_vol20", "ind_rsi14"]
        X = df[feats].iloc[:-1].values
        y = (df["Close"].shift(-1) > df["Close"]).astype(int).iloc[:-1].values
        if len(X) < 120:
            return _neutral("price_predictor", "technical", ticker, "history < 120 days")
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        model.fit(X[:-1], y[:-1])                          # never fit on the row we predict
        p_up = float(model.predict_proba(df[feats].iloc[[-1]].values)[0, 1])
    except Exception as e:
        return _neutral("price_predictor", "technical", ticker, repr(e)[:60])
    direction = 2 * p_up - 1
    return EvidenceItem(tool="price_predictor", kind="technical", ticker=ticker,
                        summary=f"P(up next day)={p_up:.2f} (logistic regression, walk-forward-safe)",
                        direction=direction, confidence=abs(direction),  # HONEST; RQ2 calibrates this
                        reliability=0.65, cost_units=1.0)


# --------------------------------------------------------------------------- #
_POS = {"beat", "surge", "record", "growth", "upgrade", "profit", "gain", "wins", "strong", "raise", "rally"}
_NEG = {"miss", "fall", "cut", "downgrade", "loss", "probe", "fraud", "slump", "weak", "lawsuit", "ban", "plunge"}


def news(ticker: str) -> EvidenceItem:
    heads = MARKET.get_news(ticker, limit=8)
    if not heads:
        return _neutral("news", "news", ticker, "no headlines")
    titles = [h["title"] for h in heads]
    if llm_available():
        joined = "\n".join(f"- {t}" for t in titles[:8])
        j = judge("You are a financial news analyst. From these headlines judge near-term direction "
                  "for the stock. Cite the single most market-moving headline.",
                  f"{ticker} recent headlines:\n{joined}")
        if j:
            return EvidenceItem(tool="news", kind="news", ticker=ticker, summary=j.summary,
                                direction=j.direction, confidence=j.confidence, reliability=0.6, cost_units=2.0)
    score = 0
    for t in titles:
        low = t.lower()
        score += sum(w in low for w in _POS) - sum(w in low for w in _NEG)
    direction = _clamp(score / max(3, len(titles)), -1, 1)
    return EvidenceItem(tool="news", kind="news", ticker=ticker,
                        summary=f"{len(titles)} headlines; lexicon score {score:+d} (top: {titles[0][:70]})",
                        direction=direction, confidence=_clamp(0.3 + 0.3 * abs(direction), 0, 0.6),
                        reliability=0.5, cost_units=1.0)


# --------------------------------------------------------------------------- #
def fundamental(ticker: str) -> EvidenceItem:
    try:
        f = MARKET.get_fundamentals(ticker)
    except Exception as e:
        return _neutral("fundamental", "fundamental", ticker, repr(e)[:60])
    pe, pm, rg, roe = f.get("trailingPE"), f.get("profitMargins"), f.get("revenueGrowth"), f.get("returnOnEquity")
    score = 0.0
    if pm is not None:
        score += 0.4 if pm > 0.10 else (-0.4 if pm < 0 else 0.1)
    if rg is not None:
        score += 0.4 if rg > 0.08 else (-0.3 if rg < 0 else 0.1)
    if roe is not None and roe > 0.15:
        score += 0.2
    facts = f"{ticker} fundamentals: trailing P/E={pe}, profit margin={pm}, revenue growth={rg}, ROE={roe}."
    if llm_available():
        j = judge("You are a fundamental analyst. Judge medium-term direction from these figures. "
                  "Reward durable margins and growth; penalise losses and extreme valuations.", facts)
        if j:
            return EvidenceItem(tool="fundamental", kind="fundamental", ticker=ticker, summary=j.summary,
                                direction=j.direction, confidence=j.confidence, reliability=0.78, cost_units=2.0)
    direction = _clamp(score, -1, 1)
    return EvidenceItem(tool="fundamental", kind="fundamental", ticker=ticker,
                        summary=f"P/E={pe}, margin={pm}, rev growth={rg}",
                        direction=direction, confidence=_clamp(0.4 + 0.4 * abs(direction), 0, 0.85),
                        reliability=0.75, cost_units=1.0)


# --------------------------------------------------------------------------- #
def macro(ticker: str) -> EvidenceItem:
    region = "IN" if ticker.upper().endswith(".NS") else "US"
    try:
        m = MARKET.get_macro(region)
        sma20, sma50, index = m["sma20"], m["sma50"], m["index"]
    except Exception as e:
        return _neutral("macro", "macro", ticker, repr(e)[:60])
    trend = _clamp((sma20 - sma50) / sma50 * 12, -1, 1) * 0.7
    facts = f"Market index {index}: SMA20={sma20:.1f} vs SMA50={sma50:.1f} ({'up' if sma20 > sma50 else 'down'}-trend)."
    if llm_available():
        j = judge("You are a macro strategist. From the broad market index trend, judge the market-level "
                  "tailwind/headwind for an individual stock. Keep confidence modest.", facts)
        if j:
            return EvidenceItem(tool="macro", kind="macro", ticker=ticker, summary=j.summary,
                                direction=j.direction, confidence=j.confidence, reliability=0.6, cost_units=2.0)
    return EvidenceItem(tool="macro", kind="macro", ticker=ticker,
                        summary=f"{index} {'up' if sma20 > sma50 else 'down'}-trend (SMA20 vs SMA50)",
                        direction=trend, confidence=_clamp(0.35 + 0.3 * abs(trend), 0, 0.6),
                        reliability=0.55, cost_units=1.0)


def build_registry() -> dict:
    """Name -> tool. Names MUST match the policies' tool_priorities."""
    return {"technical": technical, "price_predictor": price_predictor,
            "news": news, "fundamental": fundamental, "macro": macro}
