# Memory Architecture

Memory is produced by many parts of the system and flows through a single pipeline from raw experience to reusable context.

## Sources

Memory is created from:

- **Planner** — decisions, plans, and reasoning summaries.
- **Agents** — notable evidence and findings.
- **Reflection** — lessons after execution (see [reflection-memory.md](reflection-memory.md)).
- **Execution** — outcomes of trades.
- **User preferences** — durable user-level context.

## Pipeline

```
Event → Extract → Embed → Store → Index → Retrieve → Rank → Inject into Context
```

| Stage | What happens |
| --- | --- |
| **Event** | A source emits something worth remembering. |
| **Extract** | The salient content and metadata are pulled out. |
| **Embed** | Content is turned into a vector for similarity search. |
| **Store** | Metadata to PostgreSQL, vectors to the vector DB, large artifacts to object storage (see [storage.md](storage.md)). |
| **Index** | The vector is indexed for fast semantic retrieval. |
| **Retrieve** | Candidate memories are fetched for a query (see [retrieval.md](retrieval.md)). |
| **Rank** | Candidates are scored; only the best are kept (see [memory-ranking.md](memory-ranking.md)). |
| **Inject** | Top memories are added to planner context, within a bounded budget. |

## Notes

- The write path (Event → Store) is driven by events, so it is decoupled and auditable (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).
- The read path (Retrieve → Inject) is what the Memory Agent exposes to the planner (see [../03-agents/memory-agent.md](../03-agents/memory-agent.md)).
