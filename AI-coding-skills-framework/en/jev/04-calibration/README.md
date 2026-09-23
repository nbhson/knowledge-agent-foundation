# 🎯 04. Calibration — Honest Probabilities

> This section explains **what calibration means for a System One Model**, why **confidence is not the probability of being correct**, how to **read the full distribution instead of just the winner**, and how to **threshold, band, and log** decisions in production. Read [README.md](../README.md) first for the overall context of Module XIV — Jev & System One Models.

---

## 1. What "Calibrated" Means

> **📌 Core Concept**
>
> **Definition:** A **calibrated** model is one whose stated probabilities match reality: when Jev assigns probability **0.8** to an answer, that answer should be correct roughly **80% of the time**. The probabilities are *epistemically honest* — they describe the model's actual reliability, not a rhetorical flourish.
> **Analogy:** Like a **weather forecaster** who says "70% chance of rain" — a good forecaster is wet 7 out of 10 times on those days, not 2 out of 10. A calibrated decision model works the same way: its numbers can be *trusted as numbers*.
> **Why it matters:** Thresholds, bands, and fallbacks are all built on top of probabilities. If the probabilities are inflated (overconfidence) or deflated (underconfidence), every downstream gate is wrong. Calibration is what makes "auto-act above 0.8" a real policy instead of a guess.

### 1.1 "Epistemically Honest" Probabilities

Most LLM outputs are **confident by default** — the training process rewards fluent, decisive-sounding text, so the model can be *wrong and eloquent* at the same time. Its verbal confidence carries little information about its actual error rate.

Jev is trained differently: probabilities are optimized against **outcomes**. The reward is *"was the stated probability consistent with what actually happened?"* — not *"did a human rater like this answer?"*. The result is a distribution you can put on a scoreboard:

```
Jev calibration target:

  stated p ≈ 0.8   ──►  correct ≈ 80% of the time
  stated p ≈ 0.6   ──►  correct ≈ 60% of the time
  stated p ≈ 0.5   ──►  correct ≈ 50% of the time  (coin flip — honest about it)
```

> **The practical definition of "epistemically honest":** the number in the response is a *forecast you can bet on*, not a tone of voice.

### 1.2 LLM Overconfidence vs Jev Calibration

| Property | Typical LLM | Jev (System One Model) |
|----------|-------------|------------------------|
| Stated confidence | Verbal, stylistic | Numeric probability per option |
| Matches error rate? | Often inflated (overconfidence) | ~80% correct at 0.8 score |
| Optimized against | Human preference (RLHF) | Outcomes (RLCD) |
| Cheap to sample many times? | No — slow + token cost | Yes — 70–500 ms, parallel questions |
| Honest "I don't know" | Rarely | Distribution stays flat → low confidence |

### 1.3 RLHF vs RLVR vs RLCD

Jev's calibration comes from **RLCD (Reinforcement Learning for Calibrated Decisions)** — probabilities optimized against outcomes, not human preference. The landscape:

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

> Jev is **not an LLM** and does **no text/token generation** — it is a transformer-based model trained on synthetic data via RLCD, returning typed decisions with distributions. See [03 — Primitives](../03-primitives/) for Choice / Score / Noul.

---

## 2. Confidence ≠ Probability of Correctness

> **📌 Core Concept**
>
> **Definition:** Jev's `confidence` field (on Choice and Score) measures the **concentration / shape of the distribution** — how peaked vs how spread out it is. It is **not** the probability that the selected answer is correct. For Noul, confidence is the **margin** from the midpoint: `|p − 0.5| × 2`.
> **Analogy:** Like a **doctor's bedside manner vs a lab test**: confidence is *how firmly the doctor states the diagnosis*; the probability of correctness is *how often that diagnosis is right in cases like this one*. A doctor can be very firm and still wrong.
> **Why it matters:** Teams routinely set gates on `confidence`, then are surprised when a **wrong in-schema answer arrives with high confidence**. Understanding the distinction is the difference between a working gate and a false sense of safety.

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

### 2.2 Noul Confidence = Margin from 0.5

Noul returns `P(yes)` in `[0, 1]`. Its confidence has **no separate field** — it is derived:

```
Noul confidence = |p − 0.5| × 2
```

Worked examples:

