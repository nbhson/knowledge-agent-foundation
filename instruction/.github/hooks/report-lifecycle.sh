#!/usr/bin/env bash
# Report lifecycle automation: archive stale active reports, delete old
# archived reports, and verify manifest/link integrity.
#
# Lifecycle (mirrors skills/report-generation/SKILL.md):
#   active (in .github/reports/<workflow-type>/) -> archived (moved to
#   .github/reports/archive/YYYY-MM/, REPORTS.md row flipped + link repointed)
#   -> deleted (row removed) only when archived file is older than
#   RETENTION_DAYS (default 90).
#
# Archive rule: an active report is archived when its age exceeds
# ARCHIVE_AFTER_DAYS (default 30). Age is measured from the file's last git
# commit time (a fresh checkout resets filesystem mtime, so commit time is
# the stable source); outside git it falls back to filesystem mtime.
# Post-merge archiving for a *merged* PR still happens via the post-merge
# skill (it needs Jira + merge-log context); this script is the background
# cleanup job — run it on demand, e.g. monthly or after merging to main.
#
# Entrypoints (where a package.json exists; otherwise call bash directly):
#   npm run reports          cleanup (archive stale >30d, delete archived >90d)
#   npm run reports:dry-run  preview without touching anything
#   npm run reports:check    manifest link/status integrity check only
#                            (CI-friendly, nonzero on failure)
#
# Run it on demand (no scheduler is configured — run manually, e.g. monthly
# or after merging to main). npm lifecycle coupling (pretest, postbuild, ...)
# is deliberately NOT used:
# lint/format/test/build run constantly during development and auto-archiving
# on every run would churn the manifest and fight the explicit post-merge
# archiving flow.
#
# Usage (direct bash, no npm):
#   bash report-lifecycle.sh [--dry-run] [--check]
#     [--archive-after-days N] [--retention-days N]
#     [--age-source git|mtime] [--root PATH]
#
# Works whether cwd is the repo root or a nested app dir (monorepo layout).
# Needs: bash 4+, GNU or BSD coreutils (date/stat/find). Git Bash on
# Windows is sufficient.
set -euo pipefail

DRY_RUN=0
CHECK_ONLY=0
ARCHIVE_AFTER_DAYS=30
RETENTION_DAYS=90
AGE_SOURCE="git"     # git | mtime (git auto-falls back to mtime when untracked)
ROOT_OVERRIDE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --check) CHECK_ONLY=1; shift ;;
    --archive-after-days) ARCHIVE_AFTER_DAYS="$2"; shift 2 ;;
    --retention-days) RETENTION_DAYS="$2"; shift 2 ;;
    --age-source) AGE_SOURCE="$2"; shift 2 ;;
    --root) ROOT_OVERRIDE="$2"; shift 2 ;;
    -h|--help) sed -n '1,/^set -euo/p' "$0"; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# Resolve the repo/app dir (the one holding .github/reports/REPORTS.md).
resolve_root() {
  if [[ -n "$ROOT_OVERRIDE" ]]; then echo "$ROOT_OVERRIDE"; return; fi
  local dir="$PWD"
  while [[ "$dir" != "/" && "$dir" != "." ]]; do
    if [[ -f "$dir/.github/reports/REPORTS.md" ]]; then echo "$dir"; return; fi
    dir="$(dirname "$dir")"
  done
  if [[ -f ".github/reports/REPORTS.md" ]]; then
    echo "$PWD"
  elif [[ -f "ClientApp/.github/reports/REPORTS.md" ]]; then
    echo "$PWD/ClientApp"
  else
    echo "Cannot locate .github/reports/REPORTS.md from $PWD" >&2; exit 1
  fi
}

ROOT="$(resolve_root)"
REPORTS_DIR="$ROOT/.github/reports"
MANIFEST="$REPORTS_DIR/REPORTS.md"
ARCHIVE_ROOT="$REPORTS_DIR/archive"
WORKFLOW_DIRS=(bug-fix new-feature refactor unit-test code-review jira-ticket-investigate)

