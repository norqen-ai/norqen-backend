# FinFM @ AAAI-27 — Team Guide and TODO

**Read this whole file once (≈15 minutes) before doing anything.** It explains what the paper is, what has already been done, how the code works, and exactly what each of us does next.

| | |
|---|---|
| **Venue** | FinFM workshop at AAAI-27 (finfm.finhorizons.org), **research track, short paper** |
| **Length** | **max 4 pages** of main text; references and appendix are unlimited and come after |
| **Review** | double-blind → no names, no PICT, no "Norqen", no GitHub links in the PDF |
| **Hard deadline** | 20 Nov 23:59 AoE = **21 Nov 2026, 5:29 PM IST** |
| **Our deadline** | **submit by 21 Nov, 12:00 noon IST** |
| **Repo** | `github.com/norqen-ai/norqen-backend`, branch **`be-final-year-project`** |
| **Paper source** | `paper_finfm/` in that branch (also sent as `paper_finfm_overleaf.zip`) |
| **Owners** | **Omkar** = Setup + Limitations + open-weight model run · **Piyush** = Overleaf + Related Work + citations + anonymity + OpenReview · **Malhar** = Intro + Results + final 4-page cut + submission |
| **Availability** | Malhar is in Mumbai 18 Nov afternoon → 20 Nov afternoon (WhatsApp only) |

---

## 1. The paper in plain words

**Draft title:** *Fix What Is Checked, Inflate What Is Not: How LLM Trading Agents Respond to Investor-Mandate Enforcement*

An investor has rules (a "mandate"): for example, a conservative investor allows **at most 2%** of the portfolio in one stock, a stop-loss of **3%**, and a trade only when confidence is **≥ 0.75**. Many LLM trading systems put a rule-checker around the LLM to enforce such rules. Papers usually report only "how often were the rules broken", and every rule-checker can make that 0% simply by refusing to trade.

We ask: **when you enforce an investor's rules on an LLM trading agent, what does the agent actually end up doing, and what happens to the trades?**

We take one fixed set of LLM trade proposals and enforce the rules in **four different ways**, then compare them:

| Way of enforcing | What it does | What we found |
|---|---|---|
| **Block** | Rule-checker says no → do nothing (WAIT) | 0% violations, but only ~7% of the LLM's trades survive |
| **LLM risk manager** | A second LLM reviews the trade and may approve, shrink or reject | 0% violations, but only ~2% survive: it rejects instead of shrinking |
| **Deterministic repair** | Code shrinks the size to the limit and tightens the stop | 0% violations, ~80% of trades survive, risk roughly halved |
| **Feedback (new)** | Rule-checker tells the LLM *why* it was rejected; the LLM revises (up to 3 tries) | Fixes size and stop exactly. **And it raises its own "confidence" number to the required bar, with no new information** |

**The headline finding (our novelty):** if the feedback says "confidence 0.65 is below the required 0.75", the model's next answer simply says 0.75. In a **control** where we hide the confidence rule from the feedback (but still enforce it), the models almost never raise it. Nothing about the stock changed in either case, so the confidence change is not a real change of belief: it is the model saying whatever gets the trade approved. Our October data also shows the LLM's confidence does not predict which trades win (AUC 0.503 ≈ coin flip). So **a confidence gate based on the LLM's own number is fake safety.**

**Design rules the paper ends with:**
1. Give the agent the investor's limits as numbers, not a "be conservative" persona.
2. Repair trades instead of refusing them, and always report how many trades survive and the risk, not only the violation rate.
3. Never gate a trade on a number the agent reports about itself; gate on numbers code computes.

**What we do NOT claim:** that the system makes money. The analysts' signals have almost no predictive power (information coefficient between −0.07 and +0.05), so no strategy, LLM or code, beat simply holding the market. **Never write "profitable", "outperforms", "alpha" or "beats" anywhere.**

---

## 2. Why this is new (the gap, with the papers)

