# Tool Registry

The registry is the **catalog** of every available tool. The planner queries it before selecting a tool, so choices are made from live metadata rather than hard-coded assumptions.

## Registry metadata

For each tool:

| Field | Use |
| --- | --- |
| `capability` | What the tool does — the primary match key. |
| `health` | Whether it is currently usable. |
| `average latency` | Expected responsiveness. |
| `provider` | Which backend implements it. |
| `cost` | Relative expense of an invocation. |
| `rate limits` | Remaining quota / throttling constraints. |
| `availability` | Uptime / current reachability. |

## How it is used

> The planner queries the registry before selecting tools.

```
capability needed → registry lookup → healthy candidates → selection → invoke
```

This makes provider fallback automatic: if the preferred provider is unhealthy or rate-limited, the registry surfaces alternatives with the same capability (see [tool-selection.md](tool-selection.md), [../02-runtime/failure-recovery.md](../02-runtime/failure-recovery.md)).

## Keeping it current

Health, latency, and availability are updated from the telemetry every invocation emits (see [observability.md](observability.md)), so the registry reflects reality, not just static configuration.
