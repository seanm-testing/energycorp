# Demo Script: Claude Chat, CLI, IDE, and Chrome

**Duration:** 30-35 minutes
**Repo:** energycorp (Django REST API + React SPA)
**Prerequisites:** Claude Code CLI installed, VS Code with Claude Code extension, browser open to claude.ai, Chrome with Claude in Chrome extension installed and enabled

---

## Demo Setup (before students arrive)

1. Clone energycorp and `cd` into it
2. Verify Claude Code works: `claude --version`
3. Open VS Code in the energycorp directory
4. Open browser to claude.ai
5. Verify Claude in Chrome extension is installed and enabled in Chrome
6. Start the React dev server (`cd Frontend && npm start`) so Chrome can navigate to localhost
7. Increase terminal font size for visibility
8. Close unnecessary tabs/windows to reduce distraction

---

## Part 1: Claude Chat — Quick Look (3 min)

### Goal
Show what Claude Chat can and cannot do. Establish why Claude Code exists.

### Steps

**1.** Open claude.ai in the browser.

**2.** Type the following prompt:

```
What Django apps are in my project and what are their URL prefixes?
```

**3.** Pause. Let students see that Claude Chat has no idea — it will either ask for more info or hallucinate a generic answer.

> **Say:** "Claude Chat is great for general questions, but it can't see your project. It's working blind."

**4.** Show a useful Claude Chat interaction — paste in a Research Mode prompt:

```
Research up to date trends in the field of supply chain management technology and produce a report comparing the pros and cons of each of these new trends.
```

> **Say:** "This will take several minutes so we will let this run for now and come back to check on it later. The main takeaway should be that for isolated research and learning, Chat works well. But for real development, we need Claude Code."

---

## Part 2: Claude Code CLI (10-12 min)

### Goal
Show Claude Code reading the codebase, demonstrate CLAUDE.md, settings.json, and @ mentions.

### Steps

**1.** Switch to terminal. Navigate to the energycorp directory.

```bash
cd /path/to/energycorp
```

**2.** Launch Claude Code:

```bash
claude
```

> **Say:** "This launches Claude Code in interactive mode. It detects we're in a git repo and reads the CLAUDE.md file automatically."

**3.** Ask Claude the same question from Chat:

```
What Django apps are in this project and what are their URL prefixes?
```

> **Say:** "Watch — it reads the project structure and CLAUDE.md. It can give us an accurate answer because it has access to the actual files."

Wait for the response. It should list the apps with their URL prefixes from CLAUDE.md and/or urls.py.

**4.** Show CLAUDE.md awareness:

```
What does our CLAUDE.md tell you about this project's architecture?
```

> **Say:** "Claude reads CLAUDE.md at the start of every session. This is how it knows about our project. Let's look at the file itself."

**5.** Open CLAUDE.md in the terminal (or point to VS Code):

> **Say:** "Walk through the sections with me..."

Point out:
- **Build commands** — "These are the exact commands Claude will use when it needs to run tests or migrations."
- **Architecture** — "This tells Claude how the apps relate to each other — users, energytransfers, contracts, payments."
- **Key model relationships** — "This chain: Substation → Transformer → Counter → History — Claude uses this to understand the data flow."
- **Role-based permissions** — "Type 1 is Admin, Type 2 is Manager, Type 3 is Operator. Without this, Claude would guess."

**6.** Demonstrate @ mentions. Type in Claude Code:

```
Look at @Backend/src/users/models.py and explain the relationship between CustomUser, Client, and Worker
```

> **Say:** "The @ symbol references a specific file. Claude reads it directly instead of searching. You can also reference directories with a trailing slash."

Wait for the response. It should explain the model relationships accurately.

**7.** Show another @ mention with a specific question:

```
Look at @Backend/src/contract/views.py — which endpoints require admin permissions?
```

> **Say:** "This is how you point Claude at exactly what you need. Much faster than having it search the whole project."

**8.** Demonstrate the settings.json hierarchy. Show the project settings:

```
Show me the contents of .claude/settings.json if it exists, or explain what would go there
```

> **Say:** "Let me show you the five tiers of configuration."

Draw or show the hierarchy:

