<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Distribute CFD Commands as an Optional Plugin

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your team has encoded CFD's procedures as slash commands and wants
  teammates to install them in one step instead of copying files.
- You maintain those commands in a shared repo and want a single source
  of truth that also ships as an installable package.
- Your agent supports a plugin/marketplace mechanism (Claude Code does).

Skip if every consumer already vendors the command files directly, or
your agent has no plugin system — the portable markdown is enough on its
own.

## Context

CFD's automation lives in portable command markdown
(`.claude/commands/*.md`, see
`ai-workflow/slash-commands-vs-skills.md`). Copying those files into
every project is friction, and copies drift from the source. Claude Code
plugins solve distribution — `/plugin install` pulls the commands from a
marketplace — but a plugin manifest is Claude-Code-specific. The failure
mode this ADR prevents: treating the plugin as the canonical artifact,
which would quietly lock a model-agnostic methodology to one agent.

## Decision

**Ship the plugin as an ADDITIONAL distribution channel, never as the
source of truth.** Concretely:

1. The portable command markdown remains canonical. The plugin manifest
   **points at those existing files** (`"commands": ["./path"]`) — it
   does NOT duplicate them.
2. The manifest carries no procedure logic. All behavior stays in the
   markdown body, which any agent can read.
3. Encode the methodology's determinism choice in frontmatter:
   mandatory-boundary procedures (`session-start`, `session-close`,
   issue pickup, project bootstrap) set `disable-model-invocation: true`
   so only explicit user invocation fires them; discovery-friendly ones
   (`decision:new`, `context:validate`) allow model invocation.
4. Document that the plugin is optional. A team on a non-Claude agent
   copies the same markdown by hand and loses nothing but the installer.

## Alternatives Considered

1. **No plugin, copy files only.** Zero lock-in, but distribution stays
   manual and copies drift. Rejected as the sole option — a one-command
   install is worth offering.
2. **Plugin as canonical, markdown generated from it.** Inverts the
   dependency and couples the methodology to one agent's manifest
   format. Rejected — violates model-agnosticism.
3. **Duplicate commands into a `commands/` dir inside the plugin.** Two
   copies to keep in sync. Rejected — the manifest can reference the
   originals.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- The plugin manifest references the existing command directory; no
  command markdown is duplicated (`diff` finds no second copy).
- Every command file is a plain-prose procedure readable without the
  manifest — removing the manifest still leaves working, copyable
  commands.
- Mandatory-boundary commands set `disable-model-invocation: true`;
  discovery-friendly ones do not.

## Trade-offs

- The plugin only serves Claude-Code users; other agents still copy
  files. Accepted — the markdown covers them.
- Frontmatter adds a small per-file surface most agents ignore. Cheap
  next to the install ergonomics it buys.
