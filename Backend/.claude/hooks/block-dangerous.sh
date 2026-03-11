#!/bin/bash
# block-dangerous.sh — PreToolUse hook that blocks dangerous Bash commands
# Reads JSON on stdin, checks the command against a blocklist,
# returns hookSpecificOutput to deny if dangerous

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# If this isn't a command (e.g., it's an Edit call), allow it
if [ -z "$COMMAND" ]; then
  exit 0
fi

# Check for dangerous patterns
BLOCKED=false
REASON=""

if echo "$COMMAND" | grep -qE 'rm\s+-rf'; then
  BLOCKED=true
  REASON="Destructive command: rm -rf is blocked by project policy"
elif echo "$COMMAND" | grep -qi 'DROP\s*TABLE'; then
  BLOCKED=true
  REASON="SQL injection risk: DROP TABLE is blocked by project policy"
elif echo "$COMMAND" | grep -qE '\.env'; then
  BLOCKED=true
  REASON="Security: accessing .env files is blocked by project policy"
elif echo "$COMMAND" | grep -qE '\-\-force\s+push|push\s+.*\-\-force'; then
  BLOCKED=true
  REASON="Safety: force push is blocked by project policy"
elif echo "$COMMAND" | grep -qE 'manage\.py\s+(migrate|flush|dbshell)'; then
  BLOCKED=true
  REASON="Database safety: destructive manage.py commands are blocked by project policy"
fi

if [ "$BLOCKED" = true ]; then
  # Return hookSpecificOutput for PreToolUse (not top-level decision)
  jq -n --arg reason "$REASON" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
else
  exit 0
fi