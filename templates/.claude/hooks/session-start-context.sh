#!/usr/bin/env bash
# SessionStart hook: make orientation automatic instead of remembered.
#
# Injects the /session:start triad (CURRENT_STATUS + decisions index)
# into the agent's context at session start, plus a staleness warning
# when the code has moved past the last CURRENT_STATUS update. stdout
# from a SessionStart hook is added to the agent's context.
#
# Claude Code-specific enforcement layer. Teams on other agents rely
# on /session:start (the command remains the portable source of truth).
# See adrs/ai-workflow/enforce-rituals-with-hooks.md.
set -uo pipefail

[ -f docs/CURRENT_STATUS.md ] || exit 0

echo "=== docs/CURRENT_STATUS.md (auto-injected at session start) ==="
cat docs/CURRENT_STATUS.md
echo ""

if [ -f docs/decisions/_index.md ]; then
  echo "=== docs/decisions/_index.md ==="
  cat docs/decisions/_index.md
  echo ""
fi

# Staleness check: warn if the last commit is >1 working day newer
# than the last commit touching CURRENT_STATUS.md.
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
  last_status=$(git log -1 --format=%ct -- docs/CURRENT_STATUS.md 2>/dev/null)
  last_commit=$(git log -1 --format=%ct 2>/dev/null)
  if [ -n "${last_commit:-}" ] && [ "${last_commit:-0}" -gt $(( ${last_status:-0} + 86400 )) ]; then
    echo "WARNING — CONTEXT MAY BE STALE: the newest commit is more than a"
    echo "day newer than the last docs/CURRENT_STATUS.md update. Verify"
    echo "claims in CURRENT_STATUS.md against 'git log' before trusting"
    echo "them, and flag the drift to the user."
  fi
fi

exit 0
