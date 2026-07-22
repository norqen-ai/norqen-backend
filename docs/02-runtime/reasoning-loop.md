# Reasoning Loop

The cognitive loop the planner runs. It repeats until a stopping condition is met.

```
Observe
  → Form Hypothesis
  → Estimate Uncertainty
  → Select Tool/Agent
  → Collect Evidence
  → Update Confidence
  → Replan
  → (loop back until confident enough)
  → Risk Evaluation
  → Execute
  → Reflect
  → Learn
```

## Step by step

| Step | What happens |
| --- | --- |
| **Observe** | Ingest the goal and current state. |
| **Form Hypothesis** | Propose what might be true and what a good decision could be. |
| **Estimate Uncertainty** | Identify what is unknown and how much it matters. |
| **Select Tool/Agent** | Choose the action that most reduces that uncertainty (see [../04-tools/tool-selection.md](../04-tools/tool-selection.md)). |
| **Collect Evidence** | Invoke the tool or agent and gather sourced, timestamped evidence. |
| **Update Confidence** | Recompute confidence from the new evidence (see [confidence-model.md](confidence-model.md)). |
| **Replan** | Decide whether to loop again or move on. |
| **Risk Evaluation** | Submit a candidate decision to the deterministic Risk Engine (see [../06-risk/approval-flow.md](../06-risk/approval-flow.md)). |
| **Execute** | On approval, place the order via the Execution Engine. |
| **Reflect** | Compare expected vs. actual outcome (see [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md)). |
| **Learn** | Persist lessons to memory (see [../05-memory/reflection-memory.md](../05-memory/reflection-memory.md)). |

## Stopping conditions

The loop between *Collect Evidence* and *Replan* exits when **any** of these holds:

- Confidence meets the planner-defined threshold for the goal.
- The goal is resolved or determined to be unactionable.
- A step/cost/time budget is exhausted.
- An unrecoverable failure occurs (see [failure-recovery.md](failure-recovery.md)).
