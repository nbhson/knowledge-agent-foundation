#!/usr/bin/env bash
# check-refs.sh — verify every `.github/...` reference in markdown/JSON points
# to an existing file. CI-friendly: nonzero on failure.
#
# Usage:
#   bash .github/hooks/check-refs.sh [--fix-manifest]
#
# --fix-manifest: re-sort .github/reports/REPORTS.md rows by Date then File
# and renumber 1..N (keeps manifest readable without hand-editing).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
GITHUB="$ROOT/.github"
ERRORS=0

log() { echo "[check-refs] $*"; }

# 1. Collect `.github/<path>` refs from md/json (strip line/col anchors, quotes, parens).
# Skips: this script itself, archived historical reports (frozen in time),
# and placeholder patterns (YYYY, MM, N-, <...>, XXX).
check_file_refs() {
  local f refs ref
  while IFS= read -r -d '' f; do
    case "$f" in
      */hooks/check-refs.sh|*/reports/archive/*) continue ;;
    esac
    refs="$(grep -oE '\.github/[A-Za-z0-9._/+-]+' "$f" 2>/dev/null || true)"
    [[ -z "$refs" ]] && continue
    while IFS= read -r ref; do
      # strip trailing punctuation / anchors / globs
      ref="$(echo "$ref" | sed -E 's/[#):,`\*.]+$//; s/\.\.\.$//')"
      [[ -z "$ref" || "$ref" == ".github" ]] && continue
      case "$ref" in
        *"<"*|*"*"*|*"..."*|*YYYY*|*MM*|*phase-N-*|*XXXX*|*ci.yml*) continue ;; # placeholders / examples, not paths
      esac
      # Runtime markers (gitignored, created per-task, never committed).
      case "$ref" in
        .github/PHASE2_APPROVED|implementation_plan.md) continue ;;
      esac
      if [[ ! -e "$ROOT/$ref" ]]; then
        log "FAIL: $f → missing $ref"
        ERRORS=$((ERRORS + 1))
      fi
    done <<< "$refs"
  done < <(find "$GITHUB" -type f \( -name '*.md' -o -name '*.json' \) -print0)
}

# 2. No stale `*.hook.md` references may remain (renamed 2026-10-12).
# Excludes this script's own check + the historical rename note in phases/README.
check_hookmd() {
  local hits
  hits="$(grep -rn '\.hook\.md' "$GITHUB" 2>/dev/null | grep -v 'hooks/check-refs.sh' | grep -v 'Renamed from' || true)"
  if [[ -n "$hits" ]]; then
    log "FAIL: stale *.hook.md references remain:"
    echo "$hits"
    ERRORS=$((ERRORS + 1))
  fi
}

# 3. REPORTS.md: every link resolves; no duplicate rows per file.
check_manifest() {
  bash "$GITHUB/hooks/report-lifecycle.sh" --check || ERRORS=$((ERRORS + 1))
  local dups
  dups="$(grep -oE '\[[^]]*\]\([^)]+\)' "$GITHUB/reports/REPORTS.md" | sort | uniq -d || true)"
  if [[ -n "$dups" ]]; then
    log "FAIL: duplicate manifest rows for: $dups"
    ERRORS=$((ERRORS + 1))
  fi
}

fix_manifest() {
  # Windows 11 note: the python.org installer provides `python` / `py`, not
  # `python3`. Auto-pick whatever exists (Git Bash inherits Windows PATH).
  local py
  if command -v python3 >/dev/null 2>&1; then py="python3";
  elif command -v python >/dev/null 2>&1; then py="python";
  elif command -v py >/dev/null 2>&1; then py="py -3";
  else py="python3"; fi
  # shellcheck disable=SC2086 (word-splitting "py -3" apart is intended)
  $py - "$GITHUB/reports/REPORTS.md" <<'EOF'
import re, sys
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
rows = [l for l in lines if re.match(r'^\| \d+ \|', l)]
def key(r):
    cols = [c.strip() for c in r.split('|')]
    return (cols[4], cols[5])
rows_sorted = sorted(rows, key=key)
out = [re.sub(r'^\| \d+ \|', f'| {i} |', r) for i, r in enumerate(rows_sorted, 1)]
start = next(i for i, l in enumerate(lines) if re.match(r'^\| \d+ \|', l))
end = max(i for i, l in enumerate(lines) if re.match(r'^\| \d+ \|', l))
open(p, 'w').writelines(lines[:start] + out + lines[end+1:])
print(f'[check-refs] manifest re-sorted: {len(out)} rows')
EOF
}

if [[ "${1:-}" == "--fix-manifest" ]]; then
  fix_manifest
fi

check_file_refs
check_hookmd
check_manifest

if [[ "$ERRORS" -gt 0 ]]; then
  log "FAILED: $ERRORS problem(s)"
  exit 1
fi
log "OK: all .github refs resolve, no stale hook.md, manifest consistent"
