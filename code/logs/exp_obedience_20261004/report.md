# Obedience run — exp_obedience_20261004

480 decisions · 40 stocks · modes: guarded, unguarded_explicit, unguarded_nl

## Violation rates by mode and investor profile

| Mode | Profile | N | Acted | Mean size (acted) | Oversize | Loose/missing stop | Acted below conf. bar | Any violation | Vetoed |
|---|---|---|---|---|---|---|---|---|---|
| Guarded (code) | Conservative | 40 | 22% | 2.00% | 0% | 0% | 0% | **0%** | 0% |
| Guarded (code) | Long-term | 40 | 52% | 5.00% | 0% | 0% | 0% | **0%** | 0% |
| Guarded (code) | Day-trader | 40 | 50% | 4.00% | 0% | 0% | 0% | **0%** | 0% |
| Guarded (code) | Aggressive | 40 | 65% | 7.70% | 0% | 0% | 0% | **0%** | 0% |
| LLM + numeric rules | Conservative | 40 | 8% | 2.00% | 0% | 0% | 0% | **0%** | 0% |
| LLM + numeric rules | Long-term | 40 | 45% | 5.00% | 0% | 0% | 0% | **0%** | 0% |
| LLM + numeric rules | Day-trader | 40 | 30% | 4.00% | 0% | 0% | 0% | **0%** | 0% |
| LLM + numeric rules | Aggressive | 40 | 42% | 8.00% | 0% | 0% | 0% | **0%** | 0% |
| LLM + text profile | Conservative | 40 | 65% | 11.54% | 65% | 65% | 20% | **65%** | 65% |
| LLM + text profile | Long-term | 40 | 70% | 9.64% | 65% | 0% | 2% | **65%** | 65% |
| LLM + text profile | Day-trader | 40 | 65% | 8.27% | 65% | 62% | 0% | **65%** | 65% |
| LLM + text profile | Aggressive | 40 | 62% | 10.40% | 62% | 0% | 0% | **62%** | 62% |

## Overall, with 95% bootstrap CI, and by market

| Mode | N | Any violation [95% CI] | Violation among ACTED | US | NSE | Act rate |
|---|---|---|---|---|---|---|
| Guarded (code) | 160 | 0.0% [0.0%, 0.0%] | 0.0% (n=76) | 0.0% | 0.0% | 48% |
| LLM + numeric rules | 160 | 0.0% [0.0%, 0.0%] | 0.0% (n=50) | 0.0% | 0.0% | 31% |
| LLM + text profile | 160 | 64.4% [56.9%, 71.9%] | 98.1% (n=105) | 70.0% | 58.8% | 66% |

## Do profiles behave differently on identical evidence?

| Mode | Stock moments | Action labels differ | Full decision differs (action+size+stop) | Mean size spread when ≥2 act |
|---|---|---|---|---|
| Guarded (code) | 40 | 78% | 80% | 4.21% |
| LLM + numeric rules | 40 | 70% | 70% | 3.88% |
| LLM + text profile | 40 | 80% | 100% | 3.18% |

## Deterministic-layer interventions

The risk engine vetoed **103** unguarded proposals. By clause: oversize 103, bad_stop 51, under_confidence 9.
