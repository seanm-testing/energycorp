#!/bin/bash
# validate-prompt.sh — UserPromptSubmit hook
# Warns about dangerous keywords without blocking

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty')

WARNING=""

if echo "$PROMPT" | grep -qi 'production'; then
  WARNING="WARNING: Your prompt mentions 'production'. Ensure you're working in a development environment."
elif echo "$PROMPT" | grep -qi 'deploy'; then
  WARNING="WARNING: Your prompt mentions 'deploy'. Claude Code should not be used for production deployments."
elif echo "$PROMPT" | grep -qi 'delete all'; then
  WARNING="WARNING: Your prompt mentions 'delete all'. This is a potentially destructive operation."
elif echo "$PROMPT" | grep -qi 'drop table'; then
  WARNING="WARNING: Your prompt mentions 'drop table'. Database schema changes should go through migrations."
fi

if [ -n "$WARNING" ]; then
  # For UserPromptSubmit, stdout text is added to Claude's context
  echo "$WARNING"
fi

exit 0