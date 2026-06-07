<!-- Slash command: /review-pr <PR-number>
     CFD review using THIS project's checklist (Node 22 + Express 5
     + Postgres). The agenda comes from the project's CONVENTIONS +
     ADRs; the depth of file reading is what the agenda demands.
     Token budget: ~4k–8k typical. -->

The user passes a PR number. If not provided:

```bash
gh pr status --json number --jq '.currentBranch.number'
```

## 1. Fetch PR + commits + diff

```bash
gh pr view <n> --json baseRefName,headRefName,title,body,labels,commits,closingIssuesReferences
gh pr diff <n>
git log <base>..<head> --pretty=format:%s
```

## 2. Load context indices

- `docs/CONVENTIONS.md`
- `docs/decisions/_index.md`
- The linked issue body via `gh issue view <issue-n>`.
- Each ADR named in the issue (`docs/decisions/00<n>-*.md`).
- `.github/PULL_REQUEST_TEMPLATE.md` if present.

## 3. Read changed files to the depth this checklist demands

For this project: read every changed file in full under
`src/notifications/`. The layer rules (ADR-001, ADR-002) require
verifying cross-layer imports, which a diff alone cannot show.

## 4. Apply this project's checklist

### Workflow (ADR-004 trunk-based)

- Branch name: `feature/* | fix/* | chore/* | docs/*` (or
  `rc/X.Y.Z` / `hotfix/*`). Issue-linked branches prefix with the
  tracker ID.
- Base branch: `main` for every branch type.
- PR title: Conventional Commits (`feat(scope): …`, `fix(scope): …`,
  `chore(scope): …`, `docs(scope): …`), ≤70 chars.
- PR body references `Closes #<n>` when an issue exists.
- Every commit on the branch follows Conventional Commits.
- No `Co-Authored-By: Claude` / "Generated with Claude Code" /
  "🤖 Generated" attribution anywhere (project rule).
- All commit messages, branch name, PR title, PR body, code
  comments are English (CFD Principle 5).

### Architecture (ADR-001 layered + ADR-002 repository pattern)

- `src/notifications/domain/` files **do not import from `data/` or
  `presentation/`**. `grep -E "from '(.*/)?(data|presentation)/" src/notifications/domain/`
  must return 0 results.
- `src/notifications/presentation/` files do not import from `data/`
  except via the repository **interface** declared in `domain/`.
- All persistence touches `Pool` only inside
  `src/notifications/data/`. `grep "pool.query" src/notifications/domain/`
  and `grep "pool.query" src/notifications/presentation/` must
  return 0 results.
- Use cases (`SendNotification`, future ones) depend on the
  repository interface, not the concrete class. Verify no `new
  PostgresNotificationRepository(...)` outside `src/app.ts`.

### Testing (ADR-003 integration over mocks)

- New tests under `src/**/domain/` use the hand-written
  `InMemoryNotificationRepository` class (or equivalent fake) —
  **never** `vi.mock(...)` on the repository interface.
- New tests under `src/**/data/` run against the real Postgres in
  `docker-compose.test.yml`. `grep -E "vi\.mock\(.*pg|new Mock\(\)" src/**/data/*.test.ts`
  must return 0 results.
- Test file names: `<source>.test.ts` next to the source.

### Conventions (CONVENTIONS.md)

- TypeScript `strict: true` honored — no new `any`, no implicit
  `any` from removed annotations.
- Named exports only; no `export default` added.
- Public method return types explicitly annotated when async.
- Imports use the `.js` suffix (NodeNext resolution).

### Acceptance criteria

- Each `[ ]` from the linked issue body is implemented in the diff.
- No extra changes outside the AC scope. If found, ask the author
  to split into a separate PR.

### Documentation drift

- Diff touches a pattern an ADR governs? Confirm the ADR's
  "Verifiable Consequences" still hold; if not, propose an ADR
  amendment in the next session.
- Diff introduces a recurring pattern not in CONVENTIONS? Surface
  as a finding and recommend `/decision:new`.

## 5. Output

```text
## Critical (must fix before merge)
- <file>:<line> — <issue> — cites ADR-N / CONVENTIONS L<n>.

## Suggestions
- <file>:<line> — <issue> — citation.

## Nits
- <file>:<line> — <issue>.

## Summary
- AC coverage: X / Y items satisfied.
- Architecture compliance: ✓ / ⚠ / ✗.
- Tokens consumed: ~<n>k.
```

## Rules

- Report only. No auto-fix.
- English only.
- If a finding requires a rule that does not yet exist, surface it
  and recommend `/decision:new` — do NOT invent a rule on the spot.
