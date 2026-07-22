# Tool Selection

How the planner decides which tool to invoke next. Selection is driven by uncertainty, not by a fixed order.

## Strategy

```
Goal
  → Missing information        (what is uncertain?)
  → Candidate capabilities     (which capabilities could close the gap?)
  → Healthy tools              (which providers are available? — registry)
  → Lowest expected uncertainty (which reduces uncertainty most per cost?)
  → Execute
  → Evaluate evidence
  → Repeat if needed
```

## What informs each step

- **Missing information** comes from the current planner state and confidence estimate (see [../02-runtime/state-management.md](../02-runtime/state-management.md), [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).
- **Candidate capabilities** are matched against the tool interface's `capability` field (see [tool-interface.md](tool-interface.md)).
- **Healthy tools** are filtered using live registry metadata — health, latency, cost, rate limits (see [tool-registry.md](tool-registry.md)).
- **Lowest expected uncertainty** balances information gain against cost and latency.

## Automatic fallback

> The planner may switch providers automatically if a tool is unavailable.

Because tools are matched by capability, an unhealthy or rate-limited provider is simply skipped in favor of another that offers the same capability (see [../02-runtime/failure-recovery.md](../02-runtime/failure-recovery.md)).
