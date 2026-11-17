#!/bin/zsh
# Resume after the OpenAI credit top-up: cached calls are free; only missing ones are paid.
cd /Users/malhar.inamdar/Desktop/BE_Final_Year_Project/code
L=logs/exp_pit_20261012
MODELS=${MODELS:-"gpt-4o-mini gpt-4.1-mini gpt-5-mini"}
for m in ${=MODELS}; do
  w=32; [[ $m == gpt-5-mini ]] && w=48
  .venv/bin/python run_pit_decisions.py --models $m --workers $w > $L/run_$m.log 2>&1 &
done
wait
echo "$(date +%T) decisions done"; for m in ${=MODELS}; do grep -v -i warn $L/run_$m.log | tail -1; done
.venv/bin/python run_pit_riskagent.py --models ${MODELS// /,} --reviewer gpt-4o-mini --workers 32 2>&1 | grep -v -i warn
echo "$(date +%T) risk agent done"
.venv/bin/python run_pit_decisions.py --models gpt-4o-mini --workers 32 --rerun :rerun1 2>&1 | grep -v -i warn | tail -1
echo "$(date +%T) rerun done"
