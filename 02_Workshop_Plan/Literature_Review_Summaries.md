# Literature Review — Summaries (the papers you must know)

Companion to `Literature_Review_Papers.md` (the reading list). Each entry answers four
questions: **What is it? · What does it do/propose? · How does it work? · How does it help US?**

> Verification note: papers with arXiv IDs from **2602.xxxxx onward are from Feb 2026 or later** (after model training cutoffs). The summaries of those are based on the papers' own abstracts/pages fetched 6 Aug 2026 — re-open each before quoting it in the paper.

---

## TIER 1 — The five anchors (know these cold)

### 1. TradingAgents (arXiv:2412.20138, 2024) — *the system we position against*
- **What:** an LLM multi-agent framework that mimics how a real trading firm is organised.
- **Does:** turns a firm's roles into cooperating LLM agents that debate and then trade a stock.
- **How:** specialist analysts (fundamental / sentiment / news / technical) → bull vs. bear **researchers debate** → a **trader** proposes → a **risk-management team** checks → a fund manager approves. Reports gains in cumulative return, Sharpe, and max drawdown vs. baselines.
- **Helps us:** this is the canonical "multi-agent committee for returns." We reuse the *shape* but change the *question*: we don't claim better returns, we **measure whether such a committee obeys a mandate and is honest**. It's Related-Work anchor #1 and a baseline (B5, the committee).

### 2. "The Alpha Illusion" (arXiv:2605.16895, 2026) — *our motivation, in one paper*
- **What:** an argument that reported returns from LLM trading agents should **not** be trusted as evidence they'd work in real deployment.
- **Does:** shows that impressive Sharpe ratios from FinCon/FinMem/TradingAgents-style systems can't be distinguished from statistical artifacts.
- **How:** no new experiments — it defines a **minimum reporting protocol** and **six validity tests**: temporal integrity, real-world frictions, counterfactual robustness, **predictive calibration**, numerical execution, and multi-agent disaggregation. Argues "language confidence is not tradable probability."
- **Helps us:** this *is* our motivation slide. It says the field crossed research→deployment too early and calls for exactly the tests we run (calibration, leakage control, disaggregation). We cite it in the first paragraph to justify why "we measure, not chase returns."

### 3. FinPersona-Bench (arXiv:2606.31522, 2026) — *the closest work; must differentiate*
- **What:** a benchmark for how *stable* a financial agent's assigned behaviour is over time.
- **Does:** measures **Mandate Salience Decay (MSD)** — a mandate like "preserve capital" gradually loses its grip as market context piles up.
- **How:** a **synthetic** market (price decoupled from hidden value) tests 3 failure modes (trading on no signal, panic-selling in crashes, ignoring fundamentals in bubbles) across **18 LLMs**, each given a conservative→aggressive profile. Tests **mandate re-grounding** (periodically re-injecting the mandate). Finding: MSD compounds, is model-dependent; re-grounding helps conservative agents but *worsens* aggressive ones.
- **Helps us / how we differ:** same construct (mandate adherence) but a **different axis** — they are *longitudinal* (one mandate over time) on a *synthetic* market; we are **cross-sectional** (many mandates on the **same real** evidence at one moment), with a **per-clause violation taxonomy**, on **real US+NSE**, and we **release** the benchmark. We also *replicate* their decay finding in a real loop as validation. Cite in paragraph 2.

### 4. StockBench (arXiv:2510.02209, 2025) — *the hygiene we borrow + a humbling finding*
- **What:** the first **contamination-free** benchmark for LLM agents trading over multiple months.
- **Does:** tests whether LLM agents actually trade profitably in realistic, sequential conditions.
- **How:** agents get daily prices + fundamentals + news, make buy/sell/hold decisions over months; evaluated on cumulative return, max drawdown, Sortino; designed so the test period post-dates training data. **Finding:** most models **cannot beat buy-and-hold**, and being good at financial Q&A does **not** mean good trading.
- **Helps us:** proves (a) why returns are a weak yardstick and (b) how to keep evaluation leakage-free. We adopt its temporal hygiene and cite its "static skill ≠ trading skill" finding.

