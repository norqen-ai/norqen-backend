# A. Novelty threat deep read (4 Oct 2026)

**Project assessed:** "A Policy-Conditioned Multi-Agent LLM Framework for Auditable, Evidence-Driven Trading Decision Support" (PICT BE, repo `malharinamdar/policy-trading-agents`).
**Reviewer stance:** skeptical. Every paper below was opened and read from its full text (arXiv PDF → `pdftotext`, or the local PDF). Any paper I read only at the abstract level is labelled **[abstract only]**. No page failed to load. arXiv version and date are given for each paper because several were revised after the plan in `ICAIF_2026_AI4F_Month_Plan.md` was written.

---

## 0. Bottom line (read this if nothing else)

1. **The system is not novel at all.** Since August 2026, several papers already ship the same parts: an LLM-proposes / deterministic-layer-enforces pipeline, natural-language mandates compiled to typed constraints, frozen-evidence replay, and audit logs. See OpenPM (2608.09988), CLQT (2606.29771), BiasMix-Finance (2608.28646), Auditing-as-Executable-Actions (2606.27570) and ReguSim (2608.19974). Give the system ≤1 page and call it "the instrument".
2. **The basic RQ1 claim, "different mandates produce different decisions," is already shown.** PortBench v5 (12 Sep 2026) compares matched model-date pairs. Going from conservative to aggressive raises risk-asset exposure by +0.177 in 103/110 pairs. ReguSim measures a 30.9 pp aggressive-minus-conservative gap in rejected orders.
3. **The planned "unguarded vs guarded" measurement is also largely taken.** BiasMix-Finance reports first-pass mandate violations of 47.6–85.7%, which projection brings to 0%. CLQT's Discipline axis uses a pre-reconciler self-constraint rate plus clip dependence. OpenPM separates raw adherence from post-critic adherence. BiasMix's co-authors include **Raj Dandekar, Rajat Dandekar and Sreedath Panat (all on vizuara.com addresses)**, and it was accepted at the **ICLR 2026 FinAI workshop**. That is your intended ICLR-27 venue, and it looks like the same Raj Dandekar who is on your letter list. You must cite it and build on it explicitly.
4. **What survives, and is genuinely open:** whether the deterministic layer's interventions **help or hurt realized decision outcomes**, clause by clause and mandate by mandate. CLQT credits its drawdown edge to the constraint layer "by elimination", because it never ablates that layer on its own. BiasMix measures no returns at all. OpenPM finds the mandate caps never bind and runs one mandate only. Policy-as-Skill gives the exact analysis template (§5.3).
5. **Also surviving, but secondary:** (a) a cross-mandate design on a byte-identical evidence pool with a same-mandate re-run noise floor (nobody has this); (b) ECE/Brier of the agents' stated confidence against realized outcomes (Alpha Illusion asks for it, no paper I read measures it for trading agents); (c) NSE India coverage (no threat paper uses it, but it is not a contribution on its own).
6. **Correction to the existing plan:** "identical evidence across models" is no longer ours. OpenPM replays byte-identical analyst captures across 5 constructor models. The load-bearing design claim has to narrow to **identical evidence × mandates × enforcement counterfactual × noise floor**.

---

## 1. Papers read and how they were verified

| # | Paper | arXiv / source | Version read | Notes |
|---|---|---|---|---|
| 1 | CLQT | 2606.29771 | v3, 12 Sep 2026 (v1 29 Jun 2026) | 53 pp; read in full incl. appendices |
| 2 | FinPersona-Bench | 2606.31522 | v2, 1 Jul 2026 | 29 pp; read in full incl. appendices |
| 3 | Persona collapse in LLM advice | 2607.08326 | v1, 9 Jul 2026 | "Working draft"; read in full |
| 4 | The Alpha Illusion | 2605.16895 | v1, 16 May 2026 | position paper; read in full incl. appendices |
| 5 | TradingAgents | 2412.20138 + local PDF + website + GitHub releases | local 27-pp PDF; arXiv v1, v4, v7 | see §2.5 for what changed |
| 6 | Policy-as-Skill | local `2609.27087v1.pdf` (also live on arXiv, 22 Sep 2026) | v1 | 6 pp; read in full |
| S1 | OpenPM | 2608.09988 | v1, 6 Aug 2026 | read in full (**biggest new threat**) |
| S2 | PortBench | 2605.27887 | v5, 12 Sep 2026 | main text + profile/PAS appendices read |
| S3 | BiasMix-Finance | 2608.28646 | v1, 14 Aug 2026 | read in full |
| S4 | ReguSim | 2608.19974 | v1, 20 Aug 2026 | main text + trader experiments read |
| S5 | Auditing AI Investment Recs as Executable Actions | 2606.27570 | v1, 25 Jun 2026 | main text read |
| S6 | InvestLogicBench | 2608.06108 | v2, 20 Aug 2026 | main text read |

Abstract-only adjacent hits are listed in §3.7.

---

## 2. The six assigned papers

### 2.1 CLQT: closed-loop, cost-aware, strategy-consistent benchmark (Qu & Chen; arXiv 2606.29771, v1 29 Jun / v3 12 Sep 2026)

**Problem.** Return leaderboards don't certify an agent's process. The paper argues for diagnosing a portfolio-management agent rather than ranking it.

**Method.**
- **Loop and data integrity:** a closed loop of five stages (gather, analyze, decide, execute, reflect), with point-in-time data access enforced by a "TimeGate".
- **Costs and records:** four cost tiers (fixed bps, square-root, Almgren–Chriss) plus financing; every round's record is sealed into a hash chain.
- **Scaffold as a variable:** the same model runs either as a 6-agent "structured" committee (Research, Analyst, PM, Risk Officer, Execution, Reflection) with a Risk-Officer gate, or as one "autonomous" orchestrator with all 19 MCP tools.
- **Mandate handling:** the PM's overlay is logged pre-projection (`mapc_delta_proposed`) and post-projection (`mapc_delta_projected`). It is projected onto the feasible set and passed through a Risk-Officer gate.
- **Five-axis scorecard (APM-CS):**
  - Coherence: 0.5 × signal-action agreement + 0.5 × a held-out LLM judge.
  - Acuity: Spearman ρ of proposed tilts with an informative composite, minus ρ with a noise composite.
  - Composure: turnover-vs-volatility slope plus a consistency score.
  - **Discipline: ½ × (pre-MAPC self-constrained rate) + ½ × (1 − clip dependence).**
  - Reliability: completion × (1 − parse failure) × (1 − truncation).

