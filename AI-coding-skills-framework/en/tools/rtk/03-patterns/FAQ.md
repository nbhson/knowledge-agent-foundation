# ❓ FAQ — RTK — 03-patterns (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## 03-patterns/README.md

### Q13. There are four patterns and I only have one weekend — which one do I turn on first? [→ Pattern Picker]

**What you see**

A single agent session burns through context in three different ways. `git status` prints 120 lines of untracked files. Then `npm test` prints 400 lines of `ok`. Then the agent reads a 2,000-line file whole, just to find one function. You installed RTK to fix one of these — and you do not know which one is actually costing you.

**Why**

RTK patterns are per-command-type filters, not one global switch. Each one rewrites a different family of commands, so enabling the wrong pattern changes nothing about the command that hurt you. The four patterns cover four different kinds of noise: git chatter, test chatter, file size, and build chatter.

**What to do**

1. Look at what hurts *right now* and use the decision tree — the answer is one branch, not four.
2. If you are just starting, enable **Git Speedup** first. It is safe, easy to verify (`git status` → `rtk git status`), and it applies to every git working session.
3. If continuous integration (CI) is red right now, pick **Test Only Failures** — ~90% reduction, failures only.
4. If the repo is large and unfamiliar, pick **File Smart Read** — ~60–90% on big files.
5. If you build or lint many times a day, pick **Build & Lint Compact** — ~75–85%.
6. If you want all four, install the hook with `rtk init -g` and stop choosing.

| What hurts right now | Choose | Reduction |
|---|---|---|
| git status / log / diff | Git Speedup | ~70–93% |
| Test output long, agent lost | Test Only Failures | ~90% |
| Agent reads whole large files | File Smart Read | ~60–90% |
| Build / lint verbose | Build & Lint Compact | ~75–85% |

**Verify**

Run the raw command, then the RTK command, and count lines. Then run `rtk gain` — the saved-token line should be non-zero and should name the commands you expected.

---

### Q14. Do I have to type `rtk` in front of every command, or is there a way to make it automatic? [→ How to Use a Pattern]

**What you see**

You read the docs, ran `rtk init -g`, and nothing changed. The agent still calls plain `git status` and gets the full 120-line dump. Worse, you catch yourself rewriting every git command by hand in your prompts — `rtk git status`, `rtk git log`, `rtk git diff` — which is exactly the busywork RTK is supposed to remove.

**Why**

RTK has two usage modes. Manual mode is typing `rtk <command>` yourself. Hook mode installs itself in the shell of your AI coding tool and rewrites matching bash commands *before* they run, so the agent keeps writing plain `git status` and gets the compact output anyway. The hook only attaches to shell commands, and the four patterns do not fight each other: RTK routes each command to the right filter automatically.

**What to do**

1. **Pick the pattern** using the table or the decision tree in Q1.
2. **Enable the hook**: run `rtk init -g` for your tool (see the `02-setup` folder).
3. **Restart the AI coding tool fully** — a running tool keeps its old shell setup.
4. **Verify** by running the command and comparing raw output against RTK output.
5. **Measure** with `rtk gain` (see `04-savings`).
6. **Tune** if something gets rewritten unexpectedly: add it to `exclude_commands` in `config.toml`.

```
# manual mode — agent must remember the prefix
rtk git status
# hook mode — agent writes plain commands
git status        # RTK rewrites it, output is compact
```

**Verify**

`rtk git status` returns the compact grouped summary, and `rtk gain --history` lists commands you never prefixed. If history is empty, the hook is not attached — go to Q19.

---

### Q15. The hook rewrote a command I needed in full — should I just turn RTK off? [→ Golden rule]

**What you see**

You asked for a careful review of a security-sensitive diff. The agent ran `git diff`, got back a compressed version with most context lines stripped, and commented on changes that were not there. Or: `rtk gain` looks great on paper, but you no longer trust what the agent is reading before it acts.

**Why**

