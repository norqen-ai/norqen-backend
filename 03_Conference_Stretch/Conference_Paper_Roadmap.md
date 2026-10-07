# Conference Paper Roadmap (ICAIF 2027) — STRETCH GOAL, NOT ACTIVE

**Do not open this work before the gate below is passed. Focus = workshop first.**

## Gate (all must be true, checked ~Mar 2027)

- [ ] ICLR FinAI 2027 workshop paper submitted
- [ ] Live paper-trading loop has run ≥4 months without major gaps
- [ ] E1 (adherence) results are clean and interesting (either direction)
- [ ] Team has bandwidth after Sem-VIII report/viva prep

## Target

**ACM ICAIF 2027** (International Conference on AI in Finance) — full 8-page paper,
deadline ~Aug 2027 (2026 edition: deadline 2 Aug 2026, conference Nov, Milan).
This is *the* conference of this subfield; realistic for a strong undergrad team.
Honest odds with everything below done well: roughly 1-in-3 to 1-in-2.

## What the workshop paper lacks for conference level (the six gaps)

1. **Measurement only, no fix.** The conference paper's heart must be REPAIR:
   - **Fix A — Verifier/checker:** a deterministic checker reads every proposed decision, rejects policy violations, returns them with the violated clause quoted; agent retries.
   - **Fix B — Hard constraints:** sizing/stops clamped in code to policy bounds (never trusted to the LLM).
   - **Fix C — Policy re-injection:** mandate re-inserted fresh at every decision instead of fading into old context (directly attacks the drift FinPersona-Bench found).
   - Compare all three + combinations: violation rate ↓ vs. decision-quality cost. Title shape: *"Measuring and Enforcing Policy Adherence in LLM Trading Agents."*
2. **One model = coincidence.** ≥3 LLM families on the full grid; findings must generalize.
3. **No proper statistics.** Error bars on everything, paired tests, multiple repeats per decision, pre-registered metrics (schema frozen Aug 2026 — already done if we followed the plan).
4. **Nothing others can use.** Release the benchmark artifact: 500+ frozen evidence bundles + 4 policy files + adherence scorer + leaderboard script. This is the single biggest acceptance lever — reviewers reward "people will build on this."
5. **No stress tests.** Paraphrased policies (same mandate, different wording), conflicting-evidence days, high-volatility days, and the longitudinal drift replication.
6. **Robustness of calibration claims.** Calibration measured per-model, per-policy, per-market (US vs NSE); show whether one calibration map transfers.

## Additional experiments beyond the workshop set

- Full fix grid: {no fix, A, B, C, A+B+C} × 4 policies × 3 models on frozen bundles + 1 month live A/B (two parallel paper accounts, fix on/off)
- Policy-paraphrase invariance test
- Cross-market transfer: does adherence/calibration differ US vs NSE?
- Ablate fix components to show which does the work

## What NOT to chase

- ICLR/ICML/NeurIPS **main tracks**: no LLM-trading systems paper has landed there; ours won't be the first. Don't spend hope or pages on it.
- Real-money trading. Never. Paper accounts only — it's a strength in review ("responsible"), not a weakness.
- Beating the market. Still not the claim, even at the conference level.
