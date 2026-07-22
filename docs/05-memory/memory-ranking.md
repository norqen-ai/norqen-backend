# Memory Ranking

Ranking decides which retrieved memories actually make it into the planner's context. It is the gatekeeper that keeps context bounded and high-value.

## Ranking factors

- **Similarity** — semantic closeness to the current query/context.
- **Confidence** — how reliable the memory is.
- **Freshness** — recency, via time decay.
- **Frequency of use** — how often the memory has been retrieved.
- **Reflection score** — the weight of the lesson it carries (see [reflection-memory.md](reflection-memory.md)).
- **Planner feedback** — whether the planner found it useful before.

## The rule

> Only top-ranked memories are injected into planner context.

Retrieval produces candidates (see [retrieval.md](retrieval.md)); ranking narrows them to a small, high-value set that fits the context budget. Useful memories get reinforced, raising their future rank (see [memory-lifecycle.md](memory-lifecycle.md)).

## Why ranking matters

Injecting too much memory dilutes reasoning and inflates cost. Ranking ensures the planner sees the *most relevant* precedent and lessons — not everything that is merely similar.
