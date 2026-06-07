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
scans code to figure it out — both expensive and both prone to drift.

## Decision

Every unit of work lives as an item in a **persistent external tracker**
the agent can query via CLI. The tracker item carries a **fixed body
template** so any session can parse it in O(1) tokens.

**Canonical example: GitHub Issues + Milestones, via `gh`**. Linear
(`linear-cli`), Jira (`jira-cli`), Asana, etc. are valid alternatives if
their CLI supports `create`, `view`, `list --milestone`, and `edit`.
The principle is tracker-agnostic; the template is not.

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
- [ ] <DoD item>

## Reproduction (fixes only)
<minimal repro the agent can run>

## Estimated sessions
<1 | 2–3 | 4+>
```

If "Estimated sessions" > 1, the issue is **decomposed into sub-issues
before work starts**. Multi-session monoliths defeat the design.

### Workflow

- **Create**: `/issue:new` runs the template and `gh issue create`.
- **Start**: `/issue:start <n>` runs `gh issue view <n>` and pre-loads
  the ADRs listed.
- **Close**: PR closes the issue; the AC checklist is copied verbatim to
  the PR description.

## Alternatives Considered

1. **`specs/` directory in the repo (OpenSpec-style).** Duplicates state
   with wherever the team already tracks work; sync rots; no
   collaboration surface (humans + agents both write to the tracker).
2. **Free-form issues, no template.** Every issue forces the agent to
   discover the structure → token waste and parse errors.
3. **`TODO.md` in the repo.** Single-author OK; no querying, no DoD
   enforcement, no milestones.
4. **Chat history as task memory.** Doesn't survive restart — the exact
   gap CFD exists to close.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- Every recent issue's body contains the 6 fixed section headers (or 5
  for non-fixes). Spot check via `gh issue view <n>`.
- `docs/CURRENT_STATUS.md` references in-progress work by `#N`, not by
  free-text alone.
- PR descriptions reuse the AC checklist verbatim; merging the PR closes
  the linked issue.
- `gh issue list --search "no:milestone is:open"` returns near-zero —
  every active issue belongs to a milestone.

## Trade-offs

- Adds 3–5 minutes to issue creation. Recovered fully on the next session
  start, which now needs ~1.5–3k tokens to be fully oriented vs. ~10k+
  to discover the same context from code.
- Requires a tracker with CLI. Most modern ones have one; legacy ones
  don't and are a poor fit for CFD regardless.
