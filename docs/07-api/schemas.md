# Schemas

The API uses **strongly typed** request and response models. Validation happens at the edge, before any business logic runs.

## Core models

| Model | Represents |
| --- | --- |
| `Goal` | An objective submitted to the planner. |
| `PlannerState` | The state/progress of a reasoning run (see [../02-runtime/state-management.md](../02-runtime/state-management.md)). |
| `Evidence` | A sourced, timestamped piece of information. |
| `Decision` | A candidate action produced by reasoning. |
| `RiskResult` | The Risk Engine's verdict and explanation (see [../06-risk/risk-engine.md](../06-risk/risk-engine.md)). |
| `Trade` | An executed order and its fill. |
| `Reflection` | A post-execution lesson (see [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md)). |
| `MemoryReference` | A pointer to retrieved memory (see [../05-memory/retrieval.md](../05-memory/retrieval.md)). |

## The rule

> Validation occurs before business logic.

Requests are validated against their schemas at the boundary; malformed input is rejected with a standard error before it can reach the application layer (see [error-handling.md](error-handling.md)).

## Notes

- These are **API models** (the public contract). They are distinct from domain entities and ORM models; the application layer maps between them, keeping the public contract stable while internals evolve (see [../01-architecture/clean-architecture.md](../01-architecture/clean-architecture.md)).
- Models are versioned with the API surface (see [versioning.md](versioning.md)).
- Field naming, timestamps, and IDs follow the data schema conventions (UUIDs, provenance — see [../08-data/schemas.md](../08-data/schemas.md)).
