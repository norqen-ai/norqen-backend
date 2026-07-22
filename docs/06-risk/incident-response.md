# Incident Response

The defined procedure when a critical failure occurs. The priority is always: stop, preserve, notify, record, recover.

## On critical failures

1. **Stop execution** — halt trading immediately (often via a circuit breaker — see [circuit-breakers.md](circuit-breakers.md)).
2. **Preserve evidence** — capture the state, decisions, and data that led to the incident.
3. **Notify operators** — alert the people who can act.
4. **Record incident** — write an immutable incident record.
5. **Enable recovery workflow** — provide a controlled, explicit path back to normal operation.

## The rule

> Risk incidents are immutable audit events.

Incident records cannot be altered or deleted. They form a permanent, auditable history of what went wrong and how it was handled (see [../08-data/event-store.md](../08-data/event-store.md)).

## Recovery

Because circuit breakers require **explicit** recovery, resuming execution is a deliberate operator action, not automatic — ensuring the underlying cause is understood and addressed before trading continues (see [circuit-breakers.md](circuit-breakers.md)).

## Relationship to monitoring

Monitoring detects the conditions that trigger incident response; incident response is what happens once a critical threshold is crossed (see [monitoring.md](monitoring.md)).