RTK assumes most command output is low-signal noise. That assumption is wrong for a small set of commands — detailed diffs, plan output you must read line by line, anything a script parses. The fix is not to remove the whole hook, because the other 90% of your session still benefits.

**What to do**

1. Keep the hook. Turn off the *rewrite* for that one command — one exclusion, not a shutdown.
2. Add the exact command string to `exclude_commands` in `config.toml`.
3. Repeat for `curl` (it downloads binaries — never let a filter rewrite it), `playwright`, and `terraform plan`.
4. Re-run the excluded command yourself and read it before the agent acts on it.
5. If excluding one string is not enough, exclude the whole family (`git diff`) rather than every git command.

```toml
# ~/.config/rtk/config.toml
[hooks]
exclude_commands = ["git diff", "curl", "playwright", "terraform plan"]
```

**Verify**

Run the excluded command — you get the original format back, full lines and all. Run `rtk gain` — the overall reduction drops slightly, and that is expected and correct.

The rule to remember: RTK rewrites are transparent. The agent can always call the original command itself, so an exclusion is a preference you state, not a wall you build. If a whole category is excluded, the honest move is to reconsider whether that category belongs in the hook at all.

---

## 03-patterns/git-speedup.md

### Q16. `git push` now prints one line, `ok main` — is the push real, or did something get skipped? [→ Real Example]

**What you see**

```
# git push — 15 lines                 # rtk git push — 1 line
Enumerating objects: 5, done.              ok main
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
...
```

The familiar progress chatter is gone. Your instinct is that a push that says nothing about objects, refs, or the remote cannot be trusted.

**Why**

For push, RTK keeps only the facts that can change: it succeeded, and on which branch. Everything else — object enumeration, delta compression using up to 8 threads — is byte-identical on every single push, so it is pure context cost. RTK preserves the exit status, which is the part a script or a human actually acts on.

**What to do**

1. Read the **exit code**, not the prose. Zero means the push happened.
2. Confirm the remote really moved: `git status -sb`, or compare `git log origin/main -1`.
3. If a hook or CI system depends on the original text, add `git push` to `exclude_commands`.
4. Expect the same for the rest: `git add` → `ok` (~95%), `git commit` → `ok abc1234` (~95%), `git pull` → `ok 3 files +10 -2` (~90%).

| Command | RTK output | Reduction |
|---|---|---|
| `git status` | compact stat, grouped by state | ~80% |
| `git log -n 10` | hash + author + subject only | ~70% |
| `git diff` | reduced context, headers stripped | ~75% |
| `git push` / `git pull` | `ok main` / `ok 3 files +10 -2` | ~93% / ~90% |

**Verify**

After `rtk git push`, `git status -sb` shows your branch in sync with the remote, and `git log origin/main -1` shows the commit you just made.

---

### Q17. The agent edited the wrong lines after reading a compressed `git diff` — how do I get the real diff back? [→ Notes]

**What you see**

You ask the agent to fix a bug in `src/harness/context.ts`. It runs `git diff`, reads a compressed version with the surrounding context lines stripped, and patches the wrong function — sometimes a function that does not even exist in the file. You are now debugging the agent's mistake instead of your bug.

**Why**

`rtk git diff` is a *compression*, not a truncation: it keeps the changed lines and drops headers and context. Roughly 75% smaller, which means about 75% of the lines that explain *why* a change matters are gone. Line-level editing needs those lines; exploring does not.

**What to do**

1. Treat the compressed diff as a **map**, not as the file: use it to find which files and functions changed.
2. For any edit, have the agent call plain `git diff -- <path>` — no RTK — or `cat` / the read tool on that one file.
3. If the agent keeps getting it wrong, add `git diff` to `exclude_commands` in `config.toml` so the raw diff always reaches it.
4. Do not turn off the whole hook for this — `git status` (~80%), `git log` (~70%), and `git push` (~93%) still save on every single call.
5. Give the agent a rule in the task prompt: "locate with `rtk git diff`, edit with plain `git diff -- <path>`".

