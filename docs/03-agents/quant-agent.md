# Quant Agent

Applies quantitative and statistical methods to produce model-based evidence.

## Runs

- Factor analysis
- Statistical signals
- Regime detection
- Correlation analysis
- Portfolio metrics

## Relationship to ML

> ML models are **tools** that this agent may invoke.

Model outputs (forecasts, regime labels, anomaly scores) are treated as **evidence for the planner**, never as decisions (see [../04-tools/ml-tools.md](../04-tools/ml-tools.md) and [../00-overview/philosophy.md](../00-overview/philosophy.md)).

## Tools it uses

- ML tools — forecasting, regime detection, optimization, anomaly detection.
- Market data tools — the series these models run on.

## Output

Structured quantitative evidence: signal values, factor exposures, detected regimes, correlations, and the model/version and data window that produced them.

## Boundary

Returns to the planner; never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
