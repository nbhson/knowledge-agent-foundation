# ❓ FAQ — Safety & Loop Design Checklist (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).
(Glossary used throughout: a **loop** = an agent task that runs on a schedule. **State file** (e.g. `STATE.md`) = the loop's memory between runs. **Verifier** = a separate agent that tests the implementer's work. **Implementer** = the agent that writes the fix. **Gate** = a mandatory approval stop. **Worktree** = a separate git copy of the repo, so the agent never touches your main checkout.)

---

## Q1. My cleanup loop auto-merged at 2am and it included a change to `auth/**` — how do I stop that happening again? [→ §2.1 Path Denylist, §2.2 Auto-Merge Policy]

This answer explains why a "harmless cleanup" loop can touch sensitive code, and how to make that mechanically impossible.

**What you see**

You enabled auto-merge for a "trivial cleanup" loop. Overnight it opened a pull request, and the diff contains three files: two comment typo fixes — and one edit inside `auth/`, the exact place you had told it never to touch. The gate you configured did not fire. You are now deciding whether to revert in a hurry.
(Glossary: **auto-merge** = the loop merges its own PR without asking. **Diff** = the list of changed lines. `auth/**` = "every file under the auth/ folder". **Revert** = undo the change.)

**Why**

Auto-merge without a path allowlist is on the quick red-flags list for a reason. The default is **no auto-merge**; the only exception is an explicit allowlist. And a denylist written only inside a skill prompt is a suggestion — it is enforced by whether the loop happened to read the sentence, which is not a security boundary.

**What to do**

1. Put the denylist in the **skills** as a hard sentence the implementer must honor:

```
.env, .env.*, **/secrets/**, **/credentials/**, **/*_key*, **/*_secret*
.terraform/**, k8s/production/**, **/migrations/**
auth/**, payments/**, billing/**
```

