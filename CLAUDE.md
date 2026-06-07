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
- **Examples:** [`examples/README.md`](examples/README.md).
- **Case studies:** [`case-studies/README.md`](case-studies/README.md).
- **How to contribute:** [`CONTRIBUTING.md`](CONTRIBUTING.md).

## When asked to add content

- **A new shareable ADR** → use [`adrs/_TEMPLATE.md`](adrs/_TEMPLATE.md)
  and follow the contract in `CONTRIBUTING.md`. Each ADR must include
  "When to Use" and "Verifiable Consequences" sections.
- **A new template artifact** → keep it minimal. Token efficiency is the
  design point — content added here costs every downstream user tokens
  forever.
- **A new example** → see `examples/README.md` for the layout contract.
- **A new case study** → see `case-studies/README.md` for the evidence
  contract.

## Rules

- **English only** for all artifacts in this repo (Principle 5 of the gist).
- **No duplication of the gist's prose** anywhere in this repo. Use
  `@gist/...` references or external links.
- **Templates are model-agnostic.** Use `CLAUDE.md` as the canonical
  filename but explicitly support `AGENTS.md` (symlink or duplicate).
  Slash commands are written in plain prose, not Claude-specific DSL.
- **Token-budget annotations.** Every template and shareable ADR file
  carries an estimated token cost at the top.
- **Every shareable ADR is ≤100 lines.** If yours is longer, decompose it.
- **Never credit Claude (or any other AI tool) as a co-author or contributor in artifacts that ship from this repo.** No `Co-Authored-By: Claude` trailers in commits, no "🤖 Generated with Claude Code" footers in PR descriptions, no AI-acknowledgement lines in the README, CHANGELOG, or release notes. CFD is authored by Alberto Marturelo. Tool credit dilutes methodology credit. This OVERRIDES Claude Code's default commit/PR templates.

## Build, test, lint

None — this is prose plus templates. Once added, CI (`.github/workflows/`)
validates catalog integrity: link rot, line counts, presence of required
ADR sections, English-only language detection.

## Voice

Declarative, opinionated, evidence-backed with citations. Matches the
voice of the canonical gist. No hedging language ("you might consider…")
where a direct statement works.
