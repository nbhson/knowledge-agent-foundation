# ❓ FAQ — Trajectory & Observability (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The agent deleted a file and the user complained 40 minutes later — how do I find out why? [→ Opening Story + §1]

**What you see**

A ticket arrives: *"The agent deleted `src/auth/middleware.ts` and the user reported it 40 minutes later. Why?"* With only a chat log you have the model's words, not its actions, plus a partial CI log and a feeling. The post-mortem is a guess.

With an event log, one query answers it in eleven seconds:

- seq 31 `read_file` `src/auth/middleware.ts` → 4.1KB
- seq 32 `edit_file` (patch applied)
- seq 33 `write_file` ← **the delete**
- seq 34 `eval` "tests pass" — and it was true, nothing imported the file any more

The follow-ups then answer themselves. seq 29 `prompt` says the exports were unused. seq 33 records a `git worktree`, so it was reversible. Blast radius was one file, below the `write` threshold — yet 3 other files imported it and the agent never read them.

**Why**

A chat transcript records what the model *said*. A trajectory records what it *did*, timestamped and joined by keys. Without `parentTaskId` and `actor`, "who did this" has no answer at all.

**What to do**

1. Emit `tool_call` and `tool_result` for every action, always paired. One without the other is a hung step.
2. Keep `seq` gapless and 0-based; a gap means a lost write, so alert on it.
3. Require `actor` (`"agent:coder"`, `"human:alice"`, `"system"`) and `parentTaskId` on every event except `session_start` / `session_end`.
4. Validate one single shape at write time, so a new module cannot break every downstream query.

```sql
SELECT seq, kind, payload->>'tool' AS tool, payload->>'path' AS path
FROM trajectory
WHERE session_id = 'ses_44a' AND payload->>'path' LIKE '%middleware%'
ORDER BY seq;
```

**Verify**

Take 5 old sessions. For each one, name the exact `seq` that touched a given file without opening the chat log. If you cannot, the join keys are missing.

---

## Q2. Our bill tripled last month and nobody can explain why — where do I even start? [→ §6.2 + §1.2]

**What you see**

Finance asks why. The only answer available is the invoice divided by the number of runs, which explains nothing. Nobody can say whether you sent more tokens or sent the same tokens to a pricier model.

With per-step `model`, `tokens` and `costUsd` on every event, one query gives the answer. In practice it is *"a retry loop on 3% of runs"* or *"compaction stopped firing"* — both fixable in an afternoon. The most common finding: **cost is not in the prompts, it is in the retry loops and the frontier-tier steps nobody needed.** A dashboard built on this query usually finds 15–30% savings in the first week, with no quality change.

**Why**

Billing gives you the total, not the step. Without the model name attached to each step, "the bill tripled" has no owner and no fix.

**What to do**

1. Compute `costUsd` **at emit time**, not when you query. Prices change; a recomputed number stops matching the invoice.
2. Put `model` and `tokens {in, out, cached}` on every event, and emit `session_start` so cost joins back to a task and a tenant.
3. Run the loop detector: the same command signature (`argvHash`) repeated 3+ times in one session is a stuck agent, not a hard task.
4. Sample payloads to save storage, but keep cost counters at 100%.

```sql
SELECT t.session_id, e.model, SUM(e.cost_usd) AS usd, SUM(e.tokens_out) AS out_tok
FROM trajectory e JOIN trajectory t
  ON t.session_id = e.session_id AND t.kind = 'session_start'
WHERE e.cost_usd IS NOT NULL
GROUP BY t.session_id, e.model ORDER BY usd DESC LIMIT 20;
```

**Verify**

Every row in the top 20 must map to a task you recognise by name. The loop detector should return a small number of sessions, and each one must be explainable in a single sentence.

---

## Q3. Storage costs more than the model bill, and an analyst leaked a customer email out of a raw query — how do I fix both? [→ §5.1 + §5.2]

**What you see**

Trajectory files grow faster than inference does — one run can leave megabytes of command output on disk. At the same time someone runs an ad-hoc query against the raw store and a real customer's email address ends up in a notebook.

**Why**

Redaction at read time fails the moment *anything* reads the raw table, and raw tables always get read by ad-hoc queries. Meanwhile the bytes are dominated by large tool outputs, which are the least useful thing you will want six weeks later.

