# Lab Guide: Instructor-Led Demo with energycorp

**Duration:** 20-25 minutes (instructor-led portion)
**Repo:** energycorp
**Goal:** Walk through the full Claude Code workflow as a group — setup, CLAUDE.md review, settings configuration, implement a change, validate, and create a PR.

---

## Prerequisites

Before starting, verify:
- [ ] Claude Code CLI is installed (`claude --version`)
- [ ] You have the energycorp repo cloned locally
- [ ] Git is configured (can create branches and commits)
- [ ] Terminal and VS Code are open

If Claude Code is not installed:
```bash
npm install -g @anthropic-ai/claude-code
```

Then authenticate:
```bash
claude
# Follow the login prompts
```

---

## Step 1: Load the Project (2 min)

Open your terminal and navigate to the energycorp directory:

```bash
cd /path/to/energycorp
```

Launch Claude Code:

```bash
claude
```

Claude will detect the git repository and read the CLAUDE.md file. You should see it initialize and become ready for input.

> **Instructor says:** "Claude has loaded our project. It read CLAUDE.md automatically. Let's verify — ask it what it knows."

Ask Claude:

```
What do you know about this project from the CLAUDE.md?
```

Claude should summarize the project: Django REST API backend, React SPA frontend, energy management system, role-based permissions, etc.

---

## Step 2: Review CLAUDE.md Together (5 min)

Open `CLAUDE.md` in your editor. Walk through it section by section.

### What makes this CLAUDE.md good:

**Project Overview (2 lines)**
```markdown
Energy Corporation Management System — a full-stack app for managing energy
distribution, billing, contracts, and customer services. Backend is a Django
REST API, frontend is a React SPA.
```
- Concise one-liner tells Claude what the project *does*
- Specifies the tech split (Django backend, React frontend)

**Build Commands (exact, copy-pasteable)**
```markdown
python src/manage.py runserver    # Start dev server
python src/manage.py test         # Run all tests
npm start                         # Start dev server
npm test                          # Run tests
```
- Claude uses these exact commands when it needs to build or test
- No ambiguity — these are the commands, not suggestions

**Architecture (structured, specific)**
- Lists every Django app with its API prefix
- Specifies the permission model (Type 1/2/3)
- Describes the DRF pattern: models → serializers → views → urls
- Notes the database (SQLite locally, PostgreSQL on Heroku)

**Key Model Relationships (the chain)**
```
Substation → Transformator → Counter → History
Client → Contract → Invoice → Payment
```
- This prevents Claude from guessing how models relate
- Without this, Claude might create a direct Client → Invoice relationship (skipping Contract)

### What could be improved:

- No linting commands — Claude doesn't know how to check code style
- No mention of React version (16) — could lead to hallucinations with newer React APIs
- No "don't do" section — no explicit constraints
- Could add: test file naming conventions, any CI requirements

> **Instructor says:** "A CLAUDE.md doesn't need to be perfect on day one. Start with the basics — project description, build commands, architecture — and iterate. Add things when Claude makes a mistake that a CLAUDE.md entry would have prevented."

---

## Step 3: Configure settings.json (3 min)

Create (or review) the project settings file:

```bash
mkdir -p .claude
```

> **Instructor says:** "Let's set up a project-level settings.json that the whole team can share."

Create `.claude/settings.json` with practical defaults:

