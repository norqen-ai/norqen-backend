"""Validate the complete fixed local sample and generate its separate appendix table."""
import json
from pathlib import Path

from make_finfm_tables import wilson
from src.core.policy import load_all_policies

ROOT = Path("logs/finfm_2027/local_robustness")
MODELS = {"llama-3.1-8b-local": "Llama 3.1 8B", "gpt-oss-20b-local": "GPT-OSS 20B",
          "gemma-3-4b-local": "Gemma 3 4B", "phi-4-local": "Phi-4 14B"}


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main():
    policies = load_all_policies("config/policies")
    reference = None
    results, tex = {}, []
    for model, label in MODELS.items():
        proposals = read(ROOT / f"decisions_{model}.jsonl")
        keys = {(r["bundle"], r["policy"]) for r in proposals}
        assert len(proposals) == len(keys) == 152 and all(r["U"] for r in proposals), model
        if reference is None:
            reference = keys
        assert keys == reference, "Models evaluated different samples"
        strata = {(r["date"][:7], r["region"]) for r in proposals}
        assert len(strata) == 38
        provenance = {json.dumps(r["U"]["model_metadata"], sort_keys=True) for r in proposals}
        assert len(provenance) == 1, "Mixed model provenance"
        result = {"decisions": len(proposals), "provenance": json.loads(provenance.pop())}
        expected = {(r["bundle"], r["policy"]) for r in proposals if r["verdict"] == "VETOED"
                    and r["U"]["action"] in ("BUY", "SELL") and r["U"]["size"] > 0
                    and any("below policy threshold" in reason for reason in r["reasons"])}
        eligible_keys = None
        cells = []
        for arm, suffix in (("shown", ""), ("hidden", "_hideconf")):
            rows = read(ROOT / f"revise_{model}_r3{suffix}_confset.jsonl")
            assert {(r["bundle"], r["policy"]) for r in rows} == expected
            assert len(rows) == len(expected), "Duplicate arm rows"
            assert all(all(h["D"] is not None for h in r["history"]) for r in rows), "Failed model revision"
            rows = [r for r in rows if any("below policy threshold" not in s for s in r["U_reasons"])]
            ids = {(r["bundle"], r["policy"]) for r in rows}
            if eligible_keys is None:
                eligible_keys = ids
            assert ids == eligible_keys
            raised = 0
            for row in rows:
                history = row["history"]
                raised += bool(history and history[-1]["D"]["conf"] >= policies[row["policy"]].confidence_to_act - 1e-9)
            n = len(rows)
            result[arm] = {"n": n, "raised": raised}
            if n:
                lo, hi = wilson(raised, n)
                cells.append(f"{100*raised/n:.1f} [{lo:.1f}, {hi:.1f}]")
            else:
                cells.append("--")
        results[model] = result
        tex.append(f"{label} & {result['shown']['n']} & " + " & ".join(cells) + r" \\")
    (ROOT / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
    Path("../paper_finfm/tables/local_robustness.tex").write_text(
        r"\begin{tabular}{lrll}" + "\n" + r"\toprule" + "\n" +
        r"Model & Eligible $n$ & Bar shown (\%) & Bar hidden (\%) \\" + "\n" +
        r"\midrule" + "\n" + "\n".join(tex) + "\n" + r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
