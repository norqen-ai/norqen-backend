# B. Calibration, India/NSE, and override-outcome scout (5 Oct 2026)

**Scope:** three lanes for `policy-trading-agents`: (1) calibration and abstention for LLM trading/forecasting, (2) LLMs and agents on Indian markets, (3) whether deterministic guardrails and human-in-the-loop overrides help or hurt outcomes.
**Excluded:** the 14 papers already covered in `A_threat_deep_read.md`.

**How each paper was read:**
- **[full]** means I pulled the arXiv HTML or PDF text and read the methods, results and limitations.
- **[main text]** means I read the body but skimmed or skipped the appendices.
- **[abstract only]** is marked wherever it applies.
- Every ID and date below was checked on the paper's arXiv/Crossref/NBER page. Numbers are copied from the cited table or section.

---

## 0. Bottom line

1. **Correction to A §3.7 / §0.5(b).** One paper has now measured ECE of an LLM trading agent's per-order stated confidence against realized next-period returns: **KTD-Fin (2605.28359)**. It covers 10 frontier LLMs on CSI300, with ECE between 0.246 and 0.425 (Table 4). It reports one ECE number per model and nothing more: no reliability diagram, no resolution term, no link to sizing or vetoes, and Brier is computed but not reported. **RQ2 can no longer claim "first to measure trading-agent calibration."** It has to narrow to: role-level, policy-conditioned and veto-linked calibration, with a resolution decomposition.
2. **The strongest methodological threat to RQ2 is Ordinal Gates, Cardinal Bets (2609.00187).**
   - Verbalized confidence from 9 open LLMs on Nasdaq-100 news has almost no resolution: RES/UNC is 0.07–0.4%.
   - Fixed confidence thresholds give no reliable gain: 0 of 18 configurations survive multiple-testing correction.
   - Raw confidence adds little over sign-only sizing.
   - This bears directly on the confidence-threshold knob in the policy JSON. Expect a reviewer to cite it.
3. **India: I found no arXiv or peer-reviewed paper that evaluates an LLM trading agent on NSE with leakage controls.** What exists:
   - IndiaFinBench: SEBI/RBI regulatory QA, no market data.
   - A NIFTY-50 headline-sentiment paper with test-set leakage, whose accuracy is below the majority-class baseline.
   - AlphaNiftyAI (Digital Finance, 2026): its metadata is verified, but the body is paywalled, so its numbers are UNVERIFIED.
   - So NSE coverage is open, but thin as a contribution on its own.
4. **Override-outcome analysis is still open for LLM trading.**
   - The closest LLM-adjacent evidence is TradeArena (2605.28850). Its risk-gate on/off ablation runs on a **deterministic reference agent, not an LLM**: no-risk return 0.468 vs 0.423 with the gate (Table 3).
   - Raven-Agent (2607.03015) compares a deterministic trading layer against forecast-only on 42 Polymarket trades. Its fixed-stake confidence intervals overlap.
   - The rigorous causal designs come from the human-overrides-algorithm literature: Angelova–Dobbie–Yang (RESTUD 2026) and the smart-vending field experiment (2607.00420). Borrow their estimands.

---

## 1. Paper cards

Relevance key: **(a)** override-outcome analysis · **(b)** agent calibration · **(c)** NSE coverage.

### Lane 1: calibration, uncertainty and abstention

#### 1.1 KTD-Fin: From Knowing to Doing — A Memory-Controlled Benchmark for LLM Trading Agents on Stock Markets [full main text + App. G]
- **Citation:** Taojie Zhu, Wentao Zhao, Rui Sun, Beidi Luan, Jiacheng Lu, Sinuo Wang, Jing Li, Daxin Jiang, Yonghong He, Zuo Bai (Tsinghua / Stepfun). arXiv **2605.28359v1**, cs.AI, 27 May 2026. No venue stated.
- **Method:**
  - Qlib-based daily portfolio construction over CSI300, using price-only observations (OHLCV and technical features; no news or fundamentals).
  - Four data-side masking levels: bright, stock-blind, date-blind, blinded.
  - Three decision modes; the headline mode is open-research, with 6 tools.
  - The agent emits JSON orders. Each order has `confidence ∈ [0,1]`, side, a reason, and a target weight or share count.
  - Returns are decomposed Barra-style into Common, Style and Selection α.
