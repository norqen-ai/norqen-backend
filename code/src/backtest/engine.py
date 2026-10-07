"""Leakage-safe daily backtester for a single name.

At each day t (>= warmup): the signal sees ONLY data up to t; we size the position with
the policy's real sizing (vol from a trailing window up to t), hold from t to t+1, realise
the next-day return, and charge transaction + slippage cost on the turnover. Every decision
is recorded with its realised outcome, so RQ2 (calibration) and IC drop out for free.

No look-ahead: signal(df[:t+1]); realised return uses close[t+1]/close[t]-1 (unseen by the
signal). Returns include costs. This is the honest engine the paper's numbers come from.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.core.sizing import position_size_pct, realized_ann_vol
from src.eval import quant


@dataclass
class BacktestResult:
    ticker: str
    policy_name: str
    signal_name: str
    decisions: list          # per-day dicts (date, direction, confidence, weight, fwd_return, correct, acted)
    strat_returns: np.ndarray
    performance: dict
    ic: dict
    n_days: int
    n_trades: int
    turnover: float


def run_backtest(df, policy, signal_fn, ticker="?", signal_name="signal",
                 cost_bps: float = 5.0, slippage_bps: float = 2.0,
                 warmup: int = 60, vol_window: int = 60) -> BacktestResult:
    closes = df["Close"].values
    dates = [str(d) for d in df.index]
    prev_w = 0.0
    strat, decs, tot_turnover = [], [], 0.0

    for t in range(warmup, len(df) - 1):
        direction, confidence = signal_fn(df.iloc[:t + 1])           # data <= t only
        vol = realized_ann_vol(closes[max(0, t + 1 - vol_window):t + 1])

        if confidence < policy.confidence_to_act or abs(direction) < 0.15:
            w, acted = 0.0, False
        else:
            mag = position_size_pct(policy, direction, confidence, vol) / 100.0
            w, acted = mag * (1 if direction > 0 else -1), True

        fwd = closes[t + 1] / closes[t] - 1.0
        turnover = abs(w - prev_w)
        tot_turnover += turnover
        cost = turnover * (cost_bps + slippage_bps) / 1e4
        strat.append(w * fwd - cost)                                 # decide at t, hold t->t+1, net of cost
        decs.append({"date": dates[t], "direction": direction, "confidence": confidence,
                     "weight": round(w, 4), "fwd_return": fwd,
                     "correct": (int(np.sign(direction) == np.sign(fwd)) if acted else None),
                     "acted": acted})
        prev_w = w

    strat = np.asarray(strat, float)
    dirs = np.array([d["direction"] for d in decs])
    fwds = np.array([d["fwd_return"] for d in decs])
    return BacktestResult(
        ticker=ticker, policy_name=policy.policy_name, signal_name=signal_name,
        decisions=decs, strat_returns=strat,
        performance=quant.performance_summary(strat),
        ic=quant.information_coefficient(dirs, fwds),
        n_days=len(decs), n_trades=sum(1 for d in decs if d["acted"]),
        turnover=round(tot_turnover, 2),
    )
