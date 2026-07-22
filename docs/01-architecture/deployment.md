# Deployment

Norqen is designed to start simple and scale out without changing the domain model.

## Phase 1 — Modular monolith

A single deployable FastAPI application containing all modules, backed by:

- PostgreSQL
- Redis
- Vector DB
- Object Storage

Background work (ingestion, reflection, memory maintenance) runs as worker processes alongside the API. This keeps operations simple while the system matures.

## Future — Independently scalable services

As load grows, split along the boundaries that already exist in the monolith:

```
Frontend
API
Agent Runtime
ML Runtime
Worker Cluster
Redis
PostgreSQL
Vector DB
Monitoring
```

Each can scale independently — for example, the ML runtime and worker cluster scale with reasoning volume, while the API scales with client traffic.

> **Note:** The **ML Runtime is external to this repository.** ML models are implemented, trained, and served in a separate repository/service, and this backend fetches them over the ML port when needed (see [../04-tools/ml-tools.md](../04-tools/ml-tools.md), [../00-overview/README.md](../00-overview/README.md)). It is shown here only to place it in the overall deployment topology.

## The invariant

> Scale services independently while preserving the same domain model.

Because the architecture is Clean + Hexagonal (see [clean-architecture.md](clean-architecture.md), [hexagonal-architecture.md](hexagonal-architecture.md)), extracting a module into its own service is a deployment change, not a rewrite. The module boundaries in [module-boundaries.md](module-boundaries.md) are the seams along which the monolith splits.

## Operational baseline

- **Configuration** is environment-driven (12-factor); secrets never live in code.
- **Migrations** are version-controlled and run before rollout (see [../08-data/migrations.md](../08-data/migrations.md)).
- **Observability** (metrics, logs, traces, correlation IDs) is in place from Phase 1 (see [../07-api/observability.md](../07-api/observability.md)).
