# Database Architecture

Norqen uses several storage engines, each serving a distinct responsibility. There is no single database doing everything.

## Stack

| Engine | Responsibility | Examples |
| --- | --- | --- |
| **PostgreSQL** | Relational source of truth | Users, portfolios, positions, decisions, trades, planner history, memory metadata |
| **Redis** | Cache & ephemeral state | Quotes, indicators, planner sessions, rate-limit counters, refresh-token store |
| **Vector Database** | Embeddings | Memory, reflections, news, research (see [vector-storage.md](vector-storage.md)) |
| **Object Storage** | Large artifacts | Raw payloads, reports, model outputs |

## The principle

> Each storage engine serves a distinct responsibility.

Using the right engine for each job keeps queries fast, costs sane, and responsibilities clear:

- Relational integrity and transactions → PostgreSQL.
- Speed and expiry → Redis (see [caching.md](caching.md)).
- Similarity search → Vector DB.
- Big blobs → Object Storage.

## Access pattern

The domain talks to abstract repositories; these engines are infrastructure behind them (see [../01-architecture/clean-architecture.md](../01-architecture/clean-architecture.md)). This keeps the domain independent of any specific engine and makes each swappable.

## Foundation scope

The core-backend foundation starts with **PostgreSQL** (async SQLAlchemy 2.0 + Alembic) and **Redis**; the vector DB and object storage are introduced with the memory and artifact features (see [../00-overview/backend-master-prompt.md](../00-overview/backend-master-prompt.md)).
