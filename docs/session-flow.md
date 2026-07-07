# CFD in motion

A map of the whole workflow, then six sequence diagrams showing what a
CFD session actually looks like, message by message. Start with the
map, pick your entry point (A for an existing codebase, G for a
greenfield repo), then read B → C → D → E in order.

> **Notation.** Diagrams are [Mermaid](https://mermaid.js.org/) and
> render natively on GitHub. Token-cost annotations are approximate
> and based on the [methodology essay](../METHODOLOGY.md).

## The map — entry points and the daily loop

Two ways in, one loop forever after. Adopting on an existing project
(Scenario A) infers the docs from the code; starting from zero
(Scenario G) declares the docs before the code. Either way you land in
the same daily loop: orient, take or create an issue, implement,
close, review.

```mermaid
flowchart TD
    START(["You + an AI agent + a repository"]) --> Q{"Does the codebase<br/>exist yet?"}
    Q -- "existing project" --> A["/project:init<br/>infer docs/ + CLAUDE.md from<br/>structure — Scenario A"]
    Q -- "starting from zero" --> G["Greenfield bootstrap<br/>ADRs first, then scaffold<br/>— Scenario G"]
    A --> R["Review inferred conventions<br/>and ADR-001"]
    R --> B0["Decompose upcoming work into<br/>1-session issues via /issue:new"]
    G --> B0

    subgraph LOOP["The daily loop — every working session"]
        SS["/session:start<br/>orient in ~1.5–3k tokens"] --> P{"In-progress issue in<br/>CURRENT_STATUS.md?"}
        P -- "yes — auto-loaded" --> IMPL
        P -- "no" --> T{"Issue ready<br/>in the tracker?"}
        T -- "take one" --> IS["/issue:start N<br/>load its ADRs + pattern file"]
        T -- "create one" --> IN["/issue:new<br/>fixed body template,<br/>then /issue:start"]
        IS --> IMPL
        IN --> IMPL
        IMPL["Implement AC items<br/>(read target files before editing)"] --> MID{"Mid-session<br/>event?"}
        MID -- "user corrects a pattern" --> C["Fix code AND document rule<br/>in CONVENTIONS.md — Scenario C"]
        MID -- "significant decision surfaces" --> D["/decision:new — ADR lands<br/>BEFORE the code — Scenario D"]
        C --> IMPL
        D --> IMPL
        MID -- "AC done, or context filling up" --> SC["/session:close<br/>update CURRENT_STATUS.md"]
        SC --> PR["git push + gh pr create<br/>PR description = AC checklist"]
        PR --> RV["/review-pr N<br/>verify diff against context — Scenario E"]
    end

    B0 --> SS
    RV --> M(["Merge — closes the issue"])
    M -.->|"next session"| SS
```

Three properties make the loop cheap: orientation is O(1k) tokens
because state lives in `CURRENT_STATUS.md` and the tracker, not in
chat history; every issue is 1-session-sized by construction
(`/issue:new` forces decomposition); and sessions are disposable —
closing early costs one `/session:start`, drifting costs redone work
(see the
[short-sessions](../adrs/ai-workflow/short-sessions-over-long.md)
catalog ADR).

## Scenario A — Bootstrap: adopting CFD on an existing project

**When:** Day 0. You have a real repo with 100+ files, no `CLAUDE.md`,
no `docs/`. You run `/project:init` once.

**Key property:** the agent does NOT scan source code. It infers from
the directory layout and dependency files. Source code reading is
deferred until real work surfaces it.

```mermaid
sequenceDiagram
    autonumber
    actor E as Engineer
    participant A as Agent
    participant FS as Filesystem
    participant DOCS as docs/ + CLAUDE.md

    Note over E,A: Existing repo. No CFD scaffold yet.
    E->>A: /project:init
    A->>FS: ls / tree -L 2
    A->>FS: read package.json / pyproject.toml / Cargo.toml / …
    A->>FS: read README.md (if any)
    Note right of A: ~5–10k tokens total.<br/>NO source code reads.
    A->>DOCS: create CLAUDE.md (filled, ~100 lines)
    A->>DOCS: create docs/ARCHITECTURE.md (inferred)
    A->>DOCS: create docs/STACK.md
    A->>DOCS: create docs/CONVENTIONS.md (marked "inferred — confirm")
    A->>DOCS: create docs/CURRENT_STATUS.md (empty stub)
    A->>DOCS: create docs/decisions/{_index,001-initial-architecture}.md
    A-->>E: summary + ask to review inferred conventions
    Note over E: Review pass.<br/>Confirm or amend.
```

After this scenario you have CFD scaffold. Real work uses Scenario B.

---

## Scenario G — Greenfield: starting from zero

**When:** Day 0 of a project that does not exist yet. `git init` and
nothing else — no code, no docs, no decisions made.

**Key property:** the mirror image of Scenario A. There, docs are
**inferred** from existing code and marked "confirm"; here, docs are
**declared** before any code exists and are prescriptive — the first
commit already has an architecture it must comply with. Stack and
architecture choices are captured as ADRs *at the moment they are
made*, when the alternatives are still fresh, instead of being
reverse-engineered later.

This is not hypothetical: in the [sii case study](../case-studies/sii.md),
ADR-001 ("Adopt CFD") carries the same date as the repository's
creation.

```mermaid
sequenceDiagram
    autonumber
    actor E as Engineer
    participant A as Agent
    participant ADRs as docs/decisions/
    participant DOCS as docs/ + CLAUDE.md
    participant ISS as Tracker<br/>(via gh)
    participant CODE as Source code

    Note over E,A: Empty repository. git init, nothing else.

    E->>A: Product idea + constraints (a few paragraphs)
    A-->>E: Stack, architecture, testing posture —<br/>these are DECISIONS, not defaults.<br/>Running /decision:new for each.

    A->>E: Language/runtime? Constraints? Alternatives?
    E-->>A: Trade-offs discussed, choices made.

    A->>ADRs: 001-adopt-cfd.md
    A->>ADRs: 002-stack.md · 003-architecture.md<br/>(each with rejected alternatives)
    A->>DOCS: CLAUDE.md + STACK / ARCHITECTURE /<br/>CONVENTIONS
    Note right of DOCS: DECLARED, not inferred.<br/>Code must comply with docs —<br/>the reverse of Scenario A.
    A->>DOCS: CURRENT_STATUS.md ("scaffold is next")

    A->>ISS: /issue:new — scaffold + first feature,<br/>each sized to 1 session
    A-->>E: Day 0 done. Zero lines of code —<br/>and that is the point.

    E->>A: /issue:start 1
    A->>CODE: scaffold per ADR-002 / ADR-003
    Note right of CODE: The first commit lands inside<br/>an architecture, not before one.
```

From here on, every session is Scenario B.

---

## Scenario B — Canonical session (happy path)

**When:** every working session, once CFD is established. The vast
majority of sessions look like this.

**Key property:** session-start consumes ~1.5–3k tokens to fully
orient — including the auto-loaded in-progress issue. Source code is
read only once a focus is chosen.

```mermaid
sequenceDiagram
    autonumber
    actor E as Engineer
    participant A as Agent
    participant DOCS as docs/
    participant ADRs as docs/decisions/
    participant ISS as GitHub Issues<br/>(via gh)
    participant CODE as Source code

    Note over E,A: Project has CFD scaffold + at least one open issue.

    E->>A: /session:start
    A->>DOCS: read CURRENT_STATUS.md
    A->>ADRs: read _index.md
    Note right of A: ~500–1.5k tokens
    A->>A: detect "#142 in progress"
    A->>ISS: gh issue view 142
    A->>ADRs: read ADRs listed in "ADRs to load"
    A-->>E: objective + AC checklist +<br/>target paths + pattern to mirror
    Note right of A: Total so far: ~1.5–3k tokens

    E->>A: Ready. Implement AC item 1.
    A->>CODE: read pattern file (mirror)
    A->>CODE: Edit target paths
    A->>CODE: run tests
    A-->>E: report + next-step question

    loop until AC checklist is done
        E->>A: next AC item
        A->>CODE: implement + test
        A-->>E: report
    end

    E->>A: /session:close
    A->>DOCS: update CURRENT_STATUS.md
    A-->>E: session summary suitable for PR description

    E->>ISS: git push + gh pr create
    Note right of E: PR description<br/>= AC checklist verbatim
    Note over ISS: PR merge closes #142
```

---

## Scenario C — Correction surfaces a new convention

**When:** the agent generates code that violates an unstated team
convention. You don't just fix the code — you document the convention.

**Key property:** the convention is captured in
`docs/CONVENTIONS.md` in the **same change** as the code fix. Next
session, the model reads the convention automatically. The same
correction never repeats.

This is the
[`document-corrections-not-fixes`](../adrs/process/document-corrections-not-fixes.md)
catalog ADR in action.

```mermaid
sequenceDiagram
    autonumber
    actor E as Engineer
    participant A as Agent
    participant CODE as Source code
    participant CONV as docs/CONVENTIONS.md

    Note over E,A: Mid-implementation, inside Scenario B's loop.

    A->>CODE: write NotificationService as a module singleton
    A-->>E: implementation done

    E-->>A: ✗ We never use singletons.<br/>Dependency injection only.

    Note over E,A: Per catalog ADR<br/>"document-corrections-not-fixes":<br/>fix the CODE *and* document the rule.

    A->>CODE: refactor NotificationService<br/>to accept constructor deps
    A->>CONV: append "DI over singletons" under Patterns
    A-->>E: code fixed + CONVENTIONS.md updated<br/>(both ship in the same PR)

    Note right of CONV: Next session reads this automatically.<br/>Correction does not repeat.
```

---

## Scenario D — Mid-session decision triggers `/decision:new`

**When:** during implementation, a non-trivial decision surfaces (a
new dependency, a new pattern, a new strategy). Instead of just doing
it, the agent stops and writes the ADR first.

**Key property:** the ADR lands BEFORE the code that implements it.
Future sessions can reconstruct *why* without git archaeology, and the
rejected alternatives are preserved so the model does not later
suggest reverting.

This is the
[`adr-before-implementing`](../adrs/ai-workflow/adr-before-implementing.md)
catalog ADR in action.

```mermaid
sequenceDiagram
    autonumber
    actor E as Engineer
    participant A as Agent
    participant ADRs as docs/decisions/
    participant CODE as Source code

    Note over E,A: Working through Scenario B's AC items.

    E->>A: We need caching. Let's just use Redis.

    Note over A: Per catalog ADR<br/>"adr-before-implementing":<br/>stop, capture the decision first.

    A-->>E: Hold — this is a significant decision.<br/>Running /decision:new.

    A->>E: What problem? What constraints? What triggers it now?
    E-->>A: Reduce p99 on hot endpoint,<br/>1k req/s peak, no consistency requirement.

    A->>E: Alternatives:<br/>Redis · Memcached · in-process LRU.<br/>Trade-offs?
    E-->>A: Picks Redis.

    A->>ADRs: write 015-cache-with-redis.md (Status: Accepted)
    A->>ADRs: update _index.md
    A-->>E: ADR-015 landed. Ready to implement.

    E->>A: Go.
    A->>CODE: implement Redis client + cache invalidation
    Note right of CODE: Implementation references ADR-015<br/>in the commit message and CONVENTIONS.md.
```

---

## Scenario E — PR review against context (closing the cycle)

**When:** the session opened a PR. Before merge, the diff is reviewed
against the project's context — NOT by reading the changed files in
full, but by **cross-checking the diff against indices** (CONVENTIONS,
ADRs, the linked issue's AC, the PR template).

**Key property:** the operational thesis of CFD made literal. The
review's *agenda* is set by the indices (CONVENTIONS + ADRs + AC +
PR template + the team's curated checklist). The depth of file reads
is whatever that agenda demands — minimal for a small Node API,
exhaustive for a strict KMP project. The work is **verification
against known rules**, not **discovery of intent from code**.

This is the
[`pr-review-against-context`](../adrs/process/pr-review-against-context.md)
catalog ADR in action.

```mermaid
sequenceDiagram
    autonumber
    actor R as Reviewer
    participant A as Agent
    participant ISS as PR + Issues<br/>(via gh)
    participant CONV as docs/CONVENTIONS.md
    participant ADRs as docs/decisions/
    participant CODE as Changed files

    Note over R,A: PR #87 is open. Ready for review.

    R->>A: /review-pr 87
    A->>ISS: gh pr view 87
    A->>ISS: gh pr diff 87
    A->>ISS: git log base..head (commit story)
    Note right of A: ~1–3k tokens<br/>(PR metadata + diff)

    A->>ISS: gh issue view (linked)
    A->>CONV: read
    A->>ADRs: read each ADR named in the issue body
    Note right of A: Agenda loaded: ~2–4k tokens

    A->>CODE: read changed files to the depth the<br/>team's checklist demands
    Note right of A: Verification reads, not discovery.<br/>Strict-KMP: full files. Small-API: diff-bounded.

    A->>A: apply team checklist<br/>(workflow + architecture + tests<br/>+ AC + docs drift + ...)

    A-->>R: structured report<br/>✓ Passes (cite ADR / CONV line)<br/>⚠ Suggestions<br/>✗ Blocks merge (cite verifiable consequence)

    Note over R: Reviewer decides:<br/>request changes / approve / merge.
```

---

## How to use these diagrams

- **You're learning CFD.** Start with the map, then read A (or G) →
  B → C → D → E. By the end you've seen every flow the methodology
  actually runs.
- **You're adopting CFD on an existing repo.** A is your day 0. B is
  the loop you run from day 1 onward. C and D are the
  failure-recovery patterns that keep the methodology honest. E is
  how the loop closes before merge.
- **You're starting a project from zero.** G is your day 0 —
  decisions and docs land before the first line of code, so the
  scaffold is born compliant. Then B, same as everyone else.
- **You're presenting CFD to your team.** The map is the opening
  slide. B is the headline. A and G are the "how do I start?"
  answers. C and D are the slides that explain why CFD is more than
  "another file format". E is the slide that shows the token economy
  of the whole approach — *diff, not repo*.

## See also

- [`adrs/_index.md`](../adrs/_index.md) — the shareable ADR catalog.
- [`templates/`](../templates/) — the slash commands referenced above.
- [`case-studies/sii.md`](../case-studies/sii.md) — a real
  project running these flows.
- [`METHODOLOGY.md`](../METHODOLOGY.md) — the canonical essay.
