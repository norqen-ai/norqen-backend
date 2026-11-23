"""Unit tests for the PIT outcome simulator (src/pit/outcomes.py) on synthetic bars.

Covers: gap through the stop / target at the open, same-day stop-and-target (stop fills first),
horizon exit, short side symmetry, costs, zero-size and WAIT, and split-adjusted prices.
Run:  .venv/bin/python -m pytest tests/test_pit_outcomes.py -q
"""
import pandas as pd
import pytest

import src.pit.data as data
import src.pit.outcomes as oc


def _install(bars, ticker="TEST", index_close=100.0):
    idx = pd.bdate_range("2025-01-02", periods=len(bars))
    df = pd.DataFrame(bars, columns=["Open", "High", "Low", "Close"], index=idx)
    df["Volume"] = 1
    flat = pd.DataFrame({"Open": index_close, "High": index_close, "Low": index_close, "Close": index_close,
                         "Volume": 1}, index=idx)
    data._PRICES = {ticker: df, "^GSPC": flat, "^NSEI": flat}
    for f in (oc._window, oc._index_ret, oc.trade_return):
        f.cache_clear()
    return str(idx[0].date())


def test_horizon_exit_long_and_costs():
    t = _install([(100, 100, 100, 100), (100, 101, 99, 100.5), (100.5, 102, 100, 101), (101, 103, 100.5, 102)])
    o = oc.trade_return("TEST", t, +1, 0, 0, 3)
    assert o["exit"] == "horizon" and o["gross"] == pytest.approx(0.02) and o["net"] == pytest.approx(0.02 - 0.0014)


def test_same_day_stop_and_target_stop_first():
    t = _install([(100, 100, 100, 100), (100, 110, 90, 100)])
    o = oc.trade_return("TEST", t, +1, 5, 5, 3)
    assert o["exit"] == "stop" and o["gross"] == pytest.approx(-0.05)


def test_gap_through_stop_fills_at_open():
    t = _install([(100, 100, 100, 100), (100, 101, 99, 100), (90, 91, 89, 90)])
    o = oc.trade_return("TEST", t, +1, 5, 20, 5)
    assert o["exit"] == "stop_gap" and o["gross"] == pytest.approx(-0.10)


def test_gap_through_target_fills_at_open():
    t = _install([(100, 100, 100, 100), (100, 101, 99, 100), (112, 113, 111, 112)])
    o = oc.trade_return("TEST", t, +1, 5, 10, 5)
    assert o["exit"] == "target_gap" and o["gross"] == pytest.approx(0.12)


def test_short_is_symmetric():
    t = _install([(100, 100, 100, 100), (100, 100.5, 94, 95)])
    o = oc.trade_return("TEST", t, -1, 3, 4, 3)          # short: target at 96 is hit first in the range
    assert o["exit"] in ("target", "stop")
    assert o["exit"] == "target" and o["gross"] == pytest.approx(0.04)


def test_wait_and_zero_size_give_zero():
    t = _install([(100, 100, 100, 100), (100, 101, 99, 100)])
    assert oc.evaluate("TEST", t, "WAIT", 5, 3, 6, 1)["pnl"] == 0.0
    assert oc.evaluate("TEST", t, "BUY", 0, 3, 6, 1)["pnl"] == 0.0


def test_pnl_scales_with_size():
    t = _install([(100, 100, 100, 100), (100, 102, 100, 102)])
    a = oc.evaluate("TEST", t, "BUY", 2, 0, 0, 1)["pnl"]
    b = oc.evaluate("TEST", t, "BUY", 4, 0, 0, 1)["pnl"]
    assert b == pytest.approx(2 * a)


def test_split_adjusted_prices_have_no_artificial_jump():
    # auto-adjusted series: a 2:1 split leaves no gap in the adjusted bars, so no spurious stop fires
    t = _install([(50, 50, 50, 50), (50, 50.5, 49.5, 50), (50.2, 50.6, 49.9, 50.4)])
    o = oc.trade_return("TEST", t, +1, 3, 0, 2)
    assert o["exit"] == "horizon" and o["gross"] == pytest.approx(0.008)
