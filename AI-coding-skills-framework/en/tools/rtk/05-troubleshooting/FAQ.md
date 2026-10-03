# ❓ FAQ — RTK — Troubleshooting (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## 05-troubleshooting/README.md

### Q31. I installed RTK, ran `rtk init -g`, restarted — and my bash commands are still 100% raw. What are the checks? [→ Failure Modes & Mitigations Table]

**What you see**

You install RTK, run `rtk init -g`, close and reopen your AI coding tool, and the agent's `git status` still prints the full 120-line dump. `rtk gain` reports `Commands run: 0`. Nothing anywhere suggests RTK is active, so you start reinstalling.

**Why**

The most common cause by far: the tool was not restarted after `rtk init`, so its shell still has the old setup. Two less common causes: on Windows, versions older than **0.37.2** installed a legacy shell hook, which must be migrated to the native binary hook; and a per-project configuration may override the global filter for the directory you are standing in.

**What to do**

1. Fully quit the AI coding tool — not just the conversation — and reopen it.
2. Re-run `rtk init -g` to regenerate the hook; on Windows this also migrates away from the legacy shell hook.
3. Test with one command: `git status` should return the compact grouped stat (~80% smaller).
4. Confirm with `rtk gain --history` — an empty history means the hook is not attached at all.
5. If it works in one project and not another, check for a per-project configuration file.
6. If the agent's own Read / Grep / Glob tools are the ones running raw, that is a different cause — see Q20.

```bash
rtk init -g            # install (or re-install) the hook
rtk init -g --uninstall   # remove it entirely, if you must start over
```

**Verify**

`rtk gain --history` lists rewritten commands, `rtk git status` matches the compact format, and the reduction percentage in `rtk gain` is no longer zero. Reinstalling RTK is almost never the fix — a restart plus `rtk init -g` is.

---

### Q32. The agent's built-in Read / Grep / Glob tools go straight to RTK's bypass — no savings there at all. [→ Failure Modes & Mitigations Table]

**What you see**

`rtk gain` shows good numbers for shell commands, yet your context window still fills with file contents. You notice the agent reading whole files with its built-in tools, while `rtk read`, `rtk grep`, and `rtk find` sit unused.

**Why**

The hook only intercepts **bash commands**. The agent's built-in tools — `Read`, `Grep`, `Glob` — do not go through the shell, so RTK never sees them. This is not a bug and no setting fixes it; those tool calls are structurally outside the hook's reach.

**What to do**

1. In your task instructions, tell the agent to use `rtk read`, `rtk grep`, and `rtk find` when it explores.
2. Keep the hook for everything that does go through the shell — status, log, diff, tests, builds.
3. Remember `rtk read` returns structure, not content — pair it with a real read before editing.
4. Budget for it: shell savings do not offset a single `cat` of a 2,000-line file.

```
# shell path — rewritten by the hook
git status                → rtk git status
# built-in tools — not rewritten, must be requested by name
Read(path)  Grep(...)     → rtk read / rtk grep
```

**Verify**

`rtk gain --history` shows `rtk read` and `rtk grep` entries when you ask the agent to explore, and context use per exploration drops by roughly 60–90%.

---

### Q33. `rtk gain` fails right after `cargo install` — I installed RTK from crates.io. What now? [→ Failure Modes & Mitigations Table]

**What you see**

You run `cargo install rtk`, it succeeds, and then `rtk gain` errors out with a message about an unknown subcommand. Worse, there is a binary on your PATH that answers to a different tool's expectations — `rtk init` writes no hook, and `git status` still prints the raw dump. You installed the wrong package.

**Why**

There is a name collision on crates.io: a different, unrelated project called "Rust Type Kit" also publishes under the name `rtk`. `cargo install rtk` grabs that one, so the binary on your PATH is not the RTK described in this guide. The RTK you want must be installed straight from its own repository, which also means the hook and the binary have to point at each other correctly afterwards.

**What to do**

1. Remove the wrong binary: `cargo uninstall rtk`.
2. Install from the RTK repository instead of the registry:

```bash
cargo uninstall rtk
cargo install --git https://github.com/rtk-ai/rtk
rtk gain                       # now it should run, not error
```

3. Re-run `rtk init -g` and restart your tool, because the hook points at the binary path.
4. If `rtk gain` still misbehaves, confirm which binary is answering with `which rtk`.

**Verify**

`which rtk` resolves to the repository install, `rtk gain` prints a report (for example `Commands run: 342`, `Reduction: 82%`), and `rtk gain --history` is non-empty after a working session.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 05-troubleshooting/README.md.*