- **Data / market:**
  - CSI300 A-shares; long window 2024-01-01 to 2026-04-10 (548 trading days), plus 10 regime-stratified ~43-day windows.
  - Realistic A-share frictions: T+1, price limits, 5/15 bps.
- **Models:** 10 frontier LLMs: qwen3.6-plus, gpt-5.5, doubao-seed-2.0, claude-opus-4-7, minimax-m2.7, step-3.5-flash, gemini-3.1-pro, deepseek-v4-pro, glm-5.1, kimi-k2.6. Baselines are 18 Qlib factor models and CSI300 buy-and-hold.
- **Metrics:**
  - The 10-metric panel covers return, Sharpe, MDD, IR, turnover, HHI, cash ratio, abstention rate, parse-failure rate and **ECE**.
  - Brier on per-order confidence is "recorded for diagnostic use" only.
  - App. G defines ECE with 10 equal-width bins (bin confidence vs bin accuracy). Brier treats confidence as P(the order's realized next-period return > 0).
- **Key numbers:**
  - **Table 4 (blinded × open-research):** ECE ranges from **0.246** (claude-opus-4-7) to **0.425** (doubao-seed-2.0). Others: gpt-5.5 0.272, minimax 0.303, kimi 0.306, glm 0.322, deepseek 0.352, step 0.357, qwen 0.367, gemini 0.387.
  - **Total return:** +85.29% (qwen) down to −24.23% (kimi), against CSI300 at +36.92%.
  - **Table 5 (Barra attribution):** only Claude Opus 4.7 has selection α ≥ 0 (+0.2%). The others range from −0.7% to −77.8%.
  - **Masking:** the strongest attacker's top-5 ticker recovery is 10.2%, and joint recovery is ≤1.5% (§4.3).
- **Limitations:**
  - ECE is a single scalar per model: no reliability curve, no confidence intervals, no resolution/reliability split.
  - "Bin accuracy" for SELL orders is not defined. The Brier target ("return > 0") is wrong for sells.
  - Brier values are not reported.
  - Confidence is not linked to position size, abstention or executor rejections.
  - The full grid runs on only one anchor model.
  - Price-only inputs, China only.
- **Relevance:**
  - (a) **None-Partial.** The executor rejects invalid orders and logs them, but rejections are not analysed against outcomes.
  - (b) **Strong (direct prior art).** It is the first measurement I found of a trading agent's stated per-order confidence against realized returns.
  - (c) None.
- **What to do:**
  - Cite it as the prior measurement.
  - Differentiate on: per-agent-role confidence; the same evidence under 4 policies; confidence of vetoed vs. passed proposals; a Murphy decomposition with bootstrap CIs; and a correct label for SELL/HOLD.

#### 1.2 Ordinal Gates, Cardinal Bets: Matching LLM Confidence to the Financial Decision Operator [full]
- **Citation:** Rayansh Singh, Sara Rezaeimanesh (Michigan State Univ.). arXiv **2609.00187v2**, cs.CE, 2 Sep 2026. Venue field blank.
- **Method:**
  - LLMs classify ticker-day headline bundles as UP/DOWN with confidence. The verbalized channel asks for an integer from 0 to 100.
  - **Ordinal operators** (coverage-matched gates, top-k, abstention) use only the ranking of confidence. **Cardinal operators** (sizing) use its magnitude.
  - Theory: monotone recalibration cannot change a coverage-matched gate. Gate accuracy gain is bounded by √(RES·(1−φ)/φ) (Eq. 2).
  - Four-system design that crosses a {raw, isotonic-correctness} confidence map with a {raw, correctness} vol-target scale (κ).
- **Data:**
  - FactSet newswire headlines for Nasdaq-100 constituents. Fit on 2021 (15,034 ticker-days); test on 2022–23 (31,888 ticker-days).
  - Walk-forward extension over 2024–25 (12,911 ticker-days).
  - Named vs. anonymized inputs; 5-session holds; 5 bps costs.
- **Models:**
  - Ordinal grid: Qwen2.5-7B and Gemma-2-9B across 5 confidence channels (verbalized, two-token logit, logit-full, logit-entropy, P(True)).
  - Cardinal grid: 9 open models from 7B to 32B (Qwen2.5-7/14/32B, Gemma-2-9B, Gemma-3-27B, Mistral-7/24B, Phi-4, FinLLaMa-8B).
- **Metrics:** ECE, Brier/Murphy resolution, accuracy-coverage, certainty-equivalent return (CER, γ=3), Sharpe, MDD, ES; Holm and Romano–Wolf corrections; block bootstrap.
- **Key numbers:**
  - **§5, ECE:** two-token softmax confidence saturates at ≈0.97–0.98 (ECE ≈0.47). Temperature scaling brings ECE to 0.03–0.04, but the coverage-matched gate is exactly unchanged.
  - **§5, resolution:** RES/UNC is **0.07–0.4%** across 18 configurations. Base accuracy is 50.3–51.8% vs. a 53.8% base rate.
  - **§5, threshold gating:** fixed-threshold gates give **0/18** significant improvements (accuracy- or CER-tuned). Self-consistency (K=5) is unanimous on 96–98% of ticker-days.
  - **Table 1:** matched map+scale vs. raw gives **+9.2 pp/yr CER** [4.1, 14.6], p<0.001, positive in 9/9 models but Holm-significant in only 3/9. Excluding Qwen2.5-7B it is +5.5 [1.0, 10.1].
  - **Table 2:** sign-only sizing −0.8, raw confidence +2.7, matched +12.0 pp/yr CER. Matched MDD is −11.7% → −4.9%.
  - **Table 3:** under an adaptive-vol controller, the gain shrinks to **+1.6 pp/yr** [−0.8, 4.1], p=0.195.
  - **Table 4 (walk-forward):** isotonic +1.17 [−0.60, 3.06], Holm p=0.144.
  - **§6.4:** correctness–payoff alignment falls to 0.26 in 2025.
- **Limitations (authors' own):**
  - The base classifier is weak.
  - Contamination is possible for 2022–23.
  - The effect is concentrated in 2022 and in non-tech names.
  - Single-headline classifier, not an agent.
- **Relevance:**
  - (a) Partial. Its controller/scale-coupling result applies to any confidence → size → cap pipeline, including the vol-target sizing in this project.
  - (b) **Strong** (methodological, non-agent).
  - (c) None.
- **What to do:**
  - Report the Murphy decomposition, not only ECE.
  - Test whether the policy's confidence threshold works as a coverage gate; their prediction is that it gives little lift.
  - Treat the confidence → size mapping plus the risk engine as one coupled system.

#### 1.3 Beyond Forecasting: The Belief-to-Trade Layer in Prediction-Market Agents (Raven-Agent) [full]
- **Citation:** Yishu Wang (HKUST), Yuxuan Wang (PKU), Jiaqi Deng (HKU), Hanyang Tang (MIT). arXiv **2607.03015v1**, cs.AI, 3 Jul 2026. Code: github.com/Alchemist-X/predict-raven.
- **Method:**
  - An LLM forecaster outputs a probability *p* per contract.
  - A deterministic trading layer then:
    - ranks by time-normalised return ρ;
    - sizes at ¼-Kelly;
    - enforces 5 hard constraints outside the prompt: per-trade cap, exposure cap, per-event cap, stop-loss, drawdown halt.
  - **Replay** keeps archived forecasts fixed and varies only the trading policy.
- **Data:**
  - Polymarket archive: 59 open decisions, of which 44 were executable. Table 1 has 58 forecast-only trades.
  - Positions are held to resolution; unresolved ones are marked to market.
- **Models:** the forecaster runtime is not the object of study; probabilities are archived.
- **Metrics:** Brier on resolved rows, ROI, stake-weighted Sharpe.
- **Key numbers (Table 1, ROI / S_w / n):**

  | Policy | ROI | S_w | n |
  |---|---|---|---|
  | Forecast-only | −10.7% | −0.20 | 58 |
  | Edge-proportional | −55.5% | −0.91 | 58 |
  | Edge-filter | −9.3% | −0.16 | 48 |
  | **Raven fixed-stake (risk layer only)** | **−4.7%** | −0.09 | 42 |
  | Raven full (+¼-Kelly) | **+15.9%** | +0.42 | 42 |

  - Full-archive Brier is 0.329 for every policy. The selected-subset Brier falls to 0.258 only because of filtering.
  - **Table 3 bootstrap ROI CIs:** forecast-only [−24.7, +3.2]; Raven fixed [−20.6, +11.5]; Raven full [+3.8, +30.0].
  - **App. E (fused 132 rows, fixed stake):** +5.9% [−4.5, +16.1].
- **Limitations:**
  - Tiny n.
  - For the fixed-stake comparison that isolates the risk layer, the CIs overlap.
  - "Full" deploys $820 of stake vs. $420, so the comparison is not capital-matched.
  - Not equities; probability forecasts, not stated confidence of trade proposals.
- **Relevance:**
  - (a) **Partial-Strong in design.** Holding the LLM output fixed and replaying it under different deterministic layers is the same identification idea as frozen evidence bundles. Its effect for the risk layer alone is not significant.
  - (b) Partial (Brier of forecasts).
  - (c) None.
- **What to do:** cite it as the closest "freeze the LLM, vary the deterministic layer" prior. Our version should be capital-matched and include a re-run noise floor.

#### 1.4 TrustTrade: Human-Inspired Selective Consensus Reduces Decision Uncertainty in LLM Trading Agents [main text]
- **Citation:** Minghan Li, Rachel Gonsalves, Weiyue Li, Sunghoon Yoon, Mengyu Wang (Harvard AI & Robotics Lab / HBS / DGIST). arXiv **2603.22567v1**, cs.CE, 23 Mar 2026.
- **Method:**
  - Several heterogeneous LLM agents per information domain (fundamentals, market, news, sentiment).
  - Credibility-weighted selective consensus that discounts divergent or weakly grounded signals.
  - Deterministic temporal signals as anchors.
  - A reflective memory that adapts risk preference.
  - A/B tests against single LLM agents and human annotators.
- **Data:**
  - AAPL, GOOG, NVDA in 2024-Q1.
  - A real-time backtest from 1 Jan to 18 Feb 2026, deciding at 1 pm daily with contemporaneous data.
- **Models:** GPT-5, GPT-5-mini, GPT-4o, GPT-4o-mini, Grok-4, Gemini-2.5-lite, Claude-Haiku-4.5. TrustTrade itself runs on Grok-4 + GPT-4o-mini.
- **Metrics:** cumulative return (CR), MDD, Sharpe, API cost.
- **Key numbers (prose / figures only):**
  - At the analyst stage, market-only inputs give the best result: 33.1% CR, 9.1% MDD.
  - Full-allocation large LLMs reach ≈30% CR at ≈12% MDD.
  - Partial allocation moves GPT-4o-mini/Grok-4 from 29.6% → 12.5% CR and 12.1% → 5.0% MDD.
  - TrustTrade "shifts the partial-allocation frontier" (Fig. 4). The main comparison has no table of numbers.
- **Limitations:**
  - 3 megacap stocks.
  - Short windows.
  - Results are mostly in figures.
  - **No calibration measurement.** "Learning calibrated confidence" is listed as future work.
- **Relevance:**
  - (a) Partial: the consensus filter suppresses signals, but there is no outcome analysis of the suppressions.
  - (b) Partial: gap statement only.
  - (c) None.

### Lane 2: India and NSE

#### 2.1 IndiaFinBench: An Evaluation Benchmark for LLM Performance on Indian Financial Regulatory Text [full PDF]
- **Citation:** Rajveer Singh Pall (Gyan Ganga Institute of Technology and Sciences, Jabalpur). Sole author. arXiv **2604.19298v2**, submitted 21 Apr 2026, revised 2 May 2026. Data at github.com/rajveerpall/IndiaFinBench.
- **Method:**
  - 406 QA items written by one primary annotator from 192 SEBI and RBI documents (1992–2026).
  - Tasks: REG 174, NUM 92, CON 62, TMP 78.
  - Zero-shot, with the relevant passage injected into the context.
- **Validation:**
  - Model-based second pass: κ=0.918 on CON, 90.7% agreement over a 150-item subset.
  - Human IAA on 180 items: κ=0.645 on CON, 77.2% overall.
  - v1 reported a 60-item IAA with κ=0.611, per the search snippet. v2 expanded it.
- **Models:** 12 models: Gemini 2.5 Flash/Pro, Qwen3-32B, LLaMA-3.3-70B, Llama 4 Scout 17B, Kimi K2, LLaMA-3-8B, GPT-OSS 120B/20B, Mistral-7B, DeepSeek R1 70B, Gemma 4 E4B.
- **Key numbers (Table 6):**
  - Overall accuracy runs from 89.7% (Gemini 2.5 Flash, CI [86.3, 92.3]) to 70.4% (Gemma 4 E4B). Mean is 79.4%. Non-specialist human baseline: 69.0% (n=100).
  - NUM has the widest spread: 84.8 (Gemini 2.5 Flash) vs 48.9 (Gemini 2.5 Pro).
- **Limitations (§8):**
  - The string-match scorer has large false negatives: an LLM judge flipped **78.4%** of 874 flagged "incorrect" predictions.
  - Single primary annotator.
  - English only.
  - Context is injected, so this tests reading comprehension, not retrieval.
  - **No market data, no prices, no trading, no confidence.**
- **Relevance:** (a) None · (b) None · (c) **Partial.** It is Indian financial NLP but not NSE market data. Use it only as a citation that Indian finance is under-benchmarked.

#### 2.2 Adaptive Financial Sentiment Analysis for NIFTY 50 via Instruction-Tuned LLMs, RAG and RL [full]
- **Citation:** Chaithra (NIT Karnataka), Kamesh Kadimisetty (GVP College of Engg.), Biju R. Mohan (NITK). arXiv **2512.20082v2**, cs.AI, 24 Dec 2025. Header: CODS 2025 Research Track, Pune.
- **Method:**
  - Llama-3.2-3B, fine-tuned with QLoRA on SentiFin (10,572 Indian headlines).
  - RAG over about 8,000 scraped NIFTY-50 headlines from 2024–25 (Business Standard, NDTV Profit, FE, ET, Mint, Moneycontrol, …).
  - Source weights are updated by market feedback and by a PPO policy.
- **Labels:** the test set (6,134 headlines) is labelled by the next-day open-to-open return relative to a 30-day rolling mean ± 1 SD.
- **Key numbers (Table 4, accuracy / weighted-F1):**

  | Model | Accuracy | Weighted F1 |
  |---|---|---|
  | Fine-tuned Llama | 0.5520 | 0.5375 |
  | RAG | 0.6094 | 0.5722 |
  | RAG + feedback (WOC) | 0.6153 | 0.5746 |
  | RAG + PPO | 0.6109 | 0.5733 |
  | + price context | ≈0.66 | ≈0.567 |
  | FinBERT | 0.4852 | 0.5027 |
  | RoBERTa | 0.5800 | 0.5551 |

- **Limitations (my audit):**
  - **The majority-class baseline beats every model.** Neutral is 4,123/6,134 = **67.2%** of the test set (Table 3).
  - **Test-set leakage:** the feedback loop "iterates over the entire evaluation dataset" (§4.3.1), and Algorithm 1 takes **D_test** as the PPO input.
  - No trading, no returns, no confidence.
- **Relevance:** (a) None · (b) None · (c) **Partial.** It is the only arXiv NIFTY-50 LLM paper I could open. Do not use its numbers as a baseline.

#### 2.3 AlphaNiftyAI: conquering the Indian stock market with AI [metadata only; body UNVERIFIED]
- **Citation:** Mayur Chhalotre, Chaithra, Biju R. Mohan. *Digital Finance* 8(1), published 12 Jan 2026. DOI 10.1007/s42521-025-00174-z, verified via Crossref. Same NITK group as 2.2.
- **What I could not verify:** Springer redirected to an auth wall, so I could not read the paper. The search-engine snippet says:
  - multi-agent per-domain summarization with Llama3-70B;
  - weekly and monthly decisions on all NIFTY-50 stocks;
  - "69.23% over 15 months and 127.80% over 2 years."
  - **Treat all of these as UNVERIFIED.**
- **Look-ahead risk:** the knowledge cutoff vs. test window, leakage controls and costs cannot be checked without the full text.
- **Relevance:** (a) unknown · (b) unknown · (c) **Partial–Strong if confirmed.** It is the closest prior LLM multi-agent system on NIFTY-50. Get the PDF through PICT library access before claiming NSE novelty.

### Lane 3: deterministic guardrails and human overrides

#### 3.1 Representation Signatures and Risk-Feedback Alignment in LLM Trading Agents (TradeArena) [main text: §4–7.5, 7.14–7.17, §8]
- **Citation:** Weicheng Xue (Virginia Tech). Sole author. arXiv **2605.28850v3**, cs.LG, 15 Aug 2026.
- **Method:**
  - Auditable testbed: data → agent lifecycle → risk layer (clip / block / annotate) → execution simulator (fills, rejects, slippage) → trajectory log.
  - Ablations of the risk gate and execution realism.
  - Risk-feedback experiments with **true / placebo / hidden** feedback and a **contrarian** false-audit probe.
  - "Calibration gap" here means |intended − risk-approved weights|. That is an override-magnitude metric, not probability calibration.
- **Data:**
  - Synthetic: 3 assets, 120 periods, seeds 3/7/11; a 30-seed sweep; 120 heterogeneous synthetic markets.
  - Historical: weekly decisions on GSPC, BTC-USD and ETH-USD (Yahoo, 2021–26). LLM runs use the last 52 weekly decisions.
- **Models:** in synthetic ablations the agent is **a deterministic "reference agent" (momentum + macro/news signals)**, not an LLM. LLM rows (Poe-mediated): GPT-5.5, Gemini 3.1 Pro, Kimi K2.5, GLM-5, Claude Opus 4.7, plus direct-provider sanity runs and DeepSeek V4 Pro.
- **Key numbers:**
  - **Table 3 (reference agent):**
    - risk-aware: return 0.423, Sharpe 7.696, MDD −0.025, fill 0.876;
    - **no-risk ablation: return 0.468**, Sharpe 7.949, MDD −0.029, fill 0.673, 62.3 vs 22.0 rejected orders (§7.5).
  - **Table 7 (position caps):** strict 20% cap gives return 0.243; default 35% gives 0.423; loose 50% gives 0.459.
  - **Table 17:** after a clip/block, next-step intended exposure falls by 0.166 (Kimi) to 0.480 (Gemini).
  - **Table 19 (true vs. hidden feedback):**

    | Model | Return, true | Return, hidden | MDD, true | MDD, hidden |
    |---|---|---|---|---|
    | GPT-5.5 | −0.232 | −0.312 | −0.317 | −0.381 |
    | Kimi K2.5 | −0.125 | −0.306 | −0.228 | −0.382 |
    | Claude | −0.169 | −0.266 | −0.255 | −0.348 |

    Gemini: placebo gives the best return (−0.209 vs. −0.308 true). GLM-5: hidden is slightly better.
  - **Table 21 (contrarian false audit):** GPT-5.5 return −0.085 and Claude −0.089 vs. the truthful baseline. All three models cut exposure.
  - **Every LLM row has a negative return.**
- **Limitations (author's §8 plus mine):**
  - The risk-gate on/off result is **not on an LLM agent**.
  - 3 seeds; synthetic markets.
  - LLM horizon of 52 weeks on 3 assets.
  - Poe wrapper confound.
  - It studies **feedback about** vetoes, not the counterfactual P&L of each veto.
- **Relevance:**
  - (a) **Partial–Strong.** It is the nearest risk-gate on/off ablation. It shows "the risk layer changes the operating regime" (lower return, fewer rejects) but never runs per-intervention counterfactuals on LLM proposals.
  - (b) None. Its "calibration" means intent-vs-approved gap.
  - (c) None.
- **What to do:**
  - Borrow the intended-vs-approved gap as an override-magnitude covariate.
  - Borrow the true/placebo/hidden design if veto feedback is ever shown to agents.

#### 3.2 A Simple Solution to Improving Human Supervision of Algorithms: Evidence from Smart Vending [main text: §3.3, §4 setup, §5, §7]
- **Citation:** Minda Zhao, Brian Rongqing Han, Xin Chen, Tao Zhu (Georgia Tech ISyE; UIUC Gies). arXiv **2607.00420v1**, cs.HC, 1 Jul 2026.
- **Method:**
  - Randomized field experiment at worker level, 46 days from 4 May 2023: no-override (221), constrained override with ≤2 downward overrides per machine (223), free override (109).
  - Analysis: DID, plus **LATE via 2SLS** with the randomized policy as instrument, to estimate the effect of the override decision on compliers.
- **Data:** Fengyi Technology: 553 workers, >59,000 machines, 4,000 SKUs. The algorithm sets replenishment.
- **Key numbers (abstract / §7):**
  - Free overrides: inventory −1.95%, **sales −1.19%**.
  - Constrained overrides: inventory −1.28% **with no sales loss**.
  - A personalized policy simulation gives +9.1% sales probability.
  - Scaled to more than 170,000 machines, for about $1M/yr in savings.
- **Limitations:**
  - The direction is reversed from ours: humans override an algorithm, not rules overriding an LLM.
  - Low-stakes retail; the authors say strict constraints are impractical in high-stakes domains.
- **Relevance:**
  - (a) **Strong (methodological).** It supplies the estimand vocabulary: effect of override on the overridden decisions, compliers, and a cap on the override budget.
  - (b) None · (c) None.
- **Our advantage:** frozen-evidence replay gives the **full counterfactual for every proposal** (veto on/off). That is stronger identification than their IV. The "override budget" is a testable policy knob.

#### 3.3 Algorithmic Recommendations and Human Discretion [abstract only]
- **Citation:** Victoria Angelova, Will S. Dobbie, Crystal S. Yang. NBER WP **w31747** (Sep 2023). *Review of Economic Studies* 93(4):2250–2283 (2026), venue confirmed on the NBER page.
- **Finding:** in bail decisions, **90% of judges underperform the algorithm when they override it**. The top 10% beat it on both accuracy and fairness, by using private information and overreacting less to salient events.
- **Relevance:**
  - (a) **Partial (methodological).** Override value is heterogeneous by overrider. Our analogue is heterogeneity by clause, by policy and by agent.
  - (b) None · (c) None.
- **Note:** the NBER paper dates from 2023; the journal version is 2026.

#### 3.4 Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human [main text]
- **Citation:** Emre Turan (independent researcher). arXiv **2606.08919v1**, cs.AI, 8 Jun 2026. Code: github.com/turangenesis/headroom.
- **Method:** the LLM action guard is framed as **selective classification under asymmetric cost** (risk-coverage, AURC, Neyman–Pearson point), on 125 hand-labelled, adversarially weighted coding-agent actions. A fatiguing-reviewer model is simulated.
- **Key numbers:**
  - Fleiss κ = **0.52** among reviewers on what counts as "risky".
  - AURC 0.374 ± 0.002 across seeds (Haiku vs. Sonnet comparison).
  - The inverted-U in safety vs. escalation rate is a **modelling result, not a human study**. The author says none of the mechanisms are novel.
- **Limitations:** small n, not finance, no real outcomes.
- **Relevance:** (a) Partial (framing) · (b) Partial · (c) None.
- **Borrow:** report the veto engine's operating point as a **risk-coverage curve against realized loss**, not a single veto rate.

### Adjacent hits (not deep-read; listed so they are not re-searched)

| Paper | ID / venue | Status | Why only adjacent |
|---|---|---|---|
| What Does ChatGPT Make of Historical Stock Returns? Extrapolation and Miscalibration in LLM Stock Return Forecasts (Chen, Green, Gulen, Zhou) | arXiv 2409.11540 (Sep 2024; AEA 2026 program) | [abstract only], pre-window | LLM 80% CIs for returns are "better calibrated than survey evidence" but return forecasts over-extrapolate. A forecast, not an agent. A good background citation for RQ2. |
| TRIAD: Guardrail-Feedback-Driven Framework for LLM Agents (Sun, Zhang, Cohney, Zhang, Liu, Yuan) | arXiv 2606.05805v1, 4 Jun 2026 | [abstract only] | Proceed/refuse/update guardrail. ASR down to 10.42% on ASB/AgentHarm with the "best safety-utility trade-off". Measures the downstream utility of guard interventions, not finance. |
| AI Agents Push Humans Out of the Loop (Mitchell, Ghosh, Passi) | arXiv 2608.23642v3, 6 Sep 2026 | [abstract only], position paper | Human oversight degrades with automation. Framing only. |
| CrossAlpha (annual-report cross-market factor benchmark) | arXiv 2605.29286v3 | checked full text for India | Covers US/JP/TW/KR/HK only. **No India.** |
| `sayaliwangane/-nifty-agents-cost-study` | GitHub release "NIFTY 50 dataset (Oct 2025)" | **UNVERIFIED** (search snippet only; repo not opened) | Reportedly an M.Tech study of TradingAgents on NSE data with STT, stamp duty and GST costs. Not a paper, but the closest NSE+agent artifact. Check before claiming NSE novelty. |

---

## 2. Relevance matrix

| # | Paper | (a) override-outcome | (b) agent calibration | (c) NSE |
|---|---|---|---|---|
| 1.1 | KTD-Fin 2605.28359 | None–Partial | **Strong** | None |
| 1.2 | Ordinal Gates 2609.00187 | Partial | **Strong** (non-agent) | None |
| 1.3 | Raven-Agent 2607.03015 | **Partial–Strong** (design) | Partial | None |
| 1.4 | TrustTrade 2603.22567 | Partial | Partial (gap only) | None |
| 2.1 | IndiaFinBench 2604.19298 | None | None | Partial |
| 2.2 | NIFTY-50 sentiment 2512.20082 | None | None | Partial |
| 2.3 | AlphaNiftyAI (Digital Finance 2026) | ? | ? | Partial–Strong, **UNVERIFIED** |
| 3.1 | TradeArena 2605.28850 | **Partial–Strong** | None | None |
| 3.2 | Smart-vending overrides 2607.00420 | **Strong** (method) | None | None |
| 3.3 | Angelova–Dobbie–Yang RESTUD 2026 | Partial (method) | None | None |
| 3.4 | Oversight Has a Capacity 2606.08919 | Partial | Partial | None |

---

## 3. What is still open

**Lane 1 (calibration):**
- Stated confidence of an LLM trading agent has been measured once, as one ECE scalar per model (KTD-Fin: 0.25–0.43, CSI300, price-only).
- Ordinal Gates shows that for single-headline LLM signals the problem is **resolution**, not reliability: recalibration fixes ECE but cannot improve a gate.
- Not yet done:
  1. calibration of **each agent role** (technical/news/fundamental/macro) vs. the planner's final confidence;
  2. whether stated confidence **moves with the investor mandate** on byte-identical evidence. If it does, confidence is policy-contaminated, not epistemic;
  3. whether confidence predicts **which proposals the deterministic layer vetoes**, and whether vetoed high-confidence proposals were right;
  4. a Murphy reliability/resolution split with bootstrap CIs, a correct label for SELL/HOLD, and a test of the policy's fixed confidence threshold against Ordinal Gates' "0/18" prediction.
- This is a defensible, narrower RQ2. "First to measure ECE for trading agents" is no longer defensible.

**Lane 2 (India):**
- I found no arXiv or peer-reviewed evaluation of an LLM trading agent on NSE with leakage control (masking or post-cutoff windows) and Indian frictions (STT/stamp/GST, T+1, price bands/circuit filters, F&O ban list).
- Existing Indian work is regulatory QA (IndiaFinBench), leaky headline-sentiment classification (2512.20082), and one paywalled NIFTY-50 multi-agent system whose numbers I could not verify (AlphaNiftyAI).
- KTD-Fin's handling of A-share price limits and masking is the template to copy.
- NSE as a **second-market replication** of the override and calibration findings is defensible. NSE on its own is not a contribution.
- **Action:** obtain the AlphaNiftyAI full text and inspect the nifty-agents-cost-study repo before writing "first on NSE".

**Lane 3 (override outcomes):**
- Rigorous override-outcome estimation exists where **humans override algorithms**: Angelova et al. find 90% of overriders underperform; the vending experiment finds free overrides hurt sales and capped overrides do not.
- For **rules overriding LLM trading proposals**, the evidence is thin:
  - TradeArena's gate-off ablation runs on a non-LLM reference agent and *raises* return (0.468 vs. 0.423) while increasing rejects.
  - Raven's deterministic layer improves ROI over forecast-only only at point-estimate level, with overlapping CIs on 42 trades.
  - CLQT, OpenPM and BiasMix (see A) do not compute per-intervention P&L.
- Still open: **per-intervention counterfactual outcomes of deterministic vetoes and clips on LLM proposals.** For each clause × policy × agent, with:
  - a re-run noise floor;
  - the vending paper's "override budget" as an ablation;
  - Angelova-style heterogeneity (which clauses add value and which destroy it).
- Frozen-evidence replay gives exact counterfactuals for each proposal, which is stronger identification than any of these papers had. That is the paper.

---

## 4. Search log

- **Queries run:**
  - LLM trading-agent ECE/Brier against realized returns;
  - LLM stock-forecast calibration;
  - the "per-order confidence" Brier phrase;
  - Indian financial NLP / NSE / BSE / NIFTY LLM agents;
  - emerging-market LLM benchmarks;
  - human overrides of algorithms and their outcomes;
  - guardrail counterfactual and utility analysis;
  - risk-layer ablations in LLM trading;
  - verbalized-confidence overconfidence.
- **Opened but excluded:** CrossAlpha (no India); "LLMs and Stock Investing: Is the Human Factor Required?" (arXiv 2603.19944, Crisostomo & Mykhalyuk; abstract only; argues for human oversight but runs no override-outcome experiment and names no specific market).
- **Not opened (abstract or snippet only, would need a read if time allows):** 2512.16030 (epistemic calibration via prediction markets); 2605.27668 (Beta-Bernoulli calibrator for LLM forecasting); 2607.08046 (LLM forecasters' internal vs. verbalized calibration); 2607.13083 (Phantom Guardrails); 2607.19449 (Guardrails as Scapegoats).
