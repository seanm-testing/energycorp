# Claude Code: the complete feature guide for early 2026

**Claude Code has evolved into a deeply extensible agentic coding platform** with 14 hook events, a skills system, sub-agents, multi-repo support, and a 5-tier configuration hierarchy. This guide covers every major Claude Code feature as of February 2026 — from IDE setup through advanced automation workflows — based on official Anthropic documentation, the Claude Code GitHub repository, and community resources. The platform now supports plugins, agent teams, MCP Tool Search, and integrates tightly with the broader Claude ecosystem including the new Cowork product for knowledge workers.

---

## 1. IDE integration spans VS Code, JetBrains, and any terminal

The **VS Code extension** is the most polished integration. Install from the Extensions Marketplace (publisher: Anthropic) — it also works with Cursor, Windsurf, and VSCodium. The CLI auto-installs the extension when it detects VS Code (disable with `DISABLE_CLAUDE_CODE_VSCODE_EXTENSION_AUTOINSTALL`). Key features include inline diffs with accept/reject buttons, plan mode review, `@`-mention files with line ranges (`@src/utils.ts#L1-50`), conversation history, multi-tab parallel conversations, `@terminal:name` references, and Chrome browser integration via `@browser`. Launch with `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux). The extension supports VS Code's secondary sidebar (v1.97+) and provides status indicators — blue dot for pending permissions, orange dot for completed background tasks.

The **JetBrains plugin** supports IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, GoLand, Android Studio, and others. Install through Settings → Plugins → Marketplace. It shows code changes in the IDE's native diff viewer, shares current selections and diagnostic errors automatically, and supports file references via `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Windows/Linux). Configure the plugin in Settings → Tools → Claude Code, including the claude command path and auto-update preferences. One security note: when running with auto-edit permissions in JetBrains, Claude may modify IDE configuration files that can be auto-executed.

**Any editor with an integrated terminal** (Neovim, Emacs, Sublime Text) can run `claude` directly. Claude reads and writes files on disk, and editors pick up changes automatically. Use `/ide` in an external terminal to connect to a specific running IDE.

---

## 2. The 5-scope configuration hierarchy controls all settings

Claude Code uses a strict precedence hierarchy with five scopes, from highest to lowest priority:

| Priority | Scope | Location | Shared? |
|----------|-------|----------|---------|
| 1 (highest) | **Managed** | System directories (e.g., `/etc/claude-code/` on Linux) | Yes (IT-deployed) |
| 2 | **Command line** | CLI flags | Session only |
| 3 | **Local** | `.claude/settings.local.json` | No (gitignored) |
| 4 | **Project** | `.claude/settings.json` | Yes (committed) |
| 5 (lowest) | **User** | `~/.claude/settings.json` | No |

**Higher-scoped settings always override lower ones.** If a permission is allowed in user settings but denied in project settings, the project setting wins. Managed settings can never be overridden. The system uses deep merge with array replacement — the most specific value wins per key path. Deny rules are always evaluated first, then ask, then allow; first match wins.

Managed settings paths vary by OS: `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS, `/etc/claude-code/managed-settings.json` on Linux, and `C:\Program Files\ClaudeCode\managed-settings.json` on Windows. Claude Code automatically creates timestamped backups of configuration files, retaining the 5 most recent.

---

## 3. Settings.json offers granular control over every behavior

Access settings via `/config` in the REPL. Add `"$schema": "https://json.schemastore.org/claude-code-settings.json"` for autocomplete in VS Code. The major settings categories include:

**General settings** cover `model` (override default), `language` (response language), `outputStyle`, `cleanupPeriodDays` (default 30), `autoUpdatesChannel` ("stable" or "latest"), `alwaysThinkingEnabled`, `effortLevel` (low/medium/high), `plansDirectory`, and `respectGitignore`.

**Permission settings** (inside a `"permissions"` object) include `allow`, `ask`, and `deny` arrays with rule syntax like `Bash(npm run lint)`, `Read(~/.zshrc)`, or `WebFetch(domain:example.com)`. The `defaultMode` field accepts `default`, `acceptEdits`, `plan`, or `bypassPermissions`. The `additionalDirectories` array extends file access beyond the working directory.

**Sandbox settings** enable OS-level bash sandboxing with `autoAllowBashIfSandboxed`, `excludedCommands`, and network controls (`allowedDomains`, `allowUnixSockets`, `allowLocalBinding`).

**Hooks settings** define event-driven automation (covered in detail in section 12). **MCP settings** control server approval with `enableAllProjectMcpServers`, `enabledMcpjsonServers`, and `disabledMcpjsonServers`. **Authentication settings** include `apiKeyHelper` for dynamic credential scripts and `forceLoginMethod` to restrict login to `claudeai` or `console`.

Key environment variables include `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS` (default 32K, max 64K), `MAX_THINKING_TOKENS`, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` for tuning auto-compaction thresholds.