**Data.**
- Backtest: real US equities, an S&P-100-derived universe (14 core + 58 candidate = 72 names), 26 bi-weekly rounds from 2025-06-16 to 2026-06-12, $1M, LOW cost tier.
- Live: 4 weeks of broker paper trading (18 valid NYSE days, 2026-06-15 to 07-10).

**Models.**
- Backtest: qwen3-235b, gemini-2.5-flash-lite, deepseek-chat-v3.1, gpt-5-mini, claude-haiku-4.5; 5 seeds per reliable configuration.
- Live: minimax-m3, deepseek-v4-pro, qwen3.7-plus, gpt-5.4-mini, gemini-3.5-flash, claude-sonnet-4.6.
- Judges: minimax-m3 (backtest) and GLM-5.2 (live).

**Headline numbers.**
- **Table 5:** the capability leader is deepseek·structured (APM-CS 72.9, Sharpe 2.99). The nominal Sharpe "winner", qwen3·structured (Sharpe 9.82, beats 8/8 baselines), completed only 5/26 rounds and has Reliability 0.19.
- **Coherence gap** (signal-action agreement minus judge score): +0.30 in backtest (0.58 vs 0.28) and +0.23 live (0.63 vs 0.40).
- **Ablations (Table 6):** no module knockout clears the ±0.42-Sharpe repeated-run noise band. Bare-workflow gives ΔSharpe +0.26, range [−0.40, +0.66].
- **Constraints and drawdown (Table 8):** the full agent's MaxDD is −4.1% vs SPY's −8.9% at a similar Sharpe (2.26 vs 2.29). Table 9 attributes this to "investment-target + constraints", which were **not ablated alone**. §7.7.2 says the attribution is by elimination.
- **Discipline (D4), Table 5:** ranges from 0.42 (gpt-5-mini·autonomous) to 1.00 (haiku·structured).
- **Live (Table 10):** claude-sonnet-4.6·auto is top at APM-CS 83.6. Autonomous holds: gemini-3.5-flash 9/18, minimax-m3 8/18; none after the round-14 scaffold fix.

**What it does NOT do (that we do).**
- One standing mandate only. §8.5 says so, and §8.6 lists "vary the standing mandate" as future work.
- No cross-mandate comparison and no identical-evidence design. It is longitudinal on a single market path.
- No ECE/Brier of stated confidence. Its "Coherence" is reasoning-action consistency, not calibration.
- No outcome-conditioned analysis of what the constraint layer changes. No NSE. Artifacts are "on request" only.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 obedience | **Partial→Strong** | Discipline (pre-reconciler self-constraint + clip dependence) is our unguarded-violation metric under another name, but for one mandate only. |
| RQ2 calibration | None–Partial | Coherence ≠ calibration; no ECE/Brier. |
| RQ3 evidence cost | Partial | Module and cluster ablations show more analysis doesn't move Sharpe beyond noise (Fig. 10, Tables 6–7); no adaptive stopping. |
| System design | **Strong** | Mandate-aware synthesis, a deterministic projection plus Risk-Officer gate, proposed-vs-projected logging, hash-chained audit, multi-agent roles. |

**Borrow.**
1. **A repeated-run noise floor.** Re-run the same mandate on the same bundle and treat its divergence as the floor. Any cross-mandate divergence or intervention effect must clear it, as CLQT's ±0.42 band does.
2. **Log `proposed` vs `projected` separately and define Discipline exactly as CLQT does**, so we can cite and compare directly. Report r_self and clip dependence per mandate.
3. **Reliability telemetry** (parse fails, truncation, retries) next to every number.
4. Use **CLQT's own admission that constraints were never ablated alone** as our motivation sentence.
5. The "four cheap checks" in §8.4 (point-in-time stated, reliability telemetry, noise band, held-out judge) belong in our checklist table.

---

### 2.2 FinPersona-Bench: Mandate Salience Decay (Safder et al., MBZUAI; arXiv 2606.31522, v2 1 Jul 2026)

**Problem.** Does a mandate given once at initialization keep governing behaviour over long horizons? The paper calls the erosion "Mandate Salience Decay" (MSD).

**Method.**
- **Market:** a synthetic single-asset engine in which the observable price P_t is decoupled from a hidden fundamental value V_t. Three 200-day scenarios: flat (GARCH-like), crash (panic discount δ), bull-trap bubble.
- **Personas:** three, MBTI-worded with a finance extension. ISFJ = capital preservation (C_ideal = 1.0), INTJ = balanced (0.5), ENTJ = growth (0.2).
- **Arms:** static (mandate in the system prompt only), re-grounded (mandate re-injected every step), and a placebo (length-matched boilerplate re-injected).
- **Output:** Pydantic JSON {action, quantity, rationale}; temperature 0.
- **Metrics:**
  - MAS = mean |C_t − C_ideal|.
  - Caricature Index = maximum drawdown.
  - Rationality Gap = fraction of actions aligned with V_t.
  - Paired Wilcoxon tests, N = 270 pairs.

**Data and models.** Synthetic only, 5 seeds. 18 models: 7 GPT, 3 Claude, 3 Gemini, DeepSeek-Chat, Llama-3.1-8B, Gemma-2-9B, Qwen2.5-7B, Gemma-3-4B.

**Headline numbers.**
- **Table 1:**
  - Flat market: MAS 0.391 static vs 0.342 re-grounded (−12.7%, p = 0.028).
  - Crash: Caricature Index −26.18 vs −22.89 (p = 0.002).
  - Bull trap: Rationality Gap 85.9 vs 78.4 (re-grounding *hurts*, p < 0.001).
- **Drift over time:** the crash static-vs-re-grounded gap grows 4.4× from Q1 to Q4.
- **Re-grounding depends on persona (flat market, Fig. 4):** it helps ISFJ in 17/18 models and worsens ENTJ in 16/18.
- **Placebo (Table 5, Sonnet 4.6, flat):** the placebo sits within 0.003–0.045 MAS of static, while the memory arm moves 0.015–0.173 in a direction that depends on persona.
- **Numerical-only persona (O3, App. G):** the conservative persona is at floor (MAS 0.000 in both arms), and the aggressive over-trading penalty largely disappears (−0.028).

