# Methodology

The canonical CFD essay lives **in this repo**:

**[`context-first-development.md`](context-first-development.md)**

Reading the essay is the single requirement for understanding CFD;
everything else in this repo (templates, ADRs, examples, case studies)
is downstream of it. A copy is mirrored as a
[GitHub gist](https://gist.github.com/albertomarturelo/7b5c6f91f17b83852724fa73100c8588)
for link stability; when the two differ, the repo wins.

## Quick map of the essay

- **Introduction** — the amnesia problem.
- **Current landscape** — CLAUDE.md, AGENTS.md, Cole Medin, Spotify, ADRs,
  Addy Osmani, the academic papers, memory banks (Cline/Roo),
  spec-driven development (Spec Kit, Kiro), and multi-agent
  orchestration (BMAD) — with how CFD relates to each.
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
- **References** — 22 cited sources.

## If you only have 5 minutes

Read **The 6 principles** + **The daily routine** sections of the
essay, then come back here and:

- Skim the [ADR catalog](adrs/_index.md).
- Look at [**CFD in motion**](docs/session-flow.md) — a daily-loop
  flowchart plus six Mermaid sequence diagrams that graph what a
  session actually does, message by message.

## Why the essay lives in the repo

It didn't always — v1 kept the essay in the gist and this file was a
pointer, on Single Source of Truth grounds. In practice the pointer
inverted the principle: the canonical artifact was the one place that
couldn't take PRs, wasn't versioned with the catalog it governs, and
couldn't be read by an agent inside an adopting repo. An early
adopter (`nemo-cli`, the Python predecessor of the
[sii case study](case-studies/sii.md)) had to vendor the essay
to work around it. SSOT means one authoritative copy — and that copy
belongs where the artifacts downstream of it live and version. The
gist remains as a mirror for inbound links.
