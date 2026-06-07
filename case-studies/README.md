# Case Studies

First-person accounts of adopting Context-First Development in real
teams.

Each case study must satisfy:

- **Author identification** (LinkedIn or GitHub profile).
- **At least one measurable claim** (tokens before/after,
  time-to-first-correct-action, re-explanation rate, or comparable
  signal).
- **Explicit publication permission** from the team, stated in the PR
  body.

## Current case studies

- **[Measurement: tokens-per-session on `examples/node-express`](measurement-node-express.md)**
  — measured **12.8× reduction** (824 vs 10,519 tokens) at session
  orientation. Reproducible via
  [`scripts/measure-session-cost.sh`](../scripts/measure-session-cost.sh).
- **[nemo-cli](nemo-cli.md)** — production Python CLI (broker portal
  client) built solo with CFD. 11 ADRs with an explicit `002 → 004`
  supersession. Public, MIT-licensed, clickable end-to-end.
- [ID Watchdog Mobile (Equifax)](id-watchdog-equifax.md) — in
  progress (pending team review).

## Contributing a case study

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md#contributing-a-case-study)
for the full contract.
