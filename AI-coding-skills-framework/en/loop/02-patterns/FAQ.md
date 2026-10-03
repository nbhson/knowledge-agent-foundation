# ❓ FAQ — Loop Patterns (Real Stories, Plain Language)

If a question is unclear, read the section in the named file (named in brackets).

---


## README.md

### Q1. There are seven patterns and I cannot choose — which one do I start with? [→ Pattern Picker — Which Loop?]

**What you see**

You open `02-patterns/`, count seven pattern files, and stall. Meanwhile CI (continuous integration — the automated test run on every push) has been red for two days because nothing was ever started.

**Why**

Each pattern was built for one specific pain, so you do not need to understand all seven to begin. The README gives you an "auto-answer machine": answer one question — *what hurts right now?* — and follow the branch.

**What to do**

1. CI red → CI Sweeper, at 15 minutes or slower first.
2. Pull requests (PRs) stalling with no reviewer reaction → PR Babysitter.
3. Noisy issues plus morning chaos → Daily Triage **and** Issue Triage.
4. Dependabot or CVE (a published vulnerability) noise → Dependency Sweeper.
5. Not sure at all → Daily Triage at L1 (report only, no code changes).

```bash
npx @cobusgreyling/loop init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop audit . --suggest
```

**Verify**

After `audit . --suggest`, a state file and a scheduler entry exist, and the first run produces a report with no commits. If you cannot name the pain in one sentence, stay with Daily Triage at L1 — it teaches state discipline without the risk of auto-merge.

---

### Q2. I started a loop and my token bill tripled overnight — what am I allowed to run every 5 minutes? [→ Cost-aware Picks]

**What you see**

The summary table has a "Token cost" column: Daily Triage and Changelog Drafter are Low, Dependency Sweeper Medium, PR Babysitter High, CI Sweeper Very high. You also see the warning that a 15-minute cadence without early exit can pass 5M tokens per day.

**Why**

Cadence multiplies per-run cost. A no-op run is about 5k tokens; a full action run is about 200k. Ninety-six runs a day at 200k is a budget decision, not a bug — and CI Sweeper alone carries a 1M daily cap.

**What to do**

1. Hobby or tight plan → Changelog Drafter, Daily Triage (L1), Post-Merge. Avoid CI Sweeper at 5m and PR Babysitter at 5m.
2. CI is red → CI Sweeper at **15m or slower**, with early exit.
3. Many open PRs → PR Babysitter at 10–15m, L1 watch first, no L2 fix loop on every tick.
4. Release week → Changelog Drafter daily; no unattended Dependency Sweeper or CI Sweeper.

| Pattern | No-op | Full run |
|---|---|---|
| Daily Triage | ~5k | ~50k (L1), ~200k (L2) |
| Issue Triage | ~5k | ~40k |
| CI Sweeper | ~5k | ~50k triage, ~200k fix |

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

**Verify**

The cost command prints the projected tokens per day for the exact cadence and level you typed. Run it before every cadence change and keep the number in your loop notes.

---

### Q3. I turned on two loops and they edited the same branch within one hour — who owns what? [→ Overlap Rules]

**What you see**

CI Sweeper opened a worktree on `fix/ci-auth-refresh`. Forty minutes later another loop opened a second worktree on the same branch. One of them is silently overwritten and the state file shows two different "last actions" for one job.

**Why**

Two loops doing the same job is not parallel work, it is a race. The README ships an explicit overlap table so every loop has exactly one owner per job.

**What to do**

1. CI Sweeper owns failing checks; PR Babysitter does not re-fix the same branch in the same hour.
2. Daily Triage reports, action loops execute — triage never auto-fixes at L1.
3. Pause Dependency Sweeper while CI is red on main.
4. Post-Merge Cleanup runs off-peak only.
5. Changelog Drafter is read-mostly and safe next to anything, but never auto-publishes.

```text
CI Sweeper    -> failing checks on watched branches
PR Babysitter -> review movement, not re-fixing CI
Daily Triage  -> report only (L1)
```

**Verify**

Two consecutive `loop audit . --suggest` runs show no branch claimed by two state files, and every open worktree has exactly one owner line naming the loop that created it.

---

### Q4. My team wants to jump straight to L3 with auto-merge on a production repo — is that fine? [→ First Loop Recommendation / Golden rule]

**What you see**

A PR merged overnight without review because "the agent was confident". The diff touched authentication. Nobody can say which step approved it, and `loop-run-log.md` shows no human in the loop.

**Why**

The README's golden rule is explicit: never skip to L3 for a new pattern on a production repo. L1 is report-only, L2 proposes a fix, L3 acts. Model confidence is not evidence, and each level exists because the previous one was boring enough to trust.

**What to do**

1. Start with Daily Triage at L1 if you are unsure — it teaches state discipline without auto-merge risk.
2. Pick a pattern from the decision tree, scaffold it, copy skills from `templates/` only if you must customise.
3. Run week one at L1 report-only before enabling any fix.
4. Walk the upgrade path in `../04-operating/` before each level change.
5. Set up scheduling (`/loop`, `scheduler_create`, GitHub Action, or Codex Automation).

