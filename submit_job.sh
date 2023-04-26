#!/bin/bash
set -e
source /home/testkoch/spproxhealthmonitor/venv/bin/activate
python -u /home/testkoch/spproxhealthmonitor/spproxhealthmonitor2.py
#pm2 start spproxhealthmonitor2.py  --name pipeline-monitor
