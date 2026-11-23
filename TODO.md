# Norqen backend — TODO

Agreed on 2026-11-06. The baseline is the prototype code on `be-final-year-project` (`code/`).
Sorted by priority: **P0** → **P1** → **P2** → **P3**. Finish a tier, or at least its blocking items, before moving on.

## Rule for adding any tool
Before integrating a tool, answer two questions: **what decision does it change, and how will we measure that it helped?**
If either answer is unclear, don't integrate it. Every tool gets a walk-forward test and a with/without comparison.

---

# P0: Foundation (do first, everything else depends on it)

## P0.1 Data
For every data point, store **when it became publicly known**, not only the date it describes (point-in-time). Check each source's free-tier limits and terms first.

- [ ] **Data store** with point-in-time timestamps (Postgres, or DuckDB to start), plus `pandera` checks for missing or wrong data.
- [ ] **Prices:** NSE bhavcopy archives (via `jugaad-data` / `nsepython`) and yfinance. Stooq / Tiingo as backups.
- [ ] **Fundamentals, point-in-time:**
  - US: SEC EDGAR XBRL company facts (has filing dates).
  - India: NSE/BSE quarterly filings.
  - Ask the PICT library about CMIE Prowess or WRDS access.
  - Stop using yfinance `.info` fundamentals in backtests: they're today's values, so they leak the future.
- [ ] **Historical news with timestamps:**
  - FNSPID (US, 1999–2023).
  - GDELT (India and recent news).
  - Finnhub / Alpha Vantage news APIs.
- [ ] **Macro:** FRED (US), RBI DBIE + data.gov.in / MOSPI (India), India VIX / Nifty / S&P index history.
- [ ] **Index membership history** to avoid survivorship bias: NSE index change circulars, `fja05680/sp500` for the S&P 500.
- [ ] **Corporate actions** (splits, dividends, bonus issues) and **market calendars** (NSE + US holidays, IST vs ET).

## P0.2 Outcome tracking
- [ ] A job that, after **1, 5 and 20 trading days**, fills in each decision's real return, whether the stop-loss or target was hit, and whether the call was right.
- [ ] Store outcomes next to decisions. The simulator, measuring system, calibration and XAI all depend on this.

## P0.3 Make the current pipeline good enough
- [ ] Apply the investor profile in the orchestrator and decision layer. Keep the analyst prompts neutral about risk; if they vary, vary only the time horizon.
- [ ] Log why the orchestrator called each ML tool, and keep that choice deterministic.
- [ ] Treat news headlines as untrusted LLM input (prompt injection): clean them up before they reach the LLM.
- [ ] Add portfolio-level checks to the risk engine: sector cap, total exposure, and use `position_pct_by_ticker`.
- [ ] Log the model version and data source on every decision.
- [ ] **Langfuse tracing** on every LLM call (analyst agents, news agent, decision proposals): store prompt, response, model version, token cost and latency, and tag each trace with the decision ID, ticker and profile. This is the base for the P1.4 LLM traces, cost metrics in the scorecard and the P2.4 LLM budget. Decide first: Langfuse Cloud free tier or self-hosted (check data and terms), and make sure raw headlines in traces are handled as untrusted input.
- [ ] Fix or drop the `intraday` profile: it relies on missing tools and doesn't fit daily data.
- [ ] Don't show confidence to users until it's calibrated.

---

# P1: Simulate, measure, explain

## P1.1 Our own simulator
One simulation engine that runs the **real agent pipeline** (not a separate copy) for both historical replay and live paper trading, so backtest and live behaviour can't drift apart. Replaces `src/backtest/engine.py` over time.

