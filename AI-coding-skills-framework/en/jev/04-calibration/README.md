# 🎯 04. Calibration — Honest Probabilities

> This section covers **what "well-calibrated" means for a fast decision model**, why **confidence is not the same as being right**, how to **read the whole result instead of just the top pick**, and how to **set limits and keep track** of decisions in real use. Start with [README.md](../README.md) for the big picture of Module XIV — Jev & System One Models.

---

## 1. What "Calibrated" Means

This section explains the word "calibrated" — the word that decides how much you can trust Jev's numbers. Every threshold and gate you build later sits on top of these numbers.

> **📌 Core Concept**
>
> **Definition:** A **calibrated** model is one whose stated probabilities match reality: when Jev assigns probability **0.8** to an answer, that answer should be correct roughly **80% of the time** (probability = a number from 0 to 1 saying how likely something is). The probabilities are *epistemically honest* — they describe the model's actual reliability, not a rhetorical flourish ("epistemically honest" = honest about what the model actually knows).
> **Analogy:** Like a **weather forecaster** who says "70% chance of rain" — a good forecaster is wet 7 out of 10 times on those days, not 2 out of 10. A calibrated decision model works the same way: its numbers can be *trusted as numbers*.
> **Why it matters:** Thresholds, bands, and fallbacks are all built on top of probabilities (threshold = a cut-off line, e.g. "act only above 0.8"; band = a range between two cut-off lines). If the probabilities are inflated (overconfidence) or deflated (underconfidence), every downstream gate is wrong. Calibration is what makes "auto-act above 0.8" a real policy instead of a guess.

### 1.1 "Epistemically Honest" Probabilities

Most LLM outputs are **confident by default** — the training process rewards fluent, decisive-sounding text, so the model can be *wrong and eloquent* at the same time (LLM = large language model, the kind of AI that writes text). Its verbal confidence carries little information about its actual error rate.

Jev is trained differently: probabilities are optimized against **outcomes**. The reward is *"was the stated probability consistent with what actually happened?"* — not *"did a human rater like this answer?"*. The result is a distribution you can put on a scoreboard (distribution = the full set of probabilities across all possible answers):

```
Jev calibration target:

  stated p ≈ 0.8   ──►  correct ≈ 80% of the time
  stated p ≈ 0.6   ──►  correct ≈ 60% of the time
  stated p ≈ 0.5   ──►  correct ≈ 50% of the time  (coin flip — honest about it)
```

> **The practical definition of "epistemically honest":** the number in the response is a *forecast you can bet on*, not a tone of voice.

> **One-line summary:** Calibrated = the stated number matches the real success rate — 0.8 really means "right about 80% of the time".

### 1.2 LLM Overconfidence vs Jev Calibration

How to read it: each row compares a typical LLM with Jev on one property. For instance, the "Stated confidence" row says an ordinary LLM expresses certainty in words, while Jev returns an actual number per option.

| Property | Typical LLM | Jev (System One Model) |
|----------|-------------|------------------------|
| Stated confidence | Verbal, stylistic | Numeric probability per option |
| Matches error rate? | Often inflated (overconfidence) | ~80% correct at 0.8 score |
| Optimized against | Human preference (RLHF) | Outcomes (RLCD) |
| Cheap to sample many times? | No — slow + token cost | Yes — 70–500 ms, parallel questions |
| Honest "I don't know" | Rarely | Distribution stays flat → low confidence |

> **One-line summary:** A chat LLM *sounds* sure; Jev's numbers are built to *be* sure at the stated rate.

### 1.3 RLHF vs RLVR vs RLCD

Jev's calibration comes from **RLCD (Reinforcement Learning for Calibrated Decisions)** — probabilities optimized against outcomes, not human preference. Gloss on the three acronyms: **RLHF** = training on human preference (a rater picks which answer they like); **RLVR** = training on verifiable right/wrong answers; **RLCD** = training on whether the stated probability matched the real outcome.

