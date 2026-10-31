# Scaffold + diagnose + status (recommended: one binary for all three)
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop doctor .
npx @cobusgreyling/loop status .

# Legacy equivalents (forks that don't need to change)
npx @cobusgreyling/loop-init .

# Optional: scaffold an additional versioned harness
npx @cobusgreyling/loop init . --with-foundry
