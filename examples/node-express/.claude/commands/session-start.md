<!-- Slash command: /session:start
     Token budget: ~500–1,500 baseline;
     +1,000–2,000 if an in-progress issue is auto-loaded. -->

Read the following files in order, then produce a brief summary:

1. `docs/CURRENT_STATUS.md` — what is in progress, what is blocked,
   what is next.
2. `docs/decisions/_index.md` — recent decisions that might affect
   current work.

Then state:

- What was being worked on at the last session close.
- What is currently blocked and why.
- What should be the focus of THIS session.

**Auto-load in-progress issue.** If `docs/CURRENT_STATUS.md` references
an in-progress item by `#N`, run `gh issue view <n>` and surface its
title + acceptance criteria. (In this OFFLINE EXAMPLE the `#N` values
are illustrative — skip the `gh issue view` call and instead remind the
user that this is the example.)

Do NOT read source code files yet. Source code reading happens after
the focus is chosen.

If `docs/CURRENT_STATUS.md` was last updated more than 1 working day
ago, warn the user that the context may be stale before proceeding.
