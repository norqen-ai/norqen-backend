# Risk Philosophy

> The Planner proposes.
> The Risk Engine decides.

Risk management is **deterministic, explainable, and policy-driven**. No trade may bypass risk validation.

## Why deterministic

The planner is intentionally non-deterministic — it reasons under uncertainty. Risk is the opposite by design: given the same decision and the same policies, it always returns the same verdict. This separation is deliberate:

| Planner | Risk Engine |
| --- | --- |
| Probabilistic, adaptive | Deterministic, rule-based |
| Optimizes for good decisions | Guarantees safe decisions |
| Can be wrong | Must be predictable |
| Proposes | Disposes |

## The two-key rule

A decision executes only when **both** conditions hold:

1. The planner's confidence threshold is met (probabilistic — see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).
2. The Risk Engine approves (deterministic — see [risk-engine.md](risk-engine.md)).

Confidence alone never authorizes an action.

## Non-bypassable

Risk validation is a hard architectural boundary: the planner cannot skip it, agents cannot route around it, and the Risk Engine cannot be modified by the planner (see [../01-architecture/dependency-rules.md](../01-architecture/dependency-rules.md)). Every verdict is recorded with a structured explanation for audit.
