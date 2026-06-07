#!/usr/bin/env bash
# Measure the token cost of /session:start (CFD-style index reads)
# vs the cost of scanning the whole project to "have full context".
#
# Usage:
#   bash scripts/measure-session-cost.sh [project-dir]
#
# Token approximation: bytes / 4. Conservative for a mix of prose
# (markdown) and code (TypeScript / Python / Kotlin / Go / Rust).
# Real Anthropic / OpenAI / Google tokenizers give 3.0–4.5
# chars/token depending on content type — code-heavy projects skew
# lower (worse for the no-CFD scan number), prose-heavy higher. The
# bytes/4 estimate is intentionally simple and reproducible without
# external tooling (no Python, no npm, no anything).

set -uo pipefail

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

if [ ! -f CLAUDE.md ]; then
  echo "✗ No CLAUDE.md found in $PROJECT_DIR."
  echo "  This script measures CFD-adopted projects."
  echo "  Run /project:init first, or point at a CFD-adopted dir."
  exit 1
fi

# Scenario A: CFD /session:start triad.
cfd_files=(CLAUDE.md docs/CURRENT_STATUS.md docs/decisions/_index.md)

echo "=== Scenario A — CFD /session:start ==="
cfd_total=0
for f in "${cfd_files[@]}"; do
  if [ -f "$f" ]; then
    bytes=$(wc -c < "$f" | tr -d ' ')
    tokens=$((bytes / 4))
    cfd_total=$((cfd_total + bytes))
    printf "  %-44s %6d bytes  ≈ %5d tokens\n" "$f" "$bytes" "$tokens"
  else
    printf "  %-44s %s\n" "$f" "(missing — skip)"
  fi
done
cfd_tokens=$((cfd_total / 4))
printf "  %-44s %6d bytes  ≈ %5d tokens\n" "TOTAL (A)" "$cfd_total" "$cfd_tokens"
echo ""

# Scenario B: scan everything the agent would need to read to
# honestly answer "do you have full context?" without CFD indices.
echo "=== Scenario B — scan everything ==="
all_files=$(find . -type f \
  \( -name "*.ts"  -o -name "*.tsx"  -o -name "*.js"   -o -name "*.jsx" \
     -o -name "*.py" -o -name "*.go" -o -name "*.rs"  -o -name "*.kt" \
     -o -name "*.swift" -o -name "*.java" -o -name "*.rb" \
     -o -name "*.md" -o -name "*.json" -o -name "*.sql" \
     -o -name "*.yml" -o -name "*.yaml" -o -name "*.toml" \) \
  -not -path './node_modules/*' \
  -not -path './.git/*' \
  -not -path './dist/*' \
  -not -path './build/*' \
  -not -path './target/*' \
  -not -path './.venv/*' \
  -not -path './venv/*' \
  -not -name 'package-lock.json' \
  -not -name 'yarn.lock' \
  -not -name 'pnpm-lock.yaml' \
  -not -name 'Cargo.lock' \
  -not -name 'poetry.lock' \
  -not -name 'uv.lock' \
  | sort)

file_count=$(echo "$all_files" | grep -c .)
all_bytes=$(echo "$all_files" | xargs cat 2>/dev/null | wc -c | tr -d ' ')
all_tokens=$((all_bytes / 4))
printf "  %-44s %d\n" "Files scanned:" "$file_count"
printf "  %-44s %6d bytes  ≈ %5d tokens\n" "TOTAL (B)" "$all_bytes" "$all_tokens"
echo ""

# Result.
if [ "$cfd_tokens" -gt 0 ]; then
  ratio=$(awk "BEGIN { printf \"%.1f\", $all_tokens / $cfd_tokens }")
  savings=$(awk "BEGIN { printf \"%.1f\", (1 - $cfd_tokens / $all_tokens) * 100 }")
  echo "=== Result ==="
  printf "  CFD /session:start  ≈ %5d tokens\n" "$cfd_tokens"
  printf "  scan-everything     ≈ %5d tokens\n" "$all_tokens"
  printf "  ratio               = %sx\n" "$ratio"
  printf "  tokens saved        = %s%%\n" "$savings"
  echo ""
  echo "Methodology: bytes/4 ≈ tokens (conservative). Real tokenizers"
  echo "give 3.0–4.5 chars/token depending on content. The ratio is"
  echo "the headline; the absolute numbers are approximations."
fi
