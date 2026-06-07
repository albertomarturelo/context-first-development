# Contributing

CFD is open to contributions. The most valuable kinds, in order:

1. **New ADRs for the shareable catalog** (`adrs/`).
2. **Runnable examples** showing CFD applied to a specific stack
   (`examples/`).
3. **Case studies** documenting real adoption (`case-studies/`).
4. **Refinements to templates** (`templates/`).

## Contributing an ADR to the catalog

Every shareable ADR MUST satisfy this contract (the same contract enforced
in `templates/adrs/_TEMPLATE.md`):

- **Atomic.** One decision, one file, ≤100 lines.
- **Technology-neutral when possible.** A repository-pattern ADR is
  reusable across many stacks; a "use Knex.js 3.x" ADR is project-local
  and belongs in your own repo, not the catalog.
- **Has a "When to Use" section** with explicit applicability.
- **Has a "Verifiable Consequences" section** — how does a reader confirm
  this ADR is being followed in their repo? Be concrete (grep, file
  layout, test behavior).
- **English only.**
- **Token budget annotation** at the top, e.g.
  `<!-- Shareable ADR. Token budget: ~500. -->`.

Use [`adrs/_TEMPLATE.md`](adrs/_TEMPLATE.md) as the starting point.

### PR checklist for new ADRs

- [ ] File lives under the right category folder (`architecture/`,
  `testing/`, `process/`, `ai-workflow/`).
- [ ] Indexed in `adrs/_index.md`.
- [ ] ≤100 lines.
- [ ] "When to Use" and "Verifiable Consequences" sections present.
- [ ] Token budget annotation present.
- [ ] No project-specific names (Acme, FooCorp, MyProductService, etc.).

## Contributing an example

A good example is a tiny but complete project (≤30 source files) with CFD
fully applied. An engineer should be able to clone it, run
`/project:status`, and produce correct work in <5 minutes.

Layout:

```
examples/<stack-name>/
  README.md          what the example demonstrates
  CLAUDE.md
  docs/
    ARCHITECTURE.md
    CURRENT_STATUS.md
    decisions/
      _index.md
      001-*.md       at least 3 representative ADRs
  .claude/commands/
  src/               the actual code
```

Open an issue before starting so we can align on scope.

## Contributing a case study

Case studies are first-person accounts of adopting CFD. They require:

- Author identification (LinkedIn or GitHub profile).
- A measurable claim (tokens before/after, time-to-correct,
  re-explanation rate, or comparable signal).
- Explicit publication permission, stated in the PR body.

## What we don't accept

- ADRs for tooling decisions tied to a specific company stack — those go
  in your own repo's `docs/decisions/`, not in this catalog.
- "Awesome list" entries pointing to other CFD-adjacent tools —
  `METHODOLOGY.md` already covers the landscape.
- Translations of the gist — the gist is English by Principle 5.

## Governance

Currently the maintainer is Alberto Marturelo. PR turnaround is
best-effort. ADR contributions are reviewed against the contract above;
substantive disagreement is resolved by opening an issue first.
