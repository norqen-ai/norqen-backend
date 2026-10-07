# 01 · Competitor Landscape & Kill Matrix (verified)

**Verified:** 6 Aug 2026 by fetching each repository/page directly (not landing-page claims).
**Purpose:** answer the founder's real question — *"so many people already built this, what's the point?"* — with evidence, and tell you exactly which of your current claims to **drop**, **demote**, or **keep**.

---

## 0. The one-paragraph truth

Two of the three links that scared you are **not competitors**: **World Monitor** is a geopolitical situational-awareness dashboard (it does not make a single trade decision), and **awesome-systematic-trading** is a curated *link list*. The one that *is* a real neighbour — **Vibe-Trading (HKUDS, 30k⭐)** — is **closer and more capable than your own workshop plan admits**: it already ships a machine-readable *mandate model*, a *risk committee*, an *audit ledger*, a *kill-switch*, and *India (NSE/BSE) backtesting*. The seb.ai Instagram build shows even hobbyists now assemble "investment-committee + bull/bear debate + risk + paper trading" in a weekend. **Therefore your architecture is commoditized. Your evaluation science is not.** No product or viral build *measures* whether the mandate is actually obeyed, whether the confidence is honest, or what evidence costs — leakage-free, cross-sectionally, on a released benchmark. That gap is the whole project. Everything below is the proof and the list of claims to kill.

---

## 1. Verified feature matrix

Legend: ✅ has it · ⚠️ partial/implicit · ❌ absent · — n/a

