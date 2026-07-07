#!/usr/bin/env bash
# PreToolUse(Bash) hook: enforce the session-close ritual at the moment
# it matters — commit time — instead of relying on discipline.
#
# If a `git commit` stages code changes but does not stage
# docs/CURRENT_STATUS.md, block the commit with an actionable message
# (exit 2 → the agent sees stderr and can fix the staging).
#
# Escape hatch: include [skip-status] in the commit command for
# commits where a status update is genuinely meaningless.
#
# Claude Code-specific enforcement layer; fails open when jq is not
# installed. See adrs/ai-workflow/enforce-rituals-with-hooks.md.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')

case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac

case "$cmd" in
  *"[skip-status]"*) exit 0 ;;
esac

staged=$(git diff --cached --name-only 2>/dev/null || true)
[ -n "$staged" ] || exit 0

code_staged=$(printf '%s\n' "$staged" \
  | grep -v '^docs/' | grep -v '^\.claude/' | grep -c . || true)
status_staged=$(printf '%s\n' "$staged" \
  | grep -c '^docs/CURRENT_STATUS\.md$' || true)

if [ "${code_staged:-0}" -gt 0 ] && [ "${status_staged:-0}" -eq 0 ]; then
  {
    echo "Session-close ritual: this commit stages code changes but not"
    echo "docs/CURRENT_STATUS.md. Context updates ship in the SAME commit"
    echo "as code (see docs/decisions/ + adrs/process/session-close-ritual.md)."
    echo "Update and stage docs/CURRENT_STATUS.md (and CONVENTIONS.md / ADRs"
    echo "if a convention or decision surfaced), or add [skip-status] to the"
    echo "commit command to bypass deliberately."
  } >&2
  exit 2
fi

exit 0
