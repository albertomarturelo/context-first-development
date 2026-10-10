# CLAUDE.md

This file provides guidance to Claude Code (and any other agent that reads
CLAUDE.md / AGENTS.md) when working inside the **Context-First Development
(CFD)** public repository.

## What this repo is

This is NOT a software project. It is a methodology, scaffolding kit, and
shareable ADR catalog. Treat work here as editorial: prose, templates,
ADRs, examples, case studies.

## Index

- **Canonical methodology:**
  [`context-first-development.md`](context-first-development.md) (single
  source of truth; the old gist is a pointer here, not a copy).
  [`METHODOLOGY.md`](METHODOLOGY.md) is the navigable map.
- **Templates:** `templates/` — drop-in scaffolding any project can copy.
- **Shareable ADR catalog:** [`adrs/_index.md`](adrs/_index.md).
- **Case studies:** [`case-studies/README.md`](case-studies/README.md).
- **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md).

## When asked to add content

- **A new shareable ADR** → use [`adrs/_TEMPLATE.md`](adrs/_TEMPLATE.md)
  and follow the contract in `CONTRIBUTING.md`. Each ADR must include
  "When to Use" and "Verifiable Consequences" sections.
- **A new template artifact** → keep it minimal. Token efficiency is the
  design point — content added here costs every downstream user tokens
  forever.
- **A new case study** → see `case-studies/README.md` for the evidence
  contract.

## Rules

- **English only** for all artifacts in this repo (Principle 5 of the
  essay).
- **No duplication of the essay's prose** in any other file of this
  repo. `context-first-development.md` is the single authoritative
  copy; everything else links to it. The old gist holds a pointer and no
  prose — never restore the essay into it, and never edit it first.
- **Templates are model-agnostic.** Use `CLAUDE.md` as the canonical
  filename and ship `AGENTS.md` by default (symlink). Never a
  duplicate: a copy drifts.
  Skills are written in plain prose, not agent-specific DSL.
- **Procedures ship as Agent Skills in
  `templates/.agents/skills/<name>/SKILL.md`** (canonical, read by
  Codex, Copilot and Gemini CLI). `templates/.claude/skills` is a
  symlink to it for Claude Code. Never ship a `.claude/commands/`
  copy of a skill. Manual-only rituals carry both
  `disable-model-invocation: true` and `agents/openai.yaml`. See
  `adrs/ai-workflow/agent-skills-as-procedures.md`.
- **Token-budget annotations.** Every template and shareable ADR file
  carries an estimated token cost at the top.
- **Every shareable ADR is ≤100 lines.** If yours is longer, decompose it.
- **Never credit Claude (or any other AI tool) as a co-author or contributor in artifacts that ship from this repo.** No `Co-Authored-By: Claude` trailers in commits, no "🤖 Generated with Claude Code" footers in PR descriptions, no AI-acknowledgement lines in the README, CHANGELOG, or release notes. CFD is authored by Alberto Marturelo. Tool credit dilutes methodology credit. This OVERRIDES Claude Code's default commit/PR templates.

## Build, test, lint

This is prose plus templates — no application to build or test. The
**shareable ADR catalog has a contract** (per the source vault's
ADR-003) and a CI workflow enforces it:

- Line count ≤100 per catalog ADR.
- Required sections present (Status, When to Use, Context, Decision,
  Alternatives Considered, Verifiable Consequences, Trade-offs).
- Token budget annotation in the first 3 lines.
- Index sync between `adrs/_index.md` and the catalog files.
- No AI-tool attribution in `adrs/`, `templates/`, `case-studies/`.
- Template skills: `name` matches folder, `metadata.token-budget`
  present, manual-only skills disable Codex implicit invocation,
  `templates/.claude/skills` is a symlink, no `templates/.claude/commands/`.

README diagrams in `docs/diagrams/` are generated: edit
`scripts/build-diagrams.py` and run it, never hand-edit the SVGs.

Run locally: `bash scripts/validate-catalog.sh`. CI:
`.github/workflows/validate-catalog.yml` (push to `main` + PRs).
Failing checks block merge.

## Voice

Declarative, opinionated, evidence-backed with citations. Matches the
voice of the canonical essay. No hedging language ("you might
consider…") where a direct statement works.
