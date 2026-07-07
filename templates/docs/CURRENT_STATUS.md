<!-- Loaded at the START of every session. Updated at the END. -->

# Current Project Status

Last updated: <YYYY-MM-DD>

## In Progress

- [ ] <task description> (#<issue>)
  - <sub-state, e.g. "endpoint created, missing validation tests">
  - Blocked by: <if applicable>

## Recently Completed

- [x] <task> (#<issue>)

## Known Issues

- <issue + symptom + workaround, if any>

## Next Priorities

1. <highest priority>
2. <next>
3. <next>

<!--
Update discipline:
- Always update before closing the session. Non-negotiable.
- Commit the update in the SAME PR as the session's code changes.
- If you haven't updated this in >1 working day, your context is stale.
- `git log -1 --format=%ar -- docs/CURRENT_STATUS.md` should never read
  older than the last working day during active development.

Teams of 2+: because every PR touches this file, a single shared list
becomes a merge-conflict magnet. Split "In Progress" into one
subsection per person (### <name>), keep the rest shared, and compact
"Recently Completed" weekly. Conflicts then stay inside each person's
own subsection.
-->
