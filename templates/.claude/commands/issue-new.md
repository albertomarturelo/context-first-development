<!-- Slash command: /issue:new
     Create a self-sufficient unit of work in the tracker.
     Token budget for the full flow: ~1,500–3,000.

     The completeness of this issue determines how cheaply the NEXT
     session starts. Be thorough HERE so you can be cheap THERE. -->

Guide the user through creating a new tracker issue with the fixed body
template defined in
`adrs/process/work-units-as-external-tracker.md`. Ask, in order, and
confirm each answer before moving on:

1. **Type.** `feature` | `fix` | `chore` | `spike` | `docs`
2. **Title.** Imperative mood, ≤80 chars. e.g. "Add notification
   repository interface".
3. **Context.** 2–4 sentences: what is the trigger, what is the
   user-visible outcome.
4. **Target location.** Concrete file paths or directories where the
   work goes. If net-new, name the module + the proposed file path
   ("`src/notifications/domain/notification-repository.ts` — new file").
5. **Reference pattern.** An existing file/module the implementation
   should mirror in shape, naming, and conventions. Skip ONLY if no
   analog exists (rare; flag it explicitly).
6. **ADRs to load.** ADR numbers the agent must read before starting.
   If a needed decision isn't an ADR yet, **STOP and run
   `/decision:new` first** — implementing a decision that's not yet
   written is forbidden by the catalog's "ADR before implementing" ADR.
7. **Acceptance criteria (DoD).** Bulleted markdown `[ ]` items.
   Include all three of:
   - What works at the end of the task (behavior).
   - What tests exist (kind + location).
   - What documentation is updated (CONVENTIONS, ADRs, README).
8. **Reproduction steps.** ONLY for `fix`. Minimal repro the agent can
   run to confirm the bug.
9. **Estimated sessions.** `1` | `2–3` | `4+`. If >1, **propose
   decomposition into sub-issues before continuing.**
10. **Milestone.** Project's milestone or phase.
11. **Extra labels.** Components affected, blockers (hardware-dep,
    backend-dep, pro-only, etc.).

Then generate the body using the fixed template. Do NOT deviate from
section order or names — downstream `/issue:start` parses by section
header:

```markdown
## Context
<step 3>

## Target
- Files / dirs: <step 4>
- Pattern to mirror: <step 5>

## ADRs to load
- [ADR-NNN](docs/decisions/NNN-*.md)

## Acceptance criteria
- [ ] <step 7>
- [ ] <step 7>

## Reproduction (fixes only)
<step 8 — OR omit this section entirely if not a fix>

## Estimated sessions
<step 9>
```

Then run:

```bash
gh issue create \
  --title "<step 2>" \
  --body "<body above>" \
  --label "<type>,<step 11>" \
  --milestone "<step 10>"
```

If `docs/CONVENTIONS.md` defines a `project_board_add` snippet under
"Tracker conventions", also run it with the new issue URL. Otherwise
skip — do NOT invent a board URL or owner name.

Output the issue URL when done. English only.
