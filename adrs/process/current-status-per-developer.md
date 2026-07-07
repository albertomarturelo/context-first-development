<!-- Shareable ADR. Token budget: ~450. -->

# ADR-`<NNN>`: CURRENT_STATUS Is Per-Developer, Out of Version Control

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Two or more developers work on the repo with AI agents.
- Work units live in an external tracker (see
  [work-units-as-external-tracker](work-units-as-external-tracker.md))
  — the tracker, not the status file, must already be the shared
  source of "who is doing what".

Do NOT adopt solo: a tracked `CURRENT_STATUS.md` doubles as a session
log (`git log -- docs/CURRENT_STATUS.md`) and its freshness is
verifiable from history. Keep it in git until a second developer
arrives.

## Context

With one shared, committed `docs/CURRENT_STATUS.md`, the session-close
ritual makes every PR touch the same file: a merge-conflict magnet
that scales linearly with team size. Worse, the file stops doing its
job — developer A's session start injects developer B's in-flight
sub-state, blockers, and scratch notes, polluting the context the
agent orients from. The file's actual role is **session continuity
for one developer and their agent**; the shared coordination role
already belongs to the tracker.

## Decision

For teams of 2+:

- **`.gitignore` `docs/CURRENT_STATUS.md`.** Each developer keeps a
  personal local copy, created from the template on first
  `/session:start`.
- **Shared in-flight state lives in the tracker** (issues, milestone
  boards, assignees) — never in the status file.
- The session-close ritual is unchanged (update before closing), but
  the same-commit rule now applies only to `CONVENTIONS.md`, ADRs,
  and other tracked docs.
- Enforcement adapts automatically: the commit-time guard and the CI
  freshness check skip when the file is untracked; the staleness
  warning uses file mtime instead of git history.

## Alternatives Considered

1. **Shared tracked file with per-person subsections.** Reduces
   conflicts but doesn't eliminate them, and still injects everyone's
   WIP into every session start.
2. **Per-developer tracked files (`docs/status/<name>.md`).** No
   conflicts, but publishes personal scratch state into review
   history and adds commit noise to every PR.
3. **Auto-generate status from the tracker.** Loses the sub-state
   granularity ("endpoint created, missing validation tests") that
   makes the next session start cheap.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `.gitignore` contains `docs/CURRENT_STATUS.md`.
- `git log --oneline -- docs/CURRENT_STATUS.md` shows no commits
  after the adoption date; PRs no longer touch the file.
- Tracker issues carry assignees and in-progress state; no
  "who's doing what" section survives in any tracked doc.

## Trade-offs

- Loses the git-history session log and the history-based freshness
  metric — both become local (file mtime).
- A fresh clone or new machine starts with no status file; the first
  `/session:start` bootstraps it from the template plus the tracker's
  assigned issues. Costs one orientation session.
- Personal status quality is now invisible to the team; the tracker
  must be kept honest or the shared picture degrades.
