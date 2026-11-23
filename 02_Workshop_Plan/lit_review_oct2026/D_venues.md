# D: Venue fact-check for the ICAIF'26 AI4F submit/no-submit decision

Verified **Sun 4 Oct 2026**. Sources were the official pages, fetched as raw HTML or through the OpenReview API, with quotes copied from those pages. Times are converted to IST (UTC+5:30). AoE means UTC−12.
"Could not verify" means the page would not load or did not state the fact.

---

## TL;DR (read this first)

| Item | Verified fact |
|---|---|
| **AI4F deadline** | **7 Oct 2026, 23:59 AoE = Thu 8 Oct 2026, 17:29 IST** (≈3.5 days from now) |
| Submission site | **OpenReview**: `openreview.net/group?id=ACM.org/ICAIF/2026/Workshop/AI4F` |
| Archival? | **Non-archival, no proceedings, no DOI.** Only names and titles go on the website. |
| Format | No length limit and no strict format. ACM `sigconf` is recommended but not required. PDF only. |
| Review | **Single-blind**, no rebuttal |
| Notification | 14 Oct 2026 AoE = Thu 15 Oct, 17:29 IST |
| Author registration due | **18 Oct 2026 AoE = Mon 19 Oct, 17:29 IST**. That is **4 days after notification**, and the fee is non-refundable. |
| In person? | **Effectively yes.** ICAIF's CFP says workshop papers are expected to be presented in person and pre-recorded videos are not accepted. |
| Cost (registration only) | Somewhere between **€207** and **€647** including VAT. The registration page is ambiguous about which ticket type covers a workshop paper (see §1.6). Flights, a Schengen visa and a stay in Milan come on top. |
| LLM-writing policy | **Neither the workshop nor ICAIF states one.** ACM's general authorship policy says to disclose AI use. |

**Decision-relevant risks the team may not have priced in:**
1. **The in-person requirement and the Schengen visa timeline.** Notification is 15 Oct IST and the workshop is in Milan on 14 Nov, which leaves about 30 days. ICAIF asks you to *pay registration first* to get a visa support letter, and the fee is refunded only if the visa is *denied*.
2. **Registration-type ambiguity.** If the "Passport or Main Conference" rule applies to workshop papers, the cheapest valid ticket is €427 including VAT, and the student rate does not qualify.
3. **The ICAIF umbrella page shows a later date (12 Oct).** AI4F's own site and OpenReview both enforce 7 Oct AoE. Plan for 7 Oct.

---

## 1. ICAIF 2026: The 3rd Workshop on LLMs & Generative AI for Finance (AI4F)

### 1.1 Deadline
- **ai4f.org (Key Dates):** "Submission Deadline … October 7, 2026 (Anywhere on Earth)". Submissions opened 23 Aug 2026.
- **OpenReview venue header, read through the API:** "Submission Deadline: Oct 08 2026 11:59AM UTC-0". This is the same instant as 7 Oct 23:59 AoE.
- **In IST: Thursday 8 Oct 2026, 17:29 IST.**
  - The OpenReview invitation `duedate` is 1791460740000 ms, which is 17:29 IST.
  - Its `expdate` is 17:59 IST. That is a 30-minute hard-close buffer in the system. **Do not plan around it.**
- **Conflicting umbrella date.** icaif2026.org/workshop/ (the generic "Workshop paper dates") says: "Paper submission October 1, 2026 Extended to October 12, 2026" and "Paper notification … Extended to October 16, 2026". AI4F's own site and its OpenReview invitation still say **7 Oct AoE**. Treat 7 Oct as binding. If you want slack, email contact@ai4f.org and ask whether the umbrella extension applies. Do not assume it does.

### 1.2 Submission site and form fields
- **OpenReview.** ai4f.org links to `https://openreview.net/group?id=ACM.org/ICAIF/2026/Workshop/AI4F`, and icaif2026.org/workshop/ lists it as "OpenReview venue".
- Form fields, from the API: title (≤250 chars), authors/authorids, keywords, **abstract (maxLength 5000)**, TL;DR (≤250 chars, optional), PDF (max 50 MB).
  - The form has **no LLM-use checkbox** and no reproducibility checklist.
  - Co-authors without a profile can be added by name plus email. The form says: "you can add the author by completing name as well as author email address".
- **Practical risk:** OpenReview docs say "It can take up to 2 weeks for profiles using public email services to be activated." The *submitting* author needs an active profile today. Use the one that was already used for EMNLP/UniReps.
- Rule on ai4f.org: "at least one author must agree to serve as a reviewer and deliver reviews on time." Also, "The author list cannot be modified after the initial submission".

