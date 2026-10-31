# 🛡️ 03. Safety & Loop Design Checklist

> Loops make your judgment stronger — for better or worse. This section covers the **Loop Design Checklist** (the production readiness rubric) and **Safety & Guardrails** (the minimum you need for production loops that touch code or external systems).
>
> How to read this file: each `§` is one checklist area (e.g. §4 = who builds vs who checks). Checkboxes = things to tick before going live. A *loop* = an agent that runs on a schedule and acts without you clicking "run" each time — so a mistake repeats until you stop it. That is why the safety bar here is higher than for one-off agent runs.

---

## 1. Loop Design Checklist

This section explains: what to check before you let a loop run on its own in production. Use it before you switch a loop on. Please score **honestly** — a loop without verification is not ready to run on its own.

### §1 Purpose & Scope
- [ ] **One clear goal** — in one sentence: what does this loop accomplish?
- [ ] **Explicit non-goals** — what will this loop *not* do?
- [ ] **Watched scope** — which repos, branches, PRs, tickets? (= a bounded list of what it may look at)
- [ ] **Phased rollout** — report-only first, then act?
- [ ] **Ambiguous input handled** — when a work item is too vague to verify "done", the loop clarifies or escalates instead of guessing (scaffold an `loop-intake` skill)

> **One-line summary:** Write down exactly what the loop does, does not do, and may touch — vague loops guess, and guessing at scale is damage.

### §2 Scheduling
- [ ] **Cadence chosen** — does the interval match the urgency? (cadence = how often it runs)
- [ ] **Fire immediately** — run the first time now or wait for the interval?
- [ ] **Durable** — does it survive restarts?
- [ ] **Off-hours behavior** — slower cadence or pause overnight?
- [ ] **Self-cleanup** — `scheduler_delete` (the command that removes a scheduled loop) when the watchlist is empty?

> **One-line summary:** Set how often the loop runs, make it survive restarts, and make it delete itself when there is nothing left to watch.

### §3 Skills
- [ ] **Triage skill** (= the skill that sorts incoming items into buckets) exists with a strict output format
- [ ] **Action skills** (minimal-fix...) match project conventions
- [ ] **Skill descriptions** are boring + specific (good for auto-triggering)
- [ ] **Build/test commands** are written down in skills / AGENTS.md

> **One-line summary:** Give the loop boring, specific skills with fixed output formats and written-down build/test commands — creativity is not what you want from a repeat process.

### §4 Maker / Checker Split
- [ ] **Implementer** and **verifier** are two separate entities (agent, model, or instructions) (implementer = writes the change; verifier = checks it)
- [ ] The implementer **cannot** mark its own work "done"
- [ ] The verifier runs **tests** in isolation (worktree = a separate working copy of the repo, so experiments cannot touch your real files) before approving
- [ ] `/goal` or equivalent uses a **fresh model** for the stop condition

> **One-line summary:** Whoever writes the change must never be the one who approves it — that is the same trust problem as students grading their own exams.

### §5 State / Memory
- [ ] **State file** or board schema is documented
- [ ] The loop **reads** old state at the start of each run
- [ ] The loop **writes** outcomes, timestamps, last actions
- [ ] **Prunes** (= removes) resolved/merged/closed items every run
- [ ] Human overrides are recorded in state

> **One-line summary:** The state file is the loop's memory — it must read it, update it, and clean it every run, or the loop forgets and repeats work.

### §6 Human Handoff
- [ ] **Escalation triggers** are explicit (max attempts, risky paths, ambiguity) (escalate = stop and ask a human)
- [ ] **Denylist paths** — auth, payments, secrets, infra (denylist = "blacklist" of files the loop must never touch)
- [ ] **Notification rule** — ping a human only when action is needed
- [ ] **Inbox** — where ambiguous items land

> **One-line summary:** Define in advance what forces a human review, which paths are off-limits, and where unsure items wait — so escalation is a rule, not a judgment call.

### §7 Connectors (MCP)
- [ ] Minimum permissions (read vs write) (MCP = Model Context Protocol, the standard way agents plug into external tools like GitHub or Slack)
- [ ] The loop can **open/update PRs** or tickets if it is acting
- [ ] Clear bot identity on PR comments (e.g. "Loop Engineering — PR Babysitter" = label the comments with a clear bot name, so people know a loop wrote them)

> **One-line summary:** Connect each external tool with the fewest permissions possible, and label the bot clearly so humans know who is commenting.