2. Enforce it **mechanically** from `gate.yaml`, not from the prompt. The `loop-gate` tool checks the changed file list and returns an exit code — 2 means escalate, 0 means proceed (`gate.yaml` = a config file the gate tool reads; exit code = the number a tool returns to say pass/fail, like a referee's signal).
(In plain terms: a rule inside a prompt is a *request*; a rule in `gate.yaml` is a *fence* — the agent cannot climb over it. Example setup:)

> 📄 **Example code:** [`examples/01-q1-my-cleanup-loop-auto-merged-at-2am.sh`](examples/01-q1-my-cleanup-loop-auto-merged-at-2am.sh)

3. Write the allowlist down as **policy-as-code**: versioned, reviewed, and checked by `gate check` before any merge. Keep it in `AGENTS.md` or `loop-auto-merge-allowlist.md`. (policy-as-code = writing your rules as a versioned file that tools check, instead of as a paragraph nobody enforces. allowlist = "whitelist" — the only paths auto-merge is ever allowed to touch.)
4. Keep the allowlist narrow — typos in comments and docs, lint auto-fixes in test files only, import ordering, config inside allowlisted `docs/` paths. Never: behavior changes, dependency version bumps, lockfile changes, anything on the denylist. (lint auto-fix = mechanical style cleanup, e.g. reordering imports; lockfile = the file that pins exact dependency versions.)
5. Remember there is no exception path for the denylist. Migration paths stay gated **unless a dedicated migration loop exists** (migration = a script that changes the database structure — wrong edits there can destroy data).

**Verify**

Put one denylisted file in a test patch and run `gate check`. It must exit 2 and create no merge. Then run the same command on an allowlisted docs typo and confirm exit 0.

> **One-line summary:** Auto-merge stays off by default; when allowed at all, it is fenced by a mechanically enforced path allowlist that is tested before you trust it.

---

## Q2. How do I know my loop is actually ready to run without me watching? [→ §1 Loop Design Checklist, Readiness Levels]

This answer explains how to score a loop's autonomy level honestly, before you let it run unsupervised.

**What you see**

A colleague asks whether their new issue-triage loop can go unattended overnight. You scroll the design doc, see a clear goal and a nice cadence, and say "yeah, looks fine." Then you remember the loop has no state file, and the verifier is literally the same agent session as the implementer.
(cadence = how often the loop runs; state file = the loop's memory between runs; verifier = the agent that checks the work; implementer = the agent that writes it.)

**Why**

Readiness is scored honestly against a checklist, and a loop missing verification is not ready to run unattended. The checklist has ten sections (§1–§10), and the readiness level tells you exactly which ones you must have passed. Guessing is how a green-looking loop merges bad code at 3am.

**What to do**

1. Score against the section that matches your claimed level. How to read it: "Level" = how much the loop may do on its own; "Checklist" = which checklist sections (§) must be passed for that level. For instance, L2 ("small auto-fixes with a verifier") requires sections §1 through §7.

| Level | Description | Checklist |
|---|---|---|
| L0 — Draft | Intent written down only | §1 |
| L1 — Report | Triage → state, no auto-action | §1–3, §5 |
| L2 — Assisted | Small auto-fixes with a verifier | §1–7 |
| L3 — Unattended | Runs without you watching | All sections |

2. Stop immediately if any **quick red flag** is true: more than 3 auto-fix attempts on the same pull request with no progress; the verifier is the same agent session as the implementer; there is no state file; notifications fire on every run regardless of findings; auto-merge is on without a path allowlist. (red flag = an instant "not safe" signal; path allowlist = the whitelist of paths auto-merge may touch.)
3. Complete the **pre-flight safety check** before L3: denylist in the skills, auto-merge off or strictly allowlisted, connector scopes reviewed, human gates documented in the pattern, kill switch documented. (pre-flight = like a pilot's checks before takeoff; connector scopes = which permissions each external tool token has, e.g. "read issues only"; kill switch = the one command that stops everything immediately.)
4. Be honest about §4 — implementer and verifier must be **two separate entities** (different agent, model, or instructions), the implementer must not be able to mark its own work done, and the verifier must run tests in isolation inside a worktree before approving. (In plain terms: the student may not grade their own exam.)

**Verify**

Have someone who did not build the loop read only the state file and the checklist. If they can name the readiness level and the evidence behind it, the score is real.

> **One-line summary:** A loop is ready to run alone only when it passes the checklist for its claimed level, trips no red flags, and has passed the pre-flight safety checks.

---

## Q3. The loop burned through a month's tokens in one night — can the agent just raise its own cap? [→ §8 Cost & Limits, §2.4 Human Gates]

This answer explains why token cost ran away and who is allowed to raise the spending limit (spoiler: only you).

**What you see**

You wake up to a bill that makes no sense. The loop retried a failing item over and over, spawned the full implementer-plus-verifier chain each time, and ran for six hours. Now it is stuck: `BlockedBudget` — budget exceeded. And the loop wants more budget to keep going.
(Glossary: **tokens** = the billing unit of model usage; **sub-agent chain** = helper agents (implementer + verifier) the loop spawns, each one a full model call.)

**Why**

Cost control is not a setting you configure once; it is a set of named artifacts the loop reads every run: **token budget estimated**, `loop-budget.md` with daily caps and a kill switch, `loop-run-log.md` as append-only history, and a `loop-budget` skill that checks spend at the **start and end of each run**. `BlockedBudget` is a legitimate branch of the state machine — the loop is doing its job. The rest is the missing caps.
(In plain terms: `loop-budget.md` = the spending limit file; append-only = new lines are added, existing lines are never edited or deleted, like a proper logbook; kill switch = the one command that stops everything.)

**What to do**

1. Set the hard caps before you need them: **max iterations** per item per run, **max auto-PRs** per day, and explicit **pause/kill criteria** (iteration = one fix attempt on the same item; auto-PR = a pull request the loop opens by itself).
2. Give the loop a bounded retry policy at the execution level — retry with a wait between tries, a circuit breaker, a timeout, and a hard cap on attempts before escalating. An ATM analogy helps here: a second try after "transaction error" is reasonable, fifty tries in a row is a runaway. (circuit breaker = a rule that cuts the power after repeated failures; escalate = hand the problem to a human.)
3. **Agents cannot raise caps in `loop-budget.md` on their own.** A human must approve and make the edit. At L3 the loop may only use the `budget-negotiator` skill to *request* more budget — the cap itself is a human gate.
4. Keep the append-only run log so cost spikes are explainable: `run_id`, `pattern`, `duration_s`, `items_found`, `actions_taken`, `escalations`, `tokens_estimate`, `outcome`.
5. Make notifications earn their place — ping a human only when action is actually needed, and define the inbox where ambiguous items land.

**Verify**

Set a deliberately tiny daily cap and let the loop hit it. Confirm the run ends in `BlockedBudget`, that no further sub-agent chain starts, and that the run log shows the spend at start and end.

> **One-line summary:** Cost is controlled by named files with hard caps that only a human can raise; `BlockedBudget` is the safety brake working as designed.

---

## Q4. My agent's CI token ended up in `STATE.md`, which is committed to the repo — what now? [→ §2.5 Secrets in Prompts & Logs, §7 Connectors]

This answer explains how secrets leak into state files and what to do the moment one does.

**What you see**

You open `STATE.md` to check on the loop and see a long base64 string under a "recent failure" note. The file is committed. Anyone with repo read access, and every CI log that echoes the state file, can now see it. The loop itself put it there — it copied a command line from a failing job into its notes.
(Glossary: a **token** = a secret password-like string a program uses to call an API. **base64** = just an encoding, not encryption — anyone can decode it. **committed** = saved permanently into the repository's history. **rotate** = replace the secret with a new one and invalidate the old.)

**Why**

State files and CI logs are both places secrets leak into by accident. The triage skill reads CI output and writes state, so anything printed by a failing job — including an echoed environment variable — travels straight into a committed file. This is why **no credentials ever belong in `STATE.md`**.
(In plain terms: a failing CI job often prints its own settings, e.g. `API_KEY=ghp_xyz...`; the loop copies that output into its notes; the notes get committed; now the secret is public to everyone who can read the repo.)

**What to do**

1. Rotate the exposed token first. Treat it as compromised the moment it is committed, not when someone reports it.
2. Never paste API keys into scheduler prompts. The prompt is durable, versioned, and often world-readable in the tool that stores the schedule.
3. Make redaction a step inside triage, before state is written — not a cleanup pass afterwards. The triage skill should redact before writing state. (redaction = masking secrets before saving, e.g. replacing them with `***`.)
4. Audit connector scopes, because a broad token is what made the leak possible. Use **dedicated bot accounts and tokens with minimal scopes**, per integration. How to read it: "Read" = what the token may look at; "Write" = what it may change. For instance, GitHub's token may read issues and PRs, but can only comment and label — it cannot merge by default.

| Connector | Read | Write |
|---|---|---|
| GitHub | issues, PRs, checks | comment, label (no merge by default) |
| Linear | team issues | comment, status (no delete) |
| Slack | channel history | post to `#loop-escalations` only |
| Database | — | no production writes from loops |

5. Add `.env*`, `**/secrets/**`, and `**/credentials/**` to the denylist so the loop cannot rewrite its own secret handling. (denylist = the blacklist of paths the loop must never touch — `.env*` = files like `.env` that hold local secrets.)

**Verify**

Grep the repository history and every `STATE.md` for the old token prefix and confirm zero hits after the rotate. Then confirm the connector token can still read tickets but cannot merge or delete.

> **One-line summary:** A committed secret is compromised the moment it lands — rotate immediately, redact before writing state, and give every connector a minimal-permission token.

---

## Q5. A flaky test keeps blocking my loop — should the agent just retry it or raise the timeout? [→ §2.6 Flake & Test Safety, §10 Safety, §2.9 Consensus Sandboxing]

This answer explains why retrying or loosening a flaky test hides a real problem, and what to do instead.

**What you see**

The loop's verifier rejects the same pull request on attempt 1, attempt 2, attempt 3, and escalates to you — every time because of a test that fails roughly one run in six. You are tempted to let the agent bump the timeout or mark the test as skipped so the pipeline goes green.
(Glossary: a **flaky test** = a test that fails randomly on code that has not changed — like a smoke detector that goes off when nobody is cooking. **Timeout** = how long a step may run before being declared failed. **Skip** = telling the pipeline to ignore a test.)

**Why**

Both shortcuts are explicitly on the unsafe list. **Don't disable tests to make CI green**, and **don't raise timeouts blindly without a root-cause note**. A flaky test that is retried until it passes is not fixed — it just moves the failure somewhere less visible. And in a loop the cost is multiplied, because the retry runs inside a full implementer-plus-verifier chain. (root-cause note = a written explanation of *why* it failed, e.g. "the test times out because the DB is slow on first boot".)

**What to do**

1. Quarantine the flaky test with an **explicit ticket plus human approval** — never silently, and never inside the same run that discovered it. (quarantine = move the test into a "known flaky" list so it no longer blocks, with a ticket (a tracked task) saying why.)
2. If you must raise a timeout, attach a root-cause note in the ticket and in state. An unexplained timeout bump is indistinguishable from hiding a real failure.
3. Tighten the loop instead of loosening it: cap max iterations per item per run so one flaky test cannot consume the whole daily budget, and treat "3 attempts, no progress" as a quick red flag worth fixing before continuing.
4. Where a change is genuinely risky, add a second opinion. `loop-sandbox` gives one run an ephemeral git worktree and captures changes as reviewable patch files before applying; `loop-swarm` runs several sequential sandboxes and requires **byte-identical patch consensus** between runs before accepting edits. (In plain terms: sandbox = a throwaway copy of the repo where a risky run can happen without touching anything real; patch file = a small text description of exactly what changed; byte-identical consensus = two independent runs must produce exactly the same change — if they disagree, a human looks.)
5. Route anything touching security, authentication, authorization, payments, billing, personal data, infrastructure, or dependency upgrades to a human gate. Dependency upgrades in particular carry supply chain risk and are never a loop's call. (supply chain risk = a malicious or broken *upstream* package slipping in through a routine update.)

**Verify**

Run the loop against the flaky test ten times with no retries and no skips enabled. The escalations should be honest and cheap, and the ticket should exist before the first escalation — not after.

> **One-line summary:** Never silence a flaky test to go green — quarantine it with a ticket and human approval, cap retries, and route risky areas to humans.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
