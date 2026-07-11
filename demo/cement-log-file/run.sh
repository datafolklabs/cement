#!/usr/bin/env bash
#
# Demonstrates CEMENT_FRAMEWORK_LOG_FILE (issue #593): route Cement's internal
# framework/extension debug output to a file, in addition to the console.
#
set -euo pipefail
cd "$(dirname "$0")"

LOG_FILE="./framework.log"
rm -f "$LOG_FILE"

echo "==> CEMENT_LOG=1 enables framework logging (console)."
echo "==> CEMENT_FRAMEWORK_LOG_FILE also routes it to: $LOG_FILE"
echo "-------------------------------------------------------------"
CEMENT_LOG=1 CEMENT_FRAMEWORK_LOG_FILE="$LOG_FILE" python app.py

echo
echo "==> Contents of $LOG_FILE (last 5 framework log lines):"
echo "-------------------------------------------------------------"
tail -n 5 "$LOG_FILE"

echo
echo "==> Same framework output is now on BOTH the console (above) and the file."
