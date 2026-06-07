# Examples

Tiny, runnable projects with CFD fully applied. Each example is
≤30 source files and demonstrates a stack-specific application of the
methodology.

**The goal**: an engineer adopting CFD for a Node/Express project (or
Python/FastAPI, Go, Rust, etc.) can clone the matching example, see CFD
in action, and start a fresh session in <5 minutes.

## Status

No examples are authored yet. Intentional — examples come from
contributors using their preferred stacks. PRs welcome; see
[`../CONTRIBUTING.md`](../CONTRIBUTING.md#contributing-an-example) for
the layout contract.

## Wanted

- `node-express/` — TypeScript + Express, layered architecture.
- `python-fastapi/` — Python + FastAPI, repository pattern.
- `go-stdlib/` — Go with stdlib HTTP, clean architecture.
- `rust-axum/` — Rust + Axum, hexagonal architecture.

If you'd like to contribute one, open an issue first so we can align on
scope.

## What a good example looks like

```
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
      002-<a-real-decision>.md
      003-<another>.md       (at least 3 ADRs total)
  .claude/commands/  copied from templates/, lightly adapted
  src/               working code
```

A reviewer should be able to clone the example, run `/session:start`,
and within 2 minutes know what the project does, what's in progress, and
what conventions apply — without reading any source file.
