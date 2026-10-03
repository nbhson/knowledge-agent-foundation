# ❓ FAQ — Calibration (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The model returned confidence 0.95 and the answer was still wrong — so is confidence useless? [→ §2 Confidence ≠ Probability of Correctness]

**What you see**

Your routing code sends every answer with `confidence >= 0.8` straight into production. On Thursday a ticket lands in the `infra` queue with `confidence: 0.95`, full distribution `billing 0.02 / infra 0.95 / product 0.02 / data 0.01` — and it should have gone to `billing`. Nothing in the response looks weak. The model was decisive, the schema was respected, and the answer was still the wrong queue.

**Why**

`confidence` on Choice and Score measures the **shape of the distribution** — how peaked versus how spread out it is. A fully peaked distribution returns `confidence → 1.0`; a perfectly flat one returns `confidence → 0.0`. It says nothing about whether the winning option is the right one. Think of a doctor's bedside manner: confidence is how firmly the diagnosis is stated, correctness is how often that diagnosis is right in cases like yours.

So a wrong answer can be very confident, as long as the wrong answer sits *inside* the schema you gave it. Type safety constrains the shape of the output; it does not check the selected category. Almeida confirmed this on Hacker News.

**What to do**

1. Treat confidence and correctness as **two separate checks**. Confidence is free and always available; correctness needs your own labelled data.
2. Gate on both numbers, not one. Read the winner's probability out of the distribution as a proxy for "likely right", and require both to pass:

```python
winner_p = probabilities.get(answer, 0.0)
if confidence >= HIGH_THRESHOLD and winner_p >= HIGH_THRESHOLD:
    band = "auto_act"
```

3. On `Score` questions, remember the probability-weighted score can land *between* two levels, so a single integer thrown away the information you needed.
4. Only labelled data can confirm the second half. Measure "correct given stated 0.8" and you own the real number.

**Verify**

Take 200 labelled decisions. Bucket them by stated probability and check that the `0.8` bucket really is ~80% correct. If it is 95%, your gate is looser than you think; if it is 60%, raise the bar. Re-run this every time the model version changes.

---

## Q2. Jev answered 0.50 — is that "medium confidence, lean yes"? Should I nudge it along? [→ §2.2 Noul Confidence = Margin from 0.5]

**What you see**

Your approval policy reads "if confidence < 0.5, send to a human". A Noul question comes back with `P(yes) = 0.50` and your computed confidence of `0.00`. The other case: `P(yes) = 0.45`, confidence `0.10` — your rule waves it through as a weak yes and the code acts. Six hours later the refund was for an account that was already closed.

**Why**

Noul has **no separate confidence field**. It is derived from the margin away from the midpoint:

```
Noul confidence = |p − 0.5| × 2
```

| P(yes) | Confidence | Reading |
|---|---|---|
| 0.01 | **0.98** | Very confident NO |
| 0.10 | **0.80** | Confident NO |
| 0.45 | **0.10** | Barely off midpoint — weak signal |
| 0.50 | **0.00** | Perfectly balanced — maximum doubt |

Near 0.5 means **balanced, not medium**. It is not "half a yes" — the evidence cuts almost evenly in both directions, which is exactly when a human should look.

**What to do**

1. Rename the field in your code from `medium` to `balanced`, so nobody reads it as a nudge.
2. Route anything with confidence below roughly `0.20` (that is `P(yes)` between 0.40 and 0.60) to **escalate**, not to confirm.
3. Treat `P(yes) = 0.99` as "confident yes" and `P(yes) = 0.01` as "confident no" — both are strong, just opposite.
4. If you keep many Noul questions sitting at 0.45–0.55, the state you sent is not discriminating. Add context instead of lowering the bar.

**Verify**

Log `P(yes)` and the derived confidence side by side for a week. If more than a few percent of Noul answers cluster in 0.45–0.55, log the question name too — it will point at the under-specified state, not at the model.

---

## Q3. I copied the 0.6 threshold everyone uses — why does my "high confidence" bucket still contain wrong answers? [→ §4.2 Choosing Thresholds from Labelled Data]

**What you see**

You set one global gate: above `0.6` auto-act, below escalate. It works fine for "which queue should this ticket go to" — a wrong queue is cheap to fix. Then you reuse the same `0.6` in front of a destructive tool call that deletes a staging database, and it passes on a wrong "allow". The blog-post number was never yours.

