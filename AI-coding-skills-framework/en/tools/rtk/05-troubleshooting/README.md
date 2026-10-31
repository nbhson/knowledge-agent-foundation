# 🛠️ 05. Troubleshooting — Handling Failures

> Common hiccups you might hit with RTK, how to figure out what went wrong, and how to fix it. Covers failure modes, exclude rules, and when it is better to turn RTK off.

## Failure Modes & Mitigations Table

How to read this table: each row is one symptom. **Failure** = what you observe, **Cause** = why it happens, **Solution** = the fix. For instance, "bash commands not rewritten" almost always means the AI tool was not restarted after `rtk init`. ("Rewritten" = RTK silently replaces `git status` with `rtk git status`.)

| Failure | Cause | Solution |
|---------|-------|----------|
| Bash commands not rewritten | Haven't restarted the AI tool after `rtk init` | Restart the tool and retest `git status` |
| Outside the hook: built-in tools (`Read`/`Grep`/`Glob`) bypass | Use shell commands or call `rtk read`/`rtk grep` directly |
| `Binary 'rg' not found on PATH` | Missing ripgrep — some filters need `rg` | `brew install ripgrep` / `winget install BurntSushi.ripgrep.MSVC` |
| `rtk gain` fails after `cargo install` | Installed the wrong "Rust Type Kit" package (crates.io collision) | `cargo install --git https://github.com/rtk-ai/rtk` |
| Important commands compressed too far | Filter too aggressive | Add to `exclude_commands` in `config.toml` |
| Output loses context in pipelines (`\| grep`) | Compressed format not parseable | Check the pipeline; call the original command directly if needed |
| Token cost still high | Not using all RTK features | `rtk discover` finds 0%-reduction commands; add custom TOML filters |
| On Windows: legacy shell hook | Version < 0.37.2 | Re-run `rtk init -g` to migrate to the native binary hook |
| Filter not applied for a specific project | Needs per-project config | See the Configuration guide (per-project filters) |

> **One-line summary:** Most failures are "restart the tool", "install ripgrep", or "exclude this command" — check the table before reinstalling anything.

## Exclude Rules — When to Keep the Original Command

This section lists when RTK should *not* touch a command. `exclude_commands` is a do-not-rewrite list in `config.toml` — commands on it run exactly as typed.

Add a command to `exclude_commands` if:

- It needs the **exact full** output (e.g., detailed `git diff`, `terraform plan`).
- It **should not be rewritten** to avoid danger (curl downloading binaries, playwright).
- A pipeline/script depends on the original output format.

> 📄 **Example code:** [`examples/01-exclude-rules-when-to-keep-the-original-command.toml`](examples/01-exclude-rules-when-to-keep-the-original-command.toml)

> **One-line summary:** Exclude any command whose full, raw output is the point — safety or format beats savings.

## Safety Notes (harness Guardrails connection)

How to read this table: left = a safety principle from the harness guardrails, right = how RTK applies it in practice. For instance, "Tee recovery" means RTK keeps a full copy of failed output on disk so nothing is lost.

| Principle | Applied to RTK |
|-----------|----------------|
| Per the harness guardrails principle | RTK rewrites are transparent — the agent can still call the original command. Always check important output before the agent acts on it. |
| Tee recovery | When a command fails, RTK stores the full output — the agent should read the complete log before deciding on a fix. |
| Privacy by default | Telemetry is off by default. AWS filters proactively strip secrets. Set `RTK_TELEMETRY_DISABLED=1` for an absolute block if desired. |

> **One-line summary:** RTK compresses output but never destroys it — originals stay callable, failures keep full logs, and nothing is sent anywhere by default.

## When You Should Turn RTK Off

This section is the "press the off switch" list — cases where compression costs more than it saves.

- Debugging the exact output of a specific tool and you need the raw version.
- A command with important side effects where you want to see the full log.
- A pipeline/CI script that parses output in the original format.

> 📄 **Example code:** [`examples/02-when-you-should-turn-rtk-off.sh`](examples/02-when-you-should-turn-rtk-off.sh)

Or use `exclude_commands` per command instead of turning it off entirely.

> **One-line summary:** Turn RTK off (or exclude the single command) whenever you need the raw, untouched output.

---

*Back to [rtk/README.md](../)* · Previous: [04 — Savings](../04-savings/)
