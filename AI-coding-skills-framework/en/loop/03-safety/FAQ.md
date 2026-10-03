# ❓ FAQ — Safety & Loop Design Checklist (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My cleanup loop auto-merged at 2am and it included a change to `auth/**` — how do I stop that happening again? [→ §2.1 Path Denylist, §2.2 Auto-Merge Policy]

**What you see**

You enabled auto-merge for a "trivial cleanup" loop. Overnight it opened a pull request, and the diff contains three files: two comment typo fixes — and one edit inside `auth/`, the exact place you had told it never to touch. The gate you configured did not fire. You are now deciding whether to revert in a hurry.

**Why**

Auto-merge without a path allowlist is on the quick red-flags list for a reason. The default is **no auto-merge**; the only exception is an explicit allowlist. And a denylist written only inside a skill prompt is a suggestion — it is enforced by whether the loop happened to read the sentence, which is not a security boundary.

**What to do**

1. Put the denylist in the **skills** as a hard sentence the implementer must honor:

```
.env, .env.*, **/secrets/**, **/credentials/**, **/*_key*, **/*_secret*
.terraform/**, k8s/production/**, **/migrations/**
auth/**, payments/**, billing/**
```

2. Enforce it **mechanically** from `gate.yaml`, not from the prompt. The `loop-gate` tool checks the changed file list and returns an exit code — 2 means escalate, 0 means proceed:

```bash
npx @cobusgreyling/loop gate check --action auto-merge --paths <changed files>
# exit 2 = escalate to a human, exit 0 = proceed
```

3. Write the allowlist down as **policy-as-code**: versioned, reviewed, and checked by `gate check` before any merge. Keep it in `AGENTS.md` or `loop-auto-merge-allowlist.md`.
4. Keep the allowlist narrow — typos in comments and docs, lint auto-fixes in test files only, import ordering, config inside allowlisted `docs/` paths. Never: behavior changes, dependency version bumps, lockfile changes, anything on the denylist.
5. Remember there is no exception path for the denylist. Migration paths stay gated **unless a dedicated migration loop exists**.

**Verify**

Put one denylisted file in a test patch and run `gate check`. It must exit 2 and create no merge. Then run the same command on an allowlisted docs typo and confirm exit 0.

---

## Q2. How do I know my loop is actually ready to run without me watching? [→ §1 Loop Design Checklist, Readiness Levels]

**What you see**

A colleague asks whether their new issue-triage loop can go unattended overnight. You scroll the design doc, see a clear goal and a nice cadence, and say "yeah, looks fine." Then you remember the loop has no state file, and the verifier is literally the same agent session as the implementer.

**Why**

Readiness is scored honestly against a checklist, and a loop missing verification is not ready to run unattended. The checklist has ten sections (§1–§10), and the readiness level tells you exactly which ones you must have passed. Guessing is how a green-looking loop merges bad code at 3am.

**What to do**

1. Score against the section that matches your claimed level:

| Level | Description | Checklist |
|---|---|---|
| L0 — Draft | Intent written down only | §1 |
| L1 — Report | Triage → state, no auto-action | §1–3, §5 |
| L2 — Assisted | Small auto-fixes with a verifier | §1–7 |
| L3 — Unattended | Runs without you watching | All sections |

2. Stop immediately if any **quick red flag** is true: more than 3 auto-fix attempts on the same pull request with no progress; the verifier is the same agent session as the implementer; there is no state file; notifications fire on every run regardless of findings; auto-merge is on without a path allowlist.
3. Complete the **pre-flight safety check** before L3: denylist in the skills, auto-merge off or strictly allowlisted, connector scopes reviewed, human gates documented in the pattern, kill switch documented.
4. Be honest about §4 — implementer and verifier must be **two separate entities** (different agent, model, or instructions), the implementer must not be able to mark its own work done, and the verifier must run tests in isolation inside a worktree before approving.

**Verify**

Have someone who did not build the loop read only the state file and the checklist. If they can name the readiness level and the evidence behind it, the score is real.

---

## Q3. The loop burned through a month's tokens in one night — can the agent just raise its own cap? [→ §8 Cost & Limits, §2.4 Human Gates]

**What you see**

You wake up to a bill that makes no sense. The loop retried a failing item over and over, spawned the full implementer-plus-verifier chain each time, and ran for six hours. Now it is stuck: `BlockedBudget` — budget exceeded. And the loop wants more budget to keep going.

**Why**

Cost control is not a setting you configure once; it is a set of named artifacts the loop reads every run: **token budget estimated**, `loop-budget.md` with daily caps and a kill switch, `loop-run-log.md` as append-only history, and a `loop-budget` skill that checks spend at the **start and end of each run**. `BlockedBudget` is a legitimate branch of the state machine — the loop is doing its job. The rest is the missing caps.

