import { defineConfig } from 'vitest/config';

// Integration tests run against the real Postgres in
// docker-compose.test.yml. See docs/decisions/003-integration-over-mocks.md.
//
// The default vitest.config.ts is used for unit tests with an
// `--exclude` filter; integration discovery is config-driven here
// because vitest 2.x does not expose `--include` as a CLI flag.

export default defineConfig({
  test: {
    environment: 'node',
    testTimeout: 30000,
    fileParallelism: false,
    include: ['src/**/data/**/*.test.ts'],
  },
});