| Paper | What it did | What it leaves open (our gap) |
|---|---|---|
| TradingAgents (arXiv 2412.20138); FinCon (NeurIPS 2024) | Multi-agent LLM traders with an LLM "risk manager" | Never test whether that risk manager actually enforces anything |
| BiasMix-Finance (ICLR 2026 FinAI workshop) | LLMs break investor limits 48–86% of the time; projection fixes it to 0% | No real outcomes, no comparison between ways of fixing |
| OpenPM (arXiv 2608.09988) | Turns a written mandate into constraints, code enforces them | Tests one mandate; its limits never actually trigger |
| CLQT (arXiv 2606.29771) | Benchmark with a constraint layer | Credits the constraint layer without testing it alone |
| TradeArena (arXiv 2605.28850) | Risk layer that can clip, block or annotate | Mostly synthetic data |
| Inside the Trading Loop (arXiv 2611.11657) | Says LLMs shouldn't control position size | One model, one component, no investor profiles |
| Sycophancy (Sharma et al., ICLR 2024); reward hacking (Skalse et al., NeurIPS 2022) | LLMs bend to feedback; optimising a measured target invites gaming | Not shown in a trading-agent pipeline |

**Gap in one sentence:** nobody has compared different ways of enforcing an investor mandate on the *same* LLM trade proposals using real outcomes, and nobody has studied how the agent *reacts* to enforcement feedback.

⚠️ These summaries came partly from abstracts. **Piyush verifies each one in the paper's full text** (Section 7).

---

## 3. What has already been done

### 3.1 The system (BE project)
For a stock on a date:
1. **Five analysts** each give an opinion: direction (−1 sell … +1 buy) and confidence (0–1). Four are LLMs (technical, news, fundamentals, macro), one is a small ML model (logistic regression on price history).
2. **Investor profile** (4 profiles, `code/config/policies/*.json`):

   | Profile | Max size | Stop-loss | Confidence bar | Holding period |
   |---|---|---|---|---|
   | Conservative | 2% | 3% | 0.75 | 20 days |
   | Long-term | 5% | 12% | 0.70 | 40 days |
   | Intraday | 4% | 1.5% | 0.65 | 1 day |
   | Aggressive | 8% | 5% | 0.60 | 5 days |
3. **A decision-maker** turns the opinions into a trade: BUY/SELL/WAIT, size, stop-loss, take-profit, confidence. Either **code** (formula) or an **LLM**.
4. **Risk engine** (`code/src/risk/engine.py`, no AI): checks size ≤ cap, stop present and ≤ limit, confidence ≥ bar. Returns APPROVED or VETOED with written reasons like `position 10.00% exceeds policy cap 2.00%`.
5. Everything is logged so any decision can be replayed exactly.

### 3.2 The October experiment (45,600 decisions)
- **1,900 "cases"** = 100 stocks (50 US, 50 Indian NSE) × 19 monthly dates (Jan 2025 – Jul 2026). For each case the five analysts' opinions were computed **once, using only information available on that day**, and frozen. All dates are **after** the three models' training cutoffs, so they can't have memorised what happened.
- Each case was given to **3 models** (gpt-4o-mini, gpt-4.1-mini, gpt-5-mini) × **4 profiles** × **2 prompt styles**:
  - **persona**: "you are a conservative investor…" (no numbers)
  - **rules**: the actual numbers ("max 2%, stop 3%, confidence ≥ 0.75")
- 1,900 × 24 = **45,600 decisions**. Each was scored on what the stock really did next (enter next day's open, hold for the profile's period, stops checked on daily high/low, trading costs 14 bp US / 36 bp NSE).
- One example row: *Apple, 15 Apr 2025, aggressive profile, gpt-4.1-mini, persona → BUY 15%, stop 7%, confidence 0.70.* Cap is 8%, so it's a violation. As proposed it earned +45 bp, repaired to 8% +24 bp, blocked 0.
- "bp" = basis point = 0.01% of the portfolio.

