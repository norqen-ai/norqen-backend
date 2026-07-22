# Approval Flow

How a candidate decision moves through risk validation to a verdict.

```
Planner Decision
      │
      ▼
Risk Validation
      │
      ├── Approve ──► Execution
      ├── Modify  ──► Planner Replan
      └── Reject  ──► Planner Replan
```

## The three outcomes

| Verdict | Meaning | Next step |
| --- | --- | --- |
| **Approve** | Satisfies all policies, constraints, and compliance | Proceed to the Execution Engine |
| **Modify** | Permissible only in an adjusted form (e.g. reduced size) | Return to the planner with the required adjustment |
| **Reject** | Violates one or more rules | Return to the planner to reason again |

## The guarantee

> Every outcome includes a structured explanation.

The explanation names the rules, limits, or constraints that produced the verdict — making every risk decision auditable and giving the planner concrete feedback to replan with (see [risk-engine.md](risk-engine.md)).

## Notes

- Both **Modify** and **Reject** feed back into the reasoning loop; the risk feedback becomes new evidence for the planner (see [../02-runtime/execution-flow.md](../02-runtime/execution-flow.md)).
- Validation spans policies, portfolio risk, execution constraints, compliance, and circuit-breaker state (see the other docs in this section).
- Every verdict emits a `RiskApproved` / `RiskRejected` event (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).
