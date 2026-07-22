# Technical Agent

Analyzes price action and market structure to produce technical evidence.

## Responsibilities

- Trend analysis
- Momentum analysis
- Volatility analysis
- Support & resistance
- Volume analysis

## How it works

The agent **dynamically selects indicators** (RSI, EMA, MACD, ATR, Bollinger Bands, and others) based on the planner's objective, instead of computing every indicator every time. This keeps evidence relevant and cost bounded.

Indicators are requested from the technical-analysis tools, which prefer local computation over external APIs (see [../04-tools/technical-analysis-tools.md](../04-tools/technical-analysis-tools.md)).

## Tools it uses

- Market data tools — OHLCV history and quotes (see [../04-tools/market-data-tools.md](../04-tools/market-data-tools.md)).
- Technical-analysis tools — indicator computation.

## Output

Structured technical evidence (levels, signals, readings) with the timeframe and data window it was computed on. It produces **evidence, not buy/sell calls** — the planner integrates it with other agents' findings.

## Boundary

Like all agents, it returns to the planner and never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
