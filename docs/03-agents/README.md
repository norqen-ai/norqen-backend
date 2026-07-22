# 03 - Agents

This folder specifies the **specialist agent framework** used by Norqen. Agents are the domain experts the planner consults; they gather evidence and return it, but they never orchestrate or act.

## Reading order

1. [agent-framework.md](agent-framework.md) — what an agent is and the rules all agents obey
2. [technical-agent.md](technical-agent.md) — price, trend, momentum, volatility
3. [fundamental-agent.md](fundamental-agent.md) — financials, valuation, growth
4. [macro-agent.md](macro-agent.md) — rates, inflation, policy, currencies
5. [news-agent.md](news-agent.md) — headlines, events, sentiment sources
6. [quant-agent.md](quant-agent.md) — factors, signals, regimes, correlations
7. [portfolio-agent.md](portfolio-agent.md) — holdings, exposure, fit
8. [risk-agent.md](risk-agent.md) — contextual risk evidence (not the deterministic engine)
9. [reflection-agent.md](reflection-agent.md) — post-execution learning
10. [memory-agent.md](memory-agent.md) — retrieval of relevant experience
11. [coordination.md](coordination.md) — how the planner coordinates all of them

## The one rule to remember

Agents are **specialists, not controllers**. They produce **evidence**, not commands. Every one of them returns to the planner, which owns all orchestration (see [coordination.md](coordination.md)).
