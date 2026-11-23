# Policy-Conditioned Multi-Agent Trading — Code

A real, production-shaped vertical slice: **real market data → LLM specialist agents on a
LangGraph planner → quant risk-based sizing → deterministic risk veto → audit log**, plus a
**leakage-safe evaluation suite** (the research: RQ1 adherence, RQ2 calibration, RQ3 cost).

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then set LLM_PROVIDER=openai|gemini and the matching key (+ optional FINNHUB_API_KEY, FRED)
```

Without a key, everything still runs on real data using deterministic fallbacks; the key
activates the LLM agents. `.env` is gitignored — never commit keys.

## Two layers

| Layer | Question | Code |
|---|---|---|
| **L1 · Quant core** | is the trading sound? | `src/eval/quant.py` (IC, Sharpe/Sortino/Calmar/DD, VaR/CVaR), `src/core/sizing.py` (vol-target / Kelly), `src/backtest/` |
| **L2 · Agent trust** (novelty) | is the agent obedient / honest / efficient? | `src/eval/adherence.py` (RQ1), `calibration.py` (RQ2), `cost_quality.py` (RQ3) |

## Run it

```bash
# LIVE decision(s) on real data — the product
python3 run_live.py --ticker RELIANCE.NS --compare     # 4 mandates on ONE frozen bundle
python3 run_live.py --ticker NVDA --policy aggressive_growth

# RESEARCH read-outs (numeric signals; no LLM cost)
python3 score_adherence.py                              # RQ1: adherence + cross-policy divergence
python3 run_obedience.py --n-us 20 --n-nse 20           # obedience experiment: guarded vs LLM+rules vs LLM+text profile
python3 analyze_obedience.py logs/exp_obedience_<date>  # violation rates, CIs, US vs NSE, safety-engine vetoes, figures
python3 backtest_report.py --universe --limit 8         # quant backtest: Sharpe / IC per name
python3 validate_signals.py --limit 10                  # which signals have edge (IC)?
python3 calibrate_report.py --limit 10                  # RQ2: reliability curve, ECE, Brier, temperature
python3 cost_quality_report.py --limit 8                # RQ3: cost vs quality frontier

# tests
python3 tests/test_core.py            # 5 core invariants
python3 tests/test_quant_eval.py      # 4 quant/eval invariants
```

## Layout

```
config/policies/*.json     4 investor mandates (schema v1.1: + sizing_method, target_vol)
config/universe.json       frozen 20 US + 20 NSE research universe
src/core/       policy · schemas · sizing (vol-target/Kelly)
src/data/       providers (Yahoo/Finnhub swap) · market · news · resolver (name->ticker)
src/agents/     planner_graph (LangGraph) · llm (OpenAI wrapper) · planner (rule-based baseline)
src/tools/      registry — 5 real specialist agents (technical/price_predictor/news/fundamental/macro)
src/risk/       deterministic risk engine (absolute veto)
src/backtest/   leakage-safe engine + numeric signals
src/eval/       quant · adherence(RQ1) · calibration(RQ2) · cost_quality(RQ3)
src/audit/      decision log (JSONL) + frozen evidence bundles (with risk context)
```

Metric definitions are frozen in `../PREREGISTRATION.md`. Methodology + citations in
`../docs/strategic_reassessment/07_methodology_and_references.md`.

> Note: `run_demo.py` (fake-evidence stdlib demo) is kept only as an offline fallback; the real
> pipeline is `run_live.py`. Clear `logs/` before a clean experiment run.
