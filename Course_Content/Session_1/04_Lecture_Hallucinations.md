# Lecture: Hallucinations & Safe Usage Patterns

**Duration:** 15 minutes
**Goal:** Teach students what hallucinations are, why they happen, and practical techniques to prevent and detect them.

---

## What Are Hallucinations?

A hallucination is when Claude generates output that is **plausible-looking but factually incorrect**. It's not a bug — it's a fundamental property of how language models work.

Claude doesn't "know" things the way a database does. It predicts what reasonable text looks like based on patterns. When the pattern-matching goes wrong, you get confident, detailed, *wrong* answers.

### Why Do They Happen?

**1. Training data patterns override project reality**
Claude has seen thousands of Django projects. If most of them use a certain mixin or pattern, Claude may assume yours does too — even when it doesn't.

**2. Ambiguity in context**
When your prompt is vague or your CLAUDE.md is thin, Claude fills in the gaps with its best guess. Sometimes the guess is wrong.

**3. Context window limits**
As conversations grow long, earlier details get compressed. Claude may "forget" constraints you mentioned 30 messages ago and generate code that contradicts them.

**4. Confidence without calibration**
Claude doesn't say "I'm 60% sure about this." It presents everything with the same level of confidence, whether it's reading a file it just loaded or guessing about a method signature it's never seen.

---

## Real Examples Relevant to Django + React

### Example 1: The Phantom Import (Django)

You ask Claude to add a custom permission class. It generates:

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.mixins import BulkCreateModelMixin  # <-- Does not exist in DRF

class BulkCreateView(BulkCreateModelMixin, generics.CreateAPIView):
    ...
```

**What happened:** Claude has seen `BulkCreateModelMixin` in third-party packages (like `djangorestframework-bulk`) and assumed it's part of core DRF. It isn't. The import will fail at runtime.

**How to catch it:** Run the code. The `ImportError` is immediate. Better: have a test that imports the module.

### Example 2: The Wrong React Hook Pattern (React)

You ask Claude to add state management to a component. It generates:

```jsx
import { useActionState } from 'react';  // <-- React 19+ only

