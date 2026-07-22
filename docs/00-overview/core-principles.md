# Core Principles

These are the non-negotiable rules of Norqen. Code, reviews, and design decisions are measured against them. If a change violates one of these, the change is wrong.

1. **The planner is never deterministic.** It reasons; it does not follow a fixed script.
2. **Risk always has veto authority.** No decision reaches a broker without deterministic risk approval.
3. **Everything is a Tool.** Capabilities are exposed behind a uniform interface, independent of provider.
4. **Agents are specialists, not controllers.** They gather evidence and return it; they never orchestrate, execute, or talk to each other.
5. **FastAPI exposes capabilities, not CRUD.** The API lets clients ask Norqen to reason, analyze, and execute.
6. **LangGraph is the orchestration runtime.** The planner lifecycle runs as a graph with conditional edges and expected loops.
7. **Python is the primary backend language.** Async-first, strongly typed.
8. **Every decision is explainable.** Reasoning, evidence, and confidence are always recoverable.
9. **Every trade generates reflection.** Learning after execution is mandatory, not optional.
10. **Every module is replaceable.** Business rules never depend on frameworks or providers.

## Enforcement

These principles map to concrete, checkable boundaries in [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md):

- Agents cannot call brokers directly.
- The planner cannot bypass risk.
- Risk cannot modify planner state.
- Broker adapters never contain business logic.
- Infrastructure never depends on the domain.
