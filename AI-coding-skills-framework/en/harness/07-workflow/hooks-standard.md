# Hooks: guards at every door, every job gets checked

> Addendum to `harness/07` + `harness/10`.
> Source: GitHub Docs "Use hooks with Copilot agents / CLI".

## Picture this

Instructions are **a reminder**: "remember to format before commit" — the agent may forget.
Hooks are **guards at the door**: before a tool runs (`preToolUse`) they stop and check,
after it finishes (`postToolUse`) they check again. No forgetting possible.

An agent session has many such "doors": session start (`sessionStart`),
user message (`userPromptSubmitted`), before/after each tool
(`preToolUse`/`postToolUse`), errors (`errorOccurred`), session end (`sessionEnd`).
The CLI adds `agentStop`.

## How to write a hook

One `NAME.json` per purpose inside `.github/hooks/`
(cloud agents require the file on the default branch).
The CLI reads from the working directory. After writing, do two things:
check JSON with `jq . NAME.json` and make scripts runnable with `chmod +x script.sh`.

Standard frame:

> 📄 **Example code:** [`examples/01-how-to-write-a-hook.json`](examples/01-how-to-write-a-hook.json)

Each hook is one concrete command. Always write **both** `bash` (Linux/macOS)
and `powershell` (Windows) so every machine runs it:

> 📄 **Example code:** [`examples/02-how-to-write-a-hook.json`](examples/02-how-to-write-a-hook.json)

Besides local scripts, hooks can POST the JSON payload to a URL (HTTP hooks).

## What is each door for?

- **`preToolUse` — the key door.** The hook gets stdin JSON with
  `toolName` (which tool) + `toolArgs` (planning what), then answers:
  `deny` (no), `ask` (ask a human), or rewrites with `modifiedArgs`/`updatedInput`
  plus `additionalContext`. Use for approval gates, secret redaction,
  blast-radius checks. Example: block `edit/create` without an approval artifact.
- **`postToolUse` — cleanup door.** Run formatters, update hash manifests,
  trigger tests after the tool finishes.
- **`userPromptSubmitted` / `sessionStart` / `sessionEnd` — logbook doors.**
  Inject context at session start, write audit logs at the end.
  Those logs feed `harness/13-trajectory-observability`.
- **Custom agents** can declare hooks inline (`hooks:`) or opt into shared repo hooks.
  Untrusted file hooks don't load by default — opt in only when you trust the folder.

## Test it on your machine first

Fake one tool call, pipe it into your script, check the JSON answer:

> 📄 **Example code:** [`examples/03-test-it-on-your-machine-first.sh`](examples/03-test-it-on-your-machine-first.sh)

Three usual mistakes: file outside `.github/hooks/`, missing `"version": 1`,
script not `chmod +x`. For approval doors remember **fail-closed**:
on error or timeout, block — don't wave through (timeout-deny).
