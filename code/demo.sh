#!/usr/bin/env bash
# One-command demo for the assessment.
#   bash demo.sh           full demo (needs internet + OpenAI key in .env)
#   bash demo.sh offline   only the parts that run on saved data (no internet)
# Press Enter to move to the next step.

cd "$(dirname "$0")" || exit 1
PY=".venv/bin/python"; [ -x "$PY" ] || PY="python3"
export PYTHONWARNINGS=ignore
SAVED="logs/exp_obedience_20261004"
MODE="${1:-full}"

B=$'\033[1m'; C=$'\033[36m'; Y=$'\033[33m'; N=$'\033[0m'
step() { echo; echo "${B}${C}==================== $1 ====================${N}"; }
say()  { echo "${Y}$1${N}"; }
pause(){ echo; read -r -p "${B}[Enter] next step >${N} " _; }

step "1. AUTOMATED TESTS"
say "Checks the core rules: profiles load, safety engine blocks oversized trades,"
say "replay is repeatable, sizing respects caps, back-tester cannot see the future."
$PY tests/test_core.py && $PY tests/test_quant_eval.py
pause

if [ "$MODE" != "offline" ]; then
  step "2. LIVE: ONE US STOCK, FOUR INVESTOR PROFILES (NVDA)"
  say "Live data is fetched once and frozen; all 4 profiles decide on the SAME evidence."
  say "Read each block: action, size, stop, confidence, safety verdict, then the evidence each agent gave."
  $PY run_live.py --ticker NVDA --compare
  pause

  step "3. LIVE: AN INDIAN STOCK (RELIANCE.NS)"
  say "Same system on NSE data (fundamentals from Yahoo Finance, news via Yahoo + Google News)."
  $PY run_live.py --ticker RELIANCE.NS --compare
  pause
fi

step "4. MAIN RESULT: 480-DECISION EXPERIMENT (saved run of 4 Oct)"
say "40 stocks x 4 profiles x 3 modes. Guarded = code decides (0% by design, reference)."
say "LLM + numeric rules = AI decides, shown the limits. LLM + text profile = AI decides, shown only a description."
$PY analyze_obedience.py "$SAVED"
pause

step "5. GRAPHS"
say "Opening: violations by profile, position size vs cap, which rule is broken."
open "$SAVED/fig_violations_by_profile.png" ../06_Assessment_Oct2026/figures/fig_size_vs_cap.png \
     "$SAVED/fig_violations_by_clause.png" 2>/dev/null || echo "(open the PNGs in $SAVED manually)"
pause

step "6. ONE BLOCKED DECISION FROM THE AUDIT LOG"
say "NVDA, conservative investor, AI shown only a text profile: it asked for 10% against a 2% cap."
$PY - "$SAVED" <<'EOF'
import json, glob, sys
for line in open(glob.glob(sys.argv[1] + "/decisions_*.jsonl")[0]):
    c = json.loads(line)
    if c["ticker"] == "NVDA" and c["policy_name"] == "conservative" and "mode:unguarded_nl" in c["policy_clauses_applied"]:
        c["evidence"] = [f"{e['tool']}: direction {e['direction']:+.2f}, confidence {e['confidence']:.2f}" for e in c["evidence"]]
        for k in ("decision_id", "ts", "schema_version"):
            c.pop(k, None)
        print(json.dumps(c, indent=2))
        break
EOF
pause

if [ "$MODE" != "offline" ]; then
  step "7. OPTIONAL: RUN THE EXPERIMENT LIVE ON 3 US STOCKS (~75 s)"
  read -r -p "Run it now? [y/N] " ans
  if [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
    OUT="logs/demo_live_$(date +%H%M%S)"
    $PY run_obedience.py --n-us 3 --n-nse 0 --out "$OUT" && $PY analyze_obedience.py "$OUT" | sed -n '/## Overall/,/## Do/p;/vetoed/p'
    say "(NSE column shows nan% because this mini-run has no NSE stocks.)"
  fi
  pause

  step "8. BASELINES ON 3 YEARS OF DATA (simple signals, NOT the AI agents)"
  say "8a. Do simple signals predict tomorrow's move? (IC near 0 = no edge)"
  $PY validate_signals.py --limit 5
  pause
  say "8b. Is the stated confidence honest? (compare 'mean conf' with 'accuracy' in each row)"
  $PY calibrate_report.py --limit 5
  pause
  say "8c. Does gathering more evidence improve accuracy?"
  $PY cost_quality_report.py --limit 4
fi

step "DONE"