```bash
npx @cobusgreyling/loop init . --pattern issue-triage --tool claude
npx @cobusgreyling/loop audit . --suggest
```

**Verify**

The first seven days of `loop-run-log.md` contain zero merge commits, and a named human opened every PR in that window. If that is not true, drop back to L1 and re-run the week.

---

## daily-triage.md

### Q1. STATE.md is now 600 lines and half of it is already fixed — how do I stop it growing forever? [→ State]

**What you see**

A `Last run: 2026-06-09 08:15 UTC` timestamp sits on top of forty closed items. PR #1238 has been on the Watch List since March. The one line that matters — "flaky test in auth flow, CI red on main" — is buried at line 300.

**Why**

`STATE.md` is the loop's memory spine, but nothing ever deletes from it. The file's own failure table names this: "state file grows without bound → prune merged/closed items every run".

**What to do**

1. Prune resolved and merged items on **every** run, not once a week.
2. Move recurring low-value entries (Dependabot PRs and similar) into a `## Recent Noise` section instead of deleting them, so the loop stops re-reporting them.
3. Update the three fields the loop must write every run: the `Last run` timestamp, item status plus last action taken, and human decisions that overrode the loop.
4. Keep the Watch List to one line per stalled item.

```markdown
## High Priority (loop is handling / waiting on human)
- [ ] #1241 — flaky test in auth flow (CI red on main)
  Loop action: Opened worktree. Fix proposed. Waiting for human PR review.

## Watch List
- PR #1238 open for 4 days without activity.
```

**Verify**

After a run, every item under `High Priority` has a status line newer than the previous `Last run`, and the file is no longer than it was before the run started. If it grew, the pruning step was skipped.

---

### Q2. The 08:15 report lists 30 items and 25 are junk — how do I cut the noise? [→ Failure Modes & Mitigations]

**What you see**

Morning state lists a Dependabot PR, three duplicate issues, and a build failure that had already fixed itself. Within a week you stop opening the file at all.

**Why**

Triage produces noise when the skill has no ignore list. It also burns money: a no-op run is ~5k tokens, a full L1 triage is ~50k, and every noisy run is a full run instead of a cheap one.

**What to do**

1. Tighten the `loop-triage` skill rules and add a "Noise / Ignore" section to the state template.
2. Start report-only, then add effort and risk gates before allowing auto-fixes — wrong-priority fixes are the named failure here.
3. Use `/loop 1d` for morning triage and `/loop 2h` only during an active sprint, for faster signal rather than louder signal.
4. Write the post-run critique every cycle: false positives, repeated items, one adjustment for next time.

```bash
/loop 1d Run $loop-triage and update STATE.md. Do not auto-fix in the first week — report only.
```

**Verify**

For three mornings in a row, the number of items you actually acted on is at least half the items listed. If not, move the offenders into `## Recent Noise` and tighten the skill the same day.

---

### Q3. The loop proposed a fix on Monday and it is still waiting on Friday — what should have happened? [→ Human Handoff Points]

**What you see**

One line reads `Loop action: Opened worktree. Fix proposed. Waiting for human PR review.` and it stays byte-identical across five runs. Then a customer reports the same bug.

**Why**

A proposal sitting in a file is not a notification. The loop has explicit handoff conditions — anything surfaced for 3+ days without resolution is one of them — but nothing pushes them to a human.

**What to do**

1. Escalate any item the loop has surfaced for 3 days or more without resolution.
2. Hand off design decisions, multi-file refactors, and anything touching security, auth, payments, or infrastructure.
3. Hand off anything the triage output marked "needs discussion".
4. If the post-run critique accumulates over N runs without review, force a human handoff instead of writing critique N+1.

```markdown
- [ ] #1241 — flaky test in auth flow (CI red on main)
  Loop action: Escalated — 5 runs, no human response. Needs an owner.
```

**Verify**

No item under `High Priority` is older than three days without either an owner or an escalation line. Count the leftovers each morning and treat a non-zero count as the alarm.

---

### Q4. The loop ran at 08:00 and I never heard about the 02:00 failure — how do I catch overnight? [→ Scheduling]

**What you see**

`Last run: 2026-06-09 08:15 UTC` is the only timestamp in the whole state file. A deploy at 02:14 broke the pipeline and nothing surfaced until the next morning's report.

**Why**

A daily schedule is a sampling window, not a monitor. Between two ticks you are blind, and the 100k daily token cap is the reason the cadence exists in the first place.

**What to do**

1. Set `fireImmediately: true` so the scheduler fires the moment CI turns red.
2. Or run twice per day: at the start of the day plus a midday pass.
3. No terminal interface (TUI)? Use the GitHub Action cron `0 8 * * 1-5`; `daily-triage.yml` updates `STATE.md` and `loop-run-log.md`.
4. Check the projected cost before tightening the interval below 2h.

