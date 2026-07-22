# Vision

Norqen is an **AI-native Financial Intelligence Operating System**.

It is not a trading dashboard.
It is not an LLM wrapper.
It is not a prediction engine.

Norqen continuously observes markets, plans investigations, gathers evidence, reasons over uncertainty, evaluates deterministic risk, executes when appropriate, reflects on outcomes, and learns over time.

## The reasoning loop

Everything Norqen does is an instance of a single loop:

```
Observe → Plan → Acquire Evidence → Reason → Risk → Execute → Reflect → Learn
```

- **Observe** — take in a goal, a market condition, or a scheduled trigger.
- **Plan** — decide what is unknown and what to investigate next.
- **Acquire Evidence** — call the tool or specialist that most reduces uncertainty.
- **Reason** — integrate new evidence and update confidence.
- **Risk** — submit any proposed decision to the deterministic Risk Engine.
- **Execute** — act only after risk approval.
- **Reflect** — compare expected vs. actual outcomes.
- **Learn** — persist lessons as memory that improves future loops.

## What "AI-native" means here

The intelligence is not a feature bolted onto a workflow — it *is* the runtime. The planner (an LLM-driven reasoner) decides the path through the system at run time. There is no fixed sequence of API calls. See [why-norqen.md](why-norqen.md) and [../02-runtime/planner.md](../02-runtime/planner.md).

## What Norqen is optimizing for

- **Explainability** — every decision can be traced to the evidence and reasoning behind it.
- **Auditability** — every action emits an immutable event (see [../08-data/event-store.md](../08-data/event-store.md)).
- **Safety** — no action reaches a broker without passing deterministic risk validation (see [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md)).
- **Continuous improvement** — reflection and memory make the system better with every cycle.
