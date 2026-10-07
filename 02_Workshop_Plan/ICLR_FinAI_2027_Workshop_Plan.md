# ICLR 2027 FinAI Workshop — Complete Plan

**Status:** ACTIVE TARGET (decided 20 Jul 2026). Conference-paper work is out of scope until this ships — see `03_Conference_Stretch/`.

---

## 1. Target venue and dates

- **Primary: ICLR 2027 Workshop on Advances in Financial AI** (expected 3rd edition; the 2nd ran 27 Apr 2026 in Rio with organizers from RBC Borealis, UNIST, NVIDIA, JPMorgan — an audience that explicitly wants *agentic and responsible* finance work, not return-chasing).
  - CFP for the 2027 edition is **not out yet**. Expected deadline: **late Jan – Feb 2027** (the 2026 edition's was early Feb 2026). **Watch from Nov 2026:** https://sites.google.com/view/iclr2026finai/home + ICLR 2027 workshops page.
  - Format: short paper, typically 4–8 pages + appendix, non-archival.
- **Backup A:** AAAI-27 finance/FinAI workshop (AAAI-27 runs 16–23 Feb 2027, Montréal; workshop paper deadlines typically ~Oct–Nov 2026 — only if our results mature early).
- **Backup B:** FinNLP (joint NLP-finance workshop series, runs with ACL/EMNLP-family conferences).
- **Backup C:** ACM ICAIF 2027 (full conference, deadline ~Aug 2027) — this is the `03_Conference_Stretch` target anyway.

## 2. The idea (what we will claim)

**Research object = the agent system, not the market.** We build a multi-agent LLM trading
system in which the investor's mandate is a machine-readable *policy* (JSON: objective, risk
tolerance, horizon, sizing/drawdown limits, tool priorities, confidence threshold), and we answer:

- **RQ1 — Steerability.** Given *identical frozen evidence*, do the four policies (Aggressive Growth, Conservative, Long-Term, Intraday) produce measurably different, mandate-compliant behaviour — or does the system drift to one "average" behaviour? Metrics: violation rate per policy clause (sizing bound broken? horizon-inappropriate tool used?), cross-policy decision divergence, tool-selection divergence.
- **RQ2 — Confidence honesty.** When the system says "78% confident," is it right ~78% of the time? Metrics: reliability curves, ECE, Brier score; effect of post-hoc calibration (temperature scaling, conformal) on sizing and drawdowns.
- **RQ3 — Evidence efficiency.** Confidence-thresholded stopping vs. call-every-tool: decision quality per token/₹ across budget levels (cost–quality frontier).

Secondary (reported, never headlined): returns, Sharpe, max drawdown vs. baselines.

**Why this is defensible even if the strategy earns nothing:** the claims are about obedience,
honesty, and efficiency of the agent system — valid regardless of market outcome. This also
sidesteps the contamination critique that invalidates most published backtests (Gao et al. 2025).

## 3. Novelty positioning (what reviewers will check)

| Neighbour | What it does | Our difference |
|---|---|---|
| TradingAgents / FinCon / FinAgent / FinMem | Agent teams maximizing returns | One fixed goal; no policy input; contaminated eval |
| StockBench / Agent Market Arena / LiveTradeBench | Clean live benchmarks | Only ask "who earns" — never "who obeyed" |
| **FinPersona-Bench (Jun 2026)** ⚠️ | Shows ONE mandate erodes over TIME | We compare MANY mandates on IDENTICAL evidence (cross-sectional); we also replicate their drift finding in our live run — cite as motivation, differentiate explicitly |
| **CLQT (Jun 2026)** ⚠️ | Cost-aware diagnostic benchmark | No policy-conditioned planner, no calibration, no live run, no India |
| Calibrate-Then-Act / BATS | When agents should stop gathering info | Never instantiated in a trading loop |
| Persona-collapse repair (Jul 2026) | Fixes drift in *advice chat* | Not an agentic trading system |

⚠️ = closest concurrent work; the intro MUST cite and differentiate both, or a reviewer will do it for us.

