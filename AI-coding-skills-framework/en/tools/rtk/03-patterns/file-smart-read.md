# 📖 File Smart Read Pattern

**Goal**: Read files "smartly" — take signatures and structure instead of the full content. (A "signature" is just the function/struct name plus its parameters, without the body.) Helps the agent understand large files (1000+ lines) in just a few dozen tokens, exactly the harness "Tier 5 — Immediate Context" philosophy (put only what is needed right now into the model's context).

## When to Use

- The agent needs to understand the structure of a large file before editing it.
- Large repo, the agent often `cat`s whole files just to find one function. (`cat` = print the entire file to the screen.)
- Exploring the codebase fast: `rtk find` + `rtk grep` + `rtk smart`.

> **One-line summary:** Use this pattern when the agent needs a file's *map* — not every line of it.

## Commands & Reduction Levels

How to read this table: each row pairs a normal shell command with its RTK version, says what the RTK version does, and how much output it removes. For instance, `cat file.rs` prints the whole file; `rtk read file.rs` returns only the structure (~60-90% smaller).

| Original command | RTK | Purpose | Reduction |
|------------------|-----|---------|-----------|
| `cat file.rs` | `rtk read file.rs` | Smart file reading — signatures/structure | ~60-90% |
| `cat file.rs` | `rtk read file.rs -l aggressive` | Signatures only, strip bodies | ~90%+ |
| `head file.rs` | `rtk smart file.rs` | 2-line heuristic code summary | ~95% |
| `find` | `rtk find "*.rs" .` | Compact find results | ~70% |
| `grep -r` | `rtk grep "pattern" .` | Grouped search results | ~75% |
| `diff file1 file2` | `rtk diff file1 file2` | Condensed diff (exit 1 if different) | ~75% |

> **One-line summary:** Swap `cat`/`find`/`grep`/`diff` for their `rtk` versions and cut 60-95% of the output the agent has to read.

## Real Example

Here is what `rtk read -l aggressive` returns for a 1,240-line file: just struct and function names with line numbers (`L42` = line 42), no bodies.

```
# rtk read file.rs -l aggressive
File: src/harness/context.rs (1,240 lines)
  pub struct ContextManager            // L42
    fn build(&mut self, ctx: Ctx)      // L45
    fn compress(&self) -> Result       // L210
    fn limit(&self) -> TokenBudget     // L390
...
```

> **One-line summary:** The agent gets the file's table of contents in a handful of lines instead of 1,240.

## Notes

- **Not equivalent to `cat`**: `rtk read` returns structure, not full content. If the agent needs the exact content (e.g., to edit a specific line), the agent should still use `cat`/`read_file` directly.
- **Harness connection**: this pattern is exactly the implementation of the "extract function signatures" technique in module `02-build-context` — only the necessary part goes into context.

> **One-line summary:** Smart read is for *understanding* a file; switch back to a full read when the agent must *edit* it.

---

*Back to [03 — Patterns](../03-patterns/)*
