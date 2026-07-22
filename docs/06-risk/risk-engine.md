# Risk Engine

The Risk Engine is the deterministic authority that validates every proposed decision before it can execute.

## Responsibilities

- **Validate proposed trades** against all applicable rules.
- **Enforce policies** (see [policy-framework.md](policy-framework.md)).
- **Calculate exposure** at position and portfolio level (see [portfolio-risk.md](portfolio-risk.md)).
- **Check liquidity** and tradability.
- **Verify limits** — position, sector, leverage, loss.
- **Return a verdict:** `APPROVE`, `MODIFY`, or `REJECT`.

## Verdicts

| Verdict | Meaning | What happens next |
| --- | --- | --- |
| `APPROVE` | The decision satisfies all rules | Proceeds to the Execution Engine |
| `MODIFY` | Allowed only in an adjusted form (e.g. smaller size) | Returns to the planner to replan |
| `REJECT` | Violates one or more rules | Returns to the planner to replan |

See the full flow in [approval-flow.md](approval-flow.md).

## The hard rule

> The engine never uses probabilistic reasoning for policy enforcement.

Every check is deterministic and rule-based. The same decision under the same policies always yields the same verdict, and every verdict carries a structured explanation of which rules applied and why (see [risk-philosophy.md](risk-philosophy.md)).

## Inputs

The candidate decision, the current portfolio state, the active (versioned) policy set, execution constraints, compliance rules, and circuit-breaker state (see the other docs in this section).
