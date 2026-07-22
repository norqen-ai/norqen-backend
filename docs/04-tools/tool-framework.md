# Tool Framework

> **Everything is a Tool.**

Market data, indicators, ML models, memory search, and brokers are all exposed as tools behind a common interface. The planner requests **capabilities**, never implementations.

## What "capability" means

The planner asks for *what* it needs, not *how* it is done:

- Get market history
- Search memory
- Compute RSI
- Forecast volatility
- Execute order

Each of these is a capability. One capability may have several implementations (providers), and the planner can switch between them freely.

## Why this matters

- **Interchangeability** — providers are swappable without touching the planner or agents (see [../01-architecture/hexagonal-architecture.md](../01-architecture/hexagonal-architecture.md)).
- **Resilience** — if one provider fails, another with the same capability takes over (see [tool-selection.md](tool-selection.md), [../02-runtime/failure-recovery.md](../02-runtime/failure-recovery.md)).
- **Uniform observability** — every tool invocation is measured the same way (see [observability.md](observability.md)).

## The contract

Every tool exposes the same interface regardless of provider — name, capability, schemas, health, latency, retry policy, and more. See [tool-interface.md](tool-interface.md). Tools are cataloged in the [tool registry](tool-registry.md), which the planner queries before selecting one.
