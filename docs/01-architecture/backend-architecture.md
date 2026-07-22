# Backend Architecture

## Stack

- **Language:** Python 3.11+ (async-first, strongly typed)
- **Frameworks:** FastAPI (API), LangGraph (planner orchestration)
- **Storage:**
  - PostgreSQL — relational source of truth
  - Redis — cache, rate limiting, ephemeral planner/session state
  - Vector Database — embeddings for memory and semantic search
  - Object Storage — large artifacts (reports, raw payloads, model outputs)

## Engineering principles

- **Async-first** — non-blocking I/O throughout (DB, HTTP, brokers, tools).
- **Strong typing** — Pydantic models at the edges, typed domain entities within.
- **Dependency Injection** — dependencies are provided, not constructed inline, so they can be swapped and tested.
- **Repository Pattern** — the domain talks to abstract repositories; infrastructure implements them.
- **Service Layer** — application services coordinate use cases and transactions.
- **Event Bus** — components emit and react to events instead of tight coupling (see [event-driven-design.md](event-driven-design.md)).
- **Background Workers** — long-running and scheduled work (ingestion, reflection, memory maintenance) runs outside the request path (see [../08-data/market-data-pipeline.md](../08-data/market-data-pipeline.md)).

## The guiding rule

> The backend should expose **capabilities**, not CRUD resources.

Endpoints let clients ask Norqen to reason, analyze, execute, and retrieve state — they do not expose internal tables. See [../07-api/api-philosophy.md](../07-api/api-philosophy.md).

## Foundation-first build

The reasoning system depends on a solid platform layer. Build that first: application factory, config, DB/session, auth, error handling, and observability (see [../00-overview/backend-master-prompt.md](../00-overview/backend-master-prompt.md)). Everything else layers on top of it behind interfaces.
