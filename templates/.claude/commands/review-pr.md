<!-- Slash command: /review-pr <PR-number>
     Review a PR against the project's CONTEXT (ADRs + CONVENTIONS
     + linked issue AC + PR template) WITHOUT scanning full files.
     Token budget: ~3,000–6,000 total. -->

The user passes a PR number. If not provided, infer from the current
branch:

```bash
gh pr status --json number --jq '.currentBranch.number'
```

If still no PR, ask the user.

1. **Fetch PR metadata + diff** (this is the operational heart — do
   it before reading anything else):

   ```bash
   gh pr view <n>           # title, body, base branch, labels, linked issue
   gh pr diff <n>           # the diff itself; do NOT read full files
   ```

2. **Load the context indices** the review will check against:

   - `docs/CONVENTIONS.md`
   - `docs/decisions/_index.md` (orient on which ADRs exist)
   - The **linked issue body** via `gh issue view <issue-n>` —
     extract the **AC checklist** and the **"ADRs to load"** list.
   - **Each ADR named in the issue body** under
     `docs/decisions/<NNN>-*.md`.
   - **PR template** if `.github/PULL_REQUEST_TEMPLATE.md` exists.

   Token cost so far: ~2–4k. Still no full source file reads.

3. **Cross-check the diff against each artifact**, one at a time:

   - **AC checklist.** For each `[ ]` in the issue body: is it
     implemented in the diff? Missing items? Extras the issue
     does not authorize?
   - **CONVENTIONS.** Walk the relevant sections (code style,
     patterns, testing, naming, commits). Any diff line violating a
     stated convention? Cite the line number in CONVENTIONS.
   - **Touched ADRs.** For each ADR loaded: does the diff respect
     the ADR's *Verifiable Consequences*? (e.g. ADR-002 says no
     `pool.query` in `domain/` — does the diff add any?)
   - **PR template.** Did the PR body fill the required sections?
   - **Branch name** and **PR title.** Conform to the project's
     conventions (per the trunk-based ADR or equivalent)?

4. **Output a structured report**:

   ```text
   ## Review summary

   ### ✓ Passes
   - <item> (CONVENTIONS L42)
   - <item> (ADR-007 verifiable consequence #2)

   ### ⚠ Watch
   - <item> — non-blocking; suggest follow-up issue.

   ### ✗ Blocks merge
   - <item> — violates ADR-002 verifiable consequence #1.
     Concrete fix: <one-line>.

   ### Notes
   - Tokens consumed: ~<n>k (target: <6k).
   ```

5. **Do NOT auto-fix.** Report only. The author runs `/issue:start`
   or `/decision:new` to address the findings on their next
   session.

**Hard rule: NO full-file reads by default.** If the diff is too
narrow to be understood on its own, **name the file** you need to
read and **explain why** before reading it. Silent scope expansion
is forbidden — that is the discipline. The diff + indices are the
review.

English only.
