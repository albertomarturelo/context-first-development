# Changelog

This file is written for the agent that upgrades an adopting repository,
not only for people. Every release carries an **Upgrade** section: the
exact steps that take a project from the previous version to this one.
`/cfd-upgrade` reads the installed version from the artifacts
(`metadata.cfd-version` in every `SKILL.md`, a `CFD version:` line in the
scaffold files), fetches this file, and applies the Upgrade sections
between the two versions, oldest first.

Versions follow [Semantic Versioning](https://semver.org/): **major** when
a workflow rule changes (an agent following the old rule now does the
wrong thing), **minor** when a skill, ADR or template is added, **patch**
for corrections that change no behaviour. One version covers the essay,
the templates and the catalog; it lives in `.claude-plugin/plugin.json`
and is stamped into the templates by `scripts/stamp-version.sh`.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Catalog ADR [agent-telemetry-from-local-logs](adrs/ai-workflow/agent-telemetry-from-local-logs.md):
  the decision behind `telemetry-report` (local logs as the source,
  counters only, gaps as numbers, per-developer reports on an orphan
  branch, private repositories only), plus the rule for a team view: it
  filters by contributor and never ranks.
- Catalog ADR [agent-cost-estimates-at-read-time](adrs/ai-workflow/agent-cost-estimates-at-read-time.md):
  reports stay in tokens; a reader computes dollar estimates from a
  dated price table the team owns, prices each token type and tier on
  its own, leaves unknown models unpriced instead of at $0, and shows
  billed units (credits, premium requests) in their own unit.

### Changed

- `scripts/stamp-version.sh` also stamps the README setup prompt, the
  line that sets the version a new project starts at, and
  `scripts/validate-catalog.sh` therefore refuses a stale one. The
  marker is replaced, never inserted: a README without it fails.
  Repository-only; adopters copy nothing new.

## [0.4.0] — 2026-11-09

### Added

- `telemetry-report`: a `copilot-cli` adapter. It reads the usage table
  of the Copilot CLI session store (`~/.copilot/session-store.db`,
  `COPILOT_HOME`), selecting named columns only: the tables and files
  that hold prompts and responses are never opened. Sessions from
  before any OpenTelemetry setup count; the CLI's own OpenTelemetry
  export is not read, so nothing counts twice. The summary and the
  dashboard footer tell apart no store, a store from a CLI version
  that records no usage, an unreadable store, a store with no session
  for this project, and sessions read. Published reports carry
  `a: "copilot-cli"` (albertomarturelo/context-first-development#25).
- `telemetry-report`: a `copilot` line for Copilot Chat in VS Code in
  the summary and the dashboard footer. It says whether an
  OpenTelemetry file export of Copilot Chat exists on this machine,
  found through the `outfile` user setting of VS Code only:
  `COPILOT_OTEL_FILE_EXPORTER_PATH` is shared with Copilot CLI, so a
  path there cannot be attributed to either product. When an export
  exists, the line says this version does not read it yet; a
  `copilot_unparsed` note marks that gap. The parser follows once the
  export's record shape has been observed on a real file
  (albertomarturelo/context-first-development#23).
- `scripts/tests/`: a dependency-free test harness over synthetic
  fixtures for every adapter of `telemetry-report`, run by
  `scripts/validate-catalog.sh` and CI. Repository-only; adopters copy
  nothing new.

### Changed

- `telemetry-report`: the dashboard names the agents Copilot CLI and
  Copilot Chat, and the "not measured here" sentence names Gemini
  only. Nothing in the workflow rules; the other skills change only in
  their version stamp.

### Upgrade

Run from the repository root. Each step is idempotent.

1. Fetch the templates as in 0.3.0, step 1.
2. Replace the skills (this updates `telemetry-report` and stamps
   0.4.0 into every skill):
   `cp -R "$tmp/cfd/templates/.agents/skills/." .agents/skills/`
   Skills installed with `npx skills add` or as the Claude Code plugin:
   as in 0.3.0, step 2.
3. Restamp the scaffold: change `CFD version: 0.3.0` to
   `CFD version: 0.4.0` in the comment at the top of `CLAUDE.md`, and
   `# CFD version: 0.3.0` to `# CFD version: 0.4.0` in
   `.claude/hooks/*.sh` and `.github/workflows/context-freshness.yml`.
   Nothing else in those files changed.
4. A central reader of the `cfd-telemetry` branch accepts the agent
   `copilot-cli`; the schema stays `cfd-telemetry/1`.
5. Verify: `grep -h '^  cfd-version:' .agents/skills/*/SKILL.md | sort -u`
   prints one line, `0.4.0`.

## [0.3.0] — 2026-11-09

### Added

- `telemetry-report` skill: a local dashboard built from the session
  logs Claude Code and Codex already keep (tokens per day, task, skill
  and session; context at first request; tokens before the first edit;
  medians before and after each change to the context files), with a
  local history and an opt-in, counters-only monthly report published
  to an orphan `cfd-telemetry` branch. Public repositories are refused.
  Quickstart in `docs/telemetry-quickstart.md`.
- `cfd-upgrade` skill: reads the installed version, fetches this file
  and applies the Upgrade steps between the two versions.
- Version stamps: `metadata.cfd-version` in every skill, `CFD version:`
  in `CLAUDE.md`, the hooks and the CI workflow. `scripts/stamp-version.sh`
  writes them; `scripts/validate-catalog.sh` refuses a mismatch.

### Changed

- Nothing in the workflow rules. Existing skills are unchanged except
  for the version stamp.

### Upgrade

Run from the repository root. Each step is idempotent.

1. Fetch the templates:
   `tmp=$(mktemp -d) && git clone --depth 1 https://github.com/albertomarturelo/context-first-development.git "$tmp/cfd"`
2. Replace the skills (this adds `telemetry-report` and `cfd-upgrade`
   and stamps the version into every skill):
   `cp -R "$tmp/cfd/templates/.agents/skills/." .agents/skills/`
   Skills installed with `npx skills add` instead: rerun
   `npx skills add albertomarturelo/context-first-development`. Skills
   installed as the Claude Code plugin: `/plugin update cfd`.
3. Ignore the telemetry output: add `.cfd/` to `.gitignore`.
4. Stamp the scaffold. Add the line `CFD version: 0.3.0` inside the
   HTML comment at the top of `CLAUDE.md` (create a one-line comment
   `<!-- CFD version: 0.3.0 -->` if the file has none). Copy the hooks
   and the workflow only if the project never edited them:
   `cp "$tmp/cfd/templates/.claude/hooks/"*.sh .claude/hooks/` and
   `cp "$tmp/cfd/templates/.github/workflows/context-freshness.yml" .github/workflows/`.
   Otherwise add `# CFD version: 0.3.0` as the second line of each.
5. Verify: `grep -h '^  cfd-version:' .agents/skills/*/SKILL.md | sort -u`
   prints one line, `0.3.0`.

## [0.2.0] — 2026-10-10

Reconstructed from git history; this version was not tagged.

### Added

- Procedures ship as [Agent Skills](https://agentskills.io/specification)
  in `.agents/skills/<name>/SKILL.md`, one copy for Claude Code, Codex,
  Copilot and Gemini CLI; `.claude/skills` is a symlink
  ([agent-skills-as-procedures](adrs/ai-workflow/agent-skills-as-procedures.md)).
- Catalog ADRs: [parallel loops in git worktrees](adrs/ai-workflow/parallel-loops-in-worktrees.md),
  [ADR identity is a date-prefixed slug](adrs/process/adr-ids-date-slug.md).
- README diagrams per setup (solo, team, worktrees, several agents).

### Changed

- **Workflow rule:** ADR files are named `YYYY-MM-DD-<slug>.md`; the
  slug is the identity, there is no sequence number.
- `/review-pr` runs on the local diff before `/session-close` when the
  developer reviews alone.

### Removed

- `.claude/commands/` as a distribution format. Skills are the only
  procedure format.

### Upgrade

1. Move each `.claude/commands/<name>.md` to
   `.agents/skills/<name>/SKILL.md` with the frontmatter the template
   skill of the same name carries, or copy the template skills:
   `cp -R "$tmp/cfd/templates/.agents/skills/." .agents/skills/`
   (fetch `$tmp` as in 0.3.0 step 1). Delete `.claude/commands/`.
2. `mkdir -p .claude && ln -s ../.agents/skills .claude/skills`.
3. New ADRs use the date-slug name. Existing numbered ADRs may keep
   their names; do not rename files that other documents link to.
4. In `CLAUDE.md`, replace any mention of `.claude/commands` with
   `.agents/skills`.

## [0.1.1] — 2026-09-23

Reconstructed from git history; this version was not tagged.

### Added

- `AGENTS.md` ships by default as a symlink to `CLAUDE.md`, so agents
  other than Claude Code find the index.
- README § "Using CFD with other agents": the config line per tool.
- CI named as the agent-agnostic enforcement layer in
  [enforce-rituals-with-hooks](adrs/ai-workflow/enforce-rituals-with-hooks.md).

### Changed

- The canonical essay lives in this repository; the gist is a pointer.

### Upgrade

1. `ln -s CLAUDE.md AGENTS.md` at the repository root. Never a copy.
2. Replace links to the gist with
   `https://github.com/albertomarturelo/context-first-development`.

## [0.1.0] — 2026-07-03

### Added

- First versioned release: the essay, the templates (`CLAUDE.md`,
  `docs/`, hooks, CI checks), the shareable ADR catalog, the work-tracking
  layer, `/review-pr` closing the daily cycle, and the Claude Code plugin.

### Upgrade

- Fresh install: `cp -R "$tmp/cfd/templates/. .` and follow
  `/project-init`.

[0.4.0]: https://github.com/albertomarturelo/context-first-development/compare/68b9599...main
[0.3.0]: https://github.com/albertomarturelo/context-first-development/compare/bf55ab8...68b9599
[0.2.0]: https://github.com/albertomarturelo/context-first-development/compare/c7dda28...bf55ab8
[0.1.1]: https://github.com/albertomarturelo/context-first-development/compare/a6a1e64...c7dda28
[0.1.0]: https://github.com/albertomarturelo/context-first-development/commits/a6a1e64
