# 🏗️ Build & Lint Compact Pattern

**Goal**: Compress build/lint output — keep only important errors and warnings, grouped by file/rule. Helps the agent see "what's broken" instead of reading hundreds of lines of compiler output. (Build = turning source code into a runnable program; lint = automatic checks for code style and common mistakes.)

## When to Use

- Frequent builds (`cargo build` = build a Rust project, `npm run build`, `next build`).
- Lint/type-check after every code edit (`tsc` = TypeScript's type checker, `ruff` = a fast Python linter, `clippy` = Rust's linter, `eslint` = a JavaScript linter).
- CI is red due to compile/lint errors. (CI = the automated build-and-test pipeline that runs on every commit; "red" = the pipeline is failing.)

> **One-line summary:** Use it whenever build or lint output floods the screen — after every edit, and especially when CI is red.

## Commands & Reduction Levels

How to read it: each row maps one original command to its RTK version; "Output" says what the compressed result looks like; "Reduction" says how much smaller it gets (~85% means the output is cut to roughly 15% of the original). For instance, `tsc` output becomes a list of TypeScript errors grouped by file, about 15% of its original size.

| Original command | RTK | Output | Reduction |
|------------------|-----|--------|-----------|
| `cargo build` | `rtk cargo build` | Compact build output | ~80% |
| `cargo clippy` | `rtk cargo clippy` | Compact clippy | ~80% |
| `tsc` | `rtk tsc` | TS errors grouped by file | ~85% |
| `eslint` | `rtk lint` | Grouped by rule/file | ~80% |
| `ruff check` | `rtk ruff check` | JSON, grouped by rule/file | ~80% |
| `golangci-lint run` | `rtk golangci-lint run` | JSON | ~85% |
| `rubocop` | `rtk rubocop` | JSON | ~60%+ |
| `next build` | `rtk next build` | Compact | ~75% |
| `prettier --check .` | `rtk prettier --check .` | Files needing formatting | ~75% |
| `sbt compile` | `rtk sbt compile` | Compilation errors only | ~75% |

> **One-line summary:** Every command keeps its behavior; only the output shrinks — to just the errors, grouped by file or rule.

## Real Example

This side-by-side shows the same TypeScript check before and after RTK: same errors, one line each, grouped by file.

```
# tsc (many lines)                       # rtk tsc
src/harness/context.ts(42,9):            src/harness/context.ts
  error TS2322: Type 'string' ...          L42  TS2322  Type mismatch
src/harness/loop.ts(18,5):                 src/harness/loop.ts
  error TS2554: Expected 2 args ...          L18  TS2554  Expected 2 args
```

## Notes

- Linters that need JSON output (`ruff`, `golangci-lint`, `rubocop`) — RTK parses the JSON, so use the right formatter. (JSON = a structured text format the tool can read reliably.)
- `next build` has multiple stages — RTK keeps the failure logs at the important steps.
- Some filters shell out to ripgrep (`rg`) — make sure `rg` is on PATH. (PATH = the list of folders where the shell looks for programs.)

> **One-line summary:** RTK keeps the real errors and drops the noise — just make sure your linter's formatter and `rg` are available.

---

*Back to [03 — Patterns](../03-patterns/)*