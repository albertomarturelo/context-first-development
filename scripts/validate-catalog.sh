#!/usr/bin/env bash
# Validate the shareable ADR catalog integrity.
# Implements the contract from the source vault's ADR-003 and the
# no-AI-attribution rule from CLAUDE.md.
#
# Run locally:  bash scripts/validate-catalog.sh
# Runs in CI:   .github/workflows/validate-catalog.yml

set -uo pipefail

cd "$(dirname "$0")/.."

FAILED=0
WARN=0

err()  { printf '  \033[31m✗\033[0m %s\n' "$1"; FAILED=$((FAILED+1)); }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; WARN=$((WARN+1)); }

catalog_files() {
  find adrs/architecture adrs/testing adrs/process adrs/ai-workflow \
    -maxdepth 1 -name '*.md' 2>/dev/null | sort
}

REQUIRED_SECTIONS=(
  "## Status"
  "## When to Use"
  "## Context"
  "## Decision"
  "## Alternatives Considered"
  "## Verifiable Consequences"
  "## Trade-offs"
)

echo "== Catalog integrity =="

# 1. Line count cap.
echo ""
echo "1. Line count ≤100 per shareable ADR"
while IFS= read -r f; do
  lines=$(wc -l < "$f" | tr -d ' ')
  if [ "$lines" -gt 100 ]; then
    err "$f has $lines lines (>100)"
  fi
done < <(catalog_files)

# 2. Required sections.
echo ""
echo "2. Required sections per ADR-003"
while IFS= read -r f; do
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -qF "$section" "$f"; then
      err "$f missing section: $section"
    fi
  done
done < <(catalog_files)

# 3. Token budget annotation.
echo ""
echo "3. Token budget annotation in head of file"
while IFS= read -r f; do
  if ! head -3 "$f" | grep -qE "[Tt]oken budget"; then
    err "$f missing token budget annotation in first 3 lines"
  fi
done < <(catalog_files)

# 4. Index sync.
echo ""
echo "4. Index sync: catalog ↔ adrs/_index.md"
while IFS= read -r f; do
  rel=${f#adrs/}
  if ! grep -qF "$rel" adrs/_index.md; then
    err "$f not listed in adrs/_index.md"
  fi
done < <(catalog_files)

while IFS= read -r link; do
  link=${link#\(}
  link=${link%\)}
  if [ ! -f "adrs/$link" ]; then
    err "adrs/_index.md links to non-existent: adrs/$link"
  fi
done < <(grep -oE '\([a-z][a-z-]*/[a-z][a-z0-9-]*\.md\)' adrs/_index.md)

# 5. AI-tool attribution forbidden.
# Match only column-0 occurrences. Real commit trailers and PR
# footers sit at column 0; markdown mentions of the same strings
# (as rules to enforce in `/review-pr` checklists, for example)
# are always indented or inside backticks. This pattern catches
# the real thing without false positives on rule documentation.
echo ""
echo "5. No AI-tool attribution in shipped artifacts"
ATTRIB_HITS=$(grep -rEn '^Co-Authored-By: Claude|^🤖 Generated with Claude|^Generated with Claude Code' \
  adrs/ templates/ case-studies/ examples/ 2>/dev/null || true)
if [ -n "$ATTRIB_HITS" ]; then
  err "AI-tool attribution found:"
  echo "$ATTRIB_HITS" | sed 's/^/    /'
fi

# Summary.
echo ""
echo "== Summary =="
echo "  Failures: $FAILED"
echo "  Warnings: $WARN"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