How to read it: each row is one training method; the "Feedback signal" column is the information the trainer gets back after each answer. For instance, RLHF's signal is a human saying "I prefer A over B".

| Method | What is optimized | Feedback signal | Typical result |
|--------|-------------------|-----------------|----------------|
| **RLHF** | Preference between outputs | Human rater likes A over B | Fluent, agreeable, often overconfident |
| **RLVR** | Correct answers on verifiable tasks | Ground-truth check (right/wrong) | Accurate on solvable tasks; weak on "how sure are you?" |
| **RLCD** | Probability quality itself | Stated probability vs actual outcome | **Calibrated** — 0.8 means ~80% |

```
RLHF:  "Which answer do you prefer?"      ──►  fluency + agreeableness
RLVR:  "Was it right?"                    ──►  accuracy (no honesty about doubt)
RLCD:  "You said 0.7 — was it right 70%?" ──►  calibration (honest probabilities)
                                              ▲
                                              └── Jev trains here
```

> Jev is **not an LLM** and does **no text/token generation** — it is a transformer-based model trained on synthetic data via RLCD, returning typed decisions with distributions. See [02 — Primitives](../02-primitives/) for Choice / Score / Noul.

> **One-line summary:** RLHF optimizes for liked answers, RLVR for right answers, RLCD for honest probabilities — Jev trains with RLCD.

---

## 2. Confidence ≠ Probability of Correctness

This section explains the most misread field in the API: `confidence`. Confusing it with "probability of being right" is how false-safety gates get built.

> **📌 Core Concept**
>
> **Definition:** Jev's `confidence` field (on Choice and Score) measures the **concentration / shape of the distribution** — how peaked vs how spread out it is (peaked = one option clearly ahead; flat = options nearly equal). It is **not** the probability that the selected answer is correct. For Noul, confidence is the **margin** from the midpoint: `|p − 0.5| × 2`.
> **Analogy:** Like a **doctor's bedside manner vs a lab test**: confidence is *how firmly the doctor states the diagnosis*; the probability of correctness is *how often that diagnosis is right in cases like this one*. A doctor can be very firm and still wrong.
> **Why it matters:** Teams routinely set gates on `confidence`, then are surprised when a **wrong in-schema answer arrives with high confidence** (in-schema = a valid value from your own option list — the shape is legal, the content can still be wrong). Knowing the distinction is the difference between a working gate and a false sense of safety.

### 2.1 Choice / Score Confidence = Distribution Concentration

```
Fully peaked distribution (one option dominates)   →  confidence → 1.0
Perfectly flat distribution (all options equal)    →  confidence → 0.0

confidence describes SHAPE, not TRUTH:
  ┌───────────────────────────────┐
  │ ████████████████████  0.95    │  peaked → high confidence
  │  A    B    C    D             │  ...but A can still be WRONG
  └───────────────────────────────┘
```

A model can be **very sure and very wrong** — as long as the wrong answer is *inside* the schema you gave it. Type safety constrains the *shape* of the output; it does not guarantee the *selected category* is correct (Almeida confirmed this on Hacker News).

> **One-line summary:** Confidence says "the answer was decisive", never "the answer was right".

### 2.2 Noul Confidence = Margin from 0.5

Noul (the yes/no question type) returns `P(yes)` in `[0, 1]` — the probability that the answer is yes, on a scale from 0 to 1. Its confidence has **no separate field** — it is derived (calculated from P(yes) itself):

```
Noul confidence = |p − 0.5| × 2
```

How to read it: each row is one P(yes) value and the confidence it produces. For instance, P(yes) = 0.01 means "almost certainly no" — and that is a *strong* signal, hence confidence 0.98.

