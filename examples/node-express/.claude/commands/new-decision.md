<!-- Slash command: /decision:new
     Token budget: ~1,000–2,500 for the whole flow. -->

Guide the user through documenting a new architectural decision.

1. Ask: "What decision needs to be made?"

2. Help articulate the **Context**: what problem are we solving, what
   constraints apply, what is the trigger for deciding now.

3. Propose **2–3 alternatives** with explicit pros and cons. Do not
   short-circuit to your favorite — the user has to choose.

4. Once chosen, generate a new ADR at
   `docs/decisions/<NNN>-<slug>.md`. Increment `<NNN>` to one above
   the highest existing.

5. Update `docs/decisions/_index.md` with the new entry.

Constraints:

- The ADR MUST be ≤100 lines.
- If the decision affects a recurring convention, ALSO update
  `docs/CONVENTIONS.md` and reference the new ADR there.
- Do NOT skip "Alternatives Considered".
- Status starts as `Accepted` unless the user explicitly asks for
  `Proposed`.

When the ADR file is written, stop. The user reviews it before the
implementation begins.
