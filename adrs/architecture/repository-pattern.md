<!-- Shareable ADR. Token budget: ~500. -->

# ADR-`<NNN>`: Repository Pattern for Data Access

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Your project has multiple data sources (DB, external API, cache) and
  the domain layer should not know about them.
- You want to unit-test domain logic without spinning up a database.
- You expect to swap or add a persistence backend later.

Do NOT adopt this if your project is a thin CRUD wrapper around a single
data source and has no domain logic worth isolating — the indirection is
overhead.

## Context

AI agents often default to inlining `db.query(...)` or ORM calls into
route handlers and service methods. This makes domain logic untestable in
isolation and couples future agent suggestions to whichever ORM happens
to be imported. Without an ADR, the agent rederives the wrong pattern
every session.

## Decision

All persistence access goes through repository interfaces defined in the
domain layer:

- Domain layer declares the interface:
  `interface UserRepository { findById(id): User|null; save(u: User): void }`.
- Data layer implements it:
  `class PostgresUserRepository implements UserRepository`.
- Services / use-cases depend on the interface, never on the concrete
  class.

File conventions (adapt to your stack):

- Interfaces: `src/<feature>/domain/<entity>-repository.<ext>`.
- Implementations: `src/<feature>/data/<impl>-<entity>-repository.<ext>`.
- Wiring (dependency injection) lives in a single composition root, not
  scattered.

## Alternatives Considered

1. **Active Record (model classes that save themselves).** Faster to
   write; couples domain to ORM and makes domain non-portable.
2. **Direct ORM access in services.** Simplest; every test needs a real
   DB or a heavy ORM mock, and the mock often diverges from real
   behavior.
3. **Generic `Repository<T>`.** Rejected: forces uniform CRUD shape on
   every entity, fits ~30% of real entities, forces escapes for the
   rest.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `grep -r "db\.query\|orm\." src/<feature>/domain/` returns 0 results.
- Every test under `src/<feature>/domain/` runs without a database
  connection.
- Every concrete `*Repository` class implements an interface declared in
  the domain layer of the same feature.

## Trade-offs

- Adds indirection. Worth it once you have ≥3 features with non-trivial
  logic.
- Requires a dependency-injection mechanism (constructor injection,
  container, or factory).