| P(yes) | Confidence `|p−0.5|×2` | Reading |
|--------|-------------------------|---------|
| 0.01 | `\|0.01 − 0.5\| × 2` = **0.98** | Very confident **NO** |
| 0.10 | **0.80** | Confident NO |
| 0.45 | `\|0.45 − 0.5\| × 2` = **0.10** | Barely off the midpoint — weak signal |
| 0.50 | **0.00** | Perfectly balanced — maximum doubt |
| 0.55 | **0.10** | Barely leans YES |
| 0.90 | **0.80** | Confident YES |
| 0.99 | **0.98** | Very confident YES |

> **Near 0.5 is "balanced", not "medium".** A Noul at 0.50 is not "medium confidence yes" — it is the model saying the evidence cuts almost evenly. Treat it as *escalate*, not *nudge*.

### 2.3 The One-Line Summary

> **Confidence is about clarity, not correctness.**
> High confidence = "the distribution is decisive". Correctness = "the decisive answer is the right one". You need both — and only *your labelled data* can confirm the second.

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

---

## 3. Read the Distribution, Not Just the Winner

> **📌 Core Concept**
>
> **Definition:** Every Choice/Score response includes the **full probability distribution**, not just the selected option. Reading the distribution tells you *how ambiguous the decision was* — flat means "several answers are plausible", peaked means "one answer dominates".
> **Analogy:** Like a **jury vote count**: "Guilty, 12–0" and "Guilty, 7–5" are both convictions, but they are *completely different signals* about the case. Looking only at the verdict throws away the vote count.
> **Why it matters:** The winner is downstream of your gate anyway; the distribution is where the *diagnostic* information lives — it shows which alternatives are close, whether your question is well-posed, and whether the state you sent was sufficient.

### 3.1 Flat vs Peaked — Two Mini-Histograms

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

### 3.2 What the Distribution Reveals

| Distribution shape | What it usually means | What to do |
|--------------------|-----------------------|------------|
| One option ≫ others | Clear signal in state | Auto-act if calibrated threshold holds |
| Two options close | Genuine ambiguity, or under-specified state | Inspect both; consider richer state |
| All options near-uniform | Question not answerable from this state | Escalate; re-check the question design |
| Unexpected option close behind | Possible label overlap | Review taxonomy — labels may be too similar |

### 3.3 Keep the Distribution in Agent State

Probabilities are cheap to keep around: store them alongside the decision so later steps (and later audits) can see *how sure* the system was when it chose. For Score, remember the **probability-weighted score can fall between levels** — another reason not to reduce the response to a single integer.

---

## 4. Thresholding & Bands

> **📌 Core Concept**
>
> **Definition:** Thresholding converts probabilities/confidence into **action policy**: act automatically, confirm with a human, or escalate. Bands are the usual three-tier version of that policy.
> **Analogy:** Like **airport security lanes**: pre-check passengers sail through (high trust), random passengers get a scan (medium), flagged passengers go to secondary (low trust). One system, three responses — matched to signal quality.
> **Why it matters:** Without explicit thresholds, every consumer of the API re-invents its own — inconsistently. With bands, "what happens when the model is unsure" becomes a **designed decision**, not an accident.

### 4.1 The Standard Bands

| Band | Signal | Action |
|------|--------|--------|
| **High** | confidence / p above your high threshold | **Auto-act** — execute the decision |
| **Medium** | between thresholds | **Confirm** — ask a human, or gather more context |
| **Low** | below low threshold | **Escalate** — route to a human, another system, or an LLM |

### 4.2 Choosing Thresholds from Labelled Data

