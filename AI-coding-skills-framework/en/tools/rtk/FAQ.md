# ❓ FAQ — RTK (Real Stories, Plain Language)

If a question is unclear, read the section in the named file (named in brackets).

---

## README.md

### Q1. My agent keeps missing the one error line it needs to fix — is the shell to blame? [→ The Opening Story / Overview]

**What you see**

The harness already has tools, memory and context, yet the agent reads a failed `cargo test` and fixes the wrong file. The output it received was 200+ lines; only about 20 lines mattered, and the actual compile error sat in the middle of the noise. The same happens with `git status`, `ls`, `docker ps`.

**Why**

Bash output is the quiet context glutton. Every shell call pours hundreds of lines into the model's immediate context, and the longer the pile, the more likely the one useful line is missed. RTK (Rust Token Killer) is a command-line proxy written in Rust that sits between the agent and the shell, cutting up to **90%** of that output. One binary, 100+ supported commands, less than 10ms of added delay.

**What to do**

1. Install RTK and let it rewrite shell commands (see the `02-setup/README.md` section of this FAQ).
2. Let it apply its four compression strategies: smart filtering (`git push` → `ok main`), grouping (`ls` → a tree with file counts), truncation (`git diff` → headers dropped), deduplication (`docker logs` → `×42 repeated line`).
3. Keep raw output recoverable: on failure, RTK saves the whole log to disk so nothing is lost.

```bash
git status     # agent asks for this
rtk git status # what actually runs; output is filtered first
```

**Verify**

Run the same command with and without RTK and count lines. Expect roughly: `ls -la` 45 → 12 lines (~73%), `git push` 15 lines → `ok main` (~93%), failing `cargo test` 200+ → ~20 lines (~90%).

---

### Q2. Is RTK one more module to study, or is it already part of the harness I built? [→ Is RTK Part of the Harness?]

**What you see**

You finish `harness/01` to `harness/11` and then find RTK waiting in `tools/rtk/`. It is unclear whether it counts as harness work or as a separate tool, and whether skipping it leaves a hole.

**Why**

The harness has 7 components. RTK belongs directly to **Component #3, Context Management** (the token-reduction branch), and only indirectly to Tools (#1) and Evaluation. Concretely it maps to `harness/02-build-context` (primary), `harness/06-decide-tools-mcp` (secondary) and `harness/11-evaluation` (secondary, via `rtk gain`). Because it is a real executable, not a knowledge module, it lives in the `tools/` branch alongside `harness/` and `loop/`.

**What to do**

1. Count RTK as the concrete implementation of the "limit tool output" idea from module `06`, not as an 8th module.
2. Point your Context Management notes at `tools/rtk/` so the theory and the tool stay linked.
3. Use `rtk gain` as your Evaluation evidence for the "cut costs 40-60%" goal.

**Verify**

Your roadmap has one line for `harness/02-build-context` and one line for `tools/rtk/`; no new numbered harness module appears.

---

### Q3. Does this really cut my token bill, or does it just print a prettier table? [→ Why RTK Matters?]

**What you see**

You install RTK, everything looks tidier, and you still cannot prove anything got cheaper. Nobody asked for "prettier" — you wanted a number you can defend to your team.

**Why**

Input tokens are the currency of agent reasoning, and bash noise is pure waste in that budget. RTK reduces measured bash output, and `rtk gain` turns that into a token-saved dashboard, which lines up with the "cut costs 40-60%" target in the harness engineering notes. It does not promise to cut your entire bill — input tokens are only one part of it.

**What to do**

1. Install, then run `rtk gain` and record the baseline before and after.
2. Quote the measured reductions per command, not a single global number.
3. State the scope honestly: bash output reduction, not total bill reduction.

| Command | Raw | RTK | Reduction |
|---|---|---|---|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `ruff check` | many lines | grouped by rule | ~80% |

**Verify**

`rtk gain` opens the dashboard and shows non-zero saved tokens; the numbers in your write-up match a fresh run, not a copied table.

---

### Q4. Six folders, three of them empty-looking — which one do I open first? [→ Learning Roadmap (Directory Structure)]

**What you see**

`tools/rtk/` contains `01-concepts/`, `02-setup/`, `03-patterns/`, `04-savings/`, `05-troubleshooting/`, each with just a README. You cannot tell whether to install first or study theory first.

**Why**

The directory layout is the intended order, not an accident. Each folder answers one question: how it works, how to install, which pattern to try, how to measure, what to do when it breaks. Every folder has a `README.md`, matching the convention used by `harness/` and `loop/`.

**What to do**

1. Read `README.md` (this file's parent) for the context and roadmap.
2. Go to `01-concepts/` for the hook architecture and the four compression strategies.
3. Go to `02-setup/` to install and integrate with your AI tool.
4. Then start a pattern in `03-patterns/` (Git Speedup first), measure in `04-savings/`, and keep `05-troubleshooting/` for when something misbehaves.

**Verify**

You can run `rtk git status` through your AI tool and you know which folder to open next without guessing.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md. Câu hỏi chi tiết cho từng thư mục con nằm trong `FAQ.md` của thư mục con đó.*
