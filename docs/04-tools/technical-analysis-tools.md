# Technical Analysis Tools

Indicator computation tools used mainly by the Technical Agent (see [../03-agents/technical-agent.md](../03-agents/technical-agent.md)).

## Prefer local computation

> Prefer local computation over APIs.

Indicators are deterministic math over price series. Computing them locally is cheaper, faster, and avoids provider dependence — market data comes from the market-data tools, and the indicators are derived in-process.

## Examples

RSI, EMA, SMA, MACD, ATR, VWAP, ADX, OBV, Bollinger Bands, SuperTrend.

## How they are used

The Technical Agent **requests only the indicators required for the current objective**, rather than computing the full set every time. Each result carries the parameters (period, source series) and the data window it was computed over, so it is reproducible.

## Notes

- **Cacheable.** Indicator results for a given series+parameters are cached to avoid recomputation (see [../08-data/caching.md](../08-data/caching.md)).
- **Versioned.** The computation version is recorded so historical evidence stays reproducible (see [tool-interface.md](tool-interface.md)).
