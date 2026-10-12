#!/usr/bin/env bash
# verify-report-hash.sh — recompute the stable content-hash of every ACTIVE
# report and fail on mismatch (catches post-hash edits, e.g. adding the PR
# link without recomputing — the documented cause of HASH_MISMATCH).
#
# Usage: bash .github/hooks/verify-report-hash.sh [--root PATH] [file...]
# With file args: verify only those files (used by the pre-commit hook).
set -euo pipefail

ROOT_OVERRIDE=""
FILES=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT_OVERRIDE="$2"; shift 2 ;;
    -h|--help) sed -n '1,9p' "$0"; exit 0 ;;
    *) FILES+=("$1"); shift ;;
  esac
done

resolve_root() {
  if [[ -n "$ROOT_OVERRIDE" ]]; then echo "$ROOT_OVERRIDE"; return; fi
  local dir="$PWD"
  while [[ "$dir" != "/" && "$dir" != "." ]]; do
    if [[ -f "$dir/.github/reports/REPORTS.md" ]]; then echo "$dir"; return; fi
    dir="$(dirname "$dir")"
  done
  echo "$PWD"
}
ROOT="$(resolve_root)"
REPORTS_DIR="$ROOT/.github/reports"
MANIFEST="$REPORTS_DIR/REPORTS.md"

sha12() {
  if command -v sha256sum >/dev/null 2>&1; then
    grep -v 'SHA-256 Hash' "$1" | sha256sum | cut -c1-12
  else
    grep -v 'SHA-256 Hash' "$1" | shasum -a 256 | cut -c1-12
  fi
}

ERRORS=0
checked=0

check_one() {
  local file="$1" expected="$2" actual
  if [[ ! -f "$REPORTS_DIR/$file" ]]; then
    echo "[verify-hash] FAIL: missing file $file (manifest row dangles)"
    ERRORS=$((ERRORS + 1)); return
  fi
  actual="$(sha12 "$REPORTS_DIR/$file")"
  checked=$((checked + 1))
  if [[ "$actual" != "$expected" ]]; then
    echo "[verify-hash] FAIL: HASH_MISMATCH $file (manifest $expected, actual $actual)"
    echo "  Fix: recompute with: grep -v 'SHA-256 Hash' $file | shasum -a 256 | cut -c1-12"
    echo "  then update the REPORTS.md row to the new value (never one without the other)."
    ERRORS=$((ERRORS + 1))
  fi
}

if [[ "${#FILES[@]}" -gt 0 ]]; then
  for f in "${FILES[@]}"; do
    rel="${f#"$ROOT"/}"; rel="${rel#.github/reports/}"
    expected="$(grep -F "$rel)" "$MANIFEST" | awk -F'|' '{gsub(/ /,"",$(NF-1)); print $0}' | grep -oE '[0-9a-f]{12}' | head -1 || true)"
    if [[ -z "$expected" ]]; then
      echo "[verify-hash] SKIP: $rel not in REPORTS.md (new report? add its row first)"
      continue
    fi
    check_one "$rel" "$expected"
  done
else
  while IFS= read -r row; do
    case "$row" in '|'*) ;; *) continue ;; esac
    status="$(echo "$row" | awk -F'|' 'NF>=2{gsub(/ /,"",$(NF-1)); print $(NF-1)}')"
    [[ "$status" == "active" ]] || continue
    link="$(echo "$row" | sed -n 's/.*](\([^)]*\)).*/\1/p')"
    expected="$(echo "$row" | grep -oE '[0-9a-f]{12}' | head -1)"
    [[ -n "$link" && -n "$expected" ]] || continue
    check_one "$link" "$expected"
  done < "$MANIFEST"
fi

if [[ "$ERRORS" -gt 0 ]]; then
  echo "[verify-hash] FAILED: $ERRORS mismatch(es) in $checked checked"
  exit 1
fi
echo "[verify-hash] OK: $checked active report(s), all hashes match"