**Unique combination we own:** policy-conditioned planner + adherence measurement + calibration + cost analysis + contamination-free live evaluation + first NSE (Indian market) track.

## 4. System to build (detailed architecture)

See `architecture_detailed.png` (full version — the synopsis carries the simplified one).

Components (build in this order):
1. **Data pipeline** — OHLCV + indicators (yfinance/Alpaca for US; jugaad-data/nsepy for NSE), news (NewsAPI/RSS), macro (FRED). Validation + timestamping of every item.
2. **Policy schema + 4 canonical policies** (JSON). Freeze v1.0 of the schema and the *metric definitions* BEFORE live logging starts (pre-registration — protects against "you defined the metric to look good").
3. **Orchestrator/planner** (LangGraph) — policy-conditioned; adaptive loop: assess gaps → select tool/agent → collect → validate → stop when confidence ≥ policy threshold or budget exhausted.
4. **4–6 specialist agents** — technical, news, fundamental, macro (+quant if time). Keep prompts in version control; every prompt logged.
5. **ML tool layer** — XGBoost price/volatility predictors, HMM regime detector, position-size calculator. Numbers come from code, never from the LLM.
6. **Risk engine** — deterministic rules (max daily loss, drawdown, position/sector limits, liquidity). Absolute veto. No AI inside.
7. **Paper execution** — Alpaca paper API (US) + custom NSE simulator. NO REAL MONEY, ever.
8. **Logging/replay layer** — every decision moment snapshotted as a frozen *evidence bundle* → deterministic replay under any policy. This is simultaneously our experiment harness and a future public benchmark. Non-negotiable, built from day one.
9. **Memory** — Postgres + pgvector (episodic trades, semantic notes). Keep simple; not our novelty.

### Policy schema (v0 sketch)
```json
{
  "policy_name": "conservative",
  "objective": "protect_capital",
  "horizon": "weeks_to_months",
  "max_position_pct": 2,
  "max_daily_loss_pct": 1,
  "stop_loss_pct": 3,
  "confidence_to_act": 0.75,
  "tool_priorities": ["fundamental", "macro", "news"],
  "forbidden_evidence": ["order_book", "intraday_momentum"],
  "evidence_budget": 10
}
```

### Software stack (moved here from synopsis per Turuk ma'am)

| Category | Tools | Purpose |
|---|---|---|
| Language | Python 3.11+ | everything |
| Orchestration | LangGraph | planner graph, agent routing, adaptive loop |
| LLMs | Claude/GPT APIs + one open-weight (Llama/Qwen via Ollama) | agents; ≥3 models for generality |
| Classical ML | XGBoost, scikit-learn, hmmlearn, statsmodels, PyTorch | predictors, regime detector |
| Data | yfinance, Alpaca, jugaad-data/nsepy, NewsAPI/RSS, FRED | market/news/macro |
| Execution | Alpaca paper API; custom NSE sim | paper trading only |
| Storage | PostgreSQL + pgvector; Parquet/DuckDB | memory, logs, evidence bundles |
| Replay/backtest | custom frozen-evidence harness; vectorbt | experiments, baselines |
| Calibration/stats | netcal, MAPIE, SciPy | ECE/Brier, conformal, significance tests |
| Tracking | MLflow or W&B; GitHub | reproducibility |
| Ops | Docker, Ubuntu VM (8 vCPU/16 GB), cron/systemd | 24×7 live loop |
| Dashboard | Streamlit | monitoring decisions/vetoes |
| Budget | ~₹2,500/month API cap | enforced by evidence-budget design |

## 5. Evaluation protocol

