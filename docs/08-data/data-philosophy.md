# Data Philosophy

> Data is a strategic asset.

Raw market data, planner state, evidence, memories, and execution history are **persisted independently** to maximize auditability and reuse.

## Why persist everything independently

- **Auditability** — any decision can be reconstructed from the exact data that produced it (see [event-store.md](event-store.md)).
- **Reuse** — the same raw data feeds many purposes: reasoning, backtesting, memory, and analytics.
- **Reproducibility** — because inputs are stored with provenance and timestamps, past reasoning can be re-examined faithfully (see [schemas.md](schemas.md)).
- **Learning** — accumulated history is what makes reflection and memory valuable (see [../05-memory/memory-philosophy.md](../05-memory/memory-philosophy.md)).

## Principles

- **Separation of concerns** — each data type lives in the engine suited to it (see [database-architecture.md](database-architecture.md)).
- **Immutability where it matters** — events and incidents are append-only and never edited (see [event-store.md](event-store.md), [../06-risk/incident-response.md](../06-risk/incident-response.md)).
- **Provenance everywhere** — important records track where they came from and when.
- **Governed lifecycle** — data is retained and archived by explicit policy (see [retention.md](retention.md)).
