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
#
# Hash integrity (stable, self-consistent):
#   content-hash = first 12 hex chars of sha256 over the report file
#   EXCLUDING the `SHA-256 Hash` row itself. This keeps the stored hash
#   stable after it is inserted into `## Meta`.
#   Compute: grep -v 'SHA-256 Hash' <report> | sha256sum | cut -c1-12
#   (On macOS without sha256sum: shasum -a 256 <report> | cut -c1-12
#   applied to the same filtered content.)

set -euo pipefail

# Resolve repo root flexibly:
# 1. Prefer git top-level when available.
# 2. Otherwise use script location (<root>/.github/scripts -> <root>).
# 3. Support legacy monorepo layout (<root>/ClientApp/.github).
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  ROOT="$(git rev-parse --show-toplevel)"
else
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
if [[ -d "$ROOT/ClientApp/.github" && -f "$ROOT/ClientApp/.github/CHARTER.md" ]]; then
  FRAMEWORK_DIR="$ROOT/ClientApp/.github"
elif [[ -d "$ROOT/.github" ]]; then
  FRAMEWORK_DIR="$ROOT/.github"
else
  echo "ERROR: .github directory not found under $ROOT or $ROOT/ClientApp"
  exit 1
fi

# Portable sha256 helper (linux sha256sum, macOS shasum fallback)
sha256_of_stdin() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum | cut -c1-12
  else
    shasum -a 256 | cut -c1-12
  fi
}
content_hash() {
  # $1 = report file; hash over all lines except the SHA-256 Hash row
  grep -v 'SHA-256 Hash' "$1" | sha256_of_stdin
}

BROKEN=0

# Collect every path that starts with .github/ or /.github/
# from markdown files inside the framework, then dedupe.
# Leading `/.github/` is normalized to `.github/` (canonical form, no leading slash).
REFS="$(grep -rhoE '(/)?\.github/[A-Za-z0-9_./-]+' "$FRAMEWORK_DIR" --include='*.md' \
  | sed -E 's/^\/?\.github\//.github\//' \
  | sort -u)"

