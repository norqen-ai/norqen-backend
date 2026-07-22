# Reflection Memory

Reflection memories capture **lessons after execution**. They are produced by the Reflection Agent (see [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md)) and are the most directly actionable kind of memory.

## What they capture

- Incorrect assumptions
- Missing evidence
- Successful reasoning paths
- Failed strategies

## Why they are special

> These memories directly improve future planning.

Unlike episodic memory (what happened) or semantic memory (what is true), reflection memory encodes **what to do differently**. On future runs it:

- warns the planner away from assumptions that previously proved wrong,
- reminds it to gather evidence it once missed,
- reinforces reasoning paths that worked,
- and feeds the confidence model so similar setups are judged with hindsight (see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).

## Lifecycle

Created after every execution, embedded and stored like other memory (see [memory-architecture.md](memory-architecture.md)), and ranked highly when its lesson matches the current situation (see [memory-ranking.md](memory-ranking.md)).
