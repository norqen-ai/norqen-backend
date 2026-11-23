"""Run the adherence scorer (RQ1) over everything in logs/.

  python3 score_adherence.py

This is the research read-out: it turns the decision logs into per-policy behaviour,
per-clause violation rates, and cross-policy divergence — the numbers the paper reports.
"""
from src.eval.adherence import score, format_report

if __name__ == "__main__":
    print(format_report(score()))
