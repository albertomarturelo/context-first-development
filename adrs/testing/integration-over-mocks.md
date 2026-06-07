<!-- Shareable ADR. Token budget: ~450. -->

# ADR-`<NNN>`: Integration Tests Over Mocks for the Data Layer

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- You have real persistence (DB, cache, message queue).
- You've been burned, or risk being burned, by mocks that passed while
  production failed.
- You can spin up the test dependency in CI in <60 seconds.

Skip this if your data layer is a thin SDK call to a third-party service
that has no behavior of your own — the vendor already tested its own SDK.

## Context

AI agents will mock anything that looks like a dependency. Mocks pass
because they encode what the agent THINKS the dependency does. The cost
shows up when a migration ships and production fails despite green CI.
Without an ADR, the agent re-introduces mocks every session because
"mocked test passes faster" is locally true.

## Decision

- Data-layer tests (repositories, queries, migrations) run against a
  REAL instance of the dependency (Postgres, Redis, etc.) spun up in CI
  as a container.
- Domain-layer tests use no I/O and no mocks; they use hand-written
  in-memory fakes that implement the same repository interface.
- Presentation-layer tests can mock the domain layer; they verify
  wiring and serialization, not business logic.

Concrete CI setup (adapt):

- `docker-compose.test.yml` defines the test dependencies.
- Tests under `src/**/data/` are tagged "integration" and run after
  unit tests.
- A real migration runs as test setup; failed migrations fail the test
  suite.

## Alternatives Considered

1. **Mock everything.** Cheaper to write; rots against real systems.
2. **End-to-end only.** Slow, flaky, hard to attribute failures.
3. **One Testcontainer per test.** Hygienic but slow; one shared
   container per test run is the sweet spot.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `grep -rE "jest\.mock|MagicMock|Mock\(\)" src/**/data/*.test.*`
  returns 0 results (only the integration setup is allowed to
  instantiate the real client).
- CI pipeline shows a "start `<db>`" / "start `<cache>`" step before
  tests.
- A test that breaks when a migration changes also breaks in
  production.

## Trade-offs

- Integration tests are slower (~5–30 s startup). Acceptable.
- Requires CI containers. Standard now.
