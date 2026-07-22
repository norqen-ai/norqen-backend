# WebSocket API

Real-time channels that keep the frontend synchronized with reasoning runs and system state. This is the transport for planner streaming (see [../02-runtime/streaming.md](../02-runtime/streaming.md)).

## Streams

- Planner progress
- Active agent
- Evidence updates
- Confidence changes
- Risk decisions
- Execution status
- Portfolio updates
- System events

## Purpose

> Streaming keeps the frontend synchronized with planner state.

Because reasoning runs are long-lived and asynchronous (a REST call starts them — see [rest-api.md](rest-api.md)), WebSockets deliver progress as it happens instead of forcing the client to poll.

## Conventions

- **Authenticated** — connections are authenticated like REST requests (see [authentication.md](authentication.md)).
- **Correlated** — every message carries the run's `correlation_id` so the client can group updates by run (see [observability.md](observability.md)).
- **Sanitized** — streamed reasoning is scrubbed of secrets and internal detail (see [error-handling.md](error-handling.md)).
- **A view, not the source of truth** — the authoritative record is the event store; a reconnecting client can resync from persisted state (see [../08-data/event-store.md](../08-data/event-store.md)).
