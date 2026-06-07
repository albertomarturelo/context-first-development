<!-- Shareable ADR. Token budget: ~550. -->

# ADR-`<NNN>`: Review the PR Against Context, Not Against Intent Discovery

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your project ships work via PRs (branch → review → merge).
- The repo has CFD context (`CLAUDE.md`, ADRs, `CONVENTIONS.md`,
  issue tracker with AC checklists, optionally a PR template).
- You want PR review to scale, to be reproducible across reviewers,
  and to apply the team's rules mechanically.

Skip if you commit straight to `main`, or if your PRs do not link to
issues with explicit AC.

## Context

PR review is the last validation before code reaches `main`. Without
indices, an agent asked to review a PR has to **discover the project's
intent from the code** — what patterns it uses, what conventions
apply, why certain choices were made. That discovery work scales with
repo size and burns the most tokens.

CFD's bet is that intent does NOT need re-discovery. It is captured
in:

- The linked issue's **AC checklist** (the "what must be true").
- `CONVENTIONS.md` (the "how we do things here").
- The relevant **ADRs** with their *Verifiable Consequences*.
- The **PR template** (the "what the PR body must contain").
- Any **team-specific review checklist** the project defines.

A CFD review loads those first, then applies them as a verification
agenda against the diff AND the changed files. **The depth of file
reading is a project-level decision, codified in the slash command
itself.** A strict KMP project reads every changed file in full
because the ADRs demand layer-boundary checks, Compose recomposition
safety, networking conventions, etc. A small Node API may stop at the
diff. The work is verification against known rules, not discovery
from scratch.

## Decision

PR review on this project is mediated by a `/review-pr <n>` slash
command (or equivalent Skill) that:

1. **Fetches** PR metadata + diff via `gh pr view` / `gh pr diff`,
   plus the branch's commit history.
2. **Loads the indices** that define the verification agenda:
   `CONVENTIONS`, the linked issue body, every ADR named there, the
   PR template, and any team-curated review checklist embedded in
   the slash command body.
3. **Reads source files to the depth the agenda requires.** No
   project-agnostic "minimize reads" rule — the team's checklist
   decides. Reads in service of verification, not discovery.
4. **Reports** ✓ / ⚠ / ✗ per checklist item, citing the specific
   ADR / CONVENTIONS line / AC item being satisfied or violated.
5. **Does NOT auto-fix.** Findings are surfaced for the author to
   address on the next session.

The slash command body itself **is** the team's checklist — it
evolves with the project (new convention → new line in the slash
command), echoing the `document-corrections-not-fixes` discipline.

## Alternatives Considered

1. **Discovery-driven review (no indices).** Scales with repo size;
   re-derives intent each PR; ignores rejected alternatives that
   live only in ADRs. The default everywhere CFD is not adopted.
2. **Project-agnostic depth rule** (e.g. "always read full files" or
   "always diff only"). Rejected — depth belongs to the team, not the
   methodology.
3. **External code-review SaaS.** Useful complement; doesn't load
   your ADRs as the agenda.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- A `/review-pr` (or equivalent) exists in `.claude/commands/` or
  `.claude/skills/` and its body **embeds the team's checklist**
  citing real ADR numbers and CONVENTIONS sections.
- Recent PR comment threads reference specific ADRs / CONVENTIONS
  lines, not generic "looks good" reactions.
- The slash command grows with the project: `git log` on its file
  shows additions after new conventions land.

## Trade-offs

- Depends on indices being current. Stale CONVENTIONS or out-of-date
  ADRs poison the review. Mitigation: `/context:validate` + the
  `document-corrections-not-fixes` discipline.
- Customizing the checklist is upfront work; pays back from review 1.
