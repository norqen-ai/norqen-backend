# 07 · Methodology & References — the solid core (two layers)

The system has **two measurement layers**. Keeping them separate is what makes the project
both a credible quant product AND a defensible paper.

```
        ┌─────────────────────────────────────────────────────────────┐
   L2   │  AGENT-TRUSTWORTHINESS  (our research novelty — RQ1/2/3)      │
        │  adherence · calibration (ECE/Brier) · evidence cost         │
        ├─────────────────────────────────────────────────────────────┤
   L1   │  QUANT-FINANCE CORE  (industry-standard; makes it credible)  │
        │  IC signal-vetting · vol/Kelly sizing · Sharpe/Sortino/DD ·  │
        │  VaR/CVaR · transaction costs · deflated-Sharpe / PBO        │
        └─────────────────────────────────────────────────────────────┘
```

- **L1 answers "is the trading any good?"** with the exact math quant funds use. This is what
  makes the product real and stops the paper being dismissed as "LLM vibes." Built: `src/eval/quant.py`.
- **L2 answers "is the AGENT honest / obedient / efficient?"** — the questions nobody else measures.
  This is the contribution. Built: `src/eval/adherence.py` (RQ1); calibration + cost next.

The agent's `confidence` is **not trusted** — it is the *object of study* in L2 (RQ2 asks: when it
says 76%, is it right 76% of the time?). L1 keeps the signals and sizing grounded in real math so
the confidence has something honest to be measured against.

---

## Layer 1 — Quant-finance canon (what we implement & cite)

| Method | Paper | What it gives us | Where in code |
|---|---|---|---|
| Mean-variance portfolio | **Markowitz 1952**, *Portfolio Selection* | the risk-return tradeoff foundation | sizing rationale |
| Sharpe ratio | **Sharpe 1966/1994** | risk-adjusted return (the headline metric) | `quant.sharpe` |
| Downside risk | **Sortino & Price 1994** | penalise only harmful volatility | `quant.sortino` |
| Drawdown / Calmar | Young 1991; Magdon-Ismail 2004 | worst peak-to-trough; return-per-pain | `quant.max_drawdown/calmar` |
| Optimal sizing | **Kelly 1956** | bet size from edge & variance (we use ½-Kelly) | `quant.kelly_fraction` |
| Vol targeting / risk parity | RiskMetrics (J.P. Morgan 1996) | size from risk, not confidence | `quant.vol_target_size` |
| Factor models | **Fama & French 1993**; **Jegadeesh & Titman 1993** (momentum); Carhart 1997 | what "alpha" means vs known factors | signal design (next) |
| **Information Coefficient** | **Grinold & Kahn**, *Active Portfolio Management* | vet a signal: IC = corr(prediction, realised return); IR = IC·√breadth | `quant.information_coefficient` |
| Tail risk | VaR / CVaR — Rockafellar & Uryasev 2000 | expected loss in the bad tail | `quant.var/cvar_historical` |
| Volatility models | **Bollerslev 1986 (GARCH)**; EWMA | time-varying risk for sizing/regime | planned (`src/ml`) |
| **Backtest overfitting** | **López de Prado 2018**, *Advances in Financial ML*; Bailey & López de Prado 2014 (**Deflated Sharpe**, **PBO**) | proof our results aren't curve-fit — directly supports our leakage-free story | eval (next) |

**Fundamental Law of Active Management** (Grinold): `IR ≈ IC × √breadth`. This tells us plainly:
weak signals (low IC, which our momentum test just confirmed) can only help if applied across
**many** names — motivating the 40-stock universe, not 3.

---

## Layer 2 — Agent-trustworthiness (our novelty) & its foundations

| Method | Paper | Role |
|---|---|---|
| Calibration: ECE, reliability | **Guo et al. 2017**, *On Calibration of Modern NNs* | RQ2 — is stated confidence honest? |
| Proper scoring | **Brier 1950** | RQ2 — Brier score of confidence vs outcome |
| Distribution-free intervals | Vovk et al. (conformal prediction) | RQ2 — calibrated abstention |
| Cost-aware stopping | Calibrate-Then-Act (2026); BATS (2025) | RQ3 — evidence efficiency |
| Mandate adherence | **FinPersona-Bench (2026)**; hierarchical-safety adherence (2506.02357) | RQ1 — closest work, we differentiate |

---

## What existing agentic-finance systems do — and their unsolved problems (cite in Related Work)

(Full summaries in `../../02_Workshop_Plan/Literature_Review_Summaries.md`.)

| System | How it works | Problem it left open → our answer |
|---|---|---|
| **TradingAgents (2024)** | firm-style agents (analysts → bull/bear debate → trader → risk) chasing returns | reports Sharpe on possibly-contaminated data; never checks obedience/calibration → **we do** |
| **FinCon (NeurIPS'24)** | manager–analyst hierarchy + verbal-reinforcement risk control | same — returns-first, no honesty/adherence metric |
| **FinMem / FinAgent** | layered memory / multimodal single agent | assume the persona is followed; never measure it |
| **StockBench (2025)** | contamination-free multi-month benchmark | finds most agents can't beat buy-and-hold → **motivates measuring behaviour, not returns** |
| **The Alpha Illusion (2026)** | argues reported alpha ≠ deployment evidence; lists 6 validity tests incl. calibration | **this is our mandate** — we implement those tests |
| **CLQT (2026)** | cost-aware, "diagnose before rank", capability scorecard | no policy-conditioning / calibration / NSE → we add all three |
| **FinPersona-Bench (2026)** | mandate decay over time, synthetic market, 18 LLMs | longitudinal & synthetic → **we go cross-sectional, real, released** |

---

## The methodology sentence for the paper
> "We evaluate an LLM investment committee on two levels: standard quant metrics
> (IC, Sharpe/Sortino, drawdown, VaR, deflated-Sharpe) establish whether the trading is
> sound, and a novel trust layer (policy-adherence, confidence calibration, evidence cost)
> establishes whether the *agent* is obedient, honest, and efficient — the latter measured
> leakage-free and cross-sectionally on identical evidence across US and NSE."
