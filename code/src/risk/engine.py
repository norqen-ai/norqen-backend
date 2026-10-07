"""Deterministic rule-based risk engine. NO AI IN THIS FILE — ever.

Every rule is a plain, auditable check derived from the active policy and the
portfolio state. The engine has absolute veto power: a VETOED card must never
reach execution. The planner cannot negotiate with it.
"""
from __future__ import annotations

from src.core.policy import Policy
from src.core.schemas import DecisionCard, PortfolioState


class RiskEngine:
    def __init__(self, policy: Policy):
        self.policy = policy

    def check(self, card: DecisionCard, portfolio: PortfolioState) -> DecisionCard:
        """Stamp APPROVED or VETOED (with reasons) onto the card. Pure function of inputs."""
        reasons: list[str] = []
        p = self.policy

        if card.action in ("HOLD", "WAIT"):
            card.risk_verdict = "APPROVED"
            card.risk_reasons = ["no position change requested"]
            return card

        # 1. position size cap
        if card.position_size_pct > p.max_position_pct:
            reasons.append(
                f"position {card.position_size_pct:.2f}% exceeds policy cap {p.max_position_pct:.2f}%"
            )

        # 2. daily loss limit already breached -> no new risk today
        if portfolio.daily_pnl_pct <= -p.max_daily_loss_pct:
            reasons.append(
                f"daily loss {portfolio.daily_pnl_pct:.2f}% breaches limit -{p.max_daily_loss_pct:.2f}%"
            )

        # 3. max open positions
        if card.action == "BUY" and portfolio.open_positions >= p.max_open_positions:
            reasons.append(
                f"open positions {portfolio.open_positions} at policy max {p.max_open_positions}"
            )

        # 4. stop-loss must be present and no looser than policy
        if card.stop_loss_pct <= 0:
            reasons.append("missing stop-loss")
        elif card.stop_loss_pct > p.stop_loss_pct:
            reasons.append(
                f"stop-loss {card.stop_loss_pct:.2f}% looser than policy {p.stop_loss_pct:.2f}%"
            )

        # 5. confidence floor (defence in depth; planner should already enforce)
        if card.confidence < p.confidence_to_act:
            reasons.append(
                f"confidence {card.confidence:.2f} below policy threshold {p.confidence_to_act:.2f}"
            )

        # 6. forbidden evidence must not have influenced the decision
        used_kinds = {e.get("kind") for e in card.evidence} | {e.get("tool") for e in card.evidence}
        banned = used_kinds & set(p.forbidden_evidence)
        if banned:
            reasons.append(f"decision used forbidden evidence: {sorted(banned)}")

        card.risk_verdict = "VETOED" if reasons else "APPROVED"
        card.risk_reasons = reasons or ["all checks passed"]
        return card
