#!/usr/bin/env bash
# sync-routing.sh — render the workflow→phases routing table in
# .github/phases/README.md from the SOLE owner
# .github/phases/session.json → workflow_phase_config.
#
# Usage:
#   bash .github/hooks/sync-routing.sh          # rewrite the marked block
#   bash .github/hooks/sync-routing.sh --check  # fail if the block is stale (CI)
set -euo pipefail

CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SESSION="$ROOT/.github/phases/session.json"
README="$ROOT/.github/phases/README.md"

# Windows 11 note: the python.org installer provides `python` / `py`, not
# `python3`. Auto-pick whatever exists (Git Bash inherits Windows PATH).
pick_python() {
  if command -v python3 >/dev/null 2>&1; then echo "python3";
  elif command -v python >/dev/null 2>&1; then echo "python";
  elif command -v py >/dev/null 2>&1; then echo "py -3";
  else echo "python3"; fi
}
# shellcheck disable=SC2209 (word-splitting "py -3" apart is intended)
PYTHON="$(pick_python)"

BLOCK="$($PYTHON - "$SESSION" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
w = d['workflow_phase_config']['workflows']
PNUM = {'phase-1-understanding': 'P1', 'phase-2-planning': 'P2',
        'phase-3-execution-formatting': 'P3', 'phase-4-validation-pr': 'P4',
        'phase-5-report-generation': 'P5'}
rows = []
for name in sorted(w):
    skip = w[name].get('skip_phases', [])
    if not skip:
        phases = 'P1→P5 (full)'
    else:
        skipped = ', '.join(PNUM.get(s, s) for s in skip)
        phases = f'P1+P5 only (skips {skipped})'
    rows.append(f'| `{name}` | {phases} |')
print('\n'.join(rows))
PY
)"

START='<!-- ROUTING:START (generated from session.json — do not edit by hand; run bash .github/hooks/sync-routing.sh) -->'
END='<!-- ROUTING:END -->'
NEWBLOCK="$START
| Workflow | Phases |
|---|---|
$BLOCK
$END"

if $PYTHON - "$README" "$START" "$END" <<'PY'; then
import sys
readme, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(readme).read()
assert start in s and end in s, 'routing markers missing in README'
print('markers ok')
PY
  :
fi

if [[ "$CHECK" -eq 1 ]]; then
  EXPECTED="$BLOCK"
  CURRENT="$($PYTHON - "$README" <<'PY'
import sys
s = open(sys.argv[1]).read()
block = s.split('<!-- ROUTING:START', 1)[1].split('<!-- ROUTING:END -->', 1)[0]
lines = [l for l in block.splitlines() if l.startswith('|')]
print('\n'.join(lines[2:]))  # drop the header + separator rows
PY
)"
  if [[ "$EXPECTED" == "$CURRENT" ]]; then
    echo "[sync-routing] OK: README routing block matches session.json"
  else
    echo "[sync-routing] FAIL: README routing block stale — run bash .github/hooks/sync-routing.sh"
    echo "--- expected (session.json) ---"; echo "$EXPECTED"
    echo "--- current (README.md) ---"; echo "$CURRENT"
    exit 1
  fi
  exit 0
fi

$PYTHON - "$README" "$NEWBLOCK" <<'PY'
import sys, re
readme, newblock = sys.argv[1], sys.argv[2]
s = open(readme).read()
pat = re.compile(r'<!-- ROUTING:START.*?<!-- ROUTING:END -->', re.S)
assert pat.search(s), 'routing markers missing in README'
open(readme, 'w').write(pat.sub(newblock, s, count=1))
print('[sync-routing] README routing block regenerated from session.json')
PY
