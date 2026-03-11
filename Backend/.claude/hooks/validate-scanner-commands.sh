#!/usr/bin/env bash
# PreToolUse hook for security-scanner agent: restricts Bash commands
# to an allowlist of safe scanning tools.

set -euo pipefail

# Read JSON from stdin
input=$(cat)

# Extract the command field from tool_input
command=$(python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" <<< "$input" 2>/dev/null) || command=""

# Allowlist patterns (anchored to the first token / common pipe components)
ALLOWED_PATTERNS=(
  'pip-audit'
  'pip3-audit'
  'manage\.py check'
  'git ls-files'
  '\bgrep\b'
  '\brg\b'
  '\bruff\b'
  '\btail\b'
  '\bhead\b'
  'cd'
)

# Check command against each allowed pattern
for pattern in "${ALLOWED_PATTERNS[@]}"; do
  if echo "$command" | grep -qE "$pattern"; then
    echo '{"hookSpecificOutput": {"permissionDecision": "allow"}}'
    exit 0
  fi
done

# Command did not match any allowed pattern — deny
reason="Security scanner restricted to: pip-audit, manage.py check, git ls-files, grep, ruff. Attempted: ${command}"
# Escape the reason string for valid JSON
reason_escaped=$(python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" <<< "$reason" 2>/dev/null) || reason_escaped="\"${reason}\""

cat <<EOF
{"hookSpecificOutput": {"permissionDecision": "deny", "reason": ${reason_escaped}}}
EOF

exit 0
