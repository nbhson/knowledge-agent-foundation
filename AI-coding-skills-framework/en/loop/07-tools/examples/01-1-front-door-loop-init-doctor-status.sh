# Front door (recommended) — one binary for init + doctor + status
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .

# Legacy equivalent (still supported — forks don't need to change)
npx @cobusgreyling/loop-init .

# Optional: scaffold a versioned harness too (harness-foundry)
npx @cobusgreyling/loop init . --with-foundry