```bash
# map: compressed, cheap
rtk git diff
# act: raw diff for the one file being edited
git diff -- src/harness/context.ts
```

**Verify**

The agent's edit lands on a function that exists at the line it names. `git diff --stat` afterwards shows only the intended file changed.

---

### Q18. `rtk git log -n 10` gave me no file names — my review needs the changed files, where did they go? [→ Commands & Reduction Levels]

**What you see**

You run `rtk git log -n 10` before reviewing someone else's branch. You get hash, author, subject — ten tidy lines, ~70% smaller. The list of files each commit touched is gone, so you cannot tell which commit touched the payment module, and you end up running `git show` per commit anyway.

**Why**

RTK keeps three fields for log: hash, author, subject. That is enough to answer "what happened and who did it", but not "where". File-level information lives in `--stat` / `--name-only`, which the compact format drops.

**What to do**

1. Use `rtk git log -n 10` to pick the interesting commits — cheap orientation.
2. For file detail, call plain `git log --stat -n 10`, or `rtk git log -n 10 --stat` if you want the rest of the summary compact too.
3. If file names in history are a daily need, add `git log` to `exclude_commands` rather than paying for it every single time.
4. To diff two commits directly, use `rtk diff file1 file2` — condensed diff, ~75% smaller, exit code 1 when the files differ.

```bash
rtk git log -n 10                 # hash + author + subject
git log --stat -n 10              # adds the changed-file list
rtk diff a.rs b.rs                # condensed diff; exit 1 if different
```

**Verify**

The review shows, per commit, the files it touched. If a pipeline that greps `git log` output comes back empty, the compact format is the cause — see Q7-style exclude handling in `05-troubleshooting`.

---

## 03-patterns/build-lint-compact.md

### Q19. The compact build output never says "Build succeeded" — did my build pass or fail? [→ Commands & Reduction Levels]

**What you see**

```
# tsc — many lines                    # rtk tsc
src/harness/context.ts(42,9):          src/harness/context.ts
  error TS2322: Type 'string' ...         L42  TS2322  Type mismatch
src/harness/loop.ts(18,5):               src/harness/loop.ts
  error TS2554: Expected 2 args ...       L18  TS2554  Expected 2 args
```

Three lines in, four lines out. The words "compiled successfully" or "Build succeeded" are not there, and the agent starts guessing whether the build is green.

**Why**

RTK keeps what is *actionable*: errors, warnings, and the file they belong to, grouped so one file is one block. The progress narration (`Compiling 214 crates`, `Finished dev [unoptimized] target(s) in 42.19s`) repeats on every run and carries no information you act on. The pass/fail fact was never lost — it is in the exit code, exactly as it is without RTK.

**What to do**

1. Read the exit code. Zero means every check passed; non-zero means it failed — that fact is never compressed away.
2. Read the grouped blocks: file path, then line number, then rule or error code.
3. Expect the same shape everywhere: `rtk tsc` (~85%), `rtk lint` (~80%), `rtk ruff check` (~80%), `rtk golangci-lint run` (~85%), `rtk next build` (~75%), `rtk cargo build` and `rtk cargo clippy` (~80% each), `rtk prettier --check .` (~75%), `rtk sbt compile` (~75%).
4. If a stage name matters — for example which `next build` stage broke — check the failure log for that step; RTK keeps those logs.
5. If you genuinely need the raw narration, add that one command to `exclude_commands` instead of rebuilding your habit around silence.

**Verify**

Run `rtk tsc; echo $?` — the number is the answer. Cross-check one grouped error against plain `tsc` and confirm the line and code match.

---

### Q20. `Binary 'rg' not found on PATH` — what broke, and why does RTK need ripgrep? [→ Notes]

**What you see**

