"""Obedience experiment (RQ1, made falsifiable).

For each stock: gather ONE real evidence bundle, freeze it (with its risk context), then
replay the identical evidence under every investor policy in three decision modes:

  guarded            action/size/stop computed in code from the policy   (reference)
  unguarded_explicit the LLM decides, shown the policy's numeric rules
  unguarded_nl       the LLM decides, shown only a natural-language profile

Every decision is audited by the deterministic risk engine and logged RAW, so we can count
how often an LLM breaks the mandate and how often the deterministic layer has to intervene.

  python3 run_obedience.py --n-us 10 --n-nse 10
  python3 analyze_obedience.py logs/exp_obedience_<date>
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from src.core.policy import load_all_policies
from src.core.schemas import PortfolioState
from src.core.sizing import realized_ann_vol
from src.tools.registry import build_registry
from src.agents.planner_graph import PolicyPlannerGraph
from src.agents.llm import llm_available, DEFAULT_MODEL
from src.risk.engine import RiskEngine
from src.audit.log import DecisionLogger, EvidenceBundle
from src.data.providers import MARKET

PORTFOLIO = PortfolioState(equity=1_000_000, cash=1_000_000, open_positions=0, daily_pnl_pct=0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-us", type=int, default=10)
    ap.add_argument("--n-nse", type=int, default=10)
    ap.add_argument("--modes", default="guarded,unguarded_explicit,unguarded_nl")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if not llm_available():
        raise SystemExit("OPENAI_API_KEY not set — unguarded modes need the LLM.")
    out = Path(args.out or f"logs/exp_obedience_{time.strftime('%Y%m%d')}")
    (out / "bundles").mkdir(parents=True, exist_ok=True)
    modes = [m.strip() for m in args.modes.split(",")]
    uni = json.load(open("config/universe.json"))
    tickers = uni["US"][:args.n_us] + uni["NSE"][:args.n_nse]
    policies = load_all_policies("config/policies")
    tools = build_registry()
    logger = DecisionLogger(out)
    meta = {"model": DEFAULT_MODEL, "modes": modes, "tickers": tickers,
            "policies": list(policies), "started": time.strftime("%Y-%m-%d %H:%M:%S")}
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"obedience run -> {out}  | model={DEFAULT_MODEL} | {len(tickers)} stocks x "
          f"{len(policies)} policies x {len(modes)} modes")

    done = 0
    for i, t in enumerate(tickers, 1):
        t0 = time.time()
        try:
            closes = MARKET.get_ohlcv(t, period="3mo")["Close"].values
            ctx = {"ann_vol": realized_ann_vol(closes)}
            evidence = [tools[name](t) for name in tools]          # one real bundle per stock
            bundle = EvidenceBundle(t, evidence, context=ctx)
            bundle.save(out / "bundles")
            frozen = bundle.as_tools()
            for mode in modes:
                for pname, pol in policies.items():
                    card = PolicyPlannerGraph(pol, frozen, market_ctx=ctx, decision_mode=mode).decide(t)
                    RiskEngine(pol).check(card, PORTFOLIO)          # deterministic audit, logged raw
                    logger.log(card)
                    done += 1
            print(f"[{i:>2}/{len(tickers)}] {t:<14} ok  ({time.time() - t0:.0f}s)", flush=True)
        except Exception as e:
            print(f"[{i:>2}/{len(tickers)}] {t:<14} FAILED: {repr(e)[:90]}", flush=True)

    meta["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    meta["decisions_logged"] = done
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"done: {done} decisions logged to {logger.path}")


if __name__ == "__main__":
    main()
