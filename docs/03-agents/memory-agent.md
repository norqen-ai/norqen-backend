# Memory Agent

Retrieves relevant historical experience so the planner can reason with hindsight instead of from scratch.

## Searches

- Similar trades
- Past reflections
- Historical outcomes
- Prior planner decisions

## How it works

The agent queries the memory subsystem and **returns only the most relevant memories** to keep the planner's context bounded (see [../05-memory/retrieval.md](../05-memory/retrieval.md) and [../05-memory/memory-ranking.md](../05-memory/memory-ranking.md)).

## Tools it uses

- Memory tools — semantic search, reflection lookup, similar-trade retrieval, summarization (see [../04-tools/memory-tools.md](../04-tools/memory-tools.md)).

## Output

A ranked, size-bounded set of memories with their type, source, timestamp, and relevance — ready to be injected into planner context.

## Boundary

Returns to the planner; never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
