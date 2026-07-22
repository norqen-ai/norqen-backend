# Vector Storage

The vector database stores **embeddings** and powers semantic retrieval across the system.

## What is embedded

- Memories
- Reflections
- News
- Research
- Planner context

## What it enables

> Expose semantic retrieval APIs.

Vector search finds content by *meaning*, not keywords — the foundation of memory retrieval (see [../05-memory/retrieval.md](../05-memory/retrieval.md)) and the Memory Agent (see [../03-agents/memory-agent.md](../03-agents/memory-agent.md)).

## How it fits with the other stores

- **Vector DB** holds the embedding and an ID.
- **PostgreSQL** holds the corresponding metadata (type, source, confidence, timestamp) for filtering and joins (see [../05-memory/storage.md](../05-memory/storage.md)).
- **Object Storage** holds any large underlying artifact.

A retrieval typically does a vector similarity search, then enriches and filters results using PostgreSQL metadata, then ranks them (see [../05-memory/memory-ranking.md](../05-memory/memory-ranking.md)).

## Notes

- Embedding quality is measured and improved over time (see [../05-memory/memory-observability.md](../05-memory/memory-observability.md)).
- Introduced alongside the memory features, after the core-backend foundation (see [database-architecture.md](database-architecture.md)).
