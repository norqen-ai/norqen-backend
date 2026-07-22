# Tool Observability

Every tool invocation is measured. This telemetry powers debugging, cost control, and the live registry that drives selection.

## Metrics tracked

- Success rate
- Failure rate
- Latency
- Timeouts
- Retries
- Cost
- Usage frequency

## How it is emitted

> Every tool invocation emits structured telemetry and events.

Telemetry is keyed by `name`, `capability`, `provider`, and `version` (see [tool-interface.md](tool-interface.md)) and carries the run's `correlation_id` so it can be tied back to a reasoning run (see [../07-api/observability.md](../07-api/observability.md)).

## What it feeds

- **The tool registry** — health, latency, and availability are updated from these metrics so selection reflects reality (see [tool-registry.md](tool-registry.md)).
- **Failure recovery** — repeated failures inform ret/reroute decisions (see [../02-runtime/failure-recovery.md](../02-runtime/failure-recovery.md)).
- **Optimization** — cost and usage frequency reveal where to cache or switch providers.

## Why

Tools are the boundary with the outside world; they are where cost, latency, and flakiness live. Measuring them thoroughly is what keeps adaptive tool selection honest.