### §8 Cost & Limits
- [ ] **Token budget** estimated (tokens = word-pieces you pay for; budget = a spending cap)
- [ ] **`loop-budget.md`** with daily caps + kill switch
- [ ] **`loop-run-log.md`** for append-only run history (append-only = you only ever add lines, never edit old ones)
- [ ] **`loop-budget` skill** checks spend at start/end of each run
- [ ] **Max iterations** per item per run
- [ ] **Max auto-PRs** per day (cleanup loops)
- [ ] **Pause/kill criteria** defined (kill switch = one command that stops all loops now)

> **One-line summary:** Cap the spend and the retries in writing before launch, and keep a kill switch — an unbounded loop is an open tab on your invoice and your repo.

### §9 Observability
- [ ] Log each run: started, items found, actions taken, escalations
- [ ] **Success metrics** chosen
- [ ] The team can **inspect the state file** without reading chat logs

> **One-line summary:** Log every run and define success metrics, so anyone can answer "what did the loop do today?" from one file.

### §10 Safety
- [ ] No auto-merge without an explicit allowlist (allowlist = "whitelist": only named paths may merge automatically)
- [ ] Secrets/env files are on the denylist
- [ ] Flake handling — don't "fix" flaky tests with retries (flaky test = a test that randomly passes and fails on the same code)

> **One-line summary:** Merge only from an explicit allowlist, never touch secret files, and never mask flaky tests with retries.

### Readiness Levels

How to read this table: each row is a maturity level. **Level** = the name, **Description** = what the loop is allowed to do at that level, **Checklist** = which `§` sections you must pass to claim it. For instance, L1 means the loop may triage and write reports, but never act on its own.

| Level | Description | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Intent written down only | §1 |
| **L1 — Report** | Triage → state, no auto-action | §1–3, §5 |
| **L2 — Assisted** | Small auto-fixes with a verifier | §1–7 |
| **L3 — Unattended** | Runs without you watching | All sections |

> **One-line summary:** Climb the levels in order — L3 ("runs alone") is only earned when every checklist section passes.

### Quick Red Flags

Please stop and fix things first if you see any of these:
- The same PR has > 3 auto-fix attempts with no progress (the loop is stuck in a loop)
- The verifier is **the same agent session** as the implementer (no real checker)
- There is no state file — the loop loses its memory every run
- Notifications on every run regardless of findings (alert fatigue → humans stop reading)
- Auto-merge on without a path allowlist

> **One-line summary:** Any of these five signs means the loop is not safe to leave running — stop and fix before adding more automation.

---

## 2. Safety & Guardrails

This section explains: the minimum guardrails for loops that edit code or talk to external systems. Guardrails = hard limits that stop the loop even if its instructions are wrong.

### 2.1 Path Denylist

A loop must **never** auto-edit these paths without human approval (= these are the files where one bad edit leaks secrets or breaks production):

```
.env
.env.*
**/secrets/**
**/credentials/**
**/*_key*
**/*_secret*
.terraform/**
k8s/production/**
**/migrations/**          # unless a dedicated migration loop exists
auth/**
payments/**
billing/**
```

Please put this rule in the `minimal-fix` and implementer skills:

> Do not modify files matching the denylist. Escalate to a human with context.

The `loop-gate` tool enforces this denylist **automatically** from `gate.yaml` (a config file listing forbidden paths; automatic means it does not depend on whether the loop has read the file):

> 📄 **Example code:** [`examples/01-2-1-path-denylist.sh`](examples/01-2-1-path-denylist.sh)

> **One-line summary:** Secrets, credentials, infra, and payment paths are never auto-edited — the gate blocks them by config, not by trust.

### 2.2 Auto-Merge Policy

