# 00 · START HERE — Strategic Reassessment (6 Aug 2026)

Read in this order:
1. **This file** — the verdict and the seven next actions.
2. `01_competitor_kill_matrix.md` — verified landscape; what to stop claiming.
3. `02_reviewer2_novelty_stress_test.md` — 3× Area-Chair rejection→redesign; the defensible core.
4. `03_product_strategy.md` — the product wedge (don't build "another platform").
5. `04_saturday_demo_plan.md` — compliance matrix, live-demo script, Q&A.
6. Deck: `../05_Evaluation_PPT/BE_Project_Evaluation_Group02.pptx` (also in `~/Downloads/`).

---

## A. Bottom-line verdict

**The original idea, *as a system*, is NOT sufficiently novel — and you already knew it, which is why your synopsis correctly pivoted to studying the agent's behaviour.** Verified on 6 Aug 2026: the architecture (multi-agent committee, mandate input, risk veto, audit log, even NSE support) is fully commoditised — Vibe-Trading (30k★, MIT) ships all of it; hobbyists build it in a weekend. **But the project is defensible as an *evaluation-science* contribution** — measuring obedience, honesty, and evidence-cost, leakage-free and cross-sectionally, released as a benchmark — which *no* product and *no* single benchmark does. Verdict: **PROMISING-BUT-NEEDS-REFRAMING → DISTINCT** once you lead with the released benchmark, not the system. You are not "doing the same thing again"; you are doing the *measurement* everyone else skipped.

## B. Recommended pivot (≤200 words)

Keep the thesis; sharpen the framing. Stop presenting a *system*; present an **instrument + finding**. Contribution = **the first leakage-free, cross-sectional benchmark and scorer that measures whether an LLM trading agent obeys its investor's written mandate**, extended to confidence-honesty (calibration) and evidence-efficiency (cost) on the *same* frozen real-market evidence, across **US + NSE** and **≥3 model families**, **released** so others can score their own agents. The multi-agent system is the *instrument under test* (≤1.5 pages), not the claim. Differentiate hard from **FinPersona-Bench** (they: longitudinal, single-mandate, synthetic; you: cross-sectional, many-mandate, real, released) and **CLQT** (cost-only). Make adherence **un-gameable** by always pairing it with a non-trivial-action rate + decoy moments, so a do-nothing agent can't score perfectly. Report returns only as an openly-underpowered secondary. This survives the three strongest Area-Chair rejections (system-in-costume, scooped-by-FinPersona, gameable-metrics) — each pre-empted in `02_*`.

## C. Why this is not just another trading-agent dashboard (5 implementable, evaluable differentiators)

1. **Cross-sectional identical-evidence adherence** — freeze one evidence bundle, run 4 policies × 3 models × repeats, score per-clause violations. (No competitor does cross-sectional.)
2. **A released benchmark artifact** — 500+ frozen bundles + policies + adherence scorer + leaderboard. (Products never release benchmarks.)
3. **Joint obedience × honesty × cost on the same decision** — enables "does stricter obedience cost calibration?" (Others isolate one axis.)
4. **Leakage-free on real US + NSE** — post-cutoff replay + live loop, per-model cutoffs documented. (FinPersona is synthetic.)
5. **Un-gameable metrics** — adherence conditioned on competence + two-sided decoy suite. (Pre-empts the deadliest reviewer objection.)

## D. Research-paper contribution

- **Main RQ:** Given identical, time-valid evidence, do machine-readable investor policies produce measurably different, mandate-compliant agent behaviour — and how honest and efficient is that behaviour — under leakage-free evaluation across US and Indian markets?
- **Primary hypothesis:** agents are *steerable* (policies change behaviour measurably) but *imperfectly obedient*, *mandate-erosion-prone over time*, and *poorly calibrated* — consistently across models.
- **Baselines:** B0 market/majority · B1 non-LLM quant · B2 single general LLM · B3 prompted-financial LLM · B4 multi-agent no-debate · B5 committee · B6 +verifier · B7 +calibration+abstention.
- **Key metrics:** per-clause violation rate (+ competence-conditioned) · cross-policy divergence · ECE/Brier/reliability · selective accuracy · cost–quality frontier. Returns/Sharpe = secondary, with CIs, labelled underpowered.
- **Dataset/benchmark contribution:** released frozen-evidence bundles (US+NSE) + 4 policy files + adherence scorer + leaderboard script.
- **Biggest threat to validity:** construct validity (gameable adherence) and being out-sharpened by FinPersona-Bench. Both neutralised only by the Redesign-2/3 moves in `02_*` — do them *before* freezing the metric doc.

## E. Product contribution

- **Primary user:** Indian retail investor / independent analyst who wants explainable, auditable, mandate-respecting NSE research and will **never** use a CLI. **Secondary:** students/researchers who benchmark against your released artifact.
- **Pain point:** trust-starved, drowning in finfluencer/Telegram tips; needs *defensible, logged* reasoning, not a black-box "BUY".
- **Core workflow:** pick stock + policy → time-valid evidence → agents analyse → risk may VETO → **Decision Card** (thesis, counter-thesis, dated sources, binding clauses, invalidation conditions, abstain/act) → logged → adherence badge + veto log.
- **Why not World Monitor / Vibe-Trading:** World Monitor is a monitoring dashboard (no decisions); Vibe-Trading is a *developer* tool optimising capability. You win on **no-code, explanation-first, mandate-auditable** — exactly what they ignore.
- **What must NOT be in the MVP:** real-money execution; a global dashboard; a second market beyond US+NSE; anything competing with Vibe-Trading on developer capability; accounts/billing before 10 real users.

## F. Current progress (repository-verified only)

**VERIFIED IMPLEMENTED** (runs today, `code/`):
- Policy schema + 4 investor policies (`config/policies/*.json`).
- Shared contracts `EvidenceItem` / `DecisionCard` / `PortfolioState` (`src/core/schemas.py`, v1.0).
- Rule-based policy-conditioned planner stub (`src/agents/planner.py`).
- Deterministic risk engine with absolute veto (`src/risk/engine.py`).
- Decision log (JSONL) + frozen-evidence bundle + **deterministic replay** (`src/audit/log.py`).
- `run_demo.py` → same NVDA evidence: conservative WAIT, aggressive BUY 6.41%, oversize trade VETOED. **Verified.**
- `tests/test_core.py` → **5/5 pass** (incl. replay determinism, cross-policy divergence).
- Two professional architecture diagrams; synopsis (dept format); 40+-paper reading list; per-member plans.

**PARTIAL:** planner is a stub (not LLM/LangGraph yet); predictor + market fetcher are starters.
**PLANNED:** LLM agents, real ML tools, data pipeline, paper execution, live loop (Oct gate), calibration/adherence scorers, dashboard.
**BLOCKED/TODO:** `git init` not yet run (code not under version control).

Honest completion: **~20%** — exactly what Progress Evaluation-I expects.

## G. Saturday evaluation

- **PPT:** `05_Evaluation_PPT/BE_Project_Evaluation_Group02.pptx` (+ `~/Downloads/`).
- **Slides:** 19, with speaker notes on each.
- **Rubric compliance:** all 8 sections / 25 marks covered — matrix in `04_*` §2.
- **Demo:** `run_demo.py` + `tests/test_core.py` (offline, no keys) — script in `04_*` §3.
- **Needs human input:** (1) confirm Sat/Sun date (notice says "09/08 Saturday" but 9th is Sunday); (2) confirm Group No. 02 on the sheet; (3) `git init` tonight; (4) print 4 papers; (5) one rehearsal; (6) all 3 members attend with the evaluation sheet.

## H. Next seven actions (ordered)

1. **Tonight:** `git init` in `code/` + push to a private repo (commands in `code/README.md`). Reproducibility is a paper requirement and an evaluator question.
2. **Before Saturday:** rehearse the deck + live demo once (~12–15 min); print the 4 papers; confirm the date and Group No.
3. **This week:** freeze **policy schema v1.0 + metric definitions** in a committed `PREREGISTRATION.md` — including the **competence-conditioned adherence** definition (do this *before* any logging, or Reviewer-3's objection returns).
4. **Rewrite the intro framing** (in the paper skeleton) to lead with the *released benchmark*, and cite+differentiate FinPersona-Bench and CLQT in the first two paragraphs.
5. **Weeks 1–2 (Malhar):** data pipeline for ~20 US + ~20 NSE large-caps, one command refresh; commit `config/universe.json`.
6. **Weeks 1–4 (Omkar):** replace the stub with a LangGraph planner + the first real LLM agent (Technical), keeping `tests/test_core.py` green; log every prompt.
7. **Protect the Oct hard-gate:** the live paper-trading loop must be logging 24×7 by mid-October — 4+ months of contamination-free records is the one thing calendar time alone produces. Cut agents/features before you delay this.

---

### One sentence to remember
> *"We don't ask whether the bot earned — we're the first to prove whether it obeyed, whether its confidence was honest, and whether it knew when to stop — leakage-free, on US and Indian markets, released for anyone to test their own agent."*
