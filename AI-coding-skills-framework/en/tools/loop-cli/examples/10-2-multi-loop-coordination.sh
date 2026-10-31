# Developer A runs a loop in their own worktree
loop-worktree create --run-id fix-123 --pattern post-merge-cleanup

# Developer B runs a different loop — lock avoids conflicts
loop-worktree lock --scope refs/heads/main

# Both finish → gate check before auto-merge
loop gate check --action auto-merge --paths src/,tests/
