"""Direction predictor tool (MALHAR). Requires: pip install xgboost scikit-learn pandas.

Contract with the platform: `predict(ticker)` returns an EvidenceItem whose
- direction  = 2*P(up) - 1        (so P(up)=0.74 -> +0.48)
- confidence = |2*P(up) - 1| mapped to [0,1] — HONEST, not inflated;
  calibration of this number IS research question RQ2.

Training rule (non-negotiable): walk-forward only. Never fit on data that is
after the prediction date. No shuffled cross-validation on time series, ever.
"""
from __future__ import annotations

from src.core.schemas import EvidenceItem

try:
    import numpy as np
    import pandas as pd
    from xgboost import XGBClassifier
    _HAS_DEPS = True
except ImportError:
    _HAS_DEPS = False

FEATURES = ["ind_sma20", "ind_sma50", "ind_ema12", "ind_ret1", "ind_vol20", "ind_rsi14"]


def make_dataset(df):
    """Features at day t predict direction of day t+1 close. Drops warm-up NaNs."""
    X = df[FEATURES].iloc[:-1]
    y = (df["Close"].shift(-1) > df["Close"]).astype(int).iloc[:-1]
    mask = X.notna().all(axis=1)
    return X[mask], y[mask]


class DirectionPredictor:
    def __init__(self):
        if not _HAS_DEPS:
            raise ImportError("run: pip install -r requirements.txt")
        self.model = XGBClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.05,
            subsample=0.9, eval_metric="logloss",
        )

    def walk_forward_fit(self, X, y, min_train: int = 250):
        """Fit on all rows before the last one; returns out-of-sample hit-rate
        over an expanding-window walk-forward pass (honest skill estimate)."""
        hits, total = 0, 0
        step = max(1, len(X) // 40)
        for split in range(min_train, len(X) - 1, step):
            self.model.fit(X.iloc[:split], y.iloc[:split])
            pred = self.model.predict(X.iloc[split:split + step])
            hits += int((pred == y.iloc[split:split + step].values).sum())
            total += len(pred)
        self.model.fit(X, y)  # final fit on everything for live use
        return hits / total if total else float("nan")

    def predict_evidence(self, ticker: str, X_latest) -> EvidenceItem:
        p_up = float(self.model.predict_proba(X_latest.iloc[[-1]])[0, 1])
        direction = 2 * p_up - 1
        return EvidenceItem(
            tool="price_predictor",
            kind="technical",
            ticker=ticker,
            summary=f"P(up tomorrow)={p_up:.2f} (XGBoost walk-forward)",
            direction=direction,
            confidence=abs(direction),
            reliability=0.7,
            cost_units=1.0,
        )
