# Measurement: tokens-per-session on `examples/node-express`

> **TL;DR.** On the [`examples/node-express`](../examples/node-express/)
> project (32 files, 9 TypeScript source files), a CFD-style
> `/session:start` consumes **~824 tokens** against a no-CFD
> "scan-everything to have full context" baseline of **~10,519 tokens**
> — a **12.8× reduction (92.2% savings)** at session orientation.
> Reproducible via
> [`scripts/measure-session-cost.sh`](../scripts/measure-session-cost.sh).

## Why this measurement exists

The repo's README "Evidence" section previously cited only the
ballpark estimates from the [canonical methodology essay](../METHODOLOGY.md)
(500–1,500 vs 20,000–50,000 tokens). Those numbers are reasonable
order-of-magnitude estimates **but were never measured on an actual
adoption in this repository.**

This case study replaces estimation with measurement on the smallest
realistic CFD-adopted project shipped in this repo. The ratio is
expected to be **larger** on bigger codebases — but a measured 12.8×
on a 9-source-file example is the right floor to publish.

## Method

The measurement is a 60-line bash script,
[`scripts/measure-session-cost.sh`](../scripts/measure-session-cost.sh),
that:

1. Counts bytes in the **CFD session-start triad**: `CLAUDE.md` +
   `docs/CURRENT_STATUS.md` + `docs/decisions/_index.md`.
2. Counts bytes in **every source / config / doc file** the agent
   would need to read to honestly answer *"do you have full
   context?"* without CFD indices.
3. Approximates tokens as `bytes / 4`. This is **conservative** —
   real Anthropic / OpenAI / Google tokenizers give 3.0–4.5
   chars/token depending on content type. TypeScript-heavy projects
   tokenize closer to 3 chars/token, which would *increase* the
   no-CFD number and the ratio.
4. Reports the ratio.

### Reproduce it

```bash
git clone https://github.com/albertomarturelo/context-first-development.git
cd context-first-development
bash scripts/measure-session-cost.sh examples/node-express
```

Or point it at any CFD-adopted project of your own:

```bash
bash scripts/measure-session-cost.sh /path/to/your/project
```

## Result

```text
Scenario A — CFD /session:start
  CLAUDE.md                              1191 bytes ≈   297 tokens
  docs/CURRENT_STATUS.md                 1516 bytes ≈   379 tokens
  docs/decisions/_index.md                591 bytes ≈   147 tokens
  TOTAL                                  3298 bytes ≈   824 tokens

Scenario B — scan-everything (32 files)
  TOTAL                                 42079 bytes ≈ 10519 tokens

Ratio  : 12.8×
Saved  : 92.2%
```

For reference, the [methodology essay](../METHODOLOGY.md) estimates
500–1,500 tokens for session start vs 20,000–50,000 for scan-based
discovery — implying a 13×–33× range on typical projects. The 12.8×
measured here lands at the lower end, consistent with this project
being intentionally small.

## What this number does NOT prove

Honest framing matters more than the headline:

- **These are orientation tokens, not comprehension tokens.** The
  824 tokens tell the agent what the project does, what is in
  flight, and what decisions apply. They do NOT tell the agent "I
  know what line 42 of `postgres-notification-repository.ts` does."
  For specific implementation questions the agent reads the specific
  file. **The savings are about reaching ready-to-work cheaply**,
  not about completing the work for free.
- **Cumulative session tokens depend on discipline.** A CFD session
  that ends up reading 8 files unnecessarily can outspend a no-CFD
  session that reads only 3. The discipline that makes CFD cheap is
  in scoping subsequent reads to what the issue body declares as
  `Target` and `Pattern to mirror` (see
  [`adrs/process/work-units-as-external-tracker.md`](../adrs/process/work-units-as-external-tracker.md)).
- **The ratio scales with project size but not linearly.** Bigger
  projects → bigger no-CFD scan → bigger ratio. CFD's
  `/session:start` files grow modestly (more ADRs in `_index.md`,
  more bullets in `CURRENT_STATUS`), so they fall behind quickly.
  The right read of the headline is **"≥10× at any non-trivial
  size"**, not "27× on every project".
- **One project is one data point.** A CFD-shaped Node/Express
  service. Other stacks, other domain complexities, other team
  sizes give other numbers. Pull requests welcome.

## How to extend this

PRs welcome that measure tokens-per-session on:

- A larger CFD-adopted project (50+ source files).
- A non-CFD project before and after `/project:init`.
- A real-world adopter (with permission to publish the numbers).

See the [contribution layout](../CONTRIBUTING.md#contributing-a-case-study).

---

*Measured on 2026-06-07. Methodology: `bytes / 4` token approximation
via `scripts/measure-session-cost.sh`. Reproducible.*