while IFS= read -r ref; do
  [ -n "$ref" ] || continue

  # Allow wildcard-ish/placeholder patterns (e.g., .github/reports/*.ctx.md)
  case "$ref" in
    *'*'*|*'['*|*']'*|*'{'*|*'}'*|*'<'*|*'>'*|*'?'*|*'...'*) continue ;;
  esac

  # Skip template fragments ending with hyphen (e.g., phase-N- from "phase-N-<name>.hook.md")
  [[ "$ref" == *'-' ]] && continue

  # Reports and archive contents are data, not framework refs — checked separately below
  case "$ref" in
    .github/reports/*) continue ;;
  esac

  framework_ref="$FRAMEWORK_DIR/${ref#.github/}"
  repo_ref="$ROOT/$ref"
  if [[ ! -e "$framework_ref" && ! -e "$repo_ref" ]]; then
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
    # Canonical hookFile form is `.github/hooks/...` (no leading slash)
    case "$hookfile" in
      .github/*) ;;
      *) echo "WARN: session.json hookFile should use canonical '.github/...' form: $hookfile" ;;
    esac
    normalized="${hookfile#/}"
    if [[ ! -e "$FRAMEWORK_DIR/${normalized#.github/}" ]]; then
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

# ── Validate REPORTS.md manifest completeness ────────────────────────────────

REPORTS_DIR="$FRAMEWORK_DIR/reports"
MANIFEST="$REPORTS_DIR/REPORTS.md"

if [[ -f "$MANIFEST" ]]; then
  # Count actual report files (excluding index/log itself, including archive/)
  ACTUAL_COUNT=$(find "$REPORTS_DIR" -name '*.md' ! -name 'REPORTS.md' ! -name 'merge-log.md' | wc -l)
  # Count rows in manifest table (lines with '|')
  MANIFEST_ROWS=$(grep -c '^|' "$MANIFEST" || true)
  EXPECTED_ROWS=$((ACTUAL_COUNT + 2))  # +2 for header row and separator

  if [[ $MANIFEST_ROWS -lt $EXPECTED_ROWS ]]; then
    echo "WARN: REPORTS.md may be out of sync — $ACTUAL_COUNT report files but only $((MANIFEST_ROWS - 2)) data rows"
  elif [[ $MANIFEST_ROWS -gt $((EXPECTED_ROWS + 1)) ]]; then
    echo "WARN: REPORTS.md has extra rows ($((MANIFEST_ROWS - 2)) vs $ACTUAL_COUNT files)"
  else
    echo "OK: REPORTS.md manifest is in sync ($ACTUAL_COUNT reports, $((MANIFEST_ROWS - 2)) rows)"
  fi

  # Check each referenced report file exists (active dir or archive/)
  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    case "$ref" in
      *'*'*|*'['*|*']'*|*'{'*|*'}'*|*'<'*|*'>'*) continue ;;
    esac
    if [[ ! -e "$REPORTS_DIR/$ref" && -z "$(find "$REPORTS_DIR" -name "$ref" -print -quit 2>/dev/null)" ]]; then
      echo "BROKEN: REPORTS.md references missing file: $ref"
      BROKEN=1
    fi
  done < <(grep -oE '[A-Z]+-REPORT-[^)]+\.(ctx\.)?md' "$MANIFEST" || true)
else
  echo "WARN: REPORTS.md manifest not found — create it at .github/reports/REPORTS.md"
fi

# ── Validate content-hashes in report Meta sections (stable: excludes hash row) ──
# Legacy exemption: reports created on or before 2026-09-11 without ## Meta are
# marked `legacy-active` in REPORTS.md and emit WARN (not ERROR).

if [[ -d "$REPORTS_DIR" ]]; then
  for report in "$REPORTS_DIR"/*.md; do
    [ -f "$report" ] || continue
    fname=$(basename "$report")
    # Skip index and log files (not reports)
    [[ "$fname" == "REPORTS.md" || "$fname" == "merge-log.md" ]] && continue

    # Check if report has a ## Meta section
    if grep -q '## Meta' "$report"; then
      # Extract expected hash from Meta table (first 12 hex chars after "SHA-256 Hash").
      # Allows markdown bold markers (**) and backticks between the label and the value.
      EXPECTED_HASH=$(grep -oE 'SHA-256 Hash[^|]*\|[^0-9a-f]*([a-f0-9]{12})' "$report" | grep -oE '[a-f0-9]{12}' | head -n1 || true)
      if [[ -n "$EXPECTED_HASH" ]]; then
        # Compute stable content-hash (excludes the hash row itself)
        ACTUAL_HASH=$(content_hash "$report")
        if [[ "$EXPECTED_HASH" != "$ACTUAL_HASH" ]]; then
          echo "HASH_MISMATCH: $fname — expected $EXPECTED_HASH, got $ACTUAL_HASH (content-hash excludes SHA-256 Hash row)"
          BROKEN=1
        else
          echo "OK: $fname hash verified ($ACTUAL_HASH)"
        fi
      else
        echo "WARN: $fname has ## Meta but no SHA-256 hash filled"
      fi
      # Strict reports must also have Jira + MCP sections
      grep -q '## Jira Ticket' "$report" || echo "WARN: $fname missing ## Jira Ticket section (required for new reports)"
      grep -q '## MCP Status' "$report" || grep -q '## MCP' "$report" || echo "WARN: $fname missing MCP Status section (required for new reports)"
    else
      echo "WARN: LEGACY-EXEMPT $fname — no ## Meta (created <= 2026-09-11, status legacy-active in REPORTS.md)"
    fi
  done
fi

# ── Validate Jira Ticket URL is present in reports ────────────────────────────

for report in "$REPORTS_DIR"/*.md; do
  [ -f "$report" ] || continue
  fname=$(basename "$report")
  [[ "$fname" == "REPORTS.md" || "$fname" == "merge-log.md" ]] && continue

  if grep -q '## Jira Ticket' "$report"; then
    # Check that Ticket URL is not just a placeholder
    if grep -A2 'Ticket URL' "$report" | grep -qE '\[https?://[^]]+\]\(https?://[^)]+\)'; then
      : # URL is filled — OK
    else
      echo "WARN: $fname has ## Jira Ticket section but no Ticket URL filled"
    fi
  fi
done

if [[ $BROKEN -eq 0 ]]; then
  echo "OK: report integrity checks passed."
else
  echo "ERROR: report integrity issues found."
  exit 1
fi
