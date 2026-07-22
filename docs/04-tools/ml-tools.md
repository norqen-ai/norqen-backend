# ML Tools

Machine-learning models exposed as tools. Used mainly by the Quant Agent (see [../03-agents/quant-agent.md](../03-agents/quant-agent.md)).

## Out of scope for this repository

**ML models are not implemented, trained, or served in this repo.** They live in a **separate repository/service** and are **fetched over an interface when needed**.

This repo owns only the **ML port and adapter stubs** — a uniform tool interface (see [tool-interface.md](tool-interface.md)) that the planner and agents call. Requests are routed to the external ML service; the model code, training, and serving are external. This keeps the reasoning backend independent of any specific model implementation (see [../00-overview/README.md](../00-overview/README.md), [../01-architecture/hexagonal-architecture.md](../01-architecture/hexagonal-architecture.md)).

## The defining rule

> ML models are **tools, not decision makers.**

A model's output is **evidence for the planner** — it never triggers an action on its own. This is a core principle of Norqen (see [../00-overview/philosophy.md](../00-overview/philosophy.md)).

## Examples

- Volatility prediction
- Regime detection
- Price forecasting
- Portfolio optimization
- Sentiment analysis
- Anomaly detection

## How outputs are treated

Each output becomes evidence carrying:

- the **model and version** that produced it (for reproducibility),
- a **confidence** where applicable (feeds the confidence model — see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)),
- the **input window** it was computed on.

## Notes

- ML tools obey the same interface as every other tool — health, latency, timeout, retry (see [tool-interface.md](tool-interface.md)).
- Because they are just tools, models can be swapped, versioned, or A/B compared without changing the planner or agents.
