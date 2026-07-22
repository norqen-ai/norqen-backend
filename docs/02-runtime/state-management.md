# State Management

The planner carries a single **state object** through the graph. It is the working memory of a reasoning run and the source of truth every node reads from and writes to.

## What planner state contains

| Field | Meaning |
| --- | --- |
| **Goal** | The objective being pursued. |
| **Tasks** | The decomposition of the goal into investigable units. |
| **Active agents** | Which specialists are currently engaged. |
| **Evidence** | All sourced, timestamped evidence collected so far. |
| **Confidence** | The current confidence estimate and its inputs (see [confidence-model.md](confidence-model.md)). |
| **Decisions** | Candidate decisions produced by reasoning. |
| **Memory references** | Retrieved memories injected into context (see [../05-memory/retrieval.md](../05-memory/retrieval.md)). |
| **Reflection context** | Data carried forward for post-execution reflection. |

## Properties

- **Persists across graph iterations.** State survives every loop of the LangGraph runtime (see [langgraph-runtime.md](langgraph-runtime.md)).
- **Agents are stateless.** They receive an objective and the relevant slice of state, and return output; they hold no state of their own (see [../03-agents/coordination.md](../03-agents/coordination.md)).
- **Bounded.** Context is kept within limits by retrieving only ranked, relevant memory (see [../05-memory/memory-ranking.md](../05-memory/memory-ranking.md)).
- **Auditable.** State transitions emit events so a run can be replayed and explained (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).

## Persistence

Ephemeral run state lives in Redis for speed; durable planner history is persisted to PostgreSQL for audit and later retrieval (see [../08-data/caching.md](../08-data/caching.md), [../08-data/retention.md](../08-data/retention.md)).
