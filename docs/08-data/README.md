# 08 - Data

Defines Norqen's **persistence, ingestion, and data architecture** — where every kind of data lives and how it flows.

## Reading order

1. [data-philosophy.md](data-philosophy.md) — data as a strategic asset
2. [database-architecture.md](database-architecture.md) — the storage engines and their roles
3. [domain-model.md](domain-model.md) — the core entities
4. [market-data-pipeline.md](market-data-pipeline.md) — ingesting external market data
5. [event-store.md](event-store.md) — immutable events for audit and replay
6. [vector-storage.md](vector-storage.md) — embeddings for semantic retrieval
7. [caching.md](caching.md) — Redis caching strategy
8. [schemas.md](schemas.md) — relational schema conventions
9. [retention.md](retention.md) — how long data is kept
10. [migrations.md](migrations.md) — version-controlled schema changes
11. [observability.md](observability.md) — data quality as an operational signal

## The storage map

| Engine | Role |
| --- | --- |
| PostgreSQL | Relational source of truth |
| Redis | Cache, rate limiting, ephemeral state |
| Vector DB | Embeddings for memory and search |
| Object Storage | Large artifacts |

Each engine has a distinct responsibility (see [database-architecture.md](database-architecture.md)). In the core-backend foundation, PostgreSQL (via async SQLAlchemy + Alembic) and Redis come first.