log() { echo "[report-lifecycle] $*"; }
run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then echo "[dry-run] $*"; else "$@"; fi
}

# Portable mtime in epoch seconds (GNU stat, else BSD/macOS stat).
mtime_epoch() {
  local f="$1"
  if stat -c %Y "$f" >/dev/null 2>&1; then stat -c %Y "$f";
  else stat -f %m "$f"; fi
}

# Last git commit time of the file (epoch). Empty when untracked / not a repo.
# Robust in CI, where a fresh checkout sets every file's mtime to "now".
git_epoch() {
  local f="$1" rel
  command -v git >/dev/null 2>&1 || return 0
  git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1 || return 0
  rel="${f#"$ROOT"/}"
  git -C "$ROOT" log -1 --format=%ct -- "$rel" 2>/dev/null || true
}

# Age in whole days. Source precedence: git commit time (default), else mtime.
age_days() {
  local f="$1" now ts=""
  now="$(date +%s)"
  if [[ "$AGE_SOURCE" == "git" ]]; then
    ts="$(git_epoch "$f")"
  fi
  if [[ -z "$ts" || "$ts" == "0" ]]; then
    ts="$(mtime_epoch "$f")"
  fi
  echo $(( (now - ts) / 86400 ))
}
current_ym() { date +%Y-%m; }

ARCHIVED_COUNT=0
DELETED_COUNT=0
SKIPPED_COUNT=0
ERRORS=0

# Rewrite the manifest row for $1 (filename) to archived status pointing at
# archive/$2/$1. Table stays otherwise byte-identical (awk).
flip_row_to_archived() {
  local filename="$1" ym="$2" link="archive/$2/$1" tmp
  tmp="$(mktemp)"
  awk -v RPT_NAME="$filename" -v RPT_LINK="$link" '
    {
      line = $0
      if (index(line, "](") > 0 && index(line, RPT_NAME ")") > 0) {
        if (index(line, "legacy-active") > 0) {
          sub(/legacy-active/, "legacy-archived", line)
        } else {
          sub(/\| active \|/, "| archived |", line)
        }
        sub(/\]\([^)]*\)/, "](" RPT_LINK ")", line)
        found = 1
      }
      print line
    }
    END { exit(found ? 0 : 1) }
  ' "$MANIFEST" > "$tmp" || {
    log "WARN: no manifest row for $filename (manifest unchanged)"
    rm -f "$tmp"; ERRORS=$((ERRORS + 1)); return 1
  }
  run mv "$tmp" "$MANIFEST"
}

# Drop the manifest row whose link target ends with $1 (filename).
remove_row() {
  local filename="$1" tmp
  tmp="$(mktemp)"
  awk -v RPT_NAME="$filename" '
    { if (index($0, "](") > 0 && index($0, RPT_NAME ")") > 0) next; print }
  ' "$MANIFEST" > "$tmp"
  run mv "$tmp" "$MANIFEST"
}

archive_one() {
  local src="$1" age="$2" filename ym destdir dest
  filename="$(basename "$src")"
  ym="$(current_ym)"
  destdir="$ARCHIVE_ROOT/$ym"
  dest="$destdir/$filename"
  if [[ -e "$dest" ]]; then
    log "SKIP $filename: already exists in $destdir/ (not overwriting)"
    SKIPPED_COUNT=$((SKIPPED_COUNT + 1)); return 0
  fi
  log "ARCHIVE $filename (active, ${age}d old) -> $destdir/"
  run mkdir -p "$destdir"
  run mv "$src" "$dest"
  flip_row_to_archived "$filename" "$ym" || true
  ARCHIVED_COUNT=$((ARCHIVED_COUNT + 1))
}

