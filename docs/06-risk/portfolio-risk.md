# Portfolio Risk

Evaluates risk at the **portfolio level** — the aggregate effect of a decision, not just the single position.

## Evaluated dimensions

- Concentration
- Correlation
- Sector exposure
- Geographic exposure
- Cash allocation
- VaR (optional)
- Drawdown

## When it runs

> Portfolio health is checked before every execution.

Even a decision that is fine in isolation can be unsafe in aggregate (e.g. it pushes sector exposure over a limit or raises correlation-driven risk). The Risk Engine runs these checks as part of validation and can return MODIFY or REJECT accordingly (see [risk-engine.md](risk-engine.md)).

## Relationship to other checks

- Complements **position sizing** (single-position downside — see [position-sizing.md](position-sizing.md)).
- Enforces portfolio-level **policies** (max exposure, sector limits — see [policy-framework.md](policy-framework.md)).
- Distinct from the **Portfolio Agent**, which only *advises* the planner; the hard limits are enforced here, deterministically (see [../03-agents/portfolio-agent.md](../03-agents/portfolio-agent.md)).
- Drawdown breaches can trip circuit breakers (see [circuit-breakers.md](circuit-breakers.md)).
