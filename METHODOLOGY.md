# Methodology

The canonical CFD essay lives in a GitHub gist:

**<https://gist.github.com/7b5c6f91f17b83852724fa73100c8588>**

This file exists to make the gist a navigable artifact from inside this
repo. Reading the gist is the single requirement for understanding CFD;
everything else in this repo (templates, ADRs, examples, case studies) is
downstream of it.

## Quick map of the gist

- **Introduction** — the amnesia problem.
- **Current landscape** — CLAUDE.md, AGENTS.md, Cole Medin, Spotify, ADRs,
  Addy Osmani, the academic papers.
- **The 6 principles** — Context Before Code, SSOT, Hierarchical Context,
  Decisions as First-Class, English, Automation.
- **Knowledge architecture** — the `docs/` + `docs/decisions/` +
  `.claude/commands/` layout.
- **The daily routine** — session start, development, session close.
- **GitHub CLI integration** — issues, PRs, reviews, validation workflows.
- **Anti-patterns** — six explicit failure modes.
- **Scaling** — solo → team → monorepo.
- **Metrics** — tokens/session, time-to-first-correct-action,
  re-explanation rate, status freshness.
- **Complementary tools** — Repomix, `gh` CLI.
- **Case study** — implementing CFD in an existing project.
- **Conclusion** — context is the competitive advantage.
- **References** — 17 cited sources.

## If you only have 5 minutes

Read **The 6 principles** + **The daily routine** sections of the gist,
then come back here and skim the [ADR catalog](adrs/_index.md).

## Why a pointer instead of a copy

Principle 2: **Single Source of Truth**. Duplicating the essay here would
guarantee drift. The gist is the canonical artifact; this repo carries
artifacts that are downstream of it (templates, ADRs, examples, case
studies).
