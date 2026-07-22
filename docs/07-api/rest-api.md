# REST API

The REST surface is grouped by capability. All endpoints live under a version prefix (see [versioning.md](versioning.md)), e.g. `/api/v1/planner/...`.

## Endpoint groups

| Group | Purpose |
| --- | --- |
| `/planner` | Start and track reasoning runs (see [planner-endpoints.md](planner-endpoints.md)) |
| `/agents` | Inspect specialist agents and their capabilities |
| `/tools` | Inspect the tool registry and tool health (see [../04-tools/tool-registry.md](../04-tools/tool-registry.md)) |
| `/memory` | Query stored experience (see [../05-memory/retrieval.md](../05-memory/retrieval.md)) |
| `/risk` | Inspect policies and risk evaluations (see [../06-risk/README.md](../06-risk/README.md)) |
| `/execution` | Paper and live execution (see [execution-endpoints.md](execution-endpoints.md)) |
| `/portfolio` | Portfolio state, holdings, exposure |
| `/analytics` | Analytics and reporting |
| `/backtest` | Historical strategy evaluation |
| `/system` | Health, version, readiness/liveness |

## The nature of these endpoints

> REST endpoints initiate long-running reasoning tasks and retrieve results.

Reasoning is not instantaneous. A call to `/planner/analyze` **starts** a run and returns a task ID and a streaming reference; the client then follows progress over WebSockets (see [websocket-api.md](websocket-api.md)) and/or polls for the final result. This keeps the API responsive and the reasoning asynchronous.

## Conventions

- **Versioned** paths under `/api/v1` (see [versioning.md](versioning.md)).
- **Authenticated** — every request is authenticated and authorized (see [authentication.md](authentication.md)).
- **Typed** request/response models with validation before business logic (see [schemas.md](schemas.md)).
- **Standard errors** with a correlation ID (see [error-handling.md](error-handling.md)).
- **Rate limited**, especially the expensive planner and execution groups (see [rate-limiting.md](rate-limiting.md)).
