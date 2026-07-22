# Retention

How long each kind of data is kept, and how it is archived or deleted. Retention is governed by explicit policy, not left to chance.

## Data with retention policies

- Market data
- Planner history
- Execution history
- Logs
- Embeddings

## The rule

> Support archival and deletion policies where required.

Each data type has its own policy balancing usefulness, cost, and compliance:

- **Archive** — move cold-but-valuable data to cheaper storage while keeping it accessible.
- **Delete** — remove data when policy or regulation requires it.

## Constraints from other parts of the system

- **Immutable records** (events, incidents) are archived, never edited or silently dropped (see [event-store.md](event-store.md), [../06-risk/incident-response.md](../06-risk/incident-response.md)).
- **Memory** decays in ranking but is retained until policy requires deletion (see [../05-memory/memory-lifecycle.md](../05-memory/memory-lifecycle.md)).
- **Compliance** may mandate both minimum retention (keep for N years) and deletion rights (see [../06-risk/compliance.md](../06-risk/compliance.md)).

## Notes

Storage growth is monitored so retention policies can be tuned before cost or performance becomes a problem (see [observability.md](observability.md)).