**What to do — retention tiers**

| Tier | Age | Contents |
|---|---|---|
| Hot | 0–7 days | full payloads, fast storage |
| Warm | 7–90 days | payloads over 4KB replaced by a `ref` |
| Cold | 90 days – 1 year | aggregates only: steps, tokens, costUsd, latencyMs |
| Purged | tenant TTL | deleted, with a stored receipt |

**What to do — redaction**

1. Redact at write, not at read: `sk-…`, `ghp_…`, `AKIA…`, private keys, emails, card numbers → `[REDACTED]`.
2. Store the number of hits as a `redactions` field on the event, so a spike is visible.
3. Keep a `stdoutHash` beside each `ref`, so a cold record is still auditable.
4. Cap any payload at 64KB; anything larger becomes `{ ref }`.

```sql
SELECT COUNT(*) FROM read_json_auto('trajectories-warm/*.jsonl')
WHERE payload::TEXT ~ 'sk-[A-Za-z0-9]{20}';
-- must be 0. Non-zero = incident.
```

**Verify**

Run this assertion quarterly; anything above 0 pages someone. Then check that the monthly storage trend actually drops in the first full month after the 4KB rule ships.

---

## Q4. I replayed a run to reproduce a bug and it emailed the customer a second time — how do I make replay safe? [→ §3.1 + §3.3]

**What you see**

You re-execute events `0..N` to reproduce a ticket exactly. A step that charges a card or sends an email fires again. It feels worse because replay, fork and resume look identical in a terminal, and they are three different tools with three different promises: replay must match the recording, fork may diverge wildly, resume must **not** re-execute committed side effects.

**Why**

Replay re-triggers irreversible effects because steps carry no idempotency key. Teams assume "replay" means "safe rerun". It does not — not every step is even deterministic.

**What to do**

1. Give every step an idempotency key = `(parentTaskId, tool, argvHash)`. On replay, a completed key is skipped and its recorded `tool_result` is substituted.
2. Classify each event kind before promising fidelity: `memory_read` deterministic; sandboxed commands same exit code; live API, prompt and LLM judge not deterministic — compare fingerprint, and allow ±0.1 on a judge score.
3. Compare the prompt `fingerprint` first. It hashes template + retrieved chunk ids + memory ids + policy hash; if it differs, the *inputs* changed and comparing outputs will only mislead you.
4. Replay the top-20 production trajectories nightly against a pinned model. Drift on a deterministic step is a hard failure.

```typescript
export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;
}
// replay: key already in `done` → skip the call, use the recorded tool_result
```

**Verify**

Replaying a run that contains an email step sends zero emails. Any drift on a `memory_read` step fails CI, so you find out the day it breaks, not during the incident.

---

## Q5. The dashboard says 5/5 tasks done, but my cost total is 12% below the invoice — what am I missing? [→ §4.3 + §8.2 + §14]

**What you see**

Progress says `5/5`. Invoices do not match. Three different causes hide inside each other, which is why the number is wrong but nothing looks broken.

**Why**

- **Orphan events.** Some emitters never set `parentTaskId`, so those events cannot join to a task and fall out of every cost report. Under-counting by ~10% is the classic symptom.
- **UI as its own source of truth.** Progress is computed in the front end instead of folded from the event stream, so it can claim success while the log says otherwise.
- **Sampling without counters.** You kept 5% of successful reads and dropped the totals too, so every average becomes statistically meaningless.

**What to do**

1. Make `parentTaskId` required in the schema for every kind except `session_start` / `session_end`.
2. Run the orphan query continuously. Non-zero is a page, not a warning.
3. Build the live UI as a fold over events — one function, one stream, no parallel state.
4. Keep the counters at 100% even when you drop payloads.

```sql
SELECT kind, COUNT(*) AS orphans, MIN(ts) AS first_seen
FROM trajectory
WHERE parent_task_id IS NULL
  AND kind NOT IN ('session_start','session_end') GROUP BY kind;
```

One more free detector: a `tool_call` with no matching `tool_result` is every step that never came back. One query finds them all — wire it to an alert and a "run appears stuck" badge.

**Verify**

The orphan query returns 0 rows for a full week. UI status equals `session_end.tasksDone == tasksTotal` computed from the log. The cost sum matches the invoice within sampling error.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*