```bash
npx @cobusgreyling/loop cost --pattern daily-triage --cadence 1d --level L1
```

**Verify**

Break `main` on purpose after the morning run. Within one interval, `Last run` in `STATE.md` is newer and the new failure appears under `High Priority` with a suggested next action.

---

## issue-triage.md

### Q1. An issue only says "app slow" and the loop proposed a fix — what should it have done instead? [→ How the Loop Runs]

**What you see**

Issue #1311 — "app slow" — shows up in the state file with a suggested next action. Nobody can reproduce it, so the suggestion is a guess wearing a plan's clothes.

**Why**

`loop-triage` classifies, and a second skill, `issue-intake`, exists precisely for issues too ambiguous to verify as done. Its rule is no guessing: ask for more information, or escalate.

**What to do**

1. Classify every issue as bug, feature, question, duplicate, or stale.
2. If it is ambiguous, `issue-intake` asks the reporter through a comment or escalates — never guess.
3. If it is actionable, write the suggested next action into `issue-triage-state.md`. Suggestions only, no code edits: this loop is L1 propose-only.
4. Attach evidence to every finding — the issue link plus the reasoning behind the classification.

```markdown
- #1311 — "app slow" — [Ambiguous] — loop-intake: needs more info, has asked via comment
- #1312 — duplicate of #1305 — [Dup] — suggested: close
```

**Verify**

Every `[Ambiguous]` line has a matching comment on the issue asking for more, or an entry under `## Needs Human`. No line anywhere says "guessed" or "probably".

---

### Q2. The backlog has 500 open issues and one run reads all of them — what stops the cost? [→ Failure Modes & Mitigations]

**What you see**

A 2-hour schedule meets a 500-issue backlog. A no-op run is ~5k tokens and a full triage scan is ~40k, and this pattern shares the same suggested daily cap of 100k as Daily Triage.

**Why**

"Overwhelmed by many issues" is a named failure mode with a named mitigation: cap how much a single run is allowed to touch. The fix is not a bigger model, it is a smaller slice.

**What to do**

1. Cap the number of issues processed per run, newest first (the last 24 hours).
2. Prioritise by severity so the cap never drops the high-priority items.
3. Run on `/loop 2h–1d`; go faster only if the backlog actually shrinks between runs.
4. Reduce misclassification with evidence on every finding plus periodic human review.

```bash
npx @cobusgreyling/loop cost --pattern issue-triage --cadence 2h --level L1
```

**Verify**

Each run log shows a processed count at or below the cap, and the `## Needs Human` bucket is not growing faster than a human empties it.

---

### Q3. A security issue landed in the backlog — should the loop treat it like any other issue? [→ Human Handoff Points]

**What you see**

An issue describing an authentication bypass sits in `## New Issues (last 24h)` with a classification and a suggested action, listed right next to a typo report.

**Why**

Security issues are an escalate-immediately handoff point, not a classification bucket. Reading and sorting an issue is fine; suggesting a code fix for a vulnerability is not.

**What to do**

1. Classify it and record it, but escalate in the same run — do not let it wait for the next tick.
2. Hand off feature requests that need a product decision, and high-priority issues with no owner.
3. Hand off anything still unclear after asking for more information.
4. Keep the chain clean: Issue Triage classifies, Daily Triage prioritises, action loops execute.

```markdown
## Needs Human
- #1298 — large feature request — needs a product decision
- #1302 — auth bypass reported — SECURITY: escalate now, do not auto-reply
```

**Verify**

No security issue stays in `New Issues` for more than one run interval. Each one appears in `Needs Human` with a timestamp, and the escalation comment is on the issue itself.

---

## ci-sweeper.md

### Q1. CI is red and the loop retried the same failure all night — millions of tokens gone. What stops it? [→ How the Loop Runs]

**What you see**

`loop-ledger.json` shows attempts climbing on job `test-auth` with `AssertionError in test_refresh_token_expiry` and nothing new in the message. Each L2 fix attempt costs ~200k tokens, and the README warns that 15m cadence without early exit exceeds 5M tokens per day.

**Why**

Without a circuit breaker the sweeper keeps proposing minimal fixes for a failure it cannot resolve. Repeating a fix that does not work is the exact loop the `loop-guard` skill exists to break.

**What to do**

1. Require `loop-guard` — it logs every attempt to `loop-ledger.json` and escalates instead of looping on the same failure.
2. Trip the breaker when the same failure recurs N times or attempts exceed the maximum, for example 3.
3. Escalate with a pruned context summary, not the full log history.
4. Pause the loop after N failures on a red main and batch the fixes instead.

```bash
/loop 15m Run ci-triage, then minimal-fix in a worktree. Run loop-guard before every retry.
```

**Verify**

`Attempts: 1/3` in `ci-sweeper-state.md` never exceeds 3, and any failure sitting at 3/3 has an escalation line with a named human owner.

---

### Q2. The loop turned CI green by deleting the failing test — is that a fix? [→ Verification Strategy]

**What you see**

