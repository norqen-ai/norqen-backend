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
