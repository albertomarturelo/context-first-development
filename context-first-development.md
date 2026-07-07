# Context-First Development (CFD): A Methodology for AI-Assisted CLI Development

> *"The most expensive code an AI agent can write is code written without context."*

## Introduction: The Problem Nobody Wants to Admit

There's an elephant in the room of AI-assisted development. Every time you start a new session with your AI agent — whether it's Claude Code, Gemini CLI, or any terminal tool — you start from scratch. The model doesn't remember the architectural decisions you made yesterday. It doesn't know why you chose PostgreSQL over MongoDB. It doesn't understand that your team decided to use the Repository pattern for specific testability reasons.

The result is predictable: **the agent generates technically correct but contextually incorrect code**. And you end up spending more time correcting the model than writing the code yourself.

This problem scales in direct proportion to project size. In a 50-file project, the model can scan everything and understand the structure. In a 500-file project, scanning consumes tokens exponentially and the model starts losing coherence. In a 5,000-file project — where any serious production project lives — the model is essentially blind.

The solution isn't a model with more context. GPT-4 Turbo has 128K tokens. Claude has 200K. Gemini reaches 2M. And yet, the problem persists. **Because the problem isn't context capacity — it's context quality.**

This article proposes **Context-First Development (CFD)**: a methodology for structuring code repositories so that AI agents can operate with persistent, accurate, and efficient context. It's not a framework. It's not a tool. It's a work discipline that transforms your repository into a living knowledge base that any agent can consume.

---

## The Current Landscape: What Exists and Why It's Not Enough

Before proposing something new, let's understand what the industry has built so far.

### CLAUDE.md and the First Generation of "Agent Instructions"

Anthropic introduced the concept of `CLAUDE.md` as an instruction file that Claude Code reads automatically when starting a session. The idea is simple: a Markdown file at the project root that tells the model how to behave.

