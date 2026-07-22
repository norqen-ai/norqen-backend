# Caching

Redis is the caching and ephemeral-state layer. It keeps hot data fast and shields expensive providers from repeated calls.

## What Redis caches

- Quotes
- Technical indicators
- Planner sessions
- Tool responses

Redis also backs non-cache ephemeral state: rate-limit counters (see [../07-api/rate-limiting.md](../07-api/rate-limiting.md)) and the refresh-token store (see [../07-api/authentication.md](../07-api/authentication.md)).

## The rule

> Use TTLs and invalidation to maintain freshness.

- **TTLs** — every cached entry expires; freshness requirements set the TTL (real-time quotes short, computed indicators longer).
- **Invalidation** — entries are proactively invalidated when the underlying data changes.

## Why cache these

- **Quotes / tool responses** — avoid re-hitting rate-limited, paid providers (see [../04-tools/observability.md](../04-tools/observability.md)).
- **Indicators** — deterministic computations that are expensive to repeat (see [../04-tools/technical-analysis-tools.md](../04-tools/technical-analysis-tools.md)).
- **Planner sessions** — fast access to in-flight run state (see [../02-runtime/state-management.md](../02-runtime/state-management.md)).

## Notes

- Cache is **not** the source of truth — PostgreSQL and the event store are (see [database-architecture.md](database-architecture.md), [event-store.md](event-store.md)).
- Cache hit ratio is monitored as a data-quality signal (see [observability.md](observability.md)).