You install RTK, enable the hook, and the first build or lint command fails with `Binary 'rg' not found on PATH`. Git and test commands work fine, so you assume the install failed. On macOS the fix is `brew install ripgrep`; on Windows it is `winget install BurntSushi.ripgrep.MSVC`.

**Why**

Some RTK filters shell out to `rg` (ripgrep) instead of filtering in its own process — it is simply faster at scanning a tree. `rg` is a separate program from RTK. If it is not installed, or not visible to the tool that spawned the shell, only the filters that depend on it break. This is a missing dependency, not a broken install.

**What to do**

1. Confirm it is missing: `rg --version` in the same shell your agent uses.
2. Install it: `brew install ripgrep` on macOS, `winget install BurntSushi.ripgrep.MSVC` on Windows.
3. If `rg` exists but still errors, it is a PATH problem — the tool's shell was started before the install, so restart it.
4. Verify with `rtk grep "pattern" .` (~75% reduction, grouped results) and `rtk find "*.rs" .` (~70%).
5. Check `rtk gain --history`: the failing entries disappear once the dependency is present.

**Verify**

`rg --version` prints a number in the agent's shell, `rtk grep` returns grouped hits, and `rtk gain --history` shows the previously failing command now counting savings instead of errors. Installing ripgrep is a one-line fix — there is nothing to configure in `config.toml` for it.

---

### Q21. RTK turned my linter output into JSON and my tooling choked — is that expected? [→ Notes]

**What you see**

`ruff check` used to print human-readable lines. Through RTK it prints JSON grouped by rule and file, and an editor plugin or a small script that expected text now fails to parse it. Same story for `golangci-lint run` and `rubocop`.

**Why**

Those three linters already have a machine-readable format, and RTK parses that format to do the grouping — it does not invent JSON from human text. If the formatter is missing or set to the default human format, the reduction drops or the filter cannot do its job. `rubocop` shows the smallest gain (~60%+) for exactly this reason.

**What to do**

1. Tell the linter to emit the format RTK expects, so RTK reads JSON and re-groups it.
2. Leave the linter's own human output for when you read it yourself — call it directly.
3. If a downstream script or editor plugin parses the original text, add that command to `exclude_commands`.
4. Remember which gain each one should reach: `golangci-lint run` ~85%, `eslint` ~80%, `ruff check` ~80%, `rubocop` ~60%+.

```bash
ruff check . --output-format json   # RTK parses this and groups it
ruff check .                         # human output, when you read it
```

**Verify**

`rtk ruff check` returns grouped entries (rule + file), and your editor plugin is pointed at plain `ruff check`, not at RTK output. Grouping by rule is the practical win here: 400 lines of the same rule across 90 files becomes one block, and the agent fixes the rule instead of the line.

---

## 03-patterns/file-smart-read.md

### Q22. The agent used `rtk read`, then edited a function that is not in the file — why? [→ Notes]

**What you see**

You ask the agent to change `fn compress`. It runs `rtk read src/harness/context.rs`, gets back a list of signatures, and rewrites the file — replacing a body it never actually read. The result either fails to compile or, worse, silently deletes logic.

**Why**

`rtk read` is **not** `cat`. It returns structure — signatures, line numbers, a skeleton — and drops function bodies. That is the point (~60–90% smaller), and it is enough to *understand* a file. It is not enough to *edit* one, because editing needs the exact current text of the lines being changed.

**What to do**

1. Use `rtk read` to locate: which file, which line, which function.
2. Then read the real content for the edit — plain `cat`, or the agent's built-in read tool, on that file or that range.
3. If the agent edits from `rtk read` output alone, say so explicitly in the task prompt.
4. Keep the search cheap too: `rtk find "*.rs" .` (~70%), `rtk grep "pattern" .` (~75%), `rtk diff file1 file2` (~75%, exit code 1 when the files differ).
5. Give the pattern a name so it survives: "locate with `rtk read`, read the body before editing".

```bash
rtk read src/harness/context.rs            # where is it?  (cheap)
cat src/harness/context.rs                 # exact text for editing
```

