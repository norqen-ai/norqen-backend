# Broker Adapters

Adapters behind the Broker port that place orders and report account/position state.

## Supported adapters

- Alpaca
- Interactive Brokers
- Zerodha
- Angel One
- Paper Broker

## The mandatory path

> Execution always flows through the Execution Engine before reaching adapters.

```
Approved Decision → Execution Engine → Broker Adapter → Broker
```

Nothing calls a broker adapter directly — not agents, not the planner (see [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md)). And nothing reaches the Execution Engine without deterministic risk approval (see [../06-risk/approval-flow.md](../06-risk/approval-flow.md)).

## Rules

- **Adapters contain no business logic.** They only translate the Execution Engine's order contract into a provider API and back.
- **Paper Broker** is a first-class adapter for paper trading and testing, using the same contract as live adapters (see [../07-api/execution-endpoints.md](../07-api/execution-endpoints.md)).
- Adapter availability is part of the execution constraints checked before any order (see [../06-risk/execution-constraints.md](../06-risk/execution-constraints.md)).
