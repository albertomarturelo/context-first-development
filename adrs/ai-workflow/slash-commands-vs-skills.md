<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Slash Commands vs Claude Skills — Both Are Valid

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your team is encoding CFD's automation procedures
  (`session:start`, `session:close`, `decision:new`, `issue:new`,
  `issue:start`, `context:validate`, etc.).
- You've seen examples or case studies using both styles and want a
  clear answer on which fits which procedure.
- You're on Claude Code (where both primitives are available) or on
  any agent that supports one of them.

Skip if your agent supports neither (rare today — most major coding
agents implement slash commands at minimum).

## Context

CFD's automation procedures need to be invoked somehow. Two primitives
dominate today:

- **Slash commands** (`.claude/commands/<name>.md`). User types
  `/<name>`. Explicit, deterministic, portable across most coding
  agents (Claude Code, Aider, several others).
- **Claude Skills** (`.claude/skills/<name>/SKILL.md`). The model
  discovers and invokes based on context. Lower typing friction,
  Claude-Code-specific today.

Both achieve the same outcome (automation of context maintenance).
Picking one without thinking through the trade-offs leads to "we
should use the other" debates that don't actually serve the
methodology.

## Decision

**Both are valid.** Pick per procedure on three axes:

1. **Determinism.** If forgetting the procedure breaks the
   methodology (`/session:start`, `/session:close` qualify), prefer
   **slash commands** — explicit user choice, no model judgement.
2. **Discoverability.** If the procedure should fire on context
   signals the user might miss (`/decision:new` after the user says
   "let's just use Redis"), **Skills** earn their keep — the model
   notices and prompts.
3. **Portability.** If the team uses non-Claude agents alongside
   Claude Code, **slash commands** win — they translate.

A defensible default mix:

| Procedure          | Recommended       | Reason                                       |
| ------------------ | ----------------- | -------------------------------------------- |
| `session:start`    | slash command     | Mandatory at session boundary                |
| `session:close`    | slash command     | Mandatory at session boundary                |
| `decision:new`     | either            | Skills shine — model catches the signal      |
| `issue:new`        | slash command     | Explicit creation moment                     |
| `issue:start <n>`  | slash command     | Explicit pickup moment                       |
| `context:validate` | either            | Periodic, low-stakes                         |

All-Skills or all-slash-commands setups also work. The point is to
**choose intentionally**, document the choice in
`docs/CONVENTIONS.md`, and stick with it.

## Alternatives Considered

1. **Slash commands only.** Loses Claude Skills adopters; closes off
   the model-discovered ergonomic for procedures where it shines.
2. **Skills only.** Locks you to Claude Code; breaks multi-agent
   workflows when a new agent enters the toolbox.
3. **Both with no guidance.** Forces every team to rediscover the
   axes. This ADR exists to prevent that.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- The repo's `.claude/commands/` and/or `.claude/skills/` contains
  procedures matching the methodology's named ones (start, close,
  new-decision, etc.).
- Mandatory-at-boundary procedures (`session:start`, `session:close`)
  exist as slash commands UNLESS the team has explicitly justified
  Skills with a per-project addendum ADR.
- `docs/CONVENTIONS.md` documents which primitive owns which
  procedure — no half-implemented duplicates.

## Trade-offs

- Mixing primitives costs documentation overhead (CONVENTIONS lists
  which is which). Worth it when per-procedure fit matters.
- Skills-only setups stop translating when the team adds a
  non-Claude agent. Migration is mechanical but real.
