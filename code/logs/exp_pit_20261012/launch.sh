#!/bin/zsh
cd /Users/malhar.inamdar/Desktop/BE_Final_Year_Project/code
until grep -q '^done' logs/exp_pit_20261012/build.log; do sleep 5; done
echo "build finished $(date +%T): $(tail -1 logs/exp_pit_20261012/build.log)"
.venv/bin/python run_pit_decisions.py --models gpt-4o-mini --workers 32 > logs/exp_pit_20261012/run_4o.log 2>&1 &
.venv/bin/python run_pit_decisions.py --models gpt-4.1-mini --workers 32 > logs/exp_pit_20261012/run_41.log 2>&1 &
.venv/bin/python run_pit_decisions.py --models gpt-5-mini --workers 48 > logs/exp_pit_20261012/run_5.log 2>&1 &
wait
echo "all decision runs finished $(date +%T)"
