<!-- Adapted from the parent CFD catalog:
     adrs/process/trunk-based-with-release-candidates.md -->

# ADR-004: Trunk-Based Workflow with RC Branches

## Status
Accepted — 2026-06-07

## Context

This example is a single-developer project (it is, after all, an
example). Long-lived integration branches would add daily friction
without ever catching a multi-developer integration failure mode. We
still want a stable target if an `rc/X.Y.Z` of the example is ever cut
for a workshop or demo.

## Decision

- `main` is the trunk and the default branch.
- All work branches (`feature/* fix/* chore/* docs/*`) target `main`
  via PR.
- If an `rc/X.Y.Z` is cut (e.g., for a workshop), it stabilizes in
  place and squash-merges back to `main` + tag `vX.Y.Z`.
- `main` protection: required PR before merge, required linear
  history (rebase / squash only).
- `enforce_admins: false` while solo; flip to `true` once the team is
  ≥2 contributors (does not apply to this example).

Issue-linked branches use `feature/GH-<n>-<slug>` (the issue numbers
are illustrative — see `CURRENT_STATUS.md`).

## Alternatives Considered

1. **Git Flow with long-lived `develop`.** Overkill for a
   single-author example; never catches anything.
2. **No branches, commit straight to `main`.** Demos can pretend, but
   real CFD adoption needs the PR cycle to be the demo.

## Consequences

- `git log main --merges` returns 0 (linear history).
- One open `rc/*` at most at any time.
- Any tag `vX.Y.Z` is reachable from `main`.
