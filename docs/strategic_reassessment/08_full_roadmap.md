# 08 · Full Roadmap — from working prototype to complete system

**Two goals, in parallel:** (A) a **research paper** for the ICLR 2027 Financial-AI workshop, and
(B) a **real product/service**. They share one engine (the logged, replayable decisions), but they
need *different* work. This doc lists everything, honestly prioritised.

## The one guiding rule (read this first)

**For the PAPER, the differentiator is the evaluation/trust layer — not more agents, more data, or a
prettier UI.** Most "add more" ideas below make a better *product* but do **not** strengthen the
*paper* (and some quietly weaken it by turning it back into "another trading system"). So each item is
tagged **[R]** research value, **[P]** product value, **[E]** engineering — and a priority **P0/P1/P2**.
When time is short, do the **[R] P0** items; the rest is product polish.

---

## 0. IMMEDIATE next steps (P0 — do these first)

| # | Task | Why | Tag |
|---|---|---|---|
| 1 | **Agent-as-signal back-test** — run the LLM agents through the 3-year engine; get their IC + calibration vs the ~0 numeric baseline | **The paper's headline experiment.** Do the AI agents actually add value? | [R] P0 |
| 2 | **Anti-over-fitting**: Deflated Sharpe + PBO (López de Prado) | Nobody believes a backtest without them | [R] P0 |
| 3 | **`git init` + private GitHub + commit every prompt/config** | Reproducibility is a paper requirement and an evaluator question | [E] P0 |
| 4 | **Live daily paper-trading loop** (start mid-Oct) | The ONE thing calendar time alone produces — 4+ months of clean records | [R][P] P0 |
| 5 | **Freeze `PREREGISTRATION.md`** + clear `logs/` before clean runs | Stops "you defined the metric after seeing data" | [R] P0 |

---

## 1. Data layer  — *(current: real, single-source-per-type; ~60%)*

What we have: Yahoo OHLCV + fundamentals, Google-News RSS, Finnhub (auto), provider abstraction, resolver, frozen 40-stock universe.

| Improvement | Detail | Tag |
|---|---|---|
| **More history + better news** | Multi-year news; later SEC filings, earnings-call transcripts, analyst notes (where licensing permits) | [P] P1 |
| **Richer fundamentals** | Debt/Equity, Free Cash Flow, EV/EBITDA, ROE, dividends, insider/institutional ownership, earnings surprises | [P] P1 |
| **Real macro** | Treasury yields, CPI/PPI, unemployment, GDP, PMI, dollar index, oil, VIX (FRED) | [P] P1 |
| **Corporate events** | Splits, dividends, mergers, earnings dates, buybacks (also needed to avoid data errors like the delisted TATAMOTORS.NS) | [P][R] P1 |
| **Data hygiene** | Point-in-time snapshots, de-duplication, timestamp every item (partly done) | [R] P1 |
| More markets (EU, Japan, crypto, forex) | Only after US+NSE is solid | [P] P2 |

## 2. Intelligence layer (models + features) — *(current: logistic + LLM; ~45%)*

| Improvement | Detail | Tag |
|---|---|---|
| **Better ML models** | Compare LightGBM, CatBoost, and a small temporal model (TCN / Temporal Fusion Transformer) vs the logistic baseline — **report IC honestly** | [R][P] P1 |
| **Better features** | Earnings surprises, analyst revisions, volatility regime, sector rotation, factor exposures | [P] P1 |
| **RAG (finance memory)** | Retrieve past filings/earnings/company history for the agents to cite | [P] P2 |
| Multi-modal inputs | Price + news + fundamentals + macro + filings together | [P] P2 |

## 3. Agent layer — *(current: 4 specialists + planner; ~70%, already strong)*

| Improvement | Detail | Tag |
|---|---|---|
| **Agent memory** | Remember past decisions, mistakes, prior reasoning | [P] P1 |
| **Structured debate** | Bull → bear → challenge → committee vote (not everyone speaks once) | [R][P] P1 |
| **Self-critique** | A critic agent finds weaknesses → revise before deciding | [R] P1 |
| More specialists | Options, sector, portfolio, execution, compliance agents | [P] P2 |
| ⚠️ **Caution** | Adding agents is easy and looks impressive but rarely helps the *paper*. Add one only if an **ablation shows it helps.** | — |

