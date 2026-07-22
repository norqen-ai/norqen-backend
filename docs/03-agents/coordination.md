# Coordination

All coordination in Norqen happens **through the planner**. Agents never coordinate with each other.

## The pattern

```
Planner
  │  assign objective
  ▼
Agent
  │  gather evidence
  ▼
Evidence
  │  return
  ▼
Planner   ← integrates, updates confidence, decides next step
```

The planner may repeat this with different agents, in any order it chooses, as many times as needed.

## Rules

- **All coordination occurs through the planner.** There is no agent-to-agent channel.
- **Agents are stateless specialists.** They hold no memory between invocations.
- **Shared state lives in the planner runtime**, not inside individual agents (see [../02-runtime/state-management.md](../02-runtime/state-management.md)).

## Why a hub-and-spoke model

- **Explainability** — the planner sees every objective and every piece of evidence, so any decision can be fully traced.
- **Safety** — no agent can trigger side effects or route around risk.
- **Simplicity** — agents stay small and independently testable; orchestration complexity lives in one place.

This is the concrete expression of the module boundaries in [../01-architecture/module-boundaries.md](../01-architecture/module-boundaries.md) and the dependency rules in [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md).