**Verify**

The agent's patch applies to lines that exist. `git diff` after the change shows only the intended function touched, no accidental deletions. If it does not, that is the signal to stop using `rtk read` for edits in that session and go back to full reads.

---

### Q23. How does a 1,240-line file fit into 20 lines — and can I trust what I am seeing? [→ Real Example]

**What you see**

```
File: src/harness/context.rs (1,240 lines)
  pub struct ContextManager            // L42
    fn build(&mut self, ctx: Ctx)      // L45
    fn compress(&self) -> Result       // L210
    fn limit(&self) -> TokenBudget     // L390
```

Twenty lines describe a 1,240-line file. Your worry: the agent now "knows" the file but is reasoning from a summary, so it will confidently answer questions about logic it never saw.

**Why**

This is the same idea as the harness's "Tier 5 — Immediate Context": put only the necessary part into context. Signatures and structure answer the questions you ask 90% of the time — does this function exist, what does it take, what does it return, which line is it on — at roughly 90%+ reduction with `-l aggressive`, which strips bodies entirely.

**What to do**

1. Use the summary for orientation and for locating the code you will change.
2. Use `-l aggressive` (signatures only, bodies stripped, ~90%+ smaller) when you only need the shape of the file.
3. Use plain `rtk read file.rs` (~60–90% smaller, keeps some body) when you need behaviour, not just shape.
4. Drop to `rtk smart file.rs` (~95% smaller) for a two-line heuristic summary when even signatures are too much.
5. Treat the `// L42` comments as an index, not as content — they are there so the next read can jump straight to the line.

**Verify**

Every line number in the summary matches the real file — spot-check one with `sed -n '210p'`. If the agent makes a claim about logic, ask it to quote the body from the raw file first. If a line number is wrong, the summary is stale: the file changed since it was produced, so regenerate it.

---

### Q24. `rtk read`, `rtk read -l aggressive`, and `rtk smart` — which one should the agent use? [→ Commands & Reduction Levels]

**What you see**

Three commands for one file, and the agent picks randomly: sometimes the 2-line summary when it needs the code, sometimes full structure when it only needed to know the file exists. You end up paying 60% reduction on a question that needed 95%, or losing detail it needed.

**Why**

They answer different questions at different costs. `rtk read` returns signatures plus structure. `rtk read -l aggressive` returns signatures only, with bodies stripped — cheapest useful view. `rtk smart` returns a two-line heuristic summary — a guess about what the file does, useful for triage, not for editing. Choosing by intent instead of habit is the whole difference.

**What to do**

1. "Does this file have X, and where?" → `rtk read file.rs`.
2. "What is the shape of this file?" → `rtk read file.rs -l aggressive`.
3. "What does it do?" → `rtk smart file.rs`.
4. "I must edit line 210" → plain `cat` / built-in read tool.
5. Explore a repo you do not know with the trio: `rtk find "*.rs" .` → `rtk grep "pattern" .` → `rtk smart`.

```
# triage a file you have never opened
rtk smart file.rs                 # 2 lines: what it probably does
rtk read file.rs -l aggressive    # signatures + line numbers only
rtk read file.rs                  # signatures + structure, some body
```

| Question | Command | Reduction |
|---|---|---|
| What is in this file? | `rtk read file.rs` | ~60–90% |
| What is its shape? | `rtk read file.rs -l aggressive` | ~90%+ |
| What does it do? | `rtk smart file.rs` | ~95% |

**Verify**

`rtk gain --daily` shows a spread of reduction levels across your reads, not every read landing on the same one. And no edit ever gets made from a `rtk smart` summary.

---

## 03-patterns/test-only-failures.md

### Q25. My test suite went from 200 lines to 20 — where did the other 180 lines go? [→ Real Example]

**What you see**

