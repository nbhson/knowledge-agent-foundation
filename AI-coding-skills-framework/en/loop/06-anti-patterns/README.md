# ⚠️ 06. Anti-Patterns & Failure Modes

> These are design mistakes to avoid **before** you let loops run on their own, plus a **catalog of the real ways loops actually break** and how to fix them.

---

## 1. Anti-Patterns (Design Mistakes)

This section lists ten design mistakes. Each row names the mistake, explains in plain words why it breaks, and gives the fix.

| # | Anti-Pattern | Why it breaks | Do this instead |
|---|--------------|--------------|----------|
| 1 | **Same agent implements AND verifies** | It grades its own homework — weak tests get stamped "approved" without a real check | Use a separate verifier agent or model; its default stance is REJECT |
| 2 | **No attempt cap** | "Just try until CI is green" means the loop retries forever and burns tokens | Hard cap (e.g. 3 tries), then stop and escalate with full context in state |
| 3 | **Vague triage output** | The loop cannot parse priorities; humans ignore STATE.md | Structured markdown, one-line items, an explicit `Suggested loop action` |
| 4 | **L3 before L1 quality** | The loop acts on bad signal; nobody can explain the changes it made | Week one: L1 report-only; measure triage accuracy before enabling L2 |
| 5 | **Shared state without a schema** | Three loops append to one unstructured STATE.md — state rots, entries conflict | One state file per pattern, or clearly separated sections with prune rules |
| 6 | **MCP with write-everything scope** | One bad triage decision can write anywhere in your systems | L1: read-only connectors; expand scope only after the loop earns trust |
| 7 | **No kill switch** | A loop runs 24/7 with no pause criteria — alert fatigue, budget overrun | Document pause/kill criteria in LOOP.md + the budget template |
| 8 | **Fixing flakes with code** | Masks infra problems; produces random diffs | Classify, then quarantine/retry policy, then escalate env/infra |
| 9 | **Auto-merge without an allowlist** | Security and business-logic bugs slip through weak verifiers | Explicit path allowlist; a human merges denylist paths |
| 10 | **No run log** | Only STATE.md exists, no history — you cannot debug later runs | Append to `loop-run-log.md` every run |

> **How to read this table:** the **#** column is just a row number, so other sections can refer back (for example, "anti-pattern 2"). **Anti-Pattern** = the mistake in short form. **Why it breaks** = the damage it causes, in plain words. **Do this instead** = the fix. For instance, row 9: *auto-merge* = the loop merges its own pull request without asking a human; *allowlist* = a whitelist of file paths the loop is allowed to touch or merge — everything else needs a human click. Row 2: a *cap* = a maximum number of retries; without one, a stuck loop tries forever and you pay for every try.

> **One-line summary:** Ten mistakes that break autonomous loops — separate the verifier, cap the retries, keep state clean, restrict write access, and always keep a kill switch and a run log.

---

## 2. Failure Mode Catalog

This section explains the real ways loops break in practice. Use it when you are debugging a misbehaving loop or writing a new pattern: find the symptom, read the causes, apply the mitigations.

> **One-line summary:** Ten failure modes, each with symptom, severity, cause, and fix — find your symptom, apply its mitigation.

### Severity Classification

| Severity | Meaning |
|----------|-------|
| **S1 — Annoying** | Wastes time/tokens, no harm |
| **S2 — Harmful** | Wrong code merged, bad tickets, alert fatigue |
| **S3 — Critical** | Security, data loss, production incident |

> **How to read it:** every failure below is tagged S1, S2 or S3. S1 = annoying (wastes time or tokens, but nothing breaks). S2 = harmful (wrong code gets merged, the team gets noisy alerts). S3 = critical (security leaks, data loss, or the production site goes down). For example, a loop that burns tokens is S1; a loop that merges an unreviewed security bug is S3.

> **One-line summary:** S1 wastes time, S2 does real damage, S3 breaks production — every failure below carries one of these tags.

### 2.1 Infinite Fix Loop

- **Symptom**: The same PR or CI job gets auto-fixed 5+ times and never converges (*converges = the fixes stop changing anything because the problem is actually solved*).
- **Severity**: S2 — harmful.
- **Causes**: A weak verifier, or the verifier shares the implementer's session; the real cause was misdiagnosed (fixing symptoms); a flaky test was treated as a real regression.
- **Mitigations**: Hard cap on attempts (e.g. 3), then escalate; separate the verifier model/effort; classify flakes; record the attempt count in state.

> **One-line summary:** A loop that retries the same fix forever means the verifier is too weak or the cause is wrong — cap attempts and escalate.

### 2.2 State Rot

- **Symptom**: `STATE.md` (*the file where the loop stores what it is working on and what it decided*) references merged PRs, closed tickets, stale branches.
- **Severity**: S1, becoming S2 — the loop starts acting on "ghosts" (work that no longer exists).
- **Causes**: No prune step (*prune = delete entries that are done*) at the end of the run; state not read at the start; multiple loops writing to the same file without a schema.
- **Mitigations**: Prune closed/merged items every run; keep a `Last run` timestamp and validate IDs; one state file per pattern.

