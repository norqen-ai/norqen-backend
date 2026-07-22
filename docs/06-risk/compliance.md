# Compliance

Configurable rules that enforce regulatory and user-defined restrictions, distinct from risk-limit policies.

## Rule types

- Restricted securities
- Jurisdiction rules
- User-defined restrictions
- Audit logging

## The rule

> Compliance decisions are recorded for traceability.

Every compliance evaluation — pass or block — is logged as an immutable record so the system can demonstrate *why* a trade was or was not permitted (see [../08-data/event-store.md](../08-data/event-store.md)).

## Where it fits

Compliance is part of deterministic risk validation. A decision that violates a compliance rule is rejected regardless of confidence or profitability (see [risk-engine.md](risk-engine.md), [risk-philosophy.md](risk-philosophy.md)).

## Notes

- **Configurable** — rules vary by user and jurisdiction and are applied per request.
- Compliance restrictions are separate from risk **policies** (exposure/limits — see [policy-framework.md](policy-framework.md)); both must pass.
- User-defined restrictions let a user exclude instruments or strategies they do not want, and those choices are honored deterministically.
