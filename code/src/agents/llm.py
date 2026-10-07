"""LLM layer — OpenAI via LangChain, with a hard rule and a soft fallback.

HARD RULE: the LLM only ever produces a *judgement* (direction, confidence,
one-line summary). It never computes position sizes, stops, or indicator values —
those come from policy + Malhar's numeric tools. This keeps RQ2 (is the confidence
honest?) meaningful and keeps numbers auditable.

SOFT FALLBACK: if OPENAI_API_KEY is not set (or a call fails), `judge()` returns
None and the caller uses its deterministic signal. So the whole pipeline runs on
real market data with zero API access — the key just makes the agents smarter.

The key is read from the environment / .env and is NEVER printed or logged.
"""
from __future__ import annotations

import os
from functools import lru_cache

try:
    from dotenv import load_dotenv
    load_dotenv()  # loads .env from the current working directory if present
except Exception:
    pass

from pydantic import BaseModel, Field

DEFAULT_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")


class Judgement(BaseModel):
    """The only shape an LLM agent is allowed to return."""
    direction: float = Field(description="-1.0 (clearly bearish) to +1.0 (clearly bullish)")
    confidence: float = Field(description="0.0 to 1.0 — HONEST probability the direction is correct")
    summary: str = Field(description="one sentence citing the single most important fact")


def llm_available() -> bool:
    """True only if an API key is configured. Callers branch on this."""
    return bool(os.environ.get("OPENAI_API_KEY"))


@lru_cache(maxsize=2)
def _chat(model: str, temperature: float):
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model, temperature=temperature, timeout=30, max_retries=1)


class DecisionProposal(BaseModel):
    """An UNGUARDED decision proposed by the LLM (used only in obedience experiments).
    Values are logged raw — never clamped — so policy violations are observable."""
    action: str = Field(description="exactly one of BUY, SELL, HOLD, WAIT")
    position_size_pct: float = Field(description="percent of TOTAL portfolio to allocate; 0 for WAIT/HOLD")
    stop_loss_pct: float = Field(description="stop-loss distance in percent from entry; 0 for WAIT/HOLD")
    take_profit_pct: float = Field(description="take-profit target in percent from entry; 0 for WAIT/HOLD")
    confidence: float = Field(description="0.0 to 1.0 probability that the chosen direction is correct")
    rationale: str = Field(description="one or two sentences")


def propose_decision(system: str, human: str, model: str | None = None,
                     temperature: float = 0.0) -> DecisionProposal | None:
    """Ask the LLM to make the full decision itself. Only the action label is normalised
    and confidence kept in [0,1]; size/stop/take-profit are returned exactly as proposed."""
    if not llm_available():
        return None
    try:
        chat = _chat(model or DEFAULT_MODEL, temperature).with_structured_output(DecisionProposal)
        r = chat.invoke([("system", system), ("human", human)])
        action = str(r.action).upper().strip()
        if action not in ("BUY", "SELL", "HOLD", "WAIT"):
            action = "WAIT"
        return DecisionProposal(
            action=action, position_size_pct=float(r.position_size_pct),
            stop_loss_pct=float(r.stop_loss_pct), take_profit_pct=float(r.take_profit_pct),
            confidence=max(0.0, min(1.0, float(r.confidence))), rationale=str(r.rationale)[:400])
    except Exception:
        return None


def judge(system: str, human: str, model: str | None = None, temperature: float = 0.0) -> Judgement | None:
    """Ask the LLM for a structured judgement. Returns None if unavailable/failed
    so the caller falls back to its deterministic signal. Numbers are clamped."""
    if not llm_available():
        return None
    try:
        chat = _chat(model or DEFAULT_MODEL, temperature).with_structured_output(Judgement)
        r = chat.invoke([("system", system), ("human", human)])
        d = max(-1.0, min(1.0, float(r.direction)))
        c = max(0.0, min(1.0, float(r.confidence)))
        return Judgement(direction=d, confidence=c, summary=str(r.summary)[:240])
    except Exception:
        return None
