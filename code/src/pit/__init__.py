"""Point-in-time (PIT) historical replay of the multi-agent system.

Rebuilds every specialist agent's evidence AS OF a past decision date t, using only
data with timestamp <= t, so LLM decisions can be scored against realised outcomes
on dates after each model's training cutoff. Used by the decision-component study
(build_pit_bundles.py -> run_pit_decisions.py -> analyze_components.py).
"""
