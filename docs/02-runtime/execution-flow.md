# Execution Flow

The full path a goal takes from arrival to a persisted lesson.

```
User Goal
   │
   ▼
Planner ─────────────┐
   │                 │ replan
   ▼                 │
Evidence Loop        │   (iterative: gather → score → update confidence)
   │                 │
   ▼                 │
Decision Candidate   │
   │                 │
   ▼                 │
Risk Engine          │
   │                 │
   ├── Approved ──► Execution Engine ──► Broker Adapter
   │
   └── Modify / Reject ──► Planner (replan) ───────────┘
   │
   ▼
Reflection
   │
   ▼
Memory Update
```

## Notes

- The **Evidence Loop** is the adaptive core (see [adaptive-evidence-acquisition.md](adaptive-evidence-acquisition.md)); it repeats until confidence is sufficient.
- A **Decision Candidate** is only a proposal. It has no effect until the Risk Engine approves it (see [../06-risk/approval-flow.md](../06-risk/approval-flow.md)).
- **Modify** and **Reject** both return control to the planner, which replans with the risk feedback as new evidence.
- **Execution** only ever reaches a broker via the Execution Engine — never directly from an agent or the planner (see [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md)).
- **Reflection** and **Memory Update** run after every execution, closing the learning loop (see [../03-agents/reflection-agent.md](../03-agents/reflection-agent.md)).

## Events along the way

Each stage emits an event — `PlannerStarted`, `EvidenceCollected`, `DecisionCreated`, `RiskApproved`/`RiskRejected`, `TradeExecuted`, `ReflectionCreated`, `MemoryUpdated` — for audit and replay (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).
