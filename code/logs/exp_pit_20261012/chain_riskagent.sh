#!/bin/zsh
cd /Users/malhar.inamdar/Desktop/BE_Final_Year_Project/code
L=logs/exp_pit_20261012
for pair in "gpt-4.1-mini:run_41.log" "gpt-4o-mini:run_4o.log" "gpt-5-mini:run_5.log"; do
  m=${pair%%:*}; f=${pair##*:}
  until grep -q "\[$m\] done" $L/$f; do sleep 10; done
  echo "$(date +%T) $m decisions done -> risk-agent review"
  .venv/bin/python run_pit_riskagent.py --models $m --reviewer gpt-4o-mini --workers 32 2>&1 | grep -v -i warn
done
echo "$(date +%T) risk-agent chain finished"