```
Priority 1 (highest): Managed   → /etc/claude-code/ (IT-deployed)
Priority 2:           CLI       → command-line flags
Priority 3:           Local     → .claude/settings.local.json (personal, gitignored)
Priority 4:           Project   → .claude/settings.json (shared, committed)
Priority 5 (lowest):  User      → ~/.claude/settings.json (personal)
```

> **Say:** "For your team, the Project scope is key. You'll commit `.claude/settings.json` to git so everyone shares the same Claude configuration. Local settings override project settings for personal preferences — like if someone wants a different default model."

**9.** Show a practical settings example:

```
Here's what a practical project settings.json looks like:
```

Type (or show pre-prepared):

```json
{
  "permissions": {
    "allow": [
      "Bash(python src/manage.py test)",
      "Bash(npm test)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(*DROP TABLE*)",
      "Bash(*--force*)"
    ]
  }
}
```

> **Say:** "Allow lists let Claude run your test commands without asking each time. Deny lists prevent dangerous operations. Deny always wins over allow."

---

## Part 3: VS Code IDE Extension (5-7 min)

### Goal
Show the same Claude Code capabilities inside VS Code with visual diffs.

### Steps

**1.** Switch to VS Code with energycorp open.

> **Say:** "Everything we just did in the terminal works in VS Code too. The IDE extension adds visual diffs, inline code references, and a tighter feedback loop."

**2.** Open the Claude Code panel (Ctrl+Esc or Cmd+Esc).

**3.** Open `Backend/src/users/models.py` in the editor. Select the `Client` class.

**4.** Use Alt+K (Windows/Linux) or Option+K (Mac) to reference the selection.

> **Say:** "I selected the Client model and used the keyboard shortcut to reference it. Claude now sees exactly what I'm looking at."

**5.** Ask in the Claude Code panel:

```
Add a property to this Client model that returns the client's full display name in the format "name (id_user)"
```

**6.** Wait for Claude to generate the change. Show the inline diff.

> **Say:** "See the diff? Green lines are additions. I can accept or reject each change. This is the core workflow in the IDE — Claude proposes, you review."

**7.** **Accept the change** (we will revert after to not modify the demo repo permanently).

> **Say:** "If you decide after accepting that you want to reject the change, you can use the "rewind" function in Claude Code CLI by hitting 'Esc' twice. From there you just select the change you want to revert to and hit 'Enter'"

---

## Part 4: Claude in Chrome (~10 min)

### Goal
Show Claude operating inside the browser — the fourth and final surface.

### Steps

**1.** Open Chrome with the energycorp React app running on localhost (`http://localhost:3000`).

> **Say:** "We've seen Claude in chat, in the terminal, and in the IDE. Now let's see it in the browser. Claude in Chrome is a browser extension that lets Claude see, navigate, and interact with web pages."

**2.** Open the Claude in Chrome side panel (click the Claude extension icon or use the keyboard shortcut).

> **Say:** "The side panel is where you interact with Claude while browsing. It can see what's on your screen and take actions in the browser."

**3.** Ask Claude to describe the running app:

```
Navigate to http://localhost:3000 and describe what you see on the page.
```

> **Say:** "Watch — Claude navigates to the page, takes a screenshot, and tells us what it sees. It's reading the actual rendered UI, not source code."

Wait for Claude to navigate and respond. It should describe the login page or whichever page is displayed.

**4.** Ask Claude to identify a specific UI element:

```
What form fields and buttons are on this page?
```

> **Say:** "Claude can identify individual UI elements — form fields, buttons, navigation items. This is useful for testing and accessibility reviews."

**5.** Demonstrate the screenshot capability:

```
Take a screenshot of this page.
```

> **Say:** "Claude can capture screenshots of the current page state. During development, this is how you verify that your UI changes look right without switching windows."

**6.** Show Claude reading page content and DOM state:

```
What text content is visible on this page? Are there any console errors?
```

> **Say:** "Claude reads the actual DOM — not just what's visible, but the underlying page structure. When connected to Claude Code, it can also read console errors and network requests, creating a build-test-debug loop."

**7.** **Safety model segment (2-3 min):**

> **Say:** "Now let's talk about safety — because giving an AI control of your browser is a big deal."

