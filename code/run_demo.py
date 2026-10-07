"""End-to-end offline demo — runs with NO API keys, NO network, stdlib only.

What it shows (and what you can demo to Varade sir today):
  1. The SAME frozen evidence fed to two different investor policies
     produces two different decisions  -> cross-policy divergence (RQ1).
  2. The risk engine vetoing an oversized trade -> the safety layer works.
  3. Every decision logged + the evidence bundle saved for replay.

Run:  python3 run_demo.py
"""
import json

from src.core.policy import load_all_policies
from src.core.schemas import EvidenceItem, PortfolioState
from src.agents.planner import Planner
from src.risk.engine import RiskEngine
from src.audit.log import DecisionLogger, EvidenceBundle

TICKER = "NVDA"

# ---- synthetic evidence for one decision moment (stands in for live tools) ----
FROZEN = [
    EvidenceItem("price_predictor", "technical", TICKER,
                 "P(up)=0.74 from walk-forward model", direction=+0.48, confidence=0.48, reliability=0.70),
    EvidenceItem("technical", "technical", TICKER,
                 "breakout above 20-day range on volume", direction=+0.80, confidence=0.75, reliability=0.75),
    EvidenceItem("news", "news", TICKER,
                 "strongly bullish coverage: AI demand, new orders", direction=+0.90, confidence=0.85, reliability=0.80),
    EvidenceItem("fundamental", "fundamental", TICKER,
                 "revenue growth strong; valuation stretched", direction=+0.30, confidence=0.70, reliability=0.90),
    EvidenceItem("macro", "macro", TICKER,
                 "rates neutral; no major events this week", direction=0.00, confidence=0.60, reliability=0.85),
]

def main() -> None:
    policies = load_all_policies("config/policies")
    logger = DecisionLogger("logs")

    bundle = EvidenceBundle(TICKER, FROZEN)
    bundle_path = bundle.save("logs/bundles")
    tools = bundle.as_tools()

    portfolio = PortfolioState(equity=1_000_000, cash=400_000,
                               open_positions=3, daily_pnl_pct=-0.2)

    print(f"=== same evidence, different policies — {TICKER} ===\n")
    for name in ("conservative", "aggressive_growth"):
        policy = policies[name]
        card = Planner(policy, tools).decide(TICKER)
        card = RiskEngine(policy).check(card, portfolio)
        logger.log(card)
        print(f"[{name}]")
        print(f"  action={card.action}  size={card.position_size_pct}%  "
              f"stop={card.stop_loss_pct}%  confidence={card.confidence}")
        print(f"  verdict={card.risk_verdict}  ({'; '.join(card.risk_reasons)})")
        print(f"  used {len(card.evidence)} evidence items, cost {card.evidence_cost_spent}\n")

    # ---- veto demonstration: force an oversized trade past the planner ----
    policy = policies["conservative"]
    card = Planner(policy, tools).decide(TICKER)
    card.action = "BUY"                   # tamper: force a trade the planner declined
    card.position_size_pct = 9.0          # tamper: 9% vs conservative cap 2%
    card.stop_loss_pct = policy.stop_loss_pct
    card = RiskEngine(policy).check(card, portfolio)
    logger.log(card)
    print("=== veto demo: oversized trade under conservative policy ===")
    print(f"  verdict={card.risk_verdict}  reasons={card.risk_reasons}\n")

    print(f"evidence bundle frozen at: {bundle_path}")
    print(f"decisions logged to:       {logger.path}")
    print(f"decisions in log:          {len(logger.read_all())}")

if __name__ == "__main__":
    main()
