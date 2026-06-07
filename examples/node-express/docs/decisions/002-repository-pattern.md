<!-- Adapted from the parent CFD catalog:
     adrs/architecture/repository-pattern.md -->

# ADR-002: Repository Pattern for Data Access

## Status
Accepted — 2026-06-07

## Context

This project will likely grow beyond a single Postgres backend (a Redis
cache for hot reads, possibly a vendor email/SMS gateway accessed as if
it were a "repository"). Without an explicit ADR the agent inlines
`pool.query()` calls into routes — making the domain logic untestable
in isolation and coupling future suggestions to `pg`.

## Decision

All persistence access goes through repository INTERFACES defined in
the domain layer:

- Interface: `src/notifications/domain/notification-repository.ts`
  → `NotificationRepository.save(...)`, `.findByUserId(...)`.
- Implementation: `src/notifications/data/postgres-notification-repository.ts`.
- Use cases (`SendNotification`) depend on the interface, never on the
  concrete class.

Wiring: `src/app.ts` instantiates the concrete repository and passes it
into the use case + routes via constructor / params.

## Alternatives Considered

1. **Direct `pool.query()` in routes.** Simplest now; untestable later.
2. **Active Record (`Notification.save()`).** Couples domain to the
   ORM / driver; harder to swap or fake.
3. **Generic `Repository<T>`.** Forces a CRUD shape that won't fit
   future operations (`markAllAsRead`, `archiveOlderThan`).

## Consequences

- Domain tests use a hand-written in-memory fake
  (`InMemoryNotificationRepository` in the test file).
- Adding a new backend (a read-replica for `findByUserId`, a vendor
  gateway for `send`) is a data-layer change only.
- `grep "pool.query" src/notifications/domain/` returns 0 results.
- `grep "pool.query" src/notifications/presentation/` returns 0
  results.