1. **Frozen-evidence replay (RQ1 core):** ~500+ decision moments, each replayed under all 4 policies × ≥3 repeats (LLM outputs vary run-to-run) × ≥3 models. Score adherence per clause; measure cross-policy divergence.
2. **Post-cutoff replay:** historical experiments only on market data AFTER each LLM's training cutoff. Document each model's cutoff explicitly in the paper.
3. **Live paper trading:** ≥4 months, ~20 US + ~20 NSE large-caps, continuous. Everything logged.
4. **Baselines:** buy-and-hold; momentum rule; mean-reversion rule; single-agent LLM (one prompt, no team); policy-blind ablation (same system, policy removed).
5. **Ablations:** no risk engine; no adaptive loop (call-everything); each specialist agent removed one at a time (if time permits).
6. **Statistics:** report every rate with 95% confidence intervals (bootstrap over decisions); paired comparisons (same evidence bundle with/without X); state number of decisions everywhere. Never claim a returns difference is significant — 4 months is too short; that's deliberate and stated openly.

## 6. Experiments for the workshop paper (scoped)

- **E1 (RQ1):** adherence + divergence table across 4 policies × 3 models. *The headline.*
- **E2 (drift check):** does adherence decay over the live months? (Replicates FinPersona-Bench's erosion finding in a full trading system — confirmation in a new setting is a valued contribution.)
- **E3 (RQ2):** reliability curves before/after calibration; impact on sizing/drawdown.
- **E4 (RQ3):** cost–quality frontier across evidence budgets.
- **E5 (secondary):** financial metrics vs. baselines, clearly labelled underpowered.
- **Stretch (only if ahead of schedule):** one simple fix — deterministic clamp of sizing/stops to policy bounds + policy re-injection per decision — before/after violation rates. (Full fix study belongs to the conference stretch.)

## 7. Month-by-month timeline

| Month | Deliverable |
|---|---|
| **Aug 2026** | Synopsis signed/submitted; name decided; repo + data pipeline running; policy schema v1.0 + metric definitions FROZEN and committed (pre-registration) |
| **Sep 2026** | Planner + 4 agents + ML tools + risk engine working end-to-end on US data; replay harness stores evidence bundles |
| **Mid-Oct 2026** | 🚨 HARD GATE: live paper-trading loop running 24×7 on US + NSE, logging everything. If late, cut agents/features — never delay this |
| **Nov 2026** | First frozen-evidence replay results (E1 pilot); decide on AAAI-27 backup submission; fix bugs revealed by pilot |
| **Dec 2026** | Full E1 + E4 runs; E3 data accumulating from live loop; internal mini-paper draft (4 pages) for guide review |
| **Jan 2027** | E2 + E3 analysis on 3+ months of live data; complete all tables/figures; full draft |
| **Feb 2027** | Polish, internal red-team review against Section 3 table, **submit to ICLR FinAI 2027**; Sem-VIII report reuses the paper |
| **Mar–May 2027** | Reviews/camera-ready if accepted; final demo + viva; live loop keeps running (feeds conference stretch) |

## 8. Paper skeleton (write toward this from day one)

1. Intro: mandates matter; nobody measures obedience; contamination crisis (cite lookahead-bias test, FinPersona-Bench)
2. Related work: the six piles (see `Literature_Review_Papers.md`)
3. System: policy schema, planner, risk veto (1.5 pages max — system is the instrument, not the contribution)
4. Evaluation protocol: frozen replay + post-cutoff + live; metric definitions
5. Results: E1 (headline), E2, E3, E4, E5
6. Limitations: 4 policies only, large-caps only, paper trading, short horizon for returns
7. Release: code + evidence bundles + scorer

## 9. Risks

| Risk | Mitigation |
|---|---|
| Engineering eats the semester, no experiments | Oct hard gate; scope cuts pre-agreed (quant agent, memory features, dashboard polish go first) |
| Live loop crashes silently | Daily Streamlit check rota + email alert on missed cycles |
| Concurrent paper scoops RQ1 | Monthly arXiv sweep (queries in `Literature_Review_Papers.md`); our live+NSE+combination still differentiates |
| API costs blow up | Budget cap in code; small models default |
| ICLR 2027 workshop doesn't repeat | Backups A/B/C in §1 |
| Team drift back to "cool bot, who cares about metrics" | This file is the contract. Re-read §2 monthly. |
