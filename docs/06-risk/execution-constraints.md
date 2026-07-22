# Execution Constraints

Pre-trade gating checks that must pass before an approved decision can be sent to a broker. These are the practical "can we actually do this right now?" checks.

## Checks

- Market open
- Instrument tradable
- Sufficient buying power
- Position limits
- Broker availability
- Order validity

## The rule

> Failures prevent execution.

If any constraint fails, the order does not go out. Depending on the failure, the planner may replan (e.g. wait for market open) or the decision is rejected (see [approval-flow.md](approval-flow.md)).

## Where it fits

Execution constraints are the last deterministic gate before the Execution Engine hands the order to a broker adapter (see [../04-tools/broker-adapters.md](../04-tools/broker-adapters.md)):

```
Approved Decision → Execution Constraints → Execution Engine → Broker Adapter
```

They complement policy checks (which govern *whether* a trade is allowed by rule — see [policy-framework.md](policy-framework.md)) by verifying *whether it can be placed* under current market and broker conditions.
