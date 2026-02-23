# Presentation: What is Claude?

**Duration:** 15-20 minutes
**Format:** Slide-by-slide content for the instructor to present. Each section below represents one slide or a small group of related slides.

---

## Slide 1: Title

**Claude Code: AI-Powered Software Engineering**

Session 1 — Introduction & Safe Usage Patterns

---

## Slide 2: What is Claude?

Claude is Anthropic's family of large language models built with a focus on safety and helpfulness.

**Key distinction:** Claude is not a search engine, not a database, and not a compiler. It's a *reasoning engine* that predicts what good code looks like based on patterns learned from training data.

**What this means for you:**
- It can write code, explain code, refactor code, and debug code
- It doesn't "know" your project — it reads it fresh each session (without explicit memory configuration)
- It can be wrong, and it will be confident about it

> **Speaker note:** Emphasize the "reads it fresh each session" point. This is the single biggest misconception new users have — they think Claude remembers previous sessions. It doesn't (without explicit memory configuration).

---

## Slide 3: The Claude Model Family

| Model | Strengths | Best For | Relative Cost |
|-------|-----------|----------|---------------|
| **Opus** | Deep reasoning, complex analysis, nuanced judgment | Architecture decisions, hard debugging, multi-file refactors | $$$ |
| **Sonnet** | Strong all-around performance, good speed | Daily coding tasks, code generation, reviews | $$ |
| **Haiku** | Fast, lightweight, cost-efficient | Quick lookups, simple questions, sub-agent tasks | $ |

**In Claude Code:**
- Sonnet is the default for most operations
- Haiku powers the Explore sub-agent (fast codebase searches)
- Opus is available for Plan Mode deep reasoning and complex tasks
- Switch models with `/model` or configure in settings

> **Speaker note:** Use the "gears" analogy — Haiku is first gear (quick starts), Sonnet is third gear (cruising), Opus is fifth gear (heavy lifting). You don't drive in fifth gear through a parking lot.

---

## Slide 4: Three Ways to Use Claude

### 1. Claude Chat (Web — claude.ai)
- Browser-based conversation interface
- Upload files, paste code, get explanations
- **No project access** — works with what you give it
- Best for: research, brainstorming, one-off questions

### 2. Claude Code (CLI — terminal)
- Runs in your terminal, inside your project directory
- Reads your filesystem, runs commands, creates/edits files
- Full agentic loop: reads → plans → implements → verifies
- Best for: real development work, CI/CD integration, automation

### 3. Claude Code (IDE — VS Code / JetBrains)
- Same engine as CLI, embedded in your editor
- Inline diffs with accept/reject buttons
- @ mentions from open files and selections
- Best for: interactive development, code review, pair programming

