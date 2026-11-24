"""Conservative persistent OpenRouter reservations shared by all experiment processes."""
import json
import os
from pathlib import Path
import sqlite3


def connect():
    path = Path(os.environ["PIT_SPEND_DB"])
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=60)
    db.execute("CREATE TABLE IF NOT EXISTS spend (id INTEGER PRIMARY KEY, usd REAL NOT NULL)")
    return db


def reserve(payload):
    # UTF-8 bytes plus a generous message/template allowance bound input tokens.
    # Provider routing is capped to these prices in llm_client.py (USD per token).
    ceiling = (len(json.dumps(payload).encode()) + 4096) * 0.08e-6 + 2048 * 0.16e-6
    limit = float(os.environ["PIT_BUDGET_USD"])
    if not 0 < limit <= 5:
        raise RuntimeError("Budget must be positive and at most the authorized $5")
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        used = db.execute("SELECT COALESCE(SUM(usd), 0) FROM spend").fetchone()[0]
        if used + ceiling > limit:
            raise RuntimeError("OpenRouter budget exhausted; no request sent")
        return db.execute("INSERT INTO spend(usd) VALUES (?)", (ceiling,)).lastrowid


def settle(reservation, actual):
    # Missing usage or failed requests retain their full reservation, including across restarts.
    if actual is not None and float(actual) >= 0:
        with connect() as db:
            db.execute("UPDATE spend SET usd=? WHERE id=?", (float(actual), reservation))
