# CLAUDE.md

This file provides guidance to Claude Code (and any other agent that reads
CLAUDE.md / AGENTS.md) when working inside the **Context-First Development
(CFD)** public repository.

## What this repo is

This is NOT a software project. It is a methodology, scaffolding kit, and
shareable ADR catalog. Treat work here as editorial: prose, templates,
ADRs, examples, case studies.

## Index

- **Canonical methodology:** [`METHODOLOGY.md`](METHODOLOGY.md) → links to
  the gist (single source of truth).
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

- **English only** for all artifacts in this repo (Principle 5 of the gist).
- **No duplication of the gist's prose** anywhere in this repo. Use
  `@gist/...` references or external links.
- **Templates are model-agnostic.** Use `CLAUDE.md` as the canonical
  filename but explicitly support `AGENTS.md` (symlink or duplicate).
  Slash commands are written in plain prose, not Claude-specific DSL.
- **Slash commands are the canonical invocation primitive in
  `templates/`, but Claude Skills (`.claude/skills/<name>/SKILL.md`)
  are equally valid for project adopters.** See
  `adrs/ai-workflow/slash-commands-vs-skills.md` for the per-procedure
  guidance. Do NOT ship a parallel `templates/.claude/skills/`
  directory — one canonical template set is enough.
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

Run locally: `bash scripts/validate-catalog.sh`. CI:
`.github/workflows/validate-catalog.yml` (push to `main` + PRs).
Failing checks block merge.

## Voice

Declarative, opinionated, evidence-backed with citations. Matches the
voice of the canonical gist. No hedging language ("you might consider…")
where a direct statement works.
