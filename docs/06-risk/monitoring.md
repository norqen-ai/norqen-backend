# Monitoring

Continuous visibility into the risk framework's behavior and the portfolio's risk posture.

## Metrics tracked

- Approval rate
- Rejection rate
- Policy violations
- Drawdown
- Exposure
- Risk latency

## The rule

> Expose metrics through dashboards and alerts.

Risk metrics are surfaced in real time so operators can see how the system is behaving and be alerted before conditions become critical.

## What the metrics reveal

- **Approval / rejection rates** — whether the planner is proposing sound decisions or repeatedly hitting limits.
- **Policy violations** — which rules are binding most often (a signal to revisit policy or planner behavior).
- **Drawdown / exposure** — the live risk posture; breaches can trip circuit breakers (see [circuit-breakers.md](circuit-breakers.md)).
- **Risk latency** — that validation stays fast enough to not bottleneck execution.

## Relationship to the rest of the system

Risk monitoring is part of overall observability; metrics carry correlation IDs and integrate with the platform's dashboards, logs, and traces (see [../07-api/observability.md](../07-api/observability.md), [../08-data/observability.md](../08-data/observability.md)). Critical thresholds feed incident response (see [incident-response.md](incident-response.md)).
