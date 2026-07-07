<!-- Shareable ADR. Token budget: ~450. -->

# ADR-`<NNN>`: Enforce Rituals with Hooks and CI, Not Discipline

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your project runs the CFD session rituals (`/session:start`,
  `/session:close`) and you have observed them being skipped under
  deadline pressure.
- Your agent supports lifecycle hooks (Claude Code `settings.json`
  hooks, or an equivalent), or your repo has CI.

Do NOT adopt the blocking layer on projects where most commits are
legitimately doc-free (e.g. a scratch repo); the escape hatch would
become the default and teach everyone to ignore the guard.

## Context

CFD Principle 6 promises "automation through slash commands", but a
slash command is automation the human must *remember to invoke* — the
same failure mode the session-close ritual ADR criticizes in ad-hoc
updates ("predictably skipped under deadline pressure"). A ritual
whose only enforcement is discipline degrades exactly when the
project is busiest, and stale context then actively misleads the
next session. The fix is to move enforcement from memory to
mechanism, at the moments where the workflow already stops.

## Decision

Layer mechanical enforcement under the rituals, keeping the portable
slash commands as the source of truth:

1. **Session start → hook.** A `SessionStart` hook injects
   `docs/CURRENT_STATUS.md` + `docs/decisions/_index.md` into
   context automatically and warns when the newest commit is more
   than a day newer than the last `CURRENT_STATUS.md` update.
2. **Session close → commit-time guard.** A `PreToolUse` hook on the
   shell tool blocks `git commit` when code is staged but
   `docs/CURRENT_STATUS.md` is not, with an actionable message and a
   deliberate `[skip-status]` escape hatch.
3. **Team backstop → CI WARN.** A workflow annotates (never blocks)
   PRs that change code without touching `CURRENT_STATUS.md`.

Hooks are agent-specific (layer 1–2 ships for Claude Code); the CI
layer is agent-agnostic. Teams on other agents keep the commands and
the CI check and lose only the local automation. When
`CURRENT_STATUS.md` is untracked (per-developer mode, see
[current-status-per-developer](../process/current-status-per-developer.md)),
layers 2–3 skip themselves and layer 1 falls back to file mtime.

## Alternatives Considered

1. **Discipline only (status quo).** Free, portable — and reliably
   skipped when it matters most; the ritual ADR itself predicts this.
2. **Blocking CI check.** Enforces at the wrong distance: feedback
   arrives after push, when the session that had the context is gone.
   WARN in CI, block at commit time instead.
3. **Auto-generate `CURRENT_STATUS.md` from `git log`.** Loses the
   "why" and "blocked by"; already rejected by the session-close
   ritual ADR.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `.claude/settings.json` registers `SessionStart` and `PreToolUse`
  hooks pointing at scripts under `.claude/hooks/`.
- `git log --format=%H -- docs/CURRENT_STATUS.md` shows commits that
  also touch source files — the same-commit rule holds in history.
- `[skip-status]` appears rarely in `git log --grep`; frequent use
  means the guard is mis-tuned for the repo.

## Trade-offs

- Hook scripts are per-agent maintenance surface; a Claude Code hook
  does nothing for a Gemini CLI teammate (CI covers them).
- A commit-time block adds friction on genuinely doc-free commits;
  the escape hatch trades a few keystrokes for an audit trail.
- The staleness heuristic (1 working day) is approximate and will
  occasionally warn on weekends or vacations. False positives cost
  one glance; false trust in stale context costs a session.
