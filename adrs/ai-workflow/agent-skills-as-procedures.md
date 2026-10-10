<!-- Shareable ADR. Token budget: ~875. -->

# CFD Procedures Ship as Agent Skills, One Copy for Every Agent

## Status

`Accepted` — `<YYYY-MM-DD>`. Supersedes
[slash-commands-vs-skills](slash-commands-vs-skills.md).

## When to Use

Adopt this ADR when:

- More than one coding agent touches the repo (Claude Code, Codex,
  GitHub Copilot, Gemini CLI), or parallel loops run different agents.
- You want procedures (`session-start`, `session-close`, …) installable
  in one command and identical in every worktree.

## Context

Slash commands looked portable when Skills were Claude-only. That
inverted: [Agent Skills](https://agentskills.io/specification) became
an open standard in December 2025 (a folder with `SKILL.md`, `name` +
`description` frontmatter), adopted by Claude Code, Codex, Copilot,
Gemini CLI and Cursor. Command formats are the part that still differs
per agent (Copilot prompt files, Gemini TOML). Claude Code merged
commands into skills: both create `/name`.

Discovery paths differ: Codex, Copilot and Gemini CLI read
`.agents/skills/`; Claude Code reads `.claude/skills/`.

## Decision

- **Canonical location:** `.agents/skills/<name>/SKILL.md`.
  `.claude/skills` is a symlink to it. Never a copy; a copy drifts.
- **Mandatory-boundary procedures stay deterministic.** `session-start`,
  `session-close`, `issue-new`, `issue-start` and `project-init` set
  `disable-model-invocation: true` (Claude Code, Copilot) and ship
  `agents/openai.yaml` with `policy.allow_implicit_invocation: false`
  (Codex). They run only when the user invokes them: `/name` in Claude
  Code and Copilot, `$name` in Codex.
- **Discovery-friendly procedures** (`new-decision`, `review-pr`,
  `validate-context`) allow model invocation; the description says when.
- **Token budget** lives in `metadata.token-budget`, the spec's
  extension map.
- **Install:** copy the templates, or
  `npx skills add <repo>` to install into every detected agent.

## Alternatives Considered

1. **Keep slash commands canonical.** No common command format exists
   across agents; every non-Claude adopter re-translates by hand.
2. **Canonical `.claude/skills`, symlink `.agents/skills`.** Works, but
   three of four target agents read `.agents/`; the neutral path is the
   one to keep if Claude Code adds it. The `skills` CLI lays out the
   same way.
3. **Strict spec only (drop `disable-model-invocation`).** Passes the
   reference validator, but rituals would fire on model judgement in
   Claude Code and Copilot, re-opening the "forgotten ritual" gap.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `.agents/skills/*/SKILL.md` exists, `name` matches its folder, and
  `.claude/skills` is a symlink (`test -L .claude/skills`).
- No `.claude/commands/` directory duplicates a skill.
- Every manual-only skill has both `disable-model-invocation: true` and
  `agents/openai.yaml` with `allow_implicit_invocation: false`.

## Trade-offs

- The strict reference validator (`agentskills validate`) rejects
  `disable-model-invocation` and `argument-hint`, which Claude Code and
  Copilot document. Validate with a check that allows those two.
- Gemini CLI has no manual-only flag; it asks for consent before each
  activation. Hooks and CI remain the enforcement layer
  ([enforce-rituals-with-hooks](enforce-rituals-with-hooks.md)).
- Copilot reads both `.agents/skills` and `.claude/skills`; through the
  symlink it may list a skill twice. Unverified; cosmetic if it does.
