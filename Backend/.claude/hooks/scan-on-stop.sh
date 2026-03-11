#!/usr/bin/env bash
# Hook: scan-on-stop
# Triggers security-scanner agent when security-relevant files were modified.
# Only fires once per session — uses stop_hook_active + session_id flag.

set -euo pipefail

DEBUG_LOG="/tmp/claude-hooks/scan-debug.log"
mkdir -p /tmp/claude-hooks

# Read hook input from stdin
INPUT=$(cat)

echo "--- $(date) ---" >> "$DEBUG_LOG"
echo "stop_hook_active: $(echo "$INPUT" | jq -r '.stop_hook_active')" >> "$DEBUG_LOG"
echo "session_id: $(echo "$INPUT" | jq -r '.session_id')" >> "$DEBUG_LOG"

# If Claude is already continuing from a prior stop hook, approve immediately
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  echo "APPROVED: stop_hook_active=true" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
  exit 0
fi

# Use session_id to ensure this hook only fires once per conversation
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
FLAG_FILE="/tmp/claude-hooks/scan-${SESSION_ID}.fired"

echo "FLAG_FILE: $FLAG_FILE" >> "$DEBUG_LOG"
echo "FLAG_EXISTS: $([ -f "$FLAG_FILE" ] && echo yes || echo no)" >> "$DEBUG_LOG"

if [ -f "$FLAG_FILE" ]; then
  echo "APPROVED: flag file exists" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
  exit 0
fi

# Get modified files relative to HEAD
changed_files=$(git diff --name-only HEAD 2>/dev/null || true)

# Filter for .py files and dependency/config files
security_files=$(echo "$changed_files" | grep -E '\.(py)$|requirements\.txt|package\.json|\.env|settings\.py|docker-compose' || true)

if [ -n "$security_files" ]; then
  # Mark as fired for this session
  touch "$FLAG_FILE"
  echo "BLOCKED: created flag, found files" >> "$DEBUG_LOG"

  # Format file list as comma-separated string
  file_list=$(echo "$security_files" | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')
  cat <<EOF
{"decision": "block", "reason": "Security-relevant changes detected in: ${file_list}. Use the security-scanner agent to run pip-audit, Django deployment checks, and secret scanning on the affected areas."}
EOF
else
  echo "APPROVED: no matching files" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
fi

exit 0
