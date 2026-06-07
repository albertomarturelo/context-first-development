<!-- Loaded on demand. -->

# Tech Stack

## Runtime
- Node.js `>=22` (ES modules, top-level `await`).

## Frameworks
- `express` 5 — HTTP server.
- `zod` 3 — input validation.

## Database & Storage
- PostgreSQL 16 (production target).
- Local test instance via `docker-compose.test.yml` on port `5433`.

## External Services
- None — this is an example.

## Development Tools
- Package manager: `npm`.
- Test runner: `vitest` 2.
- Type checker: `tsc --noEmit` via `npm run typecheck`.
- Linter / formatter: not configured (example is intentionally minimal).
- Dev runner: `tsx` (watch + run TypeScript directly).
