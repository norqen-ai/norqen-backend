# Dependency Rules

These rules make the architecture enforceable. A change that violates one of them is architecturally wrong, regardless of whether it "works."

## Layer direction

```
Allowed:    API → Application → Domain ← Infrastructure
```

- The **domain** is the center; it depends on nothing.
- **Application** depends on the domain.
- **API** depends on the application.
- **Infrastructure** depends on the domain's interfaces (ports) and implements them.

```
Forbidden:  Infrastructure → Domain (as a hard dependency of domain on infra)
```

The domain never imports infrastructure. Infrastructure implements domain-defined ports; the dependency arrow points *into* the domain via interfaces, never the reverse.

## Module rules

- **Agents cannot call brokers directly.** Execution flows only through the Execution Engine. See [../04-tools/broker-adapters.md](../04-tools/broker-adapters.md).
- **The planner cannot bypass risk.** Every decision passes through the Risk Engine. See [../06-risk/approval-flow.md](../06-risk/approval-flow.md).
- **Risk cannot modify planner state.** It returns a verdict; the planner decides what to do with it.
- **Broker adapters never contain business logic.** They only translate orders to a provider API.
- **Agents never communicate with one another.** All coordination is via the planner. See [../03-agents/coordination.md](../03-agents/coordination.md).

## Why enforce this

These constraints are the concrete, checkable form of the [core principles](../00-overview/core-principles.md). They guarantee safety (risk is unavoidable), explainability (the planner sees everything), and replaceability (infrastructure is swappable).
