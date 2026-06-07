<!-- Shareable ADR. Token budget: ~400. -->

# ADR-`<NNN>`: The Session-Close Ritual

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Always, in any project where work happens across multiple AI sessions.

## Context

The single most common context-loss failure mode: a session produces
good work, the session closes, the next session starts, and the agent
has no record of what was just done. The user pays the cost in
re-explanation tokens — or, worse, the agent invents a different plan
and contradicts the prior work. The fix is procedural, not technical.

## Decision

Every session ends with the `/session:close` ritual:

1. **Update `docs/CURRENT_STATUS.md`:**
   - Move completed items from "In Progress" to "Recently Completed".
   - Note anything still pending or newly surfaced.
   - Update "Known Issues" if new issues were discovered.
   - Re-rank "Next Priorities".
   - Update the "Last updated" date.
2. **Update `docs/CONVENTIONS.md`** if any convention was clarified.
3. **Write an ADR** if any significant decision was made informally
   during the session.
4. **Stage all `docs/` changes in the SAME commit/PR** as the code
   changes. Context updates ship with code, not separately.

The ritual is **non-negotiable**. If a session ends without it, the next
session starts with stale context — and you'll feel it.

## Alternatives Considered

1. **Update `CURRENT_STATUS.md` ad-hoc when convenient.** Predictably
   skipped under deadline pressure.
2. **Auto-generate `CURRENT_STATUS.md` from `git log`.** Loses the
   "why" and the "blocked by"; commit messages are too terse.
3. **Use a PM tool (Jira, Linear) instead.** Fine for humans; the agent
   doesn't read those by default, so the project-context surface stays
   blind to them.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `git log -1 --format=%ar -- docs/CURRENT_STATUS.md` is never older
  than the last working day during active development.
- Every PR that touches `src/` also touches
  `docs/CURRENT_STATUS.md`. A CI check can WARN (not block) when this
  is not true.

## Trade-offs

- ~3–5 minutes per session. Recovered 10× in the next session's faster
  startup.
