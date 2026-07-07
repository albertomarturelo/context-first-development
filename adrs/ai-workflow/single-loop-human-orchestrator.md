<!-- Shareable ADR. Token budget: ~450. -->

# ADR-`<NNN>`: One Loop, with the Developer as Orchestrator

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- An individual or small team (2–20) supervises AI-generated changes
  to production code and accountability per change matters.
- Your CFD persistence (ADRs, conventions, tracker issues) is in
  place — it is what makes each loop iteration cheap to restart and
  cheap to review.

Reconsider when throughput demonstrably outgrows one loop: many
independent, well-specified issues idle in the tracker while review
capacity sits unused. See the migration note in Trade-offs.

## Context

Multi-agent orchestration (role agents handing artifacts to each
other, autonomous agent teams) buys throughput and separation of
concerns — and it moves the human checkpoint from *every decision* to
*the end of a chain*. CFD's drift thesis (see
[short-sessions-over-long](short-sessions-over-long.md)) says
adherence degrades as context accumulates; in an agent-to-agent
chain, an early drift compounds through every subsequent handoff
before a human sees it. For a small team paying its own tokens and
answerable for its production code, the review point belongs inside
the loop, not after it.

## Decision

CFD defines **no agent-to-agent handoff**. There is one working loop
(orient → take or create an issue → implement → close → review), and
the developer sits inside it in two roles:

- **Orchestrator** — chooses the issue, sets the session's focus,
  decides when a decision needs an ADR, fires the close ritual.
- **Observer** — reviews each AC item as it lands and each PR against
  context; catches drift at the session boundary, before it
  compounds.

Handoffs happen through **artifacts, not agents**: the issue body
(context, target, ADRs to load, pattern to mirror, AC) is the
package; whoever picks it up — the same developer tomorrow, a
teammate, or a future parallel agent — starts from the same spec.

## Alternatives Considered

1. **Role-agent pipelines (e.g. BMAD-Method).** Strong separation of
   concerns and genuine throughput; the cost is that human review
   moves to the end of the chain and token spend multiplies per
   role. A deliberate fit for larger or more autonomous setups than
   CFD's audience.
2. **Autonomous background agents per issue.** Attractive precisely
   because CFD issues are self-contained handoff packages; rejected
   as a *default* because unattended chains re-introduce the drift
   window CFD exists to close.
3. **No stance (leave orchestration undefined).** Reads as an
   oversight and invites ad-hoc agent chains without the persistence
   that makes them safe. An explicit scope choice documents the why.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- No workflow in the repo spawns an agent whose output feeds another
  agent without a human checkpoint between them.
- Every merged PR maps to a tracker issue and a human review
  (Scenario E) — the observer role is visible in history.
- Issue bodies are self-sufficient (parseable sections, ADRs listed)
  — the artifact, not a conversation, carries the handoff.

## Trade-offs

- Throughput is bounded by one human's orchestration attention.
  Parallelism is deliberately left on the table.
- The migration path is cheap by design: independent 1-session
  issues can run as parallel CFD loops (e.g. in git worktrees), one
  agent per issue, with the developer orchestrating N loops and
  reviewing N PRs against context. That evolution changes *how many*
  loops run — not a single artifact. Write it as its own ADR when
  evidence justifies it.
