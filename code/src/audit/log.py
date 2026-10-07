"""Audit log + frozen-evidence replay. This module is the research instrument.

Two jobs:
 1. DecisionLogger — append-only JSONL of every DecisionCard (approved AND vetoed).
    The dashboard reads this; the paper's numbers come from this.
 2. EvidenceBundle — freeze the evidence of a decision moment so it can be
    replayed deterministically under ANY policy later ("time-machine mode").
    This is experiment E1's engine and the future public benchmark artifact.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from src.core.schemas import DecisionCard, EvidenceItem


class DecisionLogger:
    def __init__(self, log_dir: str | Path = "logs"):
        self.dir = Path(log_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"decisions_{time.strftime('%Y%m%d')}.jsonl"

    def log(self, card: DecisionCard) -> None:
        with self.path.open("a") as f:
            f.write(json.dumps(card.to_dict()) + "\n")

    def read_all(self) -> list[dict]:
        cards: list[dict] = []
        for p in sorted(self.dir.glob("decisions_*.jsonl")):
            with p.open() as f:
                cards += [json.loads(line) for line in f if line.strip()]
        return cards


class EvidenceBundle:
    """A frozen decision moment: ticker + timestamp + every EvidenceItem gathered."""

    def __init__(self, ticker: str, evidence: list[EvidenceItem], ts: float | None = None,
                 context: dict | None = None):
        self.ticker = ticker
        self.evidence = evidence
        self.ts = ts or time.time()
        self.context = context or {}     # frozen market context (e.g. ann_vol) for leakage-safe sizing

    def save(self, bundle_dir: str | Path = "logs/bundles") -> Path:
        d = Path(bundle_dir)
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"bundle_{self.ticker}_{int(self.ts)}.json"
        path.write_text(json.dumps({
            "ticker": self.ticker,
            "ts": self.ts,
            "context": self.context,
            "evidence": [e.to_dict() for e in self.evidence],
        }, indent=2))
        return path

    @classmethod
    def load(cls, path: str | Path) -> "EvidenceBundle":
        raw = json.loads(Path(path).read_text())
        ev = [EvidenceItem(**e) for e in raw["evidence"]]
        return cls(raw["ticker"], ev, raw["ts"], raw.get("context", {}))

    def as_tools(self) -> dict:
        """Expose frozen evidence as a tool registry, so the SAME planner code
        runs on frozen data — one item per tool name, returned verbatim."""
        by_tool = {e.tool: e for e in self.evidence}
        return {name: (lambda t, _e=item: _e) for name, item in by_tool.items()}
