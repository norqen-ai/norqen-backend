# Memory Lifecycle

Every memory moves through a lifecycle from creation to eventual archival.

```
Create → Embed → Store → Retrieve → Reinforce → Archive → Delete (if required)
```

| Stage | What happens |
| --- | --- |
| **Create** | A source emits an experience worth remembering (see [memory-architecture.md](memory-architecture.md)). |
| **Embed** | The content is vectorized for similarity search. |
| **Store** | Metadata, embedding, and artifacts are persisted (see [storage.md](storage.md)). |
| **Retrieve** | The memory is fetched when relevant to a query (see [retrieval.md](retrieval.md)). |
| **Reinforce** | Being useful raises its ranking signals (see [memory-ranking.md](memory-ranking.md)). |
| **Archive** | Rarely useful memories fade in ranking but remain stored. |
| **Delete** | Removed only when policy requires it (see [../08-data/retention.md](../08-data/retention.md)). |

## Decay, not deletion

> Old memories may decay in ranking but remain accessible.

Aging reduces a memory's retrieval priority (time decay — see [retrieval.md](retrieval.md)) without erasing it. This keeps the working set focused while preserving the full history for audit and rare-but-relevant recall. Hard deletion happens only to satisfy retention or compliance requirements.