A small PR, a green pipeline, and a diff that removes an assertion. The implementer also marked the item done itself, so nobody else ever looked.

**Why**

Green CI is necessary but not sufficient. The named failure mode is fix-the-symptom looping: the verifier must check the root cause, not just the colour of the badge.

**What to do**

1. The verifier sub-agent runs the tests **in the worktree** before approving.
2. It confirms the fix scope — no unrelated changes, and tests pass locally.
3. The implementer never marks itself done and must never merge; it only proposes.
4. Watch the repeat-failure rate: the same job failing again within 48 hours means the cause was never found.

```markdown
### main @ abc1234
- Job: test-auth
- Last action: Minimal fix proposed in worktree fix/ci-auth-refresh
- Status: Waiting for verifier + human
```

**Verify**

Every sweeper PR carries a verifier line naming the tests it ran, and the number of tests in the repository never goes down across those diffs.

---

### Q3. One flaky test fails every third run and the loop keeps patching it — how do I stop it? [→ How the Loop Runs / Verification Strategy]

**What you see**

The same test alternates red and green with no code change. The sweeper opens a fresh worktree each time, and the state file shows six attempts against one job.

**Why**

Flake detection has a clear rule: if the same test fails then passes on retry with no code change, do not auto-fix. "Fighting flakes with retries" is its own failure mode, and each retry costs ~200k tokens.

**What to do**

1. Classify first: flake, real regression, or infrastructure.
2. If it is a flake, add it to the Watch list and do **not** auto-fix.
3. Quarantine or skip it with a ticket, so the noise has a named owner.
4. Escalate infrastructure failures — runner out of memory, registry down, missing secrets — instead of patching code.

```markdown
### main @ abc1234
- Job: test-auth
- Status: FLAKE — passed on retry with no change. Watch list, ticket #481.
```

**Verify**

No flake-classified job has an open worktree or a PR. Review the Watch list count weekly — if it grows, you need quarantine rules, not more retries.

---

### Q4. The sweeper opened a PR touching 12 files on a branch I never named — how do I bound it? [→ Failure Modes & Mitigations / Human Handoff Points]

**What you see**

A PR against `main` from a branch named after the failing job, changing 12 files across authentication and billing. The skill was supposed to make the smallest change that resolves the failure.

**Why**

Two guards are missing. An explicit branch allowlist in the skill prevents the wrong-branch failure, and the human handoff rule for failures touching more than 5 files or core architecture catches the rest.

**What to do**

1. Put an explicit branch allowlist in `ci-triage`: `main`, `release/*`, and active PR branches only.
2. `minimal-fix` must produce the smallest change that resolves the specific failure.
3. Escalate failures touching more than 5 files or core architecture.
4. Escalate security-sensitive test failures and any failure that hit max attempts.

```text
watch  : main, release/*, active PR branches
escalate: >5 files changed, core architecture, security tests, attempts exhausted
```

**Verify**

Every open sweeper PR names a watched branch and touches 5 files or fewer. Anything larger should be sitting in the human queue rather than waiting in review.

---


## dependency-sweeper.md

### Q1. Dependabot shows me 40 open alerts and the sweeper only touches two — is it just being lazy? [→ How the Loop Runs]

**What you see**

You open the Dependabot page and count 40 alerts: a critical one in `lodash`, 30 patch bumps, and 9 major version jumps. The sweeper opens exactly one pull request — `lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low)` — and leaves the other 39 sitting there. The state file shows one item in flight and one on hold:

```
## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260
## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting on human decision
```

**Why**

The sweeper is not a bulk updater on purpose. Only **low-risk CVEs with a patch-only fix inside the first 30 days** get automatic worktree + patch + verify treatment. Major version bumps and denylisted packages (`openssl`, auth, payments, infrastructure libraries) are escalated to a human instead. Patching everything at once means forty separate breaking changes landing in one week, and nobody can review forty diffs.

**What to do**

1. Do not widen the automatic branch. Sort the 40 alerts by severity, then patch only the low-risk CVE group inside the 30-day window.
2. Send majors and denylisted packages to the state file under `## Denylisted (human required)` so they stay visible instead of being forgotten.
3. Batch the long tail weekly instead of daily, so a week of patch bumps arrives as a reviewable pile rather than 30 single-line pull requests.
4. Keep Dependabot as the discovery tool (it finds alerts) and let the sweeper own the patch + verify half of the job.

```bash
npx @cobusgreyling/loop cost --pattern dependency-sweeper --cadence 1d --level L2
```

**Verify**

The "% of alerts resolved without a human" number should only be high for the low-risk bucket. Open the state file after a run: anything sitting under `Denylisted (human required)` should have a named human owner or a decision date, and the patch-only items should all show `verifier PASS` and a pull request number.

---

### Q2. The sweeper tried to upgrade `openssl` 1.1 → 3.0 on its own and broke the build — why didn't the gate stop it? [→ Human Handoff Points]

**What you see**

