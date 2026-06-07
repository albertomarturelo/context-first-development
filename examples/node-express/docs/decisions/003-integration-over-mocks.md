<!-- Adapted from the parent CFD catalog:
     adrs/testing/integration-over-mocks.md -->

# ADR-003: Integration Tests Over Mocks for the Data Layer

## Status
Accepted — 2026-06-07

## Context

The `PostgresNotificationRepository` contains SQL strings the agent
could easily get wrong (column names, NULL handling, `ORDER BY`,
`CHECK` constraints on `channel`). A mocked `pg.Pool` would pass any
SQL — including SQL that fails in production. The repository pattern
(ADR-002) gives us the seam to test the real behavior cheaply.

## Decision

- Tests under `src/**/data/` run against a real Postgres instance
  defined in `docker-compose.test.yml` (port 5433, db `cfd_test`).
- Tests under `src/**/domain/` use a hand-written class
  `InMemoryNotificationRepository` that implements the same interface
  — NOT `vi.mock(...)` on the repository.
- Tests under `src/**/presentation/` (when added) may mock the use
  case; they verify wiring and serialization, not business logic.

CI / local setup:

- `npm run test:db:up` starts the DB (waits for healthcheck).
- `npm run migrate:test` applies `migrations/001-create-notifications.sql`.
- `npm test` runs unit then integration.
- `vitest.config.ts` sets `fileParallelism: false` because the
  integration suite shares one database and the per-test
  `TRUNCATE` would race.

## Alternatives Considered

1. **Mock `pg.Pool`.** Cheaper to write, decoupled from the real
   schema, rots silently against migrations.
2. **One Testcontainer per test.** Hygienic but slow; one shared
   container per run is the sweet spot for an example.
3. **End-to-end only.** Slow, flaky, hard to attribute failures.

## Consequences

- `grep -E "vi\.mock\(.*pg|new Mock\(\)" src/**/data/*.test.ts`
  returns 0 results.
- Failed migrations fail the test suite — the schema is part of the
  contract.
- Test runtime ~5–10s longer than mocked equivalents. Acceptable.