---

## 4. CLAUDE.md is the highest-leverage configuration point

CLAUDE.md is a Markdown file that Claude reads automatically at the start of every conversation, serving as persistent project-specific memory. Claude Code loads memory from **six hierarchical locations**: managed (system directories), user (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md` or `./.claude/CLAUDE.md`), project local (`./CLAUDE.local.md`), parent directories (recursing upward from CWD), and child directories (on-demand when Claude accesses files there). Additionally, `.claude/rules/*.md` files load when working with relevant paths.

More specific memory takes precedence over broader memory. Files support `@` import syntax for referencing other markdown files (max depth: 5 hops). Claude also maintains auto-generated `MEMORY.md` files (first 200 lines loaded) in `~/.claude/projects/<project>/memory/`.

**Best practices for CLAUDE.md content:**

- **Include**: project context (one-liner), tech stack and architecture, code style rules, build/test/lint commands, gotchas, and verification instructions
- **Keep it lean**: aim for **50–80 lines** — frontier models reliably follow ~150–200 instructions, and Claude's system prompt already consumes ~50
- **Avoid**: generic instructions ("write clean code"), auto-generated content, formatting rules (use linters instead), and stuffing every possible command
- **Use separate files** for detailed reference docs (`@docs/architecture.md`) rather than embedding everything
- **Split into `.claude/rules/`** for modular, team-owned rule files that avoid merge conflicts

Create with `/init` (auto-generates from codebase analysis), add memories with the `#` prefix shortcut, or edit directly with `/memory`.

---

## 5. Skills extend Claude Code with modular, auto-invoked capabilities

Agent Skills are directories containing a required `SKILL.md` file with YAML frontmatter plus optional supporting files. Unlike slash commands (user-invoked), **skills are model-invoked** — Claude autonomously decides when to use them based on the description field.

```yaml
---
name: your-skill-name
description: What this does and when to use it
allowed-tools: Read, Grep, Glob
context: fork          # run in isolated subagent
agent: Explore         # specify agent type
---
# Markdown instructions here
```

Skills live in `~/.claude/skills/` (personal) or `.claude/skills/` (project, shared via git). Claude scans all skill frontmatter at startup (~100 tokens each) and loads full content only when invoked (<5K tokens). The `context: fork` option runs skills in isolated subagent contexts. The `disable-model-invocation: true` flag restricts to user-only invocation, while `user-invocable: false` makes skills background-only.

The **Skills API** is available via `/v1/skills` on the Claude API with beta headers. Pre-built skills (pptx, xlsx, docx, pdf) can be referenced by `skill_id`. An official repository at `github.com/anthropics/skills` provides pre-built skills including skill-creator, mcp-builder, and webapp-testing. Community repositories offer 50+ additional contributions. Skills support hot-reload in v2.1+ — edit during a session without restarting.

---

## 6. Multi-repo context uses --add-dir for cross-repository work

The primary mechanism is the `--add-dir` flag, which extends file access beyond the current working directory:

```bash
claude --add-dir ../backend-api --add-dir ~/shared/libraries
```

During a session, use `/add-dir /path/to/other/project`. For persistent configuration, add paths to `additionalDirectories` in settings. By default, CLAUDE.md files from additional directories are **not** loaded — enable with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Skills in `.claude/skills/` within added directories load automatically with live change detection.

Practical patterns include launching Claude from a parent directory containing related repos, using VS Code multi-root workspaces, or temporarily adding a microservice repo mid-session. Current limitations include no multi-repo support in remote/web sessions and no coordinated cross-repo PR creation. Agent Teams (experimental) offer parallel work across repos with different teammates assigned to different repositories.

---

## 7. Plan mode restricts Claude to read-only research before implementation

Plan mode blocks all file modifications and command execution, restricting Claude to **read-only operations**: Read, LS, Glob, Grep, Task (research subagents), WebFetch, WebSearch, and TodoRead/TodoWrite. Activate with **Shift+Tab twice** (cycles Normal → Auto-Accept → Plan), `claude --permission-mode plan`, or the `/plan` command. Configure as default with `"defaultMode": "plan"` in settings.

Internally, Claude analyzes the codebase, may spawn the **Plan subagent** (Sonnet-powered) or **Explore subagent** (Haiku-powered), creates a markdown plan, and presents it via the `exit_plan_mode` tool. Users can approve, edit (Ctrl+G opens in editor), or refine the plan. An **Opus Plan Mode** option (model menu option 4) uses Opus for deep reasoning during planning and Sonnet for cost-efficient execution.

Plan mode excels for multi-step features, complex refactors, architecture decisions, and code exploration. The recommended workflow is: plan first, get approval, then Shift+Tab to auto-accept for rapid execution.

---

## 8. Sub-agents run in isolated context windows with specialized roles

Sub-agents are specialized AI assistants with their own context window, custom system prompt, specific tool access, and independent permissions. Their work doesn't pollute the main conversation, enabling focused delegation.

**Built-in sub-agents** include Explore (Haiku-powered, read-only codebase search), Plan (Sonnet-powered, used during plan mode), and a general-purpose agent (Sonnet-powered, full tool access). Create custom sub-agents via `/agents` command, manual file creation in `.claude/agents/`, or the `--agents` CLI flag.

```yaml
---
name: code-reviewer
description: Reviews code for quality. Use proactively after changes.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
skills: skill1, skill2
memory: user
---
Your system prompt defining role and approach.
```

Sub-agents cannot spawn other sub-agents (preventing infinite recursion). Claude matches tasks to sub-agents based on description fields — include "use PROACTIVELY" for more automatic delegation. Project-level sub-agents override user-level ones with the same name.

**Agent Teams** (experimental, requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) take this further: teammates message each other directly, self-coordinate via shared task lists with dependency tracking, and each has a full independent session. They require tmux or iTerm2 for split-pane visualization and cost ~5x tokens per teammate compared to regular sub-agents.

---

## 9. Memory spans built-in files, auto-notes, and third-party solutions

Claude Code's memory architecture has three layers. The **built-in layer** is the CLAUDE.md hierarchy (managed → user → project → local), loaded at session start with recursive upward scanning and on-demand child directory loading.

The **auto memory layer** (v2.1.32+) has Claude writing notes to `~/.claude/projects/<project>/memory/MEMORY.md` based on session discoveries. Only the first **200 lines** are loaded per session; topic files (debugging.md, api-conventions.md) load on-demand. Control with `CLAUDE_CODE_DISABLE_AUTO_MEMORY`. Caveats include the hard 200-line limit, uncontrolled quality, and potential for accumulated files needing cleanup.

**Third-party memory solutions** include:

- **@modelcontextprotocol/server-memory**: Official Anthropic MCP server with knowledge graph storage in local JSON
- **Basic Memory** (basicmemory.com): Complementary MCP server storing detailed knowledge with search and relations
- **mcp-memory-service** (doobidoo): Feature-rich with semantic search, SQLite-vec, web dashboard, and HTTP/OAuth transport
- **claude-mem** plugin: Automatically captures session activity, compresses with AI, provides web viewer UI
- **episodic-memory** (fsck.com): Comprehensive solution combining conversation archives, SQLite vector search, Haiku sub-agent for context management, and a skill teaching Claude when to search past sessions
- **claude-supermemory** plugin: Cloud-based team memory with auto-capture and signal extraction

---

## 10. Over 30 built-in slash commands plus extensible custom commands

Key built-in commands include `/init` (bootstrap CLAUDE.md), `/compact` (compress context with optional focus), `/clear` (reset conversation), `/config` (open settings), `/context` (visualize context usage), `/memory` (edit memory files), `/model` (switch models), `/permissions` (manage permissions), `/agents` (manage sub-agents), `/hooks` (manage hooks), `/mcp` (manage MCP servers), `/plugin` (manage plugins), `/review` (code review), `/security-review` (security audit), `/sandbox` (enable sandboxing), `/rewind` (rewind conversation/code), `/export` (export conversation), and `/doctor` (health check).

**Custom slash commands** are Markdown files stored in `.claude/commands/` (project-scoped) or `~/.claude/commands/` (personal). They support YAML frontmatter with `allowed-tools`, `argument-hint`, `description`, `model`, and `hooks` fields. Use `$ARGUMENTS` for all arguments or `$1`, `$2` for positional parameters. Commands can execute shell commands with `!` prefix and reference files with `@`. Subdirectories create namespaces: `.claude/commands/frontend/component.md` becomes `/component` tagged as "(project:frontend)".

MCP servers expose prompts as `/mcp__<server>__<prompt>` commands. Plugins provide namespaced commands. Skills in `.claude/skills/` supersede commands with the same name and add auto-invocation based on context.

---

## 11. @ mentions reference files, directories, line ranges, and MCP resources

Type `@` to trigger file path autocomplete. Supported types: **files** (`@src/components/Header.tsx`), **directories** (`@path/to/dir/`), **line ranges** (`@app.ts#5-10` in VS Code), and **MCP resources** (`@server:protocol://resource/path`). Tab completion navigates the file system, respecting `.gitignore`. In VS Code, `Option+K` / `Alt+K` inserts references from the current selection, and holding Shift while dragging files creates `@`-references.

Multiple files can be referenced in a single message. When you `@`-reference a file, Claude also loads any CLAUDE.md files from that file's directory hierarchy. Inside CLAUDE.md files, `@path/to/import` syntax imports other files (up to 5 hops deep). A known limitation: files from directories added via `/add-dir` don't appear in `@`-autocomplete.

---

## 12. Fourteen hook events enable deterministic automation at every lifecycle point

Hooks are user-defined shell commands, LLM prompts, or agent spawns that execute automatically at specific lifecycle points. Unlike prompt instructions (suggestions), **hooks guarantee execution every time their matching event fires**.

| Event | Fires When | Can Block? |
|-------|-----------|------------|
| **PreToolUse** | Before tool execution | Yes (exit 2 or JSON deny) |
| **PostToolUse** | After successful tool completion | Yes (JSON block) |
| **PostToolUseFailure** | After tool failure | No |
| **PermissionRequest** | Permission dialog shown | Yes (allow/deny) |
| **UserPromptSubmit** | User submits prompt | Yes (exit 2) |
| **Notification** | Claude sends notification | No |
| **Stop** | Claude finishes responding | Yes (JSON block) |
| **SubagentStop** | Sub-agent finishes | Yes (JSON block) |
| **SubagentStart** | Sub-agent starts | No |
| **SessionStart** | Session starts/resumes/clears | No |
| **SessionEnd** | Session terminates | No |
| **PreCompact** | Before context compaction | No |
| **TeammateIdle** | Agent team member going idle | N/A |
| **TaskCompleted** | Task marked complete | Yes |

**Three hook types** exist: `command` (shell script receiving JSON on stdin), `prompt` (single-turn LLM evaluation, Haiku by default), and `agent` (sub-agent with tool access for verification). Configure in `~/.claude/settings.json` (all projects), `.claude/settings.json` (project, shared), `.claude/settings.local.json` (personal), or managed settings (enterprise, highest precedence).

**PreToolUse hooks can modify tool inputs** before execution (v2.0.10+), enabling transparent sandboxing and security enforcement invisible to Claude. Hooks communicate via exit codes (0 = success, 2 = blocking error), stdout JSON (with fields like `decision`, `reason`, `additionalContext`, `continue`), and stderr (error messages). All matching hooks run in parallel with automatic deduplication. The `/hooks` command provides interactive setup.

---

## 13. MCP connects Claude Code to external tools, data, and services

The Model Context Protocol (MCP) is an open-source standard connecting AI applications to external systems. The architecture comprises hosts (Claude Code), MCP clients (1:1 sessions), MCP servers (tools/resources/prompts), and transports (stdio for local, HTTP for remote, SSE deprecated).

**Install MCP servers** via CLI:
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
claude mcp add --transport stdio airtable --env API_KEY=xxx -- npx -y airtable-mcp-server
```

Three scopes: **local** (private, in `~/.claude.json`), **project** (shared via `.mcp.json`), and **user** (all projects). Manage with `claude mcp list`, `claude mcp get <name>`, `claude mcp remove <name>`, and `/mcp` in-session. **MCP Tool Search** (Sonnet 4+, Opus 4+) dynamically loads tools on-demand when descriptions exceed 10% of the context window, reducing MCP context usage by up to **95%**.

Popular servers include GitHub (`@modelcontextprotocol/server-github` or HTTP at `https://api.githubcopilot.com/mcp`), Figma (`https://mcp.figma.com/mcp`), PostgreSQL, Brave Search, Puppeteer, Notion, Sentry, Slack, and Stripe. Multiple marketplace platforms exist: Claude Code Marketplace (1,261+ servers), MCP.so (17,665+ servers), and Claude Market (open-source, hand-curated). Plugins can bundle MCP servers, and enterprise settings support allowlists/denylists for restricting which servers can be used.

---

## 14. The permission system layers rules, modes, hooks, and sandboxing

When Claude requests a tool, permissions check in order: **Hooks** (PreToolUse) → **Permission Rules** (deny → allow → ask, first match wins) → **Permission Mode** → approval prompt. Rules use glob-style syntax: `Bash(npm run *)`, `Read(./.env*)`, `Edit(src/**)`, `WebFetch(domain:github.com)`.

**Five permission modes** control default behavior:

- **default**: Allows reads, asks before modifications
- **plan**: Read-only, no tool execution
- **acceptEdits**: Auto-approves file edits and filesystem commands
- **bypassPermissions**: Skips all checks (only for isolated environments)
- **dontAsk**: Auto-denies all unapproved tools silently

Switch modes with Shift+Tab during sessions. Permission lists override modes — modes only affect unspecified tools. **Sandboxing** provides a complementary OS-level layer via `sandbox-exec` (macOS), restricting what Bash commands can actually access at the filesystem/network level. Configure with `sandbox.enabled`, `network.allowedDomains`, and `excludedCommands` in settings.

Enterprise managed settings have highest precedence, cannot be overridden, and support `disableBypassPermissionsMode: "disable"` plus MCP server allowlists/denylists.

---

## 15. Artifacts and Projects power Claude.ai's web-based creation environment

**Artifacts** are standalone content objects created in a dedicated panel alongside the chat. Types include documents, code snippets, live HTML websites, SVG images, Mermaid diagrams, interactive React components, and file outputs (Excel, Word, PowerPoint, PDF). A major June 2025 upgrade enabled **AI-Powered Artifacts** that embed Claude's intelligence directly — shared artifacts run against the viewer's subscription. Over **half a billion artifacts** have been created. An October 2025 update added inline editing for 3–4x faster updates via targeted replacement instead of full regeneration. Artifacts support MCP integration, persistent storage (20 MB per artifact), and publishing via an Artifact Catalog at claude.ai/catalog/artifacts.

**Projects** are persistent workspaces with custom instructions, a **200,000-token knowledge base** (~500 pages), and grouped conversation history. Documents uploaded once are referenced across all chats in the project. RAG mode activates automatically when knowledge approaches context limits. September 2025 added role-based permissions (private, view, edit), bulk invitations, and chat search across history. Free users get 5 projects; paid plans get unlimited.

These are distinct from Claude Code: Artifacts create individual content pieces in a visual canvas; Claude Code operates on entire codebases via terminal.

---

## 16. Claude Cowork brings agentic capabilities to knowledge workers

**Claude Cowork is an official Anthropic product** launched as a research preview on January 12, 2026. It runs as a tab in the Claude Desktop app alongside Chat and Code, executing work in a **sandboxed virtual machine** (Apple's Virtualization Framework on macOS) on the user's computer. Cowork analyzes requests, creates plans, breaks work into subtasks, coordinates parallel sub-agents, and delivers outputs to the local filesystem.

On January 30, 2026, Anthropic launched **11 open-source plugins** covering productivity, enterprise search, marketing, sales, finance, data analysis, legal, customer support, product management, biology research, and a meta-plugin for creating new plugins. Plugins combine skills, connectors, slash commands, and sub-agents. Available on GitHub at `github.com/anthropics/knowledge-work-plugins`.

Cowork is available to all paid plan subscribers (Pro at $20/month through Enterprise) on macOS and Windows desktop apps. Conversation history is stored locally. As Simon Willison noted, Cowork is essentially "Claude Code wrapped in a less intimidating interface with a filesystem sandbox configured for you" — designed for non-developers doing knowledge work like project management, research synthesis, financial analysis, and document creation.

---

## 17. LiteLLM proxies Claude Code requests to alternative model providers

LiteLLM is a third-party proxy translating between Anthropic's Messages API format and 100+ providers (OpenAI, Google, Azure, etc.). Setup involves installing LiteLLM (`pip install 'litellm[proxy]'`), creating a `config.yaml` with model definitions, starting the proxy (`litellm --config config.yaml`), and pointing Claude Code at it:

```bash
export ANTHROPIC_BASE_URL="http://0.0.0.0:4000"
export ANTHROPIC_AUTH_TOKEN="$LITELLM_MASTER_KEY"
claude --model gpt-4o  # or gemini-3.0-flash-exp, azure-gpt-4, etc.
```

Provider-specific pass-through endpoints exist for **Bedrock** (`ANTHROPIC_BEDROCK_BASE_URL`) and **Vertex AI** (`ANTHROPIC_VERTEX_BASE_URL`). Authentication can use static API keys or dynamic helper scripts via `apiKeyHelper` in settings. Advanced features include load balancing with automatic failover, per-team usage tracking and budgets, and routing to local models via Ollama or LM Studio. Tools like ccproxy add intelligent routing rules — sending thinking requests to one model and background tasks to cheaper ones. The gateway must expose `/v1/messages` (Anthropic), `/invoke` (Bedrock), or `:rawPredict` (Vertex) endpoints.

---

## 18. Figma integration offers three paths from design to code

**Option A — Remote MCP Server** (no desktop app required): `claude mcp add --transport http figma https://mcp.figma.com/mcp`, then authenticate via `/mcp` → figma → Authenticate. Link-based: provide Figma URLs in prompts.

**Option B — Desktop MCP Server** (selection-based, richer features): Enable in Figma Desktop's Dev Mode (Shift+D) inspect panel. Server runs at `http://127.0.0.1:3845/mcp`. Select frames/components directly in Figma, then ask Claude to generate code.

**Option C — Claude Code Plugin** (simplest): `claude plugin install figma@claude-plugins-official`. Includes both MCP servers plus Agent Skills.

The Figma MCP provides tools for `get_code` (generates code, default React + Tailwind, customizable), `get_variables` (extracts design tokens), `get_code_connect_map` (maps Figma components to codebase), and screenshots. Specify technology stack clearly ("Next.js 14 with Tailwind CSS and TypeScript"), start with individual screens, name Figma frames descriptively, and use Code Connect for consistency. Limitations include no surgical updates to existing code, no animation conversion, and complex multi-frame flows requiring manual assembly.

---

## 19. Preventing hallucinations requires verification-first workflows

**Test-driven development is the single most effective counter-measure.** Have Claude build the test first, then implement against it. Tests provide concrete, mechanically verifiable expectations that catch hallucinated behavior immediately.

Anthropic's official **4-phase workflow**: Explore (Plan Mode, read-only analysis) → Plan (explicit implementation plan, written to files) → Implement (Normal Mode) → Verify & Commit (tests, linters, type checkers). The official docs state: "Include tests, screenshots, or expected outputs so Claude can check itself. This is the **single highest-leverage thing** you can do."

Critical anti-patterns to avoid:

- **The Correction Spiral**: If you've corrected Claude more than twice on the same issue, run `/clear` and start fresh — a clean session with a better prompt almost always outperforms accumulated corrections
- **Context Degradation**: Quality degrades after extended conversations; compact or restart
- **Autonomous Rabbit Holes**: Don't let Claude run autonomously without scoping — it can burn tokens on unproductive paths, creating "negative productivity"
- **The Over-Specified CLAUDE.md**: Too-long rules files cause Claude to ignore critical instructions

Additional techniques: give Claude permission to say "I don't know," restrict to provided documents for factual tasks, use PostToolUse hooks for automatic linting/formatting, and run different models for different task types.

---

## 20. Rules files work best when lean, modular, and contextually loaded

The **critical constraint**: Claude Code's system prompt already contains ~50 instructions, consuming nearly a third of the ~150–200 instruction limit frontier models reliably follow. Your CLAUDE.md must be lean — **under 60–80 lines** is a good benchmark.

**What to include**: tech stack, project structure (especially in monorepos), build/test/lint commands (exact commands Claude will run), and non-obvious gotchas. **What to exclude**: formatting rules (use linters), instructions Claude already follows, generic advice ("write clean code"), and rarely-used specifics.

**Break large files into contextual pieces** using two mechanisms:

1. **`.claude/rules/` directory** (v2.0.64+): All markdown files here load automatically at the same priority as main CLAUDE.md. Different teams can own different files (code-style.md, testing.md, security.md) — no merge conflicts
2. **Subdirectory CLAUDE.md files**: `src/auth/CLAUDE.md` loads on-demand only when Claude works in `src/auth/`, keeping the root file lean while providing deep context where needed

For critical rules, use emphatic language ("IMPORTANT: Never modify the migrations folder directly") — but sparingly, since marking everything as important makes nothing important. Tools like **claude-rules-doctor** detect dead rule files by checking if paths/globs actually match repo files. Periodically ask Claude to review and suggest improvements to your CLAUDE.md.

---

## 21. Learning from corrections turns manual fixes into permanent rules

The most complete implementation is the **claude-reflect plugin** (by BayramAnnakov), which captures corrections via hooks, detects patterns (corrections like "no, use X", positive feedback like "perfect!", explicit "remember:" markers), assigns confidence scores (0.60–0.95), and queues them for review:

```bash
claude plugin marketplace add bayramannakov/claude-reflect
/reflect              # Process queued learnings with review
/reflect --scan-history  # Scan all past sessions
/reflect --dedupe     # Consolidate similar entries
/reflect-skills       # Discover patterns → reusable skills
```

**Build your own** by creating `.claude/commands/learn.md`:
```markdown
---
description: Compare AI-generated code with manual corrections and update rules
argument-hint: [file-path]
---
1. Run `!git diff HEAD -- $ARGUMENTS` to see changes
2. Analyze patterns in corrections (style issues, architecture violations, conventions)
3. Categorize → update appropriate .claude/rules/ files
4. Present findings for approval before updating
5. Check for duplicates in existing rules
```

The **"Procedural Knowledge" pattern** has every skill include a "Failed Attempts" section. The self-improving loop: reflect on failures → abstract the general pattern → generalize into a reusable decision framework → write to CLAUDE.md. **Prompt learning / meta-prompting** automates this: run Claude on test tasks, evaluate outputs with LLM evals, meta-prompt generates optimized rules, test again, iterate until improvement plateaus.

---

## 22. Hooks and sub-agents automate testing and security at generation time

**PostToolUse hooks for auto-testing** run tests after every file write:
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{"type": "command", "command": "cd \"$CLAUDE_PROJECT_DIR\" && npm test -- --bail 2>&1 | head -50"}]
  }]
}
```

**Stop hooks for auto code review** trigger a sub-agent with a "very critical mindset" to review modified files when Claude finishes. Return exit code 2 to block completion and force corrections — asking the main agent to "mark its own homework" is ineffective; use an independent reviewer. The **TaskCompleted hook** enforces that tests pass and lint checks are clean before any task can be marked complete.

**PreToolUse security hooks** block dangerous operations:
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "python3 -c \"import json,sys; cmd=json.load(sys.stdin)['command']; sys.exit(2) if any(x in cmd for x in ['rm -rf','DROP TABLE','.env']) else 0\""}]
  }]
}
```

**Prompt-based security hooks** send tool inputs to Haiku for context-aware evaluation of credential exposure, SQL injection, and XSS patterns. **Trail of Bits security skills** provide 12+ professional code auditing capabilities including CodeQL, Semgrep, variant analysis, and differential review.

For CI/CD, the **claude-code-action** GitHub Action automates PR reviews:
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Review this PR for bugs and security issues."
```

The **PubNub pipeline pattern** chains sub-agents: pm-spec (writes requirements) → architect-review (validates design, produces Architecture Decision Record) → implementer-tester (implements code, writes tests, updates docs). Each sub-agent lives in `.claude/agents/` with focused tools and prompts.

---

## Conclusion

Claude Code in early 2026 has matured into a layered platform where **configuration, automation, and extensibility operate independently but compose powerfully**. The most impactful practices are: keep CLAUDE.md under 80 lines with contextual `.claude/rules/` files for specifics; use TDD and PostToolUse hooks to verify every change automatically; leverage Plan Mode before complex implementations; delegate research to sub-agents to preserve main context quality; and build correction-learning workflows that convert manual fixes into permanent rules. The emergence of Skills as an evolution beyond slash commands, Agent Teams for parallel collaboration, and MCP Tool Search for efficient tool management signals that the platform is shifting toward increasingly autonomous, multi-agent workflows — while hooks and the permission system ensure deterministic safety guarantees regardless of model behavior.