"""Exploratory profile × region standardized comparison of kept feedback trades.

Raised: below-bar proposals kept after bar-shown feedback. Above: originally
above-bar proposals kept after ordinary feedback. This is observational, not a
causal estimate: proposal selection, direction and size can still differ.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.core.policy import load_all_policies
from src.pit.outcomes import HORIZON, evaluate


def matched_difference(frame, metric):
    cells = frame.groupby(["policy", "region", "group"])[metric].agg(["sum", "count"])
    means = (cells["sum"] / cells["count"]).unstack("group")
    counts = cells["count"].unstack("group")
    if not {"raised", "above"} <= set(means):
        return float("nan")
    common = means.dropna(subset=["raised", "above"])
    if common.empty:
        return float("nan")
    weights = counts.loc[common.index, ["raised", "above"]].sum(axis=1)
    return float(np.average(common.raised - common.above, weights=weights))


def compare(frame, repeats=2000):
    rng = np.random.default_rng(20261123)
    months = sorted(frame.month.unique())
    # Resample entire decision months jointly for both groups and all cells.
    boot = {m: [] for m in ("hit", "pnl")}
    for _ in range(repeats):
        sampled = rng.choice(months, len(months), replace=True)
        replicate = pd.concat([frame[frame.month == month] for month in sampled], ignore_index=True)
        for metric in boot:
            boot[metric].append(matched_difference(replicate, metric))
    result = {"n_raised": int((frame.group == "raised").sum()),
              "n_above": int((frame.group == "above").sum()), "months": len(months)}
    for metric, values in boot.items():
        finite = np.asarray(values)[np.isfinite(values)]
        result[metric] = {"difference": matched_difference(frame, metric),
                          "ci95": np.percentile(finite, [2.5, 97.5]).tolist() if len(finite) else None,
                          "valid_bootstraps": len(finite)}
    return result


def load_model(model, directory):
    policies = load_all_policies("config/policies")
    records = []
    seen = set()
    for group, suffix in (("raised", "_confset"), ("above", "")):
        path = directory / f"revise_{model}_r3{suffix}.jsonl"
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            row = json.loads(line)
            policy = policies[row["policy"]]
            below = row["U"]["conf"] < policy.confidence_to_act - 1e-9
            if below != (group == "raised"):
                continue
            final = row.get("final")
            if not final or final["action"] not in ("BUY", "SELL") or final["size"] <= 0:
                continue
            key = (row["ticker"], row["date"], row["policy"], group)
            if key in seen:
                raise ValueError(f"Duplicate outcome: {key}")
            seen.add(key)
            outcome = evaluate(row["ticker"], row["date"], final["action"], final["size"],
                               final["stop"], final["tp"], HORIZON[row["policy"]])
            if outcome["traded"]:
                records.append({"policy": row["policy"], "region": row["region"],
                                "month": row["date"][:7], "group": group,
                                "hit": float(outcome["ret"] > 0), "pnl": outcome["pnl"]})
    return pd.DataFrame(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", default="gpt-4o-mini,gpt-4.1-mini,gpt-5-mini")
    parser.add_argument("--out", default="logs/finfm_2027/matched_confidence.json")
    parser.add_argument("--bootstrap", type=int, default=2000)
    args = parser.parse_args()
    results = {}
    for model in args.models.split(","):
        frame = load_model(model, Path("logs/finfm_2027"))
        if frame.empty or frame.group.nunique() < 2:
            results[model] = {"status": "insufficient overlapping groups"}
            continue
        results[model] = compare(frame, args.bootstrap)
        print(model, json.dumps(results[model]), flush=True)
    Path(args.out).write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
