"""Draft BE Project Log Book (Group 02) as .docx — copy into the hard-copy log book.
Entries are only for work with evidence (files / git / notes); weeks without project
files are merged into the neighbouring row."""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Pt, Cm

TITLE = ("A Policy-Conditioned Multi-Agent LLM Framework for Auditable, "
         "Evidence-Driven Trading Decision Support")
MEMBERS = [("42205", "Malhar Inamdar"), ("42333", "Omkar Joshi"), ("42364", "Piyush Ochani")]
GUIDE = "Dr. P. S. Varade"

WEEKS = [
    ("1", "03–09 Aug 2026", [
        "Competitor and literature study: TradingAgents, FinCon, StockBench, FinPersona-Bench, CLQT, "
        "Vibe-Trading; identified that the multi-agent architecture is common and that evaluation "
        "(rule-following, confidence accuracy, evidence cost) is the open gap.",
        "Replaced the demo pipeline with real market data: provider layer (Yahoo Finance + Finnhub), "
        "company-name→ticker resolver, frozen research universe of 20 US + 20 NSE stocks.",
        "Built the LangGraph planner with four LLM agents (technical, news, fundamental, macro) and a "
        "logistic-regression predictor; added volatility-target position sizing.",
        "Built the evaluation suite: leakage-safe back-tester with transaction costs, quant metrics "
        "(IC, Sharpe, drawdown, VaR), calibration (ECE/Brier), cost–quality analysis. 9 automated tests pass.",
        "Progress Evaluation-I: presentation and live demonstration to guide."], False),
    ("2", "10–16 Aug 2026", [
        "Analysed first results on numeric baselines: simple signals show IC ≈ 0 (no predictive edge); "
        "stated confidence over-confident (ECE 0.075, reduced to 0.029 by temperature scaling); "
        "extra evidence did not improve accuracy for these signals.",
        "Froze metric definitions in PREREGISTRATION.md; wrote methodology and references document."], False),
    ("3–5", "17 Aug–06 Sep 2026", [
        "Prepared the repository for release: README, MIT licence, secrets audit (API keys excluded from "
        "version control).",
        "Published the code at github.com/malharinamdar/policy-trading-agents (17 Aug)."], False),
    ("6", "07–13 Sep 2026", [
        "Venue study for the ICAIF 2026 'LLMs & Generative AI for Finance' workshop: reviewed the accepted "
        "papers of the 2024 (49) and 2025 (33) editions to calibrate scope.",
        "Code audit: found that the rule-following metric could never fail because decisions were clamped "
        "to the policy before logging; planned an 'unguarded' mode to make the test meaningful.",
        "Wrote a one-month execution plan with weekly milestones, owners and review gates."], False),
    ("7–8", "14–27 Sep 2026", [
        "Gate-1 milestone of the plan (unguarded decision mode by 14 Sep) was not met; the work was "
        "re-scheduled and completed in the week of 28 Sep (see week 9)."], False),
    ("9", "28 Sep–04 Oct 2026", [
        "Received Paper-Publication and Project-Assessment-I notices; started paper preparation.",
        "Literature update: Policy-as-Skill, OpenPM, BiasMix-Finance, PortBench, KTD-Fin and other 2026 "
        "agentic-finance papers; built a 32-paper survey table.",
        "Implemented two 'unguarded' decision modes (LLM proposes action, position size and stop-loss, "
        "with numeric rules vs a text-only investor profile) audited by the deterministic risk engine.",
        "Ran the rule-following experiment on 40 stocks (20 US + 20 NSE) × 4 investor profiles × 3 modes "
        "(480 decisions): LLM shown numeric rules broke them in 0% of decisions; LLM shown only a text profile "
        "broke the intended limits in 64.4% (safety engine blocked 103 proposals).",
        "Refreshed baselines on 3 years of data (signal IC ≈ 0; calibration error 0.071 → 0.025 after "
        "correction); wrote the research paper in single- and double-column IEEE formats."], False),
    ("10", "05–11 Oct 2026", [
        "Paper Publication Assessment (5 Oct, A3-204): presentation of the paper, survey and results.",
        "Project Assessment-I (5–10 Oct): demonstration of the working system (live decisions on US and "
        "NSE stocks, risk-engine vetoes, audit log) and the rule-following experiment.",
        "Revised plan for Oct–Nov: historical evidence bundles (2025–26 dates) with outcome labels to "
        "measure whether the safety engine's overrides improve or worsen realised outcomes."], False),
]


def shade_yellow(par):
    for run in par.runs:
        run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def centered(doc, text, size=12, bold=False, space=4):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    p.paragraph_format.space_after = Pt(space)
    return p


doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin = s.bottom_margin = Cm(2.0)
doc.styles["Normal"].font.name = "Times New Roman"
doc.styles["Normal"].font.size = Pt(11)

# ---- cover
centered(doc, "Group No. 02", 11, True, 30)
centered(doc, "LOG BOOK ON", 14, True, 6)
centered(doc, TITLE.upper(), 15, True, 28)
for line in ["SUBMITTED TO SAVITRIBAI PHULE PUNE UNIVERSITY", "FOR PARTIAL FULFILLMENT OF THE REQUIREMENTS",
             "for the award of the DEGREE OF", "BACHELOR OF ENGINEERING", "in",
             "Electronics and Telecommunication Engineering"]:
    centered(doc, line, 11, line in ("BACHELOR OF ENGINEERING",), 2)
centered(doc, "", 11)
centered(doc, "By", 11, False, 4)
for roll, name in MEMBERS:
    centered(doc, f"{name}  ({roll})", 12, True, 2)
