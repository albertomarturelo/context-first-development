# Case Study: sii

**Repository:** <https://github.com/albertomarturelo/sii>
**Author:** Alberto Marturelo
**Stack:** TypeScript (strict), Node, pnpm workspaces, vitest, zod
**License:** MIT
**Distribution:** public npm — `@albertomarturelo/sii-core` + CLI + MCP surfaces

> `sii` is **referenced**, not mirrored. The canonical source lives at
> its own repo above. This page captures what CFD adoption looks like
> in that codebase as of 2026-07-07.

## What it is

A TypeScript monorepo that automates routine interactions with Chile's
tax authority (SII — Servicio de Impuestos Internos). One shared domain
core backs two surfaces: a human **CLI** and an **MCP server** that
plugs into Claude Code and Claude Desktop. The core holds every legal
and operational guardrail (throttling, audit log, secrets posture), so
the rails apply regardless of which surface is in front. ~130
TypeScript source files across three packages (`core`, `cli`, `mcp`).

## Why this case study matters

`sii` was **born with CFD on day 0**: ADR-001, dated the same day the
repo was created (2026-06-27), is *"Adopt Context-First Development
(CFD) for this repo."* Every signal below is clickable:

- **`CLAUDE.md` is an index** (~3.9 KB) with a dense "Critical Rules"
  section in which almost every rule cites the ADR that backs it
  (`(ADR-003)`, `(ADR-006)`, …) — rules and rationale stay linked.
- **21 ADRs in the first week** (48 commits, 2026-06-27 → 2026-07-04),
  indexed in `_index.md`. Decision velocity tracks work velocity — the
  ADR habit survived real deadline pressure instead of decaying.
- **`docs/CURRENT_STATUS.md` is `.gitignore`d** with the comment
  "status is managed locally, not versioned" — the posture the catalog
  now recommends via
  [`current-status-per-developer`](../adrs/process/current-status-per-developer.md).
- **Cross-repo decision lineage.** `sii` is a ground-up rewrite of a
  Python predecessor; where a rule is ported, the ADR cites the
  predecessor's ADR ("ported from sii-py ADR-016"). Context survives
  even a full stack rewrite.
- **7 slash commands** under `.claude/commands/` matching the CFD
  template set: `session-start`, `session-close`, `new-decision`,
  `issue-new`, `issue-start`, `review-pr`, `validate-context`.

## Measurable claim

Using the `bytes/4 ≈ tokens` method from
[`scripts/measure-session-cost.sh`](../scripts/measure-session-cost.sh)
on the repo tree (2026-07-07):

- Orientation surface (`CLAUDE.md` + `docs/decisions/_index.md`;
  `CURRENT_STATUS.md` is local): **≈ 1.8k tokens**.
- Reading every scannable file (204 files, lockfile excluded):
  **≈ 234k tokens**.
- Ratio: **≈ 130× — an upper bound**, since a real agent explores
  selectively. The durable claim is the adherence surface: 21 ADRs and
  a rule-to-ADR citation graph that selective exploration of source
  code could never recover.

## The deferred-gate moment

The publishing chain shows decisions constraining *future* decisions:

1. **ADR-004** (day 0) ports the ToS/guardrail posture and explicitly
   flags: *"a future public release will need its own ADR."*
2. **ADR-015** (day 3) publishes the core privately and states that
   the public-release gate "does not apply" — the deferral is cited,
   not forgotten.
3. **ADR-018** (day 5) pays the gate: public release under MIT, then
   ADR-019/021 take the packages to public npm.

A pre-registered decision gate held across a week of fast solo work
because it lived in the decision log, not in memory. This is CFD
Principle 4 doing its job.

## CFD adoption checklist

| CFD element                | Adopted? | Notes                                                                   |
| -------------------------- | :------: | ----------------------------------------------------------------------- |
| `CLAUDE.md` as index       |    ✓     | Critical Rules cite backing ADRs by number                              |
| `docs/ARCHITECTURE.md`     |    ✓     | Plus `STACK.md`, `CONVENTIONS.md`, `ROADMAP.md`                         |
| `docs/decisions/_index.md` |    ✓     | 21 ADRs, table-indexed, dated                                           |
| `docs/CURRENT_STATUS.md`   |    ✓     | Local-only (`.gitignore`d) — now the catalog's recommended posture       |
| Slash commands             |    ✓     | Full CFD template set under `.claude/commands/`                         |
| English-only model context |    ✓     | All docs and ADRs in English                                            |
| ADR-before-implementing    |    ✓     | Codified as a Critical Rule; the ADR-004→015→018 gate is the proof      |
| Document corrections       |    ✓     | Critical Rule: "Corrections become conventions"                         |

## Variation worth noting

`sii`'s `CLAUDE.md` links its docs via `@references`. The catalog's
template now uses plain markdown links instead, because in Claude Code
`@path` is an eager import that loads every referenced doc each
session. `sii` predates that guidance; its docs are small enough that
the eager load stays cheap, but new adopters should start from the
current template.

## How to read this case study

1. Open [`docs/decisions/_index.md`](https://github.com/albertomarturelo/sii/blob/main/docs/decisions/_index.md).
   Read ADR-001 (the CFD adoption decision), then ADR-004 → 015 → 018
   for the deferred-gate chain.
2. Open [`CLAUDE.md`](https://github.com/albertomarturelo/sii/blob/main/CLAUDE.md).
   Notice the Critical Rules → ADR citation pattern.
3. Check `.gitignore` for the local-only `CURRENT_STATUS.md` posture.
4. Skim `.claude/commands/` and compare against
   [`templates/.claude/commands/`](../templates/.claude/commands/).

## Attribution

- Methodology author and `sii` author: Alberto Marturelo.
- Referenced with the author's permission. `sii` is MIT-licensed at
  the upstream repository; this prose page is CC-BY-SA 4.0 per the
  publication repo's prose license.

---

*Snapshot of the upstream repo as of 2026-07-07. `sii` evolves
independently — click the repo link above for the current state.*
