"""Shared data contracts between the three tracks (ML, agents, full-stack).

These schemas ARE the team interface:
  - ML tools (Malhar) return EvidenceItem
  - the planner/agents (Omkar) consume EvidenceItem and produce DecisionCard
  - the risk engine stamps a RiskVerdict onto the card
  - the dashboard (Piyush) renders logged DecisionCards

Change them only by team agreement + a version bump.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict

SCHEMAS_VERSION = "1.0"

Action = str  # "BUY" | "SELL" | "HOLD" | "WAIT"


@dataclass
class EvidenceItem:
    """One piece of evidence produced by a tool or agent."""
    tool: str                      # e.g. "price_predictor", "news_agent"
    kind: str                      # e.g. "technical", "news", "fundamental", "macro"
    ticker: str
    summary: str                   # short human-readable finding
    direction: float               # -1.0 (bearish) .. +1.0 (bullish)
    confidence: float              # tool's own confidence in [0, 1]
    reliability: float = 0.8       # source reliability score in [0, 1]
    ts: float = field(default_factory=time.time)
    cost_units: float = 1.0        # tokens/calls consumed to obtain this

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DecisionCard:
    """The system's per-decision output — the product AND the research datum."""
    ticker: str
    action: Action
    position_size_pct: float
    stop_loss_pct: float
    take_profit_pct: float
    confidence: float                       # stated confidence in [0, 1]
    policy_name: str
    reasoning: str
    evidence: list[dict] = field(default_factory=list)   # EvidenceItem dicts
    policy_clauses_applied: list[str] = field(default_factory=list)
    evidence_cost_spent: float = 0.0
    risk_verdict: str = "PENDING"           # PENDING | APPROVED | VETOED
    risk_reasons: list[str] = field(default_factory=list)
    decision_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    ts: float = field(default_factory=time.time)
    schema_version: str = SCHEMAS_VERSION

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PortfolioState:
    """Minimal portfolio snapshot the risk engine needs."""
    equity: float                   # total account value
    cash: float
    open_positions: int
    daily_pnl_pct: float            # today's P&L as % of equity (negative = loss)
    position_pct_by_ticker: dict[str, float] = field(default_factory=dict)
