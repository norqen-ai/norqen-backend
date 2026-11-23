# Literature Review — Reading List

Rule: every team member reads all ★★★ papers fully. ★★ = one member reads fully, summarizes
for the team. ★ = abstract + skim. Write a 5-line summary per paper into this file as you go:
(1) what they did, (2) what they measured, (3) what they did NOT do, (4) how we differ, (5) one sentence we might cite.

## Pile 1 — Multi-agent trading frameworks (what we improve upon)

| ★ | Paper | Link |
|---|---|---|
| ★★★ | TradingAgents: Multi-Agents LLM Financial Trading Framework (2024) | https://arxiv.org/abs/2412.20138 |
| ★★★ | FinCon: Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement (NeurIPS 2024) | https://proceedings.neurips.cc/paper_files/paper/2024/file/f7ae4fe91d96f50abc2211f09b6a7e49-Paper-Conference.pdf |
| ★★ | FinAgent: Multimodal Foundation Agent for Financial Trading (KDD 2024) | https://arxiv.org/abs/2402.18485 |
| ★★ | FinMem: LLM Trading Agent with Layered Memory (2023) | https://arxiv.org/abs/2311.13743 |
| ★ | QuantAgent (price-driven HFT multi-agent, 2025) | search arXiv |

## Pile 2 — The evaluation crisis (our motivation)

| ★ | Paper | Link |
|---|---|---|
| ★★★ | A Test of Lookahead Bias in LLM Forecasts (Gao, Jiang, Yan, Dec 2025) — READ TWICE | https://arxiv.org/abs/2512.23847 |
| ★★ | Assessing Look-Ahead Bias in GPT Stock Return Predictions (2023) | https://arxiv.org/abs/2309.17322 |

## Pile 3 — Benchmarks & live evaluation (we borrow hygiene, add new questions)

| ★ | Paper | Link |
|---|---|---|
| ★★★ | StockBench: Can LLM Agents Trade Stocks Profitably? (2025) | https://arxiv.org/abs/2510.02209 |
| ★★★ | When Agents Trade: Live Multi-Market Benchmark / Agent Market Arena (WWW 2026) | https://arxiv.org/abs/2510.11695 |
| ★★★ | CLQT: Closed-Loop, Cost-Aware, Strategy-Consistent Benchmark (Jun 2026) — CLOSEST CONCURRENT WORK | https://arxiv.org/pdf/2606.29771 |
| ★★ | LiveTradeBench (2025) | https://arxiv.org/pdf/2511.03628 |
| ★ | From Knowing to Doing: Memory-Controlled Benchmark (May 2026, CSI300) | https://arxiv.org/pdf/2605.28359 |
| ★ | Agentic Trading: When LLM Agents Meet Financial Markets (May 2026) | https://arxiv.org/pdf/2605.19337 |

## Pile 4 — Mandate/persona adherence (⚠️ hottest, closest to RQ1 — cite & differentiate)

| ★ | Paper | Link |
|---|---|---|
| ★★★ | FinPersona-Bench: Longitudinal Psychometric Stability of Financial Agents (Jun 2026) | https://arxiv.org/abs/2606.31522 |
| ★★★ | Diagnosing and Repairing Persona Collapse in LLM Advice (Jul 2026) | https://arxiv.org/pdf/2607.08326 |
| ★★ | ASTRA: Agentic Steerability and Risk Assessment (2025) | https://arxiv.org/abs/2511.18114 |
| ★★ | High-Stakes Personalization for Investor Decision-Making (Apr 2026) | https://arxiv.org/abs/2604.04300 |

## Pile 5 — Cost-aware agents (RQ3 foundations)

| ★ | Paper | Link |
|---|---|---|
| ★★ | Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents (2026) | https://arxiv.org/abs/2602.16699 |
| ★★ | BATS: Budget-Aware Tool-Use Enables Effective Agent Scaling (2025) | https://arxiv.org/abs/2511.17006 |
| ★ | Cost-Aware Evidence Selection in RAG (Jun 2026) | https://arxiv.org/abs/2606.02245 |
| ★ | CostBench (2025) | https://arxiv.org/pdf/2511.02734 |

## Pile 6 — Confidence & calibration (RQ2 foundations)

| ★ | Paper | Link |
|---|---|---|
| ★★ | TrustTrade: Selective Consensus Reduces Decision Uncertainty in LLM Trading (2026) | https://arxiv.org/pdf/2603.22567 |
| ★★ | Uncertainty Quantification in LLM Agents: Foundations & Challenges (2026) | https://arxiv.org/abs/2602.05073 |
| ★ | Are LLM Decisions Faithful to Verbal Confidence? (2026) | https://arxiv.org/pdf/2601.07767 |
| ★ | Agentic Confidence Calibration (2026) | https://arxiv.org/pdf/2601.15778 |

## Pile 7 — Surveys (read first for the map)

| ★ | Paper | Link |
|---|---|---|
| ★★ | LLM Agent in Financial Trading: A Survey (2024) | https://arxiv.org/abs/2408.06361 |
| ★ | LLM Agents in Finance: Survey (Findings of EMNLP 2025) | https://aclanthology.org/2025.findings-emnlp.972.pdf |
| ★ | LLM Agents for Investment Management (ICAIF 2025) | https://dl.acm.org/doi/10.1145/3768292.3770387 |

## Monthly arXiv re-sweep (1st of every month; 30 minutes; rotate owner)

Search arxiv.org for, and log anything new in this file:
- `LLM trading agent policy adherence`
- `financial agent mandate steerability`
- `LLM agent calibration trading`
- `contamination lookahead bias LLM finance`
- `benchmark LLM portfolio agent`

**If something lands on RQ1 directly: don't panic — read it, add a row to the Section-3
table in the plan, and sharpen our differentiators (live + NSE + calibration + cost combination).**
