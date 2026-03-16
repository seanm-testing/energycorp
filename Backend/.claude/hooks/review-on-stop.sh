#!/usr/bin/env bash
# Hook: review-on-stop
# Triggers code-reviewer agent when .py or .jsx files were modified in this response.
# Reads from the tracker file written by track-changed-files.sh (PostToolUse hook),
# so it only sees files Claude actually edited — not pre-existing dirty files.
# Only fires once per session — uses stop_hook_active + session_id flag.

set -euo pipefail

TRACKER_FILE="/tmp/claude-hooks/changed-files.txt"
DEBUG_LOG="/tmp/claude-hooks/review-debug.log"
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
FLAG_FILE="/tmp/claude-hooks/review-${SESSION_ID}.fired"

echo "FLAG_FILE: $FLAG_FILE" >> "$DEBUG_LOG"
echo "FLAG_EXISTS: $([ -f "$FLAG_FILE" ] && echo yes || echo no)" >> "$DEBUG_LOG"

if [ -f "$FLAG_FILE" ]; then
  echo "APPROVED: flag file exists" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
  exit 0
fi

# Read files changed in this response from the tracker (written by PostToolUse hook)
if [ ! -f "$TRACKER_FILE" ] || [ ! -s "$TRACKER_FILE" ]; then
  echo "APPROVED: no files changed in this response" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
  exit 0
fi

changed_files=$(sort -u "$TRACKER_FILE")

# Skip if only .md files were changed
non_md_files=$(echo "$changed_files" | grep -v '\.md$' || true)
if [ -z "$non_md_files" ]; then
  echo "APPROVED: only .md files changed" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
  exit 0
fi

# Filter for .py and .jsx files only
code_files=$(echo "$changed_files" | grep -E '\.(py|jsx)$' || true)

if [ -n "$code_files" ]; then
  # Mark as fired for this session
  touch "$FLAG_FILE"
  echo "BLOCKED: created flag, found files" >> "$DEBUG_LOG"

  # Format file list as comma-separated string
  file_list=$(echo "$code_files" | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')
  cat <<EOF
{"decision": "block", "reason": "Code changes detected in: ${file_list}. Use the code-reviewer agent to review these files for permission classes, import validity, serializer consistency, and test coverage."}
EOF
else
  echo "APPROVED: no matching files" >> "$DEBUG_LOG"
  echo '{"decision": "approve"}'
fi

exit 0