| P(yes) | Confidence `|p−0.5|×2` | Reading |
|--------|-------------------------|---------|
| 0.01 | `\|0.01 − 0.5\| × 2` = **0.98** | Very confident **NO** |
| 0.10 | **0.80** | Confident NO |
| 0.45 | `\|0.45 − 0.5\| × 2` = **0.10** | Barely off the midpoint — weak signal |
| 0.50 | **0.00** | Perfectly balanced — maximum doubt |
| 0.55 | **0.10** | Barely leans YES |
| 0.90 | **0.80** | Confident YES |
| 0.99 | **0.98** | Very confident YES |

> **Near 0.5 is "balanced", not "medium".** A Noul at 0.50 is not "medium confidence yes" — it is the model saying the evidence cuts almost evenly. Treat it as *escalate*, not *nudge* (escalate = hand the case to a human or another system).

> **One-line summary:** For Noul, the distance from 0.5 *is* the confidence — and 0.5 means "genuinely torn", not "kind of yes".

### 2.3 The One-Line Summary

> **Confidence is about clarity, not correctness.**
> High confidence = "the distribution is decisive". Correctness = "the decisive answer is the right one". You need both — and only *your labelled data* can confirm the second (labelled data = examples where you already know the right answer).

```
                    ┌──────────────────────┐
                    │  HIGH CONFIDENCE     │
   clear signal ───►│  + correct answer    │──► AUTO-ACT  ✅
                    │  + wrong answer      │──► FALSE SAFETY ⚠ (still happens)
                    └──────────────────────┘
                    ┌──────────────────────┐
                    │  LOW CONFIDENCE      │
 fuzzy signal   ───►│  (either way)        │──► ESCALATE / MORE CONTEXT
                    └──────────────────────┘
```

> **One-line summary:** Trust high confidence only after your own labelled data shows it deserves the trust.

---

## 3. Read the Distribution, Not Just the Winner

This section explains why you should read the full probability list, not only the top answer. The winner tells you *what* was picked; the distribution tells you *how close the call was*.

> **📌 Core Concept**
>
> **Definition:** Every Choice/Score response includes the **full probability distribution**, not just the selected option. Reading the distribution tells you *how ambiguous the decision was* — flat means "several answers are plausible", peaked means "one answer dominates".
> **Analogy:** Like a **jury vote count**: "Guilty, 12–0" and "Guilty, 7–5" are both convictions, but they are *completely different signals* about the case. Looking only at the verdict throws away the vote count.
> **Why it matters:** The winner is downstream of your gate anyway; the distribution is where the *diagnostic* information lives — it shows which alternatives are close, whether your question is well-posed, and whether the state you sent was sufficient.

### 3.1 Flat vs Peaked — Two Mini-Histograms

Read the two histograms side by side: the left one is decisive, the right one is a coin toss dressed up as an answer.

```
PEAKED (decisive)                    FLAT (ambiguous)
Question: "Is this a refund          Question: "Which team owns this?"
 request?"                            options: [billing, infra, product, data]

 billing  ████████████████ 0.88       billing  ████████ 0.31
 infra    ██ 0.05                     infra    ██████ 0.26
 product  █ 0.04                      product  ██████ 0.25
 data     ▌ 0.03                      data     █████ 0.18

 → act on billing with confidence     → the state didn't discriminate;
 → confidence HIGH                      add context or escalate
```

> **One-line summary:** Peaked = act; flat = the state didn't give the model enough to work with.

### 3.2 What the Distribution Reveals

How to read it: each row is one distribution shape, what it usually means, and the action to take. For instance, "one option ≫ others" (≫ = far bigger than) means the state carried a clear signal and you can auto-act.

| Distribution shape | What it usually means | What to do |
|--------------------|-----------------------|------------|
| One option ≫ others | Clear signal in state | Auto-act if calibrated threshold holds |
| Two options close | Genuine ambiguity, or under-specified state | Inspect both; consider richer state |
| All options near-uniform | Question not answerable from this state | Escalate; re-check the question design |
| Unexpected option close behind | Possible label overlap | Review taxonomy — labels may be too similar |

> **One-line summary:** The distribution is your free diagnostic — flat shapes point at bad questions or thin state, not bad luck.

### 3.3 Keep the Distribution in Agent State

