# Migrations

All schema changes are made through **version-controlled migrations**. The database schema is never changed by hand.

## The rule

> Every schema change must be reproducible, reversible where possible, and tested before deployment.

- **Reproducible** — the same migration produces the same schema in every environment.
- **Reversible where possible** — provide a downgrade path so changes can be rolled back.
- **Tested before deployment** — migrations are validated before they touch production (see [../01-architecture/deployment.md](../01-architecture/deployment.md)).

## Tooling

The core-backend foundation uses **Alembic** with async SQLAlchemy, tracking the declarative base defined for all ORM models (see [../01-architecture/project-structure.md](../01-architecture/project-structure.md), [schemas.md](schemas.md)).

## Conventions

- Migrations are **committed to version control** alongside the code that depends on them.
- They are **ordered and dependency-aware**, so a fresh database can be built from scratch by applying them in sequence.
- Migrations **run before rollout**, so application code never runs against an out-of-date schema (see [../01-architecture/deployment.md](../01-architecture/deployment.md)).

## Why

Schema is part of the contract between the code and the data. Managing it as versioned, tested artifacts is what keeps deployments safe and history reproducible (see [data-philosophy.md](data-philosophy.md)).