**What it does NOT do.**
- Not real data, not multi-asset, no multi-agent pipeline, no deterministic enforcement layer.
- No frozen-evidence cross-sectional design. Personas share a seed's exogenous price path, but holdings, and therefore prompts, diverge.
- No calibration, no evidence-cost analysis.
- Mandate compliance is a single scalar per scenario, with no clause-level taxonomy.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | **Partial** | Mandate adherence across 3 risk profiles × 18 models is the same construct, but it is longitudinal, synthetic and unenforced. |
| RQ2 | None | |
| RQ3 | None | |
| System | None–Partial | Single LLM with a JSON action schema. |

**Borrow.**
1. **A placebo-policy arm.** Give the agent a JSON policy with the same structure and neutral values, or length-matched boilerplate. This shows decisions differ because of the *content* of the mandate, not its length or position.
2. **The numerical-only ablation (O3).** Compare a JSON-numeric policy, a natural-language persona text, and both together. Their finding that persona vocabulary *amplifies* both help and harm is directly testable in our setup.
3. **Re-grounding as an intervention.** Restating the policy right before the decision helped conservative but hurt aggressive personas. That predicts a policy-by-intervention interaction we should test, not assume away.
4. **Paired Wilcoxon tests matched by (model, ticker, date, seed).**

---

### 2.3 Diagnosing and Repairing Persona Collapse in LLM Advice (Kumar, Vold, Tay, Anderson; arXiv 2607.08326, v1 9 Jul 2026, "working draft")

**Problem.** Do LLM advisors change their posture with the situation, as good human advisors do? Not finance-specific; personal advice on Reddit and similar forums.

**Method.**
- **Persona space:** a 2-D space of hedonic tone H ∈ {−1, 0, 1} by agentic depth E ∈ {−2…2}, giving 5 personas (Healer, Stoic challenger, Technician, Enabler, Doomer). Responses are judged by GPT-5.4-nano.
- **Collapse metrics:** N_eff = 2^entropy of the persona distribution, and JS divergence to the top-rated human distribution. Item-level Cohen's κ and macro-recall.
- **Repair:** Inverse-Process Distillation, a LoRA SFT on a teacher-reconstructed "situational reading" placed before the human reply.

**Data and models.**
- Diagnosis: 1,281 posts across 14 contexts; GPT-5.1, Claude Opus 4.5, Gemini 3 Pro.
- Repair: an 8,262-situation augmented corpus; OLMo3-7B, Llama-3.1-8B, Qwen3-4B. Human study: N = 199.