Probabilities are cheap to keep around: store them alongside the decision so later steps (and later audits) can see *how sure* the system was when it chose. For Score, remember the **probability-weighted score can fall between levels** — another reason not to reduce the response to a single integer.

> **One-line summary:** Store the whole distribution, not just the winner — it costs nothing and answers "how sure were we?" later.

---

## 4. Thresholding & Bands

This section explains how to turn probabilities into actions: automatic, human-confirm, or hand-off. This is where the numbers become a working policy.

> **📌 Core Concept**
>
> **Definition:** Thresholding converts probabilities/confidence into **action policy**: act automatically, confirm with a human, or escalate. Bands are the usual three-tier version of that policy (band = one of the ranges between two thresholds).
> **Analogy:** Like **airport security lanes**: pre-check passengers sail through (high trust), random passengers get a scan (medium), flagged passengers go to secondary (low trust). One system, three responses — matched to signal quality.
> **Why it matters:** Without explicit thresholds, every consumer of the API re-invents its own — inconsistently. With bands, "what happens when the model is unsure" becomes a **designed decision**, not an accident.

### 4.1 The Standard Bands

How to read it: each row is one band — a range of confidence — and the action it triggers. For instance, "High" means above your top cut-off line, so the code executes on its own.

| Band | Signal | Action |
|------|--------|--------|
| **High** | confidence / p above your high threshold | **Auto-act** — execute the decision |
| **Medium** | between thresholds | **Confirm** — ask a human, or gather more context |
| **Low** | below low threshold | **Escalate** — route to a human, another system, or an LLM |

> **One-line summary:** Three bands, three actions: above the top line act, in the middle confirm, below the bottom line hand off.

### 4.2 Choosing Thresholds from Labelled Data

