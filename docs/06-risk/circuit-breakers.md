# Circuit Breakers

Automatic halts that stop execution when the system enters a dangerous state. They are the emergency brakes of the risk framework.

## Triggers

Execution is halted automatically on:

- Excessive drawdown
- Consecutive failures
- Extreme volatility
- Data integrity issues
- Broker outages

## The rule

> Circuit breakers require explicit recovery.

A tripped breaker does not reset itself. Execution stays halted until an operator (or a defined recovery workflow) explicitly clears it — this prevents the system from resuming into the same dangerous condition (see [incident-response.md](incident-response.md)).

## Relationship to other risk layers

- Policies and constraints validate **individual** decisions (see [policy-framework.md](policy-framework.md), [execution-constraints.md](execution-constraints.md)).
- Circuit breakers act at the **system** level, overriding everything and halting *all* execution when tripped.
- Breaker state is an input to the Risk Engine: while tripped, no decision can be approved for execution (see [risk-engine.md](risk-engine.md)).

## Observability

Trips, causes, and recoveries are recorded as immutable events and surfaced through monitoring and alerts (see [monitoring.md](monitoring.md)).
