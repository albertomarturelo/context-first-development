<!-- Loaded at the START of every session. Updated at the END. -->

# Current Project Status

Last updated: 2026-06-07

## In Progress

- [ ] Add `DELETE /notifications/:id` endpoint (#7)
  - `NotificationRepository` needs a `deleteById(id)` method.
  - Blocked by: decision on hard-vs-soft delete (see issue #7 — ADR-005
    pending).

## Recently Completed

- [x] `POST /notifications` + `GET /notifications/:userId` (#3)
- [x] `PostgresNotificationRepository` + integration tests (#4)
- [x] Initial CFD scaffold + ADRs 001-004 (#1)

## Known Issues

- Tests run with `fileParallelism: false` because the data-layer suite
  shares a single Postgres database and the truncation step races under
  parallelism. Cheap fix; haven't needed it.
- No migration runner — `migrations/001-create-notifications.sql` is
  applied manually via `npm run migrate:test`. Acceptable while only
  one migration exists; revisit when a second one lands.

## Next Priorities

1. Resolve `#7` (DELETE endpoint, decision on hard-vs-soft delete).
2. `PUT /notifications/:id` to mark a notification as read (`#8`).
3. Migrate to a proper migration runner (`node-pg-migrate` or
   equivalent).
4. Add a presentation-layer test that hits the routes end-to-end with
   `supertest`.

<!--
Note for the agent: issue numbers above are illustrative. This is an
offline example, not a live GitHub repo. In a real adoption, every
`#N` here resolves via `gh issue view <N>` and `/session:start`
auto-loads the most recent in-progress issue.
-->
