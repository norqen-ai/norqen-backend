# Event-Driven Design

Every major action in Norqen emits an **event**. Events are the backbone of auditability, loose coupling, and replay.

## Why events

- **Auditability** — an immutable trail of everything that happened (see [../08-data/event-store.md](../08-data/event-store.md)).
- **Loose coupling** — producers do not need to know their consumers.
- **Replay** — reconstruct state or debug a run by replaying its events.
- **Observability** — events double as structured telemetry.

## Core events

| Event | Emitted when |
| --- | --- |
| `PlannerStarted` | A reasoning run begins |
| `EvidenceCollected` | A tool or agent returns evidence |
| `AgentCompleted` | A specialist agent finishes its objective |
| `DecisionCreated` | The planner proposes a candidate decision |
| `RiskApproved` / `RiskRejected` | The Risk Engine returns a verdict |
| `TradeExecuted` | An approved order is filled |
| `ReflectionCreated` | Post-execution reflection completes |
| `MemoryUpdated` | Memory is written or reinforced |

## Conventions

- Events are **immutable** and **append-only**.
- Each event carries a `correlation_id` tying it to its reasoning run (see [../07-api/observability.md](../07-api/observability.md)).
- Each event is timestamped and versioned so the schema can evolve safely.
- Components communicate through events **where appropriate** — this complements, not replaces, direct application-layer calls for synchronous use cases.

## Relationship to the event store

The event bus delivers events at run time; the [event store](../08-data/event-store.md) persists them immutably for audit and replay.
