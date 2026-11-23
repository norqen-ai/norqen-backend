"""Policy-conditioned planner — v0 rule-based skeleton.

OMKAR: this is your file. The v0 planner is deliberately LLM-free so the whole
pipeline runs end-to-end today. Your job is to replace the internals with a
LangGraph graph + LLM agents while KEEPING the same interface:

    planner = Planner(policy, tools)
    card = planner.decide(ticker)

Interface rules (do not break):
  - tools: dict[tool_name -> callable(ticker) -> EvidenceItem]
  - the planner may only call tools listed in policy.tool_priorities,
    never ones in policy.forbidden_evidence
  - stop gathering when running confidence >= policy.confidence_to_act
    OR cost spent >= policy.evidence_budget  (the adaptive evidence loop)
  - every EvidenceItem used goes into card.evidence (audit requirement)
  - the LLM never invents numbers: sizes/stops come from policy + code
"""
from __future__ import annotations

from src.core.policy import Policy
from src.core.schemas import DecisionCard, EvidenceItem


class Planner:
    def __init__(self, policy: Policy, tools: dict):
        self.policy = policy
        self.tools = tools

    # ---- evidence aggregation (v0: reliability-weighted average) ----
    @staticmethod
    def _aggregate(evidence: list[EvidenceItem]) -> tuple[float, float]:
        """Return (direction in [-1,1], confidence in [0,1])."""
        if not evidence:
            return 0.0, 0.0
        wsum = sum(e.reliability * e.confidence for e in evidence)
        if wsum == 0:
            return 0.0, 0.0
        direction = sum(e.direction * e.reliability * e.confidence for e in evidence) / wsum
        confidence = wsum / sum(e.reliability for e in evidence)
        # agreement bonus/penalty: unanimous evidence is more convincing
        signs = {1 if e.direction > 0 else -1 if e.direction < 0 else 0 for e in evidence}
        if len(signs - {0}) > 1:
            confidence *= 0.8  # conflicting evidence -> less confident
        return direction, confidence

    def decide(self, ticker: str) -> DecisionCard:
        p = self.policy
        evidence: list[EvidenceItem] = []
        clauses = ["tool_priorities", "evidence_budget", "confidence_to_act"]
        spent = 0.0

        # adaptive evidence loop: walk tools in policy priority order, stop early
        for tool_name in p.tool_priorities:
            if tool_name in p.forbidden_evidence or tool_name not in self.tools:
                continue
            if spent >= p.evidence_budget:
                clauses.append("evidence_budget:exhausted")
                break
            item = self.tools[tool_name](ticker)
            evidence.append(item)
            spent += item.cost_units
            _, conf = self._aggregate(evidence)
            if conf >= p.confidence_to_act and len(evidence) >= 2:
                clauses.append("confidence_to_act:early_stop")
                break

        direction, confidence = self._aggregate(evidence)

        # synthesise action (v0 heuristic; LLM synthesis replaces this)
        if confidence < p.confidence_to_act or abs(direction) < 0.15:
            action, size = ("WAIT", 0.0)
        elif direction > 0:
            action, size = ("BUY", round(p.max_position_pct * min(1.0, confidence), 2))
        else:
            action, size = ("SELL", round(p.max_position_pct * min(1.0, confidence), 2))
        clauses.append("max_position_pct")

        reasoning = (
            f"[{p.policy_name}] {len(evidence)} evidence items "
            f"(cost {spent:.1f}/{p.evidence_budget}), direction {direction:+.2f}, "
            f"confidence {confidence:.2f} vs threshold {p.confidence_to_act:.2f} -> {action}"
        )
        return DecisionCard(
            ticker=ticker,
            action=action,
            position_size_pct=size,
            stop_loss_pct=p.stop_loss_pct if action in ("BUY", "SELL") else 0.0,
            take_profit_pct=p.take_profit_pct if action in ("BUY", "SELL") else 0.0,
            confidence=round(confidence, 4),
            policy_name=p.policy_name,
            reasoning=reasoning,
            evidence=[e.to_dict() for e in evidence],
            policy_clauses_applied=clauses,
            evidence_cost_spent=spent,
        )