### 1.3 Format
- ai4f.org says "There is no length limit or strict format requirement." It adds that "Formatting according to ACM guidelines is recommended". It links the ACM LaTeX `sigconf` template and the Word template. Submissions must be PDF.

### 1.4 Anonymity
- ai4f.org: "Single-blind (authors known to reviewers, reviewers anonymous). No rebuttal period."
- So **names go on the PDF**, and the artifact/GitHub link can be public.

### 1.5 Archival status
- ai4f.org: "The workshop is non-archival and will not have official proceedings."
- Also: "Non-archival: only author names and titles of accepted papers appear on the website."
- Consequence: the same work **can** go later to ICAIF-27 main. The ICAIF'26 CFP allows papers that "may have appeared previously as technical reports or in other non-archival venues".

### 1.6 Notification, registration, cost
- **Notification:** "October 14, 2026 (Anywhere on Earth)", which is Thu 15 Oct, 17:29 IST.
- **Workshop day:** 14 Nov 2026 (Sat), Main Hall, Bocconi University, Milan.
- **Registration is required.** ai4f.org says ticket registration is "managed on the main ICAIF conference site". Attendees select the AI4F workshop when registering.
- **Author deadline (icaif2026.org/registration.html):** each accepted main-conference or workshop paper needs its "author registration completed by October 18, 2026, 23:59 AoE". That is **Mon 19 Oct, 17:29 IST**.
- **Ambiguity: which ticket covers a workshop paper.** The same page says two different things:
  - "Each accepted main conference paper must be covered by at least one in-person registration". This line refers to main-conference papers only.
  - Lower down: "Each accepted paper must be associated with one in-person Passport or Main Conference registration". This line is unqualified.
  - **Email contact@ai4f.org or katieduke@linqalpha.com and ask whether a student "Workshop Days" ticket covers an AI4F poster.**
- **Fees.** These are EUR excluding 22% VAT. The page says VAT applies when the invoice goes to "an individual acting as a private person, whether Italian, EU, or non-EU". Early bird runs until 25 Oct.

| Ticket (early bird) | ex-VAT | incl. 22% VAT |
|---|---|---|
| Student, Workshop Days (14–15 Nov) | €170 | **€207.40**. Valid only if a workshop ticket covers the paper. |
| Main Conference, ACM member / non-member | €350 / €400 | **€427 / €488** |
| Passport (4 days), ACM member / non-member | €480 / €530 | €585.60 / €646.60 |
| Virtual (4 days) | €100 | Does **not** satisfy the in-person requirement |

- **Refunds:** "registration fees are generally non-refundable". The "only exception applies to participants whose visa applications are denied", and that refund is minus a processing fee.
- **Visa:** "If you require a visa support letter, please complete your registration first." So you pay before you can apply for the visa.
- **Travel support:** the QRT Student Travel Awards / ICAIF Travel Grant (Google Form) are open to undergrads. "A closing date has not yet been published." The award amount and coverage are not stated.

### 1.7 In-person presentation
- **ICAIF'26 CFP (In-person Presentation Policy):** "accepted papers in the main track and workshops are expected to be presented in person". Also: "No pre-recorded videos will be accepted."
- **ai4f.org:** "on-site participation is strongly preferred for all sessions". Accepted posters: "presenters print and bring their own posters".
- Precedent:
  - The 2025 AI4F page said "At least one author of each accepted paper is required to attend the conference to present their work."
  - The 2024 list tagged a few papers "(In-person constrained)". The page does not explain the tag.
- **Bottom line: assume one author must physically be in Milan on 14 Nov.**

### 1.8 LLM-assisted writing policy
- **ai4f.org:** none stated. I read the full page text.
- **ICAIF'26 CFP:** none stated. I read the full page text.
- **Parent default:** ACM's authorship policy FAQ says generative-AI use is permitted but must be disclosed, for example in the Acknowledgements. *Caveat:* acm.org returned HTTP 403 to direct fetch, so this comes from an acm.org search snippet (acm.org/publications/policies/frequently-asked-questions). It applies formally to ACM publications, and AI4F is not one.
- Recommendation: add a one-line AI-use disclosure in Acknowledgements anyway. It costs nothing.

### 1.9 Calibration: accepted papers closest to our topic

