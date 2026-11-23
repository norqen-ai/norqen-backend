"""Re-run noise floor (pre-registered robustness): an independent second query of gpt-4o-mini on
every (bundle, profile, style), compared with the primary run on identical prompts.

  python noise_floor.py --exp logs/exp_pit_20261012 --model gpt-4o-mini --tag _rerun1
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_components import score, boot_mean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default="logs/exp_pit_20261012")
    ap.add_argument("--model", default="gpt-4o-mini")
    ap.add_argument("--tag", default="_rerun1")
    a = ap.parse_args()
    exp = Path(a.exp)
    A = [json.loads(l) for l in (exp / f"decisions_{a.model}.jsonl").open()]
    Bb = [json.loads(l) for l in (exp / f"rerun_{a.model}{a.tag}.jsonl").open()]
    key = lambda r: (r["bundle"], r["policy"], r["style"])
    bmap = {key(r): r for r in Bb if r["U"]}
    pairs = [(r, bmap[key(r)]) for r in A if r["U"] and key(r) in bmap]
    out = {"pairs": len(pairs)}
    for style in ("nl", "explicit"):
        ps = [(x, y) for x, y in pairs if x["style"] == style]
        same_action = np.mean([x["U"]["action"] == y["U"]["action"] for x, y in ps])
        both = [(x, y) for x, y in ps if x["U"]["action"] in ("BUY", "SELL") and y["U"]["action"] in ("BUY", "SELL")]
        same_size = np.mean([abs(x["U"]["size"] - y["U"]["size"]) < 1e-9 for x, y in both]) if both else np.nan
        same_verdict = np.mean([x.get("verdict") == y.get("verdict") for x, y in ps])
        out[style] = {"n": len(ps), "same_action": float(same_action), "same_size_if_both_trade": float(same_size),
                      "same_verdict": float(same_verdict)}
    # pipeline means on each run (pnl, pooled profiles), to compare with the between-pipeline gaps
    sa = score([x for x, _ in pairs]); sb = score([y for _, y in pairs])
    for style in ("nl", "explicit"):
        for name in ("raw", "block", "repair", "judge"):
            ma = boot_mean(sa[sa["style"] == style], f"pnl_{name}")[0]
            mb = boot_mean(sb[sb["style"] == style], f"pnl_{name}")[0]
            out[style][f"{name}_run1"], out[style][f"{name}_run2"] = round(ma, 3), round(mb, 3)
    print(json.dumps(out, indent=1))
    (exp / "analysis" / "noise_floor.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
