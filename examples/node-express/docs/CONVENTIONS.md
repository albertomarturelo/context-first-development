<!-- Loaded on demand. -->

# Conventions

## Code Style
- TypeScript `strict: true`.
- Named exports only — no default exports.
- Public method return types are explicitly `Promise<T>` when async.
- Module imports use the `.js` suffix (NodeNext resolution).

## Patterns
- Repository pattern for ALL data access (ADR-002).
- Dependency injection via constructor; composition in `src/app.ts`.
- No module-level singletons.

## Testing
- Domain tests use an in-memory fake class (e.g.,
  `InMemoryNotificationRepository`) — NOT `vi.mock(...)` on the
  repository interface (ADR-003).
- Data-layer tests run against the real Postgres in
  `docker-compose.test.yml`.
- Presentation tests (when added) may mock the use case; they verify
  wiring and serialization, not business logic.
- Test files sit next to source as `*.test.ts`.

## Naming
- Files: kebab-case (`notification-repository.ts`).
- Classes: PascalCase. Functions and methods: camelCase.
- Test classes for in-memory fakes: prefix `InMemory` (e.g.,
  `InMemoryNotificationRepository`).

## Commits & PRs
- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
- One issue per PR; PR title matches the squash commit message.
- All branches target `main` (ADR-004).

## Tracker conventions

For `/issue:new`:

- Issue body template: see
  [`adrs/process/work-units-as-external-tracker.md`](../../../adrs/process/work-units-as-external-tracker.md)
  in the parent CFD repo.
- `project_board_add`: not configured — this is an offline example.
  In a real project, add a snippet here like:

  ```bash
  project_board_add() {
    gh project item-add <PROJECT_NUM> --owner <OWNER> --url "$1"
  }
  ```

  and `/issue:new` will pick it up automatically.
