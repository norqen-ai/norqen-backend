"""Replay every PIT bundle under every investor profile: one guarded CODE decision and one
unguarded LLM PROPOSAL per (decision model, prompt style), all on the identical evidence view.

  python run_pit_decisions.py --models gpt-4o-mini --styles nl,explicit
  python run_pit_decisions.py --models gpt-4.1-mini,gpt-5-mini --workers 32

Output: logs/exp_pit_20261012/decisions_<model>.jsonl (one row per bundle x profile x style).
Guardrails, outcomes and component analyses are computed afterwards (analyze_components.py),
post hoc on these exact proposals, so no comparison mixes two different LLM samples.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import src.agents.planner_graph as pg
from src.agents.llm import DecisionProposal
from src.agents.planner_graph import PolicyPlannerGraph, aggregate
from src.audit.log import EvidenceBundle
from src.core.policy import load_all_policies
from src.core.schemas import PortfolioState
from src.core.sizing import position_size_pct
from src.pit.llm_client import MODELS, available, structured
from src.risk.engine import RiskEngine

pg.llm_available = lambda: False      # guarded path: skip the cosmetic one-line LLM explanation
OUT = Path("logs/exp_pit_20261012")
PORTFOLIO = PortfolioState(equity=1_000_000, cash=1_000_000, open_positions=0, daily_pnl_pct=0.0)
POLICIES = load_all_policies("config/policies")


def code_decision(bundle: EvidenceBundle, pname: str) -> dict:
    """Guarded decision + the evidence view the policy's router consulted."""
    pol = POLICIES[pname]
    planner = PolicyPlannerGraph(pol, bundle.as_tools(), market_ctx=bundle.context, decision_mode="guarded")
    card = planner.decide(bundle.ticker)
    ev = planner.last_evidence
    d, c = aggregate(ev)
    return {"card": card, "evidence": ev,
            "C": {"action": card.action, "size": card.position_size_pct, "stop": card.stop_loss_pct,
                  "tp": card.take_profit_pct, "conf": card.confidence},
            "agg_dir": round(d, 4), "agg_conf": round(c, 4),
            "code_size_ungated": position_size_pct(pol, d, c, bundle.context.get("ann_vol")),
            "tools": [e.tool for e in ev]}


def llm_proposal(bundle, pname, ev, model, style, rerun: str = "") -> tuple[dict | None, str]:
    pol = POLICIES[pname]
    planner = PolicyPlannerGraph(pol, bundle.as_tools(), market_ctx=bundle.context,
                                 decision_mode=f"unguarded_{style}")
    system, human = planner.unguarded_prompts(bundle.ticker, ev)
    h = hashlib.sha1((system + human).encode()).hexdigest()[:12]
    r = structured(model, system, human, DecisionProposal, temperature=0.0, tag=f"pit:{style}{rerun}")
    if r is None:
        return None, h
    action = str(r["action"]).upper().strip()
    if action not in ("BUY", "SELL", "HOLD", "WAIT"):
        action = "WAIT"
    return {"action": action, "size": float(r["position_size_pct"]), "stop": float(r["stop_loss_pct"]),
            "tp": float(r["take_profit_pct"]), "conf": max(0.0, min(1.0, float(r["confidence"]))),
            "rationale": str(r["rationale"])[:400], "usage": r.get("_usage"), "model_metadata": r.get("_model")}, h


