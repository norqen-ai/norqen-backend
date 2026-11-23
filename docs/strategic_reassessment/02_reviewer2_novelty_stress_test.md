# 02 · Reviewer #2 Mode — Novelty Stress Test

**Rule of this document:** I do not assume the project is novel. I try to *reject* it, cite the closest work, decide if the criticism is valid, and redesign until no major novelty objection survives — while keeping everything buildable by three final-year students. Nothing is preserved just because a doc already exists for it.

**What I am NOT changing:** the core thesis. The team already made the correct pivot — *research object = the agent's obedience/honesty/efficiency, not the market's returns*. That is right and is confirmed by the field (StockBench, Agent Market Arena, "The Alpha Illusion"). This document pressure-tests that thesis; it does not replace it.

---

## PART A — Three Area-Chair rejections, each followed by a redesign

I wrote the strongest rejection I could, three times. After each, the project is redesigned so that rejection is no longer valid. This is iterative on purpose.

### Iteration 1

> **REJECT — "System paper wearing an evaluation costume."**
> The paper describes a multi-agent LLM trading system with a policy input, specialist agents, a risk veto, and an audit log, then reports some metrics. Every one of those components exists in open-source products (Vibe-Trading, 30k⭐) and in prior research (TradingAgents, FinCon, FinAgent). The three "research questions" are a checklist of known techniques — adherence (FinPersona-Bench), calibration (a decade of ECE/Brier work), cost-aware stopping (CLQT, BATS). There is no single crisp contribution; there is a competent integration. Workshop is about *ideas*, not integrations. **Reject.**

**Is it valid?** *Yes, largely.* This is the most likely rejection and it is fair against the project *as currently framed* (three parallel RQs, system-forward).

**Redesign 1 — collapse three RQs into one artifact-centered contribution.**
- The contribution is **not** "we answer RQ1/2/3." The contribution is **one released instrument**: a *leakage-free, cross-sectional, multi-market benchmark + scorer that measures whether ANY LLM trading agent obeys a written mandate, reports honest confidence, and stops gathering evidence efficiently — on the SAME frozen evidence.* RQ1/2/3 become **demonstration experiments run on the instrument**, not the contribution itself.
- Reframe the system to ≤1.5 pages, explicitly "the instrument, not the finding" (your workshop plan §8 already commits to this — enforce it).
- Headline becomes the *benchmark + the cross-sectional identical-evidence design*, which is the one thing no competitor has.

### Iteration 2

> **REJECT — "Scooped by FinPersona-Bench."**
> FinPersona-Bench (Jun 2026) already assigns behavioral mandates from strict-conservative to aggressive across 18 LLMs, measures whether the mandate is followed, and tests mandate re-grounding. Your RQ1 and your "policy re-injection fix" are their contribution with a different market wrapper. Concurrent, published first, larger model sweep. **Reject on novelty.**

**Is it valid?** *Partially.* FinPersona-Bench is genuinely the closest work and *will* be cited by a reviewer. But it differs on axes you can own — if you sharpen.

**Redesign 2 — move to the axis FinPersona-Bench does not occupy.**
| FinPersona-Bench | Your redesign |
|---|---|
| **Longitudinal** — one mandate erodes over time | **Cross-sectional** — *many* mandates on the **same** frozen evidence, measuring divergence *between* mandates at a single decision moment |
| **Synthetic** market (price decoupled from hidden value) | **Real** US + NSE market evidence, leakage-controlled by training-cutoff + live logging |
| Aggregate "salience decay" score | **Per-clause violation taxonomy** (forbidden-tool used? sizing bound broken? horizon-inappropriate tool? confidence-threshold ignored?) — a structured, reusable scorer |
| Re-grounding as their result | You **replicate** their temporal decay finding in a real agentic loop (independent confirmation in a new setting = a valued contribution) and treat re-injection as *their* idea you validate, not yours |
| Not released as a cross-mandate real-market artifact | **You release** the bundles + policies + scorer |
- Net: RQ1 is no longer "do mandates matter" (scooped) but "**how do we measure cross-sectional mandate obedience on real evidence, and does it transfer across markets (US↔NSE) and models?**" — an orthogonal, releasable axis.

### Iteration 3

> **REJECT — "The metrics are gameable; the results will be uninterpretable."**
> A do-nothing agent that always outputs WAIT/abstain scores ~100% policy adherence and perfect calibration (never acts, never wrong). So "high adherence" proves nothing. Meanwhile 4 months of live trading on ~40 stocks yields a few hundred decisions — far too few for calibration curves or Sharpe with confidence intervals. The paper will either report a trivially-obedient system or an underpowered one. **Reject on construct validity + statistical power.**

