import pytest
from src.pit import spend_guard


def test_budget_survives_restart_and_refuses_before_overspend(tmp_path, monkeypatch):
    monkeypatch.setenv("PIT_SPEND_DB", str(tmp_path / "spend.sqlite"))
    monkeypatch.setenv("PIT_BUDGET_USD", "0.001")
    first = spend_guard.reserve({})
    with pytest.raises(RuntimeError, match="exhausted"):
        spend_guard.reserve({})
    spend_guard.settle(first, 0.00001)
    spend_guard.reserve({})
    with pytest.raises(RuntimeError, match="exhausted"):
        spend_guard.reserve({})


def test_budget_rejects_increased_authorization(tmp_path, monkeypatch):
    monkeypatch.setenv("PIT_SPEND_DB", str(tmp_path / "spend.sqlite"))
    monkeypatch.setenv("PIT_BUDGET_USD", "6")
    with pytest.raises(RuntimeError, match="authorized"):
        spend_guard.reserve({})
