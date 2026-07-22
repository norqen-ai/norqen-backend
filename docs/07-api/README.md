# 07 - API

Defines the **public interface** of the Norqen backend — the FastAPI surface clients use to reason, analyze, execute, and observe.

## Reading order

1. [api-philosophy.md](api-philosophy.md) — capabilities, not CRUD
2. [rest-api.md](rest-api.md) — endpoint groups
3. [websocket-api.md](websocket-api.md) — real-time streams
4. [authentication.md](authentication.md) — JWT, refresh, API keys, RBAC
5. [versioning.md](versioning.md) — explicit API versions
6. [planner-endpoints.md](planner-endpoints.md) — starting and tracking reasoning
7. [execution-endpoints.md](execution-endpoints.md) — paper and live execution
8. [schemas.md](schemas.md) — strongly typed models
9. [error-handling.md](error-handling.md) — the standard error envelope
10. [rate-limiting.md](rate-limiting.md) — protecting expensive endpoints
11. [observability.md](observability.md) — metrics, logs, traces, correlation IDs

## Foundation-first

The core backend build lands here first: the FastAPI app, `/api/v1` versioning, authentication, error handling, rate limiting, and observability — plus a `system` group for health/version. The reasoning-specific endpoints (planner, execution) are thin layers over the application services described elsewhere in these docs. See [../00-overview/backend-master-prompt.md](../00-overview/backend-master-prompt.md).
