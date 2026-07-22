# Suggested Project Structure

A layout that honors Clean Architecture (see [clean-architecture.md](clean-architecture.md)) while keeping each domain module cohesive. Names are a guide, not a contract.

```
backend/
  app/
    main.py              # FastAPI app factory + lifespan
    api/                 # PRESENTATION: routers, request/response schemas, deps
      v1/
    core/                # cross-cutting: config, security, errors, logging, DI
    planner/             # the reasoning brain (LangGraph graph + nodes)
    agents/              # specialist agents (technical, fundamental, macro, ...)
    tools/               # capability layer (market data, TA, ML, memory, broker)
    evidence/            # evidence collection, scoring, storage
    memory/              # episodic/semantic/reflection memory + retrieval
    reflection/          # post-execution learning
    risk/                # deterministic risk engine + policies
    execution/           # execution engine + broker adapters
    policies/            # versioned policy definitions
    analytics/           # portfolio analytics, backtesting
    domain/              # DOMAIN: entities, value objects, repository interfaces
    database/            # INFRASTRUCTURE: ORM models, sessions, migrations
    events/              # event bus, event definitions, handlers
    workers/             # background workers (ingestion, reflection, maintenance)
    websocket/           # streaming endpoints and channels
    tests/
```

## How this maps to the four layers

| Layer | Directories |
| --- | --- |
| Presentation | `api/`, `websocket/` |
| Application | `planner/`, service layers within each module |
| Domain | `domain/`, business rules inside `risk/`, `agents/`, `memory/`, etc. |
| Infrastructure | `database/`, `tools/` adapters, `execution/` broker adapters, `events/` bus |

## Foundation subset (Phase 1)

The first build touches only the platform slice:

```
app/
  main.py
  core/            # config, security, errors, logging
  api/v1/          # router aggregator + system (health/version) endpoints
  domain/          # base entities + repository interfaces
  database/        # async session, ORM base, Alembic migrations
  tests/
```

Auth, users, and portfolio management fill in next; the reasoning modules come after. See [../00-overview/backend-master-prompt.md](../00-overview/backend-master-prompt.md).
