# Policy-Conditioned Multi-Agent Trading Agents

**Do LLM trading agents actually follow the investor's mandate — and is their confidence honest?**

Most "AI trading" systems are judged on one question: *did it make money?* That number is easy to
inflate and hard to trust. This project asks three different questions, and builds the tooling to
answer them on real market data:

1. **Obedience** — given the *same* market evidence, does the system behave differently for a
   cautious investor than for an aggressive one, and does it stay inside each one's stated limits?
2. **Honesty** — when the system says it is *76% confident*, is it right about 76% of the time?
3. **Efficiency** — does gathering more evidence actually improve the decision, or just cost more?

A team of LLM agents produces the decisions; a deterministic layer sizes and vetoes them; every
decision is logged with its full evidence so it can be replayed and scored.

> ⚠️ Research prototype. **Paper trading only — no real money, no brokerage execution.**
> Nothing here is investment advice.

---

## Current work: FinFM @ AAAI-27 short paper (deadline 20 Nov 2026 AoE)

**Team guide: [`TODO_FinFM_2027.md`](TODO_FinFM_2027.md)** — read it first. It covers what the paper is,
the gap, what's done, the code map, setup commands, each person's tasks, and the timeline.

*Fix What Is Checked, Inflate What Is Not: How LLM Trading Agents Respond to Investor-Mandate
Enforcement.* On 1,900 point-in-time cases (100 US + NSE large caps, Jan 2025–Jul 2026, after the
models' training cutoffs) we enforce investor mandates on the same LLM trade proposals in four ways
(block, LLM risk manager, deterministic repair, rule-engine feedback) and score each on real
outcomes. Main findings:
- Blocking and a standard-prompt LLM risk manager reach 0% violations by keeping 6.8% and 2.1% of
  the proposed trades; deterministic repair keeps 80.4%.
- Told the rule engine's rejection reasons, models fix size and stop and raise their stated confidence
  to the required bar in 92% of cases, vs 10% when the confidence rule is left out of the feedback
  (n = 2,570 per arm). Stated confidence doesn't rank outcomes (AUC 0.503).
- No return claim: the evidence signals are weak (IC between −0.07 and +0.05).

| Where | What |
|---|---|
| `paper_finfm/` · `paper_finfm_overleaf.zip` | the paper (AAAI-27 template, compile with **pdfLaTeX**) |
| `code/run_finfm_arms.py` | feedback arm, its control, LLM risk-manager re-test |
| `code/score_finfm_arms.py` | comparison tables for the new arms |
| `code/make_finfm_tables.py` | every table and number in the paper → `paper_finfm/tables/` |
| `code/logs/exp_pit_20261012/` | October run: frozen cases, 45,600 decisions, scored outcomes |
| `code/logs/finfm_2027/` | new-experiment outputs + `scores.txt` |

```bash
cd code && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python score_finfm_arms.py && .venv/bin/python make_finfm_tables.py   # no API key needed
```

> 🔒 This branch contains licensed news and price data and the LLM response cache. **Keep the repo
> private; never anonymise or publish this branch.** Code for reviewers goes in a separate code-only
> repo (guide, Section 7G).

---

## What it does

```bash
python3 run_live.py --ticker NVDA --compare
```

Fetches live data for NVIDIA, freezes one evidence bundle, then replays it under **four investor
profiles**. Real output:

```
risk context: realised annual vol = 41%
froze real evidence bundle (5 items) -> logs/bundles/bundle_NVDA_*.json

[conservative]       BUY   size=2.0%  stop=3.0%   conf=0.76   APPROVED
    why: strong profit margin and revenue growth indicate robust fundamentals
[long_term]          BUY   size=5.0%  stop=12.0%  conf=0.76   APPROVED
    why: strong company fundamentals combined with a favourable market trend
[aggressive_growth]  WAIT  size=0.0%              conf=0.48   APPROVED
    why: conflicting signals — technical uptrend tempered by weak news flow
[intraday]           WAIT  size=0.0%              conf=0.56   APPROVED
    why: signals conflict; a cautious approach is warranted
```

Same facts, four mandates, four different decisions — each with a plain-English reason, a
risk-based position size, and a full audit trail.

## How it works

```
                    investor profile (JSON: limits, priorities, confidence bar)
                                    │ governs everything below
   real market data  ──►  planner (LangGraph)  ──►  decision  ──►  risk engine  ──►  paper trade
   prices · news ·          gathers evidence          BUY/SELL/     deterministic,      + audit log
   fundamentals · macro     in the profile's          WAIT + size    no AI, can VETO          │
                            order, stops when                                                 ▼
                            confident enough                                    evaluation suite
                                    │                                        (obedience · honesty
                                    ▼                                            · efficiency)
                    5 evidence sources (4 LLM agents + 1 ML model)
```

**Evidence sources** — each returns a direction (−1…+1), an honest confidence (0…1) and a reliability weight:

| Source | Data | Type |
|---|---|---|
| `technical` | price history, SMA/RSI | LLM agent |
| `news` | live headlines | LLM agent |
| `fundamental` | margins, growth, valuation | LLM agent |
| `macro` | market-index trend | LLM agent |
| `price_predictor` | price history | logistic regression (no LLM) |

**Design rules**
- The LLM only ever produces a *judgement*. Every number that touches money — position size, stop
  loss — comes from code, never from the model.
- The risk engine is deterministic and contains **no AI**; it can veto any decision.
- Nothing is trusted because it sounds confident — confidence is measured (see below).

## Results on real data

Measured with the leakage-safe backtester (signals see only data up to the decision day; returns
are net of transaction costs and slippage):

| Finding | Result |
|---|---|
| **Simple signals are close to noise** | Momentum / SMA / RSI / combo across 8 large caps, 3 years: mean Information Coefficient ≈ **−0.02**, statistically significant in **0%** of names |
| **Stated confidence is over-confident** | At a stated **73%** confidence, real accuracy was **51%**. Calibration error **ECE 0.075 → 0.029** after temperature scaling |
| **More evidence didn't help (for these signals)** | As the stopping threshold rose, mean cost went **2.0 → 2.9** sources while accuracy stayed flat at **~50%** |
| **Mandates genuinely diverge** | On identical frozen evidence: **50%** of decision moments differed once size and stop-loss are counted; mean position-size spread **3.2%** |

These are deliberately unflattering numbers. Establishing that the cheap baselines are ~noise is
what makes the next experiment meaningful: **do the LLM agents beat a zero-edge baseline?**

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r code/requirements.txt
cp code/.env.example code/.env      # add OPENAI_API_KEY (optional: FINNHUB_API_KEY)
cd code
```

Runs **without** an API key using deterministic fallbacks on real market data; the key activates the
LLM agents.

```bash
# product
python3 run_live.py --ticker RELIANCE.NS --compare   # 4 profiles, one frozen evidence bundle
python3 run_live.py --ticker NVDA --policy conservative

# evaluation suite
python3 score_adherence.py            # obedience + cross-profile divergence
python3 backtest_report.py --universe --limit 8   # Sharpe / Information Coefficient
python3 validate_signals.py           # which signals actually have edge
python3 calibrate_report.py           # reliability curve, ECE, Brier, temperature scaling
python3 cost_quality_report.py        # cost vs quality frontier

# tests
python3 tests/test_core.py && python3 tests/test_quant_eval.py     # 9 tests
```

## Layout

```
code/
  config/policies/*.json   4 investor profiles (limits, priorities, confidence bar, risk budget)
  config/universe.json     frozen 20 US + 20 NSE research universe
  src/core/                policy schema · decision schemas · risk-based position sizing
  src/data/                provider layer (Yahoo/Finnhub) · news · symbol resolver
  src/agents/              LangGraph planner · LLM wrapper
  src/tools/               the 5 evidence sources
  src/risk/                deterministic risk engine (absolute veto)
  src/backtest/            leakage-safe backtester + numeric signals
  src/eval/                quant metrics · obedience · calibration · cost-quality
  src/audit/               decision log (JSONL) + frozen evidence bundles
PREREGISTRATION.md         metric definitions, frozen before large-scale runs
docs/                      methodology and references
```

Every decision is one line of JSONL containing the action, size, stop, confidence, **all evidence
used**, which profile clauses applied, the effort spent, and the risk verdict — so any result can be
recomputed from the log.

## Methodology

Two layers, kept separate on purpose:

- **Quant layer** (is the trading sound?) — Information Coefficient, Sharpe/Sortino/Calmar, max
  drawdown, VaR/CVaR, volatility-target and Kelly sizing.
  *Sharpe (1994) · Kelly (1956) · Grinold & Kahn · López de Prado (2018).*
- **Trust layer** (is the agent obedient, honest, efficient?) — obedience scoring, calibration
  (ECE/Brier/temperature scaling), cost–quality frontier.
  *Guo et al. (2017) · Brier (1950).*

Related agentic-finance work: TradingAgents (2412.20138), FinCon (NeurIPS 2024), FinAgent (KDD 2024),
StockBench (2510.02209). Full notes in [`docs/`](docs/strategic_reassessment/07_methodology_and_references.md).

## Status

**Working:** live multi-market data (any US/NSE ticker, or a company name), 4 LLM agents + ML model,
LangGraph planner, risk-based sizing, deterministic veto, audit log, leakage-safe backtester, the
full evaluation suite, 9 passing tests.

**Next:** replay the LLM agents across 3 years to measure their edge and calibration against the
baselines; over-fitting checks (Deflated Sharpe, PBO); multi-model comparison; continuous
paper-trading loop; web dashboard.

Final-year B.E. project, Dept. of E&TC, Pune Institute of Computer Technology — with a research
paper in preparation. Team: Malhar Inamdar, Omkar Joshi, Piyush Ochani.

## License

MIT — see [LICENSE](LICENSE).
