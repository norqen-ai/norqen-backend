# Memory Observability

Memory performance is measured so it can be continuously improved. A memory system you cannot measure is one you cannot trust.

## Metrics tracked

- **Retrieval latency** — how fast relevant memories are returned.
- **Hit rate** — how often retrieval finds useful memories.
- **Memory usefulness** — whether injected memories actually helped the run.
- **Context contribution** — how much of the context budget memory consumes.
- **Embedding quality** — how well embeddings capture relevance.

## The principle

> Memory performance should be measurable and continuously improved.

## What these metrics drive

- **Usefulness** and **planner feedback** feed back into ranking (see [memory-ranking.md](memory-ranking.md)).
- **Hit rate** and **embedding quality** reveal when to re-embed or adjust retrieval signals (see [retrieval.md](retrieval.md)).
- **Context contribution** guards the context budget so memory never crowds out fresh evidence.

Metrics carry the run's `correlation_id` and are exposed alongside the rest of the system's observability (see [../08-data/observability.md](../08-data/observability.md)).
