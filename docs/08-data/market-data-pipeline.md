# Market Data Pipeline

How external market data becomes trustworthy, normalized data that tools can serve.

## Pipeline

```
Provider → Validation → Normalization → Storage → Cache → Tool Access
```

| Stage | What happens |
| --- | --- |
| **Provider** | Raw data is fetched from a market-data adapter (see [../04-tools/market-data-tools.md](../04-tools/market-data-tools.md)). |
| **Validation** | The payload is checked for integrity and completeness. |
| **Normalization** | Provider-specific formats are converted to a common shape. |
| **Storage** | Normalized data is persisted (see [database-architecture.md](database-architecture.md)). |
| **Cache** | Hot data is cached with TTLs (see [caching.md](caching.md)). |
| **Tool Access** | Agents and the planner read it through market-data tools. |

## Supported data

- Historical OHLCV
- Quotes
- Fundamentals
- News metadata

## Why normalize early

Normalizing at ingestion means every downstream consumer — agents, indicators, ML, backtests — sees one consistent format, regardless of which provider supplied it. This is what makes providers interchangeable (see [../01-architecture/hexagonal-architecture.md](../01-architecture/hexagonal-architecture.md)).

## Notes

- **Validation failures** are surfaced as data-quality signals and can trip circuit breakers on integrity issues (see [observability.md](observability.md), [../06-risk/circuit-breakers.md](../06-risk/circuit-breakers.md)).
- Ingestion runs as **background work**, off the request path (see [../01-architecture/backend-architecture.md](../01-architecture/backend-architecture.md)).
