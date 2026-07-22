# Execution Endpoints

Endpoints for placing and tracking orders. Execution is always gated by the Risk Engine.

## Examples

| Endpoint | Purpose |
| --- | --- |
| `POST /execution/paper` | Place a simulated order via the Paper Broker. |
| `POST /execution/live` | Place a live order via a broker adapter. |
| `GET /execution/orders` | List orders and their status. |
| `GET /execution/trades` | List filled trades. |
| `POST /execution/cancel` | Cancel a working order. |

## The hard gate

> Execution is allowed only after Risk Engine approval.

No request to these endpoints bypasses risk. A submitted decision runs through deterministic validation — policies, portfolio risk, execution constraints, compliance, and circuit-breaker state — and only an `APPROVE` verdict proceeds to a broker adapter (see [../06-risk/approval-flow.md](../06-risk/approval-flow.md), [../04-tools/broker-adapters.md](../04-tools/broker-adapters.md)).

## Paper vs. live

- **Paper** and **live** share the same contract and the same risk path; only the broker adapter differs (see [../04-tools/broker-adapters.md](../04-tools/broker-adapters.md)). This makes paper trading a faithful rehearsal of live behavior.

## Notes

- **Authenticated and authorized** — live execution in particular is gated by role (see [authentication.md](authentication.md)).
- **Rate-limited** — execution is an expensive, high-impact capability (see [rate-limiting.md](rate-limiting.md)).
- Every order, verdict, and fill emits events for audit (see [../01-architecture/event-driven-design.md](../01-architecture/event-driven-design.md)).
