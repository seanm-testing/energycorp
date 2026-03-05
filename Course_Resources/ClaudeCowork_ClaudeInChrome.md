# Claude Cowork and Claude in Chrome: a security-first deep dive

**Anthropic's two newest agentic features — Claude Cowork and Claude in Chrome — give Claude unprecedented ability to act on your computer and in your browser, creating powerful productivity gains alongside serious security risks that organizations must actively manage.** Both tools represent Anthropic's push to transform Claude from a conversational assistant into an autonomous agent that reads files, executes code, navigates websites, and fills forms. While Anthropic has built layered defenses including VM sandboxing, content classifiers, and permission gates, independent security researchers demonstrated a file exfiltration vulnerability just two days after Cowork's launch. Organizations considering adoption should treat these tools as early-stage, high-capability software that demands strict governance, scoped access, and active monitoring.

---

## What Cowork and Chrome actually do

**Claude Cowork**, launched January 12, 2026 as a research preview, brings the agentic power of Claude Code to non-developers. Users grant Claude access to a local folder, and Claude can then **read, edit, create, and permanently delete files** within it. Rather than back-and-forth chat, Cowork operates more like delegating to a coworker: you describe a task, Claude builds a plan, breaks it into subtasks, and executes them — often spawning multiple sub-agents working in parallel. It produces polished outputs like Excel spreadsheets with working formulas, PowerPoint presentations, formatted PDFs, and Word documents through a set of pre-built Agent Skills. Users can queue multiple tasks, set scheduled recurring jobs (daily, weekly, monthly), and connect Claude to external services via MCP connectors (Google Drive, Gmail, Slack, GitHub, DocuSign, FactSet, and others). The system runs inside a **virtual machine** — Apple's Virtualization Framework on macOS, Hyper-V on Windows — that isolates Claude's code execution from the host OS.

**Claude in Chrome** is a browser extension (currently in beta for all paid plans) that lets Claude **navigate websites, click buttons, fill forms, run JavaScript, and take screenshots** within your browser. It operates as a side panel in Chrome, working across multiple tabs simultaneously. Users can record workflows for reuse, schedule recurring browser tasks, and choose between "ask before acting" and fully autonomous modes. The extension connects to both Claude Code (for build-test-debug loops) and Claude Desktop/Cowork (as a web research layer that feeds into document creation). When paired with Cowork, Chrome handles web navigation and data gathering while Cowork produces finished files — eliminating copy-paste between browser and desktop.

Both tools are available on **Pro ($20/month), Max ($100–200/month), Team ($125/user/month), and Enterprise** plans, though browser interactions and Cowork tasks consume significantly more compute than regular chat. A single complex Cowork task may use the equivalent of **50–100 standard messages**.

---

## The agent skills and plugin ecosystem powering these tools

Cowork's capabilities extend far beyond basic file manipulation through a layered extensibility stack. **Pre-built Agent Skills** handle common document creation — PowerPoint, Excel, Word, and PDF — using a progressive loading architecture that keeps token costs low. Skills load metadata at startup (~100 tokens each), full instructions only when triggered (under 5,000 tokens), and execute bundled scripts without loading code into the context window. This means Skills can bundle effectively unlimited reference material without degrading performance.

**Custom Skills** let organizations package domain expertise as reusable modules. These are filesystem-based directories containing a SKILL.md instruction file plus optional scripts and templates. Skills can reference MCP tools using fully qualified names (e.g., `BigQuery:bigquery_schema`) and compose together for complex workflows. However, **custom Skills do not sync across surfaces** — Skills uploaded to claude.ai are not automatically available in Claude Code or Cowork, and vice versa.

The **plugin system**, launched January 30, 2026, bundles Skills, connectors, slash commands, and sub-agents into installable packages. Anthropic released 11 open-source starter plugins covering sales, legal, finance, marketing, HR, engineering, design, operations, and data analysis. Enterprise customers can build **private plugin marketplaces** connected to private GitHub repositories, with per-user provisioning (auto-install, available, or blocked). A major February 24 enterprise update added 13 new MCP connectors, 10+ department-specific plugins, and cross-app workflows between Excel and PowerPoint.

For the Chrome extension specifically, Claude has built-in understanding of popular platforms — Slack, Google Calendar, Gmail, Google Docs, GitHub — enabling natural-language commands like "schedule a meeting" without detailed instructions. The extension exposes browser tools via MCP (`claude-in-chrome`), enabling Claude Code to read console errors, DOM state, and network requests during development.

---

## How the architecture connects Claude's product ecosystem

Cowork and Claude Code share **identical agentic architecture** — the "Master Agent Loop," a single-threaded while-loop control pattern built on the Claude Agent SDK. Cowork was reportedly built by Claude Code itself in approximately 10 days. The key architectural difference: Claude Code is a CLI tool for developers with full system access, while Cowork wraps the same engine in a GUI with a preconfigured filesystem sandbox for non-technical users.

