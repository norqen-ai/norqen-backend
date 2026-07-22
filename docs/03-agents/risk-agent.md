# Risk Agent

Gathers **contextual risk evidence** for the planner. It is an advisor, not the authority.

## What it does

- Highlights unusual conditions before a decision is formalized.
- Flags volatility spikes, liquidity concerns, and abnormal market behavior.
- Provides early risk context so the planner can adjust its reasoning.

## The critical distinction

> The Risk Agent gathers evidence. The **deterministic Risk Engine decides.**

| Risk Agent (this doc) | Risk Engine ([../06-risk/risk-engine.md](../06-risk/risk-engine.md)) |
| --- | --- |
| A specialist consulted by the planner | The final, mandatory authority |
| Probabilistic, advisory | Deterministic, policy-driven |
| Produces evidence | Produces APPROVE / MODIFY / REJECT |
| Can be skipped by the planner | Can never be bypassed |

Final approval **always** belongs to the deterministic Risk Engine, regardless of what the Risk Agent reports.

## Output

Structured contextual risk evidence: flagged conditions with severity, source, and timestamp.

## Boundary

Returns to the planner; never executes, enforces policy, or contacts other agents (see [agent-framework.md](agent-framework.md)).