**Is it valid?** *Yes — this is the sharpest and most dangerous objection, and it is real.* (It is exactly the "illusion of compliance" from *Evaluating LLM Agent Adherence to Hierarchical Safety Principles*, 2506.02357.)

**Redesign 3 — make the metrics un-gameable and the N sufficient.**
- **Un-gameable adherence:** never report adherence alone. Report the pair **(violation rate, competence)** where competence = *non-trivial action rate* and *selective accuracy at matched coverage*. A do-nothing agent has 0 violations but ~0 coverage → visibly useless. Define this in the pre-registered metric doc **before** logging.
- **Add a decoy/trap suite:** inject decision moments where obeying the policy *requires* acting (clear signal within mandate) and moments where it requires abstaining (forbidden-evidence-only). A trivial agent fails the first set; a reckless agent fails the second. This turns adherence into a two-sided test.
- **Sufficient N without pretending:** the **headline adherence claim comes from frozen-evidence replay** (500+ bundles × 4 policies × 3 models × 3 repeats ≈ 18,000+ scored decisions) — legitimately high-N because replay is cheap and deterministic. The **live loop** is used only for (a) drift-over-time (E2, needs calendar time, not N) and (b) qualitative "it ran in reality" evidence. **You never claim a returns difference is significant** — you state openly that 4 months is underpowered for Sharpe and report it as a labelled secondary. This converts the power objection from a weakness into a stated scope decision.

**After three iterations, the surviving contribution is:**
> A **leakage-free, cross-sectional benchmark and scorer** for **mandate obedience** (with un-gameable competence-conditioned metrics), extended with **honesty (calibration)** and **efficiency (evidence cost)** measured on the **same** frozen real-market evidence across **US and NSE** and **≥3 model families**, **released** so others can score their own agents.

