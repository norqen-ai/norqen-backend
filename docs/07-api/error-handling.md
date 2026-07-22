# Error Handling

Errors are returned in a single, consistent structure. Internal detail never leaks to clients.

## Standard error structure

| Field | Purpose |
| --- | --- |
| `code` | Stable, machine-readable error code. |
| `message` | Human-readable summary (safe to display). |
| `details` | Structured, safe context (e.g. which field failed validation). |
| `correlation_id` | Ties the error to logs, traces, and the reasoning run (see [observability.md](observability.md)). |
| `timestamp` | When the error occurred. |

## The rule

> Never expose internal stack traces through public APIs.

Stack traces, database errors, and provider internals stay in the logs (keyed by `correlation_id`). Clients get a stable `code` and a safe `message` — enough to handle the error without exposing the system's internals.

## Conventions

- **Consistent everywhere** — REST responses, WebSocket error frames, and auth failures all use this envelope (see [authentication.md](authentication.md), [websocket-api.md](websocket-api.md)).
- **Stable codes** — `code` values are part of the API contract and versioned with it (see [versioning.md](versioning.md)).
- **Correlatable** — every error carries a `correlation_id` so support and debugging can trace it end to end.
- **Non-leaking auth errors** — authentication failures avoid revealing whether an account exists.
