# ❓ FAQ — RTK — Concepts (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## 01-concepts/README.md

### Q5. RTK is installed, but the agent's file reads are still full-size — what is bypassed? [→ Important Limitations (Scope)]

**What you see**

Bash commands come back compressed, so you assume everything is. Then the agent reads a 900-line file with its built-in read tool and dumps the whole thing into the context anyway.

**Why**

The hook only runs on shell (Bash tool) calls. Claude Code's built-in `Read`, `Grep` and `Glob` tools never pass through the hook, so they are not rewritten. This is a scope limit, not a bug — and it is exactly the pitfall the concepts page warns about.

**What to do**

1. For reading files, use shell commands instead: `cat`, `head`, `tail`.
2. For searching, use `rg` or `grep`; for finding, use `find`.
3. Or skip the agent's built-ins entirely and call `rtk read`, `rtk grep`, `rtk find` directly.
4. Remember the second limit: RTK measures bash output reduction, not total token-bill reduction.

```bash
rtk read src/main.rs   # compressed read
rtk grep "fn main"    # compressed search
```

**Verify**

Run a file read through the built-in tool and then through `rtk read`; the second one returns fewer lines for the same file.

---

### Q6. RTK claims "90% saved" but the dashboard shows a different token count — which one is true? [→ The Four Compression Strategies]

**What you see**

A filter reports ~90% reduction, `rtk gain` reports a token number that does not line up with your own calculation, and you cannot tell whether the tool is lying or the math is approximate.

**Why**

RTK is **not a tokenizer**. It estimates tokens as `bytes / 4`. That estimate is good enough for ratios and useless for absolute counts. The percentages (up to 90%) are reliable; the absolute token numbers are approximations. Expect drift whenever output contains multibyte characters, images or very long single lines.

**What to do**

1. Trust the percentage, not the token count, when you compare two versions.
2. Compare raw bytes before and after if you need an exact figure.
3. Report RTK savings as "bash output reduction", never as "total bill reduction".
4. Do not add RTK's absolute numbers to your context-budget spreadsheet as exact values.

```bash
git status | wc -c        # raw bytes
rtk git status | wc -c   # compressed bytes
```

**Verify**

Your write-up quotes percentages with the words "approximately", and the ratio you compute with `wc -c` sits close to the reported reduction.

---

### Q7. A command failed and the useful error vanished — how do I get it back without re-running? [→ When a Command Fails: Tee Recovery]

**What you see**

The agent gets two lines instead of the whole log: `FAILED: 2/15 tests` and a path like `[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]`. The real failure message is not in the context.

**Why**

Compression is lossy by design, so RTK keeps a safety net. When a command fails, it writes the **entire raw output** to a log file under `~/.local/share/rtk/tee/`, so the agent can read the full text back without paying for another run. It is on by default and controlled in `config.toml`.

**What to do**

1. Read the log path printed in the compressed output instead of re-running the command.
2. Keep the feature enabled with `mode = "failures"` (the default).
3. Use `mode = "always"` while debugging noisy pipelines; use `"never"` only if disk usage matters more than recovery.

```toml
[tee]
enabled = true
mode = "failures"   # or "always" / "never"
```

**Verify**

Force a failure, confirm the `~/.local/share/rtk/tee/` log exists and contains the original error line, and confirm you never had to re-run the command.

---

### Q8. Two AI tools behave differently after setup — is one of them broken? [→ Two Operating Modes]

**What you see**

In one tool every `git status` is rewritten silently. In another, nothing changes unless the project has a rules file, and the agent has to call `rtk` by itself. Same binary, same config, different result.

**Why**

RTK has two operating modes. **Hook rewrite** intercepts the command before it runs and rewrites `git status` → `rtk git status`; the agent never notices. **Plugin / rule-based** integration only writes rules (`.clinerules`, `AGENTS.md`, `RTK.md`) that the agent reads and follows on its own — it is not forced.

**What to do**

1. Use hook rewrite where it is available (Claude Code, Copilot in VS Code, Gemini CLI, Cursor).
2. For rule-based tools, commit the rules file to the project so every teammate and every session gets the same behaviour.
3. Do not expect automatic rewriting in rule-based mode; verify by checking the rules file exists.

**Verify**

In hook mode the log shows an `rtk …` command; in rule mode the rules file is present in the repository and a fresh session still compresses output.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 01-concepts/README.md.*
