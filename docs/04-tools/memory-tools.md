# Memory Tools

Tools that expose the memory subsystem as capabilities. Used mainly by the Memory Agent (see [../03-agents/memory-agent.md](../03-agents/memory-agent.md)).

## Capabilities

- Semantic search
- Reflection lookup
- Similar trade retrieval
- Context summarization

## The guiding constraint

> The planner retrieves only relevant memories to reduce context size.

Retrieval is ranked and bounded so the planner's context stays focused (see [../05-memory/retrieval.md](../05-memory/retrieval.md) and [../05-memory/memory-ranking.md](../05-memory/memory-ranking.md)).

## Notes

- **Backed by the vector DB + PostgreSQL** — embeddings for similarity, metadata for filtering (see [../05-memory/storage.md](../05-memory/storage.md)).
- **Summarization** compresses retrieved memories to fit context budgets without losing the essential lesson.
- These tools are read-oriented for the planner; memory *writes* happen through the memory lifecycle after reflection (see [../05-memory/memory-lifecycle.md](../05-memory/memory-lifecycle.md)).
