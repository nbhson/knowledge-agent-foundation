# Hooks: guards at every door, every job gets checked

> Addendum to `harness/07` + `harness/10`.
> Source: GitHub Docs "Use hooks with Copilot agents / CLI".

## Picture this

This section explains the difference between instructions (which can be forgotten) and hooks (which cannot).

Instructions are **a reminder**: "remember to format before commit" — the agent may forget.
Hooks are **guards at the door**: before a tool runs (`preToolUse`) they stop and check,
after it finishes (`postToolUse`) they check again. No forgetting possible (a hook = a small script the harness runs automatically at a fixed moment).

An agent session has many such "doors" (each door = one moment in the session where hooks can run):
session start (`sessionStart`),
user message (`userPromptSubmitted`), before/after each tool
(`preToolUse`/`postToolUse`), errors (`errorOccurred`), session end (`sessionEnd`).
The CLI adds `agentStop`.

> **One-line summary:** Instructions can be forgotten; hooks are scripts that run automatically at fixed "doors" in the session — before and after every tool call.

## How to write a hook

This section explains where hook files live and what they must contain.

One `NAME.json` per purpose inside `.github/hooks/`
(cloud agents require the file on the default branch — the branch used by default when nothing is specified).
The CLI reads from the working directory. After writing, do two things:
check JSON with `jq . NAME.json` (`jq` = a command-line JSON formatter; a parse error here means broken syntax) and make scripts runnable with `chmod +x script.sh` (gives the script "execute" permission).

Standard frame:

> 📄 **Example code:** [`examples/01-how-to-write-a-hook.json`](examples/01-how-to-write-a-hook.json)

Each hook is one concrete command. Always write **both** `bash` (Linux/macOS)
and `powershell` (Windows) so every machine runs it:

> 📄 **Example code:** [`examples/02-how-to-write-a-hook.json`](examples/02-how-to-write-a-hook.json)

Besides local scripts, hooks can POST the JSON payload to a URL (HTTP hooks — POST = send the data to a web endpoint).

> **One-line summary:** One JSON file per hook in `.github/hooks/`, with a command for both bash and PowerShell, validated with `jq` and made executable.

## What is each door for?

This section explains what each hook point is good for, so you pick the right one.

- **`preToolUse` — the key door.** The hook gets stdin JSON with
  `toolName` (which tool) + `toolArgs` (planning what), then answers:
  `deny` (no), `ask` (ask a human), or rewrites with `modifiedArgs`/`updatedInput`
  plus `additionalContext`. Use for approval gates (a checkpoint where a human says yes/no), secret redaction (scrubbing `sk-…`-style keys),
  blast-radius checks (blast radius = everything an action could touch or break). Example: block `edit/create` without an approval artifact.
- **`postToolUse` — cleanup door.** Run formatters, update hash manifests, trigger tests after the tool finishes.
- **`userPromptSubmitted` / `sessionStart` / `sessionEnd` — logbook doors.**
  Inject context at session start, write audit logs at the end.
  Those logs feed `harness/13-trajectory-observability` (the observability doc — trajectory = the recorded history of what the agent did).
- **Custom agents** can declare hooks inline (`hooks:`) or opt into shared repo hooks.
  Untrusted file hooks don't load by default — opt in only when you trust the folder.

> **One-line summary:** `preToolUse` is where you block or reshape risky tool calls, `postToolUse` cleans up after, and the logbook doors record the session.

## Test it on your machine first

This section shows how to test a hook locally before trusting it in the repo.

Fake one tool call, pipe it into your script, check the JSON answer:

> 📄 **Example code:** [`examples/03-test-it-on-your-machine-first.sh`](examples/03-test-it-on-your-machine-first.sh)

Three usual mistakes: file outside `.github/hooks/`, missing `"version": 1`,
script not `chmod +x`. For approval doors remember **fail-closed** (fail-closed = when anything goes wrong, refuse rather than allow):
on error or timeout, block — don't wave through (timeout-deny).

> **One-line summary:** Test each hook by piping a fake tool call into it, and make approval hooks fail-closed — any error blocks the action.
