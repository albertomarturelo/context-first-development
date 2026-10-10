<!-- Shareable ADR. Token budget: ~725. -->

# Distribute CFD Skills Through Installers, Never as the Source of Truth

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your team has encoded CFD's procedures as Agent Skills (see
  [agent-skills-as-procedures](agent-skills-as-procedures.md)) and
  wants them installed in one step instead of copied by hand.
- You maintain those skills in a shared repo and want a single source
  of truth that also ships through installers.

Skip if every consumer already vendors the skill folders directly.

## Context

Copying skill folders into every project is friction, and copies drift
from the source. Two installers remove the friction:

- **The `skills` CLI** (`npx skills add <owner/repo>`) installs from a
  git repo into every detected agent: a universal copy in
  `.agents/skills/` for Codex and Copilot, symlinks for Claude Code.
- **A Claude Code plugin** (`/plugin install`) keeps the skills updated
  from a marketplace, namespaced as `/<plugin>:<skill>`.

The failure mode this ADR prevents: treating an installer's manifest as
the canonical artifact, which quietly locks a model-agnostic
methodology to one tool.

## Decision

**Installers are additional distribution channels, never the source of
truth.** Concretely:

1. The skill folders in the repo remain canonical. The plugin manifest
   **points at them** (`"skills": ["./path"]`); it does NOT duplicate
   them. The `skills` CLI reads the same folders.
2. No installer carries procedure logic. All behavior stays in
   `SKILL.md`, which any agent can read.
3. Install at **project scope** and commit the result, so every clone
   and every worktree runs the same procedure version. A global install
   is personal and unversioned.
4. **One channel per project.** Installing the plugin on top of copied
   skills yields `/cfd:session-start` *and* `/session-start`: the same
   procedure from two places.

## Alternatives Considered

1. **No installer, copy files only.** Zero lock-in, but distribution
   stays manual. Kept as a valid path, not the only one.
2. **A CFD-specific installer.** Would maintain a per-agent path table
   forever; the `skills` CLI already does it for 40+ agents.
3. **Installer as canonical, folders generated from it.** Inverts the
   dependency and couples the methodology to one tool. Rejected.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- The plugin manifest references the existing skills directory; no
  `SKILL.md` is duplicated (`diff` finds no second copy).
- Removing every manifest still leaves working, copyable skills.
- Adopting projects commit `.agents/skills/`; it is not gitignored.

## Trade-offs

- The plugin serves Claude Code only; the `skills` CLI covers the rest.
  Two channels to document, one source to maintain.
- Project-scope installs add files to every adopting repo. That is the
  point: the procedures version with the code they govern.
