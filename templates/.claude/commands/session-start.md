<!-- Slash command: /session:start (alias: /project:status)
     Invoke at the BEGINNING of every working session.
     Token budget: ~500–1,500 baseline;
     +1,000–2,000 if an in-progress issue is auto-loaded. -->

Read the following files in order, then produce a brief summary:

1. `docs/CURRENT_STATUS.md` — what is in progress, what is blocked, what
   is next.
2. `docs/decisions/_index.md` — any recent decisions that might affect
   current work.

Then state:

- What was being worked on at the last session close.
- What is currently blocked and why.
- What should be the focus of THIS session.

**Auto-load in-progress issue.** If `docs/CURRENT_STATUS.md` references
an in-progress item by issue number (e.g. `#142`), also run
`gh issue view <n>` for that issue and surface its title + acceptance
criteria. This reaches the same readiness state as if the user had
opened with `/issue:start <n>`. If multiple in-progress issues are
referenced, list them and ASK which to focus on — do NOT load all of
them blindly.

Do **NOT** read source code files yet. The point of this command is to
orient yourself in O(1k) tokens, not O(50k). Source code reading happens
after the focus is chosen.

If `docs/CURRENT_STATUS.md` was last updated more than 1 working day ago,
warn the user that the context may be stale before proceeding.

If `docs/decisions/_index.md` is empty, suggest running `/project:init`.
