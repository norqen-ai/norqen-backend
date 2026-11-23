"""Invariant tests for the quant + evaluation layer (no network)."""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd

from src.eval import quant, calibration
from src.core.sizing import position_size_pct
from src.core.policy import load_all_policies

POLS = load_all_policies("config/policies")


def test_quant_basics():
    r = np.array([0.001] * 100)                       # steady gains
    assert quant.max_drawdown(r) >= -1e-9             # no drawdown
    assert quant.sharpe(r) > 0
    sig = np.array([1, -1, 1, -1, 1, -1.0])           # perfectly correlated predictor
    fwd = sig * 0.02
    assert quant.information_coefficient(sig, fwd)["IC"] > 0.99


def test_sizing_caps_and_vol_response():
    p = POLS["conservative"]
    assert position_size_pct(p, 0.9, 0.9, 0.15) <= p.max_position_pct   # hard cap
    s_low_vol = position_size_pct(p, 0.3, 0.5, 0.30)
    s_high_vol = position_size_pct(p, 0.3, 0.5, 0.60)
    assert s_low_vol >= s_high_vol > 0                                  # lower vol -> bigger size
    # aggressive mandate takes >= risk of conservative for identical conviction
    assert (position_size_pct(POLS["aggressive_growth"], 0.5, 0.6, 0.40)
            >= position_size_pct(POLS["conservative"], 0.5, 0.6, 0.40))


def test_calibration_perfect_is_low_ece():
    conf = np.array([0.9] * 10 + [0.1] * 10)
    correct = np.array([1] * 9 + [0] + [0] * 9 + [1])   # 0.9-bin acc 0.9, 0.1-bin acc 0.1
    _, ece, _ = calibration.reliability(conf, correct)
    assert ece < 0.10


def test_backtester_leakage_safe_smoke():
    from src.data.market import add_indicators
    from src.backtest.engine import run_backtest
    from src.backtest.signals import combo
    rng = np.random.default_rng(0)
    close = 100 * np.cumprod(1 + rng.normal(0, 0.01, 300))
    idx = pd.date_range("2024-01-01", periods=300, freq="B")
    df = add_indicators(pd.DataFrame(
        {"Open": close, "High": close * 1.01, "Low": close * 0.99, "Close": close, "Volume": 1e6}, index=idx))
    res = run_backtest(df, POLS["long_term"], combo)
    assert res.n_days > 0 and np.isfinite(res.ic["IC"])
    assert res.strat_returns.shape[0] == res.n_days       # one return per decision, no extra


if __name__ == "__main__":
    tests = [test_quant_basics, test_sizing_caps_and_vol_response,
             test_calibration_perfect_is_low_ece, test_backtester_leakage_safe_smoke]
    ok = 0
    for t in tests:
        try:
            t(); print("PASS", t.__name__); ok += 1
        except Exception:
            print("FAIL", t.__name__); traceback.print_exc()
    print(f"{ok}/{len(tests)} passed")
    sys.exit(0 if ok == len(tests) else 1)
