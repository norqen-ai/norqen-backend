# Event Store

An append-only log of immutable events. It is the backbone of auditability and replay (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).

## What it persists

Immutable events such as:

- `PlannerStarted`
- `EvidenceCollected`
- `RiskApproved` / `RiskRejected`
- `TradeExecuted`
- `ReflectionCreated`

(and the other events in the system — this is a representative set.)

## Why

> Events enable replay and auditing.

- **Audit** — a permanent, tamper-evident record of everything that happened and why.
- **Replay** — reconstruct a reasoning run or system state by replaying its events.
- **Explainability** — the event trail is how any decision is justified after the fact.

## Properties

- **Immutable & append-only** — events are never edited or deleted (retention governs archival — see [retention.md](retention.md)).
- **Correlated** — each event carries the run's `correlation_id` (see [../07-api/observability.md](../07-api/observability.md)).
- **Timestamped & versioned** — so the event schema can evolve without breaking replay.

## Relationship to the event bus

The **event bus** delivers events to consumers at run time (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)); the **event store** persists them durably. Streaming to the UI is a live *view*; the event store is the *source of truth* (see [../02-runtime/streaming.md](../02-runtime/streaming.md)).
