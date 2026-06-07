<!-- Slash command: /issue:start <issue-number>
     Pick up a tracker issue as the focus of THIS session.
     Token budget: ~2,000–4,000.

     OFFLINE EXAMPLE: in a real project the issue body comes from
     `gh issue view <n>`. Here you can paste the body directly when
     practicing the workflow. -->

The user passes an issue number. If they don't, ask which.

1. **Fetch the issue body.** In a real project:

   ```bash
   gh issue view <n>
   ```

   In this example: ask the user to paste the issue body.

2. **Parse the 6 fixed sections** (per the parent catalog ADR
   `adrs/process/work-units-as-external-tracker.md`):
   `Context`, `Target`, `ADRs to load`, `Acceptance criteria`,
   `Reproduction` (fixes only), `Estimated sessions`.

   If any required section is missing, STOP and tell the user the
   issue is malformed. Propose editing it before starting.

3. **For each ADR listed in `ADRs to load`**, read the referenced file
   in `docs/decisions/`. These set the constraints the implementation
   must satisfy.

4. **Read the file in `Pattern to mirror` ONCE for shape.** Skim, do
   not study.

5. **Do NOT read the files listed in `Target` yet** — they are where
   the work *goes*, not where context comes *from*.

6. **Summarize for the user**, exactly:
   - **Objective** (one line, from `Context`).
   - **Acceptance checklist** (verbatim — this is the DoD).
   - **ADRs loaded** and what each constrains.
   - **Target paths** (where the work goes).
   - **Pattern to mirror**.

7. Ask: **"Ready to start?"**

If `Estimated sessions` > 1, remind the user the issue should have been
decomposed before starting. Offer `/issue:new` to split it.

**Token discipline:** do NOT scan target files or unrelated code at
this step. The issue + ADRs are the spec.
