---
description: "Pick up a tracker issue as the focus of this session: fetch it, load its ADRs and one reference file, and state the objective + acceptance checklist. Reads existing target files only if they will be modified."
argument-hint: "[issue-number]"
disable-model-invocation: true
token-budget: "~2,000–4,000 (issue + ADRs + 1 reference file)"
---

The user passes an issue number. If they don't, ask which.

1. **Fetch the issue:**

   ```bash
   gh issue view <n>
   ```

2. **Parse the 6 fixed sections** (per
   `adrs/process/work-units-as-external-tracker.md`):
   `Context`, `Target`, `ADRs to load`, `Acceptance criteria`,
   `Reproduction` (fixes only), `Estimated sessions`.

   If any required section is missing, **STOP** and tell the user the
   issue is malformed. Propose editing it via `gh issue edit <n>`
   before starting. Don't try to infer.

3. **For each ADR listed in `ADRs to load`**, read the referenced file
   in `docs/decisions/`. These set the constraints the implementation
   must satisfy.

4. **Read the file in `Pattern to mirror` ONCE for shape.** Skim, don't
   study. The goal is to know what the produced code should look like.

5. **Target files — two cases:**
   - **Net-new files:** do NOT read anything at `Target` paths.
     Nothing exists there; the pattern file is the spec for shape.
   - **Existing files being modified:** READ each one before
     proposing changes. Editing a file you haven't read produces
     changes that don't fit its current state, and the rework costs
     far more than the read. This is implementation cost, not
     orientation waste.

6. **Summarize for the user**, exactly:
   - **Objective** (one line, from `Context`).
   - **Acceptance checklist** (verbatim from `Acceptance criteria` —
     this is the DoD).
   - **ADRs loaded** and what each constrains.
   - **Target paths** (the files you'll write to).
   - **Pattern to mirror**.

7. Ask: **"Ready to start?"**

If `Estimated sessions` > 1, also remind the user that the issue should
have been decomposed and ask whether to split it now via `/issue:new`.

**Token discipline:** do NOT scan unrelated code or neighboring
modules at this step. The issue body + ADRs are the spec. Reading a
target file you are about to MODIFY is mandatory (step 5) — that is
correctness, not waste. Everything else waits until implementation
surfaces a concrete need.
