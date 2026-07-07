<!-- Shareable ADR. Token budget: ~550. -->

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

Skip if your sessions are inherently short (one-shot tasks, REPL) or
your context is not yet persistent enough that restarting is cheap.

## Context

Even with very large context windows (200k, 1M, 2M tokens), an AI
agent's adherence to project conventions, the current issue's
acceptance criteria, and previously-loaded ADRs degrades as the
session's context fills. This is documented, not anecdotal: models
retrieve and follow instructions positioned mid-context markedly
worse than at the edges ([Liu et al., "Lost in the Middle," TACL
2024](https://arxiv.org/abs/2307.03172)), and performance on tasks
held constant degrades as input length grows ([Chroma, "Context
Rot," 2025](https://research.trychroma.com/context-rot)). Observable
failure modes: re-introducing rejected patterns, inventing
"conventions" that conflict with `docs/CONVENTIONS.md`, losing track
of the current AC item, mis-citing ADRs by number.

The driver is **context volume and composition, not wall-clock
time**. An hour of light back-and-forth is harmless; twenty minutes
of verbose test output and multi-file diffs is not. Curated context
(ADRs, conventions, the issue) gets buried under accumulated tool
output. Bigger windows do not fix the attention problem.

The fix is procedural: **restart before drift sets in**. CFD makes
the restart cheap because context lives outside the session —
`CURRENT_STATUS.md` (state), `CONVENTIONS.md` (rules), ADRs
(rationale), the tracker issue (AC checklist). A fresh
`/session:start` reaches readiness in ~1.5–3k tokens. **There is no
progress to lose.**

## Decision

Treat each working session as **disposable**, and trigger the restart
on **context signals**, in priority order:

1. **Drift observed** (any failure mode above) → close + restart
   immediately, even mid-task.
2. **Context fill** — the session has accumulated large tool output
   (long test runs, wide diffs, log dumps), or the agent reports
   high context usage / auto-compacts → close + restart at the next
   natural boundary (an AC item done).
3. **Wall-clock fallback** — only when the agent exposes no context
   signal: soft ceiling ~1 hour, hard ceiling ~2 hours.

Do not chain related work across one giant session. For non-trivial
AC items, one session per AC item is the right cadence. The
[session-close-ritual](../process/session-close-ritual.md) ADR
defines the mechanic that makes the restart cheap; this ADR defines
*when* to fire it.

## Alternatives Considered

1. **Long single sessions.** Avoids restart overhead; pays for it in
   code that ignores conventions and a model that loses track of what
   it agreed to. Always loses on net.
2. **Per-AC-item sessions, always.** Over-decomposition; pays the
   session-start cost (~1.5k tokens) more often than necessary.
3. **Wall-clock as the primary trigger.** Simple but measures the
   wrong thing: time correlates with context volume only loosely.
   Kept solely as the fallback when no context signal is available.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- Sessions end at AC-item boundaries, not at exhaustion; transcripts
  show `/session:close` firing before auto-compaction, not after.
- `docs/CURRENT_STATUS.md` shows multiple updates per day during
  active work, not one nightly mega-update.
- PRs land in the "1 PR ≈ 1 session" cadence rather than "1 PR =
  several days' chat history."

## Trade-offs

- Restart costs ~1.5–3k tokens. Cheaper than drift, which costs
  minutes of re-prompts plus code that has to be redone.
- Context-fill triggers require judgment (or an agent that surfaces
  usage); the wall-clock fallback stays as the teachable heuristic.
