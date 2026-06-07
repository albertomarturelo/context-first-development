<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Layered (Clean) Architecture

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- The project will live >12 months.
- Multiple developers, or frequent AI-agent sessions, touch the same
  code.
- Business logic is non-trivial (more than CRUD).

Skip this for scripts, prototypes, and projects with a single concern.

## Context

Without an architectural anchor, AI agents inline business logic into
HTTP handlers, mix persistence with validation, and accumulate
cross-cutting code that becomes impossible to test or move. The agent
will produce a different layout every session because nothing tells it
which one is correct.

## Decision

Three layers, with dependency direction always pointing **inward** toward
the domain:

```
Presentation  →  Domain  ←  Data
(HTTP, CLI,                  (DB, external
 GraphQL)                     services)
```

- **Domain**: pure business logic. No imports from presentation or data.
  Owns entities, use cases, and repository INTERFACES.
- **Presentation**: HTTP routes, CLI commands, GraphQL resolvers. Depends
  on domain. Translates I/O to domain calls.
- **Data**: repository IMPLEMENTATIONS, ORM models, external API clients.
  Depends on domain (to implement its interfaces).

File layout:

```
src/<feature>/
  domain/        # business rules + interfaces
  presentation/  # HTTP / CLI adapters
  data/          # repository impls + external clients
```

## Alternatives Considered

1. **Hexagonal architecture (ports & adapters).** Equivalent intent;
   layered uses less jargon and is more familiar. Pick hexagonal if your
   team already speaks it fluently.
2. **Feature-flat (no layers, just feature folders).** Faster for small
   projects; collapses as features intertwine.
3. **Onion architecture with 5+ layers.** Too granular for most teams;
   extra boundaries don't pay back.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `grep -r "from.*presentation\|import.*presentation" src/<feature>/domain/`
  → 0 results.
- `grep -r "from.*data\|import.*data" src/<feature>/domain/` → 0 results.
- Domain tests run with no I/O setup.

## Trade-offs

- Small upfront cost (the layer split). Pays back within ~10 features.
- Newcomers (human or AI) need to read this ADR to understand the layout.
  That is the point — the layout is no longer implicit.
