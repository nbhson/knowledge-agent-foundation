# ⚡ Git Speedup Pattern

**Goal**: Cut up to 93% of output from everyday git commands (`status`, `log`, `diff`, `push`, `add`, `commit`), so the agent sees the repo state immediately instead of reading dozens of lines. (git = the version control tool that records every change to the code.)

## When to Use

- Every git working session — this is the foundational pattern to enable first.
- The agent keeps calling `git status` (what changed), `git log` (history), `git diff` (line-by-line changes) to understand repo state.

> **One-line summary:** Enable this in every session — it's the base pattern that trims the git commands the agent runs constantly.

## Commands & Reduction Levels

How to read it: each row maps one git command to its RTK version; "Output" shows what the short answer looks like; "Reduction" says how much smaller it gets (~95% means 20 lines become 1). For instance, `git push` prints 15 lines of progress text; `rtk git push` answers just `ok main`.

| Original command | RTK | Output | Reduction |
|------------------|-----|--------|-----------|
| `git status` | `rtk git status` | Compact stat, grouped by state | ~80% |
| `git log -n 10` | `rtk git log -n 10` | Hash + author + subject only | ~70% |
| `git diff` | `rtk git diff` | Reduced context, headers stripped | ~75% |
| `git add` | `rtk git add` | `ok` | ~95% |
| `git commit -m "msg"` | `rtk git commit -m "msg"` | `ok abc1234` | ~95% |
| `git push` | `rtk git push` | `ok main` | ~93% |
| `git pull` | `rtk git pull` | `ok 3 files +10 -2` | ~90% |

> **One-line summary:** Same git commands, same effects — only the output shrinks to one short line per command.

## Real Example

This side-by-side shows the same push before and after RTK: 15 lines of progress noise collapse into one confirmation line.

```
# git push (15 lines)                    # rtk git push (1 line)
Enumerating objects: 5, done.             ok main
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
...
```

## Notes

- `git diff` is compressed — if the agent needs the full diff detail, it can call `git diff` directly (without RTK) or add it to `exclude_commands` when needed. (exclude_commands = the list of commands RTK must leave untouched.)
- Pipelines like `git diff | grep foo` may be affected by the compressed format — check if the agent needs to parse the output. (Pipeline = feeding one command's output into the next command; `grep foo` = keep only lines containing "foo".)

> **One-line summary:** Use RTK git everywhere, but fall back to raw `git diff` (or an exclude) when a script needs to parse the full output.

---

*Back to [03 — Patterns](../03-patterns/)*