function PaymentForm() {
  const [state, formAction] = useActionState(submitPayment, initialState);
  ...
}
```

**What happened:** Your project uses React 16. Claude generated code using a React 19 API because it's the pattern it's seen most recently in training data. The hook doesn't exist in your version.

**How to catch it:** The build will fail. Better: your CLAUDE.md should specify `React 16` explicitly so Claude knows the version constraint.

### Example 3: The Invented API Endpoint

You ask Claude to add a frontend feature that calls the backend. It generates:

```javascript
const response = await axios.get('/api/user/permissions/', {
  headers: { Authorization: `Token ${token}` }
});
```

**What happened:** There is no `/api/user/permissions/` endpoint. Claude inferred it from the project's URL pattern (`/api/user/`, `/api/user/login/`) and invented a plausible-looking endpoint. The request will 404.

**How to catch it:** Check `Backend/src/users/urls.py`. Better: have Claude verify the endpoint exists before generating frontend code that calls it.

---

## The Correction Spiral Anti-Pattern

This is the most important anti-pattern for new Claude Code users.

### How It Happens

1. You ask Claude to implement a feature
2. The output has a bug. You say: "That's wrong, fix the import"
3. Claude fixes the import but introduces a different issue
4. You correct that. Claude changes something else
5. After 3-4 rounds, Claude's context is polluted with failed attempts, contradictions, and confusion
6. The quality of responses degrades rapidly
7. You spend more time correcting Claude than you would have spent writing the code yourself

### The Fix

**If you've corrected Claude more than twice on the same issue, stop.**

Run `/clear` and start a fresh session with a better prompt. A clean session with a well-crafted prompt almost always outperforms an accumulated series of corrections.

> Think of it like this: if you're giving someone driving directions and they keep making wrong turns, at some point it's better to say "go back to the start" than to keep course-correcting.

### Why This Happens

Each correction adds context. Claude tries to satisfy *all* the context — your original request, the first correction, the second correction — even when they're subtly contradictory. The model gets pulled in multiple directions and produces increasingly compromised output.

---

## Context Degradation in Long Sessions

Claude has a context window — a finite amount of "memory" for the current conversation.

### What Happens as Context Fills Up

| Context Level | Behavior |
|---------------|----------|
| Fresh (0-30%) | Best performance — Claude has full attention on your task |
| Moderate (30-60%) | Still good, but may miss nuances from early in the conversation |
| Heavy (60-80%) | Auto-compaction kicks in — older messages get summarized |
| Full (80%+) | Earlier details are significantly compressed; quality degrades noticeably |

### Signs of Context Degradation

- Claude "forgets" constraints you specified earlier
- It re-suggests approaches you already rejected
- Code quality drops — more boilerplate, less project-specific awareness
- It starts asking questions you already answered

### What to Do

- **`/compact`** — Manually compress the context with an optional focus topic. Example: `/compact focus on the Invoice model changes`
- **`/clear`** — Full reset. Start fresh. Best when the task has fundamentally changed.
- **Plan your sessions** — Don't try to do everything in one conversation. Break large tasks into focused sessions.
- **Use sub-agents** — Delegate research to sub-agents so the main context stays clean for implementation.

---

## How to Prevent Hallucinations

### 1. Write a Good CLAUDE.md

The single highest-leverage thing you can do. Specify:
- Exact framework versions (`Django 3.0.3`, `React 16.13`)
- Your actual project structure (don't let Claude guess)
- Available endpoints (or tell Claude how to find them)
- Known constraints ("We don't use class-based views in the frontend")

### 2. Use Plan Mode First

For any non-trivial change:
1. Start in Plan Mode (Shift+Tab twice)
2. Ask Claude to plan the change
3. Review the plan — does it reference real files? Real APIs? Real patterns?
4. Only then switch to Normal Mode to implement

### 3. Test-Driven Development

> "Include tests, screenshots, or expected outputs so Claude can check itself. This is the **single highest-leverage thing** you can do." — Anthropic documentation

The workflow:
1. Write (or have Claude write) the test first
2. Run the test — it should fail (the feature doesn't exist yet)
3. Have Claude implement the feature
4. Run the test — it should pass
5. If it doesn't pass, give Claude the error output

Tests are *mechanically verifiable*. They don't rely on you reading every line.

### 4. Verify Against the Source

When Claude references a file, API, or import:
- Did it read the file, or is it guessing?
- Does the import actually exist in your installed version?
- Does the endpoint exist in your urls.py?

A 30-second check can save 30 minutes of debugging.

### 5. Keep Prompts Clear and Scoped

Bad: "Make the payment system better"
Good: "Add a `payment_date` field to the Payment model in `payments/models.py`, update the serializer, and write a test"

Scoped prompts give Claude less room to guess and more room to be precise.

### 6. Compact or Restart for Long Sessions

If you've been working for 30+ minutes on a complex task:
- Run `/compact` to compress context
- Or `/clear` to start fresh with a clean prompt
- Don't push through degraded quality

---

## Summary: The Safe Usage Workflow

```
1. PLAN    → Start in Plan Mode. Let Claude read and propose.
2. REVIEW  → Check the plan. Does it reference real files and APIs?
3. TEST    → Write the test first (or have Claude write it).
4. BUILD   → Switch to Normal Mode. Let Claude implement.
5. VERIFY  → Run tests. Check diffs. Review imports.
6. COMMIT  → Only after verification passes.
```

**When things go wrong:**
- Corrected twice on the same issue? → `/clear`, better prompt
- Context feels degraded? → `/compact` or `/clear`
- Claude invents an API? → Make it verify by reading the actual file
- Build fails on import? → Check the installed version, specify in CLAUDE.md

> The goal isn't to never make mistakes — it's to catch them fast and have a system that prevents the same mistake twice.
