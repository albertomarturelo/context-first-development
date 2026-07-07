---
description: "Audit CFD context integrity — CLAUDE.md size/shape, status freshness, ADR index sync and completeness, conventions, language, token annotations — and report PASS/WARN/FAIL with proposed fixes."
token-budget: "~2,000–5,000"
---

Validate the CFD context in this project. Check, in order, and output a
checklist with PASS / WARN / FAIL per item:

1. **`CLAUDE.md` size**: WARN if >150 lines, FAIL if >300.
2. **`CLAUDE.md` content shape**: should be an index of markdown
   LINKS to `docs/*.md`, not paragraphs of prose. FAIL if any section
   has >10 lines of inlined content where a link would do. WARN on
   `@docs/...` references — in Claude Code those are EAGER imports
   that load the whole file every session, defeating the index; use
   plain links plus `/session:start` for orientation reads.
3. **`docs/CURRENT_STATUS.md` freshness**: run
   `git log -1 --format=%ar -- docs/CURRENT_STATUS.md`. WARN if older
   than 2 working days; FAIL if older than 1 week.
4. **ADR index integrity**: every file matching
   `docs/decisions/[0-9]*.md` must be listed in
   `docs/decisions/_index.md`, and every row in `_index.md` must point to
   a file that exists. FAIL on mismatch.
5. **ADR completeness**: every ADR has Status, Context, Decision,
   Alternatives, Consequences sections. FAIL on any ADR missing one.
6. **Convention coverage**: spot-check 3 random source files. Do their
   patterns match `docs/CONVENTIONS.md`? If not, propose updates to
   CONVENTIONS.md (do not auto-apply).
7. **Language check**: any `docs/**/*.md` file written in a non-English
   language? WARN per file.
8. **Token budget annotations**: any template file or shareable ADR
   missing the top-of-file token-cost comment? WARN per file.

Output the checklist and propose concrete fixes for any failures.
Do NOT auto-apply fixes — the user reviews first.
