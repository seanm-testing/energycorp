---
name: create-pr
description: Creates a pull request with the specified changes. Stages all changes, commits with a clear message, pushes to a new feature branch, and creates a GitHub PR with a detailed description covering what it does, API spec, permissions, and frontend integration instructions.
allowed-tools: Bash, mcp__github__create_pull_request, mcp__github__create_branch, mcp__github__push_files, mcp__github__list_pull_requests, mcp__github__get_pull_request
context: fork
agent: general-purpose
---

# Create Pull Request Skill

## Workflow

### Step 1: Analyze Changes

1. Run `git status` and `git diff --stat` to understand what will be included.
2. Run `git log --oneline -10` to see recent commit style.
3. Determine the branch name: use the one provided by the user, or derive one from the changes.

### Step 2: Draft PR Artifacts

1. Draft the commit message, PR title, and PR description body following the PR Content format below.

### Step 3: Execute

1. **Stage all changes**: `git add -A`
2. **Commit locally**: `git commit -m "<message>"` (use a HEREDOC for multi-line messages)
3. **Push branch to GitHub via MCP** (do NOT use `git push`):
   - Use `mcp__github__push_files` to push the changed files to the branch on GitHub. This creates the branch and commits in one step. Provide `owner`, `repo`, `branch`, `message`, and `files` (each with `path` and `content` read from the working tree).
   - For the `files` parameter, read each changed file's content and include it. Use `git diff master --name-only` to get the list of changed files.
4. **Create the GitHub PR**: Use `mcp__github__create_pull_request` to open a pull request against the `master` branch. If the MCP tool is unavailable, fall back to `gh pr create` via Bash.
5. **Return the PR URL** when done.

## PR Content

The PR should include:

- **Title**: A concise summary of the feature (e.g., "Add dashboard summary endpoint for manager view")
- **Description** with these sections:
  - **What it does**: Brief overview of the feature or fix
  - **API Spec**: Endpoint path, HTTP method, request/response format, status codes
  - **Permissions**: Which roles can access it (Admin/Manager/Operator) and the permission class used
  - **Frontend Integration**: Instructions for the frontend team on how to consume the new endpoint, including example Axios calls and expected response shapes

## Error Handling

- If there are no changes to commit, stop and report that there is nothing to do.
- If the branch already exists on the remote, append a short suffix (e.g., `-v2`) and retry.
- If the PR creation fails, show the error and suggest manual steps.
