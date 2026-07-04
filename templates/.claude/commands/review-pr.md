---
description: "Review a PR against the team's curated checklist sourced from ADRs, CONVENTIONS, the linked issue's acceptance criteria, and the PR template. Report findings; do not auto-fix."
argument-hint: "[pr-number]"
token-budget: "scales with the team's checklist depth, typically 3k–15k"
---

The user passes a PR number. If not provided, infer from the current
branch:

```bash
gh pr status --json number --jq '.currentBranch.number'
```

If still no PR, ask.

## 1. Fetch PR metadata + diff + commit history

```bash
gh pr view <n> --json baseRefName,headRefName,title,body,labels,commits,closingIssuesReferences
gh pr diff <n>
git log <base>..<head> --pretty=format:%s     # branch commit story
```

## 2. Load context indices that define the agenda

- `docs/CONVENTIONS.md`
- `docs/decisions/_index.md`
- The **linked issue body** via `gh issue view <issue-n>` — extract
  the AC checklist and the "ADRs to load" list.
- **Each ADR named in the issue body** under `docs/decisions/`.
- The **PR template** if `.github/PULL_REQUEST_TEMPLATE.md` exists.

## 3. Read changed files to the depth this team's checklist demands

The depth is a project decision, not a methodology rule. Read what
you need to verify the checklist below — no more, no less.

## 4. Apply the team's checklist

This section is **the team's curated review agenda**. Replace the
placeholders with your project's real rules. Each item must cite the
specific ADR / CONVENTIONS line / AC item it derives from.

```
### Workflow

- Branch name follows `<your convention>` (ADR-NNN).
- Base branch is `main` (ADR-NNN trunk-based).
- PR title is Conventional Commits ≤70 chars (CONVENTIONS L<n>).
- PR body references `Closes #<n>` when an issue exists.
- All commits, branch, PR title, PR body are English (Principle 5).
- No `Co-Authored-By: Claude` / "Generated with Claude Code"
  attribution anywhere (CLAUDE.md rule).

### Architecture (per project ADRs)

- <ADR-N: rule + verifiable consequence>
- <ADR-M: rule + verifiable consequence>

### Conventions

- <CONVENTIONS L<n>: rule>
- <CONVENTIONS L<m>: rule>

### Acceptance criteria

- Each `[ ]` from the linked issue is implemented in this PR.
- No extra changes outside the AC scope.

### Documentation drift

- Touched a component / module with a README? Update it in the same PR.
- Touched an ADR-described pattern? Verify the ADR's Verifiable
  Consequences still hold.
- Touched CONVENTIONS-described conventions? Same.

### Testing (per project ADRs)

- <test naming / coverage / mocking rules>
```

Add more sections as your team's ADRs surface them.

## 5. Output a structured review

```text
## Critical (must fix before merge)
- <file>:<line> — <issue> — citation: <ADR-N or CONVENTIONS L<n>>
  Suggested fix: <one-line>.

## Suggestions (should fix)
- <file>:<line> — <issue> — citation.

## Nits (nice to have)
- <file>:<line> — <issue>.

## Summary
- Overall assessment.
- AC coverage: X / Y items satisfied.
- Architecture compliance: ✓ / ⚠ / ✗.
- Tokens consumed: ~<n>k.
```

## Rules

- **Do NOT auto-fix.** Report only; the author fixes on the next
  session.
- **English only.**
- **No silent scope expansion.** If the checklist genuinely needs a
  rule that is not yet in CONVENTIONS or an ADR, surface it as a
  finding ("missing convention for X") and propose `/decision:new`
  before the next review.
