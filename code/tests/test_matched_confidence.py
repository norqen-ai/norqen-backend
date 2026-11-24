import pandas as pd
import pytest
from matched_conf_check import matched_difference


def test_profile_composition_does_not_create_within_cell_effect():
    rows = []
    for policy, value, raised, above in (("safe", 0, 9, 1), ("risky", 1, 1, 9)):
        for group, count in (("raised", raised), ("above", above)):
            rows.extend([{"policy": policy, "region": "US", "group": group, "hit": value}] * count)
    frame = pd.DataFrame(rows)
    assert frame[frame.group == "raised"].hit.mean() < frame[frame.group == "above"].hit.mean()
    assert matched_difference(frame, "hit") == pytest.approx(0)


def test_unmatched_cell_is_excluded():
    frame = pd.DataFrame([
        {"policy": "a", "region": "US", "group": "raised", "pnl": 3},
        {"policy": "a", "region": "US", "group": "above", "pnl": 1},
        {"policy": "b", "region": "US", "group": "raised", "pnl": 999},
    ])
    assert matched_difference(frame, "pnl") == pytest.approx(2)
