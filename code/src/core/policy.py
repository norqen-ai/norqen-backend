"""Investor policy: the machine-readable mandate that governs the whole system.

The policy JSON is the LAW. The planner reads it, the risk engine enforces it,
and the audit log records which clauses were binding on every decision.
Schema version is frozen before live logging starts (pre-registration).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

SCHEMA_VERSION = "1.1"   # 1.1: added sizing_method + target_vol (risk-based sizing)

REQUIRED_FIELDS = [
    "policy_name", "objective", "horizon",
    "max_position_pct", "max_daily_loss_pct", "max_open_positions",
    "stop_loss_pct", "take_profit_pct",
    "confidence_to_act", "tool_priorities", "evidence_budget",
]

SIZING_METHODS = ("vol_target", "kelly", "confidence")


@dataclass(frozen=True)
class Policy:
    policy_name: str
    objective: str
    horizon: str
    max_position_pct: float
    max_daily_loss_pct: float
    max_open_positions: int
    stop_loss_pct: float
    take_profit_pct: float
    confidence_to_act: float
    tool_priorities: tuple[str, ...]
    evidence_budget: int
    forbidden_evidence: tuple[str, ...] = field(default_factory=tuple)
    sizing_method: str = "vol_target"     # how positions are sized (see src/core/sizing.py)
    target_vol: float = 0.15              # annualised vol budget for vol_target/kelly sizing
    schema_version: str = SCHEMA_VERSION

    def validate(self) -> None:
        if not (0 < self.max_position_pct <= 100):
            raise ValueError("max_position_pct must be in (0, 100]")
        if not (0 < self.confidence_to_act <= 1):
            raise ValueError("confidence_to_act must be in (0, 1]")
        if self.evidence_budget < 1:
            raise ValueError("evidence_budget must be >= 1")
        if not self.tool_priorities:
            raise ValueError("tool_priorities must not be empty")
        if self.sizing_method not in SIZING_METHODS:
            raise ValueError(f"sizing_method must be one of {SIZING_METHODS}")
        if not (0 < self.target_vol <= 2):
            raise ValueError("target_vol must be in (0, 2]  (e.g. 0.15 = 15% annual)")
        overlap = set(self.tool_priorities) & set(self.forbidden_evidence)
        if overlap:
            raise ValueError(f"tools both prioritised and forbidden: {overlap}")

    def to_dict(self) -> dict:
        return {
            **{f: getattr(self, f) for f in REQUIRED_FIELDS},
            "forbidden_evidence": list(self.forbidden_evidence),
            "sizing_method": self.sizing_method,
            "target_vol": self.target_vol,
            "schema_version": self.schema_version,
        }


def load_policy(path: str | Path) -> Policy:
    raw = json.loads(Path(path).read_text())
    missing = [f for f in REQUIRED_FIELDS if f not in raw]
    if missing:
        raise ValueError(f"policy {path}: missing fields {missing}")
    policy = Policy(
        policy_name=raw["policy_name"],
        objective=raw["objective"],
        horizon=raw["horizon"],
        max_position_pct=float(raw["max_position_pct"]),
        max_daily_loss_pct=float(raw["max_daily_loss_pct"]),
        max_open_positions=int(raw["max_open_positions"]),
        stop_loss_pct=float(raw["stop_loss_pct"]),
        take_profit_pct=float(raw["take_profit_pct"]),
        confidence_to_act=float(raw["confidence_to_act"]),
        tool_priorities=tuple(raw["tool_priorities"]),
        evidence_budget=int(raw["evidence_budget"]),
        forbidden_evidence=tuple(raw.get("forbidden_evidence", [])),
        sizing_method=raw.get("sizing_method", "vol_target"),
        target_vol=float(raw.get("target_vol", 0.15)),
    )
    policy.validate()
    return policy


def load_all_policies(policies_dir: str | Path) -> dict[str, Policy]:
    out: dict[str, Policy] = {}
    for p in sorted(Path(policies_dir).glob("*.json")):
        pol = load_policy(p)
        out[pol.policy_name] = pol
    return out
