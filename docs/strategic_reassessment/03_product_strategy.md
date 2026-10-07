# 03 · Product Strategy (honest)

**Question the founder asked:** *"we also want to develop it into a product — something actually worth using."* Here is the honest read and a defensible plan.

---

## 1. The uncomfortable truth about the product

The **product** space is far more crowded than the **research** space. Vibe-Trading (30k⭐, MIT, free) already gives a technical user: a mandate model, multi-agent committees, a risk layer with kill-switch, backtesting across US/China/crypto/**India**/Korea, 18+ data providers, and opt-in live trading. You **cannot** win by being "an open-source multi-agent trading platform" — that product exists, is free, and has a two-year head start and a community.

So the product thesis must **not** be "more agents / more markets / more data." It must be a **wedge**: one user, one pain, one thing you do that Vibe-Trading structurally does *not*.

---

## 2. The wedge: *trust and auditability for the Indian retail/analyst who cannot code*

Vibe-Trading is a **developer tool** — a CLI + MCP for people who write `vibe-trading run -p "..."`. It optimizes for *capability*. It does **not** optimize for a non-coder who needs to *trust and defend* a recommendation. That is the gap.

- **Primary user:** the **Indian retail investor / independent RIA (Registered Investment Adviser) or research analyst** who wants **explainable, auditable, mandate-respecting** research on NSE names — and who will *never* touch a CLI. They are drowning in Telegram tips and finfluencer noise, and (post-SEBI-crackdown on unregistered advice) they need *defensible, logged* reasoning, not a black-box "BUY."
- **Secondary user:** the **student / researcher** who wants to benchmark their own agent against yours (they consume the *released benchmark* from the research track — the two tracks share one artifact).

**Why they'd pick you over Vibe-Trading / World Monitor:**
- vs **Vibe-Trading:** you are *no-code, explanation-first, and mandate-auditable*. Your signature screen is not a backtest curve — it's **"here is exactly why, here is the counter-thesis, here is when this becomes wrong, and here is the rule that would have vetoed it."** Vibe-Trading shows *what*; you show *why + why-not + under-what-mandate*.
- vs **World Monitor:** World Monitor tells you the world is on fire; it never tells you what to do about your NSE portfolio. Different category.

---

## 3. The core product workflow (the MVP)

One screen, one decision, fully traceable:

1. User picks a stock (or a watchlist) and a **policy** (choose a preset — Conservative / Long-Term / Aggressive / Intraday — or answer a 6-question wizard that emits the JSON).
2. System retrieves **time-valid** evidence (never post-dated).
3. Specialist agents produce distinct analyses; ML tools produce the numbers.
4. Risk engine may **VETO**.
5. Output = a **Decision Card**: action · size · confidence · **thesis · counter-thesis · the evidence with dated sources · which policy clauses bound the decision · what would invalidate it · abstain-or-act.**
6. Every card is **logged**; the **Adherence badge** ("0 policy violations this month") and the **Veto log** ("where the rules said no") are first-class pages.
7. **Paper trading only.** The card timestamp is recorded; later the outcome is scored (the same loop that feeds the paper).

**The demo money-shot is the product's home page:** two panels, same stock, same day — Aggressive **BUYs 6.4%**, Conservative **WAITs** — "why" one tap away. *This already runs today* (`run_demo.py`). It is the single most convincing 10 seconds you have; build the UI around it.

---

## 4. Primary/secondary user decision

| Candidate user | Verdict | Why |
|---|---|---|
| Indian retail investor wanting explainable research | **PRIMARY** | Underserved, trust-starved, non-coder → Vibe-Trading can't reach them; NSE focus is a moat here even though it isn't a *research* moat |
| Student/researcher benchmarking agents | **SECONDARY** | Free distribution of the benchmark = academic credibility + inbound; near-zero extra build (it's the research artifact) |
| Financial analyst (event-driven company research) | Tertiary | Real need but longer sales cycle; revisit post-MVP |
| "Everyone" | **Reject** | The death of every student product |

---

## 5. What to build in the MVP — and what NOT to

**Build (aligned with Piyush's plan):**
- Decisions feed → Decision detail ("Why?") → **Compare view (the money-shot)** → **Veto log** → Policies (read-only, then the wizard) → Adherence badge.
- Read the same `decisions_*.jsonl` the research loop writes. One schema, two consumers.
- Boring-trustworthy design (your own handoff says it): confidence = neutral blues, BUY green / SELL red / WAIT grey, VETO = amber shield. Dark mode.

**Do NOT build in the MVP (these sink student products):**
- ❌ Real-money / live-broker execution. Ever. (It's also your review *strength* — "responsible.")
- ❌ A World-Monitor-style global dashboard. Out of scope, out of category.
- ❌ Portfolio optimization, tax, options, HFT, social feed, mobile app.
- ❌ A second market beyond US + NSE.
- ❌ Accounts/billing before you have 10 users who want it.
- ❌ Anything that competes with Vibe-Trading on *developer capability*. You lose that race by definition.

---

## 6. Safety, regulatory, and honesty boundaries (India-specific)

A disclaimer does **not** solve regulation — say so plainly.
- Present strictly as **research / decision-support**, **not** investment advice; in India, giving personalized investment advice for consideration requires **SEBI RIA registration** — the product must stay *educational/analytical* and *paper-only* until/unless that path is taken.
- **No promise of profit.** No fabricated citations (every evidence item carries a dated source or it doesn't appear). Human-in-the-loop before any hypothetical execution. Audit logging + model/prompt/data versioning already designed in. State known limitations on every card.

---

## 7. Product verdict

- **As "another AI trading platform": HEAVILY DUPLICATIVE — do not build that.**
- **As "the no-code, explanation-first, mandate-auditable NSE research companion that also *is* an open benchmark": PROMISING and defensible** — because the trust/auditability/no-code angle is exactly what the developer-first incumbents structurally ignore, and the benchmark gives you free academic distribution.
- The product and the paper **share one artifact** (the logged, replayable decision cards). That is the rare case where building the product *is* building the research instrument. Lean into it.