delete_one() {
  local src="$1" age="$2" filename bucket
  filename="$(basename "$src")"
  log "DELETE $filename (archived, ${age}d > ${RETENTION_DAYS}d retention)"
  run rm -f "$src"
  remove_row "$filename"
  DELETED_COUNT=$((DELETED_COUNT + 1))
  bucket="$(dirname "$src")"
  if [[ -d "$bucket" && "$bucket" != "$ARCHIVE_ROOT" ]]; then
    if [[ -z "$(ls -A "$bucket")" ]]; then
      log "RMDIR empty bucket $(basename "$bucket")/"
      run rmdir "$bucket"
    fi
  fi
}


# Verify: every manifest row link resolves to a real file; statuses use the
# known vocabulary. Returns nonzero on any failure (CI-friendly).
verify_manifest() {
  local failures=0 link status
  while IFS= read -r row; do
    case "$row" in
      ''|'#'*) continue ;;                    # blank line / title / quotes
      '| #'*|'| #'*|*'[WF]'*) ;;              # table header (has # col)
      '| ---'*|'|---'*) continue ;;           # separator
      '|'*) ;;                                # table row -> validate below
      *) continue ;;                          # prose (---, How to..., etc.)
    esac
    link="$(echo "$row" | sed -n 's/.*](\([^)]*\)).*/\1/p')"
    status="$(echo "$row" | awk -F'|' 'NF>=2{gsub(/ /,"",$(NF-1)); print $(NF-1)}')"
    [[ -z "$link" ]] && continue                   # non-row line
    [[ -z "$status" ]] && continue                 # not a manifest row
    case "$status" in
      active|archived|legacy-active|legacy-archived) ;;
      *) log "FAIL: unknown status '$status' in row: $row"
         failures=$((failures + 1)); continue ;;
    esac
    if [[ ! -f "$REPORTS_DIR/$link" ]]; then
      log "FAIL: broken link '$link' in row: $row"
      failures=$((failures + 1))
    fi
    case "$link" in
      archive/*) [[ "$status" == *archived ]] || {
        log "FAIL: archive link with non-archived status: $row"
        failures=$((failures + 1)); } ;;
      *) [[ "$status" == active || "$status" == legacy-active ]] || {
        log "FAIL: workflow link with non-active status: $row"
        failures=$((failures + 1)); } ;;
    esac
  done < "$MANIFEST"
  if [[ "$failures" -gt 0 ]]; then
    log "verify FAILED: $failures problem(s)"
    return 1
  fi
  log "verify OK: all manifest links resolve, statuses consistent"
}


log "root=$ROOT archive_after=${ARCHIVE_AFTER_DAYS}d retention=${RETENTION_DAYS}d age_source=$AGE_SOURCE dry_run=$DRY_RUN check=$CHECK_ONLY"

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  verify_manifest
  exit $?
fi

# Step 1: archive stale active reports.
for wf in "${WORKFLOW_DIRS[@]}"; do
  dir="$REPORTS_DIR/$wf"
  [[ -d "$dir" ]] || continue
  while IFS= read -r -d '' f; do
    age="$(age_days "$f")"
    if [[ "$age" -ge "$ARCHIVE_AFTER_DAYS" ]]; then
      archive_one "$f" "$age"
    else
      SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    fi
  done < <(find "$dir" -maxdepth 1 -type f -name '*.md' -print0)
done

# Step 2: delete archived reports past retention.
if [[ -d "$ARCHIVE_ROOT" ]]; then
  while IFS= read -r -d '' f; do
    age="$(age_days "$f")"
    if [[ "$age" -ge "$RETENTION_DAYS" ]]; then
      delete_one "$f" "$age"
    else
      SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    fi
  done < <(find "$ARCHIVE_ROOT" -type f -name '*.md' -print0)
fi

# Step 3: verify manifest integrity after mutations.
if [[ "$DRY_RUN" -eq 0 ]]; then
  verify_manifest || ERRORS=$((ERRORS + 1))
else
  log "dry-run: skipping post-run verify (no changes were made)"
fi

log "done: archived=$ARCHIVED_COUNT deleted=$DELETED_COUNT skipped(fresh)=$SKIPPED_COUNT errors=$ERRORS"
[[ "$ERRORS" -eq 0 ]]