**What to do**

1. Set the hard caps before you need them: **max iterations** per item per run, **max auto-PRs** per day, and explicit **pause/kill criteria**.
2. Give the loop a bounded retry policy at the execution level — retry with a wait between tries, a circuit breaker, a timeout, and a hard cap on attempts before escalating. An ATM analogy helps here: a second try after "transaction error" is reasonable, fifty tries in a row is a runaway.
3. **Agents cannot raise caps in `loop-budget.md` on their own.** A human must approve and make the edit. At L3 the loop may only use the `budget-negotiator` skill to *request* more budget — the cap itself is a human gate.
4. Keep the append-only run log so cost spikes are explainable: `run_id`, `pattern`, `duration_s`, `items_found`, `actions_taken`, `escalations`, `tokens_estimate`, `outcome`.
5. Make notifications earn their place — ping a human only when action is actually needed, and define the inbox where ambiguous items land.

**Verify**

Set a deliberately tiny daily cap and let the loop hit it. Confirm the run ends in `BlockedBudget`, that no further sub-agent chain starts, and that the run log shows the spend at start and end.

---

## Q4. My agent's CI token ended up in `STATE.md`, which is committed to the repo — what now? [→ §2.5 Secrets in Prompts & Logs, §7 Connectors]

**What you see**

You open `STATE.md` to check on the loop and see a long base64 string under a "recent failure" note. The file is committed. Anyone with repo read access, and every CI log that echoes the state file, can now see it. The loop itself put it there — it copied a command line from a failing job into its notes.

**Why**

State files and CI logs are both places secrets leak into by accident. The triage skill reads CI output and writes state, so anything printed by a failing job — including an echoed environment variable — travels straight into a committed file. This is why **no credentials ever belong in `STATE.md`**.

**What to do**

1. Rotate the exposed token first. Treat it as compromised the moment it is committed, not when someone reports it.
2. Never paste API keys into scheduler prompts. The prompt is durable, versioned, and often world-readable in the tool that stores the schedule.
3. Make redaction a step inside triage, before state is written — not a cleanup pass afterwards. The triage skill should redact before writing state.
4. Audit connector scopes, because a broad token is what made the leak possible. Use **dedicated bot accounts and tokens with minimal scopes**, per integration:

| Connector | Read | Write |
|---|---|---|
| GitHub | issues, PRs, checks | comment, label (no merge by default) |
| Linear | team issues | comment, status (no delete) |
| Slack | channel history | post to `#loop-escalations` only |
| Database | — | no production writes from loops |

5. Add `.env*`, `**/secrets/**`, and `**/credentials/**` to the denylist so the loop cannot rewrite its own secret handling.

**Verify**

Grep the repository history and every `STATE.md` for the old token prefix and confirm zero hits after the rotate. Then confirm the connector token can still read tickets but cannot merge or delete.

---

## Q5. A flaky test keeps blocking my loop — should the agent just retry it or raise the timeout? [→ §2.6 Flake & Test Safety, §10 Safety, §2.9 Consensus Sandboxing]

**What you see**

The loop's verifier rejects the same pull request on attempt 1, attempt 2, attempt 3, and escalates to you — every time because of a test that fails roughly one run in six. You are tempted to let the agent bump the timeout or mark the test as skipped so the pipeline goes green.

**Why**

Both shortcuts are explicitly on the unsafe list. **Don't disable tests to make CI green**, and **don't raise timeouts blindly without a root-cause note**. A flaky test that is retried until it passes is not fixed — it just moves the failure somewhere less visible. And in a loop the cost is multiplied, because the retry runs inside a full implementer-plus-verifier chain.

**What to do**

1. Quarantine the flaky test with an **explicit ticket plus human approval** — never silently, and never inside the same run that discovered it.
2. If you must raise a timeout, attach a root-cause note in the ticket and in state. An unexplained timeout bump is indistinguishable from hiding a real failure.
3. Tighten the loop instead of loosening it: cap max iterations per item per run so one flaky test cannot consume the whole daily budget, and treat "3 attempts, no progress" as a quick red flag worth fixing before continuing.
4. Where a change is genuinely risky, add a second opinion. `loop-sandbox` gives one run an ephemeral git worktree and captures changes as reviewable patch files before applying; `loop-swarm` runs several sequential sandboxes and requires **byte-identical patch consensus** between runs before accepting edits.
5. Route anything touching security, authentication, authorization, payments, billing, personal data, infrastructure, or dependency upgrades to a human gate. Dependency upgrades in particular carry supply chain risk and are never a loop's call.

**Verify**

Run the loop against the flaky test ten times with no retries and no skips enabled. The escalations should be honest and cheap, and the ticket should exist before the first escalation — not after.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
