# Macro Agent

Provides the macroeconomic backdrop against which specific decisions are evaluated.

## Evaluates

- Interest rates
- Inflation
- GDP
- Employment
- Central bank policy
- Commodity prices
- Currency markets

## Tools it uses

- Market data and macro data tools — economic indicators and series (see [../04-tools/market-data-tools.md](../04-tools/market-data-tools.md)).
- News tools — policy statements and macro events (see [../04-tools/news-tools.md](../04-tools/news-tools.md)).

## Output

Structured macro context: the current regime, notable shifts, and how they may bear on the goal — supplied to the planner as evidence, not as directives.

## Boundary

Returns to the planner; never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
