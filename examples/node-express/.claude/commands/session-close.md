<!-- Slash command: /session:close
     Token budget: ~500–1,000. -->

Before this session ends, do ALL of the following:

1. **Update `docs/CURRENT_STATUS.md`:**
   - Move completed items from "In Progress" to "Recently Completed".
   - Add new items uncovered this session.
   - Update "Known Issues" if anything new surfaced.
   - Re-rank "Next Priorities".
   - Update the "Last updated" date to today.

2. **If a convention was clarified or a pattern was corrected this
   session**, update `docs/CONVENTIONS.md`. Do NOT leave corrections
   only in chat history.

3. **If a significant decision was made informally** (in chat, in
   review), propose creating an ADR via `/decision:new` before closing.

4. **Stage all `docs/` changes in the SAME commit/PR** as the session's
   code changes.

Do NOT close the session without completing step 1.

Output a one-paragraph session summary suitable for pasting into the
PR description.
