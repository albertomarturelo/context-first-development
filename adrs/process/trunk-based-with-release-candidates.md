<!-- Shareable ADR. Token budget: ~550. -->

# ADR-`<NNN>`: Trunk-Based Workflow with Release-Candidate Branches

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- Solo developer or small team (≤5 engineers) on the same codebase.
- No continuous deployment to production yet (or none at all).
- Product has periodic client/stakeholder review cycles where a build
  is handed off and may receive small fixes during review.
- You want `git log main` to read as the canonical release story.

Skip if you already ship many times per day via CD with feature flags
(go fully trunk-based, no `rc/*`), or you run healthy Git Flow with a
real multi-team integration use case (the switch cost is not worth it).

## Context

Long-lived integration branches (Git Flow's `develop`) catch bad
integrations from multiple developers before they reach `main`. With a
solo developer or tiny team the branch never catches anything — the
work all comes from one source. The convention pays daily cost (PR
target decisions, dual protection rules, tooling that special-cases
both branches) for a benefit that never materializes.

Pure GitHub Flow removes the integration branch but offers no stable
target for fixes that surface during stakeholder review of a candidate
build. This ADR codifies the middle path: **trunk + release-candidate
branches for stabilization handoffs**. Commonly called "GitHub Flow +
RC"; principle is forge-agnostic (GitLab, Bitbucket, Gitea, etc.).

## Decision

### Branching strategy

```text
main          ← Trunk. Default branch. All work merges here.
<type>/*      ← feature | fix | chore | docs; from main, PR back to main.
rc/X.Y.Z      ← from a known-good main commit; stabilized in place;
                squash-merged to main + tagged when approved.
hotfix/*      ← from the tagged release commit; PR to main;
                cherry-pick to live rc/* if applicable.
```

### PR target rules

| Branch type                                | PR target                                  |
| ------------------------------------------ | ------------------------------------------ |
| `feature/*`, `fix/*`, `chore/*`, `docs/*`  | `main`                                     |
| `rc/X.Y.Z` (when approved)                 | `main` — squash-merge, tag `vX.Y.Z`        |
| `hotfix/*`                                 | `main` — cherry-pick to live `rc/*` if any |

### `main` protection rules

- Required PR before merge — no direct pushes.
- Required **linear history** — rebase or squash only, no merge commits.
- `enforce_admins: false` while solo; flip to `true` once team is ≥2.

### Branch naming

Issue-linked branches prefix with the tracker ID (`feature/GH-3-...`,
`fix/JIRA-42-...`) — grep-ability is the point; tracker is incidental.
PR titles follow Conventional Commits — the squash commit message
becomes the branch's story on `main`.

## Alternatives Considered

1. **Git Flow with long-lived `develop`.** Designed for multi-team
   integration; with ≤5 devs it costs daily friction without catching
   anything.
2. **Pure trunk-based with CD.** Correct end-state once you have CD +
   feature flags; premature without either.
3. **GitHub Flow tagging directly from `main`, no `rc/*`.** Cleanest
   log but no stable target for stabilization fixes. Fine for
   ship-many-times-a-day; not for periodic-handoff products.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `git branch -a` shows no long-lived branch other than `main` and
  possibly one active `rc/X.Y.Z`.
- `git log main --merges` returns 0 entries and every tag `vX.Y.Z` is
  reachable from `main`.
- Every `rc/*` that ever existed is merged into `main` (and deleted),
  except possibly the current candidate.
- Branch-protection on `main` shows "Require linear history" and
  "Require pull request before merging" enabled.

## Trade-offs

- Extra branch concept (`rc/*`) over textbook GitHub Flow — drop when
  releases become pure trunk-tag events.
- `enforce_admins: false` is a safety hole; flip to `true` at team ≥2.