> **Speaker note:** Open each one briefly (you'll demo them in depth next). The goal here is just to establish the mental model of three interfaces to the same underlying capability.

---

## Slide 5: Claude Chat — When to Use It

**Use Claude Chat for:**
- Brainstorming new architecture approaches or other novel ideas
- Research: Use Claude's "Research Mode" to enable Deep Research on a specific topic
- Project Managers: Use Claude Chat for one-off document creation (Word, Powerpoint, Etc.)

**Don't use Claude Chat for:**
- Writing code that needs to integrate with your project (use Claude Code)
- Tasks that require reading multiple project files
- Explaining error messages or stack traces
- Anything that needs to run commands or tests

**Pro tip:** Claude Chat with Research Mode can search the web for up-to-date documentation. Useful when evaluating new dependencies.

---

## Slide 6: Claude Code — The Core Tool

Claude Code is an **agentic coding assistant** that runs in your terminal (or IDE) with access to your full project.

**What it can do:**
- Read and write files anywhere in your project
- Run shell commands (build, test, lint, deploy)
- Search your codebase (grep, glob, file patterns)
- Access the internet beyond web search (Private APIs/Authentication require MCP config)
- Create branches, commits, and PRs
- Spawn sub-agents for parallel work

**What it cannot do:**
- Remember previous sessions (without explicit memory config)
- Run indefinitely — it has a context window that fills up
- Guarantee correctness — it can and will make mistakes

> **Speaker note:** The "cannot" list is as important as the "can" list. Set honest expectations now to prevent frustration later.

---

## Slide 7: CLAUDE.md — Your Highest-Leverage File

CLAUDE.md is a Markdown file at your project root that Claude reads at the start of every conversation.

**Think of it as:** onboarding documentation for the AI, not for humans.

**What to include (~50-80 lines):**
- One-line project description
- Tech stack (exact versions matter)
- Build, test, and lint commands (exact commands Claude should run)
- Architecture overview (app structure, key patterns)
- Important relationships and gotchas
- What NOT to do (critical constraints)

**What NOT to include:**
- Generic instructions ("write clean code") — Claude already tries to
- Formatting rules — use linters instead
- Everything — keep it lean; ~150-200 total instructions is the reliable limit

**Hierarchy:** managed > command-line > local > project > user
(More specific always wins)

---

## Slide 8: The settings.json 5-Tier Hierarchy

Claude Code settings cascade across five scopes:

```
1. Managed    /etc/claude-code/                (IT-deployed, highest priority)
2. CLI        --settings flag on command line  (session only)
3. Local      .claude/settings.local.json      (personal, gitignored)
4. Project    .claude/settings.json            (shared, committed)
5. User       ~/.claude/settings.json          (personal, all projects)
```

**Key settings:**
- `permissions.allow` / `deny` — what Claude can run without asking
- `defaultMode` — start in plan/default/acceptEdits mode
- `model` — override the default model

**Rule:** Higher scopes always override lower ones. Deny always beats allow.

> **Speaker note:** For this team, the Project scope (.claude/settings.json committed to git) is the most important — it lets the team share consistent Claude Code configuration.

---

## Slide 9: Research Mode

**Available in Claude Chat (web)**

Research Mode tells Claude to search the web before answering, then cite its sources.

**When to use it:**
- Evaluating a new library ("What are the trade-offs of Django Ninja vs DRF?")
- Checking for recent breaking changes in a dependency
- Finding current best practices for a technology

**When NOT to use it:**
- Questions about your own codebase (Claude Chat can't see it)
- Simple coding tasks (it adds latency)

> **Speaker note:** Research Mode is a Claude Chat feature, not Claude Code. Mention it because students will encounter it and should know when it's appropriate.

---

## Slide 10: Extended Thinking

Claude can "think step by step" before answering, showing its reasoning process.

**How it works:**
- Claude generates internal reasoning tokens before the visible response
- Useful for complex logic, debugging, and architecture decisions
- In Claude Code: enable with `alwaysThinkingEnabled: true` in settings, or use Opus which engages deep reasoning automatically

**When it helps:**
- Debugging a complex issue with multiple possible causes
- Planning a multi-step refactor
- Understanding unfamiliar code with complex logic

**Trade-off:** More thinking = better answers, but more tokens and longer wait. For quick tasks, it's overhead.

---

## Slide 11: Plan Mode — Your Safety Net

Plan Mode restricts Claude to **read-only operations**. No file edits, no commands.

**What Claude CAN do in Plan Mode:**
- Read files (Read, Glob, Grep)
- Search the web (WebSearch, WebFetch)
- Spawn research sub-agents
- Write a plan and present it for approval

**What Claude CANNOT do in Plan Mode:**
- Edit or create files
- Run shell commands
- Make any changes to your project

**How to activate:**
- `Shift+Tab` twice (cycles: Normal > Auto-Accept > Plan)
- `/plan` command
- `--permission-mode plan` flag
- Set as default: `"defaultMode": "plan"` in settings

**Recommended workflow:**
1. Start in Plan Mode — let Claude analyze and propose
2. Review the plan — edit if needed
3. Switch to Normal Mode — let Claude execute
4. Verify — run tests, review diffs

> **Speaker note:** This is the most important safety feature for new users. Drill home: "When in doubt, Plan Mode."

---

## Slide 12: What Claude Cannot Do — Honest Boundaries

**Claude does not:**
- Truly understand your business logic (it pattern-matches)
- Remember anything between sessions (without memory config)
- Run your application and test it visually (without external MCPs)
- Access private services, databases, or APIs directly (without external MCPs)
- Guarantee its output compiles, passes tests, or is secure

**Claude struggles with:**
- Very large files (>1000 lines) — it may miss details
- Cross-cutting concerns spanning many files
- Tasks requiring precise numerical computation
- Projects with no documentation or unusual patterns
- Tasks far outside its training data (proprietary frameworks, niche languages)

**Claude excels at:**
- Tasks with clear patterns (CRUD, serializers, components, tests)
- Codebases with good documentation (CLAUDE.md, inline comments)
- Iterative development with test feedback
- Explaining and refactoring existing code
- Boilerplate generation and repetitive tasks

> **Speaker note:** End on the positive. The point isn't to scare them — it's to set correct expectations so they get the most out of the tool.

---

## Slide 13: Key Takeaways

1. **Three interfaces, one brain:** Chat (research), CLI (development), IDE (pair programming)
2. **Three models, different jobs:** Haiku (fast), Sonnet (daily driver), Opus (hard problems)
3. **CLAUDE.md is your highest-leverage investment** — write one before you start coding with Claude
4. **Plan Mode is your safety net** — use it before any non-trivial change
5. **Claude will be wrong sometimes** — always verify, always test

---

*Next: Live demo of Claude Chat, CLI, and IDE using the energycorp project*
