# Memory Types

Norqen keeps several distinct kinds of memory. Each has its own storage and retrieval strategy.

| Type | Holds | Detail |
| --- | --- | --- |
| **Episodic** | Specific past experiences — trades, decisions, evidence, outcomes | [episodic-memory.md](episodic-memory.md) |
| **Semantic** | Generalized knowledge — concepts, terminology, learned abstractions | [semantic-memory.md](semantic-memory.md) |
| **Reflection** | Lessons learned after execution | [reflection-memory.md](reflection-memory.md) |
| **User Preference** | Durable user-level context and constraints | — |
| **Portfolio** | Portfolio history and positioning context | — |
| **Market Knowledge** | Persistent facts about instruments and markets | — |

## Why separate types

Different memories answer different questions:

- *"Have I seen this exact situation before?"* → episodic
- *"What does this concept mean?"* → semantic
- *"What did I get wrong last time?"* → reflection
- *"What does this user want?"* → user preference

Separating them lets each be embedded, ranked, and decayed appropriately (see [memory-ranking.md](memory-ranking.md), [memory-lifecycle.md](memory-lifecycle.md)), and lets the planner retrieve the right *kind* of memory for the task at hand (see [retrieval.md](retrieval.md)).