| System | Category | Multi-agent committee | Mandate/policy **input** | Risk veto / governance | Backtest | Paper trade | Live | India / NSE | **Measures policy adherence (science)** | **Calibration study (ECE/Brier)** | **Cost–quality frontier** | **Leakage-free protocol** | **Released benchmark + scorer** | Scale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **YOUR PROJECT** | Research + product | ✅ (4–6) | ✅ JSON, 4 policies | ✅ deterministic veto | ✅ replay | ✅ US+NSE | ✅ ≥4 mo planned | ✅ | ✅ **core RQ1** | ✅ **core RQ2** | ✅ **core RQ3** | ✅ post-cutoff + frozen | ✅ **planned artifact** | 3-person BE team |
| **Vibe-Trading** (HKUDS) | Open-source product | ✅ investment/quant/risk committees | ✅ "mandate model", bounded autonomy, mandate gates | ✅ audit ledger, fail-closed, kill-switch | ✅ multi-engine (US/CN/crypto/**India**/KR) | ✅ | ✅ opt-in real brokers | ✅ NSE/BSE | ❌ enforces, never *measures* obedience | ❌ reports IC/Sharpe/IR, not confidence calibration | ❌ | ❌ | ❌ | 30k⭐, MIT |
| **World Monitor** (koala73) | Intelligence dashboard | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | — | ❌ | ❌ | ❌ | ❌ | ❌ | 79k⭐, AGPL-3.0 |
| **awesome-systematic-trading** | Curated list | ❌ | ❌ | ❌ | — (links to libs) | — | — | — | ❌ | ❌ | ❌ | ❌ | ❌ | link catalog |
| **seb.ai** (Instagram, Jul 2026) | Creator/hobby build | ✅ research + bull/bear + risk | ⚠️ persona-style | ✅ risk controls | ✅ | ✅ | ❌ "no real money" | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | viral post |
| **TradingAgents** (2412.20138) | Research | ✅ analyst/researcher/trader/risk | ❌ one fixed goal | ⚠️ risk debate | ✅ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ dates only | ❌ | paper |
| **FinCon** (NeurIPS'24) | Research | ✅ manager–analyst + verbal RL | ❌ | ⚠️ risk control | ✅ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | paper |
| **FinPersona-Bench** (2606.31522) ⚠️ | Research benchmark | ⚠️ single agent w/ profile | ✅ behavioral mandate (conservative→aggressive) | ❌ | — | — (synthetic mkt) | — | ❌ | ✅ **but temporal decay only, synthetic** | ❌ | ❌ | ✅ synthetic-clean | ✅ synthetic | paper+bench |
| **CLQT** (2606.29771) ⚠️ | Research benchmark | ⚠️ | ❌ | ❌ | ✅ closed-loop | — | — | ❌ | ❌ | ❌ | ✅ **cost-aware core** | ✅ | ✅ | paper+bench |
| **StockBench** (2510.02209) | Research benchmark | ✅ agents | ❌ | ⚠️ | ✅ | ✅ live-style | ⚠️ | ❌ | ❌ | ❌ | ❌ | ✅ contamination-free | ✅ | paper+bench |
| **Agent Market Arena** (2510.11695) | Live benchmark | ✅ | ❌ | ⚠️ | — | ✅ live | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ live | ✅ | paper+bench |

**Read the three bold columns.** Every neighbour is ❌ on at least two of {adherence-as-science, calibration study, cost–quality} **and** none combines them with a released cross-policy, leakage-free, US+NSE artifact. That intersection is empty. That empty intersection is your project.

---

## 2. The Kill Matrix (use this verbatim to write Related Work)

| Competitor | What they already solved (stop claiming it) | Are we copying it? | Our *actual* difference | Reviewer verdict on the difference |
|---|---|---|---|---|
| **Vibe-Trading** | Product plumbing: mandate model, committees, risk gates, audit ledger, kill-switch, NSE backtest, 18+ data providers | **Yes, largely** — your product layer ≈ their product layer | We **measure obedience/honesty/cost as science**; they **enforce and log** but never test whether the LLM actually obeys, never calibrate confidence, never publish a benchmark | ✅ Valid *if* you lead with measurement, not features. ❌ Fatal if your paper's contribution reads "we built a mandate-driven committee with a risk veto" — that's their README. |
| **FinPersona-Bench** | *Mandate Salience Decay*: one mandate erodes over **time**; 18 LLMs; tests **re-grounding** (= your "policy re-injection") | Partially — same construct (mandate adherence) | We test **cross-sectional**: *many* mandates on **identical frozen real-market evidence**, per-clause violation taxonomy, **real US+NSE** (they use a synthetic market), and a **released cross-policy bundle set** | ⚠️ Incremental unless sharpened. Reviewer *will* cite this. You must frame as "orthogonal axis (cross-sectional, real, released) + we replicate their temporal finding as validation." |
| **CLQT** | Closed-loop, **cost-aware** diagnostic benchmark for portfolio agents | Partially — your RQ3 overlaps | We tie the stopping rule to the **policy's** confidence threshold + evidence budget, jointly with adherence & calibration, on US+NSE | ⚠️ RQ3 alone is weak next to CLQT. Keep it as a *third* axis, never the headline. |
| **TradingAgents / FinCon / FinAgent / FinMem** | Multi-agent LLM trading that chases returns | The architecture, yes | We change the *question* (obey? honest? efficient?) and the *evaluation* (leakage-free, cross-policy) — returns are secondary/underpowered on purpose | ✅ Valid — but only because of the evaluation, not the agents. Never sell the agents as new. |
| **StockBench / Agent Market Arena / LiveTradeBench** | Clean live/contamination-free benchmarks that ask **"who earns?"** | We borrow their hygiene | We ask **"who obeyed / who was honest / who was efficient?"** — a different dependent variable | ✅ Valid and clean differentiation. Cite as "we adopt their temporal hygiene, change the metric." |
| **World Monitor** | Real-time geopolitical + finance-radar **monitoring** | No — different category | We make **auditable decisions**; they surface signals for humans | ✅ Trivially distinct — don't even put it in Related Work; mention once as "situational-awareness tools are complementary, not decision systems." |
| **awesome-systematic-trading** | A **list** of libraries/strategies/books | No | It's a reference we *use* (vectorbt, backtrader), not a system | Not a competitor. Cite as tooling. |

---

## 3. What this KILLS in your current pitch (act on this before Saturday)

These are claims currently in your README / workshop plan that a reviewer (or a sharp evaluator) will puncture. **Demote them from "novelty" to "instrument/table-stakes."**

1. ❌ **"First NSE / Indian-market track."** Vibe-Trading already backtests NSE/BSE. → **Reframe:** *"first **leakage-free, cross-policy adherence benchmark** that **includes** NSE,"* not "first to touch NSE."
2. ❌ **"Risk veto + audit log as a differentiator."** Vibe-Trading ships fail-closed validation, an audit ledger, and a kill-switch. seb.ai has risk controls. → **Reframe:** the veto is your *deterministic instrument for a clean adherence baseline*, not a feature you invented.
3. ❌ **"Multi-agent committee is our contribution."** Everyone — products, papers, hobbyists — has this. → **Reframe:** the committee is the *system under test*, explicitly "1.5 pages max, the instrument not the contribution" (your own workshop plan §8 already says this — hold that line).
4. ⚠️ **"Policy/mandate as machine-readable input is novel."** Vibe-Trading has a mandate model; FinPersona-Bench assigns behavioral profiles. → **Reframe:** novelty is not that a policy *exists* as input, it's that you **measure cross-sectional obedience to it on identical evidence** and **release the benchmark**.
5. ⚠️ **"Policy re-injection fixes drift" (your stretch fix C).** FinPersona-Bench already showed mandate re-grounding works non-uniformly (helps conservative, hurts aggressive). → **Reframe:** you *replicate and extend* their re-grounding result in a real multi-market agentic loop; that's a valid confirmation, not a new fix. Cite them as the origin.

---

## 4. What SURVIVES — your actual moat (keep and amplify)

Every item here is something **no fetched competitor does**, and each is measurable:

1. ✅ **Cross-sectional identical-evidence adherence.** *Freeze one evidence bundle, run all 4 policies × 3 models × repeats, score per-clause violations and cross-policy divergence.* FinPersona-Bench is longitudinal-single-mandate; you are cross-sectional-many-mandate. Genuinely new axis.
2. ✅ **A released, reusable artifact.** 500+ frozen real-market evidence bundles + 4 policy files + an adherence scorer + a leaderboard script. Products don't release benchmarks; this is the biggest acceptance lever ("people will build on this").
3. ✅ **Joint obedience × honesty × efficiency on the *same* decisions.** Others isolate one axis (FinPersona=obedience, calibration lit=honesty, CLQT=cost). You measure all three on one frozen datum — enabling questions like "does higher adherence cost calibration?"
4. ✅ **Leakage-free by construction, on real US + NSE.** Post-training-cutoff replay + a live paper loop, documented per model. Real markets, not synthetic (FinPersona) — with the discipline of the benchmark papers.
5. ✅ **The "illusion of compliance" guardrail** (see doc 02 §Reviewer-2). You explicitly report adherence **conditional on a non-trivial action rate**, so a do-nothing agent can't win. Almost nobody does this; raising it *pre-emptively* is a credibility signal.

---

## 5. Sources (verified 6 Aug 2026)

- Vibe-Trading — https://github.com/HKUDS/Vibe-Trading · https://vibetrading.wiki/home/ (30k⭐, MIT; mandate model, risk committee, audit ledger, kill-switch, NSE/BSE backtest, Alpha Zoo 460 factors)
- World Monitor — https://github.com/koala73/worldmonitor · https://www.worldmonitor.app/ (79k⭐, AGPL-3.0; monitoring dashboard, no trade decisions)
- awesome-systematic-trading — https://github.com/paperswithbacktest/awesome-systematic-trading (curated list; no LLM agents)
- seb.ai Instagram build — https://www.instagram.com/p/DauS_vfFCHE/ (accessed: AI "investment committee" on Claude Fable; research + bull/bear debate + backtest + risk + paper trading; "no real money until proven"; 4.4k likes / 6.9k comments)
- FinPersona-Bench — https://arxiv.org/abs/2606.31522 (Mandate Salience Decay; 18 LLMs; synthetic market; mandate re-grounding non-uniform)
- CLQT — https://arxiv.org/abs/2606.29771 · StockBench — https://arxiv.org/abs/2510.02209 · Agent Market Arena — https://arxiv.org/abs/2510.11695
- "The Alpha Illusion" — https://arxiv.org/abs/2605.16895 (reported alpha ≠ deployment evidence — a motivation citation for your intro)
- "Evaluating LLM Agent Adherence to Hierarchical Safety Principles" — https://arxiv.org/abs/2506.02357 (the *illusion of compliance* / cost-of-compliance framing you must engage)

> ⚠️ **Team action:** the 2606.x / 2607.x arXiv IDs are from June–July 2026, after any model's knowledge cutoff. Re-open each before you cite it in the paper and confirm the exact claim — do not quote from this file alone.
