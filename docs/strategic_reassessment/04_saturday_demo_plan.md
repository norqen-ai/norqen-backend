# 04 · Saturday Evaluation — Demo Plan, Compliance Matrix & Q&A

**Event:** B.E. Project Progress Evaluation – I · Saturday (notice prints **09/08/2026**; the 9th is a Sunday, so confirm whether the meeting is Sat 8th or Sun 9th) · 10:30–11:30 a.m. · **Guide's cabin (Dr. P. S. Varade)**.
**Deck:** `05_Evaluation_PPT/BE_Project_Evaluation_Group02.pptx` (19 slides, speaker notes on every slide). A copy is in `~/Downloads/`.
**Expectation for this stage:** ~20% of software + a working module demo. You clear that bar today.

---

## 1. The notice's four "carry" requirements

| Required (from the notice) | Your status | Action |
|---|---|---|
| Copies of reference materials (IEEE/arXiv papers) | Have the list | **Print** TradingAgents (2412.20138), FinPersona-Bench (2606.31522), CLQT (2606.29771), StockBench (2510.02209) — the 4 you'll be asked about |
| 20% of H/W and/or S/W | ✅ working core runs + 5 tests pass | Have the laptop ready with `code/` (see demo script) |
| PPT demonstration / working module | ✅ deck + live `run_demo.py` | Rehearse once end-to-end |
| Purchased H/W (if applicable) | N/A (software project) | Nothing to bring |
| Every member present + evaluation sheet | — | All three attend; carry the **B.E. Project Guide Evaluation Sheet** (Group No. **02**) |

---

## 2. Rubric compliance matrix — every criterion is covered

25 marks, 8 sections. This deck maps to all of them.

| # | Criterion (marks) | Where in deck | Evidence type |
|---|---|---|---|
| 1.1 | Problem statement & architecture clear (4M) | S3 Intro, S4 Problem, S8–S9 Architecture | Implemented + designed |
| 1.2 | Literature survey conducted | S5 Literature Survey, S18 References | Done (40+ papers) |
| 1.3 | Research gaps / limitations identified | **S6 Existing Systems & Gap**, S16 Limitations | Done (verified competitors) |
| 1.4 | Objectives clearly defined | S4 Objectives | Done (from synopsis) |
| 2.1 | Block diagrams / flowcharts clear (3M) | S8 simple arch, S9 detailed arch | Diagrams ready |
| 2.2 | S/W design appropriate to objectives | S9 (box→RQ mapping), S10 | Designed |
| 3.1 | Methodology explained (3M) | S10 Methodology | Designed + partly built |
| 3.2 | Algorithms presented correctly | S10 (loop, veto, ML, calibration) | Designed |
| 3.3 | Solution technically feasible | S11 Evaluation & Feasibility | Argued (CPU-only, paper) |
| 4.1 | Project plan / timeline (3M) | S14 Timeline | Done |
| 4.2 | Milestones defined | S14 (6 milestones + hard gate) | Done |
| 4.3 | Completed as per schedule | S13 Progress, S14 (Aug=DONE) | On track |
| 5.1 | Implementation methodology (3M) | S12 Tools, S13 Progress | Explained |
| 5.2 | Tools & technologies identified | S12 Tech stack | Done |
| 5.3 | Successfully implemented / demonstrated | **S13 + live demo** | Verified (~20%) |
| 6.1–6.3 | Presentation skills (3M) | Whole deck (clean, professional) | Rehearse |
| 7.1–7.3 | Q&A (3M) | §4 below | Prepare |
| 8.1 | Objectives mapped to **SDGs** (3M) | **S15 SDG 8 & 9** | Done |
| 8.2 | Findings summarised | S13, S17 Conclusions | Honest |
| 8.3 | Future scope & limitations | S16 | Done |

**No criterion is unaddressed.** The only marks that depend on *you on the day* are 6 (delivery) and 7 (Q&A) — rehearse both.

---

## 3. Live demo script (2–3 minutes, the "working module")

Do this from `BE_Final_Year_Project/code/`. It needs **no internet, no API key** (stdlib only).

**Step 1 — the money-shot.** Say: *"Same evidence, two different investor policies, two different decisions."*
```bash
cd ~/Desktop/BE_Final_Year_Project/code
python3 run_demo.py
```
Expected (verified today):
```
[conservative]   action=WAIT  size=0.0%   confidence=0.72   APPROVED
[aggressive_growth] action=BUY size=6.41% confidence=0.80   APPROVED
veto demo: position 9.00% exceeds policy cap 2.00%  → VETOED
```
Point at it: *"The conservative policy waits; the aggressive one buys 6.4%. And when a trade breaks the rules, the deterministic risk engine vetoes it — that's the auditability our research measures."*

