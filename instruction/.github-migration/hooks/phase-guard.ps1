# Pre-tool guard (Windows): mirrors phase-guard.sh. Fail-open — always allow on error.
$input = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($input)) { $input = '{}' }
try { $d = $input | ConvertFrom-Json } catch { echo '{}'; exit 0 }
$tool = $d.toolName
if (-not $tool) { $tool = $d.tool_name }
switch -Wildcard ($tool) {
  'edit' { $blocked = $true }
  'Edit' { $blocked = $true }
  'create' { $blocked = $true }
  'Write' { $blocked = $true }
  'str_replace_editor' { $blocked = $true }
  'apply_patch' { $blocked = $true }
  default { $blocked = $false }
}
if ($blocked -and -not (Test-Path '.github/PHASE2_APPROVED')) {
  echo '{"permissionDecision":"deny","permissionDecisionReason":"Phase 2 approval gate: present a concise draft plan (goal, files, validation, contradiction resolutions) and get developer approval before code edits. Create .github/PHASE2_APPROVED after approval, or ask for trivial-confirmation for <=3-line single-file no-behavior changes."}'
} else {
  echo '{}'
}
exit 0
