# Market Data Tools

Tools that supply pricing and reference data. All sit behind the Market Data port (see [../01-architecture/hexagonal-architecture.md](../01-architecture/hexagonal-architecture.md)), so providers are interchangeable.

## Providers (adapters)

- Yahoo Finance
- Polygon
- Finnhub
- Alpha Vantage
- Twelve Data
- NSE/BSE integrations

## Capabilities

- Historical prices (OHLCV)
- Real-time quotes
- Company metadata
- Corporate actions
- Earnings

## Notes

- **Interchangeable.** The planner requests a capability (e.g. `market.history`); the registry and selection logic pick the healthiest provider (see [tool-registry.md](tool-registry.md), [tool-selection.md](tool-selection.md)).
- **Normalized.** Provider responses are validated and normalized into a common shape before use, so downstream agents never see provider-specific formats (see [../08-data/market-data-pipeline.md](../08-data/market-data-pipeline.md)).
- **Cached.** Frequently requested data (quotes, recent history) is cached with TTLs to control cost and latency (see [../08-data/caching.md](../08-data/caching.md)).