> **One-line summary:** Stale state makes the loop chase finished work — prune every run and keep one state file per loop.

### 2.3 Verifier Theater

- **Symptom**: The verifier "approves" the work, but tests fail in CI or human review finds bugs.
- **Severity**: S2 — harmful.
- **Causes**: A vague verifier prompt ("looks good"); the verifier never runs tests; the verifier uses the same model and context as the implementer.
- **Mitigations**: The verifier must run tests/lint and paste the output; give it different instructions ("find reasons to reject"); use a stronger model for unattended runs.

> **One-line summary:** An approval that runs no tests is fake safety — make the verifier execute tests and hunt for reasons to reject.

### 2.4 Notification Fatigue

- **Symptom**: Slack/email pings every 5 minutes; the team mutes the bot.
- **Severity**: S1, becoming S2 — real escalations get missed under the noise.
- **Causes**: Notifying on every run instead of every *actionable* finding; the "high priority" threshold set too low.
- **Mitigations**: Notify only when a human decision is needed; digest mode for report-only loops; tighten triage rules.

> **One-line summary:** Ping only when a human must decide — every-run alerts train the team to ignore the bot.

### 2.5 Token Burn

- **Symptom**: The bill spikes; the loop runs full sub-agent chains on empty or noisy triage (*triage = the quick first pass that sorts items into "worth doing" vs "ignore"*).
- **Severity**: S1 — annoying.
- **Causes**: Sub-minute cadence with heavy sub-agents; no early exit when the watchlist is empty; retrying the whole pipeline on transient API errors.
- **Mitigations**: A cheap triage-only pass first; `scheduler_delete` when the work is done; a daily token budget that pauses the loop.

> **One-line summary:** Empty watchlists should exit early and cheap — schedule less, budget daily, stop when the work is done.

### 2.6 Over-Reach (Wrong Scope)

- **Symptom**: The loop refactors unrelated modules, "fixes" design issues, touches denylist paths (*denylist = a blacklist of paths the loop must never touch*).
- **Severity**: S2, escalating to S3.
- **Causes**: The minimal-fix skill is too permissive; no path allowlist/denylist; triage queues architectural work under "High Priority".
- **Mitigations**: Enforce the denylist inside the skills; "smallest possible diff" + the verifier checks touched files; triage is signal-only.

> **One-line summary:** Scope creep by the loop is fixed with hard path limits, not polite instructions — enforce the denylist and check the diff.

### 2.7 Comprehension Debt Spiral

- **Symptom**: Velocity is up but nobody can explain the recent changes; review becomes a rubber stamp.
- **Severity**: S2 — harmful, and it compounds long-term.
- **Causes**: Humans stop reading the loop's output; the auto-merge allowlist keeps growing; no weekly human synthesis.
- **Mitigations**: Mandatory human review for non-trivial PRs; a weekly "loop digest"; cap auto-merge to truly trivial paths.

> **One-line summary:** If nobody can explain the merged changes, the debt is already being paid — keep human review on anything non-trivial.

### 2.8 Cognitive Surrender

- **Symptom**: "The loop handles it" — nobody has an opinion on correctness or design anymore.
- **Severity**: S2 — harmful at the team-culture level.
- **Causes**: The loop's success metric is volume, not quality; no human gates on medium-risk work.
- **Mitigations**: Explicit human gates in every pattern; success metric = time saved *with* a quality bar; Osmani: "Build it like someone who intends to stay the engineer".

> **One-line summary:** "The loop handles it" is the warning sign — keep humans accountable for quality, not just for pressing go.

### 2.9 Parallel Collision

- **Symptom**: Two sub-agents edit the same files; merge conflicts; corrupted state.
- **Severity**: S2 — harmful.
- **Causes**: No worktree isolation (*a git worktree = a private copy of the repo in its own folder, so edits there never touch the main tree*); two loops acting on the same PR without coordinating.
- **Mitigations**: `isolation: worktree` for every code-editing sub-agent; a lock/queue in state, e.g. "PR #1234 — worktree in progress".

> **One-line summary:** Two agents editing one branch will corrupt each other — give each its own worktree and a lock in state.

### 2.10 Escalation Failure

- **Symptom**: The loop is stuck retrying, but no human is ever told.
- **Severity**: S2 — harmful.
- **Causes**: Max attempts not implemented; escalation only written to a state file nobody reads.
- **Mitigations**: A connector ping on escalation (Slack, Linear comment); a `High Priority (waiting on human)` section in STATE.md; alert when an item there is older than 24h.

> **One-line summary:** A stuck loop must make noise where humans actually look — ping a channel, not just a file.

---

*Next: [07 — Tools & Ecosystem](../07-tools/) → [README](../README.md)*
