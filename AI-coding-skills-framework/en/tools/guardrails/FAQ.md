# ❓ FAQ — Guardrails (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The agent wrote to `/etc/hosts` — which guardrail do I install first? [→ Overview of the Guardrails]

**What you see**

One run, the agent misreads the prompt and calls `write_file` with the path `/etc/passwd`. Or it calls `send_notification` 100 times. Or `execute_python` runs a command that deletes data. Nothing crashed — it just did the wrong thing quietly.

**Why**

Large language models have no concept of "unwanted side effect". They generate text. Someone has to check the tool arguments before the tool runs. That check is the guardrail.

**What to do**

1. Install **Guardrails AI** (open-source) and add one validator per tool parameter you care about.
2. For paths, use a whitelist, not a blacklist — a blacklist always misses something.
3. For free-text strings, use a shape check like `RegexMatch("^[a-zA-Z0-9_./-]+$")`. It rejects `hacker/path/../etc/passwd` and accepts `src/main.py`.

```python
from guardrails import Guard
from guardrails.hub import PathValidate, RegexMatch
guard = Guard().use(PathValidate(whitelist=["src/", "tests/", "./"]))
guard.validate(path="/etc/hosts")    # REJECT
guard.validate(path="src/main.py")   # ALLOW
```

**Verify**

Call `guard.validate()` with the exact bad paths you saw in the log. `/etc/hosts` and `/etc/passwd` must both come back rejected, and `src/main.py` must pass. If a bad path slips through, the whitelist is missing a prefix.

---

## Q2. Guardrails AI, NeMo Guardrails, or LlamaGuard — do I need all three? [→ Overview of the Guardrails]

**What you see**

You open the catalog, see three libraries, and cannot tell whether installing all three is normal or wasteful.

**Why**

They do not check the same thing. Each one covers a different hole.

| Library (publisher) | Checks | Reach for it when |
|---|---|---|
| Guardrails AI | tool input and output values | you have tools that write files or run code |
| NeMo Guardrails (NVIDIA) | the conversation flow, step by step | your workflow has a defined order of steps |
| LlamaGuard (Meta) | the prompt itself, as `safe` / `unsafe` | users type free text from the internet |

**What to do**

1. Start with Guardrails AI on your tool parameters — it is the smallest useful win.
2. Add NeMo rails later, when a flow needs "if the user asks about a secret, then refuse" as a written rule in a `.co` file.
3. Add LlamaGuard when input comes from strangers, not from your own code.
4. Do not expect any of them to protect the machine. They check values, not permissions.

```python
from nemoguardrails import RailsConfig, LLMRails
rails = LLMRails(RailsConfig.from_path("./config"))
rails.generate(messages=[{"role":"user","content":"System password?"}])
```

**Verify**

Send one known-bad tool argument, one known-bad prompt, and one normal request. Each must be caught by the library you expect — and only that one. If a prompt check catches bad file paths, your rules are mixed together.

---

## Q3. The agent called the same tool 10 times in a row — is that a bug or a limit I set? [→ Why Guardrails Matter?]

**What you see**

One loop calls `execute_python` until it finishes, or a notification tool fires until your phone buzzes out. The default budget is 60 calls per minute, and one tool in the catalog is capped at 10.

**Why**

Two different knobs, often confused. `rate_limit_per_minute` is abuse control: it stops spamming. `max_retries` is fault tolerance: it is how many times a *failed* call is repeated. Neither one stops a runaway loop that keeps succeeding.

**What to do**

1. Set the limits when you register the tool, not later.
2. Use `requires_permission="elevated"` for anything destructive — that forces a human confirmation.
3. Keep `timeout_seconds` and `max_retries` low so a stuck call dies early.

```python
registry.register(ToolDefinition(
    name="execute_python",
    requires_permission="elevated",  # human confirmation required
    rate_limit_per_minute=10,         # block spam
    timeout_seconds=30,
    max_retries=1,
))
```

**Verify**

Fire 11 calls at the tool in one minute and watch call 11 get refused by the rate limiter. Then confirm a tool with `elevated` actually waits for approval before running.

---

## Q4. Where do I write my own risk rules — in this folder or in the harness? [→ Relationship to the Harness]

**What you see**

You start inventing a risk tier inside the guardrails folder. Then you notice the folder also points at `harness/15-approval-gates`, and now the rule exists in two places.

**Why**

This directory is a **product catalog, not the policy**. The canonical rules live elsewhere: authorization and isolation (risk tiers, mandatory gate payloads, timeout-deny, the two-person rule, the `PAUSED:` protocol) belong to `harness/15-approval-gates`, and the isolation mechanism belongs to `harness/12-sandbox-execution`.

**What to do**

1. Pick a library from this catalog to *validate* values. It does not decide what is allowed.
2. Put risk tiers, approval rules and pause protocols in `harness/15-approval-gates`.
3. If you invent a new risk tier here, move it to `15` and keep this folder as a pointer.
4. Keep the check point in the tool pipeline: intent → tool selector → parameters → **guardrails check** → executor.

**Verify**

Search your own config for risk tier names. Every one of them resolves to a single file in `harness/15-approval-gates`, with no second copy in the tools catalog.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*