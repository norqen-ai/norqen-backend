# ICAIF 2026 · AI4F Workshop — One-Month Execution Plan

**Window:** 8 Sep → 7 Oct 2026 (AoE) · **Venue:** ai4f.org, 3rd Workshop on LLMs & GenAI for Finance (ICAIF'26, Bocconi, Milan) · **Status:** non-archival, single-blind, no page limit, CC BY 4.0 · **Realistic target:** poster (oral is industry-skewed; do not plan around it).

> This plan supersedes the ICLR-FinAI-2027 timeline in `ICLR_FinAI_2027_Workshop_Plan.md` **for this deadline only**. The live-trading loop (Oct hard-gate) is explicitly OUT — it cannot produce data in 4 weeks and is not needed for the headline.

---

## 0. TL;DR — the decision

**Submit.** It's non-archival (zero cost to the ICLR-FinAI-2027 / ICAIF-2027 plan), the venue is drifting exactly toward eval/benchmark/reliability work, and the empirical bar is low (orals have been won on n=1 evals). **But two things must happen or we don't submit:**
1. **Make obedience able to fail** (today it is true-by-construction → the RQ1 result would be a meaningless 0%).
2. **Reposition the framing** away from "first mandate-adherence benchmark" (preempted by CLQT + FinPersona-Bench) onto **cross-sectional identical-evidence design + honest-confidence calibration + a real US-vs-NSE finding.**

If by **Gate 1 (14 Sep)** obedience can't be made to fail and outcomes can't be logged, downgrade to an **obedience-only short paper (4 pp)** and drop calibration to "future work." Still worth submitting.

---

## 1. What our paper actually is (plain language)

We are **not** claiming our trading bot makes money. We built a **measuring instrument** — a standard test for AI trading agents — that asks three questions about *any* such agent:

1. **Obedience** — does it actually follow the investor's written rulebook (position limits, stop-loss, confidence bar, forbidden data)?
2. **Honesty** — when it says "I'm 70% confident," is it right about 70% of the time? (calibration)
3. **Efficiency** — does it stop gathering evidence once it has enough, or waste effort?

The trick that makes it a *benchmark* and not just another bot: we **freeze one snapshot of real market evidence**, then hand the **same** snapshot to the agent under **different investor rulebooks** (cautious vs aggressive) and **different AI models**, and score all three questions. We do this on **US *and* Indian (NSE)** stocks, and we **release the whole test kit** (frozen data + rulebooks + scoring code) so anyone can measure their own agent. **The novelty is the measurement design, not the bot.** The multi-agent system is the *thing being tested*, and gets ≤1.5 pages.

---

## 2. The one-sentence contribution (repositioned — memorize this)

> *A leakage-controlled, **cross-sectional** benchmark that holds the evidence **identical** across models and stocks in **both US and Indian (NSE)** markets to jointly score **per-clause mandate obedience**, **honest-confidence calibration** (ECE/Brier/selective risk), and **evidence-gathering cost** — isolating agent behaviour from the market-path luck that confounds longitudinal trajectory benchmarks (CLQT, FinPersona-Bench).*

Every clause is a cell no competitor holds. If a component doesn't ladder up to this sentence, it's the "instrument" or it's cut.

---

## 3. The competitive reality — why we reframe

The venue trend is in our favour (2024→2025: econ-empirical 46%→15%; agents 6%→21%; eval/benchmark 4%→15%; calibration/interp 2%→12%). But the *obedience* headline is now contested:

| Competitor | What it already does | Why we're still distinct |
|---|---|---|
| **CLQT** (arXiv 2606.29771, Aug'26) — closest threat | Leakage-controlled + mandate-adherence + **cost** + coherence, real **US** data, 5 models, audit trail | It's **longitudinal single-path** (confounds skill w/ market luck); "calibration" = signal-action *coherence*, **not** honest-confidence ECE/Brier; **US-only**; artifact "on request" |
| **FinPersona-Bench** (2606.31522, Jul'26) | Mandate-adherence, 18 models | **Synthetic** market, **longitudinal**, mandate as a **single scalar** (no per-clause taxonomy), **no calibration, no cost** |
| **Investor Risk Profiles of LLMs** (2603.09303) | LLM answers a risk questionnaire | Self-reported disposition in the abstract, **not obedience on real decisions**; no calib/cost |
| **When Hallucination Costs Millions** (2510.00332) | Real adversarial **crypto**, task accuracy + tool-use | Not mandate-obedience/calibration; crypto not equities |

**Load-bearing claim = cross-sectional identical-evidence design**, not "first obedience benchmark." **Do NOT write "first mandate-adherence benchmark."**

---

## 4. What's built vs what remains (verified 8 Sep audit)

**Completion toward the benchmark paper: ~30–35%.**

### ✅ Real and working (the instrument + numeric layer)
- Frozen-evidence bundles + deterministic replay (`src/audit/log.py`), decision log (JSONL).
- Deterministic risk engine w/ absolute veto (`src/risk/engine.py`); risk-based sizing (`src/core/sizing.py`, hard-capped).
- Real data providers (yfinance OHLCV/fundamentals/macro, Google-News RSS, symbol resolver, optional Finnhub).
- 4 LLM agents (technical/news/fundamental/macro) via OpenAI structured output, with keyless deterministic fallback (`src/agents/llm.py`, `src/tools/registry.py`).
- Leakage-safe **numeric** backtester (`src/backtest/`) + quant metrics (IC/Sharpe/… in `src/eval/quant.py`).
- Eval scaffolding: `adherence.py` (per-clause taxonomy + competence view + divergence), `calibration.py` (ECE/Brier/temp-scaling), `cost_quality.py`.
- `PREREGISTRATION.md` (frozen 7 Aug), the reviewer-2 exhibit list (Fig 1–5 / Table 1–3), strong related-work corpus.

### ⚠️ Broken / missing / blocking (the actual research)
1. **RQ1 obedience is true-by-construction.** `planner_graph._synthesize` clamps size, sets stop = policy value, forces WAIT under the confidence bar *before logging* → all four `check_card` clauses are structurally unviolable, and the `forbidden_evidence` tool names aren't even real registry tools. **The obedience result today would be a meaningless 0%.** → **#1 fix.**
2. **No agent-level results at N.** 9 bundles, **3 tickers** (NVDA/AAPL/RELIANCE), **1 model** (gpt-4o-mini), 16 LLM cards, **zero realized outcomes logged** → RQ2 (calibration) and RQ3 (cost) on the agents are **uncomputable today**.
3. **No decoy/trap suite** (the anti-gaming fix `02_reviewer2` calls the sharpest-objection defence).
4. **Steerability may be ~0.** `06_data_architecture` records "cross-policy divergence = 0%, collapses to WAIT," contradicting the README's "50% differed." Neither is stored. **Must re-verify with a saved run.**
5. **Single model.** No non-OpenAI provider path. Need ≥2 families.
6. **No realized-outcome logging / no post-cutoff replay** (blocks calibration).
7. **Dead/misleading:** `ml/predictor.py` (XGBoost) unwired; tests don't cover the LLM planner; single git commit (reproducibility claim not real).

---

## 5. The three experiments and what each proves

**E1 — Obedience (RQ1, the headline).** Run agents in an **UNGUARDED** mode where the LLM *proposes* action + size + stop directly (so it *can* break the mandate). Score per-clause violation rates, **competence-conditioned** (violations among ACTED only + non-trivial-action rate), and **decoy pass-rate** (act-required vs abstain-required traps). Report **guarded vs unguarded** side-by-side (the guarded/deterministic layer becomes the "enforcement" contrast, not the measurement). Cross-sectional over identical frozen bundles. → proves agents are steerable-but-imperfectly-obedient. **Needs no outcomes → fully doable at scale.**

**E2 — Cross-policy divergence (steerability).** Falls out of E1 runs: same frozen bundle × 4 policies → action/size/stop divergence. **Resolves the 0%-vs-50% contradiction with real, stored numbers.**

**E3 — Cross-market finding (US vs NSE), the differentiator.** Compare E1/E4 metrics on US vs NSE names. **"We also ran India" is not enough** — we need a *gap* (e.g., obedience or calibration degrades on sparse-coverage NSE evidence).

**E4 — Honest-confidence calibration (RQ2, strong secondary).** Generate **historical** bundles on **post-cutoff dates** where the t+horizon outcome is already known → score `(confidence, was-it-right)` → ECE/Brier/reliability/temperature scaling, per policy × market. **Leakage-safe scope:** run on technical/macro/price evidence (cleanly reconstructable from historical OHLCV); news/fundamental calibration is a stated limitation (historical headlines/point-in-time fundamentals aren't leakage-safe to backfill in 4 weeks).

**E5 — Cost–quality (RQ3, labelled secondary) & returns (labelled underpowered).** Cost sweep on cached bundles; returns only with CIs, never headline.

---

## 6. Exhibits → experiment map (build backwards from these)

| Exhibit | Fed by | Must show |
|---|---|---|
| **Fig 1 — money shot** | E1 | one frozen bundle → 4 policies → 4 different compliant decision cards; one vetoed |
| **Fig 2 — divergence heatmap** | E2 | decisions × policies, coloured by action/size |
| **Fig 3 — reliability diagram** | E4 | confidence vs realized accuracy, per policy, pre/post temp-scaling |
| **Fig 4 — cost–quality frontier** | E5 | one curve per policy (conservative spends more) |
| **Fig 5 — US vs NSE panel** | E3 | the cross-market gap |
| **Table 1 — per-clause violation rates** | E1 | × 4 policies × ≥2 models, 95% CIs (**headline table**) |
| **Table 2 — competence-conditioned** | E1 | violation rate \| non-trivial-action rate (anti-gaming) |
| **Table 3 — calibration** | E4 | ECE/Brier per policy × market |

---

## 7. Week-by-week schedule (owners + gates)

**Owners:** **M** = Malhar (ML/research lead, writing lead) · **O** = Omkar (agents/infra) · **P** = Piyush (data/artifact/figures).

### Week 1 — 8–14 Sep · "make obedience able to fail + log outcomes + scale data"
- **[O] Unguarded agent mode** — LLM proposes action/size/stop; keep guarded mode as the contrast. *(#1 fix)*
- **[O] Decoy/trap suite** — hand-label ~20–30 moments as act-required / abstain-required.
- **[O] 2nd model provider** — add Anthropic Claude (or one open model via API) behind the `judge()` abstraction.
- **[P] Historical bundle generator** — frozen bundles on post-cutoff historical dates across the 40-name universe; target **≥150 bundles**. Attach `t+horizon` realized outcome to each card.
- **[M] Fix `forbidden_evidence`** to reference real registry tools; sanity-check every `check_card` clause can now trigger.
- **[M] Re-verify divergence** — one stored run to settle 0%-vs-50%.
- **⛔ GATE 1 (14 Sep):** unguarded mode logs real violations on ≥1 model×policy; outcomes logged; ≥150 bundles exist. *Miss → cut to obedience-only 4-pp paper.*

### Week 2 — 15–21 Sep · "run the grid + compute results"
- **[O+P] Full E1 grid:** ≥150 bundles × 4 policies × 2 models × 3 repeats, unguarded, logged. (~cheap, deterministic replay.)
- **[M] Compute E1/E2:** per-clause + competence-conditioned tables with 95% bootstrap CIs; divergence heatmap data; decoy pass-rates.
- **[M] Compute E3:** US vs NSE split of every metric — **look for the gap.**
- **[P] E4 calibration run** on historical post-cutoff bundles (technical/macro/price) → reliability/ECE/Brier.
- **⛔ GATE 2 (21 Sep):** Table 1 + Table 2 exist with CIs; E3 gap quantified; E4 preliminary numbers in hand.

### Week 3 — 22–28 Sep · "figures + draft v1 + artifact"
- **[M] Draft v1** (5–6 pp sigconf): intro pre-empting CLQT/FinPersona in ¶2; method; results; the E3 finding.
- **[P] Render Fig 1–5**, generate every table from a committed script that saves CSV/JSON (no pasted numbers).
- **[P] Package artifact:** clean repo, README, `PREREGISTRATION.md`, leaderboard script, bundles+policies+scorer; verify a fresh clone reproduces every number.
- **[O] E5** cost sweep + (optional) small returns section with CIs.
- **⛔ GATE 3 (28 Sep):** all exhibits generated; draft v1 complete; artifact reproduces end-to-end.

### Week 4 — 29 Sep–5 Oct · "tighten + red-team + review"
- **[M] Draft v2** — cut to a tight 5–6 pp; every number labelled agent-vs-baseline.
- **[all] Red-team vs CLQT** — can a reviewer who knows CLQT still call us incremental? If yes, sharpen E3/interaction.
- **[M] Guide (Varade) review**; fix related-work verification (open every arXiv ID ≥2601 before citing).
- **⛔ GATE 4 (5 Oct):** camera-ready-quality PDF; artifact URL live (or ready to unlist during anonymity? — single-blind, so names on; artifact can be public).

### Buffer — 6–7 Oct
- Final proofread, abstract ≤5000 chars, keywords, TL;DR, **submit on OpenReview (7 Oct AoE)**. One author agrees to review.

---

## 8. Honesty guardrails (non-negotiable — this is the team's Achilles heel)

1. **Label every number by source:** LLM-agent vs numeric-baseline. A baseline number never stands in for an agent number. (The README's 73%→51%, ECE 0.075→0.029, IC≈−0.02, cost 2.0→2.9 are **numeric-signal** — recast or drop.)
2. **Obedience only counts if measured UNGUARDED** (the LLM could have violated). Always report guarded vs unguarded.
3. **Resolve, don't paper over, the divergence contradiction** — report whatever the stored run actually shows, even if it's low.
4. **Calibration only on leakage-safe historical evidence;** news/fundamental calibration = stated limitation.
5. **Returns/Sharpe = labelled underpowered secondary,** with CIs, never a headline.
6. **Every reported number reproducible from a committed script + saved output** — not a one-off paste. Commit often (the single-commit repo undermines the reproducibility claim).
7. **Honour `PREREGISTRATION.md`;** any change = dated amendment.
8. **Cite only papers actually opened** — every arXiv ID ≥ 2601.xxxxx is post-cutoff/unverified per your own notes; read before quoting.
9. **No "first mandate-adherence benchmark" claim.** No "XGBoost/HMM/GARCH" claim (dead/unwired).

---

## 9. Scope — what we are explicitly NOT doing

- ❌ 4-month live paper-trading loop (not needed, no time) — → "future work / limitation."
- ❌ Dashboard / web UI (Piyush reassigned to data + artifact + figures).
- ❌ ≥3 models if only 2 fit the time/budget — **2 is acceptable**; add a 3rd only if cheap.
- ❌ Fix/verifier/enforcement experiments (that's the ICAIF-2027 *conference* stretch, gated).
- ❌ Real money, ever.

---

## 10. Related work we MUST cite-and-differentiate (intro ¶2)

1. **CLQT** (2606.29771) — differentiate on cross-sectional-vs-longitudinal, honest-confidence-calibration-vs-coherence, US+NSE-vs-US-only, released+pre-registered-vs-on-request.
2. **FinPersona-Bench** (2606.31522) — real dual-market vs synthetic; cross-sectional vs longitudinal; joint calib+cost vs mandate-only.
3. **One calibration ancestor from THIS venue** (signals fit): *How Much Should We Trust LLM-Based Measures* (2024) **or** *What Does ChatGPT Make of Historical Stock Returns* (2024, miscalibration).
4. Name-check **the taxonomy/cost position paper** (2603.27539): "the field called for cost-aware, taxonomy-grounded evaluation — we deliver the operational benchmark."
Anchors: TradingAgents, FinCon, FinAgent (committee baselines); StockBench, Agent Market Arena (contamination hygiene); the "illusion of compliance" safety-adherence paper (2506.02357) for the anti-gaming metric.

---

## 11. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Obedience still ~trivial after unguarded fix (agents rarely act) | Decoy suite forces two-sided decisions; report action-required failures |
| No real US-vs-NSE gap emerges | Then lead purely on cross-sectional design + calibration; frame US/NSE as robustness, not headline |
| Calibration outcomes not ready by Gate 2 | Ship obedience-only paper; calibration → "preliminary/future" |
| Historical news/fundamentals leak | Restrict E4 to technical/macro/price; state limitation openly |
| 2nd model integration slips | Ship with 1 model + explicit single-model limitation (still poster-viable) |
| Time collision with Ribhu / IITB-RI (23 Sep) / Deeksha | M protects Gates 1–2; O+P own infra/data so M isn't the bottleneck |

---

## 12. Paper skeleton (5–6 pp, `sigconf`; use `BE_PROJECT_ICAIF/sigconf.tex`)

1. **Intro (1 pp)** — problem; the 3 questions; ¶2 pre-empts CLQT + FinPersona; the cross-sectional claim; contributions (benchmark + finding + release).
2. **Related work (0.5 pp)** — §10, differentiation table.
3. **The instrument (1–1.5 pp, capped)** — policies, frozen bundles, agents, risk engine, leakage controls, pre-registration. Explicitly "instrument, not contribution."
4. **Metrics (0.5 pp)** — per-clause taxonomy, competence-conditioned, ECE/Brier/selective-risk, cost.
5. **Experiments & results (2 pp)** — E1 Table 1/2 + Fig 1/2; E3 Fig 5 (the finding); E4 Fig 3 Table 3; E5 Fig 4; returns labelled underpowered.
6. **Limitations (0.3 pp)** — single/2-model, short calibration window, no live loop, news/fundamental calibration scope.
7. **Conclusion + artifact link (0.2 pp).**
- `\documentclass[sigconf]{acmart}` · `\settopmatter{printacmref=false}` · `\setcopyright{none}` · names ON (single-blind) · unlimited refs/appendix.

---

*Written 8 Sep 2026. Gates are hard. If Gate 1 slips, cut scope, don't slip the deadline.*
