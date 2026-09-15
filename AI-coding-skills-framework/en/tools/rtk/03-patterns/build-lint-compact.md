# 🏗️ Build & Lint Compact Pattern

**Goal**: Compress build/lint output — keep only important errors and warnings, grouped by file/rule. Helps the agent see "what's broken" instead of reading hundreds of lines of compiler output.

## When to Use

- Frequent builds (`cargo build`, `npm run build`, `next build`).
- Lint/type-check after every code edit (`tsc`, `ruff`, `clippy`, `eslint`).
- CI is red due to compile/lint errors.

## Commands & Reduction Levels

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

## Real Example

```
# tsc (many lines)                       # rtk tsc
src/harness/context.ts(42,9):            src/harness/context.ts
  error TS2322: Type 'string' ...          L42  TS2322  Type mismatch
src/harness/loop.ts(18,5):                 src/harness/loop.ts
  error TS2554: Expected 2 args ...          L18  TS2554  Expected 2 args
```

## Notes

- Linters that need JSON output (`ruff`, `golangci-lint`, `rubocop`) — RTK parses the JSON, so use the right formatter.
- `next build` has multiple stages — RTK keeps the failure logs at the important steps.
- Some filters shell out to ripgrep (`rg`) — make sure `rg` is on PATH.

---

*Back to [03 — Patterns](../03-patterns/)*
