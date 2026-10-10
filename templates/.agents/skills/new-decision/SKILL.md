---
name: new-decision
description: "Guide the user through documenting a new architectural decision as an ADR (≤100 lines) with real alternatives, then update the decisions index. Use when a significant technical decision surfaces without an ADR: a new dependency, pattern, or strategy."
metadata:
  token-budget: "~1,000–2,500 for the whole flow"
---

Guide the user through documenting a new architectural decision.

1. Ask: **"What decision needs to be made?"**

2. Help articulate the **Context**: what problem are we solving, what
   constraints apply, what is the trigger for deciding now.

3. Propose **2–3 alternatives** with explicit pros and cons. Do not
   short-circuit to your favorite — the user has to choose.

4. Once chosen, generate a new ADR file at
   `docs/decisions/YYYY-MM-DD-<slug>.md` (today's date) following
   `docs/decisions/TEMPLATE.md` exactly. The slug is the ADR's
   identity: short, specific, kebab-case. Before writing, check that
   no file in `docs/decisions/` already ends in `-<slug>.md`; if one
   does, pick a different slug or ask whether this supersedes it.
   Never compute a sequence number — parallel branches would collide.
   Existing numbered ADRs (`NNN-*.md`) keep their numbers; do not
   rename them.

5. Update `docs/decisions/_index.md` with the new entry (one row, the
   slug in the ID column).

Constraints:

- The ADR MUST be ≤100 lines.
- If the decision affects a recurring convention, also update
  `docs/CONVENTIONS.md` and reference the new ADR there.
- Do NOT skip "Alternatives Considered". Future sessions need to know
  why the rejected paths were rejected, or they'll re-litigate.
- Status starts as `Accepted` unless the user explicitly asks for
  `Proposed`.

When the ADR file is written, stop. The user reviews it before the
implementation that depends on it begins.