The VM isolation layer is substantive. On macOS, Cowork downloads and boots a custom Linux root filesystem via Apple's Virtualization Framework (VZVirtualMachine). On Windows, it uses Hyper-V with a dedicated VM instance managed by CoworkVMService. Files appear inside the container at paths like `/sessions/zealous-bold-ramanujan/mnt/[folder-name]`. Code runs inside this isolated space, not directly on the host OS — though Claude can make real changes to mounted files.

Claude in Chrome connects to both Cowork and Claude Code via Chrome's **Native Messaging API**. For Claude Code, launch with `claude --chrome` or use `/chrome` within a session (requires extension v1.0.36+ and Claude Code v2.0.73+). For Cowork/Desktop, enable the Chrome connector in Settings → Connectors. This creates a three-layer integration: Chrome handles web browsing, Cowork handles file creation and local execution, and Claude Code handles development workflows. Data flows between these surfaces within a session — Chrome can gather competitor pricing from websites, and Cowork can compile it into a formatted spreadsheet without user intervention.

The **MCP (Model Context Protocol)** layer provides the connective tissue. Cowork supports both web-based connectors (Google Drive, Slack) that work across platforms and desktop extensions (local MCP servers) specific to the desktop app. Enterprise customers gained 13+ MCP connectors in February 2026, including Google Workspace, DocuSign, Apollo, FactSet, SimilarWeb, and others. MCP Apps — interactive UI components rendered in sandboxed iframes — add dashboard and form capabilities directly within the agent interface.

---

## Security and safety: the critical assessment

This is where organizations need to pay closest attention. Anthropic has built genuine, multi-layered defenses — but independent research has exposed significant gaps, and Anthropic itself acknowledges these risks are "non-zero."

### Anthropic's defense layers

Anthropic deploys **six primary safety mechanisms** across Cowork and Chrome. First, reinforcement learning trains Claude to recognize and refuse malicious instructions even when they appear authoritative. Second, content classifiers scan all untrusted content entering Claude's context and flag potential prompt injections. Third, granular permissions give users control over file access and browser actions. Fourth, site blocklists prevent Chrome from accessing financial services, banking, investment platforms, cryptocurrency exchanges, adult content, and pirated content. Fifth, action confirmations require explicit approval before destructive actions (file deletion, purchases, account creation). Sixth, ongoing red teaming — both internal researchers and external challenges — continuously probes for vulnerabilities.

For Chrome specifically, Anthropic's red-teaming across **123 test cases and 29 attack scenarios** showed attack success rates dropping from **23.6% without mitigations to 11.2% with initial mitigations**, and further to approximately **1% with Claude Opus 4.5** and updated safeguards. The browser-specific "challenge" attack set dropped from 35.7% to 0%. These are meaningful improvements — and notably, Anthropic publishes quantified metrics by surface that OpenAI and Google have not matched.

### The PromptArmor file exfiltration vulnerability

Two days after Cowork launched, security firm PromptArmor demonstrated a **file exfiltration attack via indirect prompt injection**. The attack chain: an attacker plants a .docx file containing hidden instructions (1-point white font, 0.1 line spacing) in a folder Cowork accesses. When Claude processes the file, the injection triggers a curl command that uploads the victim's files to the attacker's Anthropic account via the Files API. **The attack requires no user approval** because `api.anthropic.com` is whitelisted in the VM's network restrictions — creating an exfiltration channel through the sandbox itself.

Critically, this vulnerability was **first identified by researcher Johann Rehberger in October 2025** and reported via HackerOne. Anthropic acknowledged it but did not fix it before shipping Cowork. Both Haiku and Opus 4.5 were successfully exploited, demonstrating that this is an architectural vulnerability, not a model intelligence gap. Anthropic responded with plans for VM updates to address the API interaction, but the incident reveals a concerning pattern: shipping a known vulnerability in a consumer-facing product.

### The "lethal trifecta" and structural risks

Security researcher Simon Willison identified that Cowork embodies a **"lethal trifecta"** — three elements that make AI systems dangerous when combined: access to private data, exposure to untrusted content (web pages, emails, documents), and the ability to communicate externally (APIs, network requests). Cowork has all three by design.

Zenity Labs' threat analysis of Claude in Chrome identified additional structural risks. The extension is **always authenticated** with no opt-in toggle — operations inherit the user's logged-in sessions across all sites. In testing, Claude navigated to Wikipedia despite it not being in the approved plan, demonstrating that "ask before acting" is a **soft guardrail** subject to plan drift. Zenity also flagged "approval fatigue" — users stop carefully verifying Claude's intent after repeated permission prompts — and the risk of OAuth token exposure through Claude's ability to read console logs and web requests. Most concerning, Claude's JavaScript execution capability could effectively enable **cross-site scripting as a service** if manipulated through prompt injection.

