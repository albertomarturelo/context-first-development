<!-- Shareable ADR. Token budget: ~400. -->

# ADR-`<NNN>`: Write the ADR Before Implementing the Decision

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Always, for any decision that:

- Introduces a new tool, library, framework, or service.
- Changes a convention (testing strategy, layer boundaries, error
  handling).
- Adds a workflow step (CI, deployment, release).
- Picks one of several plausible patterns.

Skip for trivial choices (a CSS color, a log message phrasing) and bug
fixes that don't change a pattern.

## Context

When a decision is implemented first and "documented later," the
documentation rarely catches up. The decision survives in code, but its
rationale and rejected alternatives evaporate. Future sessions (and
future humans) cannot reconstruct WHY — they only see WHAT. The agent
will then suggest refactoring back toward a rejected alternative,
because nothing tells it the alternative was already evaluated and
dismissed.

This is also how AI agents develop **tunnel vision**: each session sees
only the current state and proposes locally optimal changes that
contradict earlier global decisions.

## Decision

Before any qualifying change is implemented:

1. Run `/decision:new`.
2. Articulate Context, Decision, Alternatives Considered, Consequences.
3. Save as `docs/decisions/<NNN>-<slug>.md`.
4. Update `docs/decisions/_index.md`.
5. **Only THEN** implement.

If the implementation reveals a flaw in the decision, supersede the ADR
with a new one — do not silently change behavior.

## Alternatives Considered

1. **Document decisions in PR descriptions.** PRs aren't loaded by the
   agent on session start. They're discoverable only via `gh pr view`
   archaeology.
2. **Document decisions in a wiki / Confluence.** Same problem: not in
   the agent's context.
3. **Only document after the decision proves correct.** Selection
   bias — you lose the record of decisions that turned out wrong, which
   is the most useful kind to keep.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- The `git log` of `docs/decisions/` shows the ADR file landing in the
  SAME PR (or an earlier one) as the code change it justifies.
- Reverting a feature also reverts (or supersedes) its ADR, atomically.

## Trade-offs

- Adds ~10 minutes per significant decision. Recovers that within 1–2
  future sessions that would otherwise re-litigate the same question.