- [ ] **Market replay clock:** steps through trading days using only the point-in-time data store. Each step sees only data known at that moment (leakage-safe by construction).
- [ ] **Modes:**
  - historical replay of the full pipeline (LLM runs only after the model's knowledge cutoff)
  - fast numeric-signals-only replay
  - live paper trading on today's data
- [ ] **Order fill model:**
  - fill at the next day's open, not today's close
  - slippage
  - Indian costs: brokerage, STT, stamp duty, GST, exchange fees
  - US costs: commission, SEC/FINRA fees
- [ ] **Exits:** stop-loss and take-profit trigger from the day's high and low (wicks), with gap-downs filled at the open.
- [ ] **Paper portfolio:** cash, positions, P&L and daily P&L. This replaces the hardcoded `PortfolioState` and feeds the risk engine.
- [ ] **Multi-currency:** USD and INR positions with an FX rate.
- [ ] **Corporate actions and calendars** applied (from P0.1).
- [ ] **Scenario injection** for safety tests:
  - market crashes
  - gap-downs
  - missing or stale data
  - delayed news
  - headlines written to manipulate the LLM
- [ ] **Deterministic runs:** seeds, cached LLM responses and a recorded config, so any run can be replayed exactly.
- [ ] **Scheduler** (APScheduler): runs the live paper loop daily after market close.
- [ ] **Kill switch:** one flag that stops all new decisions immediately.

## P1.2 Universal measuring system (the Norqen scorecard)
One metrics layer that every run (simulator, experiments, live paper) writes to, so "how well are we doing?" always has the same answer in the same format. Builds on the existing `src/eval/`.

- [ ] **Decision quality:**
  - hit rate, IC / rank IC
  - returns vs benchmark (Nifty / S&P)
  - Sharpe, Sortino, max drawdown, VaR / CVaR
- [ ] **Honesty:** calibration (ECE, Brier, reliability curve) per tool, per profile, per model.
- [ ] **Obedience:** violation rate per profile clause, veto rate, act rate vs WAIT rate (so a do-nothing agent can't score well), and divergence between profiles.
- [ ] **Efficiency:** LLM cost in ₹ per decision, tokens, latency, evidence cost spent.
- [ ] **Robustness:** LLM consistency (how often the decision flips when the same input is run 5 times), scenario pass rate.
- [ ] **Data health:** freshness, missing-data rate, leakage-check results.
- [ ] **Per-tool contribution:** what each tool adds, from with/without runs and attribution.
- [ ] **Slicing:** every metric can be split by profile, market (US / NSE), regime, model, tool and time period.
- [ ] **Baselines always shown next to us:**
  - buy-and-hold
  - index
  - always-WAIT
  - logistic-regression baseline
  - single LLM without the multi-agent setup
- [ ] **Versioned results:** each run is tied to a git commit, model version, data snapshot and profile version, so results can be compared across versions.
- [ ] **Regression alerts:** flag when a change makes any key metric worse.
- [ ] **Scorecard view / dashboard** reading from this layer.

## P1.3 Test suite
Split the whole project's data **by time, never randomly**, with gaps between splits:
- **Develop:** e.g. 2015–2021. Fit models, try ideas, tune.
- **Validate:** e.g. 2022–2023. Choose the final settings.
- **Test:** e.g. 2024–2025. Lock settings in `PREREGISTRATION.md` first, run once, report.

Prefer walk-forward where possible. LLM parts are only tested on data after the model's knowledge cutoff, and **forward paper trading is the final exam**.

- [ ] **Unit tests:** sizing, risk checks, aggregation, profile validation.
- [ ] **Pipeline tests** with the LLM mocked, so runs are repeatable.
- [ ] Point `tests/test_core.py` at `PolicyPlannerGraph`, not the v0 `Planner`.
- [ ] **Golden replay tests:** a saved evidence bundle must produce the same decision as before.
- [ ] **Leakage tests:** no feature or signal reads data after day t.
- [ ] **Safety scenarios** (run through the simulator):
  - COVID crash (Feb–Apr 2020)
  - 2022 rate-hike bear market
  - Adani (Jan 2023)
  - SVB (Mar 2023)
  - India election-result day (4 Jun 2024)
  - plus gap-downs, missing or stale data, daily-loss breach, and headlines written to manipulate the LLM
- [ ] **Research evaluation** on the develop / validate / test split, reported through the scorecard.
- [ ] **Forward paper trading:** run continuously from now on.
- [ ] **LLM consistency:** same evidence run 5 times; check whether the decision flips.

## P1.4 Explainable AI: know where the app goes wrong and fix it
Goal: for any bad decision, be able to answer **which component caused it, and why**.

- [ ] **Decision trace:** log every LangGraph step:
  - the tool queue
  - each tool called, with its inputs, output and latency
  - why `route` stopped (confidence reached, budget spent, or queue empty)
  - the final mode
- [ ] **Evidence attribution:** aggregation is linear, so store each tool's exact share of the final direction and confidence (`d·r·c / Σ(r·c)`). Show "fundamental drove 60% of this BUY".
- [ ] **LLM traces:** store the full prompt and response (Langfuse, set up in P0.3), with cost and model version.
- [ ] **LLM explanations:** require the rationale to cite which evidence it relied on, and flag rationales that mention facts not in the evidence (hallucination check).
- [ ] **ML explanations:**
  - SHAP values for tree models
  - coefficients for the logistic regression baseline
  - log the top features for each prediction
- [ ] **Counterfactuals:** what would change the decision ("would be BUY if confidence ≥ 0.75", "vetoed only because the size was over 2%").
- [ ] **Risk explanations:** the risk engine already records veto reasons. Keep them structured (clause, value, limit).
- [ ] **Error analysis report:** using outcomes, group wrong decisions by tool, profile, regime, market and mode, and feed the results into the scorecard.
- [ ] **Decision Card view:** for each decision, show the evidence breakdown, the stop reason, binding clauses, the veto reason and the counterfactual.

---

# P2: Build out

## P2.1 ML tools, Phase 1
Each ML tool is a fixed script that the orchestrator decides when to run. It follows the existing tool contract (`tool(ticker) -> EvidenceItem`, or a risk number).

- [ ] **Volatility forecaster** (GARCH / HAR, `arch`): forecast 5–20 day volatility and feed it into position sizing and stop-loss. Replaces the 3-month realised volatility.
- [ ] **Confidence calibrator** (isotonic / Platt, `sklearn`; later `MAPIE`): make stated confidence honest (currently 73% stated vs 51% actual).
- [ ] **Regime detector** (HMM, `hmmlearn` on Nifty / S&P returns and volatility): label the market calm, choppy or crisis. The orchestrator uses the label to decide which tools to run and how strict to be.

## P2.2 Support for more than one LLM
- [ ] Wrap the LLM calls so you can swap OpenAI, Anthropic, Gemini or an open model through config. The research plan needs ≥3 model families.
- [ ] Cache LLM responses by input hash, so replays are cheap and repeatable.

## P2.3 Backend skeleton
- [ ] FastAPI app, config management, database layer with migrations (Alembic), consistent error handling.
- [ ] **API endpoints:**
  - request a decision
  - get a Decision Card
  - list decisions
  - see the explanation and trace
  - paper portfolio state
  - scorecard metrics
- [ ] Simple auth (the app isn't public yet).

## P2.4 Cost, reliability and reproducibility
- [ ] An LLM spending budget per day or run, with alerts.
- [ ] Rate limits, retries and timeouts for every data API.
- [ ] Docker setup so the whole team can run it the same way.
- [ ] **MLflow** for model versions, training windows and metrics.

## P2.5 Update the staging docs
- [ ] Fix or mark as outdated the parts that contradict decisions already made: ML stays in the backend, and the profile goes in the orchestrator rather than the analyst prompts.

---

# P3: Later / low priority

## P3.1 ML tools, Phase 2 (only after Phase 1 is proven)
- [ ] **Cross-sectional factor ranker** (`LightGBM`, walk-forward): add only if it beats the current signals on IC.
- [ ] **FinBERT news sentiment** (`ProsusAI/finbert`): a cheap, repeatable cross-check against the LLM news agent.

## P3.2 CI
- [ ] GitHub Actions: unit, pipeline, golden-replay and leakage tests on every PR.
- [ ] `ruff` + `mypy`.
- [ ] Protect `prod`: nothing merges without passing tests and a review.

## P3.3 Live data
- [ ] A proper NSE data source (Zerodha Kite / Upstox) for live data, in place of yfinance.

## P3.4 Research deliverables
- [ ] Freeze `PREREGISTRATION.md` before the test run.
- [ ] Release the frozen evidence bundles plus the scorer as a public benchmark.
- [ ] Track ICAIF / ICLR workshop deadlines.

## P3.5 Product and team
- [ ] User feedback on decisions ("wrong / confusing / useful"), fed into error analysis.
- [ ] Compliance basics:
  - a "research and education only, not investment advice" disclaimer on every Decision Card
  - a check of data-source terms of use
  - a decision on SEBI registration before anything goes public
- [ ] Team process:
  - owners (Omkar orchestrator, Malhar ML, Piyush full-stack)
  - branch strategy `staging` → `prod`
  - a weekly review of the scorecard and error analysis

---

## Not doing (for now)
- Anomaly detector: data checks (`pandera`) cover most of the benefit.
- Portfolio optimizer (`skfolio` / `PyPortfolioOpt`): use simple portfolio rules in the risk engine instead.
- Keep the logistic regression `price_predictor` as a **baseline** only. Park the XGBoost `src/ml/predictor.py`.
- No LSTM / transformer price predictors and no reinforcement-learning traders.
- No real-money execution.