The accepted lists come from ai4f.org/2025-workshop and ai4f.org/2024-workshop. Matches below are on **titles only**; I did not read the papers.

| Year | Title | Authors | Slot |
|---|---|---|---|
| 2025 | Investor Risk Profiles of Large Language Models | Cho, Bae, Kim | Poster |
| 2025 | When Hallucination Costs Millions: Benchmarking AI Agents in High-Stakes Adversarial Financial Markets | Dai, Peng, Cheng, Li | Poster |
| 2025 | LLM Output Drift: Cross-Provider Validation & Mitigation for Financial Workflows | Khatchadourian, Franco | **Oral** |
| 2024 | What Does ChatGPT Make of Historical Stock Returns? Extrapolation and Miscalibration in LLM Stock Return Forecasts | Chen, Green, Gulen, Zhou | Poster |
| 2024 | AlphaAgents: LLM based Multi-Agents to Build Better Equity Portfolios | Zhao, …, Pasquali, Mehta (BlackRock) | **Oral** |

Also adjacent:
- 2025: "Financial Agents With Zero-Shot Adaptive Memory" (oral, BlackRock)
- 2025: "Constructing a Portfolio Optimization Benchmark Framework for Evaluating LLMs" (poster)
- 2025: "Risk, Ambiguity, and Infinity: Behavioral Signatures of Modern LLMs" (poster)
- 2024: "Using Large Language Models for Financial Advice" (poster)

**What the lists tell you about the bar:**
- 2025: **10 oral + 23 poster = 33** accepted titles.
- 2024: about 49 titles listed, with 6 under the "Oral Presentation" header.
- **Submission counts are not published, so the acceptance rate is unknown.**
- Many accepted papers are finance/accounting-econ empirical work rather than ML-methods papers.
- Orals skew toward industry labs (BlackRock, etc.).
- An eval/benchmark paper with clean measurement design is squarely in scope. The 2026 topics list "Workflow-level benchmarks" and "Evaluation, Verification, and Red Teaming".

---

## 2. Does a non-archival workshop paper count as "published"?

This section gives only the general distinction, with no speculation about the university.

- **Archival venue.** The paper appears in official proceedings, such as ACM DL, IEEE Xplore, Springer LNNS/SIST, the ACL Anthology or CEUR-WS.
  - These usually carry a persistent identifier (typically a DOI) or an ISSN'd volume, plus a citable bibliographic record.
  - The publication counts as "published", and other archival venues treat it as prior publication. ICAIF main rejects papers "already published in … archival publication".
- **Non-archival venue (AI4F).** The paper is peer-reviewed and presented, but the venue publishes nothing except the title and author names.
  - There are no proceedings, no DOI from the venue, and no paper hosted by the venue. AI4F's own words are quoted in §1.5.
  - What you *would* get is an **OpenReview acceptance email** and, after registering, an **ICAIF registration fee receipt**.
  - You would **not** get a published paper record from the venue.
  - Posting to arXiv gives a public preprint, with an arXiv DOI, but that is not peer-reviewed publication.
- Whether the college accepts "acceptance mail + fee receipt" from a non-archival workshop is the college's call. Ask them, and don't assume.
- Archival options at ICAIF'26 itself, as of 4 Oct:
  - **RAIOps4Fin** offers *optional* CEUR proceedings: "Accepted papers of at least 5 pages may be considered for inclusion in the CEUR Workshop Proceedings". The deadline is 12 Oct and review is double-blind (see §3).
  - Everything else is in the Scopus table in §4.

---

## 3. Backup venues (Oct 2026 – Feb 2027)

### 3a. Sibling ICAIF'26 workshops: same Milan trip, deadline 12 Oct AoE (Tue 13 Oct, 17:29 IST)

| Workshop | Deadline (official page) | Site | Format / review | Archival | Fit |
|---|---|---|---|---|---|
| **RL4LLM-Agents** (rl-for-llm-agents.github.io) | "October 12, 2026", extended | CMT, ICAIF2026 track | Full ≤8pp+2 refs; short ≥4pp; **single-blind** | "non-archival" | Fit is medium. Our agents aren't RL-trained, but harness-side and "benchmarks needed to evaluate" are in scope. **"must not be under review elsewhere"**, so it **cannot overlap with an AI4F submission**: AI4F notifies on 14 Oct and this deadline is 12 Oct. |
| **IAFM'26** (iafm-icaif.netlify.app) | "October 12, 2026 (AoE)" | CMT | **Double-blind**, ≤8pp total incl. refs/appendix | Not stated on the page (could not verify) | Medium. Covers safety and evaluation of financial LLM agents. |
| **RAIOps4Fin** (raiops4fin2026.github.io/ICAIF) | "October 12, 2026" | CMT | **Double-blind**, ≤6pp excl. refs; all accepted papers get an oral slot | **Optional CEUR proceedings** for papers ≥5pp | Medium-high. Topics include "Model Risk & Compliance" and governance of agentic systems; mandate obedience reads as compliance. |
| Financial AI Security/Privacy/Safety (vercel site) | "October 08, 2026" | OpenReview | ≤4pp, double-blind | "non-archival and has no official proceedings" | Low-medium |