LayerX Security separately discovered a **CVSS 10/10 vulnerability** in Claude Desktop Extensions (DXT), which run unsandboxed with full system privileges. Their demonstration showed an attacker creating a Google Calendar event with a malicious payload; when a victim asks Claude to check their calendar, the payload chains from a low-risk connector to high-risk code execution, compromising the device. Anthropic reportedly responded that DXT is "designed as a local development tool" and decided not to fix it at the time of reporting.

### Enterprise-critical gaps

Several security gaps are particularly concerning for enterprise adoption:

- **Cowork activity is NOT captured in audit logs, Compliance API, or data exports.** This is a fundamental barrier for regulated industries. Anthropic explicitly warns: "Do not use Cowork for regulated workloads."
- **Conversation history is stored locally only** — not centrally manageable by administrators. There is no granular role-based access control, only an organization-wide toggle.
- **Cross-app data flow** between Claude in Excel and Claude in PowerPoint during Cowork sessions means data from one application may flow into another without explicit user direction, creating potential data leakage between sensitivity contexts.
- **The MCP ecosystem** represents a software supply chain vulnerability — repository poisoning, typosquatting, and dependency confusion attacks apply to plugins and connectors just as they do to npm packages.
- **Network egress permissions don't apply to the web search tool**, which can access the broader web regardless of network settings configured by admins.

### What Anthropic's own safety docs explicitly warn about

Anthropic's official safety documentation is unusually candid about limitations. Key warnings from official sources include: "While we've enacted these safety measures to reduce risks, the chances of an attack are still non-zero." Users "remain responsible for all actions taken by Claude" including content published, purchases made, data modified, and actions taken by scheduled tasks. "Agent safety is still an active area of development in the industry." Output filters that block sensitive data patterns like auth tokens "are not a security boundary." And for Chrome's autonomous mode: "Due to the nature of LLMs, we can't guarantee that Claude will request permission" before high-risk actions.

---

## Intended workflows and realistic use cases

Cowork excels at **file-heavy knowledge work**: organizing downloads by sorting and renaming files, creating expense reports from receipt screenshots, synthesizing research from scattered notes into formatted reports, batch-renaming files with consistent date patterns, and producing spreadsheets with VLOOKUP formulas and conditional formatting. The scheduled tasks feature enables recurring automations like weekly report generation, daily email cleanup, or periodic data compilation — though Anthropic advises starting with low-risk tasks before automating anything consequential.

Chrome's strongest use cases include **pulling metrics from analytics dashboards**, organizing files in Google Drive, comparing products across websites into structured spreadsheets, logging sales calls to CRMs, and preparing meeting briefs from calendar and email context. The build-test-debug loop with Claude Code is genuinely powerful for developers: build in the terminal, verify in the browser, read console errors, and fix code without context-switching.

The Cowork-plus-Chrome combination is designed for workflows like competitive intelligence (Chrome visits competitor sites, Cowork builds comparison decks) and research synthesis (Chrome gathers web data, Cowork produces formatted reports). Enterprise adopters like Spotify report a **90% reduction in engineering migration time**, while Novo Nordisk claims **10+ weeks of documentation reduced to 10 minutes**.

---

## How Cowork compares to Cursor, Devin, and Codex

Cowork occupies a distinct niche in the AI agent landscape. **Cursor** is a VS Code fork focused on "flow state" coding with fast autocomplete — it has no sandbox and auto-selects 50+ context files per request without visibility, consuming up to 400,000 tokens per agent operation. **Devin** is a fully autonomous coding agent operating in its own cloud sandbox, accessible via Slack, with the highest autonomy level but narrowly focused on engineering tasks. **GitHub Copilot** remains primarily a suggestion-based pair programmer with the most mature enterprise governance (SSO, SCIM, SOC 2, IP indemnity). **OpenAI Codex** runs in cloud sandboxes bundled with ChatGPT subscriptions, offering what some analysts call "the strongest" task isolation.

On security specifically, Cowork's constrained autonomy model — explicit folder permissions, mandatory approval gates, VM isolation — is **more secure than Cursor's uncontained agent mode** but **less isolated than Codex's cloud sandboxes** (which have no local filesystem access at all). Cowork's unique position is extending agent capabilities to non-coding knowledge work, which none of these competitors target. The trade-off: broader capability surface means broader attack surface.

| Feature | Cowork | Codex | Copilot | Devin | Cursor |
|---------|--------|-------|---------|-------|--------|
| Sandbox | Local VM | Cloud container | GitHub environment | Cloud container | None |
| Filesystem isolation | Mount-based | Full container | GitHub-scoped | Full container | No |
| Human approval gates | Mandatory | Configurable | PR-based | Optional | None |
| Enterprise compliance | No audit logs | SOC 2 | SOC 2, SCIM, SSO | SOC 2 | Privacy modes |
| Non-coding workflows | Yes | No | No | No | No |

