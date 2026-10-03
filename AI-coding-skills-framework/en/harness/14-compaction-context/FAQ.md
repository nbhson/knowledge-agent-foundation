# ❓ FAQ — Context Compaction (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My agent died at turn 47 with a context-length error after 20 minutes of work. Why not just drop the oldest messages? [→ §2 Trigger Policy]

**What you see**

Turn 47. The run has done 31 tool calls, rewritten four files, run two test suites, and buried one confusing stack trace in the middle. Context is at 96% of the budget. The next tool result is 4,000 tokens and it does not fit. The user sees "something went wrong" after 20 minutes of work.

**Why**

Dropping the oldest messages is not compaction, it is amnesia. The agent loses the task description from turn 1, then re-reads a file it already read in turn 12 — because the read result is gone but the edit it produced is still there — and confidently writes a patch that undoes its own work from turn 30. Summarizing the whole transcript equally is just as bad: the paragraph keeps the stack trace and drops the task definition, so the agent solves the wrong problem fluently.

**What to do**

Trigger on measured token counts, at 70% used, not 90%. The arithmetic of a 200k window: one `read_file` of a 30 KB file costs 8% of the budget in a single step. Trigger at 90%, accept that 8%, and you are at 98% — the next result overflows and you must compact again mid-task, with no room left to summarize carefully. Compaction under pressure is the worst possible time to be lossy.

1. Add a turn-count backstop for when token estimates are unreliable.
2. Reserve 30% headroom so the next 2–3 tool results always fit.
3. Never let the model decide. Ask it "should we compact?" while it holds 195k tokens and it answers "no, I'm fine".
4. Trigger at a task seam when the plan has one, instead of in the middle of a task's reasoning.

```typescript
export const COMPACT_AT = 0.70, MAX_TURNS = 20;
export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}
```

**Verify**

Run a long recorded trajectory and confirm the run passes turn 47 without a context-length error, and that no compaction ever fires above 70%. Track the compaction ratio (`tokens_before ÷ tokens_after`); alert when it drops below 1.5 on a large context, because that means the summarizer is barely shrinking anything.

---

## Q2. Right after compaction the agent re-reads files it already edited and undoes its own changes. What did I miss? [→ §3 The Pin Set, §5 The Resume Block]

**What you see**

Compaction runs, the transcript shrinks from 188k to 74k tokens, and the run continues. Five turns later the agent reads a file it already edited in turn 20 and produces a patch that reverses the earlier work. Nothing crashes. Nothing is logged as an error.

**Why**

Two pieces were missing. Without a pin set, the task specification, the invariants, the currently edited files, and the last user instruction are all just old messages competing to be evicted. Without a resume block, the agent wakes up with no state, so it re-derives everything from scratch and the bill triples.

**What to do**

Pin anything whose absence changes the *task* rather than the taste: system prompt, goal and definition of done, at most 5 invariants, the last user instruction, files with uncommitted edits, the unresolved loop failure, pending approvals, and the output schema. Then replace the evicted mass with a fixed-key resume block, hard-capped at 300 tokens. The keys are fixed because code reads them — a parser rebuilds the pending task list from `Open[]`, seeds the retry from `Repro`, and writes the audit event from `Evicted[]`. Free-form prose breaks all three.

```
Goal: refactor auth middleware to use shared session
Decisions: [session store = redis][kept jwt compat shim]
Open: [t5: update 3 call sites][t6: run integration]
Repro: npm test -- auth → FAIL test_refresh_rotation
Next: fix refresh rotation, then t5, t6
Invariants: [no new deps][JWT v1 must validate]
```

**Verify**

Assert three things on every compaction: no pinned span id appears in the dropped list, `totalTokens(kept) ≤ budget`, and the resume block is under 300 tokens. Derive the pin set from the plan and the pending gate list, never by hand — and make a resolved loop's failure signal become evictable again, or your pin set grows until it eats the budget on its own.

---

## Q3. The agent forgot a rule I gave it in turn 12 — "no new runtime dependencies" — and added a package. How does that happen? [→ §4 Utility-Based Pruning]

**What you see**

Turn 12 carried an 80-token constraint: `no new deps`. Turn 44 the agent installs a new package. Meanwhile three `ls` calls from turns 38–40 are still in context, and turn 4's 40 KB tool output — the one the agent actually needs at turn 44 — is gone.

**Why**

Oldest-first eviction assumes value decays with age. In an agent run it does not. That order throws away one irrelevant span and one fatal one, and keeps three recent directory listings. Value lives in the plan graph, not in the message list: a span that feeds a *pending* task is gold, a span that feeds a *finished* task is dead weight.

