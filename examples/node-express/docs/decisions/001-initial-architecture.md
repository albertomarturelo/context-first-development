# ADR-001: Initial Architecture — Layered with Express + Postgres

## Status
Accepted — 2026-06-07

## Context

This service exposes a tiny REST API for creating and listing user
notifications. It exists as a runnable CFD example, so the architecture
should be the smallest viable shape that:

- Exercises the catalog's shareable ADRs (repository pattern,
  integration over mocks, trunk-based + RC).
- Remains realistic enough to read as production-shaped code, not a
  toy.
- Scales to a second module without restructuring.

## Decision

Three-layer architecture, dependency direction inward toward `domain/`:

```
src/notifications/
  domain/        # entities, use cases, repository interfaces
  presentation/  # Express routes + zod input validation
  data/          # repository implementations + DB clients
```

Concrete files (initial pass):

- `domain/notification.ts` — `Notification` entity + `NewNotification`
  input type + `Channel` union.
- `domain/notification-repository.ts` — `NotificationRepository`
  interface.
- `domain/send-notification.ts` — `SendNotification` use case.
- `presentation/notification-routes.ts` — Express router with `POST`
  and `GET` handlers.
- `data/postgres-notification-repository.ts` — concrete `pg` impl.

Wiring lives in `src/app.ts` (the composition root). `src/server.ts`
holds the process bootstrap (`Pool` construction, `listen`). No DI
container.

## Alternatives Considered

1. **Feature-flat (no layers).** Faster for 2 endpoints; defeats the
   point of an example demonstrating layered architecture.
2. **Hexagonal with explicit ports/adapters terminology.** Equivalent
   intent; layered is the lower-jargon choice and matches the catalog
   ADR.
3. **Single-file Express app.** Tempting for an example, but does not
   demonstrate any of the catalog ADRs — defeats the educational goal.

## Consequences

- Domain folder is testable without I/O.
- Adding a second persistence backend (e.g., Redis cache,
  vendor email gateway) is local to `data/`.
- Newcomers (human or AI) read this ADR + ADR-002 before writing
  routes.
- The `src/app.ts` composition root is the only file that knows about
  concrete implementations.
