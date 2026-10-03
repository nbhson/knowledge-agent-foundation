# ❓ FAQ — Jev Limits & Evaluation (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I asked Jev to explain its choice and it gave me nothing back — is it broken? [→ §1 What Jev Can't Do]

**What you see**

You send a state and a question like `route_ticket`, and you get back a clean typed object: `selected: "billing"`, `probabilities: {billing: .91, infra: .04}`, `confidence: 0.87`. No words. You add a question named `why_billing` and you get `null`, an empty string, or something plausible and invented. You ask it to draft a customer reply, to read a file, to add up a list, or to compare two dates, and the call fails. It looks exactly like a model that is refusing to cooperate.

**Why**

Jev is a System One model: fast, typed, calibrated **decisions**. It is not a large language model (LLM). It has no text generation, no visible reasoning chain, no tool-argument synthesis, no file reading, no images. Its total context is 64k tokens — 32k for state plus the longest question — and anything beyond that returns `ModelHTTPError: max_tokens_exceeded`. Think of a traffic light, not a tour guide: it tells you go, stop, or which lane in milliseconds, and it will never narrate the route.

**What to do — route the task before you route the model**

| Signal in your requirement | Send it to |
|---|---|
| "write", "explain", "summarize", "respond" | LLM |
| "count", "sum", "compare dates", "exact match" | Code |
| "classify", "route", "is this authorized?", "rank these" | Jev |
| "decide it, then write a paragraph about it" | Both — Jev decides, LLM writes |

1. Stop asking Jev for prose. Log the probabilities and render the explanation yourself, in your own dashboard code.
2. If a step needs tool arguments synthesized from language, put an LLM in front as the fallback — Jev only accepts no-argument tools.
3. If you need arithmetic or date math, do it in code (`int`, `sum`, SQL, `datetime`) and feed the result in as a state field.
4. Do not write your question into a prompt and ask an LLM to judge it — that path is uncalibrated and slow. Questions belong in Jev's own `questions` field.

**Verify**

Grep your codebase for question names containing `explain`, `why`, or `reason` — there should be none. Confirm your UI renders probabilities, not sentences. Feed it a state that needs a file read and check the failure is a clean rejection, not a hallucinated answer.

---

## Q2. The output is always one of my options, so I deleted the fallback — was that a mistake? [→ §2 Type-Safety ≠ Correctness]

**What you see**

Jev returns `selected: "refund"` at confidence `0.94`, and the options were only `{billing, infra, refund, other}`. The schema is clean, the value is legal, and the answer is wrong. A peaked distribution sitting on the wrong option produces confidence close to 1.0, so the more certain it sounds, the more your team trusts it. This is not a bug report — the vendor's CEO has confirmed it publicly on Hacker News: a closed answer space stops out-of-schema invention, it does not guarantee the chosen category is correct.

**Why**

