"""Risk-based position sizing — the quant core of every decision.

Replaces the toy `max_position_pct * confidence` with the sizing math real desks use.
Sizing is driven by the POLICY, so different mandates take different RISK from identical
conviction — this is where steerability becomes quantitative.

`policy.target_vol` is the PER-POSITION annualised volatility budget (e.g. 0.02 = a
position whose own vol contributes ~2%/yr at full conviction). A low-vol name therefore
gets a bigger weight than a high-vol name for the same conviction — inverse-vol / risk
parity at the single-name level. The per-name `max_position_pct` still hard-caps it.

Methods (policy.sizing_method):
  * "vol_target" (default) — w = (target_vol / realised_vol) * conviction
  * "kelly"      — w = 0.5 * (target_vol / realised_vol) * conviction   (half-Kelly, robust)
  * "confidence" — w = conviction                                        (legacy ablation baseline)

conviction = |direction| * confidence  ∈ [0,1].
Every result is a POSITIVE magnitude in percent, HARD-CAPPED by policy.max_position_pct
(the risk engine also enforces this cap — defence in depth). The planner sets BUY/SELL
from the sign of `direction`; this function returns magnitude only.
"""
from __future__ import annotations

from src.eval.quant import ann_vol, daily_returns


def realized_ann_vol(closes) -> float:
    """Annualised volatility from a close-price array (>=2 points)."""
    r = daily_returns(closes)
    return ann_vol(r) if len(r) > 1 else float("nan")


def position_size_pct(policy, direction: float, confidence: float,
                      realized_vol: float | None, method: str | None = None) -> float:
    """Signed-magnitude position size in percent of equity, capped by the policy."""
    method = method or getattr(policy, "sizing_method", "vol_target")
    conviction = abs(direction) * max(0.0, min(1.0, confidence))
    target_vol = getattr(policy, "target_vol", 0.15)

    if method in ("vol_target", "kelly") and realized_vol and realized_vol > 0:
        risk_weight = target_vol / realized_vol            # full risk-appropriate weight
        w = risk_weight * conviction
        if method == "kelly":
            w *= 0.5                                        # half-Kelly for robustness
    else:
        w = conviction                                     # legacy / vol unavailable

    pct = max(0.0, w * 100.0)
    return round(min(pct, policy.max_position_pct), 2)     # hard cap
