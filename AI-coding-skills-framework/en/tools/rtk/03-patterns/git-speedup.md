# ⚡ Git Speedup Pattern

**Goal**: Cut up to 93% of output from everyday git commands (`status`, `log`, `diff`, `push`, `add`, `commit`), so the agent sees the repo state immediately instead of reading dozens of lines.

## When to Use

- Every git working session — this is the foundational pattern to enable first.
- The agent keeps calling `git status`, `git log`, `git diff` to understand repo state.

## Commands & Reduction Levels

| Original command | RTK | Output | Reduction |
|------------------|-----|--------|-----------|
| `git status` | `rtk git status` | Compact stat, grouped by state | ~80% |
| `git log -n 10` | `rtk git log -n 10` | Hash + author + subject only | ~70% |
| `git diff` | `rtk git diff` | Reduced context, headers stripped | ~75% |
| `git add` | `rtk git add` | `ok` | ~95% |
| `git commit -m "msg"` | `rtk git commit -m "msg"` | `ok abc1234` | ~95% |
| `git push` | `rtk git push` | `ok main` | ~93% |
| `git pull` | `rtk git pull` | `ok 3 files +10 -2` | ~90% |

## Real Example

```
# git push (15 lines)                    # rtk git push (1 line)
Enumerating objects: 5, done.             ok main
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
...
```

## Notes

- `git diff` is compressed — if the agent needs the full diff detail, it can call `git diff` directly (without RTK) or add it to `exclude_commands` when needed.
- Pipelines like `git diff | grep foo` may be affected by the compressed format — check if the agent needs to parse the output.

---

*Back to [03 — Patterns](../03-patterns/)*
