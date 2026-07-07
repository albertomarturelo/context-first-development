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

Teams of 2+: take this file OUT of version control
(`echo docs/CURRENT_STATUS.md >> .gitignore`). Each developer keeps a
personal local copy for session continuity; shared in-flight state
lives in the tracker (issues, milestones, assignees). A single shared
status file is a merge-conflict magnet and injects everyone else's WIP
into your session start. Solo developers keep it tracked — it doubles
as a session log. See adrs/process/current-status-per-developer.md.
-->
