"""Real, live end-to-end decisions on REAL market data — replaces run_demo.py.

  python3 run_live.py --ticker RELIANCE.NS --policy conservative
  python3 run_live.py --ticker AAPL --compare      # the money-shot + RQ1 instrument

Runs with NO API key (deterministic tools on real yfinance data). Put your
OPENAI_API_KEY or GEMINI_API_KEY (+ LLM_PROVIDER) in .env to activate the LLM specialist agents.

--compare is the research money-shot: it gathers ONE real evidence bundle, freezes
it, then replays ALL FOUR policies on that identical evidence. Same facts, different
mandate -> different, policy-compliant decisions. This frozen bundle is exactly the
artifact RQ1 scores and the future public benchmark.
"""
from __future__ import annotations

import argparse

from src.core.policy import load_policy, load_all_policies
from src.core.schemas import PortfolioState
from src.tools.registry import build_registry
from src.agents.planner_graph import PolicyPlannerGraph
from src.risk.engine import RiskEngine
from src.audit.log import DecisionLogger, EvidenceBundle
from src.agents.llm import llm_available, llm_provider
from src.core.sizing import realized_ann_vol
from src.data.providers import MARKET

POLICIES_DIR = "config/policies"
PORTFOLIO = PortfolioState(equity=1_000_000, cash=1_000_000, open_positions=0, daily_pnl_pct=0.0)


def market_context(ticker: str) -> dict:
    """Freeze the risk context (annualised vol) so all policies size off the SAME
    number and replay stays leakage-safe."""
    try:
        closes = MARKET.get_ohlcv(ticker, period="3mo")["Close"].values
        return {"ann_vol": realized_ann_vol(closes)}
    except Exception:
        return {}


def show(card) -> None:
    print(f"\n[{card.policy_name}]  {card.action}  size={card.position_size_pct}%  "
          f"stop={card.stop_loss_pct}%  conf={card.confidence:.2f}  verdict={card.risk_verdict}")
    if card.risk_verdict == "VETOED":
        for r in card.risk_reasons:
            print(f"    VETO: {r}")
    print(f"    why: {card.reasoning}")
    for e in card.evidence:
        print(f"      - {e['kind']:<12} dir={e['direction']:+.2f} conf={e['confidence']:.2f}  {e['summary'][:78]}")


def decide_and_log(ticker, policy, tools, logger, market_ctx=None):
    planner = PolicyPlannerGraph(policy, tools, market_ctx=market_ctx)
    card = planner.decide(ticker)
    RiskEngine(policy).check(card, PORTFOLIO)
    logger.log(card)
    return card, planner.last_evidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="RELIANCE.NS")
    ap.add_argument("--policy", default="conservative")
    ap.add_argument("--compare", action="store_true",
                    help="freeze ONE real evidence bundle, replay all 4 policies on it")
    args = ap.parse_args()

    mode = f"LLM agents ({llm_provider()})" if llm_available() else "deterministic fallback (no API key)"
    print(f"=== LIVE decision on real market data for {args.ticker} — mode: {mode} ===")
    tools = build_registry()
    logger = DecisionLogger()

    ctx = market_context(args.ticker)
    if ctx.get("ann_vol"):
        print(f"risk context: realised annual vol = {ctx['ann_vol']:.0%}")

    if args.compare:
        # 1) gather ONE real evidence bundle (every tool, once, on live data)
        evidence = [tools[name](args.ticker) for name in tools]
        bundle = EvidenceBundle(args.ticker, evidence, context=ctx)
        path = bundle.save()
        print(f"froze real evidence bundle ({len(evidence)} items) -> {path}")
        # 2) replay ALL policies on that identical frozen evidence + frozen risk context
        frozen_tools = bundle.as_tools()
        for name, pol in load_all_policies(POLICIES_DIR).items():
            card, _ = decide_and_log(args.ticker, pol, frozen_tools, logger, market_ctx=ctx)
            show(card)
        print(f"\nSame evidence, different mandates -> different decisions. Logged to {logger.path}")
    else:
        pol = load_policy(f"{POLICIES_DIR}/{args.policy}.json")
        card, ev = decide_and_log(args.ticker, pol, tools, logger, market_ctx=ctx)
        show(card)
        if ev:
            print(f"\nevidence bundle frozen at {EvidenceBundle(args.ticker, ev).save()}")
        print(f"logged to {logger.path}")


if __name__ == "__main__":
    main()