Show the "ask before acting" vs autonomous mode toggle in the extension settings.

> **Say:** "By default, Claude asks before clicking, typing, or navigating. This is 'ask before acting' mode. There's also an autonomous mode where Claude acts without asking — but that should only be used for supervised, low-risk tasks."

Demonstrate the confirmation prompt by asking Claude to do something interactive:

```
Click on the first input field on this page.
```

> **Say:** "See the confirmation? Claude tells you what it wants to do and waits for approval. This is the safety gate."

Explain the site blocklist:

> **Say:** "Claude in Chrome blocks certain categories of sites by default — financial services, banking, cryptocurrency exchanges, and adult content. You can't accidentally let Claude log into your bank account."

Present the red-teaming results:

> **Say:** "Anthropic red-teamed Chrome across 123 test cases and 29 attack scenarios. Attack success rates dropped from 23.6% without mitigations to approximately 1% with the current safeguards. That's strong — but not zero. No AI tool is infallible, which connects directly to our next lecture on hallucinations and safe usage."

**8.** Reference the deep-dive resource:

> **Say:** "For a full security analysis of Claude in Chrome and Claude Cowork, read the document in `Course_Resources/ClaudeCowork_ClaudeInChrome.md`. It covers the architecture, known vulnerabilities, and organizational deployment recommendations."

---

## Part 5: Plan Mode (3-5 min)

### Goal
Demonstrate Plan Mode as a read-only safety net.

### Steps

**1.** In the Claude Code CLI (switch back to terminal), activate Plan Mode:

Press `Shift+Tab` twice. Show the mode indicator changing: Normal → Auto-Accept → Plan.

> **Say:** "I'm now in Plan Mode. Watch the indicator — it says 'Plan.' Claude can read everything but modify nothing."

**2.** Ask Claude to plan a change:

```
Plan how you would add a "last_payment_date" field to the Invoice model, including all necessary migrations, serializer updates, and view changes.
```

**3.** Wait for the plan. It should outline:
- Add field to `contract/models.py` (Invoice model)
- Create and run migration
- Update `contract/serializers.py`
- Update relevant views if needed
- Run tests

> **Say:** "Look at this plan. Claude identified every file that needs to change, the order of operations, and even mentioned running tests. But it hasn't touched a single file. This is why Plan Mode is your starting point for any non-trivial task."

**4.** Switch back to Normal Mode (Shift+Tab).

> **Say:** "Once you approve the plan, you switch back to Normal Mode and let Claude execute. But you always start by reading the plan."

---

## Demo Wrap-Up

> **Say:** "Let's recap the four surfaces we just saw:
> - Claude Chat is for research and isolated questions — no project access
> - Claude Code CLI gives Claude full access to your project from the terminal
> - The VS Code extension provides the same power with visual diffs
> - Claude in Chrome extends Claude into your browser — navigating pages, reading content, and taking actions, with safety controls you configure
> - CLAUDE.md is how you teach Claude about your project
> - Settings.json controls what Claude is allowed to do
> - @ mentions point Claude at specific files
> - Plan Mode lets Claude analyze without modifying
>
> Next, we're going to talk about the biggest risk when using these tools: hallucinations."

---

## Troubleshooting Common Demo Issues

| Issue | Fix |
|-------|-----|
| `claude: command not found` | `npm install -g @anthropic-ai/claude-code` |
| Authentication fails | Run `claude` and follow the login prompts; check API key |
| VS Code extension not showing | Check Extensions panel, search "Claude Code" by Anthropic |
| @ mentions not autocompleting | Ensure you're in the project root; try pressing Tab after @ |
| Claude gives wrong project info | Check that CLAUDE.md exists and is correctly formatted |
| Plan Mode not activating | Try `/plan` command instead of Shift+Tab |
| Chrome extension not showing in side panel | Check Chrome extensions page (`chrome://extensions`), ensure "Claude in Chrome" by Anthropic is installed and enabled |
| Chrome can't connect to Claude Code | Requires extension v1.0.36+ and Claude Code v2.0.73+; launch with `claude --chrome` or use `/chrome` |
| Localhost app not loading in Chrome | Verify `npm start` is running in the Frontend directory; check `http://localhost:3000` loads manually |
