"""Generate LaTeX tables, macros and the survey chart from the project's real files.
Run with the code venv:  ../../code/.venv/bin/python make_tables.py"""
import csv
import json
import shutil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
FIG = ROOT / "06_Assessment_Oct2026" / "figures"
LIT = ROOT / "02_Workshop_Plan" / "lit_review_oct2026"
HERE = Path(__file__).resolve().parent
T = HERE / "tables"
T.mkdir(exist_ok=True)
(HERE / "figs").mkdir(exist_ok=True)
for f in FIG.glob("*.png"):
    shutil.copy(f, HERE / "figs" / f.name)


def esc(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"),
                 ("$", r"\$"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")]:
        s = s.replace(a, b)
    return s.replace("≈", r"$\approx$").replace("→", r"$\rightarrow$").replace("×", r"$\times$") \
            .replace("≥", r"$\geq$").replace("≤", r"$\leq$").replace("–", "--").replace("—", "---")


# ---------------- policies
pols = {p.stem: json.load(open(p)) for p in sorted((CODE / "config/policies").glob("*.json"))}
order = ["conservative", "long_term", "intraday", "aggressive_growth"]
lab = {"conservative": "Conservative", "long_term": "Long-term", "intraday": "Day-trader",
       "aggressive_growth": "Aggressive"}
rows = []
for k in order:
    p = pols[k]
    rows.append(f"{lab[k]} & {p['max_position_pct']:g} & {p['stop_loss_pct']:g} & {p['take_profit_pct']:g} & "
                f"{p['confidence_to_act']:.2f} & {p['evidence_budget']} & {p['target_vol']:.2f} & "
                f"{esc(', '.join(t.replace('_', ' ') for t in p['tool_priorities']))} \\\\")
(T / "policy.tex").write_text(r"""\begin{table*}[!t]
\centering\footnotesize
\caption{The four machine-readable investor policies used in all experiments (frozen before the runs).}
\label{tab:policy}
\begin{tabularx}{\textwidth}{lcccccc Y}
\toprule
Profile & Max pos.\ (\%) & Stop (\%) & Target (\%) & Conf.\ bar & Budget & Vol.\ budget & Evidence order \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabularx}
\end{table*}
""")

# ---------------- stack
stack = [("Orchestration", "Python 3.13, LangGraph state machine, LangChain"),
         ("Language model", "OpenAI gpt-4o-mini, temperature 0, structured (typed) outputs"),
         ("Market data", "Yahoo Finance (prices, company data), Finnhub (news, fundamentals), Google News RSS"),
         ("Universe", "20 US + 20 NSE large-cap stocks, list frozen 6 Aug 2026"),
         ("Numeric models", "scikit-learn logistic regression; indicators (SMA, EMA, RSI, volatility)"),
         ("Risk and audit", "Deterministic Python rules (no AI); JSONL decision log; frozen evidence bundles"),
         ("Evaluation", "Leakage-safe daily back-tester with costs; IC, Sharpe, drawdown, VaR; ECE, Brier"),
         ("Quality", "9 automated tests; pre-registered metric definitions; code on GitHub")]
(T / "stack.tex").write_text(r"""\begin{table}[!t]
\centering\footnotesize
\caption{Implementation stack.}
\label{tab:stack}
\begin{tabularx}{\linewidth}{l Y}
\toprule
Component & Implementation \\
\midrule
""" + "\n".join(f"{esc(a)} & {esc(b)} \\\\" for a, b in stack) + r"""
\bottomrule
\end{tabularx}
\end{table}
""")

# ---------------- obedience results (recomputed from the raw log)
import sys
sys.path.insert(0, str(CODE))
from src.core.policy import load_all_policies           # noqa: E402
from src.eval.adherence import check_card, ACTED         # noqa: E402
P = load_all_policies(CODE / "config/policies")
run = CODE / "logs/exp_obedience_20261004"
cards = [json.loads(l) for f in run.glob("decisions_*.jsonl") for l in open(f) if l.strip()]


def mode(c):
    return next(x.split(":", 1)[1] for x in c["policy_clauses_applied"] if x.startswith("mode:"))


def ci(x, n=4000):
    x = np.asarray(x, float)
    r = np.random.default_rng(0).choice(x, size=(n, len(x))).mean(1)
    return np.percentile(r, 2.5), np.percentile(r, 97.5)


ML = {"guarded": "Guarded (code decides)", "unguarded_explicit": "LLM + numeric rules",
      "unguarded_nl": "LLM + text profile only"}
res = {}
lines = []
for m in ["guarded", "unguarded_explicit", "unguarded_nl"]:
    g = [c for c in cards if mode(c) == m]
    viol = [any(check_card(c, P[c["policy_name"]])[0][k] for k in ("oversize", "bad_stop", "under_confidence"))
            for c in g]
    acted = [c for c in g if c["action"] in ACTED]
    va = [v for v, c in zip(viol, g) if c["action"] in ACTED]
    us = [v for v, c in zip(viol, g) if not c["ticker"].endswith(".NS")]
    ns = [v for v, c in zip(viol, g) if c["ticker"].endswith(".NS")]
    lo, hi = ci(viol)
    veto = np.mean([c["risk_verdict"] == "VETOED" for c in g])
    res[m] = dict(n=len(g), act=np.mean([c["action"] in ACTED for c in g]), viol=np.mean(viol), lo=lo, hi=hi,
                  acted_viol=(np.mean(va) if va else 0), n_acted=len(acted), us=np.mean(us), nse=np.mean(ns),
                  veto=veto, size=np.mean([c["position_size_pct"] for c in acted]) if acted else 0)
    r = res[m]
    lines.append(f"{ML[m]} & {r['n']} & {r['act']*100:.0f} & {r['viol']*100:.1f} [{r['lo']*100:.1f}, {r['hi']*100:.1f}] & "
                 f"{r['acted_viol']*100:.1f} ({r['n_acted']}) & {r['us']*100:.1f} & {r['nse']*100:.1f} & {r['veto']*100:.1f} \\\\")
(T / "obedience.tex").write_text(r"""\begin{table*}[!t]
\centering\footnotesize
\caption{Rule-following on identical evidence: """ + str(len({c['ticker'] for c in cards})) + r""" stocks (20 US, 20 NSE) $\times$ 4 investor profiles per decision mode. A violation is a position above the cap, a missing or looser stop-loss, or a trade below the confidence threshold. CI = 95\% bootstrap interval.}
\label{tab:obedience}
\begin{tabularx}{\textwidth}{>{\raggedright\arraybackslash}p{3.0cm} Z Z >{\centering\arraybackslash}p{2.9cm} Z Z Z Z}
\toprule
Decision mode & $N$ & Traded (\%) & Any violation (\%) [95\% CI] & Violation among trades (\%) ($n$) & US (\%) & NSE (\%) & Vetoed (\%) \\
\midrule
""" + "\n".join(lines) + r"""
\bottomrule
\end{tabularx}
\end{table*}
""")

# ---------------- numeric baselines
B = json.load(open(FIG / "results_numbers.json"))
ic = B["ic"]
cal = B["calibration"]
cq = B["cost_quality"]
names = {"momentum": "20-day momentum", "sma_crossover": "SMA 20/50 crossover", "rsi_reversion": "RSI mean reversion",
         "combo": "Combined (SMA + momentum)"}
(T / "baseline.tex").write_text(r"""\begin{table}[!t]
\centering\footnotesize
\caption{Numeric baselines on """ + str(len(B["baseline_tickers"])) + r""" stocks, three years of daily data (leakage-safe back-test, costs included).}
\label{tab:baseline}
\begin{tabularx}{\linewidth}{Y c c}
\toprule
Signal & Mean IC & Names with $|t|>2$ \\
\midrule
""" + "\n".join(f"{names[k]} & {v['mean_IC']:+.3f} & {v['sig_frac']*100:.0f}\\% \\\\" for k, v in ic.items()) + r"""
\midrule
\multicolumn{3}{l}{Stated-confidence calibration ($n=""" + f"{cal['n']}" + r"""$ calls, acc.~""" + f"{cal['base_acc']*100:.1f}" + r"""\%)} \\
\quad ECE / Brier, raw & \multicolumn{2}{c}{""" + f"{cal['ECE']:.3f} / {cal['Brier']:.3f}" + r"""} \\
\quad ECE / Brier, temperature-scaled ($T=""" + f"{cal['T']:.1f}" + r"""$) & \multicolumn{2}{c}{""" + f"{cal['ECE_after']:.3f} / {cal['Brier_after']:.3f}" + r"""} \\
\midrule
\multicolumn{3}{l}{Evidence cost (threshold """ + f"{cq[0]['threshold']:.2f}$\\rightarrow${cq[-1]['threshold']:.2f}" + r""")} \\
\quad Mean sources used & \multicolumn{2}{c}{""" + f"{cq[0]['mean_cost']:.2f} $\\rightarrow$ {cq[-1]['mean_cost']:.2f}" + r"""} \\
\quad Directional accuracy & \multicolumn{2}{c}{""" + f"{cq[0]['accuracy']*100:.1f}\\% $\\rightarrow$ {cq[-1]['accuracy']*100:.1f}\\%" + r"""} \\
\bottomrule
\end{tabularx}
\end{table}
""")

# ---------------- survey (from the verified CSV, if available)
survey_csv = HERE / "survey_ext.csv" if (HERE / "survey_ext.csv").exists() else LIT / "C_survey_table.csv"
if survey_csv.exists():
    S = list(csv.DictReader(open(survey_csv)))

    def cite(r):
        return r["bibtex_key"].strip()
    flags = [("evaluates_returns", "Returns"), ("evaluates_risk_metrics", "Risk metrics"),
             ("evaluates_mandate_or_policy_adherence", "Rule / mandate\nfollowing"),
             ("evaluates_confidence_calibration", "Confidence\ncalibration"),
             ("evaluates_cost_or_efficiency", "Cost /\nefficiency"),
             ("controls_lookahead_leakage", "Look-ahead\nleakage control"), ("uses_indian_market", "Indian\nmarket")]

    import re as _re
    NICE = {"LLMTradingSurvey": "Ding et al. (survey)", "PersonaCollapse": "Persona collapse",
            "AlphaIllusion": "Alpha Illusion", "PolicyAsSkill": "Policy-as-Skill", "ActionAudit": "Action audit",
            "AgentMarketArena": "Agent Market Arena", "OrdinalGates": "Ordinal Gates", "InvestLogicBench": "InvestLogic\\-Bench"}

    def disp(r):
        sn = r["short_name"].strip()
        if _re.search(r"\d{4}", sn):
            return esc(r["authors"].strip())
        return NICE.get(sn, esc(sn))

    def tab(chunk, start, label, cont=""):
        body = []
        for i, r in enumerate(chunk, start):
            body.append(f"{i} & {disp(r)}~\\cite{{{cite(r)}}} & {esc(r['year'])} & {esc(r['approach'])} & "
                        f"{esc(r['data_market'] if 'data_market' in r else r.get('data', ''))} & {esc(r['key_result'])} \\\\")
        return (r"""\begin{table*}[!p]
\centering\scriptsize
\caption{Literature survey""" + cont + r""": approach, data and reported result of each surveyed paper.}
\label{""" + label + r"""}
\begin{tabularx}{\textwidth}{r p{2.5cm} c Y p{2.6cm} Y}
\toprule
\# & Paper & Year & Approach & Data / market & Key reported result \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabularx}
\end{table*}
""")
    half = (len(S) + 1) // 2
    (T / "survey.tex").write_text(tab(S[:half], 1, "tab:survey") +
                                  tab(S[half:], half + 1, "tab:survey2", " (continued)"))
    counts = [sum(r.get(k, "N").strip().upper().startswith("Y") for r in S) for k, _ in flags]
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    cols = ["#5C6B7A", "#5C6B7A", "#006633", "#006633", "#006633", "#14243A", "#B9820F"]
    b = ax.bar([l for _, l in flags], counts, color=cols)
    for rect, v in zip(b, counts):
        ax.text(rect.get_x() + rect.get_width() / 2, v + 0.3, str(v), ha="center", fontsize=9)
    ax.set_ylabel(f"Papers (of {len(S)})")
    ax.set_title("What do the surveyed papers actually measure?")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(HERE / "figs" / "fig_survey_coverage.png", dpi=300)
    shutil.copy(HERE / "figs" / "fig_survey_coverage.png", FIG / "fig_survey_coverage.png")
    n_survey = len(S)
    print("survey:", n_survey, "papers; counts", dict(zip([k for k, _ in flags], counts)))
else:
    (T / "survey.tex").write_text(r"\writebox{Survey table pending (agent output not ready).}")
    n_survey = 0

# ---------------- macros
macros = {
    "ObStocks": str(len({c["ticker"] for c in cards})),
    "ObExplicit": f"{res['unguarded_explicit']['viol']*100:.1f}\\%",
    "ObNL": f"{res['unguarded_nl']['viol']*100:.1f}\\%",
    "ObNLlo": f"{res['unguarded_nl']['lo']*100:.1f}", "ObNLhi": f"{res['unguarded_nl']['hi']*100:.1f}",
    "ObNLacted": f"{res['unguarded_nl']['acted_viol']*100:.0f}\\%",
    "ECEraw": f"{cal['ECE']:.3f}", "ECEtemp": f"{cal['ECE_after']:.3f}",
}
m = "\n".join(f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in macros.items())
m += "\n" + r"\newcommand{\PolicyTable}{\input{tables/policy}}" + "\n" + r"\newcommand{\StackTable}{\input{tables/stack}}"
m += "\n" + r"\newcommand{\ObedienceTable}{\input{tables/obedience}}" + "\n" + r"\newcommand{\BaselineTable}{\input{tables/baseline}}"
m += "\n" + r"\newcommand{\SurveyTable}{\input{tables/survey}}" + "\n"
(T / "macros.tex").write_text(m)
json.dump({k: {kk: float(vv) for kk, vv in v.items()} for k, v in res.items()}, open(HERE / "obedience_numbers.json", "w"), indent=2)
print("tables written; obedience:", {k: round(v['viol'], 3) for k, v in res.items()})
