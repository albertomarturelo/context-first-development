<!--
This file is the only context loaded unconditionally at session start.
Keep it ≤150 lines, ideally ≤100.

Deliberate choice: plain markdown LINKS below, not @references.
In Claude Code, `@path` inside CLAUDE.md is an EAGER import — the whole
referenced file is injected into context every session, which turns
this index into an encyclopedia and defeats Principle 3. Links are
lazy: the agent follows them only when the work requires it.
/session:start does the orientation reads (CURRENT_STATUS + decisions
index) explicitly.
-->

# Project: <project-name>

## What This Project Does

<2–3 sentences. What problem does it solve? Who uses it?>

## Context Map (read on demand, not upfront)

- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Tech stack: [docs/STACK.md](docs/STACK.md)
- Conventions: [docs/CONVENTIONS.md](docs/CONVENTIONS.md)
- Current status: [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md)
- Decisions index: [docs/decisions/_index.md](docs/decisions/_index.md)

## Build & Run

- Install: `<command>`
- Dev: `<command>`
- Test: `<command>`
- Lint: `<command>`

## Critical Rules

- Read `docs/CONVENTIONS.md` before writing or editing code — not at
  session start, at first-edit time.
- <rule 1>
- <rule 2>

## When Context and Code Disagree

Precedence: **code is the truth about WHAT the system does; ADRs are
the truth about WHY; `docs/` describes both and can go stale.** If a
doc contradicts the code, STOP and flag the conflict to the user — do
not silently trust the doc, and do not "fix" correct code to match a
stale doc.

<!--
This file is the INDEX, not the encyclopedia. If you find yourself
adding paragraphs of explanation here, move them to a docs/*.md file
and link it from the Context Map instead.

AGENTS.md is an accepted alias if your team uses non-Claude agents:
  ln -s CLAUDE.md AGENTS.md
-->