`openssl` is a denylisted package in this repo. Somebody (or a loop) ran the upgrade anyway. The build fails with symbol errors from a 2.x-to-3.x API change, and the diff touches nine files. The commit message says something like "chore(deps): bump openssl to 3.0.2", which is exactly the shape of change that is supposed to never appear without a person signing off.

**Why**

Because "major" and "denylisted" are two separate escalation triggers, and both of them must be checked before the loop opens a worktree, not after. `openssl 1.1 → 3.0` is a major bump with breaking changes *and* it sits in the security/infra denylist. Either trigger alone is enough to stop automation. Escalation triggers that are only documented in a table are not enforced anywhere in code, so the first run with an unusual alert slips through.

**What to do**

1. Make the denylist a real, checked input — a committed list of package names the loop refuses to patch at all — not prose in a document.
2. Require two explicit checks before any worktree opens: is this a major version change, and is this package on the denylist? Either answer being yes writes a human-handoff entry instead of a patch.
3. Add the third trigger: an alert that needs code changes, not just a version bump, is also escalated. Version-number bumps are mechanical; behavior changes are not.
4. Revert the `openssl` pull request by hand, then let the state file carry it as a pending decision. Do not let a retry loop "fix" a major it is not allowed to touch.

**Verify**

Try the loop against a synthetic alert for `openssl 1.1 → 3.0`: no worktree is created, no pull request is opened, and the state file gains an entry under `## Denylisted (human required)` saying `waiting on human decision`. Re-run it a second time and confirm nothing is retried.

---

### Q3. The patch passed `npm test` and still broke the build after merge — how is that possible? [→ Verification Strategy]

**What you see**

A verified pull request lands. `npm test` was green in the sweeper's run. Twenty minutes later the deploy job is red with `Cannot find module './internal/uuid'`, and rollback feels messy because the pull request was merged during a release window.

**Why**

The rule that saves you here is that the verifier runs the **full** `npm ci && npm test`, not a subset. A clean install first (`npm ci`, not `npm install`) is what proves the lockfile actually resolves — a leftover `node_modules` from a previous state can hide a broken or missing package. The second half of the rule is that a dependency change often breaks the **build**, not the tests, so a test-only check would have passed anyway.

**What to do**

1. Treat `npm ci && npm test` as the definition of verified. If a project is not JavaScript, use the equivalent full build plus test command.
2. Never skip the build step: a test that imports nothing from the changed package stays green while the package's own build is broken.
3. Clean install every time. `npm ci` deletes `node_modules` and installs exactly the lockfile; `npm install` may resolve to something newer and hides the problem.
4. Record the verification in the state file (`verifier PASS` plus the pull request number) so a red build after merge can be traced back to a specific run.

```markdown
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low)
  — worktree open — verifier PASS — PR #1260
```

**Verify**

The success metric is "number of patches that broke the build — target: 0". Check it every week. If it is not zero, read the failing run: either the verifier command is not the full build, or it ran without a clean install.

---

### Q4. My dependency-sweeper bill jumped from near zero to thousands of tokens a day — where did it go? [→ Cost Profile]

**What you see**

A quiet month of roughly 5k tokens a day, then a week at 90k per run. The daily total crosses the 500k suggested cap. Looking at the numbers, one patch-plus-verify cycle is the expensive part, and it runs for every single alert.

| Scenario | Tokens/run |
|---|---|
| No-op | ~5k |
| Triage alerts | ~20k |
| Patch + verify (L2) | ~150k |

**Why**

Cost is not proportional to the size of the diff. Reading alerts is cheap (~20k). The 150k is the worktree, the patch, and the full build plus test, and that cost is per alert, not per run. So a week where twelve alerts qualify means roughly 1.8M tokens, even though every individual pull request is a one-line version change. A cadence of 6h against a slow-moving dependency graph also means you pay the triage cost four times a day to find nothing.

**What to do**

1. Prioritize by severity. A critical CVE outranks three low patch bumps, even when the low ones are cheaper.
2. Batch the non-urgent patch bumps weekly. One worktree with three version changes costs less than three worktrees.
3. Set the cadence to match the alert rate. `/loop 1d` is fine for a stable repo; `6h` is for a repo where new CVEs appear constantly.
4. Make sure the no-op path stays cheap — early exit when the alert feeds are unchanged, so a quiet day really is ~5k.

**Verify**

Run the cost command above for your real cadence and level, then compare one week against the 500k daily cap. If the average is above the cap, the batching rule above is not being applied — check how many separate pull requests one week produced.

---

## pr-babysitter.md

### Q1. Reviewers got 30 identical "any update?" comments in one morning — how do I stop that? [→ Failure Modes & Mitigations]

**What you see**

Twelve pull requests sit without review. At 09:00 the babysitter wakes up and, because all twelve are stale past the threshold, it posts the same gentle nudge on every one. By 09:05 the team channel has 27 notifications, and three people muted the bot. One developer replies "I said yesterday I would look at it after the release" — which is correct and was in the pull request description.

**Why**

