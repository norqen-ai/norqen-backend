# API Philosophy

> The API exposes **capabilities**, not CRUD resources.

Clients ask Norqen to **reason, analyze, execute, and retrieve state** — they do not manipulate internal implementation details or database rows.

## Capability vs. CRUD

| CRUD mindset | Norqen capability mindset |
| --- | --- |
| `POST /decisions` (insert a row) | `POST /planner/analyze` (ask Norqen to reason toward a goal) |
| `PUT /orders/{id}` (edit a record) | `POST /execution/live` (request an execution, subject to risk) |
| Exposes the schema | Exposes the intent |

## Why

- **Safety** — clients cannot fabricate a "decision" and push it to execution; they can only *request* reasoning, and every action still passes through risk (see [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md)).
- **Stability** — internal models can change without breaking the public contract.
- **Clarity** — endpoints map to what users actually want Norqen to do.

## Consequences

- Reasoning endpoints start **long-running tasks** and return task IDs plus streaming references, rather than blocking (see [planner-endpoints.md](planner-endpoints.md), [websocket-api.md](websocket-api.md)).
- Requests and responses are **strongly typed** and validated before any business logic runs (see [schemas.md](schemas.md)).
- The surface is **versioned** so capabilities can evolve additively (see [versioning.md](versioning.md)).
