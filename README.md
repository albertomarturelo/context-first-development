# Context-First Development

[![Validate catalog](https://github.com/albertomarturelo/context-first-development/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/albertomarturelo/context-first-development/actions/workflows/validate-catalog.yml)

> Your AI agent has amnesia at the start of every session. CFD is the cure.

**CFD is a methodology for engineers who use AI coding agents** (Claude
Code, Gemini CLI, Codex, Cursor, Aider) **on real repositories.** It treats
context as a first-class artifact: structured, versioned, and reviewed like
code. The result is sessions that cost ~10–30× fewer tokens and produce
code that actually fits the project — without re-explaining decisions on
every prompt.

**Evidence.** Measure the effect on your own project with
[`scripts/measure-session-cost.sh`](scripts/measure-session-cost.sh):
it compares a CFD-style `/session:start` (reading the `CLAUDE.md` +
`CURRENT_STATUS.md` + decisions-index triad) against scanning the whole
project for "full context", and reports the token ratio.

Real-world adopter you can click through:
**[`nemo-cli`](case-studies/nemo-cli.md)** — production Python CLI
built solo with CFD discipline (`CLAUDE.md` as ~80-line index, 11 ADRs
with an explicit `002 → 004` supersession, MIT-licensed, `pyright`
strict, ~98% line coverage). A team case study from Equifax
(ID Watchdog Mobile) is in progress; see
[`case-studies/`](case-studies/).

## The 30-second pitch

|                        | Without CFD                                 | With CFD                                                          |
| ---------------------- | ------------------------------------------- | ----------------------------------------------------------------- |
| Session start          | 20–50k tokens scanning code                 | 500–1,500 tokens reading `CLAUDE.md` + `CURRENT_STATUS.md`        |
| Architectural context  | Lives in your head, re-explained each time  | Lives in `docs/decisions/` ADRs the agent reads automatically     |
| Agent's wrong patterns | Manually fixed every session                | Convention documented once; agent reads it next session           |
| Project state          | Lives in your memory                        | `docs/CURRENT_STATUS.md` is the project's running session log     |
| Hallucination surface  | Wide — agent invents details to fill blanks | Narrow — explicit ADRs constrain what is decided vs. open         |
| Multi-model            | Locks you in to whichever tool you tried    | Plain Markdown; works with any agent that reads context files     |

## Try it in 60 seconds

```bash
# In an existing repo:
git clone https://github.com/albertomarturelo/context-first-development.git /tmp/cfd
cp -r /tmp/cfd/templates/. .

# Edit CLAUDE.md and fill in your project's 2–3 sentence description.
# Open your agent (claude / gemini / codex / cursor) and run:
> /project:status
```

Templates are deliberately minimal. Fill in what the agent needs to know
about *your* project — and resist the temptation to write more. Brevity is
the design.

### Or install the commands as a plugin (Claude Code)

The CFD slash commands ship as an optional Claude Code plugin, so you can
install them without copying files:

```text
/plugin marketplace add albertomarturelo/context-first-development
/plugin install cfd@context-first-development
```

This exposes the commands namespaced (`/cfd:session-start`,
`/cfd:new-decision`, `/cfd:issue-start`, …). The plugin is a
**distribution convenience, not the source of truth** — it points at the
same portable markdown in `templates/.claude/commands/`. Teams on other
agents copy that markdown directly and lose nothing but the installer.
See [`adrs/ai-workflow/distribute-commands-as-plugin.md`](adrs/ai-workflow/distribute-commands-as-plugin.md).

## What's in this repo

```text
README.md          this file
METHODOLOGY.md     pointer to the canonical essay (gist)
templates/         drop-in scaffolding for any project
adrs/              shareable ADR catalog ("shadcn for AI context")
case-studies/      evidenced adoption write-ups
CONTRIBUTING.md    how to propose ADRs, examples, case studies
LICENSE            MIT for code, CC-BY-SA 4.0 for prose
```

## The shareable ADR catalog

This is the part that is new. Every catalog ADR is **atomic,
technology-neutral, and copyable**. You don't install a library — you copy
the file into your repo. Your agent reads it next session and knows, with
full rationale:

- *why* you use the repository pattern (alternatives evaluated,
  consequences)
- *why* tests hit a real database instead of mocks
- *why* corrections are documented, not just applied

Browse [`adrs/`](adrs/) for the catalog. Categories: `architecture`,
`testing`, `process`, `ai-workflow`.

## The work-tracking layer

CFD documents context, decisions, and in-flight state — but **tasks
themselves live in a persistent agent-readable tracker** (canonical:
GitHub Issues + Milestones), with a **fixed body template** so any
session can parse a task in O(1) tokens.

The template forces every issue to declare:

- **Context** — trigger and user-visible outcome.
- **Target** — files/dirs the work goes into, plus an existing file to
  mirror.
- **ADRs to load** — pre-reading list, so the session opens with the
  right constraints already in scope.
- **Acceptance criteria** — markdown checkboxes that copy verbatim into
  the PR description.
- **Estimated sessions** — anything `>1` must be decomposed first.

See
[`adrs/process/work-units-as-external-tracker.md`](adrs/process/work-units-as-external-tracker.md)
for the full ADR, and the
[`/issue:new`](templates/.claude/commands/issue-new.md) /
[`/issue:start`](templates/.claude/commands/issue-start.md) slash
commands in the templates. To see this layer composed with the rest of
CFD in motion (issue auto-load on `/session:start`, AC → PR
description, etc.), see [**CFD in motion**](docs/session-flow.md) —
four Mermaid sequence diagrams covering bootstrap, the canonical
session, correction-to-convention, and decision-before-implementation.

The principle is tracker-agnostic. Linear, Jira, Asana — all valid if
their CLI supports `create`, `view`, `list --milestone`, and `edit`.
The body template stays the same; only the CLI changes.

## The 6 principles (one-liner each)

1. **Context Before Code** — resolve context at session start, not during.
2. **Single Source of Truth** — every fact lives in exactly one file;
   everything else `@references` it.
3. **Hierarchical Context** — `CLAUDE.md` is an index (~100 lines), not an
   encyclopedia.
4. **Decisions as First-Class Citizens** — every significant decision
   becomes an ADR.
5. **English as Context Language** — tokenizers compress English
   ~20–40% better than other languages.
6. **Automation Through Slash Commands** — context maintenance is a
   command, not a remembered chore.

The full essay (philosophy, anti-patterns, comparative landscape,
references) lives in the canonical gist. See
[`METHODOLOGY.md`](METHODOLOGY.md).

## Who CFD is for

- **Solo developers** working with an AI agent on a non-trivial repo
  (>100 files).
- **Teams of 2–20** adopting an agent in production code.
- **Tech leads** evaluating whether AI-assisted development can scale
  beyond toy projects.

If you've ever spent the first 15 minutes of a session re-explaining your
architecture to the model, CFD is for you.

## Who CFD is NOT for

- Quick scripts, one-off prototypes, throwaway code. The setup cost
  (~30 minutes) doesn't pay back.
- "Vibe coding" workflows where the looseness is the point.

## Status

Public alpha. The methodology is in active use. PRs are welcome; turnaround
is best-effort.

## License

- Code, templates, slash commands: **MIT**.
- Prose (essay, ADRs, case studies): **CC-BY-SA 4.0**.

See [`LICENSE`](LICENSE) for the full text.

## Cite as

> Marturelo, Alberto. *Context-First Development (CFD): A Methodology for
> AI-Assisted CLI Development.* 2026.
> <https://gist.github.com/7b5c6f91f17b83852724fa73100c8588>