Nudging is the correct action for a stale pull request, but nudging is only correct **once**. The mitigation in the source file has two halves: nudge only after the threshold, and never repeat a nudge on the same pull request on the same day. Without the second half, a loop running every 5 minutes will cheerfully re-post. The bot is not broken; it is doing the right action too often.

**What to do**

1. Raise the staleness threshold to something a human can act on, and never nudge a pull request that already has a human reply saying "after the release".
2. Add a hard rule: at most one nudge per pull request per day. Store `last action` in the state file and check it before commenting.
3. Nudge via label first, comment second. A label is quiet and searchable; a comment notifies everyone.
4. Reduce the cadence when nothing is actionable. A 10-minute loop is for a shipping day; nightly is enough the rest of the time.

**Verify**

Pick one pull request that has been nudged today and let the loop run three more times. No new comment appears on it. Also confirm the state file line for it still reads `Loop action: Nudge comment sent. Waiting on review.` and does not accumulate repeats.

---

### Q2. The cost command says 200k tokens per fix attempt and my daily cap is 2M — one busy day blows it, doesn't it? [→ Cost Profile]

**What you see**

Ten pull requests go red at 09:00 because one shared test fixture broke. The babysitter scans them, opens ten worktrees, runs implementer plus verifier on each. That is 10 × 200k = 2M tokens — the entire daily cap — spent on what is really one problem reported ten times.

| Scenario | Tokens/run | Notes |
|---|---|---|
| No-op (all PRs fine) | ~5k | Required — don't run the full chain when there's nothing |
| Watch + nudge (L1) | ~30k | Scan PRs + CI status |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Why**

The babysitter is the highest tier pattern in the set: cadence 5–15m, daily cap 2M, and early exit is mandatory rather than optional. Two protections are built in and both matter. First, the no-op path must stay at ~5k — a loop that runs the full chain "just in case" has already lost. Second, active pull requests processed per run must be capped, so a burst of ten red pull requests becomes three attempts now and the rest on the next run.

**What to do**

1. Keep the no-op exit first: scan status, and if nothing is actionable, stop before any worktree opens.
2. Cap how many active pull requests one run may process, then early-exit and let the next tick pick up the rest.
3. Group before escalating. Ten pull requests failing on the same test file is one root cause, not ten fix attempts.
4. Use a 5-minute cadence only during a shipping day, when the burn is intended; drop to 10–15m otherwise.

**Verify**

Instrument the loop to log which scenario it took per run (no-op, watch + nudge, or fix attempt). A day with more than about ten L2 attempts is a red flag: either the cap is missing or something common is breaking every pull request at once.

---

### Q3. The loop retried the same broken fix nine times on one PR — when does it stop? [→ Verification Strategy]

**What you see**

PR #1248 (`lodash dep bump`, CI red on `test-auth`) stays red. The state file keeps flipping between `Fix proposed. Verifier PASS. Waiting on human.` and `Verifier REJECTS — attempt 2`, `attempt 3`, `attempt 4`. Each attempt costs roughly 200k tokens and each one opens and discards a worktree. Nine attempts later the pull request is still exactly where it started, and the team has learned to ignore the bot.

**Why**

Retrying is only correct up to a point. The rule is three attempts on the same pull request, then escalate — and the state file is supposed to hold the count. When the count lives only in the model's memory of the conversation, retries are unbounded, because every new run starts from zero and believes it is making fresh progress.

**What to do**

1. Persist the attempt counter in the state file for each pull request, next to the PR ID, branch, CI status, review count, and last action.
2. At the maximum (three), stop touching the pull request and escalate with the full history: what was tried, what the verifier rejected, and why.
3. Clean up the worktree on every rejected attempt before trying again, so stale worktrees do not pile up and mislead the next run.
4. Remember the implementer only proposes — it never merges. Escalation, not auto-merge, is where a stuck pull request is meant to end.

```markdown
- PR #1248 — lodash dep bump — CI: red (test-auth)
  Loop action: Worktree opened. Fix proposed. Verifier PASS. Waiting on human.
  attempts: 2
```

**Verify**

Force three rejections on a test pull request. The fourth attempt must not happen; the state file shows `attempts: 3` and an escalation entry, and `git worktree list` shows no leftover worktree from the failed attempts.

---

### Q4. The loop "fixed" a red CI by changing 12 files — that PR wasn't a CI fix at all [→ Human Handoff Points]

**What you see**

A security-sensitive pull request touching authentication fails its checks. The babysitter classifies the failure, deems it "actionable", and produces a fix that rewrites 12 files and moves the token refresh logic. The tests go green. Three engineers now have to review a change nobody asked for, on the most sensitive code in the repo.

**Why**

The babysitter is supposed to draft *small* fixes — the `minimal-fix` skill exists for exactly this. It has two guardrails that failed to fire: fixes touching more than 5 files, or core architecture, belong to a human; and security-sensitive changes always belong to a human. The verifier normally catches scope problems by checking the diff, so the failure is almost always in the classifier that decided the CI failure was "actionable" in the first place.

