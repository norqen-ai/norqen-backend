"""Point-in-time versions of the five specialist agents in src/tools/registry.py.

Same system prompts, same fact strings, same deterministic fallbacks, same reliability
weights and cost units — only the data source differs: every input is sliced AS OF the
decision date t (src/pit/data.py). The LLM judges run on one fixed "evidence model"
(gpt-4o-mini, T=0) so that the evidence is captured once and replayed identically to
every decision model ("capture once, replay many").
"""
from __future__ import annotations

import pandas as pd

from src.agents.llm import Judgement
from src.core.schemas import EvidenceItem
from src.pit import data
from src.pit.llm_client import structured
from src.pit.universe import INDEX, region

EVIDENCE_MODEL = "gpt-4o-mini"


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def _judge(system: str, human: str):
    r = structured(EVIDENCE_MODEL, system, human, Judgement, temperature=0.0, tag="evidence")
    if not r:
        return None
    return Judgement(direction=_clamp(float(r["direction"]), -1, 1),
                     confidence=_clamp(float(r["confidence"]), 0, 1), summary=str(r["summary"])[:240])


def _neutral(tool, kind, ticker, why, ts) -> EvidenceItem:
    return EvidenceItem(tool=tool, kind=kind, ticker=ticker, summary=f"insufficient data: {why}",
                        direction=0.0, confidence=0.1, reliability=0.3, cost_units=1.0, ts=ts)


def technical(ticker: str, t) -> EvidenceItem:
    ts = pd.Timestamp(t).timestamp()
    try:
        df = data.asof_indicators(ticker, t)
        row = df.dropna().iloc[-1]
        ret5 = float(df["Close"].iloc[-1] / df["Close"].iloc[-6] - 1) if len(df) > 6 else 0.0
    except Exception as e:
        return _neutral("technical", "technical", ticker, repr(e)[:60], ts)
    close, sma20, sma50, rsi = float(row["Close"]), float(row["ind_sma20"]), float(row["ind_sma50"]), float(row["ind_rsi14"])
    trend = _clamp((sma20 - sma50) / sma50 * 12, -1, 1)
    momentum = _clamp((rsi - 50) / 50, -1, 1)
    d_dir = _clamp(0.6 * trend + 0.4 * momentum, -1, 1)
    facts = (f"{ticker}: close={close:.2f}, SMA20={sma20:.2f}, SMA50={sma50:.2f} "
             f"({'above' if sma20 > sma50 else 'below'}), RSI14={rsi:.0f}, 5-day return={ret5:+.1%}.")
    j = _judge("You are a technical analyst. From the indicators, judge next 1-5 day direction. "
               "RSI>70 overbought, <30 oversold; SMA20>SMA50 is an uptrend. Be calibrated, not bold.", facts)
    return EvidenceItem(tool="technical", kind="technical", ticker=ticker,
                        summary=j.summary if j else f"SMA20 {'>' if sma20 > sma50 else '<'} SMA50, RSI {rsi:.0f}, 5d {ret5:+.1%}",
                        direction=j.direction if j else d_dir,
                        confidence=j.confidence if j else _clamp(0.40 + 0.45 * abs(d_dir), 0, 0.9),
                        reliability=0.75, cost_units=2.0 if j else 1.0, ts=ts)


def price_predictor(ticker: str, t) -> EvidenceItem:
    ts = pd.Timestamp(t).timestamp()
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from src.data.market import add_indicators
        df = add_indicators(data.asof(ticker, t).iloc[-504:]).dropna()     # ~2y, as in the live tool
        feats = ["ind_sma20", "ind_sma50", "ind_ema12", "ind_ret1", "ind_vol20", "ind_rsi14"]
        X = df[feats].iloc[:-1].values
        y = (df["Close"].shift(-1) > df["Close"]).astype(int).iloc[:-1].values
        if len(X) < 120:
            return _neutral("price_predictor", "technical", ticker, "history < 120 days", ts)
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        model.fit(X[:-1], y[:-1])
        p_up = float(model.predict_proba(df[feats].iloc[[-1]].values)[0, 1])
    except Exception as e:
        return _neutral("price_predictor", "technical", ticker, repr(e)[:60], ts)
    direction = 2 * p_up - 1
    return EvidenceItem(tool="price_predictor", kind="technical", ticker=ticker,
                        summary=f"P(up next day)={p_up:.2f} (logistic regression, walk-forward-safe)",
                        direction=direction, confidence=abs(direction), reliability=0.65, cost_units=1.0, ts=ts)


_POS = {"beat", "surge", "record", "growth", "upgrade", "profit", "gain", "wins", "strong", "raise", "rally"}
_NEG = {"miss", "fall", "cut", "downgrade", "loss", "probe", "fraud", "slump", "weak", "lawsuit", "ban", "plunge"}