### 3b. AAAI-27 workshops (Montréal; workshops 22–23 Feb 2027)
- **The workshop list is not yet announced.** The aaai.org/conference/aaai/aaai-27/workshops-call/ page says the list "will be posted by October 16, 2026".
- **AAAI's default deadline:** "Friday, November 20, 2026: Workshop Submissions Due to Organizers", which is Sat 21 Nov, 17:29 IST. Notifications are due 2 Dec 2026. Individual workshops may set their own dates.
- **Archival:** AAAI "does not post workshop papers in its digital library", so these are non-archival by default.
- **Finance-specific AAAI-27 workshops:** none announced yet.
  - Precedent: AAAI-26 had "Agentic AI in Financial Services" (ai-4-finance.pages.dev). Its deadline was "22 Oct 2025 (AoE)", and papers were "archived on OpenReview for public access (without proceedings)". **Its 2027 edition is not yet announced.**
  - One *proposed* AAAI-27 workshop is "LLM Agents Under Threat in Cyberspace" (llm-agents-under-threat.github.io; tentative 20 Nov deadline). It is security-focused, not finance.

### 3c. ICLR 2027 workshops on financial AI
- **Not yet announced.** iclr.cc/Conferences/2027/CallForWorkshops gives the schedule:
  - "Workshop Application Deadline: 9 October 2026"
  - Acceptance notification 29 Nov 2026
  - "Suggested Submission Deadline for Workshop Contributions: 1 Feb 2027"
  - Mandatory paper notification 26 Feb 2027
  - The page lists the workshops in San Francisco but prints the year as 2026, which looks like a typo.
- Precedent: the **ICLR 2026 FinAI workshop**, "Advances in Financial AI: Towards Agentic and Responsible Systems" (OpenReview `ICLR.cc/2026/Workshop/AFA`).
  - Deadline: "February 5th, 2026 (23:59 GMT)"
  - "Submissions are non-archival"
  - Double-blind
  - Long papers ≤8pp, short ≤4pp
  - In-person attendance required
  - Policy: AI assistance is allowed, but AI cannot be an author
  - **Whether it returns at ICLR 2027 is unknown until about 29 Nov 2026.**

### 3d. FinNLP-type workshops
- **FinNLP 2026 @ EMNLP 2026** (sigfintech.github.io/finnlp2026) is **closed**. The page says "Direct submission deadline: Aug 11, 2026 (AoE)", and the workshop is on 28 Oct 2026 in Budapest.
- **No FinNLP-family workshop with a deadline in Oct 2026 – Feb 2027 is announced.** FinNLP 2027 and FinNLP-AgentScen 2027 are not yet announced.

### 3e. ACM ICAIF 2027 main track
- **Not yet announced.**
- Precedent: the ICAIF'26 deadline was "August 2, 2026 Extended to August 9, 2026" (icaif2026.org/call-for-papers). That precedent puts ICAIF-27 well outside the Oct–Feb window.
- Rules carried over from ICAIF'26: archival, double-blind, ≤8pp sigconf including references, no appendices.

---

## 4. College-circulated Scopus conferences: deadlines checked on each site

"Open" means open as of 4 Oct 2026. On fit: all of these are generic soft-computing/AI proceedings, and none is finance-specific.

