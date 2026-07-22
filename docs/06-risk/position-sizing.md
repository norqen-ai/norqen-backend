# Position Sizing

Determines *how much* to trade, deterministically, within the risk budget.

## Inputs

- Portfolio value
- Risk budget
- Volatility
- Stop-loss distance
- Liquidity

## Outputs

- Recommended quantity
- Capital allocation
- Estimated downside

## Where it fits

Position sizing is part of risk validation. When a decision would exceed limits at its proposed size, the Risk Engine can return `MODIFY` with a compliant size rather than rejecting outright (see [risk-engine.md](risk-engine.md), [approval-flow.md](approval-flow.md)).

## Notes

- Sizing is **deterministic** — the same inputs always yield the same quantity (see [risk-philosophy.md](risk-philosophy.md)).
- It respects per-position and portfolio limits (see [policy-framework.md](policy-framework.md), [portfolio-risk.md](portfolio-risk.md)).
- **Liquidity** bounds size so orders remain executable; illiquid instruments get smaller allocations.
- The **estimated downside** output feeds portfolio-level risk checks and monitoring (see [monitoring.md](monitoring.md)).