**October results (all still valid):**
- Persona → 53.8% of decisions break the size cap; the engine vetoes 93% of persona trades. Sizing ignores the investor: aggressive positions are only 1.4× conservative ones (the rules imply 4×). With numbers stated → 0% violations.
- LLM confidence doesn't rank winning trades (AUC 0.503). LLM sizes don't track returns either.
- Repair halves P&L swings (standard deviation 53.7 → 22.2 bp), but shrinking every trade by the same amount does equally well — so repair's value is "legal trades without giving up trading", **not** "better trades".

### 3.3 The new experiment (done 17 Nov)
Script `code/run_finfm_arms.py`, results in `code/logs/finfm_2027/`:
- **Feedback arm:** take a persona proposal the engine vetoed, show the same model its proposal + the engine's reasons, let it revise (≤ 3 rounds). Still vetoed after that → WAIT.
- **Control (`--hide-conf`):** same, but the feedback never mentions the confidence rule (the engine still enforces it).
- Run on **every** persona trade vetoed for low confidence, all 3 models. Compared like-for-like on proposals that also broke size/stop, so both arms get a revision round.
- **LLM risk manager re-test:** the October prompt vs a "repair-first" prompt that tells it to fix trades rather than reject them (800 trades per model).

**Results of the new experiment (full run, 0 failed calls; all in `code/logs/finfm_2027/scores.txt`):**

*Feedback that mentions the confidence rule vs the control that hides it* (proposals that broke the confidence rule **and** size/stop, so both arms get a revision):

| Model | Cases | Raised confidence to the bar — rule shown | — rule hidden (control) | Trades kept — shown | — hidden |
|---|---|---|---|---|---|
| gpt-4o-mini | 568 | **65.8%** | 0.5% | 65.1% | 0.5% |
| gpt-4.1-mini | 332 | **94.0%** | 0.9% | 93.7% | 0.9% |
| gpt-5-mini | 1,670 | **99.9%** | 14.6% | 95.5% | 14.5% |
| Pooled | 2,570 | **92%** | **10%** | | |

