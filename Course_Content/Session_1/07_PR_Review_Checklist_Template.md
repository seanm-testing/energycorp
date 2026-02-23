# PR Review Checklist Template for Claude-Generated Code

Use this checklist when reviewing pull requests that contain code generated or modified by Claude Code. Copy the relevant sections into your PR description or use as a reviewer guide.

---

## Quick Checklist (Copy into PR Description)

```markdown
## Review Checklist

### Correctness
- [ ] All imports exist in installed package versions
- [ ] API endpoints referenced in frontend exist in backend urls.py
- [ ] Model fields and properties match the actual schema
- [ ] No invented methods, mixins, or classes from external packages
- [ ] Framework APIs match the project's framework version

### Code Quality
- [ ] Follows existing project patterns and conventions
- [ ] No unnecessary changes to files outside the scope of the PR
- [ ] No hardcoded values that should be configuration or constants
- [ ] Edge cases handled (null, empty, invalid input)
- [ ] No duplicated logic that already exists in the codebase

### Testing
- [ ] Existing tests still pass
- [ ] New tests cover the added/changed functionality
- [ ] Tests verify at least one happy path and one failure case
- [ ] Test assertions are meaningful (not just "doesn't throw")

### Security
- [ ] No secrets, API keys, or credentials in committed code
- [ ] Input validation present at system boundaries
- [ ] No SQL injection, XSS, or command injection vectors
- [ ] Authentication/authorization checks in place for new endpoints

### Integration
- [ ] Database migrations are correct and reversible (if applicable)
- [ ] API contract changes are reflected in both backend and frontend
- [ ] No breaking changes to existing interfaces without migration plan
- [ ] Documentation updated if behavior changes
```

---

## Extended Checklist for Detailed Reviews

### Django / Backend Specific

```markdown
### Backend Review
- [ ] Model changes have corresponding migrations
- [ ] Serializer fields match model fields (names, types, read-only status)
- [ ] ViewSet/View permissions are set correctly (AllowAdmin, AllowManager, etc.)
- [ ] QuerySets are filtered appropriately (no unscoped `.all()` in user-facing views)
- [ ] ForeignKey `on_delete` behavior is intentional
- [ ] New URL patterns don't conflict with existing ones
- [ ] Admin registration updated if new models are added
```

### React / Frontend Specific

```markdown
### Frontend Review
- [ ] Components use hooks/patterns consistent with the project's React version
- [ ] API calls use correct endpoints (verified against backend urls.py)
- [ ] Error states are handled (loading, error, empty data)
- [ ] State management follows project patterns (Redux, Context, etc.)
- [ ] No direct DOM manipulation (use React patterns)
- [ ] Translations/i18n keys added if user-facing strings are introduced
- [ ] Component is used in a route or parent component (not orphaned)
```

---

## How to Use This Template

### For PR Authors (using Claude Code)

1. After Claude creates the PR, **add the Quick Checklist** to the PR description
2. Go through each item yourself before requesting review
3. Check the items you've verified; leave unchecked items for the reviewer
4. Add a note for any items that don't apply: `- [x] N/A — no new endpoints`

### For PR Reviewers

1. Start with the **Correctness** section — these catch Claude's most common errors
2. Pay special attention to:
   - **Imports** — Claude frequently invents packages or uses wrong versions
   - **API endpoints** — Claude may reference endpoints that don't exist
   - **Framework version** — Claude defaults to patterns from newer versions
3. Use the Extended Checklist for larger PRs or PRs touching critical paths
4. If you find a hallucination, add it to the team's CLAUDE.md as a constraint

### For the Team (continuous improvement)

After each sprint or review cycle:
- Collect common Claude mistakes from PR reviews
- Add preventive constraints to CLAUDE.md
- Update `.claude/settings.json` deny rules if Claude keeps trying risky operations
- Share useful prompts that produced good results

---

## Common Claude Mistakes to Watch For

| Category | What to Look For | Example |
|----------|-----------------|---------|
| Phantom imports | Imports from packages not in your dependencies | `from rest_framework.mixins import BulkCreateMixin` |
| Version mismatch | Uses APIs from newer framework versions | `useActionState` (React 19) in a React 16 project |
| Invented endpoints | Frontend calls API endpoints that don't exist | `axios.get('/api/users/permissions/')` |
| Wrong relationships | Misunderstands model relationships | Direct `Client → Invoice` instead of `Client → Contract → Invoice` |
| Over-engineering | Adds abstraction layers not asked for | Creating a utility class for a one-time operation |
| Missing edge cases | Happy path only, no null/error handling | Property crashes on `None` foreign key |
| Scope creep | Modifies files outside the task scope | "While I was there, I also refactored..." |

---

## PR Description Template

Use this as a complete PR description template for Claude-assisted work:

```markdown
## Summary

[1-3 sentences: what was changed and why]

## Changes

- [File 1]: [what changed]
- [File 2]: [what changed]
- [File 3]: [what changed]

## How it was built

- [x] Planned in Claude Code Plan Mode
- [x] Implemented with Claude Code
- [x] Reviewed diffs manually before committing
- [x] Tests pass

## Testing

- [Describe how this was tested]
- [Include test commands run]

## Review Checklist

- [ ] Imports are real and version-compatible
- [ ] API endpoints exist in the backend
- [ ] Model changes have migrations (if applicable)
- [ ] Edge cases handled
- [ ] No scope creep — only requested changes
- [ ] Existing tests pass
- [ ] New functionality has test coverage
```
