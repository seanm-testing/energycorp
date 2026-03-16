#!/usr/bin/env bash
# Hook: track-changed-files (PostToolUse for Edit|Write)
# Records file paths modified by Claude to a temp file.
# Stop hooks read this file instead of git diff to detect per-response changes.

set -euo pipefail

TRACKER_FILE="/tmp/claude-hooks/changed-files.txt"
SNAPSHOT_DIR="/tmp/claude-hooks/snapshots"
DEBUG_LOG="/tmp/claude-hooks/tracker-debug.log"
mkdir -p /tmp/claude-hooks "$SNAPSHOT_DIR"

INPUT=$(cat)

echo "--- $(date) ---" >> "$DEBUG_LOG"
echo "RAW INPUT: $INPUT" >> "$DEBUG_LOG"

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

echo "EXTRACTED FILE_PATH: $FILE_PATH" >> "$DEBUG_LOG"

if [ -n "$FILE_PATH" ]; then
  echo "$FILE_PATH" >> "$TRACKER_FILE"
  echo "TRACKED: $FILE_PATH" >> "$DEBUG_LOG"

  # Save a snapshot for /learn-fix diffing (Claude's version of the file)
  if [ -f "$FILE_PATH" ]; then
    SAFE_NAME=$(echo "$FILE_PATH" | sed 's|^/||' | sed 's|/|__|g')
    cp "$FILE_PATH" "$SNAPSHOT_DIR/$SAFE_NAME"
    echo "SNAPSHOT: $SNAPSHOT_DIR/$SAFE_NAME" >> "$DEBUG_LOG"
  fi
else
  echo "NO FILE_PATH FOUND" >> "$DEBUG_LOG"
fi