def news(ticker: str, t, name: str | None = None) -> EvidenceItem:
    ts = pd.Timestamp(t).timestamp()
    heads = data.news_asof(ticker, t, name)
    if not heads:
        return _neutral("news", "news", ticker, "no headlines", ts)
    titles = [h["title"] for h in heads]
    joined = "\n".join(f"- {x}" for x in titles[:8])
    j = _judge("You are a financial news analyst. From these headlines judge near-term direction "
               "for the stock. Cite the single most market-moving headline.",
               f"{ticker} recent headlines:\n{joined}")
    if j:
        return EvidenceItem(tool="news", kind="news", ticker=ticker, summary=j.summary,
                            direction=j.direction, confidence=j.confidence, reliability=0.6, cost_units=2.0, ts=ts)
    score = sum(sum(w in x.lower() for w in _POS) - sum(w in x.lower() for w in _NEG) for x in titles)
    direction = _clamp(score / max(3, len(titles)), -1, 1)
    return EvidenceItem(tool="news", kind="news", ticker=ticker,
                        summary=f"{len(titles)} headlines; lexicon score {score:+d} (top: {titles[0][:70]})",
                        direction=direction, confidence=_clamp(0.3 + 0.3 * abs(direction), 0, 0.6),
                        reliability=0.5, cost_units=1.0, ts=ts)


def fundamental(ticker: str, t) -> EvidenceItem:
    ts = pd.Timestamp(t).timestamp()
    f = data.fundamentals_asof(ticker, t)
    if not f:
        return _neutral("fundamental", "fundamental", ticker, "no filed annual statements", ts)
    pe, pm, rg, roe = f.get("trailingPE"), f.get("profitMargins"), f.get("revenueGrowth"), f.get("returnOnEquity")
    score = 0.0
    if pm is not None:
        score += 0.4 if pm > 0.10 else (-0.4 if pm < 0 else 0.1)
    if rg is not None:
        score += 0.4 if rg > 0.08 else (-0.3 if rg < 0 else 0.1)
    if roe is not None and roe > 0.15:
        score += 0.2
    facts = f"{ticker} fundamentals: trailing P/E={pe}, profit margin={pm}, revenue growth={rg}, ROE={roe}."
    j = _judge("You are a fundamental analyst. Judge medium-term direction from these figures. "
               "Reward durable margins and growth; penalise losses and extreme valuations.", facts)
    if j:
        return EvidenceItem(tool="fundamental", kind="fundamental", ticker=ticker, summary=j.summary,
                            direction=j.direction, confidence=j.confidence, reliability=0.78, cost_units=2.0, ts=ts)
    direction = _clamp(score, -1, 1)
    return EvidenceItem(tool="fundamental", kind="fundamental", ticker=ticker,
                        summary=f"P/E={pe}, margin={pm}, rev growth={rg}",
                        direction=direction, confidence=_clamp(0.4 + 0.4 * abs(direction), 0, 0.85),
                        reliability=0.75, cost_units=1.0, ts=ts)


_MACRO: dict = {}


def macro(ticker: str, t) -> EvidenceItem:
    """Market-level judgement; identical facts for every stock in a region on a date, so the
    judgement is computed once per (region, date) and re-labelled per ticker."""
    ts = pd.Timestamp(t).timestamp()
    reg = region(ticker)
    key = (reg, str(pd.Timestamp(t).date()))
    if key not in _MACRO:
        idx = INDEX[reg]
        try:
            row = data.asof_indicators(idx, t).dropna().iloc[-1]
            sma20, sma50 = float(row["ind_sma20"]), float(row["ind_sma50"])
        except Exception as e:
            return _neutral("macro", "macro", ticker, repr(e)[:60], ts)
        trend = _clamp((sma20 - sma50) / sma50 * 12, -1, 1) * 0.7
        facts = f"Market index {idx}: SMA20={sma20:.1f} vs SMA50={sma50:.1f} ({'up' if sma20 > sma50 else 'down'}-trend)."
        j = _judge("You are a macro strategist. From the broad market index trend, judge the market-level "
                   "tailwind/headwind for an individual stock. Keep confidence modest.", facts)
        if j:
            _MACRO[key] = dict(summary=j.summary, direction=j.direction, confidence=j.confidence,
                               reliability=0.6, cost_units=2.0)
        else:
            _MACRO[key] = dict(summary=f"{idx} {'up' if sma20 > sma50 else 'down'}-trend (SMA20 vs SMA50)",
                               direction=trend, confidence=_clamp(0.35 + 0.3 * abs(trend), 0, 0.6),
                               reliability=0.55, cost_units=1.0)
    return EvidenceItem(tool="macro", kind="macro", ticker=ticker, ts=ts, **_MACRO[key])


def gather(ticker: str, t, name: str | None = None) -> list[EvidenceItem]:
    """All five tools, in registry order (technical, price_predictor, news, fundamental, macro)."""
    return [technical(ticker, t), price_predictor(ticker, t), news(ticker, t, name),
            fundamental(ticker, t), macro(ticker, t)]