**Default: no auto-merge.** (auto-merge = the loop's pull request merges into the main branch without a human clicking approve)

If you allow auto-merge for simple loops:

How to read this table: **Allowed** = changes a loop may merge by itself; **Not allowed** = look-alike changes that must always get a human. For instance, fixing a typo in a comment is safe; bumping a dependency version looks equally small but can break everything.

| Allowed | Not allowed |
|-----------|-----------------|
| Typos in comments/docs | Behavior changes |
| Lint auto-fixes in test files only | Dependency version bumps |
| Import ordering | Lockfile changes |
| Config in allowlisted `docs/` paths | Any denylist path |

Please write down the allowlist in `AGENTS.md` or `loop-auto-merge-allowlist.md`.

> 🔑 **Policy / Permission highlight:** this is a **merge-permission policy** — auto-merge is off by default, and an explicit allowlist is the only exception. Please treat the allowlist file as policy-as-code: versioned, reviewed, and checked by `gate check` before any merge.

> **One-line summary:** Auto-merge is off by default; only tiny, cosmetic changes on an explicit allowlist may merge without a human.

### 2.3 MCP Connector Least Privilege

How to read this table: one row per integration (connector). **Read** = what it may look at; **Write** = the few actions it may perform. For instance, the GitHub connector may comment and label PRs but never merge by default.

| Connector | Read | Write |
|-----------|------|-------|
| GitHub | issues, PRs, checks | comment, label (no merge by default) |
| Linear | team issues | comment, status (no delete) |
| Slack | channel history | post to `#loop-escalations` only |
| Database | — | no production writes from loops |

Please use dedicated bot accounts / tokens with the smallest scopes you need (least privilege = each tool gets only the permissions it truly needs, nothing spare).

> 🔑 **Policy / Permission highlight:** this is a **connector-permission policy** (least privilege for each integration) — every MCP connector only gets the read/write scopes it really needs, on its own dedicated identity. Mirrors `12-sandbox-execution` §6 (per-role matrix) and `06` §8 (RBAC levels).

> **One-line summary:** Give every connector its own bot account with read-only-by-default scopes — a leaked token then exposes as little as possible.

### 2.4 Human Gates

This section explains: situations where the loop must stop and wait for a human, no matter how confident it feels.

Please always ask a human to step in for:
- Security, authentication, authorization (login and permission code — a wrong edit locks everyone out or lets everyone in)
- Payments, billing, PII handling (PII = personal data like names and emails; leaking it is usually a legal problem)
- Infrastructure / Terraform / K8s production (Terraform/K8s = tools that create and run your servers — a bad change takes down services)
- Dependency upgrades (supply chain risk — a new package version can carry malware or break builds)
- Changes touching > N files (suggested N=10)
- A third failure on the same item
- Token budget extensions: agents **cannot** raise caps in `loop-budget.md` by themselves — a human must approve and make the edit. (L3 loops use the `budget-negotiator` skill to *request* more budget.)

> **One-line summary:** Money, logins, infrastructure, supply chain, big changes, repeated failures, and budget raises are human-only decisions.

### 2.5 Secrets in Prompts & Logs

- Never paste API keys into scheduler prompts (the prompt text may be stored or logged elsewhere)
- CI logs can contain secrets — the triage skill should redact them (= mask them, e.g. `sk-***`) before writing state
- State files are often committed — **no credentials in `STATE.md`** (committed = saved into git, where anyone with repo access can read them)

> **One-line summary:** Assume every prompt, log, and state file will be read by someone else one day — so no secret ever goes into any of them.

### 2.6 Flake & Test Safety

- Don't disable tests just to make CI green (CI = the automated build-and-test pipeline; green = passing)
- Don't raise timeouts without a note about the root cause
- Please quarantine flakes with an explicit ticket + human approval (quarantine = move the flaky test aside, marked, instead of deleting it)

> **One-line summary:** A flaky test is a signal, not an obstacle — investigate or quarantine it with a ticket; never silence it to see green.

### 2.7 Incident Response

This section explains: what to do in the first minutes after a loop merges bad code.

If a loop merges bad code:
1. **Pause all loops right away** (`scheduler_list` → delete) — stop the bleeding before diagnosing
2. Revert the merge (revert = create a new commit that undoes the bad one)
3. Write it up in state + `stories/`
4. Make the verifier stricter or shrink the scope before restarting

> **One-line summary:** When a loop ships a bad merge: stop all loops, revert, document, tighten the verifier — in that order.

### 2.8 Pre-Flight Safety Check (before L3)

This section explains: the final five-box tick before letting a loop run fully unattended (L3).

- [ ] Denylist in the skills
- [ ] Auto-merge off or strict allowlist
- [ ] Connector scopes reviewed
- [ ] Human gates documented in the pattern
- [ ] Kill switch documented

> **One-line summary:** Unattended mode (L3) starts only after all five safety boxes are ticked and written down.

### 2.9 Worktree Isolation & Consensus Sandboxing

This section explains: how to contain the blast radius of loop edits before they touch your real branch.

- **`loop-sandbox`**: Ephemeral git worktree isolation for single agent runs (ephemeral = created for one run, thrown away after). Captures changes as reviewable patch files before applying them — so nothing lands directly in your working copy.
- **`loop-swarm`**: Multi-agent consensus sandboxing across sequential `loop-sandbox` runs. Requires **byte-identical patch consensus** between runs before accepting edits (several independent agents must produce exactly the same patch, byte for byte — if they disagree, the change is not trusted).

> **One-line summary:** Run edits in a throwaway worktree and, for critical changes, require multiple agents to agree on the exact same patch before anything is applied.

---

*Next: [04 — Operating Loops](../04-operating/) → [05 — Multi-Loop Coordination](../05-multi-loop/)*
