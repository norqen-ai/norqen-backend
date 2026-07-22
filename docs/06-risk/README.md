# 06 - Risk

Defines the **deterministic risk management framework** that validates every decision before execution. Risk is the final authority in Norqen — nothing reaches a broker without passing through it.

## Reading order

1. [risk-philosophy.md](risk-philosophy.md) — the planner proposes, the Risk Engine decides
2. [risk-engine.md](risk-engine.md) — the engine and its verdicts
3. [policy-framework.md](policy-framework.md) — the versioned rules it enforces
4. [position-sizing.md](position-sizing.md) — how quantities are derived
5. [portfolio-risk.md](portfolio-risk.md) — portfolio-level checks
6. [execution-constraints.md](execution-constraints.md) — pre-trade gating checks
7. [compliance.md](compliance.md) — regulatory and user restrictions
8. [circuit-breakers.md](circuit-breakers.md) — automatic halts
9. [approval-flow.md](approval-flow.md) — the APPROVE / MODIFY / REJECT flow
10. [monitoring.md](monitoring.md) — risk metrics and alerts
11. [incident-response.md](incident-response.md) — handling critical failures

## The non-negotiable

Risk is **deterministic, explainable, and policy-driven**. It never uses probabilistic reasoning to enforce policy, and it can never be bypassed (see [risk-philosophy.md](risk-philosophy.md), [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md)).
