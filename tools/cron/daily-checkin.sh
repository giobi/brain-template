#!/bin/bash
# Daily Check-in Script - Runs Claude autonomously via OpenRouter API
# Usage: ./daily-checkin.sh

set -e

BRAIN_DIR="/home/claude/brain"
LOG_FILE="$BRAIN_DIR/log/cron-daily.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting daily check-in..." >> "$LOG_FILE"

cd "$BRAIN_DIR"

# Run Python script that uses OpenRouter API
python3 "$BRAIN_DIR/tools/cron/daily-checkin-api.py" 2>&1 | tee -a "$LOG_FILE"

echo "[$TIMESTAMP] Daily check-in completed" >> "$LOG_FILE"
