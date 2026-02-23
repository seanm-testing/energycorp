# Session 1 Instructor Guide: Introduction to Claude Code

**Duration:** 2 hours
**Audience:** Ukrainian software contractor (~22 employees, frontend + backend split) building "BulkSource" — a construction supply chain web portal (Django + React)
**Demo repo:** energycorp (Django REST API + React SPA)
**Prerequisites:** Students have VS Code installed, terminal access, and an Anthropic account or API key

---

## Session Overview

| Block | Topic | Duration | Format |
|-------|-------|----------|--------|
| 1 | Greeting & Introductions | 5 min | Interactive |
| 2 | Presentation: What is Claude? | 15-20 min | Slides/Lecture |
| 3 | Demo: Claude Chat, CLI, IDE | 20-25 min | Live Demo |
| 4 | Lecture: Hallucinations & Safe Usage | 15 min | Lecture |
| 5 | Hands-On Lab | 45-60 min | Guided Lab + Independent Work |
| 6 | Q&A & Wrap-Up | 5-10 min | Discussion |

**Total: ~110-135 minutes**

---

## Block 1: Greeting & Introductions (5 min)

### Objectives
- Set a collaborative tone
- Gauge the room's existing AI tool experience

### Speaker Notes

**[0:00]** Welcome everyone. Introduce yourself and the course structure.

> "This is Session 1 of a 5-session course on Claude Code. Today we'll cover the fundamentals — what Claude is, how to interact with it, how to avoid common pitfalls, and then you'll get hands-on with it on your own codebase."

**[0:02]** Quick poll (show of hands):
- "Who has used ChatGPT, Copilot, or similar AI tools for coding?"
- "Who has used Claude specifically?"
- "Who has used any AI tool from the command line?"

**[0:04]** Frame the session:

> "By the end of today, each of you will have Claude Code installed, configured for your codebase, and will have submitted a PR with a Claude-generated change and a review checklist. The goal isn't just to use the tool — it's to use it *safely* and *effectively*."

### Transition
> "Let's start with understanding what Claude actually is and how it differs from tools you may have already used."

---

## Block 2: Presentation — What is Claude? (15-20 min)

### Objectives
- Understand the Claude model family (Opus, Sonnet, Haiku)
- Distinguish Claude Chat, Claude Code (CLI), and Claude Code (IDE)
- Introduce Research Mode, Extended Thinking, and Plan Mode
- Set honest capability boundaries

### Materials
- `02_Presentation_What_Is_Claude.md` (slide-by-slide content)

### Speaker Notes

**[0:05]** Open with the model family. Emphasize the practical trade-off: cost vs. capability.

> "Think of Opus, Sonnet, and Haiku as different gears. Haiku is for quick lookups and simple tasks. Sonnet is your daily driver for most coding work. Opus is for complex architecture decisions, debugging hard problems, or when you need deep reasoning."

**[0:10]** Walk through the three interfaces. The key insight for this audience:

> "Claude Chat is great for research and brainstorming. But Claude Code is where the real power is — it reads your actual codebase, runs commands, creates files, and submits PRs. The IDE extension gives you that power with a visual interface inside VS Code."

**[0:15]** Cover the modes. Plan Mode is the most important for safe adoption:

> "Plan Mode is read-only. Claude can explore your codebase, analyze dependencies, and design an approach — but it cannot modify anything. This is your safety net. When you're unsure, start in Plan Mode."

**[0:18]** Be honest about limitations.

> "Claude will hallucinate. It will invent API endpoints that don't exist, reference packages with wrong method signatures, and confidently produce code that doesn't compile. We'll cover how to handle this in the hallucinations section, but I want you to hear it now: *trust but verify, every time*."

### Transition
> "Let's see all of this in action. I'm going to switch to my terminal and walk through Claude Code live."

---

## Block 3: Demo — Claude Chat, CLI, IDE (20-25 min)

### Objectives
- Show Claude Chat (web) briefly
- Launch Claude Code CLI, demonstrate basic interaction
- Show VS Code IDE extension
- Load energycorp, show CLAUDE.md levels (user/project/local)
- Walk through settings.json 5-tier hierarchy
- Demonstrate @ mentions and file references

### Materials
- `03_Demo_Script.md` (step-by-step demo script)
- energycorp repo cloned and ready

### Pre-Demo Checklist
- [ ] energycorp repo cloned to a visible terminal path
- [ ] Claude Code CLI installed and authenticated
- [ ] VS Code open with Claude Code extension installed
- [ ] Browser tab open to claude.ai (for Chat demo)
- [ ] Terminal font size increased for visibility

### Speaker Notes

**[0:20]** Start in the browser — show Claude Chat briefly (2-3 min).

> "This is Claude Chat — the web interface. You can paste code, ask questions, have it generate snippets. It's useful, but it has no access to your actual project. Watch..."

Ask Claude Chat: "What files are in my project?" — it can't answer. This sets up *why* Claude Code matters.