**What to do**

1. Put the scope check before the worktree, not after. Count the files the fix *will* touch; more than 5 means escalate.
2. Treat any change to auth, payments, crypto, or session code as human-only, regardless of how small the fix looks.
3. Require the reviewer sub-agent to verify scope at level L2 — it must reject a fix that edits files unrelated to the failure.
4. When two valid approaches to the same conflict exist, that is a decision, not a bug. Escalate instead of picking.

**Verify**

Feed the loop a deliberately broad "CI fix" target and confirm the answer is escalation, not a 12-file pull request. Check the verifier's own record: a PASS on a wide diff should be treated as a bug in the verifier, not a win.

---

## changelog-drafter.md

### Q1. The draft says "Breaking: 0" but two merged PRs definitely break the API — how does that happen? [→ Failure Modes & Mitigations]

**What you see**

Release prep starts. The draft `RELEASE_NOTES_DRAFT.md` is ready, and its summary reads `Breaking: 2 / Features: 15 / Fixes: 20` across 42 merged pull requests. You read two of the "fixes" and both replace a required parameter on a public function. Callers outside the repo will break, and nobody was warned because the notes buried it under bug fixes.

**Why**

Classification depends entirely on a *project conventions skill* that knows how your project separates breaking, feature, and fix. Without that, the drafter falls back on the pull request title and the commit text, and a breaking change titled "fix: correct response shape" is classified as a fix. The category counts in the state file are therefore accurate arithmetic over a wrong input.

**What to do**

1. Write the categories down as project conventions first, then let the skill use them — breaking is a caller-visible API or behavior change, not a bug fix.
2. Treat the category counts as a human checklist, not a summary. Read the two items marked `Breaking: 2` carefully, and spot-check the fix list.
3. Require every entry to stay traceable — each line points back to its pull request or issue, so a misclassification is one click from being corrected.
4. Decide the version bump (major, minor, patch) as a human, and highlight breaking changes at the top rather than in the list.

**Verify**

Count merged pull requests against draft entries (see Q2), then read every entry in the `Breaking` section and confirm each one really is breaking. The metric to watch is "% of draft entries that are correct (no rework)" — if that number drops after a release, the conventions skill needs updating.

---

### Q2. The state file says 42 merged PRs but the draft has 30 entries — 12 changes vanished [→ Failure Modes & Mitigations]

**What you see**

The state file records the run honestly:

```
## Since last tag: v1.4.0
- Merged PRs: 42
- Breaking: 2
- Features: 15
- Fixes: 20
- Draft: RELEASE_NOTES_DRAFT.md (awaiting human approval)
```

The draft itself reads as a clean, plausible document, so nothing looks broken. But 2 + 15 + 20 = 37 entries, and 42 pull requests were merged. Two entries were dropped silently, five were combined into one line, and nobody will notice until a user reports a missing change.

**Why**

The drafter collects merged pull requests and commits since the last tag, then groups them. Grouping is where entries disappear: several small pull requests folded into one bullet, a docs-only commit skipped, or a merge whose text was too thin to summarize. The arithmetic check exists precisely for this, and it has to be an explicit step rather than something the model does mentally while writing.

**What to do**

1. Compare the merged-pull-request count against the sum of the categories before showing the draft to anyone. Mismatch means investigate, not publish.
2. When entries are combined, say so: "3 pull requests fixed token refresh (#1240, #1243, #1247)" keeps the count honest.
3. Do not drop docs or dependency entries on the floor — group them, even if they sit in a small section.
4. Keep the draft as its own file with an explicit "awaiting human approval" marker in the state file.

**Verify**

Recompute the category totals from the draft text itself and compare against `Merged PRs: 42`. The two numbers must reconcile. A draft where the totals do not add up is a reject, regardless of how good it reads.

---

### Q3. Will it just publish to GitHub Releases and update `CHANGELOG.md` on its own? [→ Verification Strategy]

**What you see**

You were expecting a draft. Instead the tag exists, the GitHub release page is live, and `CHANGELOG.md` has a new version heading that nobody wrote. Someone reading the release notes finds two entries that should have been marked breaking, and there is no approval step in the history to point at.

**Why**

No. This pattern is **level 1, draft only, and no auto-publish** — it is a read-mostly loop that is safe to run alongside other loops for exactly that reason. The draft lands in `RELEASE_NOTES_DRAFT.md` and waits. Publishing, updating `CHANGELOG.md`, choosing the version number, and highlighting breaking changes are all human handoff points. If a run ever published on its own, the human gate is not wired in.

**What to do**

1. Keep the loop at draft-only level. Run it daily during release prep, or trigger it by tag, but never grant write access to the release.
2. Make the approval step explicit: someone reviews the draft, then publishes. The loop does not observe that approval and proceed — a person does the publishing.
3. Decide the version bump by hand, using the `Breaking` count as the deciding input.
4. Keep the frequency low. One run is about 30k tokens; a no-op run with no new commits is about 3k, so an unnecessary daily schedule is the only real waste here.

