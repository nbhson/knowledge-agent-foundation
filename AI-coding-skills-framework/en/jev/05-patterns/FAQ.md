# ❓ FAQ — Production Patterns (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My latency budget is tight — can I really ask four questions in one call, or does each question cost extra time? [→ §1 Overview]

**What you see**

You have an interactive intake endpoint with a 1-second budget. You need to know the destination queue *and* the urgency of a support ticket, plus two more checks. You assume one call per question, so you either drop the extra checks or you chain four calls and blow the budget.

**Why**

All questions inside a single POST are evaluated **in parallel, in one pass** — 70–500 ms for the whole set, not per question. The pattern is a division of labor: Jev (the decision layer) returns a typed result, ordinary code performs the action, and a large language model (an AI that writes text) is only used where language must be generated. Asking the model to do the routing is what makes things slow: a Jev decision step is 40–200× faster than a language-model call, and input tokens cost about $0.042 per million with free output.

**What to do**

1. Batch related decisions into **one** call. Routing & triage already does this: one Choice question for the queue, one Score question for the priority.
2. Send **small and relevant state only** — subject, body snippet, customer tier. Pasting the whole ticket history lowers accuracy.
3. Set a real timeout (`timeout=5.0`) and put the threshold decision in code, not in the model.
4. Route below threshold to a human queue instead of guessing.

```python
questions = {
    "queue":    {"type": "choice", "options": ["billing","infra","product","data"]},
    "priority": {"type": "score",  "levels": ["p0","p1","p2","p3"]},
}
band = "auto" if res["queue"]["confidence"] >= 0.7 else "human_review"
```

**Verify**

Time a call with one question and a call with four: the difference should be noise, not 4×. Then watch the misroute rate against your own labels for a week — `0.7` is a starting point, not a validated number, so retune it on your data.

---

## Q2. The agent is about to run something destructive on its own — can a decision model block the tool call? [→ §4 Gating Agent Actions]

**What you see**

The user asks "why is my invoice so high this month?" The agent, being fluent at deciding to just do it, calls the refund tool and pushes a branch with `--force`. Nothing in the loop ever asked a human, and there is no record of who decided. In LangChain this ships as `AutoModeMiddleware`; in Pydantic AI it is `typesafe_tool_call_threshold`.

**Why**

Without a gate, an open-ended judgment sits where a typed, calibrated check belongs. The fix is to put a **Noul** question (a yes/no question type) between intent and execution, and let ordinary code do the blocking — the model never grants or denies its own permission.

**What to do**

1. Before **every side-effecting** call (delete, charge, send), ask `user_authorizes: {"type": "noul"}`.
2. Put the user's latest message + tool name + target summary in the state — that is what the question is judged on.
3. Allow only when the probability is high **and** the margin is healthy; otherwise block and escalate.

```python
p_yes = res["user_authorizes"]["probability"]
margin = abs(p_yes - 0.5) * 2      # Noul has no separate confidence field
allowed = p_yes >= AUTH_THRESHOLD and margin >= 0.5
if not allowed:
    return escalate_or_ask_human(tool, audit)   # code decides, not the LLM
```

4. Log request id, probabilities, threshold, and outcome for every gate. Start at `0.80`, not the framework default of `0.6` — that default is a starting point, not validated.
5. Remember the limit: Jev does **not** judge whether the tool is safe to run. It classifies "did the user authorize this". The approval policy is yours.

**Verify**

Replay past incidents through the gate and confirm they would now be blocked. Check that no destructive tool is reachable without a gate (make it a CI test), and that a blocked call produces a log line with all four fields.

---

## Q3. I classified 500,000 records and now I don't know which labels to trust [→ §3 Classification & Tagging at Scale, §7 Map-Reduce]

**What you see**

The run finishes fast — `CONCURRENCY = 32` requests in flight, 70–500 ms each — and writes a `label` column for every row. Then the "spam" bucket looks implausibly large, and a report built on those labels is quietly wrong. There is no probability stored anywhere, so nothing can be re-checked later.

**Why**

Bulk classification is the *map* phase of map-reduce, and it is cheap enough that people store whatever comes back. But a low-probability label saved as fact poisons every downstream filter, report, and retrieval call built on it.

**What to do**

1. Always store **label + probability**, never the label alone.
2. `label_p ≥ 0.75` → store directly. Below → `needs_review = True`, and send it to a second pass, the language model, or a human queue. Do not silently accept it.
3. Bound fan-out with a semaphore so 500k records do not stampede the API.