| Conference | Official deadline (quoted) | Status | Publisher | Fit for AI/finance paper |
|---|---|---|---|---|
| CEEE 2026 (IEEE; Gwalior/Trinity) | "Last date of Full paper submission: August 14, 2026" | **Closed** | IEEE Xplore (planned) | n/a |
| ICSISCET 2026 (MITS Gwalior) | "Last date of Paper Submission: August 21, 2026" | **Closed** | Springer LNNS | n/a |
| ITI 2026 (NIT Agartala) | "Last Date of Submission: September 04, 2026" | **Closed** | Springer LNNS | n/a |
| SCIS 2026 (SCRS) | "Last date for submission: September 25, 2026" | **Closed** | Springer LNNS | n/a |
| CSCT 2026 (NIT Sikkim) | "Last date of Paper Submission: October 03, 2026" | **Closed yesterday** (no extension posted) | Springer SIST | n/a |
| **ICCI 2026** (SVNIT Surat + ABV-IIITM; 28–29 Dec) | "Last date of Full paper submission: October 18, 2026" | **Open** | Springer LNNS | Plausible. The CFP lists AI, multi-agent systems and RL. Hybrid; ₹10,000 regular author fee. |
| **WCSC 2027** (Walailak U., Bangkok; 8–9 Jan) | "Last date of paper submission October 28, 2026" | **Open** | Springer LNNS ("Approval Pending") | Plausible: "Artificial Intelligence and Machine Learning" track; ₹10,000 fee |
| **ICCCT 2027** (NFSU Goa; 30–31 Jan) | "Submission: November 21, 2026" | **Open** | Springer LNNS ("Approval Pending") | Weak-plausible (ML tracks); hybrid; ₹9,000 + 18% GST |
| WCAIAA 2027 | Not listed among scrs.in 2027 conferences; `scrs.in/conference/wcaiaa2027` returns 404 | **Could not verify / not announced** | — | — |
| **SoCTA 2026** (SVNIT Surat; 4–5 Dec) | "extended to October 15, 2026 (FIRM DATE)" | **Open** | Springer LNNS ("To be Approved") | Plausible (generic soft computing); hybrid |
| **ESIC-2027** (icesic.com; UCSI Univ., Malaysia, 14–16 May 2027) | "Paper Submission Deadline 15 January 2027" | **Open** | IEEE Xplore (planned); 6-page IEEE limit | Plausible; hybrid. *Note:* a different "ICESICSC-2027" at KIIT (esicconference.com) has an "October 30, 2026" deadline ("All deadlines are in IST"). Confirm which one the college meant. |
| **ACDSA 2027** (Rio de Janeiro; 2–4 Feb 2027; organizer ECER Events, Doha) | "deadline has been extended to 12 October" (deadlines page: "12 October 2026") | **Open** | IEEE Xplore (planned) | Plausible (AI/data science); hybrid |
| IMPACT-2027 (GBPUAT Pantnagar; 29–30 Jan 2027) | Home page: "30th September, 2026". Important Dates page: "31st October, 2026" | **Conflicting.** Possibly open until 31 Oct. | Wiley (Scopus) **or** DMPedia series, at the TPC's choice | Weak (multidisciplinary) |

**Caveat on §4:** these are archival proceedings. Publishing the benchmark paper in one of them makes it "already published" for ICAIF-27 main and other archival venues. If the college requirement has to be met this way, use a **separate survey paper** for these venues and keep the benchmark paper for AI4F/ICLR-FinAI/ICAIF-27.

---

## Sources

All fetched on 4 Oct 2026.
- ai4f.org (2026 page, raw HTML); ai4f.org/2025-workshop; ai4f.org/2024-workshop
- OpenReview API: `api2.openreview.net/groups?id=ACM.org/ICAIF/2026/Workshop/AI4F` and `/invitations?id=…/-/Submission`; also `ICLR.cc/2026/Workshop/AFA`
- icaif2026.org/registration.html · /call-for-papers/ · /workshop/ · /qrt-student-travel-awards/
- rl-for-llm-agents.github.io · iafm-icaif.netlify.app · raiops4fin2026.github.io/ICAIF/ · icaif-2026-workshop-financial-ai-security-safety-privacy.vercel.app
- aaai.org/conference/aaai/aaai-27/ and /workshops-call/ (read via WebFetch; direct curl got 403) · ai-4-finance.pages.dev · llm-agents-under-threat.github.io
- iclr.cc/Conferences/2027/CallForWorkshops · sites.google.com/view/iclr2026finai/call-for-papers
- sigfintech.github.io/finnlp2026/
- docs.openreview.net (profile moderation)
- acm.org FAQ: direct fetch got 403, so this came from a search snippet
- scrs.in/conferences and scrs.in/conference/{ceee2026, icsiscet2026, iti2026, scis2026, csct2026, icci2026, wcsc2027, iccct2027} plus their fee pages · socta.in · icesic.com/important-dates · esicconference.com/important-dates · acdsa.org/deadlines · icmpact.com and icmpact.com/date/
