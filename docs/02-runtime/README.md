# 02 - Runtime

This folder specifies the **autonomous reasoning runtime** that powers Norqen — the planner, the graph it runs on, and the mechanics of evidence, confidence, state, streaming, and recovery.

## Reading order

1. [planner.md](planner.md) — the non-deterministic brain and its responsibilities
2. [langgraph-runtime.md](langgraph-runtime.md) — the graph that orchestrates the planner lifecycle
3. [adaptive-evidence-acquisition.md](adaptive-evidence-acquisition.md) — how Norqen decides what to investigate
4. [reasoning-loop.md](reasoning-loop.md) — the step-by-step cognitive loop
5. [state-management.md](state-management.md) — what the planner remembers within a run
6. [execution-flow.md](execution-flow.md) — the path from goal to executed trade
7. [confidence-model.md](confidence-model.md) — how confidence is computed
8. [streaming.md](streaming.md) — how progress reaches the UI in real time
9. [failure-recovery.md](failure-recovery.md) — how the runtime survives tool and node failures

## Mental model

The runtime is a **loop, not a pipeline**. The planner repeatedly asks "what is uncertain, and what is the best next action?", gathers evidence, updates confidence, and only exits the loop when a stopping condition is met — then hands any decision to the deterministic Risk Engine.
