#!/bin/zsh
cd /Users/malhar.inamdar/Desktop/BE_Final_Year_Project/code
L=logs/exp_pit_20261012
echo "$(date +%T) news"; PIT_START=2024-07-15 PYTHONPATH=. .venv/bin/python data/pit_news_dl.py 2>&1 | grep -v -i warn | tail -1
echo "$(date +%T) bundles"; .venv/bin/python build_pit_bundles.py --start 2024-07-15 --workers 24 2>&1 | grep -v -i warn | tail -1
echo "$(date +%T) decisions 4o + 4.1"
.venv/bin/python run_pit_decisions.py --models gpt-4o-mini --workers 32 > $L/ext_4o.log 2>&1 &
.venv/bin/python run_pit_decisions.py --models gpt-4.1-mini --workers 32 > $L/ext_41.log 2>&1 &
wait; grep -v -i warn $L/ext_4o.log | tail -1; grep -v -i warn $L/ext_41.log | tail -1
echo "$(date +%T) risk agent 4o + 4.1"; .venv/bin/python run_pit_riskagent.py --models gpt-4o-mini,gpt-4.1-mini --reviewer gpt-4o-mini --workers 32 2>&1 | grep -v -i warn | tail -2
echo "$(date +%T) decisions 5-mini"; .venv/bin/python run_pit_decisions.py --models gpt-5-mini --workers 48 > $L/ext_5.log 2>&1; grep -v -i warn $L/ext_5.log | tail -1
echo "$(date +%T) risk agent 5-mini"; .venv/bin/python run_pit_riskagent.py --models gpt-5-mini --reviewer gpt-4o-mini --workers 32 2>&1 | grep -v -i warn | tail -1
echo "$(date +%T) EXTENSION DONE"
