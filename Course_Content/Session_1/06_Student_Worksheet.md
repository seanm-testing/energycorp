# Student Worksheet: Getting Started with Claude Code

**Duration:** 25-35 minutes (independent work)
**Goal:** Set up Claude Code for your project, create a CLAUDE.md, implement a small change, and submit a PR with a review checklist.

---

## Exercise 1: Setup & Verification (3 min)

### 1.1 Verify Installation

Open your terminal and run:

```bash
claude --version
```

If you see a version number, skip to 1.2. If not, install:

```bash
npm install -g @anthropic-ai/claude-code
```

Then run `claude` and follow the authentication prompts.

### 1.2 Navigate to Your Project

```bash
cd /path/to/your/project
```

### 1.3 Launch Claude Code

```bash
claude
```

Verify Claude detects your project. Ask it:

```
What can you tell me about this project from looking at the file structure?
```

Write down what Claude gets right and what it gets wrong:

| Correct | Incorrect or Missing |
|---------|---------------------|
| | |
| | |
| | |

> The incorrect/missing items tell you what your CLAUDE.md needs to cover.

---

## Exercise 2: Create Your CLAUDE.md (8-10 min)

### 2.1 Start with a Template

Create a file called `CLAUDE.md` in your project root. Use this structure as a starting point:

```markdown
# CLAUDE.md

## Project Overview

[One to two sentences: what is this project, what does it do, who uses it]

## Tech Stack

- Backend: [framework, version, language]
- Frontend: [framework, version, language]
- Database: [database, local vs production differences]
- Key libraries: [list 3-5 most important dependencies]

## Build & Run Commands

### Backend

```bash
[exact command to install dependencies]
[exact command to run dev server]
[exact command to run tests]
[exact command to run linter, if applicable]
[exact command to create/apply migrations]
```

### Frontend

```bash
[exact command to install dependencies]
[exact command to run dev server]
[exact command to run tests]
[exact command to build for production]
```

## Architecture

### Backend

[Describe your app structure: what are the main modules/apps, what does each one do, what are the API prefixes]

### Frontend

[Describe your component structure: routing, state management, key patterns]

## Key Model Relationships

[Describe the main data model chain(s). Example: User → Order → OrderItem → Product]

## Important Constraints

- [Anything Claude should NOT do or assume]
- [Version-specific limitations]
- [Team conventions that aren't obvious from the code]
```

### 2.2 Fill In the Template

Use your knowledge of the project to fill in each section. Aim for **50-80 lines total**.

**Tips:**
- Be specific: `Django 4.2` not just `Django`
- Use exact commands: `python manage.py test apps/` not `run the tests`
- Include your actual app/module names and their responsibilities
- List the 2-3 most important model relationships

### 2.3 Verify with Claude

Save your CLAUDE.md, then restart Claude Code (exit and re-launch `claude`). Ask:

```
What does the CLAUDE.md tell you about this project? Is there anything you'd
recommend adding to make it more useful?
```

Claude may suggest additions. Add any that make sense, but remember: lean is better than comprehensive. Only add what will prevent real mistakes.

**Self-check — Your CLAUDE.md should answer these questions:**
- [ ] What does this project do? (1-2 sentences)
- [ ] What's the tech stack? (with versions)
- [ ] How do I run the tests? (exact command)
- [ ] How is the code organized? (app/module structure)
- [ ] How do the main models relate to each other?

---

## Exercise 3: Configure settings.json (3 min)

### 3.1 Create the Settings Directory

```bash
mkdir -p .claude
```

### 3.2 Create Project Settings

Create `.claude/settings.json` with appropriate permissions for your project. Adapt this template:

```json
{
  "permissions": {
    "allow": [
      "Bash([your test command here])",
      "Bash([your lint command here])",
      "Bash([your build command here])"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(*DROP TABLE*)",
      "Bash(*--force*)",
      "Bash(*manage.py flush*)"
    ]
  }
}
```

**Replace the bracketed items** with your actual commands. For example:
- `"Bash(python manage.py test)"` — allow running Django tests
- `"Bash(npm test)"` — allow running frontend tests
- `"Bash(npx eslint .)"` — allow running the linter

### 3.3 (Optional) Create Local Settings

If you want personal overrides, create `.claude/settings.local.json`:

```json
{
  "model": "sonnet"
}
```

Add `.claude/settings.local.json` to your `.gitignore` if it's not already there.

---

## Exercise 4: Implement a Small Change (10-12 min)

### 4.1 Choose Your Change

Pick ONE of the following (or propose your own — something small and self-contained):

**Backend options:**
- Add a new read-only field or property to an existing model
- Add a new serializer field that computes a value from existing data
- Add a new filter or search parameter to an existing API endpoint
- Write a utility function for a common operation in your codebase

**Frontend options:**
- Add a display component that formats existing data in a new way
- Add a new column to an existing table/list view
- Create a small reusable component (e.g., a status badge, formatted date display)
- Add a loading state to a component that doesn't have one

