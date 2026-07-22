# Fundamental Agent

Assesses the financial health and intrinsic characteristics of an instrument.

## Analyzes

- Financial statements
- Earnings
- Ratios
- Cash flow
- Valuation
- Growth
- Sector comparisons

## Tools it uses

- Market data tools — fundamentals, earnings, company metadata (see [../04-tools/market-data-tools.md](../04-tools/market-data-tools.md)).
- Memory tools — prior fundamental context on the same instrument (see [../04-tools/memory-tools.md](../04-tools/memory-tools.md)).

## Output

Structured fundamental evidence: computed ratios, valuation readings, growth and cash-flow observations, and peer/sector comparisons — each with its source and reporting period.

> The agent produces **evidence rather than buy/sell recommendations.**

## Boundary

Returns to the planner; never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
