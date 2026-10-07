# Revised Project Plan — 5 Oct 2026

Supersedes the research framing in `ICAIF_2026_AI4F_Month_Plan.md` (8 Sep). Evidence behind every change:
`lit_review_oct2026/A_threat_deep_read.md`, `B_calibration_india_override.md`, `C_survey_table.md`, `D_venues.md`.

## 1. What changed and why

| Before (Aug–Sep) | Now | Why |
|---|---|---|
| "First policy-conditioned trading framework / mandate benchmark" | System = the instrument, ≤1 page in any paper | OpenPM (2608.09988), CLQT (2606.29771), BiasMix-Finance (2608.28646) already ship LLM-proposes / deterministic-layer-enforces + replay + audit |
| RQ1 "different mandates → different decisions" as a claim | Replicate only | PortBench (2605.27887): conservative→aggressive raises risk exposure in 103/110 matched pairs |
| "Unguarded LLM breaks mandates" as a claim | Replicate (done 4 Oct, 40 stocks) | BiasMix-Finance: 47.6–85.7% first-pass violations |
| RQ2 calibration "first" | Secondary: per-policy + resolution breakdown | KTD-Fin (2605.28359) already reports trading-agent ECE 0.246–0.425; Ordinal Gates (2609.00187) shows near-zero resolution |
| RQ3 adaptive evidence cost | Future work | Weakly pre-empted; no outcome data; our baseline frontier is flat |
| ICAIF'26 AI4F (8 Oct) | Skip | In-person Milan 14 Nov, Schengen visa, €207–647 non-refundable by 19 Oct, non-archival |

## 2. The main contribution (open as of 5 Oct 2026)

**When the deterministic safety layer overrides an LLM trading agent, does the decision's realised outcome get better or worse — clause by clause and investor profile by profile?**

Nobody measures this: BiasMix reports no returns; OpenPM's caps never bind; CLQT never ablates its constraint layer alone; TradeArena/Raven-Agent are non-LLM or tiny-N. Template: Policy-as-Skill's controller-intervention analysis (helpful / harmful / neutral split, paired tests).

Supporting exhibits: (a) numeric policy vs text profile on identical evidence (done: 0% vs 64.4%), (b) cross-profile divergence net of a same-profile re-run noise floor, (c) stated-confidence calibration per profile with resolution, (d) US vs NSE (0 of 30 surveyed papers use Indian data).

## 3. Protocol (pre-register before running)

1. Bundles: 40-stock universe × ≥15 historical decision dates in **2025–2026** (after gpt-4o-mini's training cutoff) → ≥600 bundles, price-only + fundamentals snapshot (historical news is the gap — document it).
2. For each bundle × profile × model × 2 seeds: ONE unguarded LLM proposal U; apply the risk layer post hoc to the same proposal → G. Never compare separate runs.
3. Utility fixed in advance: realised P&L over horizon h ∈ {5, 20} trading days with the stop applied, in the profile's risk-budget units; WAIT = 0.
4. Report: intervention rate; helpful / harmful / neutral counts; net Δu with paired-bootstrap CI; exact sign test; stratified by profile and clause; noise floor from seed re-runs.
5. Fix the design tension: profiles choose different tools → run a 2×2 {profile-specific view, common view} so evidence-selection effects separate from decision-rule effects.
6. Models: gpt-4o-mini + one other API model + one open-weight model (Ollama).

## 4. Timeline

| When | Deliverable | Owner |
|---|---|---|
| 5–10 Oct | Paper Assessment (5 Oct) + Project Assessment-I; team writes the paper's prose sections | all |
| 11–18 Oct | Historical bundle builder (2025–26 dates) + outcome labeller; pre-register §3 in `PREREGISTRATION.md` (dated amendment) | M |
| 19–31 Oct | Override-outcome runs (gpt-4o-mini, 2 seeds); 2×2 view ablation | M + O |
| Nov | Second/third model; calibration per profile; dashboard MVP (decision feed, "why" page, veto log) | O, P |
| Mid-Nov | Start the live daily paper-trading loop (US + NSE) | O |
| 20 Nov | AAAI-27 workshop deadline (list announced by 16 Oct — check for a finance/agents workshop) | M |
| Dec–Jan | Full results; submit to a Scopus conference from the dept list (archival — needed for the BE "published paper" requirement) | all |
| ~1 Feb 2027 | ICLR-27 FinAI-type workshop (if announced ~29 Nov) | M |

## 5. Citations we must carry (intro ¶2)
OpenPM · CLQT · BiasMix-Finance (co-authors include Raj Dandekar — cite and build on it explicitly) · PortBench · FinPersona-Bench · Policy-as-Skill · KTD-Fin · Alpha Illusion (use its TradingAgents reproduction: Sharpe 0.43 before costs, 0.22 after — not TradingAgents' own 8.21).

## 6. Honesty guardrails (unchanged, still binding)
- Guarded-mode 0% violations is by construction — never report it as a finding.
- Text-mode "violations" are against limits the LLM was never shown — describe them as "a prose persona does not produce the intended limits".
- No returns claims from the 3-year numeric baselines (IC ≈ 0); no "first" claims on NSE until AlphaNiftyAI (Digital Finance, 2026) is checked via the PICT library.
- StockBench: quote its Table 2, not its abstract (they disagree).
