"""Backtest-friendly numeric signals: `signal(history_df) -> (direction, confidence)`.

`history_df` carries indicator columns (from market.add_indicators) and includes data
ONLY up to the decision day t (the engine guarantees this). Each signal reads the latest
row / recent window and returns direction in [-1,1] and an honest confidence in [0,1].

These mirror the live numeric tools but are cheap enough to run over full history, so we
can measure their real edge (IC) and calibration without any LLM cost. They are deliberately
simple and honest — most such signals are weak, which the metrics will show plainly.
"""
from __future__ import annotations

import numpy as np


def _conf(direction: float, lo: float = 0.3, span: float = 0.5, cap: float = 0.75) -> float:
    return float(min(cap, lo + abs(direction) * span))


def momentum(df):
    c = df["Close"].values
    if len(c) < 21:
        return 0.0, 0.0
    m = c[-1] / c[-21] - 1.0
    d = float(np.tanh(m * 5))
    return d, _conf(d)


def sma_crossover(df):
    r = df.iloc[-1]
    sma20, sma50 = r.get("ind_sma20"), r.get("ind_sma50")
    if sma20 is None or sma50 is None or np.isnan(sma20) or np.isnan(sma50) or sma50 == 0:
        return 0.0, 0.0
    d = float(np.tanh((sma20 - sma50) / sma50 * 12))
    return d, _conf(d)


def rsi_reversion(df):
    rsi = df.iloc[-1].get("ind_rsi14")
    if rsi is None or np.isnan(rsi):
        return 0.0, 0.0
    d = float(np.clip((50 - rsi) / 50, -1, 1))     # high RSI -> fade (mean reversion)
    return d, _conf(d, span=0.4, cap=0.6)


def combo(df):
    """Equal-weight blend of trend (SMA) + momentum — a plain multi-signal baseline."""
    parts = [sma_crossover(df), momentum(df)]
    d = float(np.mean([p[0] for p in parts]))
    c = float(np.mean([p[1] for p in parts]))
    return d, c


SIGNALS = {"momentum": momentum, "sma_crossover": sma_crossover,
           "rsi_reversion": rsi_reversion, "combo": combo}