**Do not copy a threshold from a blog post.** The commonly cited `0.6` (e.g. Pydantic AI's `typesafe_tool_call_threshold`) is a *starting point* — originally chosen on a small set of internal support tickets, **not validated** for your domain. Build a labelled set from *your* examples and pick the threshold where the tradeoff you want actually occurs.

```
Guiding questions when setting a threshold:
  • How expensive is a wrong auto-action?   (higher bar)
  • How expensive is an unnecessary escalate? (lower bar)
  • Per question?  Different questions deserve different bars.
```

> **One-line summary:** A threshold copied from someone else's data is a guess — pick yours from your own labelled examples and error costs.

### 4.3 Per-Question Thresholds

A single global threshold is usually too coarse. Routing, gating, and verification have different error costs (gating = blocking a risky action until a check passes).

How to read it: each row is one question type and the posture it deserves. For instance, blocking a destructive tool call needs a much higher bar than picking an email queue.

| Question type | Typical posture |
|---------------|-----------------|
| Low-risk triage (which queue?) | Lower threshold — wrong queue is cheap to fix |
| Gating a destructive tool call | High threshold — wrong "allow" is expensive |
| Verification of LLM output | High threshold to pass; fail → fallback |

> **One-line summary:** Match the bar to the blast radius — cheap mistakes get low thresholds, expensive ones get high thresholds.

### 4.4 The Gate Pipeline

Read the diagram top to bottom: one Jev call, then a threshold comparison, then the branch into auto-act or human/LLM handling.

```
                    ┌─────────────┐
   state ──────────►│    JEV      │──► selected + probabilities + confidence
   questions ──────►│ (one pass)  │
                     └──────┬──────┘
                            ▼
                    ┌───────────────┐
                    │ compare to    │
                    │  THRESHOLD(s) │
                    └───┬───────┬───┘
                  high  │       │  low / mid
                        ▼       ▼
                  ┌─────────┐ ┌──────────────────┐
                  │  ACT    │ │ CONFIRM / ESCALATE│
                  │(auto)   │ │(human / LLM / more│
                  └─────────┘ │      context)      │
                              └───────────────────┘
```

> **One-line summary:** One call, one comparison, one branch — above the line the code acts, below it a human or LLM takes over.

---

## 5. Example Decision Pipeline Code

A complete, small pipeline: call Jev, read **probabilities and confidence**, apply a threshold, and branch into act / confirm / escalate.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-5-example-decision-pipeline-code.py`](examples/01-5-example-decision-pipeline-code.py)

</details>

> **One-line summary:** The code shows the whole loop end to end: call, read, compare, branch.

---

## 6. Logging & Observability

This section explains what to record about every decision. Observability = being able to answer "what did the system do and why?" after the fact — impossible without logs.

> **📌 Core Concept**
>
> **Definition:** Every gated decision should leave an **audit record**: request id, question names, probabilities, confidence, threshold applied, model version, and the eventual outcome (audit record = a saved line describing each decision, enough to reconstruct it later). The **state itself stays out of the logs** — it often contains PII (PII = personally identifiable information: names, emails, phone numbers, account IDs).
> **Analogy:** Like a **cash register receipt**: it records *what was decided, under which rules, at which time* — not the customer's diary. Enough to reconstruct the decision later; not enough to leak the private material that fed it.
> **Why it matters:** Calibration drifts, models get versioned, thresholds change. Without this record you cannot answer "why did it route Tuesday's ticket that way?" — nor can you *re-tune* thresholds, because you no longer have the probabilities that were actually served.

### 6.1 What to Log (and What Not To)

How to read it: the left column lists fields that are safe and useful to log; the right column lists things that must stay out of logs because they are private, bulky, or secret. For instance, log the probability numbers but never the raw customer text.

| Log ✅ | Don't log ❌ |
|--------|-------------|
| `request_id` | raw `state` (may contain PII) |
| question **names** (not full payloads) | full request bodies |
| selected answer | free-text customer content |
| **probabilities** (full distribution) | bearer keys / auth headers |
| confidence | — |
| threshold(s) applied at decision time | — |
| model version (`jev-1.13.0`) | — |
| outcome (acted / confirmed / escalated, and later: right/wrong) | — |

> **One-line summary:** Log the numbers and the rules, never the raw evidence — enough to replay the decision, not enough to leak anyone.

### 6.2 The Decision Audit Trail

Read the sample records left to right: request id, question, probabilities, threshold, and the band that fired. One line = one replayable decision.

```
 ┌────────────────────────────────────────────────────────────────────┐
 │  DECISION AUDIT TRAIL                                              │
 │                                                                    │
 │  request_id  │ question      │ probs              │ thr │ band    │
 │  ────────────┼───────────────┼────────────────────┼─────┼───────  │
 │  req_8f2a…   │ route_ticket  │ bill .91 inf .04 … │ .85 │ ACT     │
 │  req_8f3b…   │ authorize_del │ yes  .58 no  .42   │ .90 │ ESCAL.  │
 │  req_8f4c…   │ verify_draft  │ pass .77 fail .23  │ .90 │ CONFIRM │
 │                                                                    │
 │  + model_version, thresholds, final outcome (right/wrong)          │
 │  − state intentionally omitted (PII)                               │
 └────────────────────────────────────────────────────────────────────┘
```

> **One-line summary:** One audit line per decision — request id, probabilities, threshold, band, outcome — and no customer data.

### 6.3 Thresholds Are the Audit Signal

The threshold recorded *with each decision* tells you what bar the system applied **at that moment** — essential when thresholds are later retuned. Replaying old decisions against new thresholds is how you validate a change before shipping it: you already logged the probabilities, so the replay needs no new model calls.

> **One-line summary:** Log the threshold next to each decision and you can re-tune later by replaying — no new model calls needed.

> Calibration is a **program**, not a property: measure it on your labels, band it, log it, re-check it when the model version or the state shape changes.

> **One-line summary:** Calibration is an ongoing routine — measure, band, log, re-check — not a one-time setting.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [02 — Primitives](../02-primitives/) · Next: [05 — Production Patterns](../05-patterns/)*
