# Domain Model

The core entities of Norqen. These are the domain concepts (see [../01-architecture/clean-architecture.md](../01-architecture/clean-architecture.md)); API models and ORM models map to and from them.

## Core entities

| Entity | Represents |
| --- | --- |
| **User** | An authenticated principal (see [../07-api/authentication.md](../07-api/authentication.md)). |
| **Portfolio** | A collection of positions and capital belonging to a user. |
| **Position** | A holding in a specific instrument. |
| **Goal** | An objective submitted to the planner. |
| **PlannerState** | The working state of a reasoning run (see [../02-runtime/state-management.md](../02-runtime/state-management.md)). |
| **Evidence** | A sourced, timestamped input to reasoning. |
| **Decision** | A candidate action produced by reasoning. |
| **Order** | An instruction to a broker (pre/at execution). |
| **Trade** | An executed, filled order. |
| **Reflection** | A post-execution lesson (see [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md)). |
| **Memory** | Persisted, retrievable experience (see [../05-memory/memory-types.md](../05-memory/memory-types.md)). |

## How they relate

```
User ──owns──► Portfolio ──holds──► Position
User ──submits──► Goal ──drives──► PlannerState
PlannerState ──gathers──► Evidence ──informs──► Decision
Decision ──(risk-approved)──► Order ──filled──► Trade
Trade ──triggers──► Reflection ──becomes──► Memory
Memory ──informs future──► PlannerState
```

## Conventions

Entities use UUID identifiers and track timestamps, versions, and provenance where it matters (see [schemas.md](schemas.md)). The lifecycle from Goal to Memory mirrors the reasoning loop (see [../02-runtime/reasoning-loop.md](../02-runtime/reasoning-loop.md)).