[Anthropic's official best practices](https://code.claude.com/docs/en/best-practices) recommend keeping the file between 100-200 lines and applying a strict rule: *"For each line, ask yourself: would removing this cause Claude to make mistakes? If not, cut it."*

The problem is that most CLAUDE.md files end up being lists of build and lint commands. An [academic study from September 2025](https://arxiv.org/abs/2509.14744) analyzed 253 CLAUDE.md files from 242 repositories and found that 77.1% only contained Build/Run instructions, 71.9% implementation details, and a mere 8.7% mentioned security. **The industry is using the most powerful context file available to do what a Makefile already did.**

### AGENTS.md: The Standardization Attempt

In July 2025, Sourcegraph's Amp team launched [AGENTS.md](https://agents.md/) — an open format designed to be a "README for agents" that works with any tool: OpenAI Codex, Google Jules, Cursor, Aider, Gemini CLI. By February 2026, over 40,000 open source repositories had adopted it.

AGENTS.md proposes one file per directory level (ideal for monorepos), with a recommended limit of 150 lines and content oriented toward: project description, architecture, commands, conventions, and navigation hints.

It's a good step toward interoperability, but it suffers from the same fundamental problem: **it's a static file that doesn't scale with project complexity.**

### Cole Medin's Template: Practical Context Engineering

[Cole Medin](https://github.com/coleam00/context-engineering-intro) published a template repository that goes a step further. Its structure includes:

- `CLAUDE.md` with project rules
- `.claude/commands/` with custom slash commands
- `examples/` with patterns for the model to follow
- `PRPs/` (Product Requirements Prompts) — specifications the model executes

This approach is significantly more sophisticated because it introduces the idea of **commands as workflow** and **examples as context**. But it remains a template that each team must adapt without a clear methodology for when and how to evolve each piece.

### Spotify: 1,500 PRs in Production with Claude Code

Spotify published a [three-part series](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) in November-December 2025 documenting their experience with coding agents in production. Key findings:

- Claude Code was their top-performing agent
- They executed ~50 automated migrations
- Over 1,500 AI-generated PRs merged
- Critical discovery: Claude Code works better with **end-state descriptions** rather than step-by-step instructions

This last point is fundamental and we'll incorporate it into CFD: **context should describe the "what" and "why", not the "how"**.

### ADRs: The Missing Piece

[Chris Swan wrote in July 2025](https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/) about the connection between Architecture Decision Records and AI agents. His central argument: ADRs provide structured, natural-language context that is inherently LLM-friendly. Each documented decision includes context, evaluated alternatives, consequences, and status — exactly what a model needs to understand *why* the code is the way it is.

[Josh Rotenberg published a complete ADR system](https://gist.github.com/joshrotenberg/a3ffd160f161c98a61c739392e953764) designed specifically for Claude integration. [Piethein Strengholt built an agent](https://piethein.medium.com/building-an-architecture-decision-record-writer-agent-a74f8f739271) that automates ADR creation. But nobody has integrated ADRs as the central piece of an AI development methodology.

### Addy Osmani: The "Specs First" Workflow

Addy Osmani, engineering lead at Google Chrome, [proposed a workflow](https://addyosmani.com/blog/ai-coding-workflow/) that can be summarized as: **specs first, then plan, then code**. He also coined the [70/30 rule](https://addyo.substack.com/p/the-ai-native-software-engineer): AI completes ~70% of the task, but the last 30% (edge cases, production readiness) requires human expertise.

### The Academic Research

Three fundamental papers from 2025:

1. **"On the Use of Agentic Coding Manifests"** ([arXiv:2509.14744](https://arxiv.org/abs/2509.14744)) — Empirical analysis of 253 CLAUDE.md files.
2. **"Agent READMEs: An Empirical Study"** ([arXiv:2511.12884](https://arxiv.org/html/2511.12884v1)) — 2,303 context files from 1,925 repositories. Conclusion: these files are "not static documentation but complex, difficult-to-read artifacts that evolve like configuration code."
3. **"Context Engineering for Multi-Agent LLM Code Assistants"** ([arXiv:2508.08322](https://arxiv.org/abs/2508.08322)) — Proposes multi-agent architectures with semantic retrieval.

### What's Missing

All of the above are valuable pieces of a puzzle that nobody has assembled. There are configuration files. There are templates. There are case studies. There are academic papers. But **there is no cohesive, CLI-first methodology that an individual developer or small team can adopt tomorrow** and that scales from a 10-file project to a 10,000-file one.

That's Context-First Development.

---

## Context-First Development: The Six Principles

CFD is built on six non-negotiable principles. These aren't suggestions — they're design constraints.

### Principle 1: Context Before Code

Before writing the first line of code in any session with an AI agent, context must be resolved. This means the model must be able to answer these questions without scanning source code:

- What is the project's architecture?
- What decisions have been made and why?
- What conventions are followed?
- What is the current state of work in progress?

If the model needs to read 50 files to answer any of these questions, your context is broken.

### Principle 2: Single Source of Truth (SSOT)

Every piece of project knowledge must exist in exactly one place. If the architecture is documented in CLAUDE.md, in an ADR, in a README, and in code comments, you have four sources that will inevitably desynchronize. The model won't know which to trust.

CFD defines a clear hierarchy: the root file (CLAUDE.md or AGENTS.md) is an **index** that references specialized documents. It never duplicates content.

### Principle 3: Hierarchical Context Architecture

Context is organized in layers, from most general to most specific:

```
Level 0: Root file (CLAUDE.md / AGENTS.md)        → ~100-150 lines
Level 1: Domain documents (docs/)                   → Architecture, stack, conventions
Level 2: Decisions (docs/decisions/)                 → Individual ADRs
Level 3: Module context (CLAUDE.md per folder)       → Area-specific instructions
```

The model only needs to read Level 0 to orient itself. It dives into lower levels when the task requires it. This minimizes token consumption per session.

### Principle 4: Decisions as First-Class Citizens

Every significant technical decision is documented in an ADR (Architecture Decision Record) with a strict format:

```markdown
# ADR-NNN: Decision Title

## Status
Accepted | Superseded by ADR-XXX | Deprecated

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're actually doing?

## Alternatives Considered
What other options were evaluated and why were they rejected?

## Consequences
What becomes easier or more difficult to do because of this change?
```

This isn't bureaucracy — it's **persistent memory**. When you start a new session and the model reads `docs/decisions/007-use-repository-pattern.md`, it instantly understands why the code is structured that way. Without the ADR, the model might suggest refactoring toward a different pattern, wasting your time and its tokens.

### Principle 5: English as Context Language

All technical context is written in English. This isn't elitism — it's token efficiency.

LLM tokenizers (both Anthropic's and Google's) are optimized for English. The same information in Spanish can consume 20-40% more tokens than in English. In a context file that's loaded in every session, that adds up quickly.

Practical rule: code, file names, ADRs, context documents, and CLAUDE.md are written in English. PR comments and team communication can be in the team's language.

### Principle 6: Automation Through Slash Commands

Repetitive context maintenance tasks are automated through custom slash commands. You don't depend on someone "remembering" to update a document — the agent itself executes commands that generate and update context.

Examples of commands that CFD defines:
- `/project:init` — Initialize the context structure in an existing project
- `/project:status` — Generate a summary of the current project state
- `/decision:new` — Create a new ADR from a discussion
- `/context:validate` — Verify that context is complete and consistent
- `/session:start` — Session start routine with context loading

---

## The Knowledge Architecture: Directory Structure

A project following CFD has the following context structure (coexisting with source code):

```
project-root/
├── CLAUDE.md                          # Root context file (Level 0)
├── docs/
│   ├── ARCHITECTURE.md                # Architecture overview
│   ├── STACK.md                       # Tech stack and versions
│   ├── CONVENTIONS.md                 # Code conventions and style
│   ├── CURRENT_STATUS.md              # Current project status (WIP)
│   └── decisions/
│       ├── _index.md                  # Decision index with status
│       ├── 001-initial-architecture.md
│       ├── 002-database-selection.md
│       ├── 003-auth-strategy.md
│       └── ...
├── .claude/
│   └── commands/
│       ├── init.md                    # /project:init
│       ├── status.md                  # /project:status
│       ├── new-decision.md            # /decision:new
│       ├── validate-context.md        # /context:validate
│       └── start-session.md           # /session:start
└── src/                               # (or lib/, app/, etc.)
    ├── feature-a/
    │   └── CLAUDE.md                  # Module-specific context
    ├── feature-b/
    │   └── CLAUDE.md
    └── ...
```

### The Root File: CLAUDE.md

This is the entry point. The model reads it automatically when starting a session. It should be a **map**, not an encyclopedia.

```markdown
# Project: [project-name]

## What This Project Does
[2-3 sentences. What problem does it solve? Who uses it?]

## Architecture
@docs/ARCHITECTURE.md

## Tech Stack
@docs/STACK.md

## Conventions
@docs/CONVENTIONS.md

## Current Status
@docs/CURRENT_STATUS.md

## Key Decisions
@docs/decisions/_index.md

## Build & Run
- Install: `[command]`
- Dev: `[command]`
- Test: `[command]`
- Lint: `[command]`

## Critical Rules
- [Rule 1: e.g., "Never modify the migration files directly"]
- [Rule 2: e.g., "All API endpoints must have integration tests"]
- [Rule 3: e.g., "Use the repository pattern for data access"]
```

The `@docs/ARCHITECTURE.md` syntax is a reference that Claude Code resolves automatically. This keeps the root file compact while allowing depth exploration.

### ARCHITECTURE.md

```markdown
# Architecture Overview

## System Diagram
[ASCII diagram or reference to an image in assets/]

## Layer Structure
- **Presentation**: [framework, patterns]
- **Domain**: [business logic organization]
- **Data**: [persistence strategy, repositories]

## Module Map
| Module | Purpose | Key Files |
|--------|---------|-----------|
| auth   | Authentication & authorization | src/auth/ |
| users  | User management CRUD | src/users/ |
| ...    | ... | ... |

## Data Flow
[Description of how data flows through the system]

## External Dependencies
| Service | Purpose | Docs |
|---------|---------|------|
| Stripe  | Payments | [link] |
| ...     | ...      | ...    |
```

### CURRENT_STATUS.md

This file is **dynamic**. It's updated at the end of every work session. It's the first thing the model reads (via the reference in CLAUDE.md) to know what was happening.

```markdown
# Current Project Status

Last updated: 2026-02-19

## In Progress
- [ ] Implementing user profile API (#142)
  - Endpoint created, missing validation tests
  - Blocked by: Decision on email validation strategy (see ADR-015)

## Recently Completed
- [x] Database migration for user preferences (#138)
- [x] Auth middleware refactor (#135)

## Known Issues
- Performance degradation in search endpoint when > 1000 results
- Flaky test in auth.integration.test (timing issue)

## Next Priorities
1. Complete user profile API
2. Address search performance issue
3. Begin notification system (ADR pending)
```

### The Decision Index: decisions/_index.md

```markdown
# Architecture Decision Records

| ID | Title | Status | Date |
|----|-------|--------|------|
| 001 | [Initial architecture](001-initial-architecture.md) | Accepted | 2026-01-15 |
| 002 | [Use PostgreSQL](002-database-selection.md) | Accepted | 2026-01-16 |
| 003 | [JWT auth strategy](003-auth-strategy.md) | Superseded by 004 | 2026-01-20 |
| 004 | [Switch to session auth](004-session-auth.md) | Accepted | 2026-02-10 |
```

---

## The Daily Routine: The CFD Workflow

This is the practical part. CFD defines a daily routine with three clear phases.

### Phase 1: Session Start (2-3 minutes)

Every work session with the agent begins with a context ritual. This is not optional.

```bash
# 1. Sync with the remote repository
gh repo sync

# 2. Review project state (PRs, issues)
gh pr list --state open
gh issue list --label "in-progress"

# 3. Start a session with Claude Code
claude

# 4. Inside Claude, run the start routine
> /project:status
```

The slash command `/project:status` is defined in `.claude/commands/status.md`:

```markdown
Review the current project status by reading the following files in order:
1. docs/CURRENT_STATUS.md - What's in progress and what's blocked
2. docs/decisions/_index.md - Recent decisions that might affect current work

Then provide a brief summary of:
- What was being worked on
- What's blocked and why
- What should be the focus of this session

Do NOT read source code files unless specifically needed to answer the above.
```

This command consumes ~500-800 tokens instead of the 10,000-50,000 that scanning source code would cost. **That's the difference between a sustainable workflow and one that burns through your API budget.**

### Phase 2: Development (the main cycle)

During development, the flow follows a disciplined pattern:

#### Before implementing: Clarify and decide

```bash
# If a significant technical decision arises
> /decision:new
```

The command `/decision:new` in `.claude/commands/new-decision.md`:

```markdown
I need to document a new architectural decision. Guide me through the following:

1. Ask me what decision needs to be made
2. Help me articulate the context (what problem are we solving?)
3. Propose 2-3 alternatives with pros/cons
4. Once I choose, generate a new ADR file in docs/decisions/ following this format:
```

```markdown
# ADR-[next number]: [Title]

## Status
Accepted

## Date
[today's date]

## Context
[What I described]

## Decision
[What was chosen]

## Alternatives Considered
[The alternatives we discussed]

## Consequences
[What changes as a result]
```
Then update docs/decisions/_index.md with the new entry.
```
#### During implementation: Work in atomic blocks

CFD recommends implementation sessions focused on **one atomic task** at a time. This isn't basic productivity — it's context management. An AI agent works better when it has a clear, scoped instruction than when it has a list of 10 things to do.

```bash
# Bad: vague instruction that scatters context
> "Implement the notification system"

# Good: atomic instruction with explicit context
> "Create the notification repository interface in src/notifications/domain/.
   Follow the repository pattern we use (see ADR-001).
   Look at src/users/domain/user_repository for reference."
```

#### When the agent gets it wrong: Don't correct — document

One of the most common mistakes when working with AI agents is manually correcting code without updating context. If the model generates something incorrect, it will likely do it again in the next session because the context doesn't say it's incorrect.

```markdown
# The model generates a singleton where it should use dependency injection

# Bad: you fix the code manually and move on

# Good: you document the convention
> "That's incorrect. We use dependency injection, never singletons.
   Please fix the code AND add this rule to docs/CONVENTIONS.md
   under the 'Patterns' section."
```

Now the convention is persisted. Next session, the model reads it automatically.

### Phase 3: Session Close (3-5 minutes)

Before closing the session, the agent updates the project status. This is **non-negotiable** in CFD.

```bash
# Update project status
> Update docs/CURRENT_STATUS.md with what was accomplished in this session,
  what's still pending, and any blockers discovered. Keep the same format.

# If there are changes to commit
> /commit  # or manually:
gh pr create --title "feat: notification repository" --body "..."
```

The session close produces a diff in `CURRENT_STATUS.md` that is essentially a **session log**. This creates natural traceability:

```bash
# View project evolution over time
git log --oneline -- docs/CURRENT_STATUS.md
```

---

## GitHub CLI Integration: The Complete Flow

GitHub CLI (`gh`) is a fundamental piece of CFD because it connects repository context with the team workflow.

### Issues as Work Units

```bash
# Create an issue with full context
gh issue create \
  --title "Implement notification repository" \
  --body "## Context
See ADR-012 for the notification system decision.

## Acceptance Criteria
- [ ] NotificationRepository interface in domain layer
- [ ] PostgreSQL implementation in data layer
- [ ] Unit tests for repository implementation
- [ ] Integration test with test database

## References
- ADR-012: docs/decisions/012-notification-system.md
- Pattern reference: src/users/domain/user_repository" \
  --label "feature,notifications"
```

When starting a session to work on this issue:

```bash
# View the issue with all its context
gh issue view 42

# Inside Claude Code, link the session to the issue
> I'm working on issue #42. Read the issue description with
  `gh issue view 42` and the referenced ADR before starting.
```

### Pull Requests with Traceable Context

```bash
# Create a PR that references decisions and context
gh pr create \
  --title "feat(notifications): add notification repository" \
  --body "## Summary
Implements the notification repository following ADR-012.

## Changes
- Added NotificationRepository interface
- Added PostgresNotificationRepository implementation
- Added unit and integration tests

## Decision References
- ADR-012: Notification system architecture
- ADR-001: Repository pattern convention

## Testing
\`\`\`bash
npm test -- --grep notification
\`\`\`"
```

### Context-Assisted Code Review

When reviewing a PR from another team member (or from an agent):

```bash
# View the PR with its context
gh pr view 87

# Inside Claude Code, review with project context
> Review PR #87. Read the PR description first, then check:
  1. Does it follow our conventions in docs/CONVENTIONS.md?
  2. Is it consistent with the referenced ADRs?
  3. Are there missing tests per our testing standards?
  Use `gh pr diff 87` to see the changes.
```

### Automation with GitHub Actions

CFD recommends a validation workflow that checks context integrity:

```yaml
# .github/workflows/context-validation.yml
name: Context Validation
on:
  pull_request:
    paths:
      - 'src/**'
      - 'docs/**'
      - 'CLAUDE.md'

jobs:
  validate-context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check CURRENT_STATUS is updated
        run: |
          if git diff origin/main --name-only | grep -q "^src/"; then
            if ! git diff origin/main --name-only | grep -q "docs/CURRENT_STATUS.md"; then
              echo "::warning::Source code changed but CURRENT_STATUS.md was not updated"
            fi
          fi

      - name: Validate ADR index
        run: |
          # Check that all ADR files are listed in the index
          for adr in docs/decisions/[0-9]*.md; do
            filename=$(basename "$adr")
            if ! grep -q "$filename" docs/decisions/_index.md; then
              echo "::error::ADR $filename is not listed in _index.md"
              exit 1
            fi
          done
```

---

## Anti-Patterns: What CFD Explicitly Forbids

A methodology is defined not only by what it recommends — but by what it forbids.

### Anti-pattern 1: The Monolithic CLAUDE.md

```markdown
# ❌ BAD: Everything in a 500-line file
# CLAUDE.md containing architecture, conventions, decisions,
# project status, and a novel about the code's history
```

If your CLAUDE.md has more than 150 lines, it's already broken. Use `@references`.

### Anti-pattern 2: Duplicated Context

```markdown
# ❌ BAD: Same information in three places
# CLAUDE.md says "we use PostgreSQL"
# docs/ARCHITECTURE.md says "the database is PostgreSQL"
# docs/decisions/002.md says "we chose PostgreSQL"

# ✅ GOOD: Single source, cross-references
# CLAUDE.md: @docs/STACK.md
# docs/STACK.md: "Database: PostgreSQL 16 (see ADR-002)"
# docs/decisions/002.md: [source of truth with full context]
```

### Anti-pattern 3: Documentation in Native Language

```markdown
# ❌ BAD: Context in Spanish
## Arquitectura
La aplicación utiliza una arquitectura de capas separadas...
# Consumes ~30% more tokens than the English equivalent

# ✅ GOOD: Context in English
## Architecture
The application uses a layered architecture...
```

Articles, PRs, and team communication can be in any language. Technical context consumed by the model should be in English.

### Anti-pattern 4: Scanning Code Instead of Reading Context

```markdown
# ❌ BAD: Prompt that forces scanning
> "Read all files in src/ and tell me how the project is structured"
# Cost: 10,000-50,000+ tokens

# ✅ GOOD: Prompt that uses existing context
> "Read docs/ARCHITECTURE.md and summarize the project structure"
# Cost: 500-1,500 tokens
```

### Anti-pattern 5: Implicit Decisions

```markdown
# ❌ BAD: Decision made in a conversation that gets lost
"Let's just use Redis for caching" → implemented → session ends →
next session doesn't know why Redis is there

# ✅ GOOD: Decision documented before implementing
> /decision:new
→ ADR-015: Use Redis for caching
→ Recorded in docs/decisions/
→ Next session reads the ADR automatically
```

### Anti-pattern 6: Not Closing the Session

The most common and most costly mistake. If you don't update `CURRENT_STATUS.md` at the end of the session, the next session starts without knowing what was done. It's the equivalent of not committing — work that exists but is invisible.

---

## Scaling CFD: From Individual to Team

### For an Individual Developer

The minimum CFD implementation for a solo developer:

```
CLAUDE.md                     # Root file (required)
docs/
  ARCHITECTURE.md             # Overview (required)
  CURRENT_STATUS.md           # Current status (required)
  decisions/
    _index.md                 # Decision index (required)
.claude/
  commands/
    start-session.md          # Session start (recommended)
    new-decision.md           # New decision (recommended)
```

Setup time: ~30 minutes with `/project:init`.
Daily overhead: ~5-8 minutes (session start + close).
ROI: pays for itself after 3-4 work sessions.

### For a Team

In a team, CFD extends with:

```
docs/
  TEAM_CONVENTIONS.md         # Team conventions
  ONBOARDING.md               # Guide for new members (and new agents)
  decisions/
    TEMPLATE.md               # ADR template for consistency
```

Additional team rules:

1. **ADRs require review** — like code, decisions are reviewed in PRs.
2. **CURRENT_STATUS.md leaves version control and becomes per-developer** — `.gitignore` it; each developer keeps a personal local copy for session continuity. A single shared status file is a merge-conflict magnet (every PR touches it) and pollutes each developer's session start with everyone else's in-flight state. Shared "who is doing what" lives in the tracker (issues, milestones, assignees), not in a status file. Solo developers keep the file tracked — for one person it doubles as a session log.
3. **Slash commands are shared** — `.claude/commands/` lives in the repository.
4. **Each member can have local preferences** — `~/.claude/CLAUDE.md` for personal configuration that doesn't affect the team.

### For Monorepos

In monorepos, CFD leverages the hierarchical nature of context:

```
CLAUDE.md                     # Global monorepo context
docs/                         # Global documentation
packages/
  service-a/
    CLAUDE.md                 # service-a specific context
    docs/                     # Specific docs
  service-b/
    CLAUDE.md                 # service-b specific context
    docs/                     # Specific docs
```

The model reads the nearest CLAUDE.md to the current working directory, with inheritance from the parent level.

---

## Metrics: How to Know if CFD is Working

CFD is not dogma — it's a measurable practice. These are the metrics that matter:

### Tokens Per Productive Session

Measure how many tokens an average session consumes. With well-implemented CFD, you should see:

- **Session start**: 500-1,500 tokens (context reading)
- **Productive session**: 5,000-15,000 tokens (actual work)
- **Session close**: 500-1,000 tokens (status update)

Without CFD, session start alone can consume 20,000-50,000 tokens just scanning code.

### Time to First Correct Action

How many minutes pass from session start until the agent produces correct code (that doesn't need manual correction)? With CFD, it should be < 5 minutes. Without context, it can be 15-30 minutes of back-and-forth.

### Re-explanation Rate

How often do you have to explain to the model something that was already discussed in a previous session? If you're constantly re-explaining decisions, the context is incomplete.

### CURRENT_STATUS.md Freshness

```bash
# How many commits ago was it last updated?
git log -1 --format="%ar" -- docs/CURRENT_STATUS.md
```

If the answer is "more than 1 working day ago", the context is stale.

---

## Complementary Tools

### Repomix: For When You Need Total Context

[Repomix](https://repomix.com/) packages entire codebases into a single AI-optimized file. It's useful for:

- Generating the initial `ARCHITECTURE.md`
- Full project audits
- Technology migrations

```bash
# Generate a project snapshot (excluding context docs)
npx repomix --ignore "docs/,node_modules/,.claude/"
```

Don't use it every session — it's the "nuclear context" tool for when you need the model to understand everything.

### GitHub CLI: The Glue

Already covered in detail, but to summarize the essential `gh` commands in a CFD flow:

```bash
gh issue list                  # View pending work
gh issue view <n>              # Task context
gh pr list                     # View open PRs
gh pr create                   # Create PR with context
gh pr diff <n>                 # View PR changes
gh pr review <n>               # Review a PR
gh repo sync                   # Sync with remote
```

---

## Case Study: Implementing CFD in an Existing Project

Let's see how CFD is implemented in a project that already has code. We're not starting from zero — we have a project with 200+ files, 6 months of history, and zero context documentation.

### Step 1: Initialization (30 minutes)

```bash
# Start Claude Code in the project
claude

# Run initialization
> I want to implement Context-First Development (CFD) in this project.
  Analyze the directory structure (do NOT read individual files) and:
  1. Create docs/ARCHITECTURE.md based on the directory structure and
     dependency files (package.json, pubspec.yaml, etc.)
  2. Create docs/STACK.md listing all technologies and their versions
  3. Create docs/CONVENTIONS.md — infer 5-10 key conventions from
     the project structure
  4. Create docs/CURRENT_STATUS.md — initialize with "Project initialized
     with CFD"
  5. Create docs/decisions/_index.md — empty index
  6. Create docs/decisions/001-initial-architecture.md documenting
     the current architecture as the first ADR
  7. Update CLAUDE.md to reference all docs/ files
```

### Step 2: Document Existing Decisions (1-2 hours, distributed)

You don't need to document everything at once. Each time you work on an area of the code and discover an implicit decision:

```bash
> I see we're using [pattern X] in this module.
  Let's document this as an ADR. /decision:new
```

After 2-3 weeks of normal work, you'll have 10-15 ADRs that capture the project's most important decisions.

### Step 3: Establish the Routine (permanent)

From here, the flow is:

```
Session start → /session:start → Work → /decision:new (if applicable) → Close → Update CURRENT_STATUS.md
```

---

## Conclusion: Context Is the Competitive Advantage

There's a dangerous illusion in the industry: that increasingly larger AI models will solve the context problem. They won't. A model with a 2 million token context window isn't more useful if you feed it 2 million tokens of noise.

The competitive advantage isn't in the model — it's in the context you provide. A developer with a well-documented project using Claude 3.5 Sonnet will consistently outperform a developer with zero context using Claude Opus. **Context multiplies the model's capability; it's not a substitute for it.**

Context-First Development is not a revolutionary framework. It's the disciplined application of principles that good engineers already know — clear documentation, explicit decisions, shared state — adapted to a world where your programming partner has amnesia at the start of every session.

The question isn't whether you need a methodology like CFD. The question is how many more sessions you'll waste re-explaining the same decisions before adopting one.

---

## References

1. Anthropic. "Effective Context Engineering for AI Agents." [anthropic.com](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025.
2. Anthropic. "Claude Code Best Practices." [code.claude.com](https://code.claude.com/docs/en/best-practices), 2025.
3. Sourcegraph Amp Team. "AGENTS.md: A Standard for AI Agent Instructions." [agents.md](https://agents.md/), 2025.
4. Medin, Cole. "Context Engineering Intro." [GitHub](https://github.com/coleam00/context-engineering-intro), 2025.
5. Osmani, Addy. "My LLM Coding Workflow Going into 2026." [addyosmani.com](https://addyosmani.com/blog/ai-coding-workflow/), 2025.
6. Osmani, Addy. "The AI-Native Software Engineer." [Substack](https://addyo.substack.com/p/the-ai-native-software-engineer), 2025.
7. Spotify Engineering. "1,500+ PRs Later: Spotify's Journey with Our Background Coding Agent." [engineering.atspotify.com](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1), 2025.
8. Spotify Engineering. "Context Engineering: Background Coding Agents Part 2." [engineering.atspotify.com](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2), 2025.
9. Swan, Chris. "Using Architecture Decision Records (ADRs) with AI Coding Assistants." [blog.thestateofme.com](https://blog.thestateofme.com/2025/07/10/using-architecture-decision-records-adrs-with-ai-coding-assistants/), 2025.
10. Rotenberg, Josh. "Claude ADR System Guide." [GitHub Gist](https://gist.github.com/joshrotenberg/a3ffd160f161c98a61c739392e953764), 2025.
11. Strengholt, Piethein. "Building an Architecture Decision Record Writer Agent." [Medium](https://piethein.medium.com/building-an-architecture-decision-record-writer-agent-a74f8f739271), 2025.
12. Chatlatanagulchai et al. "On the Use of Agentic Coding Manifests: An Empirical Study of Claude Code." [arXiv:2509.14744](https://arxiv.org/abs/2509.14744), 2025.
13. "Agent READMEs: An Empirical Study of Context Files for Agentic Coding." [arXiv:2511.12884](https://arxiv.org/html/2511.12884v1), 2025.
14. "Context Engineering for Multi-Agent LLM Code Assistants." [arXiv:2508.08322](https://arxiv.org/abs/2508.08322), 2025.
15. Grandau, Mark. "Turning AI Code Reviews Into Continuous Improvement." [Medium](https://mgrandau.medium.com/turning-ai-code-reviews-into-continuous-improvement-how-github-cli-became-my-secret-weapon-5c026a3ffbdc), 2025.
16. GitHub. "Agentic Workflows." [github.github.io/gh-aw](https://github.github.io/gh-aw/), 2026.
17. Steinberger, Peter. "agent-rules." [GitHub](https://github.com/steipete/agent-rules), 2025 (archived).
18. Li, Bojie. "Claude's Context Engineering Secrets." [01.me](https://01.me/en/2025/12/context-engineering-from-claude/), 2025.