A closed answer space (Jev's `Choice`, `Score`, and `Noul` types) guarantees the **shape** of the answer, never its truth. It is a multiple-choice exam with a fixed answer sheet: the pencil can only fill bubbles A–D, but the chosen bubble can still be wrong — and the student can still feel very sure. Confidence measures how concentrated the distribution is. That is clarity, not correctness.

**What to do**

1. **Keep a fallback on every gate**, high stakes and low. Something other than the model must be able to catch the error.
2. **Verify against ground truth where you can.** Log the outcome, then measure the real error rate instead of assuming it.
3. **Set per-question thresholds from your own labelled data.** High-stakes questions get high bars.
4. **Cross-check with a parallel Noul question** (Jev's yes/no/null answer). Two questions that disagree is your escalation signal.
5. **Run a three-band policy**: act, confirm, escalate. Without the escalate band, a flat distribution silently degrades the output and nobody notices.

**Verify**

On a held-out labelled set, count the cases where `confidence ≥ 0.9` and `selected ≠ label`. That number is your real high-confidence error rate — if it is not zero, the fallback is not optional. Then grep the logs and confirm the escalate band actually fired on those runs.

---

## Q3. I hit `ModelHTTPError: max_tokens_exceeded`, and on another question accuracy quietly fell — is it the same bug? [→ §3 State Hygiene]

**What you see**

One endpoint starts throwing `ModelHTTPError: max_tokens_exceeded` right after a team added "just a couple more fields" to the state. On a different question, nothing errors at all — the per-class accuracy simply drops from 84% to 61%, and nobody can point at a commit. In both cases the state was built by dumping the whole record: full ticket history, every user attribute, irrelevant metadata, and a slice of 40k tokens of logs.

**Why**

Same root cause, two symptoms. The ceiling is 64k tokens total (32k state plus the longest question), so oversized state fails loudly. Below that ceiling, unrelated detail **dilutes the signal**, so it fails quietly. It behaves like a witness statement: a tight, relevant account helps the jury, while a 40-page autobiography with unrelated details buries the facts that matter. The model reads the equivalent of one glance.

**What to do**

1. Send only the fields the question actually reads: `subject`, `last message`, `customer tier`.
2. Truncate prose down to the part that discriminates between your options.
3. Compute derived features — tier, counts, totals — in code before the call, not in the dump.
4. Keep state well under the 32k budget. Do not approach the ceiling and hope.
5. Re-slice whenever a question changes. Never reuse a stale kitchen-sink state built for a different question.

```
WHAT YOU HAVE              WHAT YOU SEND
full ticket history   ──►  subject + last message
all user attributes   ──►  customer tier
irrelevant metadata   ──►  (only fields the question uses)
40k tokens of logs    ──►  small, comfortably under 32k
```

**Verify**

Log the token count per payload and watch the 95th percentile. Slice your accuracy by state size — if accuracy falls as tokens rise, hygiene is the problem. The `max_tokens_exceeded` error should disappear entirely once state is trimmed.

---

## Q4. We shipped with `typesafe_tool_call_threshold = 0.6` copied from the docs — how do I find the real number? [→ §4 Evaluate Before Production, §5 Tuning Thresholds]

**What you see**

The config says `typesafe_tool_call_threshold = 0.6`. Nobody measured it. It came from the documentation, where it was picked on a small internal set of support tickets and explicitly **not** validated as universal. Two weeks later a support lead asks why the bot auto-approved refunds it should have escalated, and you cannot answer, because you never recorded what fraction of traffic clears 0.6 or how often it is right when it does.

**Why**

The threshold is your risk policy expressed as a float. It was chosen on someone else's data, and a misplaced value silently changes how often you auto-act versus escalate — usually discovered only in an incident review. Moving it up means Jev hands off less often but is right more often when it does; moving it down does the reverse. The right point depends on **your** cost of a wrong auto-action versus **your** cost of an unnecessary escalation.

**What to do**

1. Collect labelled examples that look like production, state shape included.
2. Split them: one set for tuning the threshold, one held back for evaluation.
3. Run Jev, record `selected`, the probabilities, and confidence per question.
4. Sweep the threshold and plot coverage against accuracy of the auto-acted decisions.

```python
for tau in [0.5, 0.6, 0.7, 0.8, 0.9]:
    auto = [(p, ok) for p, ok in gate if p >= tau]
    print(tau, len(auto)/len(gate),                      # coverage
          sum(ok for _, ok in auto)/len(auto))          # accuracy when acting
```

5. Pick the value where your cost tradeoff holds — **per question**, not one global number. If a wrong auto-action is expensive (gating, charges), push it higher; if escalation is the expensive mistake (high-volume triage), lower it and build review tooling for what remains.
6. Re-tune whenever the model version, the question wording, the state shape, or the traffic mix changes.

**Verify**

The threshold sweep output is committed next to the config. The chosen value is confirmed on the held-out slice. The resulting escalation rate matches the human review capacity you actually have.

---

## Q5. Decisions got worse this month and nobody can say why — what was I supposed to log? [→ §6 Observability in Production]

**What you see**

Escalation volume jumps on a Tuesday. Auto-actions look wrong in three regions. When you ask "what threshold was in force, and which model version decided this?", the only record is an HTTP 200 in a proxy log. Two weeks of decisions are unrecoverable. On a dashboard, the 0.8 confidence bucket was ~80% accurate last month and is ~65% accurate now, and nobody was watching.

**Why**

Every decision is supposed to emit an audit record — like a flight data recorder. It captures the instrument readings and inputs, not the passengers' conversations, so the raw state stays out of the logs. Without that trail you cannot debug a bad week, prove which policy was active, or safely retune anything. Confidence drift is the early warning: a distribution that suddenly reads 0.95 everywhere suggests a state or model change; a calibration bucket sliding downward means re-tune or roll back.

**What to do**

| Field | Example | Why you need it |
|---|---|---|
| `request_id` | `req_8f2a…` | Correlate with the downstream action |
| question names | `["route_ticket", "priority"]` | Which gate fired, without the payload |
| probabilities | `{billing: .91, infra: .04}` | Re-threshold offline without new calls |
| confidence | `0.87` | Concentration at decision time |
| threshold | `0.80` | The policy *as applied then* |
| model version | `jev-1.13.0` | Detect version drift |

1. Record the outcome (`acted` / `escalated`, later `right` / `wrong`) so it feeds calibration monitoring.
2. Never log the raw state, full request bodies, or authentication headers — the state holds personal data.
3. Add the escalate band to your policy so a flat distribution degrades visibly instead of silently.

**Verify**

Pick any `request_id` from last month and rebuild the decision: inputs, threshold, model version. Confirm a scrub of the logs finds no state content. Watch the calibration chart weekly — if a bucket moves more than a few points, that is your investigation trigger.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*