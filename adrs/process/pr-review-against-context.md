<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Review the PR Against Context, Not the Code

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your project ships work via PRs (branch → review → merge).
- The repo already has CFD context (`CLAUDE.md`, ADRs,
  `CONVENTIONS.md`, an issue tracker with AC checklists).
- You want PR review to scale to small teams without becoming the
  bottleneck — or you want a fast pre-review pass before a human
  reviewer engages.

Skip if you commit straight to `main`, or if your PRs do not link to
issues with explicit AC.

## Context

PR review is the last validation before code reaches `main`. Without
discipline, an agent asked to review a PR will **scan every changed
file in full**, re-derive the project's intent from the code, and pay
`O(diff size + touched file sizes)` tokens — often well over 30k for
a modest PR.

But CFD's central bet is that the project's intent does NOT need to
be re-derived. It is already captured in:

- The linked issue's **AC checklist** (the "what must be true").
- The repo's **`CONVENTIONS.md`** (the "how we do things here").
- The relevant **ADRs** (the "why we chose this, what we rejected").
- The **PR template** (the "what the PR body should say").

A PR review that reads the diff and cross-checks against these
indices runs at `O(diff size)` — typically 3–6k tokens total — and
catches strictly more issues than a "read every file and judge"
review, because indices include rejected alternatives the code alone
cannot reveal.

## Decision

PR review on this project is mediated by a `/review-pr <n>` slash
command (or equivalent Skill) that:

1. **Fetches** PR metadata + diff via `gh pr view` and `gh pr diff`.
2. **Loads context first**: `docs/CONVENTIONS.md`, the linked issue
   body (AC + "ADRs to load"), each named ADR, and the PR template
   if `.github/PULL_REQUEST_TEMPLATE.md` exists.
3. **Cross-checks** the diff against each context artifact:
   - **AC checklist**: implemented? missing items? extras?
   - **`CONVENTIONS`**: respected?
   - **Touched ADRs**: consistent with each ADR's *Verifiable
     Consequences*?
   - **PR template**: required sections filled?
   - **Branch / PR title**: conform to project rules?
4. **Reports** ✓ / ⚠ / ✗ per item. Does NOT auto-fix.

**No full-file scans by default.** If the diff is too narrow to be
understood on its own, the command names the file it needs and
explains why. Silent scope expansion is forbidden.

## Alternatives Considered

1. **Full-file read on every PR.** Simple; pays `O(repo)` tokens per
   review; re-derives intent the indices already hold.
2. **Diff only, no context load.** Fast but misses ADR / convention
   violations the diff alone cannot reveal.
3. **Skip the machine review step.** PRs land without checks;
   defects surface in production. False economy.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- A `/review-pr` (or equivalent) procedure exists in
  `.claude/commands/` or `.claude/skills/`.
- Recent PR comment threads reference specific ADRs and
  `CONVENTIONS` lines, not generic "looks good" reactions.
- Tokens-per-review correlate with **diff size**, not with **repo
  size**.

## Trade-offs

- The review depends on context being current. Stale `CONVENTIONS`
  or out-of-date ADRs poison the review. Mitigation:
  `/context:validate` runs periodically.
- Diff-only can miss issues that surface only on a full file read
  (e.g. a refactor that breaks an invariant elsewhere). The
  named-file escape hatch exists for that case.
