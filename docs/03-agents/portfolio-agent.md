# Portfolio Agent

Evaluates a candidate decision against the current portfolio so the planner knows whether it *fits*.

## Evaluates

- Current holdings
- Diversification
- Exposure
- Sector allocation
- Position concentration
- Capital availability

## How it works

The agent checks whether a proposed decision is consistent with portfolio objectives and current composition — surfacing concentration, overlap, or capital constraints as evidence for the planner to weigh.

## Tools it uses

- Portfolio/analytics tools — holdings, allocations, exposure metrics.
- Memory tools — portfolio memory and prior positioning (see [../04-tools/memory-tools.md](../04-tools/memory-tools.md)).

## Output

Structured portfolio-fit evidence: current exposures, the marginal impact of the candidate decision, and any concentration or capital flags.

## Boundary

This agent informs; it does not enforce. Hard portfolio limits are enforced deterministically by the Risk Engine's portfolio-risk checks (see [../06-risk/portfolio-risk.md](../06-risk/portfolio-risk.md)). Like all agents, it returns to the planner and never executes or contacts other agents (see [agent-framework.md](agent-framework.md)).