**Why**

The commonly quoted `0.6` — the Pydantic AI `typesafe_tool_call_threshold` — was picked on a small set of *internal support tickets*. It is a starting point, not a validated constant. One global number also assumes every question has the same error cost, and they do not.

**What to do**

1. Build a labelled set from *your* own examples and pick the threshold where the tradeoff you actually want happens.
2. Answer three questions before setting any number: how expensive is a wrong auto-action, how expensive is an unnecessary escalate, and is this number per question rather than global.
3. Set a posture per question type — low threshold for triage, high threshold for gating a destructive call, high to pass with a fallback on failure for verifying output.
4. Change one threshold at a time, and replay logged decisions against the new value before shipping.

```python
HIGH, LOW = 0.85, 0.60          # gating a destructive tool call
if confidence >= HIGH and winner_p >= HIGH:
    band = "auto_act"
elif confidence >= LOW:
    band = "confirm"
```

**Verify**

Replay a week of stored distributions against the candidate threshold. Count how many auto-actions would have been wrong, and check that number against the cost of a human glance. Store the threshold value *in the record* so old rows stay interpretable after a retune.

---

## Q4. The answer is one winner out of four — should I just take it and move on? [→ §3 Read the Distribution, Not Just the Winner]

**What you see**

Two responses look identical on the surface: both selected `billing`.

```
PEAKED:  billing 0.88  infra 0.05  product 0.04  data 0.03
FLAT:    billing 0.31  infra 0.26  product 0.25  data 0.18
```

The second one is a real case. The question was "which team owns this?" and the state you sent simply did not discriminate between the four teams. Your code logged `selected=billing` and moved on.

**Why**

The winner is downstream of your gate anyway; the distribution is where the diagnostic information lives. It is like a jury count: "Guilty, 12–0" and "Guilty, 7–5" are both convictions, but they are completely different signals. Reading only the verdict throws the count away.

**What to do**

1. Keep the full distribution in your agent state and in the log — probabilities are cheap to keep.
2. Read the shape before the answer. One option far above the rest means a clear signal; two options close means genuine ambiguity or an under-specified state; all options near-uniform means the question is not answerable from that state.
3. An unexpected option close behind the winner is a **taxonomy warning** — two labels may mean the same thing. Review the label list.
4. If the distribution is flat, escalate and fix the state, rather than lowering the threshold to force a decision.

**Verify**

For each question, plot the shape you saw next to whether the outcome was right. A peaked-but-wrong pattern points at bad labels; a flat-but-right pattern points at missing context in the state you send.

---

## Q5. Six months later someone asks "why did it route Tuesday's ticket that way?" — what do you have? [→ §6 Logging & Observability]

**What you see**

You get the question and you have nothing. The threshold was changed in March, the model was upgraded from `jev-1.13.0`, and no probabilities were stored — only the final answer. You cannot tell whether the old gate was too loose or the model got worse, and you cannot re-tune anything without re-running the model on old cases.

**Why**

Calibration drifts, models get versioned, thresholds change. Without an audit record per decision there is no way to answer the question, and no way to re-tune — the probabilities that were actually served are gone.

**What to do**

1. Log the decision metadata, and nothing else. The state stays out — it often contains personal data.

| Log ✅ | Don't log ❌ |
|---|---|
| `request_id`, question **names** | raw `state` (may contain PII) |
| selected answer, full probabilities | free-text customer content |
| confidence, threshold applied, model version | bearer keys / auth headers |
| outcome (acted / confirmed / escalated) | — |

2. Record the threshold *with each decision*, not just in your config file — that is what tells you what bar applied at that moment.
3. Capture `x-request-id` from the response header so a decision can be traced back to the provider's records.
4. Add the outcome later — right or wrong — once a human or the real world tells you.

```
req_8f2a…  route_ticket   bill .91 inf .04 …   thr .85   ACT
req_8f3b…  authorize_del  yes .58  no .42      thr .90   ESCAL
req_8f4c…  verify_draft   pass .77 fail .23    thr .90   CONFIRM
```

**Verify**

Pick any row from last quarter and replay it against tomorrow's thresholds — no new model calls needed, because the probabilities are stored. Then confirm no log line contains the ticket text or the authorization header.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
