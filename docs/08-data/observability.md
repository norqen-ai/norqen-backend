# Data Observability

Data quality is treated as a first-class operational signal. If the data is wrong or stale, everything built on it is wrong too.

## Metrics monitored

- Pipeline latency
- Ingestion failures
- Cache hit ratio
- Replication health
- Query latency
- Storage growth

## The principle

> Data quality metrics are first-class operational signals.

Bad data is a safety issue, not just an inconvenience: reasoning and risk both depend on accurate, timely data. So data health is monitored with the same seriousness as API and risk health.

## What the metrics drive

- **Pipeline latency / ingestion failures** — surface stale or missing market data; integrity failures can trip circuit breakers (see [market-data-pipeline.md](market-data-pipeline.md), [../06-risk/circuit-breakers.md](../06-risk/circuit-breakers.md)).
- **Cache hit ratio** — reveals whether caching is effective or needs tuning (see [caching.md](caching.md)).
- **Query latency / replication health** — protect the responsiveness of the whole system.
- **Storage growth** — informs retention tuning (see [retention.md](retention.md)).

## Relationship to overall observability

Data observability is one facet of the system-wide picture, alongside API ([../07-api/observability.md](../07-api/observability.md)), tools ([../04-tools/observability.md](../04-tools/observability.md)), memory ([../05-memory/memory-observability.md](../05-memory/memory-observability.md)), and risk ([../06-risk/monitoring.md](../06-risk/monitoring.md)). Signals share correlation IDs so issues can be traced across layers.