**[0:23]** Switch to terminal. Launch `claude` in the energycorp directory.

> "Now I'm in Claude Code. It sees my entire project. Let me ask the same question."

Run: `claude` then ask "What Django apps are in this project?" — it will read the filesystem and answer correctly.

**[0:26]** Show CLAUDE.md.

> "This is the most important file in your project for working with Claude. It's the instructions Claude reads every single time. Think of it as onboarding documentation — not for humans, but for the AI."

Open CLAUDE.md and walk through each section. Emphasize:
- Build commands (Claude uses these to run tests, lint, etc.)
- Architecture overview (this is how Claude understands your project)
- Key model relationships (this prevents Claude from guessing)

**[0:30]** Show settings.json hierarchy. Open `.claude/settings.json` and `~/.claude/settings.json`. Explain the 5-tier precedence.

> "If your IT team sets a managed policy that says 'never run rm -rf', no project setting or user preference can override that. Higher scopes always win."

**[0:34]** Show @ mentions. In the CLI, type `@` and show autocomplete. Reference a file:

> "Watch — I'll say '@Backend/src/users/models.py explain the CustomUser model.' Claude reads that specific file and gives me a targeted answer."

**[0:38]** Switch to VS Code. Show the extension panel. Demonstrate the same interaction in the IDE:
- Open a file, select code, use Option+K/Alt+K to reference it
- Show the inline diff view
- Show how to accept/reject changes

**[0:42]** Demonstrate Plan Mode. Hit Shift+Tab twice.

> "See the indicator? I'm now in Plan Mode. Claude can read everything but modify nothing. I'll ask it to plan adding a new field to the Invoice model."

Let Claude generate a plan. Show the output — it identifies files to change, migration steps, serializer updates, etc. — but makes no actual changes.

> "This is your starting point for any non-trivial task. Plan first, then execute."

### Transition
> "Now that you've seen what Claude can do, let's talk about what it gets wrong — and how to protect yourself."

---

## Block 4: Lecture — Hallucinations & Safe Usage (15 min)

### Objectives
- Explain what causes hallucinations
- Show real Django/React examples
- Teach avoidance techniques: TDD, Plan Mode, verification
- Introduce the Correction Spiral anti-pattern
- Warn about context degradation

### Materials
- `04_Lecture_Hallucinations.md` (full lecture content)

### Speaker Notes

**[0:45]** Start with the "why." Keep it practical, not academic.

> "Hallucinations aren't bugs — they're a fundamental property of how language models work. Claude doesn't 'know' your codebase the way you do. It *predicts* what reasonable code looks like based on patterns. Sometimes those predictions are wrong."

**[0:48]** Walk through the three real examples from the lecture notes:
1. Django: Claude imports a mixin that doesn't exist in your version of DRF
2. React: Claude uses a hook pattern from React 18 when your project runs React 16
3. API: Claude invents an endpoint URL that follows the project's pattern but isn't defined

> "Notice the pattern? Claude's hallucinations are *plausible*. That's what makes them dangerous. They look right at first glance."

**[0:52]** Cover the defenses. For this audience, emphasize the workflow:

> "Here's the workflow that works: Explore in Plan Mode. Write a test for what you want. Let Claude implement against the test. Run the test. If it fails, give Claude the error — don't try to fix it yourself. If it fails twice more on the same issue, start a fresh session."

**[0:55]** The Correction Spiral. This is the most important anti-pattern for new users:

> "You ask Claude to fix something. It makes a different mistake. You correct that. It breaks something else. Three corrections in, Claude's context is polluted with failed attempts and contradictory instructions. The fix is simple: `/clear` and start over with a better prompt. A clean session beats a corrected session every time."

**[0:58]** Context degradation. Explain why long sessions lose quality:

> "Claude has a context window — think of it as short-term memory. As conversations get long, earlier details get compressed or lost. If you've been working for 30+ minutes on a complex task and Claude starts giving worse answers, it's not broken — it's full. Run `/compact` to compress, or `/clear` to start fresh."

### Transition
> "Alright, enough theory. Let's put this into practice. Open your terminals — we're going hands-on."

---

## Block 5: Hands-On Lab (45-60 min)

### Objectives
- Install Claude Code (if not already done)
- Load energycorp, create/review CLAUDE.md together
- Walk through settings.json configuration
- Implement a small change using Claude Code
- Validate the change (tests, manual review)
- Create a PR with a review checklist

### Materials
- `05_Lab_Guide_Demo.md` (instructor-led lab guide for energycorp demo)
- `06_Student_Worksheet.md` (generalized worksheet for BulkSource)
- `07_PR_Review_Checklist_Template.md` (PR checklist template)

### Structure
The lab has two phases:
1. **Instructor-led (20-25 min):** Everyone follows along using the energycorp repo
2. **Independent work (25-35 min):** Students apply the same steps to their BulkSource codebase using the worksheet

### Speaker Notes — Phase 1: Instructor-Led