```bash
npx @cobusgreyling/loop cost --pattern changelog-drafter --cadence 1d --level L1
```

**Verify**

Run the loop and confirm that afterwards the only new file is `RELEASE_NOTES_DRAFT.md` and the state file says `awaiting human approval`. If a release or a `CHANGELOG.md` commit appears without a human action, the no-auto-publish gate is broken.

---

## post-merge-cleanup.md

### Q1. The cleanup PR deleted three TODOs and login broke that night — TODOs are harmless, aren't they? [→ Failure Modes & Mitigations]

**What you see**

PR #1255 merged a feature and left three `TODO`s in `auth/service.py`, one of them reading `# TODO: remove after migration flag ships`. The cleanup loop drafted a patch, the verifier passed it, and the TODO was deleted. The migration flag shipped four weeks later, and from that day the old code path was unreferenced but still shipping — the flag now flips to a path that was already partially deleted.

**Why**

A `TODO` is a comment, but comments often document a condition — *after X happens, do Y* — that exists nowhere else in the code. Deleting one is a behavior change disguised as a comment cleanup. The rule that protects you is: **only remove a TODO when the context is clear**, and ambiguous ones go to the backlog for a human.

**What to do**

1. Read the TODO before deleting it. If it names a trigger (a flag, a date, an upstream change), record it in the backlog instead of removing it.
2. Keep the rule "small fixes only — no refactors, no behavior changes" in writing and enforce it in the verifier.
3. Require the verifier to confirm behavior is unchanged, and to check the diff is the smallest possible one with no unrelated files touched.
4. When a TODO's context is unclear, the correct output is a backlog entry with `Draft fix proposed. Waiting on human review.`, not a pull request.

```markdown
- [ ] PR #1255 left a TODO in `auth/service.py` (3 TODOs)
  Loop action: Draft fix proposed. Waiting on human review.
```

**Verify**

Every TODO removal in a merged cleanup pull request should be readable as a no-op for behavior. Track "% of cleanups merged without rework" and "new TODO/FIXME count per day" — the second should trend down, and rework should stay near zero.

---

### Q2. The loop pushed a cleanup PR at 23:00 the night before a release — why does the time matter? [→ Scheduling]

**What you see**

Release is at 09:00 the next morning. At 23:00 the cleanup loop opened a pull request deleting a stale branch's worth of leftovers and a few dead log lines. Nobody reviewed it in time, it got merged by a well-meaning auto-merge rule, and the release notes now mention a change nobody remembers approving.

**Why**

This pattern is scheduled `1d–6h` and **only in off-peak hours** — for example 22:00 or weekends — and it must not run concurrently with the PR babysitter. Timing is not a nicety here: the risk of cleanup work is not that it is wrong, it is that it lands at the moment when the smallest possible reviewer attention is available. A cleanup during a release window is a merge into a moving target.

**What to do**

1. Schedule the loop for off-peak only, and make the window explicit rather than "whenever it is quiet".
2. Never let it run at the same time as the babysitter. Two loops writing branches and pull requests in the same hour produce conflicting diffs for no benefit.
3. Keep it away from release and maintenance windows entirely, even if it finds something genuinely urgent — record it in the backlog instead.
4. Treat branch deletion as a suggestion, not an action, unless the branch is provably merged and stale.

**Verify**

Check the `Last run` timestamp in `post-merge-state.md` on a few mornings. It should land in the off-peak window every time, and never on the evening before a release. The loop also records a `Last run` line, so a daytime timestamp is the visible proof of a misconfiguration.

---

### Q3. It deleted a branch someone was still working on — how do I stop that? [→ Human Handoff Points]

**What you see**

`fix/ci-auth-refresh` is still listed as a suggested delete, but three open pull requests are based on it. Deleting it breaks their diffs and makes the next rebase painful. The cleanup loop reads merged pull requests plus `git log`, sees a branch that has not been touched since its merge, and concludes it is leftover.

**Why**

Branch age is a weak signal. A branch can look stale for a week and still be the base of active work — especially when people batch their work and merge later. Deleting dead code that is not *certain* to be unused, and force-deleting any branch, are both explicit human handoff points in the source file.

**What to do**

1. Never force-delete. A branch needing force-delete is escalated by definition, not cleaned up.
2. Before suggesting deletion, check whether any open pull request targets the branch or is based on it — not only whether the branch was merged.
3. Make the action "suggest delete" by default, so a human performs the deletion in their own workflow.
4. Keep the backlog honest with the current action, for example `Loop action: Suggest delete.`, so nobody mistakes a suggestion for a pending command.

**Verify**

Create a test branch that was merged once but has an open pull request based on it. Run the loop: the entry must stay in the backlog as a suggestion and must not be marked resolved. The resolved list only gains an entry after a person confirms the deletion.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, daily-triage.md, issue-triage.md, ci-sweeper.md, dependency-sweeper.md, pr-babysitter.md, changelog-drafter.md, post-merge-cleanup.md.*
