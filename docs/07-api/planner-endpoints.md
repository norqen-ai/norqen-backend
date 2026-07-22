# Planner Endpoints

The entry points for reasoning. These endpoints start and track planner runs (see [../02-runtime/planner.md](../02-runtime/planner.md)).

## Examples

| Endpoint | Purpose |
| --- | --- |
| `POST /planner/analyze` | Start a reasoning run for an ad-hoc analysis request. |
| `POST /planner/goal` | Submit a goal for the planner to pursue. |
| `GET /planner/{id}` | Retrieve the state/result of a run. |
| `POST /planner/cancel` | Cancel an in-progress run. |
| `GET /planner/history` | List past runs. |

## Asynchronous by design

> Planner responses include task IDs and streaming references.

A `POST` does not block until reasoning finishes. It **starts** a run and returns:

- a **task ID** to poll via `GET /planner/{id}`, and
- a **streaming reference** to follow live over WebSockets (see [websocket-api.md](websocket-api.md)).

This reflects that reasoning is long-running and adaptive (see [rest-api.md](rest-api.md), [../02-runtime/reasoning-loop.md](../02-runtime/reasoning-loop.md)).

## Notes

- Runs are **authenticated** and scoped to the caller (see [authentication.md](authentication.md)).
- Planner and execution are the **most expensive** endpoints and are rate-limited accordingly (see [rate-limiting.md](rate-limiting.md)).
- Any decision a run produces still passes through the deterministic Risk Engine before it can execute (see [execution-endpoints.md](execution-endpoints.md), [../06-risk/approval-flow.md](../06-risk/approval-flow.md)).
