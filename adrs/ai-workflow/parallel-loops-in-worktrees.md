<!-- Shareable ADR. Token budget: ~1,025. -->

# Parallel CFD Loops in Git Worktrees

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- [single-loop-human-orchestrator](single-loop-human-orchestrator.md)
  is in place and throughput demonstrably outgrew it: independent,
  well-specified issues idle in the tracker while review capacity sits
  unused.
- You run several agents at once, one per git worktree, by hand or
  through an orchestrator, possibly mixing vendors (Claude Code, Codex).

Do NOT adopt while issues routinely touch the same modules, or while
ADRs are still being settled weekly: the loops would serialize anyway.

## Context

A worktree isolates files, not decisions. The immutable context
(`CLAUDE.md`, ADRs, `CONVENTIONS.md`, skills) is identical in every
worktree at branch time. The mutable context is not: an ADR or a
convention correction written in loop A is invisible to loop B until
merge. That is CFD's drift thesis
([short-sessions-over-long](short-sessions-over-long.md)) running in
parallel instead of in series: B keeps building on a rule A just
changed. Shared counters and shared files collide too: ADR numbers,
a tracked `CURRENT_STATUS.md`.

## Decision

The single loop is unchanged; N copies of it run under these rules:

1. **One issue, one agent, one worktree, one branch.** Each issue is a
   complete handoff package (all fixed sections, 1 estimated session,
   see [work-units-as-external-tracker](../process/work-units-as-external-tracker.md)).
2. **Disjoint targets.** No two concurrent issues share a path in
   `Target`. Overlap means serialize, not parallelize.
3. **Decide before branching.** Every ADR the batch needs lands on
   `main` before the loops start
   ([adr-before-implementing](adr-before-implementing.md)).
4. **A mid-loop decision stops the loop.** If a loop surfaces an ADR or
   a convention correction, it lands on `main` as its own PR; sibling
   loops rebase before their next session.
5. **No shared counters, no shared status.** ADRs are named by slug
   ([adr-ids-date-slug](../process/adr-ids-date-slug.md));
   `CURRENT_STATUS.md` is untracked, one per worktree, even for a solo
   developer ([current-status-per-developer](../process/current-status-per-developer.md)).
   The tracker is the orchestrator's view of all loops.
6. **Same procedures everywhere.** Skills are installed at project scope
   and committed ([agent-skills-as-procedures](agent-skills-as-procedures.md)),
   so every worktree and every vendor runs the same rituals.
7. **Merge serially, review against current `main`.** Rebase each PR on
   the latest `main` and run `/review-pr` there, so the review loads any
   ADR a sibling merged first.
8. **N = review capacity.** Start with 2–3 loops. The human remains the
   checkpoint at every merge, not at the end of a chain.

## Alternatives Considered

1. **Several agents in one worktree.** No file isolation; edits
   interleave and no diff maps to one issue.
2. **Agent-to-agent pipelines.** Moves review to the end of the chain,
   where early drift has compounded. Rejected in
   [single-loop-human-orchestrator](single-loop-human-orchestrator.md).
3. **A live shared status file across worktrees.** Re-creates the
   merge-conflict magnet and injects every loop's WIP into every other.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- Every open PR maps to one issue, and no two open PRs for in-flight
  issues share a changed path
  (`gh pr diff <n> --name-only`, intersected pairwise).
- ADR files arrive in PRs that contain only decision changes, or in the
  PR of the issue that listed them; feature PRs from sibling loops
  never introduce one.
- `docs/CURRENT_STATUS.md` is in `.gitignore`; the ADR slug check passes.

## Trade-offs

- Serial merges cost a rebase per PR, and rule 4 pauses siblings. Both
  are the price of catching drift at the merge, not after it.
- Disjoint targets cap parallelism by architecture; a tangled codebase
  gets little from more loops.
- Hooks run only in Claude Code; CI is the layer that holds every
  vendor's loop to the same checks.
