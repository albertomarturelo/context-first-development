<!-- Shareable ADR. Token budget: ~400. -->

# ADR-`<NNN>`: Atomic Task Instructions for AI Sessions

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Always, in any project using an AI coding agent.

## Context

AI agents perform poorly on vague, multi-objective prompts ("implement
the notification system") and well on scoped, single-objective prompts.
Without this convention, sessions drift, output diverges from project
conventions, and tokens are wasted on the agent re-discovering context
for each sub-task. The agent also accumulates **tunnel vision** as the
prompt grows fuzzy — it picks one sub-task to start and forgets the
others.

## Decision

Every implementation instruction MUST include:

1. **One objective**, expressed as a single deliverable.
2. **The exact target location** (file path or directory).
3. **The reference ADR or pattern** to follow.
4. **One example to mirror**, when one exists in the codebase.

**Bad:**

```
Implement the notification system.
```

**Good:**

```
Create the notification repository interface in src/notifications/domain/.
Follow the repository pattern from ADR-007.
Mirror src/users/domain/user-repository.ts for shape and naming.
```

If a task can't be expressed atomically, decompose it first — that
decomposition is part of the work, not overhead.

## Alternatives Considered

1. **Trust the agent with vague prompts and iterate.** Common; produces
   inconsistent output and consumes 3–5× more tokens.
2. **Always write a detailed spec before any prompt.** Overkill for
   small tasks. The atomic-prompt rule is the minimum viable spec.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- A session log of prompts can be skimmed: every implementation prompt
  has a target path AND a reference (ADR or example).
- Re-prompts ("no, not that, do X instead") drop measurably between
  before and after adoption.

## Trade-offs

- 1–2 extra sentences per prompt. Saves 5–10× that in re-prompt rounds.
