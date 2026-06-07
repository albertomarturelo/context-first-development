<!-- Shareable ADR. Token budget: ~600. -->

# ADR-`<NNN>`: Work Units Live in an External Tracker with a Fixed Body Template

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Work crosses session boundaries (any non-trivial project).
- More than one engineer (or one engineer + an agent) collaborates.
- "What do I do next?" needs an answer that survives session restart.

Skip for one-shot scripts, single-session prototypes, or anything you
can hold in your head.

## Context

CFD documents **context** (`CLAUDE.md` + `docs/`), **decisions** (ADRs),
and **in-flight state** (`CURRENT_STATUS.md`). Without an explicit
unit-of-work artifact, the agent at session start knows that "the
notification repository is in progress" but not *what exactly* to do,
*where* to put it, what acceptance looks like, or which ADRs to load
first. The user fills the gap by re-explaining each session, or the agent
scans code to figure it out — both expensive and prone to drift.

## Decision

Every unit of work lives as an item in a **persistent external tracker**
the agent can query via CLI. The tracker item carries a **fixed body
template** so any session parses it in O(1) tokens.

**Canonical example: GitHub Issues + Milestones, via `gh`**. Linear
(`linear-cli`), Jira (`jira-cli`), Asana, etc. are valid if their CLI
supports `create`, `view`, `list --milestone`, and `edit`. Principle is
tracker-agnostic; the template is not.

### Fixed body template

```markdown
## Context
<2–4 sentences: trigger + user-visible outcome>

## Target
- Files / dirs: <paths or modules>
- Pattern to mirror: <existing file to copy shape/naming from>

## ADRs to load
- [ADR-NNN](docs/decisions/NNN-*.md)

## Acceptance criteria
- [ ] <DoD item — becomes the PR checklist>

## Reproduction (fixes only)
<minimal repro the agent can run>

## Estimated sessions
<1 | 2–3 | 4+>
```

If "Estimated sessions" > 1, decompose into sub-issues before starting.

### Workflow

- **Create**: `/issue:new` → `gh issue create` with the template.
- **Start**: `/issue:start <n>` → `gh issue view <n>` + pre-loads ADRs.
- **Close**: PR closes the issue; AC checklist copies verbatim to PR.

## Alternatives Considered

1. **`specs/` directory in the repo (OpenSpec-style).** Duplicates state
   with wherever the team already tracks work; sync rots; no native
   collaboration surface.
2. **Free-form issues, no template.** Every issue forces the agent to
   discover the structure → token waste and parse errors.
3. **`TODO.md` in the repo.** Single-author OK; no querying, no DoD
   enforcement, no milestones.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `gh issue view <n>` on any in-progress issue returns the 6 fixed
  sections (5 for non-fixes).
- `docs/CURRENT_STATUS.md` references in-progress work by `#N`.
- PR descriptions reuse the AC checklist verbatim; merging closes the
  linked issue.
- `gh issue list --search "no:milestone is:open"` returns near-zero.

## Trade-offs

- Adds 3–5 minutes to issue creation. Recovered on the next session
  (~1.5–3k tokens vs ~10k+ for code discovery).
- Requires a tracker with CLI. Most modern ones have one.
