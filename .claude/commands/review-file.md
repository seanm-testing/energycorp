---
description: Focused code review for a specific file
argument-hint: <file-path>
allowed-tools: Read, Grep, Glob
---
Perform a focused code review of @$ARGUMENTS.

Check for:
1. Import errors — are all imported modules actually installed?
2. Security issues — unvalidated input, missing permission checks
3. Error handling — are exceptions caught appropriately?
4. Project patterns — does the code follow patterns from our CLAUDE.md?

Present findings as a numbered list with severity (HIGH / MEDIUM / LOW).
If no issues found, say so explicitly.
