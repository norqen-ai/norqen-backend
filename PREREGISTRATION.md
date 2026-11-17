# PRE-REGISTRATION — metric & protocol definitions (frozen)

**Frozen:** 2026-08-07 · **Policy schema:** v1.1 · **DecisionCard schema:** v1.0
**Purpose:** define *exactly* how every number is computed BEFORE large-scale logging, so
results cannot be accused of being defined after seeing the data. Change only by dated
amendment below, never silently.

---

## 0. Frozen artifacts
- **Policies (4):** `code/config/policies/{conservative,long_term,intraday,aggressive_growth}.json`
  (each carries objective, horizon, `max_position_pct`, `confidence_to_act`, `tool_priorities`,
  `forbidden_evidence`, `evidence_budget`, `sizing_method`, `target_vol`).
- **Universe:** `code/config/universe.json` — 20 US + 20 NSE large-caps, frozen 2026-08-06.
  The **product** analyses any ticker; **experiments** use only this list (survivorship-safe).
- **Costs:** transaction 5 bps + slippage 2 bps per unit turnover (backtester default).

## 1. Leakage controls (apply to every experiment)
- A signal/agent at decision day *t* sees data with timestamp **≤ t** only.
- Realised outcome uses **t+1..t+horizon**, never visible to the decision.
- Realised volatility for sizing is frozen into the evidence bundle (leakage-safe replay).
- Historical LLM replay runs only on dates **after each model's training cutoff** (documented per model).
- Frozen-evidence bundles give **deterministic** cross-policy replay.

## 2. RQ1 — policy adherence & steerability (`src/eval/adherence.py`)
- **Per-clause violation** on a logged card, checked against ITS policy:
  - `forbidden_evidence` — any evidence `kind`/`tool` ∈ `policy.forbidden_evidence`.
  - `oversize` — acted AND `position_size_pct > max_position_pct`.
  - `under_confidence` — acted AND `confidence < confidence_to_act`.
  - `bad_stop` — acted AND NOT `0 < stop_loss_pct ≤ policy.stop_loss_pct`.
  ("acted" = action ∈ {BUY, SELL}.)
- **Competence-conditioned (anti-gaming):** adherence is ALWAYS reported alongside the
  **non-trivial action rate**; a do-nothing (always-WAIT) agent has 0 violations and ~0 action
  rate → reported as useless, never as a winner.
- **Cross-policy divergence** over shared moments (same ticker, same frozen bundle):
  `action_divergence` (labels differ), `full_divergence` (action+size+stop differ),
  `mean_size_spread` (max−min position size across mandates when acting).

## 3. RQ2 — confidence calibration (`src/eval/calibration.py`)
- Confidence ∈ [0,1] is read as **P(the directional call is correct)**.
- Outcome `correct` = 1 iff `sign(direction) == sign(realised forward return)` over the horizon.
- Report: 10-bin **reliability curve**, **ECE**, **MCE**, **Brier**; then **temperature scaling**
  (single T minimising ECE) and post-scaling ECE. Reported per-signal and (later) per-policy × per-market.

## 4. RQ3 — evidence cost vs quality (`src/eval/cost_quality.py`)
- **Cost** = mean number of evidence items gathered per decision.
- **Quality** = directional accuracy of the aggregated call.
- Sweep the stopping threshold; report the (cost, quality) **frontier**. Flat quality ⇒ stop early.

## 5. Layer-1 quant metrics (`src/eval/quant.py`)
- **Signal edge:** Information Coefficient (Pearson + Spearman rank), IC t-stat; |t|>2 ⇒ real edge.
- **Performance:** CAGR, annualised vol, **Sharpe**, **Sortino**, **Calmar**, **max drawdown**,
  hit rate, **VaR(5%)**, **CVaR(5%)** — all net of costs, annualised at 252 days.
- **Sizing:** vol-target / half-Kelly on `target_vol / realised_vol × conviction`, capped by `max_position_pct`.
- **Anti-overfitting (to add before any performance claim):** Deflated Sharpe Ratio + PBO (López de Prado).

## 6. Baselines & ablations (frozen list)
- **Baselines:** B0 buy-and-hold/majority · B1 non-LLM quant (numeric signals) · B2 single general LLM ·
  B3 prompted-financial LLM · B4 multi-agent no-debate · B5 committee · B6 +evidence verifier ·
  B7 +calibration+abstention.
- **Ablations:** remove risk engine · remove adaptive loop · remove each specialist agent · remove
  calibration · remove abstention · vary #agents.

## 7. Statistics
- Every rate with **95% bootstrap CIs**; **paired** comparisons on identical evidence bundles;
  report **N** everywhere; never claim a returns difference is significant on the short live window.

