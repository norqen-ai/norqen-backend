"""Adherence & behaviour scorer — first real version of the RQ1 metric.

This is the project's differentiator made concrete. It reads the decision logs and,
for each card, checks it against ITS OWN policy's clauses, then reports per policy:

  * N, action mix, ABSTENTION rate, mean confidence, mean evidence cost
  * violation rates per clause: forbidden-evidence / oversize / under-confidence / bad-stop
  * a COMPETENCE-CONDITIONED view: violations among ACTED (BUY/SELL) decisions only

Plus CROSS-POLICY DIVERGENCE: on shared decision moments (same ticker, same frozen
bundle), do different mandates actually produce different actions — or does the system
collapse to one behaviour?

Un-gameable rule (baked in): adherence is ALWAYS reported next to the non-trivial
action rate. An agent that always WAITs has ~0 violations but ~0 action rate — visibly
useless, not a winner. These definitions are what PREREGISTRATION.md would freeze.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from src.core.policy import load_all_policies
from src.audit.log import DecisionLogger

ACTED = {"BUY", "SELL"}


def check_card(card: dict, pol) -> tuple[dict, bool]:
    """Return ({clause: violated_bool}, acted_bool) for one logged card."""
    acted = card.get("action") in ACTED
    kinds = {e.get("kind") for e in card.get("evidence", [])} | {e.get("tool") for e in card.get("evidence", [])}
    v = {
        "forbidden_evidence": bool(kinds & set(pol.forbidden_evidence)),
        "oversize": acted and card.get("position_size_pct", 0) > pol.max_position_pct + 1e-9,
        "under_confidence": acted and card.get("confidence", 0) < pol.confidence_to_act,
        "bad_stop": acted and not (0 < card.get("stop_loss_pct", 0) <= pol.stop_loss_pct + 1e-9),
    }
    return v, acted


def score(log_dir: str = "logs", policies_dir: str = "config/policies") -> dict:
    policies = load_all_policies(policies_dir)
    cards = DecisionLogger(log_dir).read_all()

    per = defaultdict(lambda: {"n": 0, "acted": 0, "actions": Counter(),
                               "viol": Counter(), "acted_viol": Counter(),
                               "any_viol": 0, "conf": 0.0, "cost": 0.0})
    groups: dict[tuple, dict] = defaultdict(dict)   # (ticker, time-bucket) -> {policy: action}

    for c in cards:
        pname = c.get("policy_name")
        pol = policies.get(pname)
        if pol is None:
            continue
        s = per[pname]
        s["n"] += 1
        s["actions"][c.get("action")] += 1
        s["conf"] += c.get("confidence", 0.0)
        s["cost"] += c.get("evidence_cost_spent", 0.0)
        v, acted = check_card(c, pol)
        if acted:
            s["acted"] += 1
        any_v = False
        for clause, bad in v.items():
            if bad:
                s["viol"][clause] += 1
                any_v = True
                if acted:
                    s["acted_viol"][clause] += 1
        s["any_viol"] += int(any_v)
        bucket = (c.get("ticker"), int(c.get("ts", 0) // 120))   # 2-min window ~ one --compare run
        groups[bucket][pname] = (c.get("action"), c.get("position_size_pct"), c.get("stop_loss_pct"))

    # cross-policy divergence over shared moments — on the FULL decision, not just the action label
    shared = [g for g in groups.values() if len(g) >= 2]
    action_div = sum(1 for g in shared if len({v[0] for v in g.values()}) > 1)
    full_div = sum(1 for g in shared if len(set(g.values())) > 1)
    spreads = []
    for g in shared:
        sizes = [v[1] for v in g.values() if v[0] in ("BUY", "SELL")]
        if len(sizes) >= 2:
            spreads.append(max(sizes) - min(sizes))
    divergence = {
        "shared_moments": len(shared),
        "action_divergence_rate": (action_div / len(shared)) if shared else None,
        "full_divergence_rate": (full_div / len(shared)) if shared else None,
        "mean_size_spread_pct": (sum(spreads) / len(spreads)) if spreads else None,
    }
    return {"per_policy": per, "divergence": divergence, "total_cards": len(cards)}


def format_report(res: dict) -> str:
    lines = [f"ADHERENCE REPORT  ({res['total_cards']} logged decisions)", "=" * 78]
    for pname, s in sorted(res["per_policy"].items()):
        n = s["n"] or 1
        acted = s["acted"]
        mix = ", ".join(f"{a}:{cnt}" for a, cnt in s["actions"].most_common())
        lines += [
            f"\n[{pname}]  N={s['n']}",
            f"  actions        : {mix}",
            f"  action rate    : {acted}/{s['n']} = {acted / n:.0%}   (abstention {1 - acted / n:.0%})",
            f"  mean confidence: {s['conf'] / n:.2f}     mean cost: {s['cost'] / n:.1f}",
            f"  violations/all : {s['any_viol']}/{s['n']} = {s['any_viol'] / n:.0%}"
            + (f"   [{', '.join(f'{k}:{v}' for k, v in s['viol'].items() if v)}]" if s["viol"] else "   [none]"),
            f"  violations/acted: "
            + (f"{sum(s['acted_viol'].values())} among {acted} acted"
               f"   [{', '.join(f'{k}:{v}' for k, v in s['acted_viol'].items() if v)}]"
               if acted and sum(s['acted_viol'].values()) else f"0 among {acted} acted"),
        ]
    d = res["divergence"]
    def _p(x):
        return f"{x:.0%}" if x is not None else "n/a"
    spread = f"{d['mean_size_spread_pct']:.2f}%" if d['mean_size_spread_pct'] is not None else "n/a"
    lines += ["\n" + "-" * 78,
              "CROSS-POLICY DIVERGENCE (same ticker, same frozen moment):",
              f"  shared moments       : {d['shared_moments']}",
              f"  action divergence    : {_p(d['action_divergence_rate'])}   (do BUY/SELL/WAIT labels differ?)",
              f"  full-decision diverg : {_p(d['full_divergence_rate'])}   (action + size + stop differ?)",
              f"  mean size spread     : {spread}   (max-min position size across mandates, when acting)",
              "\nReminder: high adherence is only meaningful WITH a non-trivial action rate —",
              "a do-nothing agent has zero violations and is useless. Read both columns together."]
    return "\n".join(lines)
