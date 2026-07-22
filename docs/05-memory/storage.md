# Storage

Memory is stored across three engines, each serving a distinct role (see [../08-data/database-architecture.md](../08-data/database-architecture.md)).

## Stack

| Engine | Stores |
| --- | --- |
| **PostgreSQL** | Memory metadata and relationships |
| **Vector Database** | Embeddings for semantic search |
| **Object Storage** | Large artifacts (raw payloads, reports) |

## Memory record shape

Every memory carries:

| Field | Purpose |
| --- | --- |
| `id` | Unique identifier (UUID). |
| `type` | Episodic / semantic / reflection / ... (see [memory-types.md](memory-types.md)). |
| `source` | Where it came from — planner, agent, reflection, execution, user. |
| `embedding` | Vector used for similarity retrieval. |
| `timestamp` | When it was created (drives time decay). |
| `confidence` | How reliable it is (feeds ranking and the confidence model). |
| `metadata` | Structured context for filtering and explanation. |

## Notes

- Metadata lives in PostgreSQL so memories can be filtered and joined; the embedding lives in the vector DB and is linked by `id`.
- Records track provenance and timestamps consistent with the data schemas guidance (see [../08-data/schemas.md](../08-data/schemas.md)).
- Retention and archival of memory follow the data retention policy (see [../08-data/retention.md](../08-data/retention.md)).
