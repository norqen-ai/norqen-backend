# Terminology

The shared vocabulary of Norqen. These terms have precise meanings throughout the docs and code; use them consistently.

| Term | Meaning |
| --- | --- |
| **Planner** | The non-deterministic reasoning brain. Owns orchestration, plans tasks, selects agents/tools, tracks confidence, and decides when to stop. See [../02-runtime/planner.md](../02-runtime/planner.md). |
| **Agent** | A stateless specialist (technical, fundamental, macro, etc.) that receives an objective, gathers evidence, and returns structured output. See [../03-agents/agent-framework.md](../03-agents/agent-framework.md). |
| **Tool** | A capability behind a uniform interface — market data, an indicator, an ML model, memory search, a broker. See [../04-tools/tool-framework.md](../04-tools/tool-framework.md). |
| **Capability** | *What* a tool does (e.g. "get market history"), independent of *which* provider implements it. |
| **Evidence** | A sourced, timestamped piece of information produced by a tool or agent that reduces uncertainty. |
| **Observation** | An input that triggers or informs reasoning — a goal, market event, or scheduled trigger. |
| **Confidence** | A dynamic estimate of how well-supported a decision is, derived from evidence, agreement, memory, and ML. See [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md). |
| **Task** | A unit of work the planner creates while decomposing a goal. |
| **Goal** | A user- or system-level objective the planner is trying to satisfy. |
| **Decision** | A candidate action (e.g. a proposed trade) produced by reasoning, before risk validation. |
| **Risk** | The deterministic authority that validates decisions and returns APPROVE / MODIFY / REJECT. See [../06-risk/risk-engine.md](../06-risk/risk-engine.md). |
| **Execution** | The act of sending an approved order to a broker adapter via the Execution Engine. |
| **Reflection** | The post-execution comparison of expected vs. actual outcome that produces lessons. See [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md). |
| **Memory** | Persisted, retrievable experience (episodic, semantic, reflection, and more). See [../05-memory/memory-types.md](../05-memory/memory-types.md). |
| **Policy** | A versioned, deterministic rule the Risk Engine enforces. See [../06-risk/policy-framework.md](../06-risk/policy-framework.md). |
| **Reasoning** | The overall Observe → … → Learn loop the planner runs. See [../02-runtime/reasoning-loop.md](../02-runtime/reasoning-loop.md). |
| **Workflow** | A fixed sequence of steps. Norqen deliberately avoids workflows in favor of reasoning. |
| **State** | The planner's working memory for a run: goal, tasks, active agents, evidence, confidence, decisions. See [../02-runtime/state-management.md](../02-runtime/state-management.md). |
| **Event** | An immutable record of something that happened, emitted for audit and replay. See [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md). |
