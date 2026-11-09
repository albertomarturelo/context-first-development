#!/usr/bin/env bash
# Stamp the release version into every template an adopter copies, so an
# agent in an adopting repo can tell which CFD it has (and /cfd-upgrade
# can tell what is missing). The version has one source:
# .claude-plugin/plugin.json. validate-catalog.sh refuses a mismatch.
#
# Usage: bash scripts/stamp-version.sh          # stamp current version
#        bash scripts/stamp-version.sh --check  # exit 1 if any stamp differs
#
# Stamps:
#   templates/.agents/skills/*/SKILL.md   metadata.cfd-version: "X.Y.Z"
#   templates/CLAUDE.md                   "CFD version: X.Y.Z" in the header comment
#   templates/.claude/hooks/*.sh          "# CFD version: X.Y.Z" on line 2
#   templates/.github/workflows/*.yml     "# CFD version: X.Y.Z" on line 1

set -euo pipefail
cd "$(dirname "$0")/.."

VERSION=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' .claude-plugin/plugin.json | head -1)
[ -n "$VERSION" ] || { echo "✗ no version in .claude-plugin/plugin.json"; exit 1; }
CHECK=${1:-}
status=0

stamp_skill() {  # $1 = SKILL.md
  local f=$1 current
  current=$(awk 'NR==1&&/^---$/{fm=1;next} fm&&/^---$/{exit} fm' "$f" \
    | sed -n 's/^  cfd-version: *"\{0,1\}\([^"]*\)"\{0,1\}.*/\1/p')
  [ "$current" = "$VERSION" ] && return 0
  if [ -n "$CHECK" ]; then echo "  $f: cfd-version '${current:-none}' != $VERSION"; status=1; return 0; fi
  if [ -n "$current" ]; then
    perl -pi -e "s/^  cfd-version: .*/  cfd-version: \"$VERSION\"/" "$f"
  elif grep -q '^metadata:' "$f"; then
    perl -pi -e "\$_ .= \"  cfd-version: \\\"$VERSION\\\"\\n\" if /^metadata:/" "$f"
  else
    echo "  $f: no metadata block to stamp"; status=1; return 0
  fi
  echo "  stamped $f"
}

stamp_line() {  # $1 = file, $2 = line to hold the marker, $3 = marker prefix
  local f=$1 line=$2 prefix=$3
  if grep -q "CFD version: $VERSION" "$f"; then return 0; fi
  if [ -n "$CHECK" ]; then echo "  $f: missing 'CFD version: $VERSION'"; status=1; return 0; fi
  if grep -q "CFD version: " "$f"; then
    perl -pi -e "s/CFD version: [0-9][0-9.]*/CFD version: $VERSION/" "$f"
  else
    perl -pi -e "print \"${prefix}CFD version: $VERSION\\n\" if \$. == $line" "$f"
  fi
  echo "  stamped $f"
}

echo "CFD version $VERSION"
for f in templates/.agents/skills/*/SKILL.md; do stamp_skill "$f"; done
stamp_line templates/CLAUDE.md 2 ""
for f in templates/.claude/hooks/*.sh; do stamp_line "$f" 2 "# "; done
for f in templates/.github/workflows/*.yml; do stamp_line "$f" 1 "# "; done
grep -q "^## \[$VERSION\]" CHANGELOG.md || { echo "  CHANGELOG.md has no '## [$VERSION]' entry"; status=1; }
[ "$status" -eq 0 ] && echo "all stamps at $VERSION" || echo "✗ stamps out of date (run without --check to fix; add the CHANGELOG entry by hand)"
exit $status
