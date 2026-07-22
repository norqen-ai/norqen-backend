# Confidence Model

Confidence is a **dynamic** estimate of how well-supported a decision is. It is computed from evidence — never assumed or hard-coded.

## Inputs

| Input | Contribution |
| --- | --- |
| **Evidence quality** | How complete, fresh, and precise the gathered evidence is. |
| **Source reliability** | How trustworthy the providers of that evidence are. |
| **Agreement between agents** | Whether specialists corroborate or contradict each other. |
| **Historical memory** | How similar past situations turned out (see [../05-memory/retrieval.md](../05-memory/retrieval.md)). |
| **ML outputs** | Model estimates, treated as evidence — not as decisions (see [../04-tools/ml-tools.md](../04-tools/ml-tools.md)). |

## How it is used

- It drives the **stopping condition**: the evidence loop continues until confidence meets the planner-defined threshold for the goal (see [reasoning-loop.md](reasoning-loop.md)).
- It is streamed to the UI as it changes (see [streaming.md](streaming.md)).
- It is recorded on the decision for explainability and later reflection.

## The hard boundary

> High confidence is necessary but **not sufficient** to act.

Execution occurs only after **both**:

1. planner-defined confidence thresholds are met, **and**
2. deterministic risk validation approves the decision (see [../06-risk/risk-philosophy.md](../06-risk/risk-philosophy.md)).

Confidence is probabilistic; risk enforcement is deterministic. The two are never conflated.
