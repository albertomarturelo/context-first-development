# Shareable ADR Catalog

> Atomic, technology-neutral architecture decisions. Copy any of these into
> your repo's `docs/decisions/` and your AI agent will read the rationale
> on the next session.

This is not a library you install. It is a catalog you copy from.
**shadcn for AI context.**

## How to use one

```bash
# Browse the catalog, pick one (e.g., architecture/repository-pattern.md).
cp adrs/architecture/repository-pattern.md \
   /your/project/docs/decisions/007-repository-pattern.md

# Edit the file:
#   - Renumber to fit your repo's ADR sequence.
#   - Set the date.
#   - Replace placeholders with project-specific names.
#   - Add a paragraph at the top of "Context" that names the trigger
#     for adopting it in YOUR project.

# Add an entry to your docs/decisions/_index.md.
```

## The catalog

### Architecture

- [Repository pattern for data access](architecture/repository-pattern.md)
- [Layered (clean) architecture](architecture/layered-clean-architecture.md)

### Testing

- [Integration tests over mocks for the data layer](testing/integration-over-mocks.md)

### Process

- [Document the convention, not just the fix](process/document-corrections-not-fixes.md)
- [Atomic task instructions for AI sessions](process/atomic-task-instructions.md)
- [The session-close ritual](process/session-close-ritual.md)
- [Work units live in an external tracker with a fixed body template](process/work-units-as-external-tracker.md)
- [Trunk-based workflow with release-candidate branches](process/trunk-based-with-release-candidates.md)
- [Review the PR against context, not the code](process/pr-review-against-context.md)
- [CURRENT_STATUS is per-developer, out of version control](process/current-status-per-developer.md)

### AI Workflow

- [English as the context language](ai-workflow/english-as-context-language.md)
- [Write the ADR before implementing the decision](ai-workflow/adr-before-implementing.md)
- [Slash commands vs Claude Skills — both are valid](ai-workflow/slash-commands-vs-skills.md)
- [Short sessions over long ones](ai-workflow/short-sessions-over-long.md)
- [Distribute CFD commands as an optional plugin](ai-workflow/distribute-commands-as-plugin.md)
- [Enforce rituals with hooks and CI, not discipline](ai-workflow/enforce-rituals-with-hooks.md)

## Contributing

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the contract every
catalog entry must satisfy, and [`_TEMPLATE.md`](_TEMPLATE.md) for the
starting skeleton.
