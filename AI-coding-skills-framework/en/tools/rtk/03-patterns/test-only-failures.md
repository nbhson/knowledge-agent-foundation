# 🧪 Test Only Failures Pattern

**Goal**: Keep only **failures** when running tests — passing tests are collapsed into a single number. Helps the agent focus on the exact problem to fix instead of getting lost in hundreds of lines of `... ok`. (Tests = automated checks that verify the code behaves correctly; a failure = a check that did not pass.)

## When to Use

- CI is red and you need the agent to see which test failed fastest. (CI = the automated build-and-test pipeline that runs on every commit; "red" = the pipeline is failing.)
- Debugging a change that causes widespread test regressions. (Regression = something that used to pass now fails.)

> **One-line summary:** Use it when CI is red or many tests break at once — it surfaces the failures in seconds instead of scrolling.

## Commands & Reduction Levels

How to read it: each row maps one test command to its RTK version; "Output" says what you get back; "Reduction" says how much smaller the output is (~90% means 200 lines become about 20). For instance, `cargo test` output becomes just the failures, with the passing tests reduced to one summary line.

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

> **One-line summary:** Whatever your test runner, RTK keeps the failures and collapses the passes into one number — cutting output by about 90%.

Glossary for the table: **tracebacks trimmed** = the long error walk-back is shortened to what matters; **NDJSON** = one JSON object per line, a format Go's test tool emits; **Generic** = any other test command, wrapped the same way.

## Real Example

This side-by-side shows the same failing test run before and after RTK: 200+ lines of `... ok` collapse into the two failures.

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

The agent can read the full log if needed — no need to re-run the command. (The `.log` path = where RTK saved the untouched full output, so nothing is lost.)

## Notes

- **Flaky tests**: don't auto-fix based on a single failure — this pattern only helps *see* failures fast; the decision to fix still belongs to the agent/human, per the harness principles (Feedback Loops & Guardrails). (Flaky test = a test that passes and fails randomly, usually from timing or shared state, not a real bug.)
- For rspec JSON output, `rspec` needs to be configured with a formatter. (rspec = Ruby's test tool; formatter = the setting that chooses its output format.)

> **One-line summary:** Failures surface instantly and the full raw log is saved on disk — but a single failure is a signal, not an order to auto-fix.

---

*Back to [03 — Patterns](../03-patterns/)*