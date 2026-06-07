# Examples

Tiny, runnable projects with CFD fully applied. Each example is
≤30 source files and demonstrates a stack-specific application of the
methodology.

**The goal**: an engineer adopting CFD for a Node/Express project (or
Python/FastAPI, Go, Rust, etc.) can clone the matching example, see CFD
in action, and start a fresh session in <5 minutes.

## Live examples

- [**`node-express/`**](node-express/) — Node 22 + Express 5 + Postgres
  notification API. Demonstrates layered architecture, repository
  pattern, integration-over-mocks testing, trunk-based + RC workflow,
  the work-tracking layer (`/issue:new`, `/issue:start`).

## Wanted

- `python-fastapi/` — Python + FastAPI, repository pattern.
- `go-stdlib/` — Go with stdlib HTTP, clean architecture.
- `rust-axum/` — Rust + Axum, hexagonal architecture.

If you'd like to contribute one, open an issue first so we can align on
scope. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md#contributing-an-example)
for the layout contract.

## What a good example looks like

```text
examples/<stack-name>/
  README.md          purpose, stack, what's demonstrated
  CLAUDE.md          filled-in, not template
  docs/
    ARCHITECTURE.md  filled-in
    STACK.md         filled-in
    CONVENTIONS.md   filled-in
    CURRENT_STATUS.md  reflects a realistic session log
    decisions/
      _index.md
      001-initial-architecture.md
      002-<a-catalog-adr-adapted>.md
      003-<another>.md       (at least 3 ADRs total)
  .claude/commands/  adapted from templates/
  src/               working code
```

A reviewer should be able to clone the example, run `/session:start`,
and within 2 minutes know what the project does, what's in progress,
and what conventions apply — without reading any source file.
