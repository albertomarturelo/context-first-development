# Telemetry quickstart

Turn on local agent telemetry in any repository: one prompt, pasted
into the agent you already use. The agent installs the
[`telemetry-report`](../templates/.agents/skills/telemetry-report/SKILL.md)
skill and builds the first report. CFD adoption is not required; the
skill only needs a git repository and `python3`.

What you get is a single HTML file on your machine: tokens per day,
per task (git branch), per skill and per session, and medians before
and after each change to the project's context files. It is built from
the session logs your agents already keep. Only counters leave those
logs; no prompt, response or file content is stored.

## Paste one prompt

Works in Claude Code, Codex, GitHub Copilot and Gemini CLI. Run it
from the repository root.

```text
You are enabling local agent telemetry in this repository with the
`telemetry-report` skill from Context-First Development (CFD):
https://github.com/albertomarturelo/context-first-development

## Step 1 — Install the skill (do this now)

The skill is a folder: SKILL.md plus a script and an HTML template.
COPY it byte for byte. Do NOT write the script yourself, and do NOT
open scripts/telemetry.py or scripts/dashboard.html: they run outside
your context, and reading them costs ~15,000 tokens for nothing.

1. Fetch and copy:
     tmp=$(mktemp -d)
     git clone --depth 1 https://github.com/albertomarturelo/context-first-development.git "$tmp/cfd"
     mkdir -p .agents/skills
     cp -R "$tmp/cfd/templates/.agents/skills/telemetry-report" .agents/skills/
   `.agents/skills/` is the path Codex, Copilot and Gemini CLI read.
2. Make it visible to Claude Code with a symlink, never a copy (a
   copy drifts):
   - no `.claude/skills` yet:
       mkdir -p .claude && ln -s ../.agents/skills .claude/skills
   - `.claude/skills` is already a symlink to `../.agents/skills`:
     nothing to do.
   - `.claude/skills` is a real directory:
       ln -s ../../.agents/skills/telemetry-report .claude/skills/telemetry-report
3. Add `.cfd/` to `.gitignore` if it is not there. The dashboard and
   its history are per-developer and never committed.
4. Confirm `python3 --version` works. `zstd` is optional; without it
   older Codex sessions are skipped and the report says how many.

Do not add anything to CLAUDE.md or AGENTS.md. Agents find the skill
through its description; a line in the index would cost tokens in
every session.

## Step 2 — Generate the report

     python3 .agents/skills/telemetry-report/scripts/telemetry.py --open

It writes `.cfd/telemetry/index.html` and prints a summary. Then:

- Relay the totals per agent, and every `note` line as plainly as the
  totals: a note is something the script could not read.
- Say which agents have data. Claude Code and Codex need nothing
  enabled. The `copilot` line says whether an OpenTelemetry file
  export exists on this machine. If this team uses GitHub Copilot in
  VS Code and it does not, tell the user the three user settings that
  start its history (`github.copilot.chat.otel.enabled: true`,
  `github.copilot.chat.otel.exporterType: "file"` and
  `github.copilot.chat.otel.outfile: "<absolute path outside the
  repo>"`, then reload the window), and that the script does not read
  that export yet. Do not change user settings yourself.
- Tell the user to re-run it at least monthly: agents delete their own
  logs (Claude Code after 30 days) and the script only keeps what it
  has seen.

## Step 3 — Publish, ONLY if the user asks for a shared report

     python3 .agents/skills/telemetry-report/scripts/telemetry.py --publish

This commits `reports/<git user.email>/<YYYY-MM>.json` to the local
`cfd-telemetry` branch without touching the checkout. Show
`git show --stat cfd-telemetry`, state what leaves the machine
(counters, the day, branch, skill and model names, the git identity;
never prompts, responses or code), and wait for an explicit yes
before running it again with `--publish --push`. Never force-push
that branch. `--anonymous` publishes under a random id instead.

NEVER publish from a public repository: the branch would show
per-person usage and git identities to everyone. The script refuses
when the forge reports the repo as public. If it warns that it cannot
tell, ask the user and do not push until they confirm the repo is
private. Do not pass `--allow-public` on your own.

Finish by listing what you installed, the summary and its gaps, and
ask whether to commit `.agents/skills/telemetry-report`, the
`.claude/skills` symlink and the `.gitignore` change so every clone
gets the same skill.
```

## After the first run

The skill is installed, so from now on ask for it by name:

| Agent | Local dashboard | Publish |
|---|---|---|
| Claude Code, Copilot | `/telemetry-report` | `/telemetry-report publish` |
| Codex | `$telemetry-report` | `$telemetry-report publish` |
| Gemini CLI | "run the telemetry-report skill" | "… and publish" |
| No agent | `python3 .agents/skills/telemetry-report/scripts/telemetry.py --open` | add `--publish`, then `--publish --push` |

It also triggers on a plain question such as "how many tokens did this
project use last week?".

## Read it in this order

1. **Context at first request.** What every session loads before any
   work. If it grows after a change to `CLAUDE.md`, that change costs
   every session.
2. **Tokens before first edit.** The orientation cost: how much the
   agent spends finding its way before it changes a file.
3. **Context changes, before vs after.** Rows with fewer than three
   sessions on a side are anecdotes.
4. **Totals, by task and by skill.** How much was spent, and where.

## For a team

Every developer runs the same prompt once; the skill is committed, so
later clones already have it. Each person publishes their own report
to the `cfd-telemetry` branch of a **private** repository; the script
refuses public ones. One file per person and month, so the branch
never conflicts, and a task shared by several people adds up
per person and per agent. The file format is documented in
[`report-schema.md`](../templates/.agents/skills/telemetry-report/references/report-schema.md).

A central reader that merges that branch across repositories is not
shipped yet. Per-person numbers explain what a task cost; they are
not a ranking.
