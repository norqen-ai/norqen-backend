"""Realised-outcome labeller for PIT decisions (pre-registered 2026-10-12, before any outcome
was computed; see PREREGISTRATION.md amendment A1).

A decision taken after the close of day t is entered at the OPEN of the next session and held
for the profile's horizon H (trading days). Exits are checked on daily bars:
  * a gap through the stop/target at the open exits at the open;
  * otherwise, if the day's range touches the stop, exit at the stop price; if both stop and
    target are touched the same day, the STOP is assumed to fill first (conservative);
  * otherwise exit at the close of day H.
Returns are net of round-trip costs (US 14 bps; NSE 36 bps incl. STT and stamp duty).
Excess return subtracts the region's index return over the same holding window (beta = 1).
P&L contribution to the portfolio = position_size_pct/100 * net return. WAIT/HOLD = 0.
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from src.pit import data
from src.pit.universe import INDEX, region

HORIZON = {"intraday": 1, "aggressive_growth": 5, "conservative": 20, "long_term": 40}
COST_RT = {"US": 0.0014, "IN": 0.0036}


@lru_cache(maxsize=None)
def _window(ticker: str, t: str, H: int):
    df = data.prices()[ticker]
    fut = df[df.index > pd.Timestamp(t)].iloc[:H]
    return (fut["Open"].to_numpy(), fut["High"].to_numpy(), fut["Low"].to_numpy(),
            fut["Close"].to_numpy(), tuple(fut.index))


@lru_cache(maxsize=None)
def _index_ret(reg: str, t: str, exit_day) -> float:
    df = data.prices()[INDEX[reg]]
    fut = df[df.index > pd.Timestamp(t)]
    if fut.empty:
        return 0.0
    o = float(fut["Open"].iloc[0])
    upto = fut[fut.index <= exit_day]
    c = float(upto["Close"].iloc[-1]) if len(upto) else float(fut["Close"].iloc[0])
    return c / o - 1


@lru_cache(maxsize=None)
def trade_return(ticker: str, t: str, side: int, stop_pct: float, tp_pct: float, H: int) -> dict:
    """Unit-size trade outcome. side=+1 long, -1 short. stop/tp in percent (<=0 means none)."""
    o, h, l, c, idx = _window(ticker, t, H)
    if len(o) == 0:
        return {"ok": False}
    entry = o[0]
    stop_px = entry * (1 - side * stop_pct / 100) if stop_pct > 0 else None
    tp_px = entry * (1 + side * tp_pct / 100) if tp_pct > 0 else None
    exit_px, reason, k = c[-1], "horizon", len(o) - 1
    for i in range(len(o)):
        if i > 0:                                   # gap through a level at the open
            if stop_px is not None and side * (o[i] - stop_px) <= 0:
                exit_px, reason, k = o[i], "stop_gap", i
                break
            if tp_px is not None and side * (o[i] - tp_px) >= 0:
                exit_px, reason, k = o[i], "target_gap", i
                break
        adverse = l[i] if side > 0 else h[i]
        favour = h[i] if side > 0 else l[i]
        if stop_px is not None and side * (adverse - stop_px) <= 0:
            exit_px, reason, k = stop_px, "stop", i
            break
        if tp_px is not None and side * (favour - tp_px) >= 0:
            exit_px, reason, k = tp_px, "target", i
            break
    raw = exit_px / entry - 1
    reg = region(ticker)
    idx_r = _index_ret(reg, t, idx[k])
    gross = side * raw
    cost = COST_RT[reg]
    return {"ok": True, "gross": gross, "net": gross - cost, "excess_net": side * (raw - idx_r) - cost,
            "exit": reason, "days": k + 1, "truncated": len(o) < H}


def pnl_bps(size_pct: float, outcome: dict, key: str = "net") -> float:
    """Contribution to portfolio return in basis points of equity."""
    return 0.0 if not outcome.get("ok") else size_pct / 100 * outcome[key] * 1e4


def evaluate(ticker: str, t: str, action: str, size_pct: float, stop_pct: float, tp_pct: float,
             H: int) -> dict:
    """Outcome of one decision (action/size/stop/tp). WAIT/HOLD or zero size -> zero P&L."""
    if action not in ("BUY", "SELL") or size_pct <= 0:
        return {"traded": False, "pnl": 0.0, "pnl_x": 0.0, "ret": np.nan, "ret_x": np.nan, "exit": "none"}
    side = 1 if action == "BUY" else -1
    out = trade_return(ticker, t, side, round(float(stop_pct), 4), round(float(tp_pct), 4), H)
    if not out.get("ok"):
        return {"traded": False, "pnl": 0.0, "pnl_x": 0.0, "ret": np.nan, "ret_x": np.nan, "exit": "nodata"}
    return {"traded": True, "pnl": pnl_bps(size_pct, out, "net"), "pnl_x": pnl_bps(size_pct, out, "excess_net"),
            "ret": out["net"], "ret_x": out["excess_net"], "exit": out["exit"], "truncated": out["truncated"]}
