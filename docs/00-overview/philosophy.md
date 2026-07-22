# Philosophy

These beliefs are the "why" behind Norqen's design. Every architectural decision in the later sections should be traceable back to one of them.

## Core beliefs

- **The planner is non-deterministic.** It reasons about what to do next rather than following a fixed script. Two runs of the same goal may take different paths. See [../02-runtime/planner.md](../02-runtime/planner.md).
- **Evidence precedes decisions.** Norqen does not act on assumptions; it acts on gathered, sourced, timestamped evidence. See [../02-runtime/adaptive-evidence-acquisition.md](../02-runtime/adaptive-evidence-acquisition.md).
- **Confidence is earned, not assumed.** Confidence is computed from evidence quality, agreement, and history — never hard-coded. See [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md).
- **ML models are evidence providers, not decision makers.** A forecast is an input to reasoning, never a command to act. See [../04-tools/ml-tools.md](../04-tools/ml-tools.md).
- **Risk is deterministic and final.** The planner proposes; the Risk Engine decides. Probabilistic reasoning never enforces policy. See [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md).
- **Every action must be explainable.** If it cannot be explained, it should not happen.
- **Reflection is mandatory after execution.** Every executed decision produces a structured comparison of expected vs. actual outcome. See [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md).
- **Memory is a first-class capability.** Experience is captured, ranked, and reused, not discarded. See [../05-memory/memory-philosophy.md](../05-memory/memory-philosophy.md).
- **Everything is a tool.** Market data, indicators, ML, memory, and brokers all sit behind a uniform capability interface. See [../04-tools/tool-framework.md](../04-tools/tool-framework.md).
- **Every module is replaceable.** Clean and hexagonal architecture keep frameworks and providers behind interfaces. See [../01-architecture/clean-architecture.md](../01-architecture/clean-architecture.md).

## How to resolve a design conflict

When two goals collide, resolve in this order:

1. **Safety** — never bypass risk or compliance.
2. **Explainability** — never trade traceability for convenience.
3. **Correctness** — prefer accurate evidence over fast evidence.
4. **Performance** — optimize only within the bounds of the above.
