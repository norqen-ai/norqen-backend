# Tool Interface

Every tool exposes the same contract, so the planner can reason about any tool uniformly.

## Required metadata

| Field | Purpose |
| --- | --- |
| `name` | Unique identifier for the tool. |
| `description` | Human-readable summary of what it does. |
| `capability` | The abstract capability it fulfills (e.g. `market.history`). |
| `input schema` | Typed, validated inputs. |
| `output schema` | Typed, validated outputs. |
| `latency` | Expected/observed response time (feeds selection and SLAs). |
| `health` | Current availability status. |
| `timeout` | Maximum time before the call is abandoned. |
| `retry policy` | How transient failures are retried. |
| `confidence` | Reliability of the output, where applicable (e.g. ML tools). |
| `version` | Tool version, for reproducibility and auditing. |

## The selection rule

> The planner chooses tools based on **capability**, not implementation.

`capability` is what the planner matches against; the other fields (`health`, `latency`, `confidence`, ...) break ties between providers of the same capability (see [tool-selection.md](tool-selection.md)).

## Consistency guarantees

- **Typed I/O** — inputs and outputs are validated against their schemas before and after the call.
- **Bounded execution** — `timeout` and `retry policy` make every call predictable.
- **Observable** — every invocation emits telemetry keyed by `name`, `capability`, and `version` (see [observability.md](observability.md)).
