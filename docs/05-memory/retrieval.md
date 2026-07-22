# Retrieval

The planner retrieves **only relevant memories**. Retrieval is the read path of the memory pipeline (see [memory-architecture.md](memory-architecture.md)).

## Signals

Relevance is judged on:

- **Semantic similarity** — vector closeness to the current query/context.
- **Task relevance** — fit to the current task, not just surface similarity.
- **Time decay** — newer memories weigh more (but old ones remain accessible — see [memory-lifecycle.md](memory-lifecycle.md)).
- **Confidence** — how reliable the memory is.
- **Historical usefulness** — whether this memory has helped before.

## The constraint

> Context size should remain bounded.

Retrieval never dumps everything similar into context. Candidates are ranked and only the top ones are injected (see [memory-ranking.md](memory-ranking.md)), and summarization compresses them when needed (see [../04-tools/memory-tools.md](../04-tools/memory-tools.md)).

## Flow

```
query/context → vector search → candidate memories → rank by signals → top-K → inject
```

Retrieval is exposed to the planner via the Memory Agent and memory tools (see [../03-agents/memory-agent.md](../03-agents/memory-agent.md)).