centered(doc, "", 11)
centered(doc, "NAME OF GUIDE", 11, True, 2)
centered(doc, GUIDE, 12, True, 24)
for line in ["Department of Electronics and Telecommunication Engineering",
             "PUNE INSTITUTE OF COMPUTER TECHNOLOGY", "PUNE – 43", "A.Y. 2026-27"]:
    centered(doc, line, 11, True, 2)
doc.add_page_break()

# ---- group details
centered(doc, "DEPT OF ELECTRONICS AND TELECOMMUNICATION ENGINEERING", 11, True, 0)
centered(doc, "SCTR'S PUNE INSTITUTE OF COMPUTER TECHNOLOGY, PUNE 43  ·  ACADEMIC YEAR 2026-27", 10, False, 10)
centered(doc, "BE PROJECT LOGBOOK", 13, True, 10)
doc.add_paragraph().add_run("Group No: 02").bold = True
p = doc.add_paragraph(); p.add_run("Project Title: ").bold = True; p.add_run(TITLE)
t = doc.add_table(rows=1, cols=4); t.style = "Table Grid"
for c, h in zip(t.rows[0].cells, ["Sr. No", "Roll No.", "Name", "Exam Seat No."]):
    c.text = h; c.paragraphs[0].runs[0].bold = True
for i, (roll, name) in enumerate(MEMBERS, 1):
    r = t.add_row().cells; r[0].text, r[1].text, r[2].text, r[3].text = str(i), roll, name, ""
doc.add_paragraph()
for k, v in [("Internal Guide Name, Signature", f"{GUIDE}  ____________________"),
             ("Company Name (If sponsored)", "Not applicable (not sponsored)"),
             ("Company Mentor Name", "Not applicable")]:
    p = doc.add_paragraph(); p.add_run(f"{k}: ").bold = True; p.add_run(v)
doc.add_page_break()

# ---- SDG form
centered(doc, "Sustainable Development Goal (SDG) Evaluation Form", 13, True, 8)
for k, v in [("Group ID", "02"), ("Project Title", TITLE), ("Project Guide", GUIDE)]:
    p = doc.add_paragraph(); p.add_run(f"{k}: ").bold = True; p.add_run(v)
sdgs = ["No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education", "Gender Equality",
        "Clean Water and Sanitation", "Affordable and Clean Energy", "Decent Work and Economic Growth",
        "Industry, Innovation and Infrastructure", "Reduced Inequalities", "Sustainable Cities and Communities",
        "Responsible Consumption and Production", "Climate Action", "Life Below Water", "Life on Land",
        "Peace, Justice and Strong Institutions", "Partnerships for the Goals"]
t = doc.add_table(rows=1, cols=3); t.style = "Table Grid"
for c, h in zip(t.rows[0].cells, ["SDG", "Primary SDG (✓)", "Secondary SDG (✓)"]):
    c.text = h; c.paragraphs[0].runs[0].bold = True
for i, name in enumerate(sdgs, 1):
    r = t.add_row().cells
    r[0].text = f"SDG {i} – {name}"
    r[1].text = "✓" if i == 8 else ""
    r[2].text = "✓" if i == 9 else ""
doc.add_paragraph()
doc.add_paragraph("Justification: SDG 8 — trustworthy, explainable decision support that protects ordinary "
                  "investors from opaque advice and excessive risk. SDG 9 — an open, reusable tool and method "
                  "for checking whether AI systems in finance follow their rules.")
doc.add_page_break()

# ---- abstract (from the submitted synopsis)
centered(doc, "Project Abstract", 13, True, 8)
doc.add_paragraph(
    "Large language model (LLM) agents are increasingly used for financial analysis and trading, but three "
    "questions remain open: does such a system actually change its behaviour when the investor's mandate "
    "changes, is the confidence it reports trustworthy, and can it judge for itself how much evidence is enough "
    "before acting? This project develops a policy-conditioned, multi-agent framework in which a planner "
    "interprets an explicit investor policy that governs how specialist agents and tools are used, how "
    "positions are sized, and when to stop gathering evidence, together with a rule-based risk engine that "
    "can veto any decision. Instead of claiming market-beating returns, the work focuses on new ways to "
    "evaluate such systems: how faithfully they follow the given policy, how reliable their confidence is, "
    "and the trade-off between decision quality and the cost of gathering evidence. The system is assessed "
    "on US and Indian equities using paper trading, with no real money at risk.")
doc.add_page_break()

# ---- weekly log
centered(doc, "Log-Book — Weekly Progress (August–October 2026)", 13, True, 6)
t = doc.add_table(rows=1, cols=4); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [Cm(1.3), Cm(2.8), Cm(9.6), Cm(3.4)]
for c, h, w in zip(t.rows[0].cells, ["Week", "Dates", "Work carried out", "Guide's remarks & sign"], widths):
    c.text = h; c.paragraphs[0].runs[0].bold = True; c.width = w
for wk, dates, items, fill in WEEKS:
    r = t.add_row().cells
    r[0].text, r[1].text = wk, dates
    r[2].text = ""
    for j, item in enumerate(items):
        par = r[2].paragraphs[0] if j == 0 else r[2].add_paragraph()
        par.add_run(("• " if len(items) > 1 else "") + item).font.size = Pt(9.5)
        if item.startswith("[FILL"):
            shade_yellow(par)
    for c, w in zip(r, widths):
        c.width = w
out = __file__.rsplit("/", 1)[0] + "/BE_Logbook_Group02.docx"
doc.save(out)
print("wrote", out)
