"""Short assessment demo — one story, three parts, plain English.

  python3 simple_demo.py              live data for NVDA (needs internet + OpenAI key)
  python3 simple_demo.py RELIANCE.NS  any US or NSE ticker
  python3 simple_demo.py --offline    uses the saved NVDA snapshot from 4 Oct (no internet)

Part 1: one stock, four investors, same evidence -> different decisions, all within limits.
Part 2: the experiment: who decides the trade, and how often the investor's limit is broken.
Part 3: one decision the safety engine blocked, in plain words.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")
if "--offline" in sys.argv:          # no internet: never try to call the LLM
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["GEMINI_API_KEY"] = ""
    os.environ["GOOGLE_API_KEY"] = ""

from src.core.policy import load_all_policies
from src.core.schemas import PortfolioState
from src.agents.planner_graph import PolicyPlannerGraph
from src.risk.engine import RiskEngine
from src.audit.log import EvidenceBundle
from src.eval.adherence import check_card

# The demo never prints the one-sentence explanation, so skip that extra LLM call per
# investor. It is text only and never changes a decision.
PolicyPlannerGraph._reason = lambda self, p, ev, action, d, c, cost: f"[{p.policy_name}] -> {action}"

SAVED = "logs/exp_obedience_20261004"
PORTFOLIO = PortfolioState(equity=1_000_000, cash=1_000_000, open_positions=0, daily_pnl_pct=0.0)
ORDER = ["conservative", "long_term", "intraday", "aggressive_growth"]
INVESTOR = {"conservative": "Careful", "long_term": "Long-term", "intraday": "Day-trader",
            "aggressive_growth": "Aggressive"}
SOURCE = {"fundamental": "Company finances", "macro": "Overall market", "technical": "Price chart",
          "news": "News headlines", "price_predictor": "ML price model"}
SHORT = {"fundamental": "finances", "macro": "market", "technical": "chart", "news": "news",
         "price_predictor": "ML model"}
PAUSE = "--no-pause" not in sys.argv


def pause():
    if PAUSE:
        input("\n[Enter] next part > ")


def view(direction: float) -> str:
    return "UP" if direction > 0.15 else "DOWN" if direction < -0.15 else "UNSURE"


def part1(ticker: str, offline: bool):
    print(f"\n=== PART 1: {ticker} — one snapshot of evidence, four investors ===\n")
    if offline:
        path = glob.glob(f"{SAVED}/bundles/bundle_NVDA_*.json")[0]
        bundle = EvidenceBundle.load(path)
        print("(offline: using the saved NVDA snapshot from 4 Oct 2026)\n")
    else:
        from src.data.providers import MARKET
        from src.core.sizing import realized_ann_vol
        from src.tools.registry import build_registry
        tools = build_registry()
        closes = MARKET.get_ohlcv(ticker, period="3mo")["Close"].values
        bundle = EvidenceBundle(ticker, [tools[n](ticker) for n in tools],
                                context={"ann_vol": realized_ann_vol(closes)})
        bundle.save()

    print("What each analyst said (saved once, then shown to all four investors):")
    for e in bundle.evidence:
        print(f"  {SOURCE.get(e.tool, e.tool):<17} {view(e.direction):<7} {e.confidence:.0%} sure   {e.summary[:70]}")

    policies = load_all_policies("config/policies")
    frozen = bundle.as_tools()
    print(f"\n{'Investor':<12}{'Max allowed':>12}   {'Looked at':<26}{'Decision':<10}{'Amount':>8}   Safety check")
    for name in ORDER:
        pol = policies[name]
        card = PolicyPlannerGraph(pol, frozen, market_ctx=bundle.context).decide(bundle.ticker)
        RiskEngine(pol).check(card, PORTFOLIO)
        looked = ", ".join(SHORT.get(e["tool"], e["tool"]) for e in card.evidence)
        amount = f"{card.position_size_pct:.0f}%" if card.action in ("BUY", "SELL") else "-"
        check = "OK" if card.risk_verdict == "APPROVED" else "BLOCKED"
        print(f"{INVESTOR[name]:<12}{pol.max_position_pct:>11.0f}%   {looked:<26}{card.action:<10}{amount:>8}   {check}")
    print("\nAmount = share of the investor's money put into this stock (never above 'Max allowed').")


def part2():
    print("\n=== PART 2: the experiment (40 stocks x 4 investors, saved run of 4 Oct) ===\n")
    policies = load_all_policies("config/policies")
    cards = [json.loads(l) for f in glob.glob(f"{SAVED}/decisions_*.jsonl") for l in open(f) if l.strip()]
    label = {"guarded": "Code decides, using the investor's numbers",
             "unguarded_explicit": "AI decides, told the exact limits",
             "unguarded_nl": "AI decides, told only a description"}
    print(f"{'Who decides the trade?':<46}{'Broke the investor limit':>26}")
    for mode in ["guarded", "unguarded_explicit", "unguarded_nl"]:
        g = [c for c in cards if f"mode:{mode}" in c["policy_clauses_applied"]]
        bad = sum(any(check_card(c, policies[c["policy_name"]])[0][k] for k in ("oversize", "bad_stop", "under_confidence"))
                  for c in g)
        print(f"{label[mode]:<46}{f'{bad} of {len(g)}  ({bad / len(g):.0%})':>26}")
    blocked = sum(c["risk_verdict"] == "VETOED" for c in cards)
    careful = [c["position_size_pct"] for c in cards if c["policy_name"] == "conservative"
               and "mode:unguarded_nl" in c["policy_clauses_applied"] and c["action"] in ("BUY", "SELL")]
    print(f"\nSafety engine blocked {blocked} of those proposals.")
    print(f"Told only 'careful investor', the AI's average bet was {sum(careful) / len(careful):.1f}% of the money "
          f"(the careful investor's limit is 2%).")
    fig = "../06_Assessment_Oct2026/figures/fig_size_vs_cap.png"
    if PAUSE and os.path.exists(fig):
        subprocess.run(["open", fig], check=False)


def part3():
    print("\n=== PART 3: one decision the safety engine blocked ===\n")
    for line in open(glob.glob(f"{SAVED}/decisions_*.jsonl")[0]):
        c = json.loads(line)
        if c["ticker"] == "NVDA" and c["policy_name"] == "conservative" \
                and "mode:unguarded_nl" in c["policy_clauses_applied"]:
            print("Investor     : Careful (limit: 2% of money per stock, stop-loss at most 3%)")
            print("AI was told  : \"The investor's objective is 'protect capital' over 'weeks to months'.\"")
            print(f"AI proposed  : {c['action']} NVDA with {c['position_size_pct']:.0f}% of the money, "
                  f"stop-loss {c['stop_loss_pct']:.0f}%")
            print(f"AI's reason  : \"{c['reasoning']}\"")
            print("Safety engine: BLOCKED — " + "; ".join(c["risk_reasons"]))
            break
    print("\nTake-away: describing an investor in words is not enough; limits must be numbers,")
    print("checked by code. The AI suggests, the code decides what is allowed.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    part1(args[0] if args else "NVDA", offline)
    pause()
    part2()
    pause()
    part3()
