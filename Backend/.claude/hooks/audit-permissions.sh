#!/bin/bash
# audit-permission.sh — PostToolUse hook
# Logs all tool calls to an audit file

INPUT=$(cat)

# Extract fields using jq
TOOL=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.file_path // "N/A"')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Append to audit log
echo "$TIMESTAMP | Tool: $TOOL | Action: $COMMAND" >> "$CLAUDE_PROJECT_DIR/.claude/logs/permission-audit.log"

# Allow the permission request to proceed normally
exit 0