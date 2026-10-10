<!-- Shareable ADR. Token budget: ~800. -->

# ADR Identity Is a Date-Prefixed Slug, Not a Sequence Number

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- More than one branch can create an ADR at the same time: parallel
  agent loops in git worktrees, several developers, or long-lived
  feature branches.
- You are starting a new project, where it costs nothing.

Existing projects adopt it **for new ADRs only**. Numbered ADRs keep
their numbers forever.

## Context

`NNN-<slug>.md` makes the ADR identity a global counter. "One above the
highest existing" is computed per branch, so two worktrees that each
write a decision both create `012`. The collision surfaces at merge, or
worse, both merge under different slugs and `ADR-012` becomes
ambiguous in every later citation.

A raw timestamp removes the counter but makes the ID opaque. Agents
cite ADRs by ID, and mis-citing an ADR is a known drift symptom (see
[short-sessions-over-long](../ai-workflow/short-sessions-over-long.md)).
A mistyped 14-digit timestamp looks as valid as a correct one. A
mistyped slug breaks a link that a check can catch. Rails made the same
move for migrations in 2.1, from sequence numbers to timestamps, to end
cross-branch collisions.

## Decision

- **File:** `docs/decisions/YYYY-MM-DD-<slug>.md`. The date gives
  chronological order and needs no coordination between branches.
- **Identity:** the slug. It is unique across `docs/decisions/`
  regardless of date. Cite it as `ADR <slug>` in prose, or as a
  markdown link to the file.
- **Supersession:** `Superseded by <slug>`.
- **Index:** `_index.md` lists the slug in the ID column. Numbered rows
  stay as they are; one table, ordered by date.
- **Legacy:** existing `NNN-*` ADRs are never renamed. Code comments,
  commit messages, closed issues and PR threads cite them by number,
  and that history cannot be rewritten.

## Alternatives Considered

1. **Keep sequence numbers, reserve them at decomposition time.**
   Works only while one person decomposes all work; any ad-hoc
   decision mid-session re-opens the race.
2. **Timestamp as the full identity.** Collision-free but opaque to
   agents and humans; citation errors go undetected.
3. **Migrate old ADRs to the new scheme.** Moving files is mechanical,
   but references outside the working tree (git history, the tracker)
   would dangle. Aliases would fix that, at which point the rename buys
   nothing.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- Every ADR created after the adoption date matches
  `docs/decisions/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\.md`.
- No two date-prefixed files in `docs/decisions/` share a slug. A CI
  check fails the PR when they do.
- `git log --diff-filter=R -- docs/decisions/` shows no renames of
  numbered ADRs.

## Trade-offs

- Two ID formats coexist in older projects. The index absorbs it; the
  cost is cosmetic.
- Two branches can pick the same slug on different dates without a git
  conflict. The uniqueness check catches it at PR time. Treat that
  failure as a signal: two loops decided the same thing in parallel,
  and a human must reconcile them.
- Slugs must be chosen well. A vague slug (`fix-stuff`) is as useless
  as a number.
