#!/bin/bash
echo "`date`: Starting cron service"
service cron start
tail -f /dev/null