```python
CONCURRENCY, LABEL_THRESHOLD = 32, 0.75
p = cat["probabilities"].get(cat["selected"], 0.0)
row = {"id": rec["id"], "label": cat["selected"], "needs_review": p < 0.75}
sem = asyncio.Semaphore(CONCURRENCY)      # bound it; don't stampede
```

4. Do the **reduce** step in plain code over the stored probabilities — counts by label, top-k, low-probability requeue. No model needed.
5. Decide which bands enter the aggregates: exclude escalated records from the counts, or the summary will lie.
6. Output is free — keep the full distribution per record so you can re-tune the threshold without re-running.

**Verify**

Report the share of `needs_review` rows. Pull 200 of them by hand and measure real accuracy. Run the label counts twice — with and without the escalated rows — and see whether the difference matters for your dashboard.

---

## Q4. Ranking puts "relevant" above "core", and my float floor doesn't filter anything [→ §6 Ranking & Filtering]

**What you see**

A RAG pipeline (search first, then ask the model) retrieves too much, so you add a Score pass to re-rank. Two symptoms: the sorted list looks scrambled, and a floor written as `0.5` drops nothing, because the answer is a *level*, not a number.

**Why**

The levels are an ordered scale — `irrelevant < weak < relevant < core` — and the model returns both a `selected` bucket and a probability-weighted score that may land **between** two levels. Sorting only by `selected` throws away the ordering information; filtering on a float compares apples to oranges.

**What to do**

1. Define the fixed ordered scale once and reuse it, so grades are comparable across queries.
2. Filter by **level index**, not by a float.
3. Sort by the weighted score, descending.

```python
LEVELS = ["irrelevant", "weak", "relevant", "core"]
FLOOR  = "weak"
kept = [c for c in ranked if LEVELS.index(c["selected"]) > LEVELS.index(FLOOR)]
kept.sort(key=lambda c: c["weighted_score"], reverse=True)
```

4. Ask one Score question per candidate in a **single** POST (`rel_0`, `rel_1`, …) — 70–500 ms for the batch, and shortlists are small by nature.
5. Keep the full distribution (output is free) for later re-tuning.
6. If the **top** hit has low confidence, widen the context or fetch more candidates — do not auto-trust it.
7. Never ask a language model to compare candidates pairwise; that is quadratic in prose. Use the Score pass.

**Verify**

Assert that every kept item's level index is above the floor index. Confirm the top hit's weighted score is greater than or equal to the second's. Log rank-1 confidence per query and review the queries where it is low.

---

## Q5. The verifier said "pass" but the draft still had a made-up number and a customer's email address [→ §5 Verify LLM Output, §4 Caveat]

**What you see**

The cascade returns `p_pass = 0.91`, above your `PASS_THRESHOLD = 0.85`, so the draft ships. A reader then finds a figure that appears nowhere in the source policy, and an email address that should never have left the system. The team's reaction is to delete the verifier entirely.

**Why**

High confidence is not the same as correct (see the calibration section, `../04-calibration/`). The verifier is a cheap, typed check against a standard — it is one signal, not a guarantee, and deleting it removes the only automated check you had.

**What to do**

1. Keep the cascade: the expensive model drafts **once**, the cheap calibrated model gates it in under 500 ms.
2. Pass a `grounded_in_policy` Noul plus a `worst_violation` Choice question in the **same** call, so a failure already comes with a reason.
3. Below threshold → route the rework with that flag instead of blindly retrying.

```python
PASS_THRESHOLD = 0.85
p_pass = res["grounded_in_policy"]["probability"]
if p_pass >= PASS_THRESHOLD:
    return {"status": "pass", "draft": draft}
return {"status": "fail", "flag": res["worst_violation"]["selected"],
        "next": "fallback_llm"}     # stronger model, human, or discard
```

4. Use the flag values as rework routing: `none`, `unsupported_claim`, `wrong_number`, `tone`, `pii_leak`. A `pii_leak` should never go to "try a stronger model" — it should go to a human.
5. Keep a fallback path **even above** the threshold for costly or customer-facing outputs.
6. Run it as the verifier step on every harness or CI iteration, not only before release.

**Verify**

On a labelled set of good and bad drafts, plot pass rate against true quality. Count how many `fallback_llm` rewrites get accepted the second time. Add a fixture containing a leaked email address and confirm it comes back as `fail` with `pii_leak`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*