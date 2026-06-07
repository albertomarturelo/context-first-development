# CFD in motion

Four sequence diagrams showing what a CFD session actually looks like,
message by message. Read in order; each scenario builds on the previous.

> **Notation.** All diagrams are [Mermaid sequence
> diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html) and
> render natively on GitHub. Token-cost annotations are approximate
> and based on the [methodology gist](../METHODOLOGY.md).

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

## How to use these diagrams

- **You're learning CFD.** Read A → B → C → D in order. By the end
  you've seen every flow the methodology actually runs.
- **You're adopting CFD.** A is your day 0. B is the loop you run from
  day 1 onward. C and D are the failure-recovery patterns that keep
  the methodology honest.
- **You're presenting CFD to your team.** B is the headline. A is the
  "how do I start?" answer. C and D are the slides that explain why
  CFD is more than "another file format" — they show the discipline.

## See also

- [`adrs/_index.md`](../adrs/_index.md) — the shareable ADR catalog.
- [`templates/`](../templates/) — the slash commands referenced above.
- [`case-studies/nemo-cli.md`](../case-studies/nemo-cli.md) — a real
  project running these flows.
- [`examples/node-express/`](../examples/node-express/) — runnable
  code with the same flows applied.
- [`METHODOLOGY.md`](../METHODOLOGY.md) — the canonical essay.
