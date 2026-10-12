#!/usr/bin/env bash
# Pre-tool guard: block code edits before Phase 2 plan approval (non-trivial).
# Input (stdin JSON): { sessionId, timestamp, cwd, toolName, toolArgs }
# Output: {} to allow, or {"permissionDecision":"deny","permissionDecisionReason":"..."} to block.
# Fail-open on any error: never block the session on guard failure.
set -uo pipefail

INPUT=$(cat 2>/dev/null || echo '{}')
# python3 | python | py -3: the Windows python.org installer provides
# `python` / `py`, not `python3` (Git Bash inherits Windows PATH).
# Still fail-open: unparseable input allows (never block on guard failure).
py_parse() {
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('toolName','') or d.get('tool_name',''))"
  elif command -v python >/dev/null 2>&1; then
    python -c "import json,sys; d=json.load(sys.stdin); print(d.get('toolName','') or d.get('tool_name',''))"
  elif command -v py >/dev/null 2>&1; then
    py -3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('toolName','') or d.get('tool_name',''))"
  else
    return 1
  fi
}
TOOL=$(echo "$INPUT" | py_parse 2>/dev/null || echo '')

case "$TOOL" in
  edit|Edit|create|Write|str_replace_editor|apply_patch)
    if [[ -f ".github/PHASE2_APPROVED" ]]; then
      echo '{}'
    else
      # NOTE: this guard cannot verify triviality (≤3-line single-file
      # no-behavior change) from tool name alone — it blocks all code-edit
      # tools until approval. Trivial work still presents a brief plan per
      # phase-2-planning.md threshold table rule 6, then the developer creates
      # .github/PHASE2_APPROVED (or confirms trivial in chat) before edits.
      echo '{"permissionDecision":"deny","permissionDecisionReason":"Phase 2 approval gate: present a concise draft plan (goal, files, validation, contradiction resolutions) and get developer approval before code edits. Create .github/PHASE2_APPROVED after approval, or ask for trivial-confirmation for <=3-line single-file no-behavior changes."}'
    fi
    ;;
  *)
    echo '{}'
    ;;
esac
exit 0
