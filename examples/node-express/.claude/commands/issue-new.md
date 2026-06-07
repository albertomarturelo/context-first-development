<!-- Slash command: /issue:new
     Create a self-sufficient unit of work in the tracker.
     Token budget for the full flow: ~1,500–3,000.

     This example is OFFLINE — no real `gh issue create`. The command
     still produces the issue body and tells you to paste it into your
     real tracker when adopting CFD for your own project. -->

Guide the user through creating a new tracker issue with the fixed body
template defined in the parent CFD repo at
`adrs/process/work-units-as-external-tracker.md`. Ask, in order, and
confirm each answer before moving on:

1. **Type.** `feature` | `fix` | `chore` | `spike` | `docs`
2. **Title.** Imperative mood, ≤80 chars.
3. **Context.** 2–4 sentences: trigger + user-visible outcome.
4. **Target location.** Concrete file paths or directories. For this
   example: paths under `src/notifications/{domain,data,presentation}/`.
5. **Reference pattern.** An existing file the implementation should
   mirror in shape and naming.
6. **ADRs to load.** ADR numbers in `docs/decisions/`. If a needed
   decision isn't an ADR yet, STOP and run `/decision:new` first.
7. **Acceptance criteria (DoD).** Bulleted markdown `[ ]` items.
   Include: what works at the end, what tests exist, what docs are
   updated.
8. **Reproduction steps.** ONLY for `fix`. Minimal repro.
9. **Estimated sessions.** `1` | `2–3` | `4+`. If >1, propose
   decomposition before continuing.
10. **Milestone.** (Optional in this offline example.)
11. **Extra labels.** Components, blockers.

Then generate the body using the fixed template. Do NOT deviate from
section order:

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
<step 8 OR omit the section entirely if not a fix>

## Estimated sessions
<step 9>
```

In a real (online) project, run:

```bash
gh issue create \
  --title "<step 2>" \
  --body "<body above>" \
  --label "<type>,<step 11>" \
  --milestone "<step 10>"
```

And if `docs/CONVENTIONS.md` defines a `project_board_add` snippet,
run that with the new issue URL.

In THIS offline example, print the body to the chat instead and tell
the user to paste it into their tracker.

English only.
