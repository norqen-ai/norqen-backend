# Streaming

The planner streams its progress so the frontend stays synchronized with the reasoning run in real time.

## What is streamed

- **Thoughts (sanitized)** — human-readable reasoning summaries, with sensitive detail removed.
- **Current task** — which task the planner is working on.
- **Active agent** — which specialist is engaged.
- **Evidence updates** — new evidence as it is collected.
- **Confidence updates** — how confidence changes over the run (see [confidence-model.md](confidence-model.md)).
- **Decisions** — candidate decisions as they are proposed.

## Transport

Streamed over **WebSockets** for a live UI. The full channel list (including risk decisions, execution status, and portfolio updates) is defined in [../07-api/websocket-api.md](../07-api/websocket-api.md).

## Principles

- **Sanitize before streaming.** Never leak secrets, raw credentials, or internal stack traces (see [../07-api/error-handling.md](../07-api/error-handling.md)).
- **Correlate.** Every streamed message carries the run's `correlation_id` so the UI can group it (see [../07-api/observability.md](../07-api/observability.md)).
- **Streaming is a view, not the source of truth.** The authoritative record is the event store (see [../08-data/event-store.md](../08-data/event-store.md)); a client that disconnects can resync from persisted state.