## 4. Quant-research layer — *(current: IC, Sharpe/Sortino/DD/VaR, sizing, backtester; ~75%, strongest part)*

| Improvement | Detail | Tag |
|---|---|---|
| **Deflated Sharpe + PBO** | (see P0) — proof the results aren't over-fit | [R] P0 |
| **Alpha / Beta / Information Ratio / tracking error** | Standard active-management metrics | [R] P1 |
| **Factor attribution + regime analysis** | Explain *where* returns come from | [R] P1 |
| **Rolling / walk-forward / nested validation** | Not one back-test — many, properly | [R] P1 |
| **More baselines** | Buy-and-hold, random, momentum, ML, single-LLM, full committee — all on one chart | [R] P1 |

## 5. Product layer — *(current: CLI + logs; ~55%)*

| Improvement | Detail | Tag |
|---|---|---|
| **Web dashboard** | Portfolio → analysis → reasons → charts → risk → history (Piyush's track) | [P] P1 |
| **Portfolio management** | Many stocks: allocation, rebalance, sector exposure, VaR, drawdown | [P] P1 |
| **Explainability UI** | Show WHY, not just BUY (the compare view + veto log + "0 rule-breaks this month" badge) | [P] P1 |
| **Live alerts** | "NVIDIA earnings → committee re-analyses → notify user" | [P] P2 |
| **Deploy** | Web (and later mobile) | [P] P2 |

## 6. Research work that makes the paper *memorable* (prioritise for ICLR)

| Item | Why it matters | Tag |
|---|---|---|
| **Model comparison** | Run GPT / Claude / Gemini / open models — findings must generalise across models | [R] P1 |
| **Ablations** | Turn off news / macro / fundamentals / debate → what actually matters | [R] P1 |
| **Cross-market** | Same results on US **and** India → much stronger evaluation | [R] P1 |
| **Failure analysis** | *When does the committee get it wrong?* Negative results + diagnostics are increasingly valued | [R] P1 |
| **Release the artifact** | Frozen evidence bundles + profiles + scorer + leaderboard — "people can build on this" is the biggest acceptance lever | [R] P1 |

## 7. Engineering / infrastructure (don't neglect)

`git` + versioning (P0) · CI (GitHub Actions) · Docker · config management · experiment tracking
(MLflow / W&B) · dataset versioning (DVC) · unit + integration tests (started) · benchmark scripts ·
structured logging · monitoring for the live loop.  **Tag: [E], mostly P1.**

---

## 8. The north star (where this goes long-term)

Today the system answers *"Should I buy NVIDIA?"*. The real destination is:
> *"Given **my** portfolio, **my** risk tolerance, today's market and macro — what should I do?"*

That turns "stock analysis" into a **personal AI investment advisor** — closer to where the industry is
heading, and a strong product story. (For the paper, keep the scope tight; this is the product vision.)

---

## 9. What NOT to over-invest in yet (honest)

- ❌ 6 data providers, 10 agents, fancy deep models **before** the headline experiment (#0.1). They don't
  answer "do the agents beat the baseline?" — which is the whole paper.
- ❌ A polished dashboard before the research results exist. Product without the trust result is just
  another Vibe-Trading.
- ❌ Real-money trading. Ever. Paper only — it's a strength in review.

## 10. One-glance priority

| Now (P0) | Next (P1) | Later (P2) |
|---|---|---|
| Agent-as-signal experiment · Deflated Sharpe/PBO · git · live loop · pre-registration | Model comparison · ablations · cross-market · failure analysis · richer data · better ML · dashboard · portfolio view · debate/memory · release artifact | More markets · RAG · multi-modal · more agents · alerts · mobile |

**If you only do five things next:** (1) agent-as-signal back-test, (2) Deflated Sharpe + PBO,
(3) git + reproducibility, (4) start the live loop in October, (5) model comparison + one ablation.
Everything else is important but secondary to proving **the AI agents are worth it, honestly measured.**
