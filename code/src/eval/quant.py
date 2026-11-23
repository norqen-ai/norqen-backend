"""Industry-standard quantitative-finance metrics — the mathematical backbone.

This is the layer that answers "are the signals/decisions any good?" using the SAME
math quant funds use, not self-invented confidence. Two families:

  A. PERFORMANCE / RISK of a return stream (what a PM reports):
       Sharpe, Sortino, Calmar, CAGR, annualised vol, max drawdown, hit rate,
       Value-at-Risk (VaR) and Conditional VaR / Expected Shortfall (CVaR).

  B. SIGNAL QUALITY (what a quant researcher reports before trusting a signal):
       Information Coefficient (IC) — correlation of predicted direction with the
       REALISED forward return (Grinold & Kahn). Rank-IC, IC t-stat, IC-IR.
       An IC near 0 means the signal is noise; ~0.03-0.05 with a strong t-stat is real edge.

  C. RISK-BASED SIZING (replaces confidence x max_size):
       volatility targeting and the Kelly fraction — size from risk, not vibes.

Pure numpy/pandas; annualisation uses 252 trading days. No look-ahead inside any function.
"""
from __future__ import annotations

import numpy as np

TRADING_DAYS = 252


# ----------------------------- A. performance / risk ----------------------- #
def daily_returns(close) -> np.ndarray:
    c = np.asarray(close, dtype=float)
    return c[1:] / c[:-1] - 1.0


def cagr(returns) -> float:
    r = np.asarray(returns, float)
    if len(r) == 0:
        return float("nan")
    growth = np.prod(1 + r)
    return growth ** (TRADING_DAYS / len(r)) - 1


def ann_vol(returns) -> float:
    return float(np.std(returns, ddof=1) * np.sqrt(TRADING_DAYS)) if len(returns) > 1 else float("nan")


def sharpe(returns, rf_annual: float = 0.0) -> float:
    r = np.asarray(returns, float)
    if len(r) < 2 or r.std(ddof=1) == 0:
        return float("nan")
    excess = r - rf_annual / TRADING_DAYS
    return float(excess.mean() / r.std(ddof=1) * np.sqrt(TRADING_DAYS))


def sortino(returns, rf_annual: float = 0.0) -> float:
    r = np.asarray(returns, float)
    downside = r[r < 0]
    dd = downside.std(ddof=1) if len(downside) > 1 else 0.0
    if dd == 0:
        return float("nan")
    excess = r.mean() - rf_annual / TRADING_DAYS
    return float(excess / dd * np.sqrt(TRADING_DAYS))


def max_drawdown(returns) -> float:
    """Most negative peak-to-trough of the cumulative curve (a negative number)."""
    curve = np.cumprod(1 + np.asarray(returns, float))
    peak = np.maximum.accumulate(curve)
    return float((curve / peak - 1).min())


def calmar(returns) -> float:
    mdd = abs(max_drawdown(returns))
    return float(cagr(returns) / mdd) if mdd > 0 else float("nan")


def hit_rate(returns) -> float:
    r = np.asarray(returns, float)
    return float((r > 0).mean()) if len(r) else float("nan")


def var_historical(returns, alpha: float = 0.05) -> float:
    """Historical Value-at-Risk: the alpha-quantile daily loss (negative)."""
    r = np.asarray(returns, float)
    return float(np.quantile(r, alpha)) if len(r) else float("nan")


def cvar_historical(returns, alpha: float = 0.05) -> float:
    """Conditional VaR / Expected Shortfall: mean loss in the worst alpha tail."""
    r = np.asarray(returns, float)
    if not len(r):
        return float("nan")
    q = np.quantile(r, alpha)
    tail = r[r <= q]
    return float(tail.mean()) if len(tail) else q


def performance_summary(returns, rf_annual: float = 0.0) -> dict:
    return {
        "CAGR": cagr(returns), "ann_vol": ann_vol(returns),
        "Sharpe": sharpe(returns, rf_annual), "Sortino": sortino(returns, rf_annual),
        "Calmar": calmar(returns), "max_drawdown": max_drawdown(returns),
        "hit_rate": hit_rate(returns), "VaR_5%": var_historical(returns),
        "CVaR_5%": cvar_historical(returns), "n_days": len(returns),
    }


# ----------------------------- B. signal quality --------------------------- #
def _pearson(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _rank(x):
    order = np.argsort(np.argsort(np.asarray(x, float)))
    return order.astype(float)


def information_coefficient(signal, forward_return) -> dict:
    """IC of a predictive signal vs the realised forward return (aligned, same length).
    Returns Pearson IC, rank (Spearman) IC, sample size, and the IC t-statistic.
    |t| > ~2 => the signal's edge is statistically distinguishable from noise."""
    s, f = np.asarray(signal, float), np.asarray(forward_return, float)
    mask = np.isfinite(s) & np.isfinite(f)
    s, f = s[mask], f[mask]
    ic = _pearson(s, f)
    ric = _pearson(_rank(s), _rank(f))
    n = len(s)
    t = ic * np.sqrt(n - 2) / np.sqrt(1 - ic ** 2) if (n > 2 and abs(ic) < 1) else float("nan")
    return {"IC": ic, "rank_IC": ric, "n": n, "t_stat": t}


# ----------------------------- C. risk-based sizing ------------------------ #
def vol_target_size(realized_ann_vol: float, target_ann_vol: float = 0.15,
                    max_weight: float = 1.0) -> float:
    """Position weight so the position's volatility ~ target. Low-vol name -> bigger
    size, high-vol name -> smaller. This is how risk-parity / vol-target books size."""
    if realized_ann_vol is None or realized_ann_vol <= 0:
        return 0.0
    return float(min(max_weight, target_ann_vol / realized_ann_vol))


def kelly_fraction(mean_daily_ret: float, var_daily_ret: float, cap: float = 0.5) -> float:
    """Continuous Kelly optimal fraction = mean / variance (capped; 'half-Kelly' is common
    in practice for robustness). Positive edge -> positive fraction."""
    if var_daily_ret is None or var_daily_ret <= 0:
        return 0.0
    return float(max(-cap, min(cap, mean_daily_ret / var_daily_ret)))