- gpt-4o-mini and gpt-4.1-mini mostly write **exactly** the bar value (e.g. 0.75); gpt-5-mini writes a number just above it.
- gpt-5-mini changes its confidence on almost every revision anyway (it can't run at temperature 0), which is why its control is 14.6% and not ~0%. The gap (99.9% vs 14.6%) is still huge.
- No new information about the stock is given in either arm. So the confidence change is driven by being told the bar, not by evidence.
- On all vetoed trades (800 per model), feedback brings size exactly to the cap in 63–100% of cases and keeps 92–100% of trades, compared with 52–94% for deterministic repair.

*LLM risk manager, two prompts* (800 trades per proposer model, reviewer gpt-4o-mini):

| Proposals from | October prompt ("approve, modify or reject") | "Repair-first" prompt (fix it, reject only if not worth it) |
|---|---|---|
| gpt-4o-mini | 0.0% kept | 52.6% kept |
| gpt-4.1-mini | 0.1% | 52.8% |
| gpt-5-mini | 5.5% | 23.0% |

Deterministic repair keeps 52–94% of the same trades.

So the risk manager's refusal is partly a **prompt default**. The paper must say "with a standard prompt it refuses", not "LLM risk managers can't repair".

*Exploratory, not for the main text yet:* for gpt-5-mini, trades that passed only because confidence was raised won 39% of the time vs 52% for trades that were above the bar to begin with; for the other two models there's no difference. The two groups differ in profile mix, so this needs a careful matched comparison before it can be claimed.

---

## 4. How the code works (map)

Everything runs from `code/`. Python env: `code/.venv`.

```
code/
├── config/policies/*.json      the 4 investor profiles
├── config/universe.json        stock list
├── src/
│   ├── pit/                    "point-in-time" versions of everything (used by the paper)
│   │   ├── data.py             prices, fundamentals, news as of a past date
│   │   ├── agents.py           the 5 analysts, rebuilt for a past date
│   │   ├── llm_client.py       one cached client for OpenAI + Groq models (every call cached in data/pit/llm_cache.sqlite)
│   │   ├── outcomes.py         scores a trade: entry next open, stops on daily high/low, costs
│   │   └── universe.py         the 100 stocks
│   ├── agents/planner_graph.py LangGraph planner: asks analysts in the profile's order; builds the LLM prompts
│   ├── agents/llm.py           output schema for an LLM trade proposal (DecisionProposal)
│   ├── core/                   profile loader, position sizing formula, data classes
│   ├── risk/engine.py          the rule-checker (no AI)
│   └── audit/log.py            decision log + frozen evidence bundles
│
├── build_pit_bundles.py        step 1: build the 1,900 (2,500 incl. extension) frozen cases   [done]
├── run_pit_decisions.py        step 2: ask each LLM for a trade on every case                 [done for 3 OpenAI models]
├── run_pit_riskagent.py        step 3: October LLM risk manager                               [done]
├── analyze_components.py       step 4: score every decision on real outcomes → analysis/scored.pkl  [done]
├── run_finfm_arms.py           NEW: feedback arm, control, risk-manager re-test              [done for 3 OpenAI models]
├── score_finfm_arms.py         NEW: prints comparison tables for the new arms
├── make_finfm_tables.py        NEW: writes every table + number used in the paper (paper_finfm/tables/)
├── make_paper_results.py, robustness_table.py, noise_floor.py, reviewer_checks.py   October paper analyses
└── run_live.py, simple_demo.py, demo.sh                                              live demo (not used in the paper)

code/logs/exp_pit_20261012/     October experiment: bundles/, decisions_<model>.jsonl, riskagent_<model>.jsonl, analysis/scored.pkl
code/logs/finfm_2027/           new experiment outputs (*.jsonl) + scores.txt
code/data/pit/                  saved prices, fundamentals, news, and the LLM cache
paper_finfm/                    the paper (LaTeX)
```

**Flow of one decision in the paper's experiment:** frozen case (`bundles/AAPL_2025-04-15.json`) → planner picks which analysts this profile consults → LLM gets the evidence + profile and proposes a trade (`decisions_<model>.jsonl`, field `U`) → risk engine verdict + reasons (`verdict`, `reasons`) → enforcement arms applied afterwards to that same `U` → `outcomes.py` scores each version → tables.

**Why "applied afterwards" matters:** every arm modifies the *same* proposal, so differences between arms are not random LLM noise.

---

## 5. Setup (everyone, before starting tasks)

```bash
# 1. get the code + data (data is committed in this private branch; ~150 MB, takes a minute)
git clone -b be-final-year-project https://github.com/norqen-ai/norqen-backend.git
cd norqen-backend/code

# 2. Python environment (Python 3.11+; Malhar used 3.13)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. sanity check — no API calls, reads saved results
.venv/bin/python score_finfm_arms.py
.venv/bin/python make_finfm_tables.py
```
If step 3 prints tables and a list of numbers, you're set up.

**API keys** (only Omkar needs one, for the open-weight model): create `code/.env` with
```
GROQ_API_KEY=...
```
`.env` is git-ignored. **Never commit it, never paste keys in WhatsApp or GitHub.** Re-running an LLM step that was already run costs nothing (answers come from `data/pit/llm_cache.sqlite`), but the script still needs that provider's key set to start. The scoring and table scripts need no key at all.

⚠️ The data in this branch (news headlines, prices) is for our private use only. This branch must never be made public.

---

## 6. Omkar — tasks

**A. Open-weight model run (18 Nov) — most valuable extra.** Reviewers will say "only OpenAI models". Model: Llama-3.3-70B on Groq (training cutoff Dec 2023 → every 2025–26 date is clean; the client already supports it as `llama-3.3-70b`).
```bash
cd code
# 1. Groq key in .env (see Setup). Check Groq's rate limits / pricing for llama-3.3-70b-versatile first.
# 2. smoke test (20 cases)
.venv/bin/python run_pit_decisions.py --models llama-3.3-70b --styles nl --since 2025-01-15 --limit 20 --workers 4
# 3. full run: 1,900 cases × 4 profiles × 2 styles = 15,200 calls. Lower --workers if you hit rate limits.
.venv/bin/python run_pit_decisions.py --models llama-3.3-70b --styles nl,explicit --since 2025-01-15 --workers 8
# 4. the new feedback test + control on Llama
.venv/bin/python run_finfm_arms.py --arm revise --models llama-3.3-70b --only-conf --sample 0
.venv/bin/python run_finfm_arms.py --arm revise --models llama-3.3-70b --only-conf --hide-conf --sample 0
# 5. rescore and regenerate the paper tables (Llama rows appear automatically)
.venv/bin/python analyze_components.py
.venv/bin/python make_finfm_tables.py
# 6. commit ONLY the new result files + tables
git add logs/exp_pit_20261012/decisions_llama-3.3-70b.jsonl logs/finfm_2027/ logs/exp_pit_20261012/analysis/ ../paper_finfm/tables/
git commit -m "Llama-3.3-70B run for FinFM" && git push
```
- Step 3 writes `decisions_llama-3.3-70b.jsonl`. **Don't touch the three OpenAI decision files.**
- If the run crashes midway, just re-run the same command: finished calls come from the cache.
- **If it can't finish by 19 Nov night, drop it** and tell Malhar; the paper says "one provider" in limitations. Don't swap in Gemini unless its training cutoff is before Jan 2025.

**B. Write the Setup section (19 Nov)** in Overleaf, ≈ 0.8 column. Four paragraphs already outlined in `main.tex`:
- *System*: Section 3.1 above in 4 sentences; the profile table can go to the appendix.
- *Data and models*: 100 stocks, 19 dates, point-in-time rules (news published before the next open; fundamentals ≥ 90 days after fiscal year end), 3 models + cutoffs (+ Llama if run).
- *Enforcement arms*: the 4 arms + the control, one sentence each (already drafted; check against `run_finfm_arms.py`).
- *Outcomes*: entry next open, horizons 1/5/20/40 days, stops on daily high/low, costs 14/36 bp, P&L in bp of equity, bootstrap over decision months.
- Facts to copy from: `PREREGISTRATION.md`, `code/src/pit/outcomes.py` docstring, the October paper PDF (Malhar shares it).
- Put the architecture figure (`06_Assessment_Oct2026/figures/fig_block_diagram.png` or the October Figure 1) in the **appendix**, not the main 4 pages.

**C. Write Limitations (19 Nov)** — bullet list is in the TODO box in `main.tex`: weak signal (no return claims), 19 months, small models / one provider, one evidence model, decisions scored one at a time from an empty portfolio, survivorship (today's large caps), daily-bar fills, pre-registration is a dated file not a public registry.

**D. Check (20 Nov):** every sentence in Setup matches what the code does.

---

## 7. Piyush — tasks

**A. Overleaf (18 Nov morning).**
- New Project → Upload Project → `paper_finfm_overleaf.zip` (or upload the files in `paper_finfm/`).
- Menu → Settings → **Compiler: pdfLaTeX** (the AAAI style refuses XeLaTeX/LuaLaTeX). Compile once; you should see a 3-page draft with red TODO boxes.
- Share → add Omkar and Malhar as editors.
- From now on the paper is edited **only in Overleaf**. When `make_finfm_tables.py` is re-run, re-upload the files in `paper_finfm/tables/` (overwrite).

**B. Verify every reference (18 Nov).** Open `refs.bib`. For each entry: open the paper, check title, authors, year, venue; fix mistakes; fill the entries marked TODO (FINSABER, "Inside the Trading Loop", full author lists for Sharma et al. and Huang et al.). For every sentence in the paper that says what another paper did, check it in that paper's **method/results section**, not the abstract. Keep a small checklist (claim → page you confirmed it on) and send it to Malhar.

**C. Scoop check (18 Nov) — important.** Read these and tell Malhar the same day if any of them already shows "LLM agent raises its confidence after rule-engine feedback" or compares block/repair/LLM-reviewer on real outcomes:
- "Attribution Is a Propagation Problem in Multi-Agent Trading Systems" (ICAIF'26 AI4F workshop, ai4f.org)
- "Inside the Trading Loop" (arXiv 2611.11657)
- FinPanel (ICAIF'26 AI4F workshop)
- Google Scholar / arXiv searches: `LLM trading agent feedback risk engine`, `LLM confidence inflation feedback threshold`, `guardrail feedback LLM agent finance`, `verifier feedback self-reported confidence`.

**D. Write Related Work (19 Nov)**, ≈ 0.4 page, three short paragraphs (outline in the TODO box in `main.tex`): (1) LLM trading agents and why their returns don't survive careful testing; (2) guardrails and mandates — Section 2 table, ending with the gap sentence; (3) confidence and feedback — calibration papers, sycophancy, self-correction, reward hacking.

**E. Anonymity pass (20 Nov):** no names, no PICT, no Pune, no "Norqen", no GitHub URL, no acknowledgements, nothing like "our BE project". Overleaf PDF metadata clean. If we cite our own earlier work, write it in third person.

**F. OpenReview (20 Nov):** draft the submission form: title, abstract (copy from paper), keywords (LLM agents; trading; guardrails; investment mandates; confidence calibration; evaluation), one-line TL;DR, all authors' OpenReview profiles linked. Supplementary material = anonymised code zip (`code/` scripts + `src/` only — **no `.env`, no data, no logs**); Malhar decides whether to attach it.

---

## 8. Malhar — tasks

- [ ] 17 Nov: push code + data + paper to the branch ✅; send this file + Overleaf zip.
- [ ] 17 Nov: read the FinFM call + AAAI-27 author kit rules (page limit, anonymity, LLM-use policy, supplementary); set reviewer conflicts in OpenReview (also a FinFM reviewer).
- [ ] 20 Nov evening: Intro + Results, final numbers, cut to 4 pages.
- [ ] 21 Nov morning: final read by all three → **submit by noon IST**.

---

## 9. How to fill the paper (rules for whoever edits)

1. **Every number comes from `make_finfm_tables.py`** (as `\Macro` names from `tables/macros.tex` or the generated table files). Never type a result by hand. If you need a new number, ask Malhar to add it to the script.
2. Red `\todo{...}` boxes say what goes where and who owns it. **Delete every `\todo` before submission** (search the source for `\todo`).
3. Page budget for the main text (4 pages max): Abstract + Intro ≈ 0.9 · Related Work ≈ 0.4 · Setup ≈ 0.8 · Results ≈ 1.4 (incl. 2 tables) · Discussion + Limitations ≈ 0.5. Extra tables/figures → appendix after references.
4. AAAI style: don't change the preamble lines marked "DO NOT CHANGE"; no `\vspace` with negative values, no `\newpage`, no font changes, no hyperref.
5. Write simply. Short sentences. One claim per sentence.
6. Words to avoid: profitable, outperforms, alpha, beats the market, novel framework, state-of-the-art.
7. Repair's 0% violations is **automatic** — always say so.
8. Say "we found no prior work that…", never "nobody has ever…".

---

## 10. Timeline (IST)

| Date | Omkar | Piyush | Malhar |
|---|---|---|---|
| 17 Nov (tonight) | Setup + OpenReview profile | Setup + OpenReview profile | Push, send files, rules check |
| 18 Nov | Llama smoke test → full run | Overleaf, verify refs, scoop check | Morning review; travel |
| 19 Nov | Llama feedback arms; write Setup + Limitations | Write Related Work | Visa appointment; review on phone |
| 20 Nov | Commit Llama results; check Setup vs code | Anonymity pass; OpenReview form | Evening: Results + Intro, 4-page cut |
| 21 Nov | Final read | Final read | Final read; **submit by 12:00** |

---

## 11. If something breaks

- `ModuleNotFoundError` → you're not using `.venv/bin/python`, or `pip install -r requirements.txt` didn't finish.
- `FileNotFoundError: logs/exp_pit_20261012/...` → run commands from inside `code/`.
- Groq `429` / rate limit → lower `--workers`, wait, re-run the same command (cache keeps finished calls).
- Overleaf "pdfTeX is required" → compiler isn't set to pdfLaTeX.
- Anything else → WhatsApp Malhar the full error text.
