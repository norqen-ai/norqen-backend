# Agent Framework

Agents are **specialists, not autonomous systems**. Each one is an expert in a single domain that the planner consults for evidence.

## The contract

An agent:

1. **Receives an objective** from the planner (never from another agent).
2. **Gathers evidence** by invoking tools appropriate to its domain (see [../04-tools/tool-framework.md](../04-tools/tool-framework.md)).
3. **Produces structured output** — evidence with sources, timestamps, and (where applicable) confidence.
4. **Returns to the planner**, which decides what happens next.

## What agents never do

- **Never execute trades.**
- **Never bypass or enforce risk.**
- **Never communicate directly with one another.**
- **Never orchestrate** — they do not decide which agent or tool runs next.

All of the above belong to the planner. See [coordination.md](coordination.md) and [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md).

## Why specialists

- **Focus** — each agent reasons deeply about one domain and requests only the tools it needs.
- **Composability** — the planner mixes agents per goal instead of running a fixed panel every time.
- **Testability** — a stateless agent with a clear objective and structured output is easy to test in isolation.

## Statelessness

Agents hold no state between invocations. Everything they need is passed in by the planner, and everything they learn is returned as evidence. Shared state lives in the planner runtime (see [../02-runtime/state-management.md](../02-runtime/state-management.md)).
