# Agentic Platform Plan — Omkar

**Your mission:** own the brain — the policy-conditioned planner, the LLM specialist agents,
and the adaptive evidence loop. Malhar owns ML tools + data; Piyush owns the dashboard/website.
Read `02_Workshop_Plan/ICLR_FinAI_2027_Workshop_Plan.md` §2 and §4 first (15 min).

**We are building BOTH a product and a research paper.** Every design choice must serve both:
the product needs clean decision cards and explanations; the paper needs logged, replayable,
measurable behaviour. The good news: the same logging serves both.

---

## 0. Start here (already built, working today)

`code/` already runs end-to-end with a rule-based planner stub (no LLM):

```
cd code && python3 run_demo.py     # same evidence → conservative WAITs, aggressive BUYs 6.4%
python3 tests/test_core.py         # 5 invariant tests, all passing
```

Your job is to replace the internals of `src/agents/planner.py` with a real
LangGraph + LLM implementation **without breaking its interface or the tests**.
The stub shows exactly what the planner must consume and produce.

## 1. The contracts you must not break

- **Input:** `Policy` (from `src/core/policy.py`) + a tool registry `dict[name -> callable(ticker) -> EvidenceItem]`.
- **Output:** `DecisionCard` (from `src/core/schemas.py`) — action, size, stops, confidence, reasoning, ALL evidence used, policy clauses applied, cost spent.
- **Hard rules:**
  1. Never call a tool in `policy.forbidden_evidence`. (RQ1 measures exactly this.)
  2. Stop gathering when confidence ≥ `policy.confidence_to_act` or cost ≥ `policy.evidence_budget`. (RQ3 measures exactly this.)
  3. The LLM NEVER computes numbers — sizes, stops, indicators come from policy + Malhar's tools. LLM interprets and synthesizes only.
  4. Every prompt sent to an LLM is logged verbatim (add a `prompts` field or side-log).
  5. `tests/test_core.py` must stay green after every change.

## 2. Build order (aligned with Malhar's weeks)

### Phase A — LangGraph skeleton (weeks 1–2, target ~10 Aug)
- Venv + `pip install -r requirements.txt`. **LLM provider: OpenAI (team has $10 credits).**
  Default model: the cheapest mini-tier (gpt-4o-mini class), temperature 0. $10 ≈ 1,000–2,000
  full decisions at mini pricing — plenty for development, NOT enough for the live months;
  bulk/replay experiments will move to a free local model via Ollama later (which also
  satisfies the paper's ≥3-model requirement at zero cost).
- **Key hygiene (non-negotiable):** key lives in `.env` (gitignored), loaded via env var;
  never in code, never committed, never in logs. Add a per-run spend counter from day one —
  a runaway loop can eat $10 in an afternoon.
- Rebuild the stub's loop as a LangGraph graph with nodes: `assess_gaps → select_tool → collect → validate → check_confidence → synthesize`. Keep the rule-based aggregation as fallback.
- **First LLM agent: Technical Agent.** Input: Malhar's indicator dict for a ticker. Output: STRUCTURED JSON only (pydantic schema mirroring `EvidenceItem`) — summary, direction ∈ [-1,1], confidence ∈ [0,1]. Reject/retry on malformed output.
- Definition of done: `run_demo.py` works with `--llm` flag using the real technical agent; tests green.

### Phase B — the agent team (weeks 3–4, target ~24 Aug)
- News Agent (input: headlines list from data pipeline; output: same schema; must cite which headlines drove the direction).
- Fundamental Agent (quarterly numbers → direction/confidence at the policy's horizon).
- Macro Agent (rates/CPI snapshot → market-level direction).
- LLM-based `synthesize` node: combines EvidenceItems into the DecisionCard reasoning — but action/size still computed by code from policy + aggregate confidence.
- Prompt files live in `config/prompts/` under version control; never inline strings.

### Phase C — policy conditioning for real (weeks 5–6, target ~7 Sep)
- The planner's system prompt embeds the ACTIVE POLICY verbatim, and the `select_tool`
  node must justify each tool choice against a policy clause (logged).
- **Policy re-injection:** the policy is re-inserted fresh into EVERY LLM call, never
  left to drift out of context (this is our defence against the mandate-erosion
  problem found by FinPersona-Bench — see reading list Pile 4).
- Cross-policy smoke test: run all 4 policies on 5 tickers nightly; eyeball divergence.

### Phase D — hardening for live + experiments (weeks 7–8, target ~21 Sep)
- Cost tracking per decision (tokens in/out per call → `evidence_cost_spent`).
- Retry/timeout handling; deterministic temperature (T=0 or fixed seed where supported).
- Replay mode: planner runs identically from an `EvidenceBundle` (already supported by
  `bundle.as_tools()` — verify with LLM agents; cache LLM calls keyed on (prompt, model)).
- Multi-model support: model name is a config value, never hardcoded (we must run ≥3 models for the paper).

**🚨 Mid-October gate (whole team): the live loop must be logging 24×7. Anything not ready gets cut, not delayed.**

## 3. What NOT to build (scope discipline)

- No reflection/self-improvement loop (stretch goal, post-workshop).
- No real broker integration, no real money, ever.
- No fancy memory system yet — Postgres later; JSONL logs are enough until October.
- No more than 4–5 agents. A 5th mediocre agent is worth less than 4 reliable ones.

## 4. How your work becomes the paper

- RQ1 (does the system obey the policy?) is measured FROM YOUR LOGS: forbidden-tool
  usage, sizing clause citations, cross-policy divergence on frozen bundles.
- RQ3 (evidence efficiency) is YOUR adaptive loop: we sweep `evidence_budget` and
  `confidence_to_act` and plot decision quality vs cost.
- So: if it isn't logged, it didn't happen. Log everything, structured, from day one.

## 5. Sync points

- Weekly 30-min sync: interface changes to `schemas.py` need all three of us + a version bump.
- You consume Malhar's tools as black boxes returning `EvidenceItem` — if you need a new
  field, ask, don't fork the schema.
- Piyush reads `logs/decisions_*.jsonl` — never let a schema change break his dashboard silently.
