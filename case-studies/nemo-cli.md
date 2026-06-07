# Case Study: nemo-cli

**Repository:** <https://github.com/albertomarturelo/nemo-cli>
**Author:** Alberto Marturelo
**Stack:** Python 3.11+, typer, httpx, pyright (strict), pytest
**License:** MIT
**Distribution:** `pipx install .`

> `nemo-cli` is **referenced**, not mirrored. The canonical source lives
> at its own repo above. This page captures what CFD adoption looks
> like in that codebase as of 2026-06-07.

## What it is

A personal command-line tool to inspect holdings on Chilean stockbroker
portals (currently the Vector Capital client portal). Authenticates
with the user's credentials, caches a short-lived bearer token, and
exposes portal operations as composable terminal commands:

- `nemo login` / `nemo logout` / `nemo whoami`
- `nemo instruments local` / `nemo instruments international`
- `nemo instruments prices --id <ID>` (1-year history + ASCII sparkline)
- `nemo portfolio summary` (holdings + computed P&L by classification)
- `nemo portfolio movements` (cash movements classified by type)

~46 Python source files. The README claims ~98% line coverage.

## Why this case study matters

`nemo-cli` is **not** a CFD demo built to teach the methodology. It is
a real personal project that *adopted* CFD as its development
discipline. The signals are visible to anyone clicking through:

- **`CLAUDE.md` is ~80 lines, indexed via six `@references`**, with an
  explicit "Critical Rules" section that codifies must-knows: all HTTP
  traffic through `api_request()`, never commit `.env`, English for
  every model-facing artifact, update `CURRENT_STATUS.md` before
  closing a session.
- **11 ADRs in `docs/decisions/`**, indexed in `_index.md`. The
  `Status` field is actively used — see the next section.
- **The methodology essay itself is vendored at the repo root** as
  `context-first-development.md`. A new contributor (human or agent)
  does not need to know where to find CFD; it ships with the project.
- **Production-quality discipline:** `pyright` strict, `ruff`,
  `pytest`, SemVer + Keep a Changelog (ADR-007), CI in `.github/`.

## The textbook supersession moment

`ADR-002` chose Node.js + TypeScript + commander on 2026-05-01. Hours
later, **`ADR-004` superseded it** ("Switch CLI Stack to Python"). Both
ADRs remain in the catalog. The supersession is explicit
(`Accepted (supersedes ADR-002)`); the rejected alternative is
preserved with its rationale; the reader reconstructs the decision
without git archaeology.

This is **CFD Principle 4 — Decisions as First-Class Citizens** in
action: when the decision changes, the record changes; both states
survive.

## CFD adoption checklist

| CFD element                  | Adopted? | Notes                                                                                                |
| ---------------------------- | :------: | ---------------------------------------------------------------------------------------------------- |
| `CLAUDE.md` as index         |    ✓     | ~80 lines, six `@references`, "Critical Rules" section                                               |
| `docs/ARCHITECTURE.md`       |    ✓     | Loaded on demand                                                                                     |
| `docs/STACK.md`              |    ✓     | Pinned versions and rationale                                                                        |
| `docs/CONVENTIONS.md`        |    ✓     | Concrete patterns + critical-rule references                                                         |
| `docs/decisions/_index.md`   |    ✓     | 11 ADRs; `Status` actively used (Accepted / Superseded)                                              |
| `docs/CURRENT_STATUS.md`     |    ◐     | Local-only (`.gitignore`d) — explicit design choice for a solo personal project                       |
| Slash commands               |    ✓     | Implemented as **Claude Skills** under `.claude/skills/` rather than `.claude/commands/` — same intent |
| English-only model context   |    ✓     | Stated in CLAUDE.md; PR descriptions / chat may be Spanish (the author's working language)            |
| Document corrections         |    ✓     | "Critical Rules" section accumulates project-specific lessons                                        |
| ADR-before-implementing      |    ✓     | Codified as a critical rule; the 002→004 supersession follows it                                      |
| Vendored methodology essay   |    ✓     | `context-first-development.md` at repo root keeps the project self-contained                          |

## Variation worth noting: Skills vs slash commands

This catalog's templates use **slash commands** (`.claude/commands/`,
e.g. `/session:start`). `nemo-cli` uses **Claude Skills**
(`.claude/skills/<name>/SKILL.md`, e.g. `start-session`, `status`,
`new-decision`, `validate-context`). Same workflow intent; different
invocation primitive — Skills are model-discovered, slash commands are
user-invoked. Either fits the methodology; pick what your team prefers.

## How to read this case study

1. Clone `github.com/albertomarturelo/nemo-cli`.
2. Open `CLAUDE.md`. Notice how short it is and how dense the
   "Critical Rules" section is.
3. Skim `docs/decisions/_index.md`. Read ADR-002, then ADR-004 — the
   supersession is the canonical CFD discipline end-to-end.
4. Open `.claude/skills/start-session/SKILL.md` for the Skills-flavored
   equivalent of `/session:start`.
5. Compare `nemo-cli`'s `CLAUDE.md` "Critical Rules" against your own
   project's, if you keep one. Steal anything useful.

## Attribution

- Methodology author and `nemo-cli` author: Alberto Marturelo.
- Referenced with the author's permission. `nemo-cli` is MIT-licensed
  at the upstream repository; this prose page is CC-BY-SA 4.0 per the
  publication repo's prose license.

---

*Snapshot of the upstream repo as of 2026-06-07. `nemo-cli` evolves
independently — click the repo link above for the current state.*
