# System Architecture

Norqen is an AI-native Financial Intelligence Operating System. This is the end-to-end path a goal takes through the system.

## High-level flow

```
Frontend (Next.js)
      │
      ▼
FastAPI Gateway          ← authn/authz, validation, rate limiting, correlation IDs
      │
      ▼
Application Layer        ← use cases, orchestration entry points
      │
      ▼
Planner (LangGraph)      ← the brain: plans, selects, replans, decides when to stop
      │
      ▼
Specialist Agents        ← technical, fundamental, macro, news, quant, portfolio, ...
      │
      ▼
Tool Layer               ← uniform capability interface over all providers
      │
      ▼
Evidence Engine          ← collects, scores, and stores evidence
      │
      ▼
Risk Engine              ← deterministic validation: APPROVE / MODIFY / REJECT
      │
      ▼
Execution Engine         ← sends approved orders to broker adapters
      │
      ▼
Reflection               ← compares expected vs. actual outcome
      │
      ▼
Memory                   ← persists lessons for future reasoning
```

## The three anchors

- **FastAPI exposes capabilities.** Clients ask Norqen to reason, analyze, and execute — not to manipulate rows. See [../07-api/api-philosophy.md](../07-api/api-philosophy.md).
- **The Planner is the brain.** It decides the path through the system at run time; nothing below it is a fixed pipeline. See [../02-runtime/planner.md](../02-runtime/planner.md).
- **The Risk Engine is the final authority.** No order reaches a broker without its deterministic approval. See [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md).

## Cross-cutting concerns

These wrap the whole flow rather than sitting at one layer:

- **Events** — every major step emits an immutable event (see [event-driven-design.md](event-driven-design.md)).
- **Observability** — latency, success/error rates, and correlation IDs are captured end to end (see [../07-api/observability.md](../07-api/observability.md)).
- **Streaming** — planner progress is streamed to the UI over WebSockets (see [../02-runtime/streaming.md](../02-runtime/streaming.md)).
