#!/usr/bin/env bash
#
# validate-links.sh
#
# Validates that every path referenced inside the .github/ framework
# (hooks, skills, templates, knowledge) actually exists on disk.
# Prevents broken links such as the previous `.github/report/` typo.
#
# Usage: bash .github/scripts/validate-links.sh
# Exit code 0 = all references valid. Non-zero = broken references found.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FRAMEWORK_DIR="$ROOT/ai-tools/.github"

BROKEN=0

# Collect every path that starts with .github/ or /.github/
# from markdown files inside the framework, then dedupe.
REFS="$(grep -rhoE '(/)?\.github/[A-Za-z0-9_./-]+' "$FRAMEWORK_DIR" --include='*.md' \
  | sed -E 's/^\/?\.github\//.github\//' \
  | sort -u)"

while IFS= read -r ref; do
  [ -n "$ref" ] || continue

  # Allow wildcard-ish/placeholder patterns (e.g., .github/reports/*.ctx.md)
  case "$ref" in
    *'*'*|*'['*|*']'*|*'{'*|*'}'*|*'<'*|*'>'*|*'?'*|*'...'*) continue ;;
  esac

  # Allow paths to directories that may not exist yet (e.g., reports/ before first use)
  case "$ref" in
    .github/reports/*) continue ;;
  esac

  if [[ ! -e "$ROOT/$ref" && ! -e "$FRAMEWORK_DIR/${ref#.github/}" ]]; then
    echo "BROKEN: $ref"
    BROKEN=1
  fi
done <<< "$REFS"

# Validate session.json is valid JSON and every hookFile exists.
if ! python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$FRAMEWORK_DIR/hooks/session.json" 2>/dev/null; then
  echo "BROKEN: hooks/session.json is not valid JSON"
  BROKEN=1
else
  while IFS= read -r hookfile; do
    [ -n "$hookfile" ] || continue
    if [[ ! -e "$FRAMEWORK_DIR/${hookfile#.github/}" ]]; then
      echo "BROKEN: session.json references missing hook: $hookfile"
      BROKEN=1
    fi
  done < <(python3 -c "
import json,sys
data=json.load(open(sys.argv[1]))
for section in data.get('hooks', {}).values():
    for h in section:
        if 'hookFile' in h:
            print(h['hookFile'])
" "$FRAMEWORK_DIR/hooks/session.json")
fi

if [[ $BROKEN -eq 0 ]]; then
  echo "OK: all framework references are valid."
else
  echo "ERROR: broken references found. Fix them before committing."
  exit 1
fi