# Adaptive Evidence Acquisition

Traditional systems call every tool, every time. Norqen calls only the tools that change the outcome.

## The questions the planner asks

Before every step, the planner asks:

1. **What information is missing?** — where is the current uncertainty?
2. **Which tool reduces uncertainty the most?** — what is the highest-value next action?
3. **Should another specialist be consulted?** — would a different agent's perspective help?

## The property that follows

Evidence collection is **iterative**, not a checklist:

```
identify gap → pick best action → collect evidence → update confidence → repeat or stop
```

The planner decides when confidence is sufficient rather than following a predefined list of steps. See [confidence-model.md](confidence-model.md) for how "sufficient" is measured, and [../04-tools/tool-selection.md](../04-tools/tool-selection.md) for how the "best" tool is chosen.

## Why this is better

- **Cost & latency** — budget is spent only where it matters.
- **Resilience** — if a tool is unavailable, the planner reroutes instead of stalling (see [failure-recovery.md](failure-recovery.md)).
- **Focus** — irrelevant data never dilutes the reasoning context.

## The trade-off

Adaptive acquisition means runs are not identical. Determinism is recovered downstream through the Risk Engine and full event-level auditability (see [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md), [../08-data/event-store.md](../08-data/event-store.md)).
