"""Core invariants. Run:  python3 -m pytest tests/  (or python3 tests/test_core.py)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.policy import load_all_policies, load_policy
from src.core.schemas import EvidenceItem, PortfolioState
from src.agents.planner import Planner
from src.risk.engine import RiskEngine
from src.audit.log import EvidenceBundle

POL_DIR = Path(__file__).resolve().parents[1] / "config" / "policies"


def _evidence(ticker="TEST"):
    return [
        EvidenceItem("technical", "technical", ticker, "up", +0.8, 0.8, 0.8),
        EvidenceItem("news", "news", ticker, "up", +0.7, 0.7, 0.8),
        EvidenceItem("fundamental", "fundamental", ticker, "up", +0.6, 0.7, 0.9),
        EvidenceItem("macro", "macro", ticker, "flat", 0.0, 0.6, 0.9),
    ]


def test_policies_load_and_validate():
    pols = load_all_policies(POL_DIR)
    assert {"conservative", "aggressive_growth", "long_term", "intraday"} <= set(pols)
    for p in pols.values():
        p.validate()


def test_planner_respects_position_cap_and_stop():
    pols = load_all_policies(POL_DIR)
    tools = EvidenceBundle("TEST", _evidence()).as_tools()
    for p in pols.values():
        card = Planner(p, tools).decide("TEST")
        assert card.position_size_pct <= p.max_position_pct
        if card.action in ("BUY", "SELL"):
            assert card.stop_loss_pct == p.stop_loss_pct


def test_cross_policy_divergence_exists():
    pols = load_all_policies(POL_DIR)
    tools = EvidenceBundle("TEST", _evidence()).as_tools()
    sizes = {n: Planner(p, tools).decide("TEST").position_size_pct for n, p in pols.items()}
    assert sizes["aggressive_growth"] != sizes["conservative"]


def test_risk_engine_vetoes_oversize_and_daily_loss():
    p = load_policy(POL_DIR / "conservative.json")
    tools = EvidenceBundle("TEST", _evidence()).as_tools()
    ok_pf = PortfolioState(1e6, 4e5, 1, -0.1)
    card = Planner(p, tools).decide("TEST")
    card.action, card.position_size_pct, card.stop_loss_pct = "BUY", 9.0, p.stop_loss_pct
    verdict = RiskEngine(p).check(card, ok_pf)
    assert verdict.risk_verdict == "VETOED"
    assert any("exceeds policy cap" in r for r in verdict.risk_reasons)

    bad_day = PortfolioState(1e6, 4e5, 1, -5.0)
    card2 = Planner(p, tools).decide("TEST")
    card2.action, card2.position_size_pct, card2.stop_loss_pct = "BUY", 1.0, p.stop_loss_pct
    card2.confidence = 0.9
    verdict2 = RiskEngine(p).check(card2, bad_day)
    assert verdict2.risk_verdict == "VETOED"
    assert any("daily loss" in r for r in verdict2.risk_reasons)


def test_replay_is_deterministic(tmp_path=None):
    import tempfile
    p = load_policy(POL_DIR / "conservative.json")
    b = EvidenceBundle("TEST", _evidence())
    with tempfile.TemporaryDirectory() as d:
        path = b.save(d)
        loaded = EvidenceBundle.load(path)
    c1 = Planner(p, b.as_tools()).decide("TEST")
    c2 = Planner(p, loaded.as_tools()).decide("TEST")
    assert (c1.action, c1.position_size_pct, c1.confidence) == \
           (c2.action, c2.position_size_pct, c2.confidence)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