**What to do**

Score each span, evict ascending score, never crossing the budget. Weight recency at only 0.30 so it cannot outvote structure.

```text
utility = 0.30·recency + 0.40·structural_reachability + 0.30·failure_signal
reachability = 1.0  if the span feeds a PENDING plan task
                0.1  if it feeds only COMPLETED tasks
                0.4  otherwise (parallel work or unknown)
```

Two refinements pay for themselves immediately. Collapse three or more identical retries into one line — six failing `npm test` runs become `retried 6×, last_err: E2BIG @ test_refresh_rotation`, 18k tokens down to 24, with the error preserved verbatim. And summarize a finished branch in one line instead of dropping it: `branch t3 (vector cache) rejected: adds 400ms p99`. That one line stops the agent from re-exploring a road it already drove.

**Verify**

Assert no FIFO ordering in code review, and check that a span carrying the active loop's error line scores highest among its peers. Prune first, summarize second — pruning dead spans is free and lossless, so summarizing before pruning costs roughly 40% more and keeps less.

---

## Q4. The run finished green, but the code quietly contradicts a decision the user agreed to 40 minutes ago. What went wrong? [→ §6 The Compaction↔Memory Contract]

**What you see**

A compaction evicted the span where the agent chose the session store. Nothing warned you. The run succeeded, and the codebase is subtly inconsistent with the design the user signed off on. In the next session nobody — human or agent — can explain why it was built that way.

**Why**

The contract between transient context and durable memory was never closed. The information was inside a span that got evicted, and nobody persisted it first. This is the most commonly broken contract in production, because it fails silently: the run completes.

**What to do**

Ask one question to sort the two sides: *will this still be needed after this run?* Turn 4's tool output might be needed at turn 44 — that is context's job. A decision made at turn 12 will be needed by a different run next week — that is memory's job. Then persist before evicting. Not after. Not "later". If the persist step fails, abort the compaction — do not log a warning and continue.

```
1. select spans to evict (utility ascending)
2. extract durable content: decisions, open items, invariants, preferences
3. await memory.persist(facts, { fsync: true })   ← a throw here must abort
4. emit compaction event: { keptIds, evictedIds, ratio, resumeHash }
5. replace evicted spans with the resume block
```

**Verify**

Write the test that matters most: point the harness at a memory store whose `persist()` always throws, run a compaction over 40 real messages, and assert it rejects *and* that all 40 spans are still present. Then confirm every run's audit record contains `keptIds`, `evictedIds`, `ratio`, and `resumeHash`. A harness where you cannot reconstruct what the model lost is a harness you cannot debug.

---

## Q5. My resume block reads well and looks informative — and the agent still gets lost. How do I test it honestly? [→ §7 Compaction-Safe Prompts, §9 Testing Compaction]

**What you see**

The summary says "we were refactoring authentication and hit some issues". It feels complete. It fails on every line that matters: no goal, no open task, no command to re-trigger the bug, no next action. Meanwhile a paraphrased constraint turned `timeoutMs: 30000` into "the timeout is about 30 seconds", and a negative rule ("do NOT add deps") vanished because summarizers drop negatives first.

**Why**

A fluent summary creates a false impression of coverage — models often do *worse* with summarized context than with truncated context, because the prose reads like the whole story. Reading it yourself is not a test; you already know the run.

**What to do**

1. Judge the block by cold-start continuation, not by reading it: give a fresh agent with an empty context only the system prompt plus the resume block, and compare its next action to the next action from the full context.
2. Pin literal values. Paraphrase is where precision dies — keep `timeoutMs: 30000` raw and let prose sit around it.
3. Put invariants in both the HEADER and the FOOTER of the prompt, verbatim. Models attend reliably to the start and end of a long context, so a summarizer that keeps only the head and tail still preserves your constraints.
4. Keep task ids and file paths raw inside `Open[]`, and keep the raw failing error line inside `Repro`.

```typescript
it("a cold agent can continue from the resume block alone", async () => {
  const o = await writeBackAndCompact(realSpans, 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: realSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));
});
```

**Verify**

Run that test plus the invariant checks on every recorded trajectory that hit a compaction, in nightly CI. Real trajectories catch the edge cases synthetic ones never do. Finally, track the post-compaction eval score against non-compacted runs in SQL — a specific run that fails only when a compaction happened right before the failure is the strongest possible signal that your pin set is missing something.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md*