**[1:00]** Quick setup check.

> "Everyone open your terminal. Type `claude --version`. If you see a version number, you're good. If not, raise your hand and we'll get you installed."

Handle any installation issues (should be pre-installed per prerequisites, but have `npm install -g @anthropic-ai/claude-code` ready).

**[1:03]** Navigate to the energycorp repo together.

> "Navigate to where you cloned energycorp. Run `claude`. You should see Claude Code start up and detect the project."

**[1:05]** Review the CLAUDE.md together.

> "Open CLAUDE.md in VS Code. Let's read through it together. Notice how it's structured: project overview, build commands, architecture, and key relationships. This is what a good CLAUDE.md looks like. We're going to build one like this for BulkSource later."

Walk through best practices:
- Keep it under 80 lines
- Include exact build/test/lint commands
- Describe architecture concisely
- Document gotchas and non-obvious patterns

**[1:12]** Show settings.json configuration.

> "Let's look at the settings. Open `.claude/settings.json`. I'm going to add a permission rule that allows running our test command without asking every time."

Demonstrate adding: `"allow": ["Bash(python src/manage.py test)"]`

**[1:18]** Implement a small change together.

> "Let's add a `phone_display` property to the Client model that formats the phone number. We'll do this the right way: Plan Mode first, then implement."

Walk through:
1. Enter Plan Mode (Shift+Tab twice)
2. Ask Claude to plan adding a `phone_display` property to the Client model
3. Review the plan
4. Switch to Normal Mode
5. Let Claude implement it
6. Review the diff
7. Run tests

**[1:25]** Create a PR together.

> "Now let's have Claude create a PR. Watch what happens."

Ask Claude: "Create a PR for this change. Include a summary and a review checklist."

Show the PR on GitHub. Walk through the generated checklist.

### Speaker Notes — Phase 2: Independent Work

**[1:28]** Hand out the worksheet (or share the link to `06_Student_Worksheet.md`).

> "Now it's your turn. Switch to your BulkSource project. The worksheet will guide you through the same steps we just did together: create a CLAUDE.md, configure settings, implement a small change, and submit a PR. You have about 30 minutes. I'll be around to help."

**[1:28-1:55]** Circulate the room. Common issues to watch for:
- CLAUDE.md too long or too generic — guide them to be specific
- Students trying to do too much in one prompt — encourage small, focused asks
- Correction spirals — remind them to `/clear` and start fresh
- Permission issues with Claude running commands — help configure settings.json

**[1:55]** Five-minute warning.

> "Five minutes left. If you haven't submitted your PR yet, that's your priority. Even if it's a small change, get the PR created with the review checklist."

### Transition
> "Alright, let's wrap up. Who has questions?"

---

## Block 6: Q&A & Wrap-Up (5-10 min)

### Objectives
- Answer questions
- Reinforce key takeaways
- Preview Session 2

### Speaker Notes

**[2:00]** Open the floor for questions.

**[2:05]** If questions wind down, reinforce three takeaways:

> "Three things to remember from today:
> 1. **CLAUDE.md is your highest-leverage investment.** A good CLAUDE.md makes every interaction better. A bad one — or none at all — means Claude is guessing.
> 2. **Plan Mode before you build.** Especially for anything that touches more than one file.
> 3. **The Correction Spiral is real.** If Claude isn't getting it after two corrections, start fresh. Don't keep pushing."

**[2:08]** Preview Session 2.

> "Next session, we'll go deeper into Claude Code's power features: hooks for automated testing, custom slash commands, sub-agents, and how to build a CLAUDE.md that actually scales with your team. Between now and then, I'd encourage you to use Claude Code on your daily BulkSource work. Keep notes on what works and what doesn't — we'll use those experiences in Session 2."

**[2:10]** Close.

> "Great work today. If you get stuck between sessions, remember: `/help` in Claude Code, and the Anthropic docs at docs.anthropic.com. See you next time."

---

## Instructor Preparation Checklist

### Before the Session
- [ ] Clone the energycorp repo and verify it builds/runs
- [ ] Install Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- [ ] Install VS Code Claude Code extension
- [ ] Authenticate Claude Code (`claude` → follow login flow)
- [ ] Test the demo script end-to-end (run through `03_Demo_Script.md`)
- [ ] Verify students have received pre-session setup instructions
- [ ] Prepare screen sharing with increased font size
- [ ] Have `06_Student_Worksheet.md` ready to distribute
- [ ] Have `07_PR_Review_Checklist_Template.md` ready to distribute

### Technical Requirements
- Stable internet connection (Claude Code requires API access)
- Terminal with `claude` command available
- VS Code with Claude Code extension
- Git configured for creating branches and PRs
- GitHub access for PR creation (or equivalent)

### Backup Plans
- If Claude Code API is slow/down: Have pre-recorded demo video ready
- If students can't install during session: Pair them with someone who has it working
- If energycorp repo has issues: The demo can be done on any project with a CLAUDE.md
