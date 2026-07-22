# LangGraph Runtime

LangGraph orchestrates the planner lifecycle as a **graph**: nodes do work, edges decide where to go next, and the graph loops until stopping conditions are satisfied.

## Nodes

- **Planner** — the central decision node; every loop returns here.
- **Specialist agents** — Technical, Fundamental, Macro, News, Quant, Portfolio, Risk, Reflection, Memory (see [../03-agents/README.md](../03-agents/README.md)).
- **Tool nodes** — invocations of capabilities in the tool layer (see [../04-tools/tool-framework.md](../04-tools/tool-framework.md)).

## Edges

- **Conditional** — the next node is chosen by the planner based on current state, not hard-wired.
- **Looping** — the graph is expected to revisit the planner many times per run.
- **Terminating** — execution ends only when stopping conditions are met (sufficient confidence, a resolved goal, a budget/step limit, or an unrecoverable failure).

## State

All nodes read from and write to a shared planner state object that persists across iterations (see [state-management.md](state-management.md)). Agents are stateless; the graph state is the single source of truth for a run.

## Why a graph

- Loops and conditional branching are first-class — a natural fit for adaptive reasoning.
- The graph is inspectable and streamable, so progress can be surfaced live (see [streaming.md](streaming.md)).
- Node failures are contained and recoverable rather than fatal (see [failure-recovery.md](failure-recovery.md)).

## Guardrail

The graph can *propose* decisions, but the edge from "decision" to "execution" always passes through the deterministic Risk Engine (see [execution-flow.md](execution-flow.md)).
