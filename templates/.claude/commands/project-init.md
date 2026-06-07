<!-- Slash command: /project:init
     One-time bootstrap of CFD in an existing project.
     Token budget: <10,000 total. Hard cap. -->

Implement Context-First Development (CFD) in this project. Do NOT read
individual source files. Instead, analyze ONLY:

- The root directory structure (`ls`, `tree -L 2`).
- Dependency files: `package.json`, `pyproject.toml`, `Cargo.toml`,
  `go.mod`, `Gemfile`, etc.
- The README, if any.

Then create these files using the templates from this CFD repo as a base:

1. `docs/ARCHITECTURE.md` — inferred from directory structure and
   dependencies. Mark each inference as "(inferred — confirm)".
2. `docs/STACK.md` — list all detected technologies with their versions
   pulled from dependency files.
3. `docs/CONVENTIONS.md` — infer 5–10 likely conventions from directory
   layout and dependency choices. Mark each as "(inferred — confirm)".
4. `docs/CURRENT_STATUS.md` — initialize with:
   "Project initialized with CFD on `<today>`. No work in progress yet."
5. `docs/decisions/_index.md` — empty index header only.
6. `docs/decisions/001-initial-architecture.md` — document the current
   architecture as the first ADR. Status: `Accepted`. Reference
   `docs/ARCHITECTURE.md` in the Decision section.
7. `CLAUDE.md` — fill in the template, referencing the docs created
   above. Project name and 2–3 sentence description pulled from the
   README; if no README, ask the user.

Stop after these files are written. Output a summary listing what was
created and ask the user to review the inferred conventions and ADR-001
before continuing.

Hard rule: if you find yourself reading source code to "figure out the
architecture", stop. The directory layout and dependency files are
sufficient for a first pass. Refinement comes from `/decision:new`
conversations as real work surfaces it.