No remaining rejection is fatal *to that framing*. Remaining objections (single team, few models vs FinPersona's 18, short live window) are **limitations to state**, not novelty holes.

---

## PART B — Attack every research question

For each RQ: why publish / why NOT / closest work / would a reviewer call it incremental / how to make it stronger without making it unbuildable.

### RQ1 — Steerability / policy adherence *(the headline — keep)*
- **Why publish:** nobody measures cross-sectional obedience on *identical real-market evidence* with a per-clause violation taxonomy and a released scorer. Products *enforce* mandates; they never *test* obedience.
- **Why NOT:** FinPersona-Bench measures mandate adherence already; "does a policy change behavior" is nearly answered.
- **Closest:** FinPersona-Bench (2606.31522); hierarchical-safety-adherence (2506.02357); Vibe-Trading's mandate model (product).
- **Incremental?** Only if framed as "do mandates matter." **Not** incremental if framed as "cross-sectional, real, released, competence-conditioned, cross-market transfer."
- **Stronger, still buildable:** add the two-sided decoy suite (act-required vs abstain-required moments) and the US↔NSE transfer question. Both are logging/scoring work, no new modeling.

### RQ2 — Confidence honesty / calibration *(keep, but demote to second)*
- **Why publish:** calibration of *policy-conditioned* agent confidence, per-market, tied to *sizing/drawdown* impact, is unstudied. Whether one calibration map transfers US↔NSE and across policies is a real question.
- **Why NOT:** calibration (ECE/Brier/temperature/conformal) is textbook; trading-specific per-order calibration is *already appearing* in 2026 work. Alone, RQ2 is not a contribution.
- **Closest:** general LLM calibration literature; FinAbstain (2607.24875, calibrated abstention in finance); multi-agent calibration (2605.30653).
- **Incremental?** **Yes, as a standalone.** Not incremental only as "calibration *under policy conditioning*, and its interaction with adherence" (does obeying a strict mandate hurt calibration?).
- **Stronger, still buildable:** report calibration **per-policy × per-market**, and the interaction "adherence↑ ⇒ calibration?" — a plot you get for free from the same logs.

### RQ3 — Evidence efficiency / cost–quality *(keep as third, never headline)*
- **Why publish:** ties the stopping rule to the *policy's own* confidence threshold + budget, jointly with obedience and honesty.
- **Why NOT:** CLQT, Calibrate-Then-Act, BATS already own cost-aware agent evaluation.
- **Closest:** CLQT (2606.29771), BATS (2511.17006), Calibrate-Then-Act (2602.16699).
- **Incremental?** **Yes** on its own. Survives only as the third axis on the shared frozen evidence.
- **Stronger, still buildable:** show the cost–quality frontier *shifts with the policy* (a conservative mandate should rationally spend more before acting) — that links RQ3 back to RQ1 and is unique to policy-conditioning.

**Verdict on RQs:** RQ1 is the paper. RQ2 and RQ3 are supporting axes that are only defensible *because they share the frozen-evidence instrument with RQ1*. If you ever present them as three co-equal contributions, you invite Iteration-1's rejection.

---

## PART C — Novelty stress test (the remove-the-component filter)

*"If this component were removed entirely, would the paper still be publishable? YES ⇒ engineering. NO ⇒ part of the research contribution."*

| Component | Remove it — still publishable? | Classification |
|---|---|---|
| Frozen-evidence replay harness (bundles) | **NO** — no cross-sectional identical-evidence claim without it | **RESEARCH (core)** |
| Per-clause adherence scorer | **NO** — RQ1 is unmeasurable | **RESEARCH (core)** |
| The 4 policy files + schema (pre-registered) | **NO** — no cross-sectional axis, no released artifact | **RESEARCH (core)** |
| Competence-conditioned metric (anti-gaming) | **NO** — Iteration-3 rejection returns | **RESEARCH (core)** |
| Calibration analysis (RQ2) | Weaker but yes | RESEARCH (secondary) |
| Cost–quality sweep (RQ3) | Weaker but yes | RESEARCH (secondary) |
| Live paper-trading loop | Yes for RQ1; **NO** for the drift result (E2) & "it runs in reality" credibility | RESEARCH (supporting) + PRODUCT |
| LLM specialist agents (tech/news/fund/macro) | **Yes** — they are the system under test, swappable | ENGINEERING (instrument) |
| Risk-veto engine | **Yes** — instrument for a clean baseline; Vibe-Trading has one | ENGINEERING (instrument) |
| Deterministic ML tools (XGBoost/HMM) | **Yes** — any numeric tool works | ENGINEERING |
| Streamlit/Next.js dashboard | **Yes** — pure product | PRODUCT |
| Memory (Postgres+pgvector) | **Yes** | PRODUCT / future |
| NSE support | Yes for novelty (Vibe-Trading has it); **matters** for the *transfer* question & product reach | ENGINEERING + PRODUCT |

**Implication for the next 8 weeks:** protect the four RESEARCH-core rows with your life; they are cheap (logging + scoring code, no GPUs). Everything classified ENGINEERING/PRODUCT is *cuttable under time pressure* — exactly the scope-cut order your workshop plan already lists.

---

## PART D — Architecture justification (justify every box)

Every box in `architecture_detailed.png`, scored. Research value / Product value / Build complexity on 1–10.

| # | Box | Why it exists | RQ served | Experiment depending on it | Remove ⇒ novelty↓? | Remove ⇒ product↓? | Build | Research | Product | Verdict |
|---|---|---|---|---|---|---|---|---:|---:|---:|---|
| 1 | Data sources | raw evidence | all | all | no | yes | 4 | 3 | 8 | **Keep** |
| 2 | Data pipeline (validate/timestamp) | leakage control | all | leakage-free protocol | **yes** (timestamps = no-leakage proof) | yes | 5 | 7 | 6 | **Keep** |
| 3 | Policy-conditioned planner | the thing under test | RQ1,RQ3 | E1,E4 | **yes** | yes | 8 | 9 | 7 | **Keep** |
| 4 | LLM specialist agents | generate evidence/analysis | RQ1 | E1 | no (swappable) | yes | 7 | 4 | 7 | **Keep, cap at 4** |
| 5 | ML tool layer | numbers not from LLM | RQ2 | E3 | no | med | 6 | 5 | 5 | **Keep, minimal** |
| 6 | Risk engine (veto) | clean deterministic baseline | RQ1 | E1 veto stats | no (Vibe has it) | yes | 3 | 4 | 8 | **Keep (cheap, done)** |
| 7 | Paper execution | realized outcomes | RQ2 | E2,E3,E5 | no | yes | 6 | 5 | 7 | **Keep** |
| 8 | Logging / replay / evidence bundle | **the instrument** | all | E1–E4 | **YES (core)** | med | 6 | 10 | 5 | **Protect** |
| 9 | Research outputs (scorer, calibration, cost) | the contribution | all | E1–E4 | **YES (core)** | low | 5 | 10 | 3 | **Protect** |
| 10 | Memory (pgvector) | recall | none directly | none | no | med | 6 | 2 | 5 | **Defer / cut first** |

**One-glance takeaway:** boxes 8 & 9 are your entire novelty and are *low-build-complexity* (logging + analysis code). Box 10 (memory) is high effort, ~zero research value → **first to cut**. This is the correct engineering-hours allocation.

---

## PART E — Optimize for reviewer impact per engineering hour

Objective is **not** biggest architecture / most agents / most APIs / fanciest dashboard. It is **maximum reviewer impact per engineering hour.** Ranked by (research value ÷ build cost):

1. **Adherence scorer + pre-registered metric doc** — highest ratio. ~1 week. Unlocks the headline. **Do first.**
2. **Frozen-evidence bundle format + deterministic replay** — already partly built (`bundle.as_tools()` works, replay test passes). Harden it. **Second.**
3. **Competence-conditioned + decoy suite** — ~days of scoring logic. Neutralizes the deadliest rejection. **Third.**
4. **One real LLM agent (Technical) end-to-end** — proves the loop is real, not a stub. **Fourth.**
5. Calibration notebook (RQ2) — reuse `netcal`/`MAPIE`, ~1 week once outcomes accrue.
6. Cost sweep (RQ3) — a loop over `evidence_budget` on cached bundles.
7. Dashboard polish, memory, extra agents — **only if everything above is done.**

Whenever two solutions exist, take the simpler one unless the complexity buys a *measurable* research result.

---

## PART F — Your one-sentence contribution

If a reviewer remembered only one sentence:

> **"We release the first leakage-free, cross-sectional benchmark and scorer that measures whether an LLM trading agent actually obeys its investor's written mandate — and show today's agents are steerable yet mandate-erosion-prone and poorly calibrated, consistently across US and Indian markets and three model families."**

Everything in the paper, the system, and the Saturday slides should ladder up to that sentence. If a component doesn't serve it, it's product or it's cut.

---

## PART G — Design the paper backwards (build toward these, nothing else)

Assume it's accepted. These are the exhibits. Build the system until they're producible; ignore features that don't feed one.

- **Figure 1 — The money-shot.** Same frozen NVDA/RELIANCE evidence → 4 policies → 4 different, mandate-compliant decision cards; one gets vetoed. (*You can already render a 2-policy version today.*)
- **Figure 2 — Cross-policy divergence heatmap.** Decisions × policies, colored by action/size; shows the system is steerable, not "one average behavior."
- **Figure 3 — Reliability diagram** (confidence vs realized accuracy) per policy, before/after calibration; the honesty result.
- **Figure 4 — Cost–quality frontier** across evidence budgets, one curve per policy (conservative spends more — ties to RQ1).
- **Figure 5 — Drift plot** (adherence vs live week) replicating FinPersona-Bench's decay in a real loop.
- **Table 1 — Per-clause violation rates** × 4 policies × 3 models, with 95% CIs. *The headline table.*
- **Table 2 — Competence-conditioned adherence** (violation rate | non-trivial action rate) — the anti-gaming table.
- **Table 3 — Calibration (ECE/Brier)** per policy × market, and transfer (US-fit map applied to NSE).

If a planned component feeds none of Fig 1–5 / Table 1–3, it is not research — defer it.

---

## PART H — Final novelty verdict

**Scale:** DISTINCT · PROMISING-BUT-NEEDS-REFRAMING · MOSTLY-ENGINEERING · HEAVILY-DUPLICATIVE · NOT-PAPER-WORTHY

| Dimension | Verdict |
|---|---|
| **As currently framed (3 co-equal RQs, system-forward)** | **PROMISING BUT REQUIRES REFRAMING** — invites the Iteration-1 rejection |
| **After the redesign above (artifact-centered, competence-conditioned, cross-sectional)** | **DISTINCT AND RESEARCH-WORTHY** for a workshop (not a main track) |
| BE academic-project value | **High** — well-scoped, genuine systems + ML + evaluation, SDG-alignable, demonstrable now |
| Product value | **Medium** — crowded by Vibe-Trading; defensible only on *trust/auditability for the Indian retail/analyst niche* (see doc 03) |
| Research novelty | **Medium-High** *conditional on* leading with the released benchmark + cross-sectional design |
| Technical / data / experimental feasibility | **High** — CPU-only, paper trading, public data; the core is logging + scoring |
| ICLR FinAI workshop fit | **Good** — the 2026 edition explicitly wanted *agentic + responsible* finance, not return-chasing; this is squarely that |
| **Biggest threat to validity** | **Construct validity (gameable adherence)** and **being out-sharpened by FinPersona-Bench.** Both are handled *only* by the Redesign-2 and Redesign-3 moves. Do them before the metric doc is frozen. |

**Bottom line:** the idea is *not* dead and is *not* "the same thing everyone built." The *architecture* is commoditized (correctly worrying) but the *evaluation-science* framing is defensible **if you reframe from a system paper to a released cross-sectional benchmark with un-gameable metrics** and cite/differentiate FinPersona-Bench and CLQT in the first two paragraphs. Do that and Reviewer #2's strongest attacks are pre-empted.
