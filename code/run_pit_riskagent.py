"""EXPLORATORY arm (not in the pre-registered A1 plan): an LLM risk-manager agent as the
guardrail, instead of the deterministic engine — the "risk team" pattern of TradingAgents.

For every text-persona (nl) proposal that trades, a separate LLM call reviews the proposal
against the investor's numeric mandate and returns a final decision (approve / modify / WAIT).
The result is scored like the other pipelines (pipeline name: 'agent') and also re-audited by
the deterministic engine, so we can report how leaky an agentic guardrail is.

  python run_pit_riskagent.py --models gpt-4o-mini,gpt-4.1-mini,gpt-5-mini --reviewer gpt-4o-mini
"""
from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.agents.llm import DecisionProposal
from src.core.policy import load_all_policies
from src.core.schemas import DecisionCard, PortfolioState
from src.pit.llm_client import structured
from src.risk.engine import RiskEngine

OUT = Path("logs/exp_pit_20261012")
POL = load_all_policies("config/policies")
PORTFOLIO = PortfolioState(equity=1_000_000, cash=1_000_000, open_positions=0, daily_pnl_pct=0.0)


def review_prompts(row: dict) -> tuple[str, str]:
    p, U = POL[row["policy"]], row["U"]
    system = ("You are the risk manager of an equity investment committee. A portfolio manager has proposed a "
              "trade for a client. Make the final decision: approve it unchanged, modify position_size_pct / "
              "stop_loss_pct / take_profit_pct, or reject it (action WAIT, all numbers 0). Keep any genuine edge, "
              "but the decision MUST respect the client's mandate: "
              f"objective '{p.objective.replace('_', ' ')}', horizon '{p.horizon.replace('_', ' ')}'; "
              f"position_size_pct <= {p.max_position_pct}; stop_loss_pct > 0 and <= {p.stop_loss_pct}; "
              f"take_profit_pct about {p.take_profit_pct}; only BUY or SELL if confidence >= {p.confidence_to_act}. "
              "Report the final action, numbers, your confidence that the direction is right, and a one-sentence rationale.")
    human = (f"Stock: {row['ticker']}. Proposed decision: {U['action']} size {U['size']}% of portfolio, "
             f"stop-loss {U['stop']}%, take-profit {U['tp']}%, stated confidence {U['conf']:.2f}. "
             f"Rationale: {U['rationale']}\nDecide.")
    return system, human


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gpt-4o-mini")
    ap.add_argument("--reviewer", default="gpt-4o-mini")
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out)
    for model in a.models.split(","):
        src = out / f"decisions_{model}.jsonl"
        rows = [json.loads(l) for l in src.open()] if src.exists() else []
        rows = [r for r in rows if r["style"] == "nl" and r["U"] and r["U"]["action"] in ("BUY", "SELL")
                and r["U"]["size"] > 0]
        dst = (out / f"riskagent_{model}.jsonl").open("w")
        t0, n = time.time(), 0

        def work(r):
            s, h = review_prompts(r)
            v = structured(a.reviewer, s, h, DecisionProposal, temperature=0.0, tag="riskagent")
            if v is None:
                return {"bundle": r["bundle"], "policy": r["policy"], "style": r["style"], "A": None}
            act = str(v["action"]).upper().strip()
            act = act if act in ("BUY", "SELL", "HOLD", "WAIT") else "WAIT"
            A = {"action": act, "size": float(v["position_size_pct"]), "stop": float(v["stop_loss_pct"]),
                 "tp": float(v["take_profit_pct"]), "conf": max(0.0, min(1.0, float(v["confidence"]))),
                 "rationale": str(v["rationale"])[:300]}
            card = DecisionCard(ticker=r["ticker"], action=A["action"], position_size_pct=A["size"],
                                stop_loss_pct=A["stop"], take_profit_pct=A["tp"], confidence=A["conf"],
                                policy_name=r["policy"], reasoning="")
            RiskEngine(POL[r["policy"]]).check(card, PORTFOLIO)
            return {"bundle": r["bundle"], "policy": r["policy"], "style": r["style"], "reviewer": a.reviewer,
                    "A": A, "A_verdict": card.risk_verdict, "A_reasons": card.risk_reasons}

        with ThreadPoolExecutor(a.workers) as ex:
            for f in as_completed([ex.submit(work, r) for r in rows]):
                dst.write(json.dumps(f.result()) + "\n")
                n += 1
                if n % 1000 == 0:
                    print(f"[{model}] {n}/{len(rows)} {time.time() - t0:.0f}s", flush=True)
        dst.close()
        print(f"[{model}] reviewed {n} proposals in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