**Do not copy a threshold from a blog post.** The commonly cited `0.6` (e.g. Pydantic AI's `typesafe_tool_call_threshold`) is a *starting point* — originally chosen on a small set of internal support tickets, **not validated** for your domain. Build a labelled set from *your* examples and pick the threshold where the tradeoff you want actually occurs.

```
Guiding questions when setting a threshold:
  • How expensive is a wrong auto-action?   (higher bar)
  • How expensive is an unnecessary escalate? (lower bar)
  • Per question?  Different questions deserve different bars.
```

### 4.3 Per-Question Thresholds

A single global threshold is usually too coarse. Routing, gating, and verification have different error costs:

| Question type | Typical posture |
|---------------|-----------------|
| Low-risk triage (which queue?) | Lower threshold — wrong queue is cheap to fix |
| Gating a destructive tool call | High threshold — wrong "allow" is expensive |
| Verification of LLM output | High threshold to pass; fail → fallback |

### 4.4 The Gate Pipeline

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

---

## 5. Example Decision Pipeline Code

A complete, small pipeline: call Jev, read **probabilities and confidence**, apply a threshold, and branch into act / confirm / escalate.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import Any, Dict, Literal

import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"  # alias for jev-1.13.0

# Per-question thresholds — tune from YOUR labelled data, not defaults
HIGH_THRESHOLD = 0.85
LOW_THRESHOLD = 0.60

Decision = Literal["auto_act", "confirm", "escalate"]


@dataclass
class GatedDecision:
    answer: str
    probabilities: Dict[str, float]
    confidence: float
    band: Decision
    request_id: str | None


def decide(state: Any, questions: Dict[str, Any]) -> GatedDecision:
    """One Jev call → read the distribution → pick a band."""
    resp = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "state": state, "questions": questions},
        timeout=5.0,
    )
    resp.raise_for_status()
    body = resp.json()
    request_id = resp.headers.get("x-request-id")

    # Choice question: selected option + full distribution + confidence
    result = body["results"]["route_ticket"]
    answer = result["selected"]
    probabilities = result["probabilities"]
    confidence = result["confidence"]

    # Confidence = distribution concentration (NOT P(correct)).
    # For calibration you ALSO compare the winner's probability to labels.
    winner_p = probabilities.get(answer, 0.0)

    if confidence >= HIGH_THRESHOLD and winner_p >= HIGH_THRESHOLD:
        band: Decision = "auto_act"
    elif confidence >= LOW_THRESHOLD:
        band = "confirm"       # clear-ish signal — human glance or more context
    else:
        band = "escalate"      # flat distribution — human / another system / LLM

    return GatedDecision(answer, probabilities, confidence, band, request_id)


def handle_ticket(ticket: Dict[str, str]) -> str:
    """Act / confirm / escalate — the three-band policy in action."""
    d = decide(
        state=ticket,  # keep state SMALL and relevant — see 07 State Hygiene
        questions={
            "route_ticket": {
                "type": "choice",
                "options": ["billing", "infra", "product", "data"],
            },
            "priority": {
                "type": "score",
                "levels": ["p0", "p1", "p2", "p3"],
            },
        },
    )

    # Never log the state (PII) — log the decision metadata only
    audit = {
        "request_id": d.request_id,
        "question": "route_ticket",
        "selected": d.answer,
        "probabilities": d.probabilities,
        "confidence": d.confidence,
        "threshold_high": HIGH_THRESHOLD,
        "threshold_low": LOW_THRESHOLD,
        "model_version": MODEL,
        "band": d.band,
    }

    if d.band == "auto_act":
        return route_to_queue(d.answer)            # code acts
    if d.band == "confirm":
        return request_human_confirmation(d.answer)  # medium band
    return escalate_with_context(audit)              # low band
```

</details>

---

## 6. Logging & Observability

> **📌 Core Concept**
>
> **Definition:** Every gated decision should leave an **audit record**: request id, question names, probabilities, confidence, threshold applied, model version, and the eventual outcome. The **state itself stays out of the logs** — it often contains PII.
> **Analogy:** Like a **cash register receipt**: it records *what was decided, under which rules, at which time* — not the customer's diary. Enough to reconstruct the decision later; not enough to leak the private material that fed it.
> **Why it matters:** Calibration drifts, models get versioned, thresholds change. Without this record you cannot answer "why did it route Tuesday's ticket that way?" — nor can you *re-tune* thresholds, because you no longer have the probabilities that were actually served.

### 6.1 What to Log (and What Not To)

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

### 6.2 The Decision Audit Trail

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

### 6.3 Thresholds Are the Audit Signal

The threshold recorded *with each decision* tells you what bar the system applied **at that moment** — essential when thresholds are later retuned. Replaying old decisions against new thresholds is how you validate a change before shipping it: you already logged the probabilities, so the replay needs no new model calls.

> Calibration is a **program**, not a property: measure it on your labels, band it, log it, re-check it when the model version or the state shape changes.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [03 — Primitives](../03-primitives/) · Next: [05 — Production Patterns](../05-patterns/)*
