<!-- ~90 tokens loaded by your agent at session start. -->

# Project: notifications

## What This Project Does

A tiny REST API for creating and listing user notifications. Two
endpoints, PostgreSQL persistence. Exists as a runnable example of CFD
applied to a Node/Express stack.

## Architecture
@docs/ARCHITECTURE.md

## Tech Stack
@docs/STACK.md

## Conventions
@docs/CONVENTIONS.md

## Current Status
@docs/CURRENT_STATUS.md

## Key Decisions
@docs/decisions/_index.md

## Build & Run
- Install: `npm install`
- Test DB up: `npm run test:db:up`
- Migrate: `npm run migrate:test`
- Test: `npm test`
- Dev: `npm run dev`

## Critical Rules
- All persistence access goes through the repository interface
  (ADR-002).
- Data-layer tests use the real Postgres in `docker-compose.test.yml`,
  not mocks (ADR-003).
- All branches (`feature/* fix/* chore/* docs/*`) target `main`. Linear
  history enforced (ADR-004).
- Use `/issue:new` to create tracker issues; use `/issue:start <n>` to
  pick one up. Don't open work without an issue.
- Use `/review-pr <n>` before merge — cross-checks the diff against
  the AC checklist, CONVENTIONS, and the touched ADRs without
  scanning full files.
