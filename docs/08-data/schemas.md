# Schemas

Conventions for relational schemas in PostgreSQL.

## Rules

- **Use normalized relational schemas.** Model relationships explicitly; avoid duplicating data that can be joined.
- **Prefer UUID primary keys.** UUIDs avoid enumeration, ease distribution, and keep IDs stable across environments.
- **Track timestamps, versions, and provenance on important records.** Know *when* a record was created/updated, *which version* of it this is, and *where it came from*.

## Why these conventions

- **Auditability & reproducibility** — timestamps and provenance let past decisions be reconstructed from the exact data that produced them (see [data-philosophy.md](data-philosophy.md)).
- **Safe evolution** — versioned records and version-controlled migrations let schemas change without losing history (see [migrations.md](migrations.md)).
- **Consistency** — the same ID and timestamp conventions flow through domain entities and API models (see [domain-model.md](domain-model.md), [../07-api/schemas.md](../07-api/schemas.md)).

## Baseline columns

Important tables should include, at minimum:

- `id` (UUID, primary key)
- `created_at`, `updated_at` (timestamps)
- `version` (for records that evolve)
- provenance fields (source/origin) where the data comes from outside the system

## Implementation

In the core-backend foundation these conventions are captured in a shared declarative base / mixin used by all ORM models, with changes managed through Alembic (see [migrations.md](migrations.md), [../01-architecture/project-structure.md](../01-architecture/project-structure.md)).
