# Failure Recovery

A tool failure is a normal event, not a crash. The runtime is designed so that individual failures degrade gracefully instead of terminating reasoning.

## The rule

> Tool failures should not terminate reasoning.

## What the planner may do on failure

- **Retry** — transient errors, subject to the tool's retry policy (see [../04-tools/tool-interface.md](../04-tools/tool-interface.md)).
- **Choose an alternative tool** — switch to another provider with the same capability (see [../04-tools/tool-selection.md](../04-tools/tool-selection.md)).
- **Skip unavailable evidence** — proceed without it if the goal still allows.
- **Lower confidence** — reflect the missing evidence in the confidence estimate (see [confidence-model.md](confidence-model.md)).
- **Escalate to the user** — when no safe path forward exists.

## Everything is observable

Every failure becomes structured telemetry and an event, so failures are debuggable and measurable rather than silent (see [../04-tools/observability.md](../04-tools/observability.md), [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).

## Boundary with risk

Failure recovery governs the *reasoning* loop. It never relaxes safety: if degraded evidence leads to a decision, that decision still faces full deterministic risk validation, and hard failures (data-integrity issues, broker outages) can trip circuit breakers that halt execution entirely (see [../06-risk/circuit-breakers.md](../06-risk/circuit-breakers.md)).