**Step 2 — the invariants.** Say: *"Five core properties are locked by tests."*
```bash
python3 tests/test_core.py
```
Expected: `5/5 ... all tests passed` (incl. `test_replay_is_deterministic`, `test_cross_policy_divergence_exists`).

**Step 3 — show the artifact.** Open `code/logs/bundles/` (a frozen evidence bundle) and `code/logs/decisions_*.jsonl` — *"Every decision is snapshotted so we can replay it under any policy. This log is simultaneously the product's audit trail and our research dataset."*

**Offline fallback (do this the night before):** screenshot Steps 1–2 outputs and paste into a one-page PDF kept on the Desktop. If the laptop misbehaves, Slide 13 already contains the verified output — present that.

**Honesty guardrail:** if asked "is the planner using an LLM yet?" → **"No — today it's a deterministic rule-based stub with the exact same interface. The LLM planner is the September milestone. What's real now is the contract layer, the veto, and replay, which is precisely the part our research needs."** Never imply the LLM agents are running.

---

## 4. Anticipated evaluator questions + strong, honest answers

**Q. This looks like a lot of existing work — what's actually new?**
A. "The *system* isn't new — we say so on Slide 6. Multi-agent committees, risk vetoes, even NSE support exist in open-source products like Vibe-Trading. Our contribution is the *evaluation*: we're the first to measure, leakage-free, whether such an agent actually *obeys* its investor's written mandate, whether its confidence is honest, and what evidence costs — on the same frozen evidence, across US and Indian markets, released as a benchmark. Products *enforce* rules; nobody *measures* obedience scientifically."

**Q. Isn't FinPersona-Bench already doing mandate adherence?** *(the sharp one)*
A. "Yes — it's the closest work and we cite it up front. But it's *longitudinal* (one mandate eroding over time) on a *synthetic* market. We're *cross-sectional* — many mandates on the *same real* evidence — with a per-clause violation taxonomy on US+NSE, and we *release* the benchmark. We also replicate their erosion finding in a real trading loop as validation."

**Q. Why multi-agent at all? Why not one prompt?**
A. "That's literally one of our experiments — baseline B2 is a single LLM agent, and an ablation removes agents one at a time. We don't assume the committee helps; we test whether it does. If it doesn't, that's a publishable finding too."

**Q. Where's the data? How do you avoid look-ahead / leakage?**
A. "Public data — yfinance/Alpaca for US, jugaad-data for NSE, FRED for macro. Leakage is controlled three ways: every item is timestamped and only pre-decision data is visible; historical replay runs only *after* each model's training cutoff; and the live paper-trading loop from October generates records that *cannot* be contaminated because they didn't exist at training time."

**Q. Financial risk? Are you trading real money?**
A. "Never. Paper trading only — Alpaca's paper API and a custom NSE simulator. That's deliberate: it's a responsibility strength in review, not a limitation, and it keeps us out of SEBI advisory territory."

**Q. Only ~4 months of live data — is that enough?**
A. "Not for returns/Sharpe — and we say so openly and report those as secondary with confidence intervals. Our *headline* adherence claim comes from frozen-evidence replay — about 18,000 scored decisions — which is statistically powered. We separated the claims precisely so the short window doesn't undermine the main result."

**Q. Can a do-nothing agent just 'WAIT' and score perfect adherence?**
A. "Great question — that's the trap we designed against. We never report adherence alone; we pair it with a *non-trivial action rate* and selective accuracy, and we include decision moments that *require* acting. A do-nothing agent visibly fails those, so it can't win."

**Q. Is this really publishable / where?**
A. "Target is the ICLR 2027 FinAI workshop — its 2026 edition (RBC, JPMorgan, NVIDIA organisers) explicitly wanted agentic *and responsible* finance work, which is exactly us. Backups are AAAI-27, FinNLP, and ACM ICAIF'27. Non-archival workshop, 4–8 pages — realistic for a strong final-year team."

**Q. How does it map to SDGs?**
A. "SDG 8 — trustworthy, auditable decision-support protects retail investors from black-box advice; SDG 9 — we release open research infrastructure (a benchmark) for responsible financial AI."

---

## 5. Needs human input before Saturday (do these)

1. **Confirm the day/date** — notice says "09/08/2026 (Saturday)" but the 9th is a Sunday. Ask the coordinator whether it's Sat 8 or Sun 9.
2. **Group Number** — deck uses **02** (from the synopsis). Confirm it's still 02 on the evaluation sheet.
3. **Project name** — the README flags a pending choice (NITI / ARTHA / keep unnamed). The deck uses the **synopsis title verbatim** (safe — matches the submitted form). Decide the short name later; don't rename before this eval.
4. **`git init`** — the code isn't under version control yet. Run the two commands in `code/README.md` tonight so "reproducibility / version control" is answerable and nothing is lost.
5. **Rehearse once** — one full run-through of deck + live demo; time it to ~12–15 min so there's room for Q&A in the hour.
6. **Print** the 4 papers in §1.
