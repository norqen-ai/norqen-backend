"""RQ2 — is the stated confidence honest?

Given (confidence, correct) pairs — confidence in [0,1] read as P(the call is right),
correct in {0,1} — we compute the standard calibration diagnostics used across ML:

  * reliability curve : bin confidence, compare to empirical accuracy in each bin
  * ECE / MCE         : expected / maximum calibration error (Guo et al. 2017)
  * Brier score       : mean squared error of the probability (Brier 1950)
  * temperature scaling: fit one T that rescales confidence to minimise ECE

The pairs come from the leakage-safe backtester (acted decisions + realised outcome), so
this is a REAL calibration measurement — the same code later scores the LLM agent's
confidence. A model is well-calibrated when "70% confident" is right ~70% of the time.
"""
from __future__ import annotations

import numpy as np


def reliability(confidences, correct, n_bins: int = 10):
    conf = np.asarray(confidences, float)
    acc = np.asarray(correct, float)
    edges = np.linspace(0, 1, n_bins + 1)
    rows, ece, mce, N = [], 0.0, 0.0, max(1, len(conf))
    for i in range(n_bins):
        hi_incl = i == n_bins - 1
        m = (conf >= edges[i]) & ((conf <= edges[i + 1]) if hi_incl else (conf < edges[i + 1]))
        if m.sum() == 0:
            continue
        c, a, w = float(conf[m].mean()), float(acc[m].mean()), m.sum() / N
        ece += w * abs(a - c)
        mce = max(mce, abs(a - c))
        rows.append({"bin": f"{edges[i]:.1f}-{edges[i+1]:.1f}", "n": int(m.sum()),
                     "conf": c, "acc": a, "gap": a - c})
    return rows, ece, mce


def brier(confidences, correct) -> float:
    return float(np.mean((np.asarray(confidences, float) - np.asarray(correct, float)) ** 2))


def temperature_scale(confidences, correct, grid=None):
    """Grid-search a single temperature T on the confidence logits to minimise ECE.
    Returns (best_T, ece_after). T>1 shrinks overconfidence, T<1 sharpens."""
    conf = np.clip(np.asarray(confidences, float), 1e-4, 1 - 1e-4)
    y = np.asarray(correct, float)
    logit = np.log(conf / (1 - conf))
    grid = np.linspace(0.5, 3.0, 26) if grid is None else grid
    best_T, best_ece = 1.0, reliability(conf, y)[1]
    for T in grid:
        p = 1 / (1 + np.exp(-logit / T))
        ece = reliability(p, y)[1]
        if ece < best_ece:
            best_T, best_ece = float(T), float(ece)
    return best_T, best_ece


def calibration_report(confidences, correct) -> str:
    n = len(confidences)
    if n == 0:
        return "calibration: no acted decisions to score."
    rows, ece, mce = reliability(confidences, correct)
    b = brier(confidences, correct)
    T, ece_after = temperature_scale(confidences, correct)
    acc = float(np.mean(correct))
    out = [f"CALIBRATION (RQ2)  —  {n} acted decisions, base accuracy {acc:.1%}",
           "=" * 66,
           f"{'conf bin':<12}{'n':>6}{'mean conf':>11}{'accuracy':>11}{'gap':>8}"]
    for r in rows:
        out.append(f"{r['bin']:<12}{r['n']:>6}{r['conf']:>11.2f}{r['acc']:>11.2f}{r['gap']:>+8.2f}")
    out += ["-" * 66,
            f"ECE = {ece:.3f}   MCE = {mce:.3f}   Brier = {b:.3f}",
            f"temperature scaling: T*={T:.2f}  ->  ECE {ece:.3f} -> {ece_after:.3f}",
            "(gap>0: under-confident; gap<0: over-confident. Well-calibrated => gaps ~ 0, low ECE.)"]
    return "\n".join(out)
