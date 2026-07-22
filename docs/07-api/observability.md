# API Observability

Every request is measurable. Observability is part of the core backend foundation, in place from Phase 1.

## What is captured

- Request latency
- Success rate
- Error rate
- Streaming duration
- Planner runtime
- Correlation IDs

## The rule

> Expose metrics, logs, and traces for monitoring.

The three pillars work together:

- **Metrics** — aggregate health (latency, success/error rates, throughput).
- **Logs** — structured, keyed by `correlation_id`.
- **Traces** — the path of a request across layers and tools.

## Correlation IDs

A `correlation_id` is assigned at the edge and threaded through everything a request touches — logs, traces, emitted events, streamed WebSocket messages, tool telemetry, and the error envelope (see [error-handling.md](error-handling.md), [../04-tools/observability.md](../04-tools/observability.md), [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)). This makes a single reasoning run traceable end to end.

## Relationship to other observability

This is the API-layer view. It composes with tool observability ([../04-tools/observability.md](../04-tools/observability.md)), memory observability ([../05-memory/memory-observability.md](../05-memory/memory-observability.md)), risk monitoring ([../06-risk/monitoring.md](../06-risk/monitoring.md)), and data observability ([../08-data/observability.md](../08-data/observability.md)) into one operational picture.
