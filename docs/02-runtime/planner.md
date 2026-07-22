# Planner

The Planner is the **brain** of Norqen. Unlike a workflow engine, it is **non-deterministic**: it decides its next action by reasoning about the current state, not by following a fixed script.

## Responsibilities

- **Understand goals** — interpret what the user or system is asking for.
- **Break goals into tasks** — decompose a goal into investigable units.
- **Track uncertainty** — know what is unknown and how much it matters.
- **Choose the next best action** — pick the step that most reduces uncertainty.
- **Select agents and tools dynamically** — based on capability and health, at run time.
- **Replan continuously** — revise the plan as evidence arrives.
- **Decide when enough evidence exists** — apply stopping conditions and confidence thresholds.
- **Trigger execution** — submit a candidate decision to the Risk Engine, and execute only on approval.
- **Trigger reflection** — after execution, kick off the learning step.

## What the planner never does

- It **never follows a fixed sequence** of API calls.
- It **never executes trades directly** — execution flows through the Risk Engine and Execution Engine.
- It **never lets agents talk to each other** — it is the sole coordinator (see [../03-agents/coordination.md](../03-agents/coordination.md)).

## Inputs and outputs

- **Inputs:** the goal, planner state (see [state-management.md](state-management.md)), the tool registry (see [../04-tools/tool-registry.md](../04-tools/tool-registry.md)), and retrieved memory (see [../05-memory/retrieval.md](../05-memory/retrieval.md)).
- **Outputs:** evidence requests, agent objectives, candidate decisions, and streamed progress (see [streaming.md](streaming.md)).

## How it runs

The planner lifecycle is executed as a LangGraph graph with conditional edges and loops. See [langgraph-runtime.md](langgraph-runtime.md).
