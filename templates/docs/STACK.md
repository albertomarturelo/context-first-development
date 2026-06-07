<!-- Loaded on demand for dependency / version questions. -->

# Tech Stack

## Runtime

- `<language>` `<version>`
- `<runtime / platform>` `<version>`

## Frameworks

- `<framework>` `<version>` — <one-line purpose>

## Database & Storage

- `<database>` `<version>`
- `<cache / queue / etc.>`

## External Services

- `<service>` — <purpose>

## Development Tools

- Package manager: `<npm | pnpm | uv | cargo | go mod | …>`
- Test runner: `<vitest | pytest | go test | …>`
- Linter: `<eslint | ruff | golangci-lint | …>`

<!--
When the agent asks "what version of X are we on?", it reads this file,
not `cat package.json` / `cat pyproject.toml`. Update when versions
change; cite the version in ADRs that depend on it.
-->
