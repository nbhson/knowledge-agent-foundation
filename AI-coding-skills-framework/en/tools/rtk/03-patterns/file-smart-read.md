# 📖 File Smart Read Pattern

**Goal**: Read files "smartly" — take signatures and structure instead of the full content. Helps the agent understand large files (1000+ lines) in just a few dozen tokens, exactly the harness "Tier 5 — Immediate Context" philosophy.

## When to Use

- The agent needs to understand the structure of a large file before editing it.
- Large repo, the agent often `cat`s whole files just to find one function.
- Exploring the codebase fast: `rtk find` + `rtk grep` + `rtk smart`.

## Commands & Reduction Levels

| Original command | RTK | Purpose | Reduction |
|------------------|-----|---------|-----------|
| `cat file.rs` | `rtk read file.rs` | Smart file reading — signatures/structure | ~60-90% |
| `cat file.rs` | `rtk read file.rs -l aggressive` | Signatures only, strip bodies | ~90%+ |
| `head file.rs` | `rtk smart file.rs` | 2-line heuristic code summary | ~95% |
| `find` | `rtk find "*.rs" .` | Compact find results | ~70% |
| `grep -r` | `rtk grep "pattern" .` | Grouped search results | ~75% |
| `diff file1 file2` | `rtk diff file1 file2` | Condensed diff (exit 1 if different) | ~75% |

## Real Example

```
# rtk read file.rs -l aggressive
File: src/harness/context.rs (1,240 lines)
  pub struct ContextManager            // L42
    fn build(&mut self, ctx: Ctx)      // L45
    fn compress(&self) -> Result       // L210
    fn limit(&self) -> TokenBudget     // L390
...
```

## Notes

- **Not equivalent to `cat`**: `rtk read` returns structure, not full content. If the agent needs the exact content (e.g., to edit a specific line), the agent should still use `cat`/`read_file` directly.
- **Harness connection**: this pattern is exactly the implementation of the "extract function signatures" technique in module `02-build-context` — only the necessary part goes into context.

---

*Back to [03 — Patterns](../03-patterns/)*
