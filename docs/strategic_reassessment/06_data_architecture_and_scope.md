# 06 · Data Architecture & Scope — evaluating the "make it institutional" advice

Context: an LLM assistant advised building a modular multi-provider data layer, supporting
"any listed stock," a symbol resolver, and a portfolio agent — to make the BE project look
institutional. Here is the honest evaluation and what we actually did.

## Verdict in one line

**~70% good engineering, but aimed at the wrong goal.** Every suggestion makes a nicer
*commodity trading assistant* — which is exactly what Vibe-Trading (30k★) already is, and
exactly the crowded space we're trying NOT to be. None of it touches our differentiator
(the evaluation suite). We adopted the parts that are cheap and correct, and refused the
parts that add scope without adding research value.

## Point-by-point

| GPT suggestion | Verdict | Why |
|---|---|---|
| Don't build on yfinance alone; **modular provider layer** | **ADOPT** ✅ (built `src/data/providers.py`) | Correct architecture. Agents call `MARKET.get_*()`, never `yfinance`. Providers swap freely; research stays reproducible (one place controls data). |
| Add Finnhub / AlphaVantage / Polygon / TwelveData / FMP | **ADAPT** ⚠️ | The *abstraction* is right; **six providers now is premature** (more keys, more rate-limits, more failure modes, zero research value). Recommended stack: **Yahoo (default) + Finnhub (news/fundamentals) + FRED (macro)**. Finnhub auto-activates when `FINNHUB_API_KEY` is in `.env`. |
| **Support any listed stock**, not 3 | **ADOPT for the PRODUCT** ✅ — and we already do | Our tools were always `technical(ticker)`, ticker-agnostic. Verified live on NVDA, INFY.NS, etc. "3 stocks" was only what we tested. |
| Symbol resolver (company name → ticker) | **ADOPT** ✅ (built `src/data/resolver.py`) | Good product UX. India-first: "Reliance"→RELIANCE.NS, "Infosys"→INFY.NS. Returns candidates for disambiguation. |
| Ticker-agnostic agents (`analyze_stock(ticker)`) | **ALREADY TRUE** ✅ | No hardcoded companies anywhere in agent logic. |
| **Portfolio agent** (risk, diversification, sector) | **DEFER** ⏸ | A real product feature with **zero research value** for RQ1/2/3. Post-MVP; do not let it eat the semester. |
| Risk agent with VaR / Kelly sizing | **KEEP SIMPLE** | We already have a deterministic risk-veto engine (the research needs a *clean, auditable* veto, not a fancy one). VaR/Kelly are nice-to-haves, not the point. |

## The distinction GPT completely missed (the important one)

**PRODUCT = any stock. RESEARCH = a fixed, frozen universe.** These are different and both correct:

- The **product** should analyse any ticker the user types (done).
- The **benchmark/experiments** must use a **bounded, point-in-time universe** (`config/universe.json`, 20 US + 20 NSE, frozen 2026-08). A benchmark run over "any of 10,000 stocks" is **not publishable** — it invites survivorship bias (you'd only test companies that still exist) and makes evidence non-comparable across policies/models. GPT optimised for "looks impressive," not "is a valid experiment," so it never raised this.

Live proof it matters: `TATAMOTORS.NS` in an early universe list is now **delisted** (Tata Motors demerged in 2025). A frozen, dated universe with documented changes is exactly how you avoid silently testing on a stale set.

## The reframe we must hold

Chasing "institutional-looking" features is the trap. If we spend the semester on *six providers +
any stock + portfolio agent + fancy resolver*, we will have built **a worse Vibe-Trading and a weaker
paper.** The trading system must be **solid, reliable, and any-stock** — because it is the *instrument
under test* — but it is not the destination. The destination is the **evaluation suite**.

## What actually makes us unique (and is now real)

Built this turn: `src/eval/adherence.py` + `score_adherence.py` — the first RQ1 metric. On the very
first run it produced a genuine finding:

> **Cross-policy divergence = 0%.** The system currently collapses to `WAIT` regardless of mandate —
> confidence and cost differ across policies, but the final *action* does not. That is weak steerability,
> and it is a real research result (and a problem to fix) that no "impressive architecture" would ever expose.

That single number is worth more to the paper than any number of data providers.

## Recommended stack & next moves

- **Data:** Yahoo (default) + Finnhub (`FINNHUB_API_KEY` → auto) + FRED (macro). Stop there.
- **Scope:** product = any stock (done); experiments = frozen `universe.json`.
- **Effort split from here:** system just needs to be *reliable*; the *research* effort goes into the
  evaluation suite — calibration (RQ2), cost frontier (RQ3), and fixing the WAIT-collapse so steerability
  actually shows.