---
### Amendments
- *(none yet — append dated entries here)*

#### A1 — 2026-10-12 (~15:30 IST): point-in-time decision-component study
Written **before** any outcome of an LLM decision in this study was computed (only the outcome
simulator was unit-checked on hand-picked trades). Code: `code/src/pit/`, runners `build_pit_bundles.py`,
`run_pit_decisions.py`, `analyze_components.py`.

**Question.** On identical point-in-time evidence, which parts of an LLM agent's trade decision carry
skill relative to deterministic code — (T) trade selection (whether + which direction), (Z) position size,
(X) exits (stop/target), (K) stated confidence — and therefore when do deterministic guardrails
(block / repair) improve or worsen realised outcomes?

**Data.**
- Universe: 100 stocks = the frozen 40 (reported as a subset) + 30 US and 30 NSE large caps (`src/pit/universe.py`).
- Decision dates: first session on/after the 15th of each month, Jan 2025 – Jul 2026 (19 dates per market),
  after the training cutoff of every model used (gpt-4o-mini 2023-10, gpt-4.1-mini 2024-06, gpt-5-mini 2024-05,
  llama-3.3-70b 2023-12, gpt-oss-120b 2024-06).
- Evidence (all five agents) rebuilt as of t: indicators/ML on prices ≤ t; fundamentals from annual statements
  with fiscal-year end + 90 days ≤ t; news = Google News headlines published in [t−7d, t+1d 00:00 UTC);
  macro = index SMA20/50 as of t. Evidence LLM = gpt-4o-mini T=0, captured once and replayed to every decision model.

**Decisions per (bundle, profile).**
- C = guarded code decision (current planner, `decision_mode=guarded`; vol-target size, policy stop/target, confidence gate).
- U = one LLM proposal per (model, prompt style ∈ {nl: text persona, explicit: numeric rules}), T=0
  (reasoning models: provider default temperature, reasoning effort low). Same evidence view as C.

**Outcome (fixed).** Enter at next session's open; hold H trading days (intraday 1, aggressive_growth 5,
conservative 20, long_term 40); stop/target checked on daily high/low, gap fills at the open, stop first if both
touched; round-trip cost US 14 bps, NSE 36 bps. Utility u = position_size_pct/100 × net return, in bps of equity;
WAIT/HOLD = 0. Co-primary: market-adjusted (index-excess, β=1) version. SELL = short (NSE: via futures; same cost).

**Pipelines (all computed post hoc from the same U and C — no extra LLM calls).**
- RAW = U. BLOCK = U unless the risk engine vetoes it (size > cap, stop missing/looser than policy,
  confidence < bar) → WAIT. REPAIR = WAIT if confidence < bar, else size = min(size, cap) and stop = policy stop
  if missing/looser (LLM target kept). JUDGMENT-ONLY = LLM's trade selection, code's vol-target size, policy exits.
  CODE = C.

**Component estimands.**
- T: per-instance unit-size P&L (1% size, policy exits) of LLM-selected vs code-selected trades.
- Z: on LLM trades with policy exits — LLM size vs exposure-matched equal size (mean LLM size within
  model×style×profile) vs code vol-target size; Spearman ρ(size, signed return).
- X: on LLM trades at unit size — LLM stop/target vs policy stop/target vs no exits.
- K: AUC of LLM confidence for a profitable trade; unit-size P&L above vs below the profile's bar.
- Guardrails: intervention rate; helpful / harmful / neutral split (|Δu| ≤ 0.5 bp = neutral); exact sign test;
  mean Δu with 95% CI from a date-cluster bootstrap (2,000 reps); stratified by clause, profile, market, model.

**Robustness.** Index-excess utility; frozen-40 subset; a common H=20 for all profiles; re-run of gpt-4o-mini (noise floor).

**Honesty.** All results reported whatever their sign. No threshold, horizon, cost or pipeline definition will be
changed after outcomes are seen; any later change is a dated amendment and labelled exploratory in the paper.

#### A2 — 2026-10-13 (~02:30 IST): extended window (added after the A1 primary results were seen)
After an internal review flagged the 19-month window, the sample is extended back to the earliest date that is
post-cutoff for all three decision models: first session on/after the 15th of each month from **Jul 2024**
(gpt-4.1-mini cutoff 2024-06; gpt-5-mini 2024-05; gpt-4o-mini 2023-10) to Jul 2026 = 25 dates per market,
2,500 bundles. Every rule (evidence, prompts, profiles, outcome simulator, costs, pipelines, statistics) is
unchanged from A1. The A1 window (Jan 2025 – Jul 2026) remains the pre-registered primary analysis; the
25-month results are reported as a pre-specified-rules extension, labelled as added after seeing A1 results.
