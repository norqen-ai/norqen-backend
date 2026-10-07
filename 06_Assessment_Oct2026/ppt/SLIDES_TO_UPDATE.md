# Tomorrow's deck — 3 quick edits (≈15 min in PowerPoint)

Deck: BE_Assessment_Oct2026_Group02.pptx (your Aug deck, already on the PICT template, plain language).

1. **Slide 15 "Project Timeline"** — change the Sep row to "DONE", and edit to:
   - Sep–Oct '26: Code audit found the rule-following test could never fail; added "unguarded"
     mode where the LLM proposes trade size + stop-loss itself and the safety engine audits it.
   - Oct '26: Ran the rule-following test on 40 stocks (20 US + 20 NSE) × 4 investor profiles.
2. **Slide 9 "Full Design"** — optionally swap the image for `fig_block_diagram.png` (in this folder,
   300 dpi), and add `fig_flowchart.png` as a new slide after it.
3. **Slide 14 "First Results"** — add one line once the 40-stock run finishes:
   `cd code && .venv/bin/python analyze_obedience.py logs/exp_obedience_20261004`
   → read the "Any violation" row for "LLM + text profile" vs "LLM + numeric rules" in report.md,
   and use fig_violations_by_profile.png from that folder.
   (1-stock smoke test already showed: text-profile mode proposed 10% vs a 5% cap → vetoed.)
