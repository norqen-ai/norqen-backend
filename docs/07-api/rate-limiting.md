# Rate Limiting

Configurable limits protect the system from abuse and runaway cost — especially the expensive reasoning and execution endpoints.

## Limit dimensions

- Per user
- Per API key
- Per endpoint
- Burst limits

## The priority

> Protect expensive planner and execution endpoints.

A single planner run can invoke many tools and models, and execution has real financial impact. These endpoints get the tightest limits, while cheap read endpoints (e.g. `/system`, `/portfolio`) can be more permissive.

## Implementation notes

- **Redis-backed** counters make limits fast and shared across instances (see [../08-data/caching.md](../08-data/caching.md)).
- **Layered** — per-user and per-API-key limits apply together with per-endpoint and burst limits.
- **Configurable** — limits are environment-driven, not hard-coded, so they can be tuned per deployment.
- **Standard errors** — exceeding a limit returns the standard error envelope with a rate-limit code (see [error-handling.md](error-handling.md)).

## Why

Rate limiting is both a **cost control** (tools and models cost money — see [../04-tools/observability.md](../04-tools/observability.md)) and a **safety control** (it bounds how fast execution can be requested).
