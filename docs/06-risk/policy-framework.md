# Policy Framework

Policies are the deterministic rules the Risk Engine enforces. They are **versioned and auditable**.

## Policy types

- Maximum portfolio exposure
- Per-position limits
- Sector limits
- Daily loss limits
- Maximum leverage
- Approved instruments
- Trading hours

## Versioned and auditable

> Policies are versioned and auditable.

- **Versioned** — every policy change produces a new version; the Risk Engine records which version validated each decision, so past verdicts remain reproducible.
- **Auditable** — policy changes and applications are logged as immutable records (see [../08-data/event-store.md](../08-data/event-store.md)).

## How policies are applied

The Risk Engine evaluates a candidate decision against the **currently active** policy set and returns APPROVE / MODIFY / REJECT with an explanation naming the policies involved (see [risk-engine.md](risk-engine.md)).

## Notes

- Policies are **deterministic** — no probabilistic evaluation (see [risk-philosophy.md](risk-philosophy.md)).
- Compliance rules are a related but distinct layer of restriction (see [compliance.md](compliance.md)).
- Policy limits are complemented by execution constraints (pre-trade gating — see [execution-constraints.md](execution-constraints.md)) and circuit breakers (automatic halts — see [circuit-breakers.md](circuit-breakers.md)).
