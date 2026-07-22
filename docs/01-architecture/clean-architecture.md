# Clean Architecture

Norqen is organized into four concentric layers. Dependencies point **inward only**.

## Layers

```
┌─────────────────────────────────────────────┐
│ Presentation   (FastAPI routers, WebSockets) │
│  ┌───────────────────────────────────────┐   │
│  │ Application (use cases, services)      │   │
│  │  ┌─────────────────────────────────┐  │   │
│  │  │ Domain (entities, rules, ports) │  │   │
│  │  └─────────────────────────────────┘  │   │
│  └───────────────────────────────────────┘   │
│ Infrastructure (DB, brokers, market data, ML) │
└─────────────────────────────────────────────┘
```

- **Presentation** — translates HTTP/WebSocket requests into application calls. No business logic.
- **Application** — orchestrates use cases, transactions, and the planner lifecycle. Depends on the domain, not on infrastructure.
- **Domain** — pure business rules and entities (User, Portfolio, Decision, Evidence, ...). Depends on nothing external.
- **Infrastructure** — concrete implementations of domain ports: databases, broker adapters, market-data providers, ML runtimes.

## The rule that matters

> Business rules never depend on frameworks.

FastAPI, PostgreSQL, Redis, brokers, and market-data APIs are all **replaceable infrastructure**. The domain expresses what it needs through interfaces (ports); infrastructure provides adapters. See [hexagonal-architecture.md](hexagonal-architecture.md) and [dependency-rules.md](dependency-rules.md).

## Why

- **Testability** — the domain and application layers test without a database or network.
- **Replaceability** — swap Alembic, a broker, or a market-data vendor without touching business rules.
- **Longevity** — frameworks change faster than the domain; keep the domain insulated.
