# ❓ FAQ — Guardrails (Real Stories, Plain Language)

This file answers real questions about **guardrails** — automatic checks that stop the agent before it does something harmful. If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The agent wrote to `/etc/hosts` — which guardrail do I install first? [→ Overview of the Guardrails]

This question is about the first guardrail to install: a value check on tool arguments, before any tool runs.

**What you see**

One run, the agent misreads the prompt and calls `write_file` with the path `/etc/passwd` (a critical system file listing all users). Or it calls `send_notification` 100 times. Or `execute_python` runs a command that deletes data. Nothing crashed — it just did the wrong thing quietly.

**Why**

Large language models have no concept of "unwanted side effect". They generate text. Someone has to check the tool arguments before the tool runs. That check is the guardrail (guardrail = an automatic safety check between the model and the tool).

**What to do**

1. Install **Guardrails AI** (an open-source library of validators) and add one validator per tool parameter you care about.
2. For paths, use a whitelist, not a blacklist — whitelist = only listed paths are allowed (a "danh sách trắng"); blacklist = listed paths are banned, and a blacklist always misses something.
3. For free-text strings, use a shape check like `RegexMatch("^[a-zA-Z0-9_./-]+$")`. It rejects `hacker/path/../etc/passwd` and accepts `src/main.py`.

> 📄 **Example code:** [`examples/01-q1-the-agent-wrote-to-etc-hosts-which.py`](examples/01-q1-the-agent-wrote-to-etc-hosts-which.py)

**Verify**

Call `guard.validate()` (the library's check function) with the exact bad paths you saw in the log. `/etc/hosts` and `/etc/passwd` must both come back rejected, and `src/main.py` must pass. If a bad path slips through, the whitelist is missing a prefix.

> **One-line summary:** Start with a whitelist validator on file paths so bad arguments are rejected before the tool ever runs.

---

## Q2. Guardrails AI, NeMo Guardrails, or LlamaGuard — do I need all three? [→ Overview of the Guardrails]

This question is about whether three safety libraries are three separate purchases or three overlapping products. The answer: they check different layers.

**What you see**

You open the catalog, see three libraries, and cannot tell whether installing all three is normal or wasteful.

**Why**

They do not check the same thing. Each one covers a different hole.

How to read it: each row is one library; "Checks" says what it inspects; "Reach for it when" says the situation that justifies installing it. For instance, LlamaGuard only looks at the incoming text, so it cannot stop a bad file path.

| Library (publisher) | Checks | Reach for it when |
|---|---|---|
| Guardrails AI | tool input and output values | you have tools that write files or run code |
| NeMo Guardrails (NVIDIA) | the conversation flow, step by step | your workflow has a defined order of steps |
| LlamaGuard (Meta) | the prompt itself, as `safe` / `unsafe` | users type free text from the internet |

**What to do**

1. Start with Guardrails AI on your tool parameters — it is the smallest useful win.
2. Add NeMo rails later, when a flow needs "if the user asks about a secret, then refuse" as a written rule in a `.co` file (`.co` = NeMo Guardrails' Colang rule file, written in plain "rails" syntax).
3. Add LlamaGuard when input comes from strangers, not from your own code.
4. Do not expect any of them to protect the machine. They check values, not permissions (permissions = the operating system's rules on who may read, write or execute what).

> 📄 **Example code:** [`examples/02-q2-guardrails-ai-nemo-guardrails-or-llamaguard-do.py`](examples/02-q2-guardrails-ai-nemo-guardrails-or-llamaguard-do.py)

**Verify**

Send one known-bad tool argument, one known-bad prompt, and one normal request. Each must be caught by the library you expect — and only that one. If a prompt check catches bad file paths, your rules are mixed together.

> **One-line summary:** Install one library per layer — values (Guardrails AI), conversation flow (NeMo), incoming prompts (LlamaGuard) — and never all three at once by default.

---

## Q3. The agent called the same tool 10 times in a row — is that a bug or a limit I set? [→ Why Guardrails Matter?]

This question is about telling two limits apart that look similar but do different jobs: spam control and retry control.

**What you see**

One loop calls `execute_python` until it finishes, or a notification tool fires until your phone buzzes out. The default budget is 60 calls per minute, and one tool in the catalog is capped at 10.

**Why**

Two different knobs, often confused. `rate_limit_per_minute` is abuse control: it stops spamming (spamming = hammering the same call over and over). `max_retries` is fault tolerance: it is how many times a *failed* call is repeated. Neither one stops a runaway loop that keeps succeeding.

**What to do**

1. Set the limits when you register the tool, not later.
2. Use `requires_permission="elevated"` for anything destructive — that forces a human confirmation.
3. Keep `timeout_seconds` (how long one call may run) and `max_retries` low so a stuck call dies early.

> 📄 **Example code:** [`examples/03-q3-the-agent-called-the-same-tool-10.py`](examples/03-q3-the-agent-called-the-same-tool-10.py)

**Verify**

Fire 11 calls at the tool in one minute and watch call 11 get refused by the rate limiter. Then confirm a tool with `elevated` actually waits for approval before running.

> **One-line summary:** Rate limit stops spam, max_retries limits failed retries, and destructive tools need a human gate — none of them alone stops a loop that keeps succeeding.

---

## Q4. Where do I write my own risk rules — in this folder or in the harness? [→ Relationship to the Harness]

This question is about where risk rules *live*, so you do not end up with two conflicting copies.

**What you see**

You start inventing a risk tier (risk tier = a severity label like low/medium/high) inside the guardrails folder. Then you notice the folder also points at `harness/15-approval-gates`, and now the rule exists in two places.

**Why**

This directory is a **product catalog, not the policy**. The canonical rules (canonical = the one official copy everyone must follow) live elsewhere: authorization and isolation (risk tiers, mandatory gate payloads, timeout-deny, the two-person rule, the `PAUSED:` protocol) belong to `harness/15-approval-gates`, and the isolation mechanism (running risky code in a locked-down box) belongs to `harness/12-sandbox-execution`.

**What to do**

1. Pick a library from this catalog to *validate* values. It does not decide what is allowed.
2. Put risk tiers, approval rules and pause protocols in `harness/15-approval-gates`.
3. If you invent a new risk tier here, move it to `15` and keep this folder as a pointer.
4. Keep the check point in the tool pipeline: intent → tool selector → parameters → **guardrails check** → executor.

**Verify**

Search your own config for risk tier names. Every one of them resolves to a single file in `harness/15-approval-gates`, with no second copy in the tools catalog.

> **One-line summary:** This folder only recommends validation tools; the actual risk policy belongs in harness/15-approval-gates — one copy, no duplicates.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