def engine_verdict(U: dict, pname: str, ticker: str, ev) -> tuple[str, list[str]]:
    from src.core.schemas import DecisionCard
    card = DecisionCard(ticker=ticker, action=U["action"], position_size_pct=U["size"], stop_loss_pct=U["stop"],
                        take_profit_pct=U["tp"], confidence=U["conf"], policy_name=pname, reasoning="",
                        evidence=[e.to_dict() for e in ev])
    RiskEngine(POLICIES[pname]).check(card, PORTFOLIO)
    return card.risk_verdict, card.risk_reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gpt-4o-mini")
    ap.add_argument("--styles", default="nl,explicit")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--limit", type=int, default=0, help="first N bundles only (smoke test)")
    ap.add_argument("--per-month-region", type=int, default=0, help="fixed seeded sample of bundles in each month x region")
    ap.add_argument("--seed", type=int, default=20261123)
    ap.add_argument("--since", default="", help="only bundles dated on/after YYYY-MM-DD (primary window: 2025-01-15)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--rerun", default="", help="tag for an independent re-run (noise floor), e.g. ':rerun1'")
    a = ap.parse_args()
    out = Path(a.out)
    paths = sorted((OUT / "bundles").glob("*.json"))
    out.mkdir(parents=True, exist_ok=True)
    if a.since:   # bundle files are named <TICKER>_<YYYY-MM-DD>.json
        paths = [p for p in paths if p.stem.rsplit("_", 1)[1] >= a.since]
    if a.per_month_region:
        from src.pit.universe import region
        strata = {}
        for path in paths:
            ticker, date = path.stem.rsplit("_", 1)
            strata.setdefault((date[:7], region(ticker)), []).append(path)
        rng = random.Random(a.seed)
        paths = sorted(p for group in strata.values() for p in rng.sample(group, min(a.per_month_region, len(group))))
    if a.limit:
        paths = paths[:a.limit]
    bundles = {}
    for p in paths:
        raw = json.loads(p.read_text())
        from src.core.schemas import EvidenceItem
        bundles[p.stem] = EvidenceBundle(raw["ticker"], [EvidenceItem(**e) for e in raw["evidence"]],
                                         raw["ts"], raw["context"])
    t0 = time.time()
    codes = {(bid, pn): code_decision(b, pn) for bid, b in bundles.items() for pn in POLICIES}
    print(f"{len(bundles)} bundles; {len(codes)} code decisions in {time.time() - t0:.0f}s", flush=True)

    for model in a.models.split(","):
        if not available(model):
            print(f"skip {model}: no API key for provider {MODELS[model]['provider']}")
            continue
        styles = a.styles.split(",")
        jobs = [(bid, pn, s) for (bid, pn) in codes for s in styles]
        path = out / (f"decisions_{model}.jsonl" if not a.rerun else f"rerun_{model}{a.rerun.replace(':', '_')}.jsonl")
        lock = threading.Lock()
        fh = path.open("w")
        n, fails, t1 = 0, 0, time.time()

        def work(job):
            bid, pn, style = job
            b, cd = bundles[bid], codes[(bid, pn)]
            U, h = llm_proposal(b, pn, cd["evidence"], model, style, a.rerun)
            row = {"bundle": bid, "ticker": b.ticker, "date": b.context["date"], "region": b.context["region"],
                   "policy": pn, "model": model, "style": style, "prompt_hash": h,
                   "ann_vol": b.context.get("ann_vol"), "tools": cd["tools"], "agg_dir": cd["agg_dir"],
                   "agg_conf": cd["agg_conf"], "code_size_ungated": cd["code_size_ungated"], "C": cd["C"], "U": U}
            if U is not None:
                row["verdict"], row["reasons"] = engine_verdict(U, pn, b.ticker, cd["evidence"])
            return row

        with ThreadPoolExecutor(a.workers) as ex:
            futs = [ex.submit(work, j) for j in jobs]
            for f in as_completed(futs):
                row = f.result()
                n += 1
                fails += row["U"] is None
                with lock:
                    fh.write(json.dumps(row) + "\n")
                if n % 500 == 0:
                    el = time.time() - t1
                    print(f"[{model}] {n}/{len(jobs)}  {el:.0f}s  ~{el / n * (len(jobs) - n) / 60:.0f} min left  "
                          f"fails={fails}", flush=True)
        fh.close()
        print(f"[{model}] done {n} rows ({fails} failed) in {time.time() - t1:.0f}s -> {path}", flush=True)


if __name__ == "__main__":
    main()
