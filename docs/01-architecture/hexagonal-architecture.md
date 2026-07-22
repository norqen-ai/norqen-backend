# Hexagonal Architecture

Norqen isolates the domain from the outside world using **ports** (interfaces the domain defines) and **adapters** (implementations that fulfill them). The domain depends only on ports, never on concrete providers.

## Ports

Each port is a capability the domain requires, expressed as an interface:

| Port | Responsibility |
| --- | --- |
| Market Data | Prices, quotes, fundamentals, corporate actions |
| News | Headlines, articles, events, entity extraction |
| Broker | Order placement, positions, account state |
| ML | Forecasts, regime detection, sentiment, anomalies (fulfilled by an **external** ML service — see note below) |
| Memory | Store and retrieve embeddings and experiences |
| Risk | Deterministic validation of decisions |

## Adapters

Interchangeable implementations behind each port:

| Port | Example adapters |
| --- | --- |
| Market Data | Yahoo Finance, Polygon, Finnhub, Alpha Vantage, Twelve Data |
| Broker | Alpaca, Interactive Brokers, Zerodha, Angel One, Paper Broker |
| News | NewsAPI, GDELT, RSS, vendor feeds |
| Memory | PostgreSQL + Vector DB |

## The rule

> The domain depends only on interfaces.

Adapters are selected and injected at the edge (see [../01-architecture/backend-architecture.md](backend-architecture.md)). Because everything external is a port, the planner can treat providers as **interchangeable tools** and switch between them at run time — see [../04-tools/tool-framework.md](../04-tools/tool-framework.md) and [../04-tools/tool-selection.md](../04-tools/tool-selection.md).

Adapters contain **no business logic** — they only translate between the port's contract and the provider's API. See [dependency-rules.md](dependency-rules.md).

## Note: the ML port is external

The **ML port is fulfilled by a separate repository/service**, not implemented in this repo. This backend owns only the ML port and its adapter stubs, and fetches ML capabilities over that interface when needed. See [../04-tools/ml-tools.md](../04-tools/ml-tools.md) and [../00-overview/README.md](../00-overview/README.md).