---

## Current limitations and known issues

Cowork remains a **research preview** with significant rough edges. There is **no memory across sessions**, no cross-device sync, and the desktop app must remain open during tasks. On Windows, serious infrastructure issues persist: Cowork's HNS virtual network can permanently break WSL2 networking, it uses the 172.20.208.0/20 subnet which conflicts with many corporate VPN networks, and extreme NVMe I/O usage has been reported on multiple machines. One community observer characterized the Windows experience as "a product marketed at the people least equipped to debug it when it breaks."

Chrome's limitations include slower-than-manual execution for many tasks, incomplete processing on long lists (Claude may stop mid-task), variable results due to probabilistic behavior, and no memory between sessions. The extension operates as "pure Claude" — without Projects, additional MCP tool connections beyond the built-in browser tools, or cross-session memory. Chrome is only supported on Google Chrome and Microsoft Edge on desktop — not Brave, Arc, or any mobile browser.

Both tools are **not available through third-party providers** (Amazon Bedrock, Google Cloud Vertex AI, Microsoft Foundry) — they require a direct Anthropic subscription. Pro plan users are limited to Haiku 4.5 in Chrome, while Max, Team, and Enterprise users can choose between Haiku 4.5, Sonnet 4.5/4.6, and Opus 4.5/4.6.

---

## Actionable recommendations for safe organizational adoption

Organizations evaluating these tools should approach them as powerful but immature capabilities requiring active governance. The following recommendations synthesize Anthropic's official guidance, independent security research, and enterprise best practices.

**Before deployment**, establish a formal evaluation process. Pilot with a small group of non-sensitive workflows. Configure restrictive site allowlists in Chrome before expanding access. Confirm that your compliance requirements can tolerate the absence of audit logs — if they cannot, defer Cowork adoption until Anthropic adds compliance API support. Assess whether your VPN or corporate network uses the 172.20.208.0/20 subnet, which conflicts with Cowork on Windows.

**During deployment**, enforce these controls:

- **Create dedicated working folders** for Cowork with only the files needed for each task — never grant access to home directories or folders containing credentials, financial documents, or sensitive records. Maintain backups of all files in Cowork-accessible folders.
- **Use a separate browser profile** for Claude in Chrome — one without access to banking, healthcare, government, or other sensitive accounts. This is the single most effective mitigation for Chrome's JavaScript execution risks.
- **Start with "ask before acting" mode** in Chrome and review plans carefully before approval. Reserve autonomous mode for actively supervised, low-risk tasks on thoroughly trusted sites only.
- **Vet all MCP connectors and plugins** as you would vet third-party software. Audit SKILL.md files, scripts, and resources for unexpected network calls, file access patterns, or operations that don't match stated purposes. Stick to Anthropic's verified extensions and your organization's private plugin marketplace.
- **Do not schedule tasks** that access sensitive files, send messages, make purchases, or take hard-to-undo actions. Review outputs after every scheduled run.
- **Monitor for prompt injection indicators**: Claude discussing unrelated topics, accessing unexpected resources, requesting sensitive information unprompted, or scope creeping beyond the assigned task. Stop immediately and report to security-reports@anthropic.com.
- **Disable cross-app workflows** (Excel/PowerPoint add-ins) during Cowork sessions involving sensitive data, as data may flow between applications without explicit direction.

**At the governance level**, enterprise administrators should disable Chrome by default (it's already off by default for Enterprise plans), enable for specific user groups only, and implement allowlists before blocklists — it's safer to approve known-good sites than to try blocking all bad ones. Establish clear policies about what types of work are permitted in Cowork versus standard Claude chat. Document that users remain legally responsible for all actions Claude takes on their behalf, including respecting third-party terms of service restrictions on automated access.

## Conclusion

Claude Cowork and Claude in Chrome represent a genuine capability frontier — autonomous AI agents that operate on your files and in your browser with meaningful productivity gains. Anthropic's security approach is more transparent than competitors, with published attack success rates and candid risk acknowledgments. But transparency about risk is not the same as absence of risk. The PromptArmor file exfiltration exploit, the "lethal trifecta" architecture, the absence of audit logs, and the ~1% residual attack success rate in Chrome all demand that organizations treat these tools as high-capability, high-risk software requiring active governance rather than passive trust. The most important insight: **the security boundary in these tools is ultimately the user's judgment and organizational controls, not the AI's built-in defenses alone.** Organizations that deploy dedicated working folders, separate browser profiles, restrictive allowlists, and active monitoring will capture substantial value. Those that grant broad access and trust the defaults are accepting risks that Anthropic itself explicitly warns against.