### 5. CLQT (arXiv:2606.29771, 2026) — *cost-aware; "diagnose before you rank"*
- **What:** a closed-loop, cost-aware, strategy-consistent benchmark for LLM **portfolio-management** agents.
- **Does:** argues ranking agents by returns alone is flawed (market conditions dominate; leaks inflate scores) and reframes evaluation as **diagnosis, not ranking**.
- **How:** agents run a 5-stage loop (gather→synthesize→allocate→execute→reflect) with transaction/financing costs, **strategy-consistency hash chains**, a 3-tier memory, and a tool layer; scored on a 5-axis capability card (Coherence, Acuity, Composure, Discipline, Reliability). Finding: the best agent by *capability* differs from the top Sharpe agent.
- **Helps us:** the strongest neighbour for **RQ3 (evidence cost)** and for the "diagnose, don't just rank" philosophy we share. We differ: we add **policy-conditioning**, **calibration**, and **cross-sectional adherence**, and cover **NSE**. Cite as a co-traveller, differentiate on those four.

---

## TIER 2 — The multi-agent systems we build on / compare against

### 6. FinCon (NeurIPS 2024)
- **What/Does:** an LLM multi-agent system (manager–analyst hierarchy) for single-stock trading and portfolio management.
- **How:** agents communicate in natural language; a **Conceptual Verbal Reinforcement** mechanism sends risk-aware verbal feedback after episodes (a "textual gradient") to update behaviour and cut redundant chatter.
- **Helps us:** a strong committee baseline; its "verbal reinforcement" is a mechanism we deliberately don't use. It never measures mandate adherence or calibration — a gap we fill.

### 7. FinMem (arXiv:2311.13743, 2023)
- **What/Does:** an LLM trading agent with a **layered memory** and a configurable **risk/character** profile.
- **How:** memory in deep/intermediate/shallow layers with decay + importance; retrieves relevant past events; the "character" sets risk appetite.
- **Helps us:** shows persona + memory in trading agents. We keep memory minimal (not our novelty) and instead **test whether the persona/mandate is actually followed** — the question FinMem assumes but never measures.

### 8. FinAgent (KDD 2024)
- **What/Does:** a **multimodal** foundation agent for trading — text + price-chart images + numbers.
- **How:** a market-intelligence module + **dual-level reflection** (quick + deep) + tool use; ingests multimodal data to decide trades.
- **Helps us:** the multimodal single-agent state-of-the-art; still returns-focused. Reinforces that "more capable agent" is well-trodden and that the open question is evaluation, not capability.

---

## TIER 3 — Foundations for our specific claims

### 9. Look-ahead bias in LLM stock prediction (Glasserman & Lin 2023; "A Test of Look-ahead Bias in LLM Forecasts," arXiv:2512.23847, 2025)
- **What/Does:** shows LLMs asked to predict returns from historical news can "**remember the future**" (the outcome is in their training data), inflating backtested skill; proposes tests to detect it.
- **How:** compares performance on news the model could vs. couldn't have memorised; masks/anonymises entities; measures the gap.
- **Helps us:** the technical backbone of our **leakage-free** design (post-training-cutoff replay + a live loop). Cite whenever we justify temporal validity.

### 10. LLM Agent in Financial Trading: A Survey (arXiv:2408.06361, 2024)
- **What/Does:** maps the whole field — data types, agent architectures, memory, and (thin) evaluation.
- **Helps us:** the reference for our Related Work structure and evidence that **evaluation/trustworthiness is the under-developed corner** — where we plant our flag.

### 11. Calibration foundations (Guo et al. 2017, "On Calibration of Modern Neural Networks"; conformal prediction)
- **What/Does:** defines and fixes miscalibration — **ECE**, reliability diagrams, **temperature scaling**; conformal prediction gives distribution-free coverage.
- **How:** bins predicted confidence vs. actual accuracy (ECE); a single temperature rescales logits post-hoc; conformal wraps any predictor with guaranteed coverage.
- **Helps us:** the exact toolkit for **RQ2** — we compute ECE/Brier on our agents' stated confidence, then temperature-scale / conformalise and measure the effect on sizing/drawdown.

### 12. Cost-aware agents — Calibrate-Then-Act (arXiv:2602.16699); BATS (arXiv:2511.17006)
- **What/Does:** study when an agent should **stop gathering information** vs. keep spending tool calls/tokens.
- **How:** tie a stopping/exploration rule to the agent's (calibrated) confidence and a budget; measure quality-per-cost.
- **Helps us:** the foundations for **RQ3** — our planner stops when confidence ≥ the policy's threshold or the evidence budget is spent; we sweep those and plot the cost–quality frontier. (Recent; verify exact claims before citing.)

---

## How to use this for the survey slide / paper
- **Group into the six piles** already in `Literature_Review_Papers.md`.
- **Two-paragraph intro rule:** paragraph 1 = the returns-crisis (Alpha Illusion + StockBench + look-ahead bias); paragraph 2 = the closest work we differentiate from (FinPersona-Bench + CLQT).
- **One-line-per-paper for the slide:** use the bold "**What:**" line of each entry.
