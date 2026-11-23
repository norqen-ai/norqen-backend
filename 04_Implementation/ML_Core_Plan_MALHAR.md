# ML Core Plan — Malhar

**Your mission:** own the data pipeline and every numeric model — the tools the agents call —
plus, later, the calibration/evaluation analysis that is the ML-research heart of the paper (RQ2).
Starter code: `code/src/data/market.py` and `code/src/ml/predictor.py` (contracts documented inside).

**Prime directive:** every model is delivered as a *tool* returning an `EvidenceItem`
(direction ∈ [-1,1], honest confidence ∈ [0,1], reliability, cost). Never expose raw model
objects to the agent side. Never let confidence be cosmetic — RQ2 will check it against reality.

## Build order

### Phase A — data pipeline (weeks 1–2, target ~10 Aug)
- Venv, `pip install -r requirements.txt`.
- US OHLCV via yfinance (done in starter) → verify `add_indicators` on 5 tickers; store Parquet in `data/` (add DuckDB if useful).
- NSE: try `RELIANCE.NS`-style via yfinance first (already works with our fetcher); evaluate jugaad-data as backup. Pick ~20 US + ~20 NSE large-caps → commit as `config/universe.json`.
- News: pick ONE reliable free source to start (RSS from Reuters/ET Markets/Google News per ticker). Output: `list[{"ts", "title", "source"}]` per ticker per day. Omkar's News Agent consumes this raw — you don't score sentiment, his LLM does.
- Macro: FRED API for US rates/CPI; RBI/MOSPI equivalents can wait.
- Definition of done: one command refreshes all data for the whole universe without errors.

### Phase B — predictor tools (weeks 3–4, target ~24 Aug)
- Direction predictor (starter exists): validate walk-forward hit-rate on the universe. Expect ~50–55%; that's NORMAL and fine — the paper doesn't depend on alpha. Never use shuffled CV.
- Volatility estimator: rolling σ + optionally GARCH(1,1) (`statsmodels`/`arch`) → feeds position sizing and the regime detector.
- Regime detector: 2–3 state Gaussian HMM (`hmmlearn`) on returns+vol → EvidenceItem("regime": bull/bear/choppy + confidence).
- Position-size calculator: pure function `size(policy, confidence, volatility) -> pct` — this is code, not LLM; document the formula (e.g. confidence-scaled with vol dampening, capped by `policy.max_position_pct`).

### Phase C — paper-trading + NSE simulator (weeks 5–6, target ~7 Sep)
- Alpaca paper account: order submit/fill/portfolio wrapper (`PortfolioState` from `schemas.py`).
- NSE simulator: fills at next-day open with a fixed slippage assumption + brokerage; document assumptions (reviewers will ask).
- Nightly job: refresh data → run planner on universe → risk check → execute paper orders → log. This becomes the LIVE LOOP.

### Phase D — the evaluation toolkit = your research core (weeks 7–8, target ~21 Sep)
- Adherence scorer: reads `logs/decisions_*.jsonl`, checks each card against its policy's clauses → violations table. (Freeze metric definitions BEFORE the live loop starts — pre-registration.)
- Calibration notebook: reliability curves, ECE, Brier of `card.confidence` vs realised outcomes; then temperature scaling / conformal (netcal, MAPIE). This is RQ2 and overlaps your UncertaiNLP experience — own it end to end.
- Cost–quality curves: sweep `evidence_budget` on frozen bundles (with Omkar's cached LLM replay).

**🚨 Mid-October gate: the nightly live loop (your Phase C) is the single most calendar-critical artifact of the whole project.**

## Rules
- Timestamps UTC everywhere; every data row carries its fetch time (freshness feeds evidence scoring).
- No lookahead: any feature at time t uses only data ≤ t. Add a unit test asserting it.
- Keep every model CPU-trainable; no GPUs anywhere.
