# 🧪 Test Only Failures Pattern

**Goal**: Keep only **failures** when running tests — passing tests are collapsed into a single number. Helps the agent focus on the exact problem to fix instead of getting lost in hundreds of lines of `... ok`.

## When to Use

- CI is red and you need the agent to see which test failed fastest.
- Debugging a change that causes widespread test regressions.

## Commands & Reduction Levels

| Original command | RTK | Output | Reduction |
|------------------|-----|--------|-----------|
| `cargo test` | `rtk cargo test` | Failures only, passes collapsed | ~90% |
| `npm test` | `rtk npm test` | Failures only, passes collapsed | ~90% |
| `pytest` | `rtk pytest` | Failures only, tracebacks trimmed | ~90% |
| `go test` | `rtk go test` | NDJSON parsed, failures only | ~90% |
| `jest` | `rtk jest` | Failures only | ~90% |
| `vitest` | `rtk vitest` | Failures only | ~90% |
| `rspec` | `rtk rspec` | JSON, failures only | ~60%+ |
| Generic | `rtk test <cmd>` | Failures only | ~90% |

## Real Example

```
# cargo test (200+ lines on failure)     # rtk test cargo test (~20 lines)
running 15 tests                          FAILED: 2/15 tests
test utils::test_parse ... ok               test_edge_case: assertion failed
test utils::test_format ... ok              test_overflow: panic at utils.rs:18
...
```

When a command fails, RTK stores the entire raw output:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

The agent can read the full log if needed — no need to re-run the command.

## Notes

- **Flaky tests**: don't auto-fix based on a single failure — this pattern only helps *see* failures fast; the decision to fix still belongs to the agent/human, per the harness principles (Feedback Loops & Guardrails).
- For rspec JSON output, `rspec` needs to be configured with a formatter.

---

*Back to [03 — Patterns](../03-patterns/)*
