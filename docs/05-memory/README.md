# 05 - Memory

This folder defines the **memory architecture** of Norqen — how the system accumulates experience and reuses it to reason better over time.

## Reading order

1. [memory-philosophy.md](memory-philosophy.md) — why memory is a first-class capability
2. [memory-architecture.md](memory-architecture.md) — sources and the memory pipeline
3. [memory-types.md](memory-types.md) — the kinds of memory Norqen keeps
4. [retrieval.md](retrieval.md) — how relevant memory is found
5. [storage.md](storage.md) — where memory lives and its shape
6. [reflection-memory.md](reflection-memory.md) — lessons from execution
7. [episodic-memory.md](episodic-memory.md) — specific past experiences
8. [semantic-memory.md](semantic-memory.md) — generalized knowledge
9. [memory-lifecycle.md](memory-lifecycle.md) — from creation to archival
10. [memory-ranking.md](memory-ranking.md) — which memories make it into context
11. [memory-observability.md](memory-observability.md) — measuring memory quality

## The core idea

Memory turns each completed reasoning cycle into an asset that improves the next one. Retrieval is always **ranked and bounded** so context stays focused (see [retrieval.md](retrieval.md), [memory-ranking.md](memory-ranking.md)).
