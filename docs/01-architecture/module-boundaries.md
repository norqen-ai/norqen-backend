# Module Boundaries

Each module owns one responsibility and nothing outside it. This is what keeps a modular monolith from decaying into a big ball of mud.

## Ownership

| Module | Owns | Never does |
| --- | --- | --- |
| **Planner** | Orchestration, task decomposition, tool/agent selection, stopping decisions | Execute trades, enforce risk policy |
| **Agents** | Domain-specific evidence gathering | Orchestrate, execute, or call each other |
| **Tools** | Providing capabilities behind a uniform interface | Decide what to do with their output |
| **Risk** | Deterministic validation of decisions | Modify planner state, place orders |
| **Execution** | Communicating with brokers | Make or override decisions |
| **Reflection** | Turning outcomes into lessons | Change past decisions |
| **Memory** | Storing and retrieving experience | Decide; it only informs |

## The principle

> No module owns responsibilities outside its domain.

## How boundaries are enforced

- **Coordination flows through the planner.** Agents never talk to each other; shared state lives in the planner runtime. See [../03-agents/coordination.md](../03-agents/coordination.md).
- **Capabilities are accessed as tools.** Modules request capabilities, not concrete providers. See [../04-tools/tool-framework.md](../04-tools/tool-framework.md).
- **Dependencies point one way.** The allowed and forbidden edges are listed in [dependency-rules.md](dependency-rules.md).
