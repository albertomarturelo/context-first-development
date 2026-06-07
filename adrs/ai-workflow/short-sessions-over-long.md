<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Short Sessions Over Long Ones

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- You use an AI coding agent on a real codebase across multiple
  sessions.
- Your project already has CFD persistence in place — `CLAUDE.md`,
  `docs/CURRENT_STATUS.md`, ADRs, an issue tracker. Without
  persistent context this ADR is risky (state would die with the
  session).
- You have observed the model drifting from conventions or ADRs as a
  session gets long.

Skip if your sessions are inherently short (one-shot tasks, REPL
exploration) or if your context is not yet persistent enough that
restarting is cheap.

## Context

Even with very large context windows (200k, 1M, 2M tokens), an AI
agent's adherence to project conventions, the current issue's
acceptance criteria, and previously-loaded ADRs **measurably
degrades as a single session lengthens**. After ~1 hour of continuous
work, common failure modes appear:

- Re-introducing patterns the catalog explicitly rejects.
- Silently inventing "conventions" that conflict with
  `docs/CONVENTIONS.md`.
- Losing track of which AC item is being implemented.
- Mis-summarizing or mis-citing ADRs by number.

This is not a token-budget problem. It is an attention /
instruction-adherence problem. Bigger windows do NOT push the drift
horizon out proportionally.

The fix is procedural: **restart the session before drift sets in**.
CFD makes this fix viable because context lives **outside the
session**:

- `docs/CURRENT_STATUS.md` carries in-flight state.
- `docs/CONVENTIONS.md` carries the rules.
- ADRs carry the rationale.
- The tracker issue carries the AC checklist.

A fresh `/session:start` reaches the same readiness state as the
previous session in ~1.5–3k tokens. **There is no progress to lose.**

## Decision

Treat each working session as **disposable**:

- **Soft ceiling: ~1 hour. Hard ceiling: ~2 hours.**
- Any drift signal above triggers an immediate `/session:close` +
  restart — even mid-task.
- Do not chain related work across one giant session. Decompose into
  multiple sessions. For non-trivial AC items, one session per AC
  item is the right cadence.

The [session-close-ritual](../process/session-close-ritual.md) ADR
defines the mechanic that makes the restart cheap. This ADR defines
*when* to fire it.

## Alternatives Considered

1. **Long single sessions.** Avoids restart overhead; pays for it in
   code that ignores conventions and a model that loses track of what
   it agreed to. Always loses on net.
2. **Per-AC-item sessions, always.** Over-decomposition; pays the
   session-start cost (~1.5k tokens) more often than necessary.
3. **Watch token usage as the trigger.** Plausible but indirect. The
   real signal is *drift*, not token count. Models with bigger
   windows drift on the same schedule.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- Most sessions on this project last 30–60 minutes, not 3+ hours.
- `docs/CURRENT_STATUS.md` shows multiple updates per day during
  active work, not one nightly mega-update.
- PRs land in the "1 PR ≈ 1 session" cadence rather than "1 PR =
  several days' chat history."

## Trade-offs

- Restart costs ~1.5–3k tokens. Cheaper than drift, which costs
  minutes of re-prompts plus code that has to be redone.
- Loses the "deep flow" appeal of long sessions. CFD's position: that
  flow is illusory once drift starts.
