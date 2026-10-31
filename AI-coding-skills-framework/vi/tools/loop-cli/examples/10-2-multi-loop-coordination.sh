# Developer A chạy loop trong worktree riêng
loop-worktree create --run-id fix-123 --pattern post-merge-cleanup

# Developer B chạy loop khác — lock tránh conflict
loop-worktree lock --scope refs/heads/main

# Cả hai kết thúc → gate check trước khi auto-merge
loop gate check --action auto-merge --paths src/,tests/
