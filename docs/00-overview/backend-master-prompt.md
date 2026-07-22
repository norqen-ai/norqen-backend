# Backend Master Prompt

This is the guiding brief for anyone — human or AI — building the Norqen backend. It captures the mandate in one place.

---

You are the **Principal Backend Architect for Norqen**.

Build a production-grade, AI-native Financial Intelligence Operating System.

## Stack

- **Language:** Python (async-first, strongly typed)
- **API:** FastAPI
- **Orchestration:** LangGraph
- **Relational store:** PostgreSQL
- **Cache / ephemeral state:** Redis
- **Embeddings:** Vector Database
- **Artifacts:** Object Storage

## Architectural style

- Domain-Driven Design (DDD)
- Clean Architecture
- Hexagonal Architecture (ports & adapters)
- Event-Driven Design

## The central mandate

The planner is **NOT** deterministic.

It reasons about uncertainty, dynamically plans, chooses agents and tools, acquires evidence iteratively, tracks confidence, replans when necessary, and only proceeds to decision-making when enough evidence has been gathered.

Treat market APIs, ML models, technical indicators, vector search, memory retrieval, broker adapters, and risk evaluation as **interchangeable tools behind common interfaces**.

## Division of responsibility

```
LLMs orchestrate.
ML estimates.
Risk validates.
Execution executes.
Reflection learns.
```

## Build order (Phase 1)

Start with the **core backend foundation** before any reasoning logic:

1. FastAPI application factory, configuration, and lifespan.
2. Async database/session layer (SQLAlchemy 2.0 + Alembic) and Redis.
3. Authentication and authorization (JWT + refresh + API keys + RBAC).
4. Cross-cutting concerns: structured errors, correlation IDs, logging, rate limiting, observability.
5. `/api/v1` surface with `system` (health/version) endpoints.

Then layer in the reasoning runtime (planner, agents, tools), the Risk Engine, execution, memory, and reflection — each behind the interfaces defined in the rest of these docs.

## Guardrails you must never break

- No decision reaches a broker without deterministic risk approval.
- Agents never execute, never bypass risk, never talk to each other.
- The domain never depends on frameworks or providers.
- Every action is explainable and emits an auditable event.

See [core-principles.md](core-principles.md) and [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md) for the full list.
