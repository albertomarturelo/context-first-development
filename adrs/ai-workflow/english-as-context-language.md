<!-- Shareable ADR. Token budget: ~350. -->

# ADR-`<NNN>`: English as the Context Language

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- The project uses an AI coding agent (Claude, GPT, Gemini, etc.).
- The team's working language is not English.

Skip if the team is entirely English-native — there is no choice to
make.

## Context

LLM tokenizers (Anthropic's, OpenAI's, Google's) are optimized for
English. The same information in Spanish, French, Portuguese, or
Japanese can consume **20–40% more tokens**. In a `CLAUDE.md` or
`ARCHITECTURE.md` that is loaded every session, the overhead compounds.

This is not about elitism. It is about cost and reliability — non-English
context also exhibits higher hallucination rates on several public
benchmarks.

## Decision

All technical context written for the agent is in English:

- `CLAUDE.md` / `AGENTS.md`
- `docs/**/*.md` (ARCHITECTURE, STACK, CONVENTIONS, CURRENT_STATUS,
  decisions)
- `.claude/commands/**/*.md`
- ADRs
- Code comments meant for the agent

Team communication (PR descriptions, issue comments, Slack/Teams) can
be in the team's native language — those are not loaded into the
agent's context on every session.

## Alternatives Considered

1. **Write context in the team's language.** Honest about team
   composition; costs 20–40% more tokens per session forever.
2. **Auto-translate on session start.** Adds a build step; translation
   drift becomes a context-integrity problem.
3. **Write in both languages.** Doubles the maintenance surface and
   guarantees the two will drift.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- A `lang-detect` check on `docs/**/*.md` and `CLAUDE.md` returns
  English with high confidence.
- Token counts for `CLAUDE.md` + first-level `@references` stay within
  the per-session budget the team set.

## Trade-offs

- Non-English-native team members write context in a non-native
  language. Worth it; the patterns are simple, repeat, and the agent
  itself can translate user prompts.
