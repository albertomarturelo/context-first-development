<!-- Slash command: /review-pr <PR-number>
     Review a PR against context (ADRs + CONVENTIONS + linked issue
     AC + PR template) without scanning full files.
     Token budget: ~3,000–6,000 total. -->

The user passes a PR number. If not provided, infer from the current
branch via `gh pr status --json number --jq '.currentBranch.number'`.

1. **Fetch PR metadata + diff** (this is the operational heart — do
   it BEFORE reading anything else):

   ```bash
   gh pr view <n>
   gh pr diff <n>
   ```

2. **Load context indices** the review will check against:

   - `docs/CONVENTIONS.md`
   - `docs/decisions/_index.md`
   - The **linked issue body** via `gh issue view <issue-n>` —
     extract the AC checklist and the "ADRs to load" list.
   - **Each ADR named in the issue body** under `docs/decisions/`.
   - **PR template** if `.github/PULL_REQUEST_TEMPLATE.md` exists.

3. **Cross-check the diff** against each artifact:
   - **AC checklist**: implemented? missing? extras?
   - **CONVENTIONS**: respected? cite the offending CONVENTIONS line.
   - **Touched ADRs**: consistent with each ADR's *Verifiable
     Consequences*? In this example project, that includes:
     - ADR-002 (repository pattern) — `grep` for `pool.query` in
       `src/notifications/domain/` should return 0 results.
     - ADR-003 (integration over mocks) — `grep` for `vi.mock` in
       `src/**/data/*.test.ts` should return 0 results.
     - ADR-004 (trunk-based) — branch name follows convention; PR
       targets `main`.
   - **PR template**: required sections filled?
   - **Branch name** and **PR title**: Conventional Commits?

4. **Output a structured report**:

   ```text
   ## Review summary

   ### ✓ Passes
   ### ⚠ Watch
   ### ✗ Blocks merge

   ### Notes
   - Tokens consumed: ~<n>k (target <6k).
   ```

5. **Do NOT auto-fix.** Report only.

**Hard rule: NO full-file reads by default.** If the diff is too
narrow to be understood on its own, name the file you need to read
and explain why before reading it. The diff + indices are the
review.

English only.