**Headline numbers.**
- **Humans:** N_eff = 3.80.
- **Frontier models:** GPT-5.1 puts 99.8% of responses in the Healer persona (N_eff 1.02, JS 0.215); Claude Opus 4.5 94.8% (1.29, 0.157); Gemini 3 Pro 89.2% (1.55, 0.123).
- **Plan-First prompting backfires.** On OLMo3, Healer share rises 74.0% → 87.6% and κ falls 0.077 → 0.020.
- **SFT variants:** restore N_eff to 4.08–4.40 and cut JS 50–60% vs baseline in the body text (the abstract says about 80%; the two figures don't match).
- **Human raters prefer the collapsed default.** SFT conditions score 1.4–1.8 points lower on the 7-point scales and are ranked above Instruct only 24–28% of the time.

**What it does NOT do.** Anything financial, any action or outcome, any enforcement.

**Overlap.** RQ1: **None–Partial**. It is conceptual only: "situation-conditioned persona selection" is the advice analogue of policy-conditioned decisions. RQ2: None. RQ3: None. System: None.

**Borrow.**
1. **Measure policy collapse.** Per bundle, compute N_eff of the action distribution across the 4 policies, and the JS divergence between per-policy action distributions. Your own notes (`06_data_architecture`) say cross-policy divergence may be 0% and decisions collapse to WAIT. This is the right metric to report that honestly instead of hiding it.
2. **A "plan-first" ablation.** Ask the agent to restate its mandate and plan before deciding. This paper and FinPersona both suggest it can make adherence worse.
3. **An oracle probe.** Inject the policy-compliant target action as a hint to bound achievable item-level alignment, as their Persona Oracle does.

---

### 2.4 The Alpha Illusion (Ye, Han, … Mandic, Sun, Xu, Xu; arXiv 2605.16895, v1 16 May 2026)

**Problem.** A position paper. It argues that reported alpha from end-to-end LLM trading agents (FinCon, FinMem, TradingAgents, FinAgent, QuantAgent, FLAG-Trader) is not deployment evidence.

**Method.**
- Six minimum reporting protocols, P1–P6: temporal integrity, dynamic universe, counterfactual robustness (view-flip rate under reverse evidence), **epistemic calibration (ECE, reliability curves)**, realistic gross-to-net implementation, and multi-agent disaggregation. They are tiered by how strong the claim is.
- A "modular alternative": LLMs act as auditable information interfaces *upstream* of independent calibration, risk and execution modules.
- A reproduction harness for TradingAgents and QuantAgent.

**Data.** Reproduction over 1 year (2025-01 to 2026-01), equal-weight TSLA/NVDA/KO/XOM/MSTR, $100K, net of commission, token cost, spread and impact.

**Headline numbers.**
- **Sharpe, gross → net:** TradingAgents 0.43 → 0.22; QuantAgent −0.96 → −1.15. Both end below buy-and-hold.
- **End values:** buy-and-hold $104.8K; TradingAgents $106.4K gross / $102.3K net; QuantAgent $81.4K / $77.9K.
- **Unmodeled frictions:** 35 of 40 system × friction-component cells.
- **Cited contamination effect:** FinMem's return drops ≈71.85% and QuantAgent's Sharpe ≈51.48% once the window crosses the model's cutoff (citing Profit Mirage). The FinBen FinTrade Sharpe is 1.51 ± 1.08.

**What it does NOT do.** No new experiment on mandates, obedience, or calibration. It *asks* for ECE but measures none.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | None | |
| RQ2 | **Partial (motivational)** | P4 says any LLM confidence used for sizing must be ECE-audited. That is the exact justification for our RQ2, and no measurement is given. |
| RQ3 | None | |
| System | Partial (supportive) | Our architecture (LLM agents upstream, a separate predictor, a deterministic risk engine with veto, vol-target sizing) *is* their recommended modular alternative. |

**Borrow.**
1. **Frame the paper as an empirical test of Alpha Illusion's modular design**: how much does the independent risk layer actually change, and does that help?
2. **Put a P1–P6 compliance table in the appendix** and limit our language to their "historical backtest / prototype" tier.
3. **Lo (2002) Sharpe standard error** for any return number.
4. **P3 view-flip test.** Inject reverse evidence into a frozen bundle and measure direction / confidence / size flips. It is cheap and identical-evidence native.
5. **Their friction formula** for any net-return reporting.

---

### 2.5 TradingAgents (Xiao, Sun, Luo, Wang; arXiv 2412.20138), and what changed

**What the local 27-page PDF is.** `~/Downloads/26_TradingAgents_Multi_Agents_.pdf` was built 23 Feb 2025. It is the AAAI-format version and matches arXiv v1 (31 Dec 2024) and v4 (25 Feb 2025) text for text. **It is NOT a newer version.** The newest arXiv version is **v7 (3 Jun 2025, 38 pages)**, with the comment "Oral @ Multi-Agent AI in the Real World". v7 only re-formats the paper and moves baselines and metrics into Appendix S1. **Table 1 is numerically identical in v1, the local PDF, v7 and the website.**

**Problem, method, data (all versions).**
- **Roles:** a trading-firm role play with 4 analysts (fundamentals, sentiment, news, technical), Bull and Bear researchers who debate, a trader, a 3-member risk team (Risky / Neutral / Safe debaters), and a fund manager who approves.
- **Mechanics:** ReAct prompting with structured reports. Quick-thinking models (gpt-4o-mini, gpt-4o) handle retrieval; deep-thinking models (o1-preview) handle decisions.
- **Data:** Jan 1 – Mar 29, 2024 backtest on AAPL, GOOGL, AMZN; prices, news, Reddit/X, insider transactions, 60 technical indicators.
- **Baselines:** buy-and-hold, MACD, KDJ+RSI, ZMR, SMA.
- **Metrics:** cumulative return, annualized return, Sharpe, max drawdown.

**Headline numbers (Table 1, unchanged across versions).**
| Ticker | CR | ARR | Sharpe | MDD |
|---|---|---|---|---|
| AAPL | 26.62% | 30.5% | 8.21 | 0.91% |
| GOOGL | 24.36% | 27.58% | 6.39 | 1.69% |
| AMZN | 23.21% | 24.90% | 5.60 | 2.11% |

A footnote concedes the Sharpe is above the plausible empirical range and that the backtest covers only 3 months because of LLM cost.

**What actually changed since Dec 2024.**
1. **Paper:** nothing substantive. No new experiments, metrics, risk-profile-conditioning experiment, calibration or mandate. The "risk profiles" (Risky/Neutral/Safe) have been there since v1, and they are *debaters inside the risk team, not investor mandates*.
2. **Website** (tradingagents-ai.github.io): it is internally inconsistent. It says the data spans January–March 2024 and, in another place, that the trading environment "spanned from June to November 2024". The table is the same.
3. **Code** (GitHub releases, verified via the API): this is where the evolution is.
   - v0.2.4 (Apr 2026): structured outputs and a 5-tier rating.
   - v0.4.0 (31 Aug 2026): point-in-time / look-ahead fixes, and FRED macro vintages pinned to the as-of date.
   - **v0.5.0 (18 Sep 2026):** point-in-time integrity on every dated path, "decisions recorded as they were made", a backtest grid over tickers × dates, the caller's portfolio as run input, SEC EDGAR fundamentals as filed.
   - v0.6.0 (3 Oct 2026): HTML reports.
   - **No release adds investor-mandate or policy parameterization.**
4. **Tauric's newer paper is Trading-R1** (arXiv 2509.11420, Sep 2025; SFT + RL). It is out of window and unrelated to mandates.
5. **Independent reproduction:** Alpha Illusion's 1-year, 5-ticker run gives TradingAgents Sharpe 0.43 gross / 0.22 net, below buy-and-hold (§2.4). Cite that, not the 8.21.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | None | No mandate / policy conditioning experiment. |
| RQ2 | None | |
| RQ3 | None | |
| System | **Strong** | Multi-agent analyst roles, a risk team, LangGraph-style orchestration, and point-in-time logging in the 2026 code. |

**Borrow.** Use it as the canonical "system" baseline and the poster child for return-only evaluation. Do not compare returns against its Table 1.

---

### 2.6 Policy-as-Skill (Mohsenzadegan, Tavakkoli, Kyamakya, Klagenfurt; arXiv 2609.27087, v1 22 Sep 2026)

**Problem.** Governed LLM decision support for policy, compliance and risk tasks. Not finance trading.

**Method.**
- **The policy skill:** a tuple S = ⟨identity, version, retrieval scope, evidence contract, decision schema, review triggers, audit fields, failure policy, prompt template, context contract⟩.
- **Ablated variants:** PaS Retrieval, PaS+Audit (validation only, no decision override), PaS+Controller, and PaS Full (audit + a deterministic controller that inspects retrieved normative statements).
- **Comparison:** 13 methods with a fixed **gemma4:e2b** backend on 600 development tasks: 150 each of policy QA, compliance, risk classification and conflict detection, labelled by a single expert. 7,800 runs.

**Headline numbers (Table II).**
| Method | Exact accuracy | Macro-F1 | Review F1 |
|---|---|---|---|
| PaS+Audit | 0.538 | 0.346 | 0.854 |
| PaS Full | **0.612** | 0.306 | 0.820 |
| LLM+RAG | 0.498 | 0.323 | 0.695 |

**Controller intervention analysis (§V-B), the part you asked about.**
- Relative to PaS+Audit, the controller changes **401/600** decisions (66.8%).
- Of those, **181** wrong → right, **137** right → wrong, and **83** wrong → differently wrong. **Net +44 tasks (+7.3 pp).**
- **Per task type (Table III):** conflict detection +59.3 pp; risk classification **−23.3 pp** (p = 1.27×10⁻⁴); policy QA −8.7 pp; compliance +2.0 pp.
- Excluding the conflict subset, PaS Full gets 48.2% vs LLM+RAG 50.4%, while PaS+Audit gets 58.2%.
- **Conclusion:** use deterministic control selectively, where the policy semantics are precise.
- **Provenance:** the authors say plainly that the evaluation is "system-development-informed", not a held-out test.

**What it does NOT do.** No markets, no outcomes, no multiple policies applied to the same case, no calibration.

**Overlap.** RQ1: Partial (methodological). RQ2: None. RQ3: None. System: **Partial→Strong** conceptually: a versioned, executable policy with an evidence contract, a deterministic controller and audit fields is our JSON policy + risk engine + JSONL log.

**Borrow.** The intervention-transition analysis itself; see §5.3 for the adapted template.

---

## 3. Search results, Jun–Oct 2026: mandate / profile adherence and identical-evidence designs

Searches covered: mandate adherence or risk-profile compliance for LLM trading and investment agents; risk-tolerance steerability on the same evidence; mandate constraint violations with a deterministic guardrail; investment-policy-statement agents; robo-advisor suitability; confidence calibration of trading agents; evidence-acquisition cost and stopping; frozen-evidence replay; TradingAgents 2026 updates. Top hits were verified on arXiv and read.

### 3.1 OpenPM: Auditable Point-in-Time Evaluation for LLM PM Agents (Cai, Guo, … Metaxas, Li; arXiv 2608.09988, v1 6 Aug 2026) **[read in full]**

**Problem.** LLM portfolio agents' results get inflated by leakage, optimistic execution, and **risk mandates that are described but not enforced**.

**Method.**
- **Task:** a $1M long-only S&P 500 book on 5-minute bars, with a row-level availability gate (a record is used only if ts_available ≤ T).
- **Mandates:** a natural-language mandate is compiled to typed RiskConstraints. Presets: conservative ≤5% per name / ≤30 names / 10% cash; balanced ≤10% / ≤20 names; aggressive ≤25% / ≤10 names. Free text is parsed by an LLM through forced tool use.
- **"Tiered allocator":** 6 analyst LLMs score typed channels, then a constructor LLM proposes weights, then a **deterministic critic projects them onto the feasible set**, then a fill simulator.
- **Per-run audit artifacts:** a constraint-adherence report, a contamination certificate, a cost-sensitivity curve, and a bias checklist.
- **Key design, "capture-once, replay-many":** analyst evidence is frozen once and **replayed byte-identically through 5 constructor models**.

**Data and models.**
- 508 PIT S&P 500 names; 2026-03-02 to 2026-05-01 (44 days, 3,432 bars); post-cutoff for all models.
- Analysts: DeepSeek-V3.2 and gpt-5, × 3 seeds = 6 captures.
- Constructors: gpt-5, claude-opus-4.7, DeepSeek-V3.2, qwen3-max, gpt-4o-mini, at K ∈ {30, 40, 50}. That gives 90 LLM cells plus 216 baseline cells.

**Headline numbers.**
- **Constructor vs same-pool equal weight (Table 2, ΔEW):**
  - On the gpt-5 capture, four of five constructors beat same-pool EW at K = 50 (gpt-5 +5.3 pp, DeepSeek +3.9, Opus +3.6, Qwen +1.1; gpt-4o-mini −2.1).
  - On the DeepSeek capture, **none** beat EW (best is −1.0).
  - "The analyst tier is the larger lever."
- **Mandate (§6.3): under the balanced mandate, raw proposals never break the caps.** The max single-name weight hits exactly 10% in 24/90 cells and never exceeds it. The critic's real work is **liquidity clipping, in 37/90 cells**, which they report separately from mandate breaches.
- **Daily sweep (Table 3):** Opus 13.7% and DeepSeek 9.7% net vs SPY 5.8%; turnover drives cost.

**What it does NOT do.**
- **Only one mandate (balanced) in every experiment**, so there is no cross-mandate comparison.
- No outcome-conditioned analysis of critic interventions. They found no mandate breaches to analyze.
- No calibration, no NSE, no evidence-cost or stopping analysis.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | **Partial→Strong** | Raw vs post-critic adherence and replay of identical evidence, but across models, not mandates. |
| RQ2 | None | |
| RQ3 | Partial | Analyst evidence quality matters more than the constructor. |
| System | **Strong** | Frozen-evidence replay, NL mandate → typed constraints → deterministic critic, audit artifacts: our system, but more rigorous. |

**Borrow.**
1. **The terminology and design citation:** "capture-once, replay-many".
2. **Same-pool equal-weight as the hard naive baseline.**
3. **Classify every clamp by reason** (mandate clause vs liquidity/feasibility vs other) so non-mandate clips aren't counted as obedience failures.
4. **Their finding that caps never bound is our warning.** If our mandates are loose, unguarded violation rates will be ≈0 and RQ1 is dead. Include tight clauses (confidence gate, stop distance, evidence restrictions) that LLMs plausibly break.

### 3.2 PortBench (Zhao, Chen, Su, HKUST-GZ; arXiv 2605.27887, v5 12 Sep 2026) **[main text + profile appendices read]**

**Problem.** Full-pipeline, multi-asset portfolio-management benchmarking.

**Method.**
- 183 instruments across 6 asset classes, 2015–2025.
- 6,269 static QA items.
- A five-stage pipeline: S1 market interpretation → S2 signals → S3 weights (LLM), then S4 execution → S5 risk (deterministic sandbox).
- CEPS error-propagation metric and paired stage interventions (replace one stage with ground truth, then rerun the downstream stages).
- **Three investor profiles** (conservative / balanced / aggressive) with exposure and drawdown caps **stated in the prompt but not enforced**.
- PAS (profile alignment score) is computed post hoc; AdaptScore = std of PAS across profiles.

**Models and setup.** 10 frontier LLMs (Kimi-K2.6, Qwen3.7-Max, GLM-5.1, DS-V4, Doubao, Hunyuan…); temperature 0; monthly decisions; 2024 normal window plus 3 stress windows; 12-day real-time window (2026-07-16 to 31).

**Headline numbers.**
- Only 32.5% of 120 model-profile-period evaluations beat equal weight on Sharpe; only 3/30 normal-period cells do.
- **Matched model-date pairs, conservative → aggressive (Table 13, F.2):**
  - Risk-asset exposure **+0.177 [0.126, 0.223], 103/110 positive**.
  - Bond+cash exposure −0.161 (103/110).
  - HHI up in 91/110.
  - Volatility up for 9/10 models; Sharpe +0.010 (5 up / 5 down).
- PAS is 0.90 for aggressive vs 0.72 for conservative.
- 7/10 models fail at least one conservative-profile stress drawdown gate.

**What it does NOT do.**
- No deterministic enforcement and no guarded/unguarded contrast.
- The sandbox carries state: holdings differ across profiles, so the evidence isn't byte-identical.
- No re-run noise floor (temperature 0, single run). No clause-level obedience, no calibration, no NSE.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | **Strong on the basic claim** | Mandates measurably shift decisions on matched inputs. |
| RQ2 | None | |
| RQ3 | Partial | Stage interventions: more correct upstream info barely helps downstream. |
| System | Partial | |

**Borrow.**
1. **Matched-pair reporting with sign counts and model-cluster bootstrap CIs** (e.g., "103/110 positive"). Copy this format.
2. **Paired stage interventions → an evidence-view swap.** Give policy A the evidence view selected under policy B. That separates the evidence-selection effect from the decision-rule effect (§5.2).

### 3.3 BiasMix-Finance: Post-Generation KYC Guardrails (Kukreja, Kukreja, Abraar, **Raj Dandekar**, Rajat Dandekar, Panat; arXiv 2608.28646, v1 14 Aug 2026; accepted ICLR 2026 FinAI Workshop) **[read in full]**

**Problem.** LLM ETF allocations silently break KYC caps. The paper proposes post-generation verify-and-repair.

**Method.**
- Strict JSON → validate against caps (volatility, fees, HHI, max asset, max sector) → if violated, **QCQP projection to the nearest feasible portfolio**.
- **Correction distance D = ‖w* − w0‖₂.**
- 16-ETF universe, as-of 2025-09-30, **3 investor profiles × 8 "bias recipes"** (anchor tech, FOMO energy, small-cap hype…) × 3 seeds = 72 scenarios (36/15/21 split).
- 3 models (Gemini 2.5 Flash, GPT-5 nano, Llama-3.3-70B) × 3 modes (direct, critique, self-consistency).
- Wilson CIs, bootstrap, Wilcoxon + BH-FDR.

**Headline numbers.**
- First-pass violation rate 47.6–85.7% (pooled 67.2%). **Conservative = 1.0 in every test case.**
- Aggressive with self-consistency: 0.476 → 0.048.
- After projection, 0% violations; median D = 0.066 (test, pooled).

**What it does NOT do.**
- **No returns or outcomes**, by design (they state no expected returns or transaction costs).
- No multi-agent pipeline or evidence, no time series, no calibration.
- n = 21 per configuration.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 (unguarded variant) | **Strong** | First-pass violation per profile + deterministic repair + correction distance is the guarded-vs-unguarded experiment for static allocations. |
| RQ2 | None | |
| RQ3 | None | |
| System | Strong (enforcement layer) | |

**Borrow.**
1. **Per-clause first-pass violation rate with Wilson CIs.**
2. **Correction distance**: for us, |size_U − size_G| / cap, the stop shift, and action change as a categorical correction.
3. **Bias recipes as our decoy/trap suite** (the anti-gaming fix the plan needs).
4. **Position against it in one sentence.** BiasMix shows repair is *needed* and *small*. We ask whether repair *helps the outcome*.

**Strategic note.** Raj Dandekar appears to be on your MSR-RF letter list, and this paper is accepted at your ICLR-27 target venue's previous edition. Not citing it would be a serious mistake. Building explicitly on it (adding outcomes and identical-evidence cross-mandate replay) is the natural pitch to him.

### 3.4 ReguSim (Luo, Jiang, Xie, Lan, Cong, Rao, Song, HKUST; arXiv 2608.19974, v1 20 Aug 2026) **[main text read]**

**Problem.** LLM traders cite rules yet submit orders that break executable constraints.

**Method.**
- Keeps four artifacts separate: **stated reasoning, attempted action, execution enforcement result, monitor evidence**.
- Synthetic price paths under US / China A-share / HK / LAX / STRICT rule regimes; 30 decision steps per session.
- Incentive (neutral / profit / stealth) × persona (aggressive / conservative) framing.

**Models.** DeepSeek V4 Pro (4,500 decisions), Gemini 3.5 Flash (1,800).

**Headline numbers.**
- Rejected attempts: 24.2% (DeepSeek) and 14.8% (Gemini), even with the rule text visible.
- **Persona gap (aggressive − conservative rejected-attempt rate): 30.9 pp** (DeepSeek) and 9.5 pp (Gemini).
- Removing the rule text: rejected 24.2% → 33.2%, rule breaches 10.0% → 21.7%.
- Prompt-only ledger instead of hard execution: rejected 24.5%, activity 31.6% → 38.0%.
- Traders write "this order complies" and then get blocked.

**What it does NOT do.** Exchange rules, not investor mandates. Synthetic markets. No outcome or utility analysis of enforcement, no calibration.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 (unguarded) | **Partial→Strong** | Attempted-vs-enforced action conditioned on persona. |
| RQ2 | None | |
| RQ3 | None | |
| System | Partial | |

**Borrow.**
1. **A rationale-action gap metric**: the share of unguarded violations where the rationale claims compliance.
2. **A "no-policy-text + enforcement" arm**, to show whether telling the LLM the mandate adds anything beyond enforcing it.

### 3.5 Auditing AI Investment Recommendations as Executable Actions (Barbieri, Vargas, Ferraz; arXiv 2606.27570, v1 25 Jun 2026) **[main text read]**

**Problem and method.** Score any advisor on three axes:
- **Validity** under portfolio and fee constraints, checked by a deterministic failure taxonomy.
- **Stability** across repeated runs.
- **Agreement** with a deterministic baseline that replays from frozen inputs.

**Headline numbers.**
- Over a 120-scenario bank, the control with the highest agreement (0.94) is admissible in only 0.58 of its runs.
- Two frontier models are admissible in about half of bare-prompt adversarial runs and fail on order arithmetic. Supplying the arithmetic deterministically lifts both to near-perfect validity.

**Overlap.**
| RQ / part | Rating | Why |
|---|---|---|
| RQ1 | Partial | Validity of the raw proposal plus stability across runs. |
| RQ2 | None | |
| RQ3 | None | |
| System | Partial | Frozen-input replay, deterministic verifier. |

**Borrow.** **Stability across repeated runs** as a reported axis. It is the same noise-floor idea as CLQT's.

### 3.6 InvestLogicBench (Jiang et al.; arXiv 2608.06108, v2 20 Aug 2026) **[main text read]**

**Problem and method.** Investment reasoning traces P → E → R → D → O (profile, events, reasoning, decision, outcome) from 151 real investors (201,247 decisions), with profile-conditioned thesis generation scored by an LLM judge. Also a live arena, Nov 19 2025 – Jan 9 2026.

**Headline numbers.** Logical plausibility is about 4/5, but event grounding is only 0.8–2.8/5.

**Overlap.** RQ1: Partial at the framing level only ("the same evidence justifies different actions for different investors"). Not mandate obedience, enforcement or calibration. Everything else: None.

**Borrow.** The framing sentence and a citation for "process over P&L".

### 3.7 Adjacent hits [abstract only] (cite or keep in reserve)

| Paper | arXiv / date | Relevance |
|---|---|---|
| Investor risk profiles of LLMs | 2603.09303, Mar 2026 (ICAIF'25 poster) | Personas shift questionnaire risk profiles; self-report, not decisions |
| One Size Fits None: Heuristic Collapse in LLM Investment Advice | 2604.23837, Apr 2026 | Allocations driven mostly by stated risk tolerance; other factors ignored. Relevant to policy collapse |
| Behavioral Consistency Validation (trading-style switching) | 2602.07023, Feb 2026 | Style switching only partly consistent with behavioral-finance theory |
| KTD-Fin: From Knowing to Doing | 2605.28359, May 2026 | Masking plus Barra attribution; returns mostly market/style beta |
| NextFund | 2607.11141, Jul 2026 | Live multi-market decision-path logging (HK/US/A-share) |
| Beyond Agent Architecture (execution assumptions) | 2606.08285, Jun 2026 (v2 Sep) | 30-study reproducibility audit |
| Agentic Trading survey | 2605.19337, May 2026 | 1/19 primary studies report an explicit cost model |
| Your AI, Not Your View | 2507.20957 (ICAIF'25) | Counterfactual reverse-evidence bias test: the P3 protocol source |
| SHARP: rubric policy | 2605.06822, May 2026 | "Policy" = self-evolving condition-action rubric, not an investor mandate |
| Scores Are Not Decisions (CAM-DF) | 2607.27083, Jul 2026 | General cost-aware tool-acquisition stopping (37% fewer tools); the only stopping-method hit, not finance |
| Type-Checked Compliance (Lean 4) | 2604.01483, Apr 2026 | Formal guardrail proposal, no experiments |
| GitHub `pradnyaw25/ai-portfolio-manager` | repo, created 8 Jun 2026 | LangGraph + deterministic risk guardrails + Brier/calibration curves. A near-clone of our design as code; not a paper, but a reviewer may know it |

**Not found.** No Jun–Oct 2026 paper I could find replays a byte-identical evidence pool across *multiple investor mandates* with an enforcement on/off contrast. Nor did I find one that computes ECE/Brier of trading-agent stated confidence against realized outcomes. That is a statement about my search, not proof none exists.

---

## 4. Overlap matrix (None / Partial / Strong)

| Paper | RQ1 obedience | RQ2 calibration | RQ3 evidence cost | System design |
|---|---|---|---|---|
| CLQT | Partial→Strong (Discipline; one mandate) | None–Partial | Partial | **Strong** |
| FinPersona-Bench | Partial | None | None | None–Partial |
| Persona collapse | None–Partial | None | None | None |
| Alpha Illusion | None | Partial (calls for it) | None | Partial (supportive) |
| TradingAgents | None | None | None | **Strong** |
| Policy-as-Skill | Partial (method) | None | None | Partial→Strong (concept) |
| OpenPM | Partial→Strong | None | Partial | **Strong** |
| PortBench | **Strong (basic steerability)** | None | Partial | Partial |
| BiasMix-Finance | **Strong (unguarded violations + repair)** | None | None | Strong (enforcement) |
| ReguSim | Partial→Strong | None | None | Partial |
| Auditing-as-Actions | Partial | None | None | Partial |
| InvestLogicBench | Partial (framing) | None | None | None |

---

## 5. Verdict

### 5.1 Pre-empted (blunt)

- **"A policy-conditioned multi-agent trading framework" as a contribution: dead.** TradingAgents (roles, risk team), CLQT (committee + mandate-aware synthesis + Risk-Officer gate + hash-chained audit), OpenPM (typed mandate → deterministic critic + audit artifacts), BiasMix (deterministic repair), Alpha Illusion (prescribes exactly this modular design), plus open repos.
- **"The deterministic layer guarantees compliance / auditable JSONL logs / frozen-evidence replay" as novelty: dead.** OpenPM's capture-once-replay-many is byte-identical replay. CLQT hash-chains every round. 2606.27570 replays from frozen inputs. TradingAgents v0.5.0 records decisions as they were made.
- **"Different mandates produce different decisions": pre-empted at the allocation level.** PortBench gives +0.177 risk exposure in 103/110 matched pairs; ReguSim gives a 30.9 pp persona gap. You can *replicate* it, but you can't *claim* it.
- **"Unguarded LLM proposals violate mandates and enforcement fixes them": pre-empted.** BiasMix gives 67.2% pooled first-pass violations → 0% after projection, with small D. CLQT's Discipline / clip dependence and OpenPM's raw-vs-critic adherence measure the same thing.
- **"More evidence doesn't buy better decisions" (RQ3's likely finding): partly pre-empted** by CLQT (no module clears the ±0.42 band) and OpenPM (analyst quality is the lever). Adaptive stopping in trading is open, but you have zero outcomes and three days. Cut RQ3 to a one-paragraph limitation, or to an evidence-budget × decision-flip-rate table that needs no outcomes.
- **"First mandate-adherence benchmark" and "identical evidence across models": do not write either.** OpenPM owns the second.

### 5.2 Survives

1. **Outcome-conditioned enforcement analysis (the main contribution).**
   - The question: when the deterministic layer overrides the LLM, does it improve or worsen realized decision outcomes, broken down by clause (size cap, stop, confidence gate, veto, forbidden evidence) and by mandate?
   - No one measures this. BiasMix has no returns. OpenPM's caps never bind. CLQT says outright that its constraint layer was not ablated alone.
2. **A cross-mandate design on a byte-identical evidence pool, with a same-mandate re-run noise floor.**
   - Steerability = cross-mandate divergence minus same-mandate re-run divergence. Report N_eff / JS for policy collapse.
   - Nobody reports cross-mandate divergence net of re-run noise.
   - **Design tension you must fix.** Your policy chooses which tools are consulted, so the LLM sees different evidence under different policies. "Identical evidence" therefore means identical *pool*, not identical *view*.
   - Run a 2×2: {policy-specific view, common view} × {policy A, policy B}. That splits the mandate effect into an evidence-selection part and a decision-rule part. A reviewer will catch this if you don't.
3. **Stated-confidence calibration (ECE/Brier/selective risk) per mandate.** Alpha Illusion P4 demands it and no read paper measures it for trading agents. Secondary because it needs outcomes. But for *historical* bundles the forward returns already exist, so it is computable offline now (see §5.4).
4. **US + NSE.** A robustness axis only. No threat paper uses NSE.

### 5.3 Is Policy-as-Skill's controller-intervention analysis a template for guarded vs unguarded?

**Yes, and it is the best template available, with one essential change.** PaS scores "correct" against reference labels. In our system, compliance-based correctness is tautological: the guarded decision is compliant by construction. So the transition matrix has to be defined on **pre-registered outcomes**, not compliance.

**Concrete protocol.**
1. **One LLM call, two decision paths.** For each decision instance *i* = (bundle, mandate, model, seed), take the unguarded proposal U_i (action, size, stop, confidence). Apply the deterministic layer *post hoc to the same proposal* to get G_i. Never compare two separate LLM runs: sampling noise would confound the effect. This mirrors PaS+Audit vs PaS Full on identical model outputs.
2. **Intervention typing.** I_i = 1[G_i ≠ U_i], with a type: {confidence-gate → WAIT, veto → WAIT, size clamp, stop override, forbidden-evidence block, non-mandate feasibility clip}. Report non-mandate clips separately, as OpenPM does.
3. **Obedience metrics.** These come from the unguarded proposals and need no outcomes:
   - Per-clause would-violate rate with Wilson CIs (BiasMix).
   - r_self (share of U already compliant) and clip dependence (CLQT D4).
   - Correction distance (BiasMix D).
   - Rationale-claims-compliance-while-violating rate (ReguSim).
4. **Outcome utility, pre-registered.**
   - Define u(·) per mandate *before* seeing results: for example, realized P&L over a fixed horizon h with the stop applied, expressed in the mandate's risk-budget units (R-multiples).
   - WAIT gives u = 0. Also report a forgone-opportunity variant.
   - Each intervention is then **helpful** (u(G) > u(U) + ε), **harmful** (u(G) < u(U) − ε) or **neutral**. This is the PaS 181 / 137 / 83 split.
5. **Report**, as PaS does:
   - The intervention rate.
   - Helpful / harmful / neutral counts.
   - Net Δu with a paired bootstrap CI.
   - An exact sign test (McNemar-style) on helpful vs harmful.
   - **Stratified by mandate and by clause**, the analogue of PaS's per-task Table III.
6. **Noise floor.** Re-run the unguarded agent (≥2 seeds). An intervention effect only counts if it exceeds the variation between re-runs.
7. **Extra arms**, each a one-line addition:
   - (a) A policy-blind LLM plus enforcement: does telling the LLM the mandate matter, given enforcement? (ReguSim's no-rule-text arm.)
   - (b) A placebo policy (FinPersona).
   - (c) JSON-numeric vs natural-language persona policy (FinPersona O3).
8. **Prior hypothesis worth stating.** Selective enforcement wins. The layer likely *helps* the conservative mandate (vetoes losers) and *hurts* aggressive / intraday (clips winners). That is analogous to PaS's +59.3 / −23.3 split and to FinPersona's persona-dependent re-grounding.

**Caveats PaS itself teaches.**
- Freeze the policy thresholds before looking at outcomes. Your `PREREGISTRATION.md` (frozen 7 Aug) helps. If any threshold was tuned on these bundles, say so: PaS calls such an evaluation development-informed.
- Statistical power. With 9 bundles, 3 tickers and 1 model, the helpful/harmful counts will be single digits and meaningless. You need hundreds of decision instances, e.g. ≥20 tickers × ≥15 dates × 4 mandates × ≥2 models × 2 seeds.

### 5.4 The single most defensible contribution statement (4–6 pp workshop)

> *Deterministic risk layers now sit on the critical path of LLM trading agents (OpenPM, CLQT, BiasMix-Finance), but whether their overrides improve decisions has never been measured: prior work reports only that raw proposals violate mandates and that repair restores feasibility. On byte-identical frozen evidence pools from US and Indian (NSE) equities, we replay four machine-readable investor mandates through LLM agents in unguarded mode, and apply the deterministic layer post hoc to the same proposals. We report (i) per-clause violation rates and cross-mandate divergence net of same-mandate re-run noise, and (ii) a controller-intervention analysis showing, clause by clause and mandate by mandate, how often enforcement turns a losing proposal into a better outcome versus breaking a good one.*

Calibration (ECE/Brier of stated confidence) is a **secondary exhibit** only if outcomes are in. Drop RQ3 to future work.

**Feasibility note for the 7 Oct ICAIF deadline.** "Zero outcomes logged" is less blocking than the plan assumes. For historical bundles, forward returns can be computed from price data today. The catch is contamination: if a bundle date is before the model's training cutoff, the unguarded decisions may already "know" the outcome (Alpha Illusion P1; Profit Mirage). Use bundle dates after the model's cutoff, and state the cutoff per model in a table, as CLQT's Appendix C does. For gpt-4o-mini, sources disagree: OpenPM lists about 2024-10, while OpenAI's docs have listed Oct 2023 (I did not check this session). Take the later date to be safe, which means 2025–2026 bundles are clean.

### 5.5 Specific corrections to `ICAIF_2026_AI4F_Month_Plan.md`

- CLQT v1 is **29 Jun 2026**, not Aug. It is now v3 (12 Sep) with a blinded human anchoring of the judge.
- Add **OpenPM, PortBench v5, BiasMix-Finance and ReguSim** to the competitor table. They are stronger threats to RQ1 than FinPersona.
- Retire "load-bearing claim = cross-sectional identical-evidence design" as written. Replace it with §5.4.
- The local TradingAgents PDF is the old version. Cite arXiv v7 and Alpha Illusion's reproduction numbers.
