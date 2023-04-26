#!/bin/bash
set -e
source /home/testkoch/spproxhealthmonitor/venv/bin/activate
python -u /home/testkoch/spproxhealthmonitor/monitor_jobs.py