```
# cargo test — 200+ lines on failure    # rtk test cargo test — ~20 lines
running 15 tests                        FAILED: 2/15 tests
test utils::test_parse ... ok           test_edge_case: assertion failed
test utils::test_format ... ok          test_overflow: panic at utils.rs:18
...

FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Two failures, a count, and a path to a log file. The 13 passing tests are gone from view — including their timings, which you used to compare before and after a change.

**Why**

Passing tests are collapsed into a single number because `... ok` repeated 13 times carries no decision value: if it printed, it passed. The reduction is ~90% across `cargo test`, `npm test`, `pytest`, `go test`, `jest`, and `vitest`. Nothing was deleted — on failure RTK writes the entire raw output to a log file under `~/.local/share/rtk/tee/`, so the detail is one read away and does not require re-running the suite.

**What to do**

1. Read the two failures and the `FAILED: 2/15` line — that is the whole point.
2. Read the full log file when you need timing, a full stack trace, or the list of passes.
3. For `go test`, RTK parses NDJSON (one JSON object per line) — failures only.
4. If a script counts tests by parsing the original output, exclude the command instead.

```bash
cat ~/.local/share/rtk/tee/1707753600_cargo_test.log   # full raw output
```

**Verify**

The log file exists, its line count matches roughly what the raw run produced, and the failing test names in the compact output appear verbatim inside it.

---

### Q26. One test fails every third run and the agent keeps "fixing" it — what is RTK's part in this? [→ Notes]

**What you see**

```
FAILED: 1/412 tests
test_retry_backoff: expected 3 attempts, got 2
```

The agent reads this as a clear, reproducible failure, changes working code, and the test passes — so it commits. Two days later it fails again in CI, in a different place.

**Why**

RTK makes failures *visible* faster (~90% reduction) but does not make them *deterministic*. A flaky test — one that depends on timing, ordering, or shared state — looks identical to a real bug in compact output. The decision to fix still belongs to the agent and to you, not to the tool that printed the line.

**What to do**

1. Re-run the failing test in isolation before changing any code.
2. If it passes on the second run, treat it as flaky: fix the test's isolation, not the feature.
3. Confirm the pass/fail state from the run's exit code, not from a single line of text.
4. Keep the raw log around; flaky failures often only show their cause in the full trace.
5. Require three consecutive failures in a row before the agent edits implementation code.

**Verify**

The same test fails and passes on alternating runs *before* any code change. Only after it fails on three consecutive runs does the agent touch the implementation. The pattern helps you *see* the failure faster; it never makes the decision for you.

---

### Q27. `rtk rspec` only saved ~60% while `rtk pytest` saved ~90% — why the difference? [→ Notes]

**What you see**

Your Python and JavaScript suites drop to a fraction of their size: a failing `cargo test` goes from 200+ lines to ~20 (~90%). The Ruby suite barely shrinks, and sometimes the grouped output comes back empty even though tests clearly failed.

**Why**

`pytest`, `jest`, `vitest`, `go test`, and `cargo test` all report results in a format RTK can parse directly, so every passing line collapses into one count. `rspec` reports in a human format by default, so RTK has nothing structured to collapse — it needs a JSON formatter configured on the Ruby side first. Until then you get the smaller reduction (~60%+) instead of ~90%. The gap is a property of the runner, not of your Ruby code.

**What to do**

1. Configure `rspec` with a machine-readable formatter (JSON) before running it through RTK.
2. Keep the human formatter for local human reading.
3. Check the exit code either way — that is what tells you the suite actually failed.
4. Re-check after a `.rspec` or `spec_helper` change; the formatter setting is the only thing that moved.

```bash
rspec --format json     # or set it in .rspec / spec_helper
rtk rspec               # now groups failures like the other runners
```

**Verify**

`rtk rspec` lists the failing examples instead of dumping every pass; `rtk gain --daily` shows the Ruby line moving up toward the Python and JavaScript lines. Until the formatter is set, expect Ruby to be the one suite in your report that barely moves.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md, 03-patterns/*.md.*
