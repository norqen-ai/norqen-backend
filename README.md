# Norqen Backend

Norqen is an **AI-native Financial Intelligence Operating System** — an autonomous reasoning system that observes markets, plans investigations, gathers evidence, reasons over uncertainty, validates deterministic risk, executes when appropriate, reflects on outcomes, and learns over time.

It is not a trading dashboard, an LLM wrapper, or a prediction engine.

## The reasoning loop

```
Observe → Plan → Acquire Evidence → Reason → Risk → Execute → Reflect → Learn
```

The **planner** is the non-deterministic brain; the **Risk Engine** is the deterministic final authority. See [docs/00-overview/vision.md](docs/00-overview/vision.md).

## Stack

- **Language:** Python (async-first, strongly typed)
- **Frameworks:** FastAPI, LangGraph
- **Storage:** PostgreSQL, Redis, Vector DB, Object Storage
- **Architecture:** DDD · Clean · Hexagonal · Event-Driven

## Documentation

The full design lives in [`docs/`](docs/). Start with [docs/00-overview/README.md](docs/00-overview/README.md).

| Section | Topic |
| --- | --- |
| [00-overview](docs/00-overview/README.md) | Vision, philosophy, principles, vocabulary |
| [01-architecture](docs/01-architecture/README.md) | System shape, layering, boundaries, deployment |
| [02-runtime](docs/02-runtime/README.md) | The autonomous reasoning runtime |
| [03-agents](docs/03-agents/README.md) | Specialist agents |
| [04-tools](docs/04-tools/README.md) | The capability layer |
| [05-memory](docs/05-memory/README.md) | Accumulating and reusing experience |
| [06-risk](docs/06-risk/README.md) | Deterministic risk validation |
| [07-api](docs/07-api/README.md) | The public API surface |
| [08-data](docs/08-data/README.md) | Persistence and data architecture |

## Build status

This repository currently contains the **design specification**. Implementation begins with the **core backend foundation** — the FastAPI app, configuration, async database/session layer (SQLAlchemy 2.0 + Alembic + PostgreSQL), authentication (custom JWT + refresh + API keys + RBAC), error handling, and observability — before the reasoning system is layered on top. See [docs/00-overview/backend-master-prompt.md](docs/00-overview/backend-master-prompt.md).
