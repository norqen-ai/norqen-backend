"""RQ3 — cost vs quality of adaptive evidence gathering.

The planner gathers evidence in priority order and stops when confident enough. Here we
reproduce that adaptive loop over history with cheap numeric signals and sweep the
stopping threshold. For each threshold we measure:
    cost    = average number of signals gathered per decision
    quality = directional accuracy of the aggregated call
A rising frontier means more evidence genuinely helps; a flat one means it does not
(and you should stop early to save tokens/₹). Leakage-safe: each signal sees data <= t.
"""
from __future__ import annotations

import numpy as np

from src.backtest.signals import sma_crossover, momentum, rsi_reversion

# (name, fn, reliability) in gather priority order
PRIORITY = [("sma_crossover", sma_crossover, 0.70),
            ("momentum", momentum, 0.60),
            ("rsi_reversion", rsi_reversion, 0.60)]


def _aggregate(items):
    """items: list of (direction, confidence, reliability) -> (direction, confidence)."""
    wsum = sum(rel * conf for _, conf, rel in items)
    if wsum == 0:
        return 0.0, 0.0
    d = sum(dr * rel * conf for dr, conf, rel in items) / wsum
    c = wsum / sum(rel for _, _, rel in items)
    signs = {1 if dr > 0 else -1 if dr < 0 else 0 for dr, _, _ in items}
    if len(signs - {0}) > 1:
        c *= 0.8
    return d, c


def adaptive_decision(df, threshold: float, budget: int = 3):
    items = []
    for _, fn, rel in PRIORITY[:budget]:
        dr, conf = fn(df)
        items.append((dr, conf, rel))
        d, c = _aggregate(items)
        if c >= threshold and len(items) >= 2:
            break
    d, c = _aggregate(items)
    return d, c, len(items)


def frontier(dfs, thresholds, budget: int = 3, warmup: int = 60):
    rows = []
    for th in thresholds:
        costs, correct = [], []
        for df in dfs:
            closes = df["Close"].values
            for t in range(warmup, len(df) - 1):
                d, c, cost = adaptive_decision(df.iloc[:t + 1], th, budget)
                if abs(d) < 0.15:
                    continue
                fwd = closes[t + 1] / closes[t] - 1
                costs.append(cost)
                correct.append(int(np.sign(d) == np.sign(fwd)))
        rows.append({"threshold": th,
                     "mean_cost": float(np.mean(costs)) if costs else float("nan"),
                     "accuracy": float(np.mean(correct)) if correct else float("nan"),
                     "n": len(correct)})
    return rows


def format_frontier(rows) -> str:
    out = ["COST-QUALITY FRONTIER (RQ3)", "=" * 52,
           f"{'stop threshold':>15}{'mean cost':>12}{'accuracy':>11}{'n':>10}"]
    for r in rows:
        out.append(f"{r['threshold']:>15.2f}{r['mean_cost']:>12.2f}{r['accuracy']:>11.1%}{r['n']:>10}")
    out.append("(cost rises with the threshold; if accuracy is flat, extra evidence isn't worth it.)")
    return "\n".join(out)
