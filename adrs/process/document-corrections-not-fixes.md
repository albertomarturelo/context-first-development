<!-- Shareable ADR. Token budget: ~400. -->

# ADR-`<NNN>`: Document the Convention, Not Just the Fix

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Always, in any project using an AI coding agent. This is a workflow ADR,
not a technical one — it codifies a habit.

## Context

When an agent generates code that violates a project convention, the
default response is to fix it inline and move on. This wastes the fix:
next session, the agent will violate the same convention again — because
the convention exists only in the user's head, not in the agent's
context. The team pays the same correction cost forever.

## Decision

Whenever you correct an agent's pattern, the correction is incomplete
until BOTH of the following are true:

1. The wrong code is fixed.
2. The convention that was violated is documented in
   `docs/CONVENTIONS.md` — or, if it's substantial enough to deserve
   alternatives consideration, in a new ADR.

The completion phrase to use with the agent:

> "Fix the code AND add this rule to `docs/CONVENTIONS.md` under
> `<section>`."

If a convention is broken twice without being documented, the team owes
itself a short retro on why.

## Alternatives Considered

1. **Trust the agent to learn within the session.** Doesn't survive
   session restart.
2. **Add the rule to `CLAUDE.md` directly.** Inflates the root file;
   `CLAUDE.md` is an index, not a rulebook.
3. **Only document violations after the third occurrence.** The cost
   compounds; "we'll deal with it later" is exactly how mock-vs-real
   testing went wrong.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `git log docs/CONVENTIONS.md` shows ~1 entry per week minimum during
  active development. If it goes flat for a sprint, either the project
  is mature or corrections are being silently applied.
- New conventions surface in the SAME PR as the code that motivated
  them, not in a follow-up PR.

## Trade-offs

- Adds ~30 seconds per correction. Payback: "I don't have to explain
  this again in a month."