```json
{
  "permissions": {
    "allow": [
      "Bash(python src/manage.py test)",
      "Bash(python src/manage.py makemigrations)",
      "Bash(python src/manage.py migrate)",
      "Bash(npm test)",
      "Bash(npm run build)"
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

> **Instructor says:** "The allow list lets Claude run tests and migrations without prompting you each time. The deny list prevents dangerous operations — even if Claude tries. Deny always beats allow."

**Optional:** Show the local settings override:

```json
// .claude/settings.local.json (personal, gitignored)
{
  "model": "opus"
}
```

> **Instructor says:** "Local settings are for personal preferences. Maybe you prefer Opus for its reasoning. Your teammates might prefer Sonnet for speed. Both are fine — local overrides project."

---

## Step 4: Implement a Change — Plan First (8 min)

### The Task

Add a `phone_display` read-only property to the `Client` model that formats the user's phone number for display.

### Step 4a: Enter Plan Mode

Press `Shift+Tab` twice to enter Plan Mode. Verify the mode indicator shows "Plan."

> **Instructor says:** "We're in Plan Mode. Claude can read everything but modify nothing. Let's ask it to plan."

### Step 4b: Ask Claude to Plan

```
Plan how you would add a read-only "phone_display" property to the Client model
in users/models.py. This property should return the associated user's phone
number formatted as "(XXX) XXX-XXXX". Include what files need to change and in
what order.
```

### Step 4c: Review the Plan

Claude should propose something like:
1. Add a `phone_display` property to the `Client` model in `Backend/src/users/models.py`
2. Add `phone_display` to the `ClientSerializer` in `Backend/src/users/serializers.py`
3. No migration needed (it's a property, not a database field)
4. Run existing tests to verify nothing breaks

> **Instructor says:** "Look at this plan. It identified the right files, the right order, and correctly noted that a property doesn't need a migration. This is why we plan first — we can verify the approach before any code is written."

### Step 4d: Switch to Normal Mode and Implement

Press `Shift+Tab` once to switch to Normal Mode (or Auto-Accept if you prefer).

```
Implement the plan: add the phone_display property to Client and expose it in
the serializer.
```

### Step 4e: Review the Changes

Claude will edit the files. Review the diffs:

**Expected in `users/models.py`:**
```python
@property
def phone_display(self):
    phone = self.user.phone
    if phone and len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    return phone or ""
```

**Expected in `users/serializers.py`:**
```python
# phone_display added to the serializer fields
```

> **Instructor says:** "Check the diff. Does the property reference `self.user.phone`? That's correct — Client has a ForeignKey to CustomUser, and phone is on CustomUser. If Claude had used `self.phone`, that would be a hallucination — Client doesn't have a phone field."

---

## Step 5: Validate the Change (3 min)

### Run Tests

Ask Claude to run the existing tests:

```
Run the Django tests to make sure nothing is broken.
```

Claude should run:
```bash
python src/manage.py test
```

> **Instructor says:** "Tests pass? Good. If they didn't, we'd give Claude the error output and let it fix the issue. Remember — if it takes more than two corrections, `/clear` and start fresh."

### Manual Verification

Quick sanity checks:
- Does the property handle `None` phone numbers? (Check the code)
- Is the serializer field read-only? (Check if it's in `read_only_fields` or uses `SerializerMethodField`)
- Does the formatting logic match what we asked for?

> **Instructor says:** "Automated tests catch functional regressions. Manual review catches logic issues and edge cases that tests don't cover. You need both."

---

## Step 6: Create a PR with Review Checklist (4 min)

### Create a Branch and PR

Ask Claude:

```
Create a new git branch called "feature/client-phone-display", commit the
changes, and create a PR. Include a summary of what changed and a review
checklist for the reviewer.
```

Claude should:
1. Create the branch
2. Stage the changed files
3. Commit with a descriptive message
4. Push the branch
5. Create a PR with a body that includes a summary and checklist

### Review the PR

Open the PR link Claude provides. Check that it includes:

**Summary:**
- What was added and why
- Which files were modified

**Review checklist (something like):**
- [ ] Property handles None/empty phone gracefully
- [ ] No migration needed (confirmed: property, not field)
- [ ] Serializer correctly exposes read-only field
- [ ] Existing tests still pass
- [ ] Phone formatting matches expected pattern

> **Instructor says:** "This is the deliverable for today's session. A PR with a Claude-generated change and a review checklist. The checklist isn't just for show — it's how you systematically verify Claude's work. We'll give you a reusable template for this."

---

## Recap

What we did in this lab:

| Step | What | Why |
|------|------|-----|
| Load project | `claude` in the project directory | Claude reads CLAUDE.md, understands the project |
| Review CLAUDE.md | Read it together, identified strengths and gaps | A good CLAUDE.md prevents hallucinations |
| Configure settings | Created `.claude/settings.json` | Consistent team config, safe permission boundaries |
| Plan first | Used Plan Mode before implementing | Verify the approach before writing code |
| Implement | Switched to Normal Mode, let Claude build | Claude generates code against the reviewed plan |
| Validate | Ran tests + manual review | Catch regressions and logic errors |
| Create PR | Branch, commit, PR with checklist | The deliverable — reviewable, traceable, verifiable |

> **Instructor says:** "Now it's your turn. Switch to your BulkSource project and follow the student worksheet. You're doing the same steps we just did, but on your own codebase."
