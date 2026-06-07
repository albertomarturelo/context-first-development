# Example: Node + Express + Postgres

A tiny but complete CFD-applied service: a notification API with two
endpoints, layered architecture, repository pattern, and integration
tests against a real Postgres instance.

## What this example demonstrates

- **Full CFD scaffolding**: `CLAUDE.md`, `docs/`, `docs/decisions/`,
  `.claude/commands/`.
- **Catalog ADRs adopted**: layered architecture, repository pattern,
  integration over mocks, trunk-based + RC.
- **Work-tracking layer**: `docs/CURRENT_STATUS.md` references issues
  by `#N` (issue numbers here are illustrative — this is an offline
  example, not a real GitHub repo).
- **Session start in <2 minutes**: `/session:start` orients the agent
  without reading source code.

## Stack

- Node 22+
- Express 5 + zod (input validation)
- PostgreSQL 16
- vitest 2

9 source files, ~25 total files including config and docs.

## Run it

```bash
# Install deps
npm install

# Start the test database (Postgres in Docker)
npm run test:db:up

# Apply the migration
TEST_DATABASE_URL=postgres://cfd:cfd@localhost:5433/cfd_test \
  npm run migrate:test

# Run all tests (unit + integration)
TEST_DATABASE_URL=postgres://cfd:cfd@localhost:5433/cfd_test \
  npm test

# Run the dev server
cp .env.example .env
npm run dev
```

Try the endpoints:

```bash
curl -X POST http://localhost:3000/notifications \
  -H 'Content-Type: application/json' \
  -d '{"userId":"u1","message":"hello","channel":"email"}'

curl http://localhost:3000/notifications/u1
```

## CFD entry points

| Command            | Purpose                                                 |
| ------------------ | ------------------------------------------------------- |
| `/session:start`   | Orient the agent in <1.5k tokens                        |
| `/issue:new`       | Create a tracker issue with the fixed body template     |
| `/issue:start <n>` | Pick up an issue as session focus                       |
| `/decision:new`    | Document an architectural decision before implementing  |
| `/session:close`   | Update CURRENT_STATUS + CONVENTIONS before ending       |

See [`CLAUDE.md`](CLAUDE.md) for the index of context the agent reads.

## What this example is NOT

- Production-ready (no auth, no rate limits, no migration runner).
- A framework or template you should clone for new projects.
  Copy [`templates/`](../../templates/) instead.

The point of this example is to show *what CFD adoption looks like* in
a real-shaped codebase, not to be the starting point for your service.

## Adapting catalog ADRs

`docs/decisions/002-repository-pattern.md`,
`docs/decisions/003-integration-over-mocks.md`, and
`docs/decisions/004-trunk-based-with-rc.md` are adapted copies of
entries in the parent CFD repo's
[`adrs/`](../../adrs/) catalog. Each one carries a top-of-file comment
pointing back to the catalog source — the "shadcn for AI context"
pattern in action.