**Write down your chosen change here:**

> I will: _______________________________________________________________
>
> Files likely affected: _________________________________________________

### 4.2 Plan First

Enter Plan Mode: press `Shift+Tab` twice (or type `/plan`).

Ask Claude to plan your change:

```
Plan how to [describe your change]. Tell me which files need to change
and in what order.
```

**Review the plan. Verify:**
- [ ] Does it reference real files in your project?
- [ ] Does the order of operations make sense?
- [ ] Does it mention running tests?
- [ ] Does it avoid unnecessary changes?

### 4.3 Implement

Switch to Normal Mode: press `Shift+Tab` once.

Ask Claude to implement:

```
Implement the plan: [brief description of the change]
```

### 4.4 Review the Code

Before accepting, check:
- [ ] Are all imports real? (No phantom packages or methods)
- [ ] Does the code match your project's patterns? (Naming conventions, file organization)
- [ ] Are there any hardcoded values that should be configurable?
- [ ] Does it handle edge cases? (null values, empty strings, etc.)

---

## Exercise 5: Validate (3 min)

### 5.1 Run Tests

Ask Claude:

```
Run the tests to verify nothing is broken.
```

Or run them yourself:

```bash
[your test command]
```

**Test results:**
- [ ] All tests pass
- [ ] If tests fail, I gave Claude the error and it fixed the issue
- [ ] If it took more than 2 corrections, I used `/clear` and started fresh

### 5.2 Manual Review

Check the diff manually:

```bash
git diff
```

Verify:
- [ ] Only the intended files were changed
- [ ] No unrelated changes snuck in
- [ ] The code does what was requested

---

## Exercise 6: Create a PR with Review Checklist (5 min)

### 6.1 Create the PR

Ask Claude:

```
Create a new branch called "feature/[short-description]", commit the changes,
and create a PR. Include a summary and a review checklist for the reviewer.
```

If Claude can't create a PR directly (e.g., no GitHub CLI), do it manually:

```bash
git checkout -b feature/[short-description]
git add [changed files]
git commit -m "Add [description of change]"
git push -u origin feature/[short-description]
```

Then create the PR through your platform's web interface.

### 6.2 Add the Review Checklist

If Claude didn't generate one, add this checklist to your PR description (adapt as needed):

```markdown
## Review Checklist

### Code Quality
- [ ] All imports reference real, installed packages
- [ ] Code follows project naming conventions
- [ ] No hardcoded values that should be constants or config
- [ ] Edge cases handled (null, empty, unexpected input)

### Testing
- [ ] Existing tests still pass
- [ ] New functionality has test coverage (or justification for skipping)
- [ ] Tests cover happy path and at least one error case

### Integration
- [ ] Changes are backward compatible
- [ ] API changes are reflected in serializers
- [ ] Frontend changes match backend data contracts
- [ ] No unnecessary files modified

### Claude-Specific Checks
- [ ] No hallucinated imports or API calls
- [ ] Code matches the project's framework version
- [ ] Generated code doesn't duplicate existing utilities
- [ ] Review the full diff, not just Claude's summary
```

### 6.3 Record Your PR

**PR URL:** ____________________________________________________________

**Branch name:** ________________________________________________________

**What was changed:** ___________________________________________________

---

## Self-Assessment

Answer these questions honestly. They're for your own learning — not graded.

### Understanding

1. What is the purpose of CLAUDE.md?

> Your answer: ___________________________________________________________

2. What are the five tiers of settings.json, from highest to lowest priority?

> Your answer: ___________________________________________________________

3. Why should you use Plan Mode before implementing a non-trivial change?

> Your answer: ___________________________________________________________

### Experience

4. Did Claude hallucinate anything during your session? If so, what?

> Your answer: ___________________________________________________________

5. Did you hit the Correction Spiral? What did you do?

> Your answer: ___________________________________________________________

6. What's one thing you'd add to your CLAUDE.md based on today's experience?

> Your answer: ___________________________________________________________

### Confidence

Rate your comfort level (1 = not comfortable, 5 = very comfortable):

| Skill | Rating (1-5) |
|-------|:------------:|
| Launching and using Claude Code CLI | |
| Writing a useful CLAUDE.md | |
| Using Plan Mode before implementing | |
| Recognizing hallucinations | |
| Creating a PR with Claude's help | |
| Knowing when to `/clear` and start fresh | |

---

## What to Bring to Session 2

- Your CLAUDE.md (we'll review and improve them)
- Notes on any Claude mistakes or frustrations you encountered
- One question about Claude Code you want answered

---

## Quick Reference

| Action | How |
|--------|-----|
| Launch Claude Code | `claude` in your project directory |
| Switch to Plan Mode | `Shift+Tab` twice, or `/plan` |
| Switch to Normal Mode | `Shift+Tab` |
| Compress context | `/compact` |
| Clear session | `/clear` |
| Reference a file | `@path/to/file` |
| Switch model | `/model` |
| Get help | `/help` |
