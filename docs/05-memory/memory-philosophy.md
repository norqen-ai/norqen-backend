# Memory Philosophy

> Memory is a first-class capability.

Norqen does not merely store conversations — it **accumulates experience**. Every completed reasoning cycle can improve future reasoning through structured memory.

## What this means

- Memory is a **capability**, exposed as tools and consulted like any other evidence source (see [../04-tools/memory-tools.md](../04-tools/memory-tools.md)).
- Memory is **structured**, not a transcript. Experiences are typed, embedded, ranked, and retrievable (see [memory-types.md](memory-types.md)).
- Memory is **selective**. Only relevant, high-value memories are injected into context, keeping reasoning focused (see [memory-ranking.md](memory-ranking.md)).

## Why it matters

Without memory, every reasoning run starts from zero. With it, Norqen:

- recognizes situations it has seen before,
- avoids repeating past mistakes (via reflection memory — see [reflection-memory.md](reflection-memory.md)),
- calibrates confidence using how similar past situations actually resolved (see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).

Memory is the mechanism behind the final step of the reasoning loop: **Learn** (see [../02-runtime/reasoning-loop.md](../02-runtime/reasoning-loop.md)).
