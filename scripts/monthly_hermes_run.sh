#!/bin/bash
# monthly_hermes_run.sh - scheduled cron entrypoint for MarkusOS monthly PR loop

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR" || exit 1

# Execute using project virtualenv Python
echo "Running monthly Hermes review loop..."
.venv/bin/python scripts/monthly_hermes_run.py
echo "Monthly Hermes review loop finished."
