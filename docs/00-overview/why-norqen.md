# Why Norqen

Traditional trading software follows fixed workflows. It calls the same APIs in the same order every time, regardless of what is actually uncertain.

**Norqen reasons instead.**

## The difference

A workflow engine asks: *"What is the next step in the script?"*

Norqen asks: *"What do I not yet know, and what is the single best way to find out?"*

Instead of calling every API in sequence, the planner:

- decides what information is missing,
- chooses the most valuable tool or specialist to close that gap,
- revises its plan as new evidence arrives,
- and stops only when it determines sufficient confidence has been achieved.

This makes Norqen an **autonomous reasoning system** rather than an automated workflow.

## Why this matters

| Fixed workflow | Norqen (adaptive reasoning) |
| --- | --- |
| Calls all tools every time | Calls only the tools that reduce uncertainty |
| Wastes cost and latency on irrelevant data | Spends budget where it changes the outcome |
| Fails hard when a step is unavailable | Reroutes to alternative tools or lowers confidence |
| Opaque "it ran the pipeline" | Explains *why* each step was taken |
| Static — never improves | Reflects and learns after every cycle |

## The trade-off we accept

Non-determinism makes the system harder to test and reason about than a static pipeline. We accept this cost because financial decisions are inherently uncertain, and we mitigate it with:

- **Deterministic guardrails** — the Risk Engine is fully deterministic (see [../06-risk/risk-engine.md](../06-risk/risk-engine.md)).
- **Full observability** — every step emits events and telemetry (see [../08-data/event-store.md](../08-data/event-store.md)).
- **Bounded loops** — explicit stopping conditions prevent runaway reasoning (see [../02-runtime/reasoning-loop.md](../02-runtime/reasoning-loop.md)).
