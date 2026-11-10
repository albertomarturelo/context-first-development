<!-- Shareable ADR. Token budget: ~1,165. -->

# Agent Telemetry from Local Logs, Published per Developer

## Status

`Accepted` — `<YYYY-MM-DD>`

## When to Use

Adopt this ADR when:

- A team wants to know what its coding agents consume per task, and
  whether a change to the context made sessions cheaper.
- More than one agent or vendor is in use, so no vendor dashboard
  covers all of it.

Do NOT adopt it in a public repository, or where the numbers would
feed performance reviews: the rules below exist to prevent that use.

## Context

Agents already keep session logs on the developer's machine: tokens
per request, model, branch, timestamps. Vendor dashboards report per
seat and per vendor, not per repository or task, and none spans
vendors. The logs are undocumented, change between agent versions and
are pruned by the agent itself. Two failure modes follow. Silent gaps:
a format change reads as "no usage". Surveillance: per-person numbers
turn into a leaderboard, and developers stop publishing.

## Decision

1. **The source is the logs agents already keep**, read on the
   developer's machine by one dependency-free script with one adapter
   per agent. No proxy, no SDK, nothing to install per agent.
2. **Counters only.** Tokens by type, requests, turns, active minutes,
   models, branches, skill names, days. Never prompts, responses, file
   contents or paths. A source that mixes counters and text is read by
   named field or column, never whole.
3. **Gaps are numbers.** Each adapter counts what it could not read.
   "No source on this machine", "source with nothing for this project"
   and "sessions read" are three different lines, never a zero.
4. **A local history** folds in every session read, so log pruning
   loses nothing that was seen once.
5. **Publishing is opt-in and per developer.** One counters-only file
   per developer and month on an orphan branch of the same repository
   (`reports/<developer>/<YYYY-MM>.json`), written through git plumbing.
   The developer is the git identity that already signs the work; an
   anonymous mode replaces it with a random id.
6. **Private repositories only.** Publishing refuses a public one.
7. **The team view filters by contributor; it never ranks.** Beside the
   agent filter, a reader may offer a contributor filter: select one or
   more people and every total, chart and table recomputes for them.
   No view sorts or charts people against each other: no leaderboard,
   no per-person column, no "top consumers". A contributor whose last
   report is stale shows as "not reporting", distinct from zero usage.
8. **Per-person numbers explain a task's cost**, and let each developer
   see their own. They are not a performance measure.

## Alternatives Considered

1. **Vendor dashboards.** Per seat and per vendor: no repository, task
   or context-change dimension, and nothing spans vendors.
2. **An OpenTelemetry collector or proxy.** Accurate, but one more
   service and per-machine setup for every agent, and history starts
   only when it is installed.
3. **A central database.** Credentials, hosting and migrations, for
   data that git already versions and repository permissions scope.
4. **No person dimension at all.** Cannot tell a developer their own
   consumption, nor whom to ask when a task cost ten times the median.
5. **Per-person rows only inside a task's detail.** Safer, but no one
   sees their own consumption across tasks; the filter gives that view
   without a side-by-side comparison.

## Verifiable Consequences

A reader can confirm this ADR is being followed if:

- `git ls-tree -r --name-only <telemetry-branch>` lists only
  `reports/<developer>/<YYYY-MM>.json` and `status.json` files.
- A phrase from a recent prompt appears in no file of that branch
  (`git grep -c '<phrase>' <telemetry-branch>` prints nothing).
- Every repository that has the branch is private
  (`gh repo view --json visibility`).
- The script prints one line per agent even when it read nothing, and
  a note for every non-zero gap counter.
- The team view has a contributor filter, and no table or chart ordered
  by a contributor's consumption.

## Trade-offs

- Log formats change without notice: the gap counters make a break
  visible, they do not prevent it. Each adapter is upkeep.
- Coverage is voluntary: only developers who publish appear.
- The git identity is personal data inside the organisation, and forge
  admins see who pushed even in anonymous mode.
- A filter still lets someone compare two people one at a time. The
  rule removes the leaderboard, not the possibility; this record is
  the team's agreement not to use it that way.
