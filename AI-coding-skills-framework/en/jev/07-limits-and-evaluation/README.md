# 🛑 07. Limits & Evaluation

> This section draws the **hard boundary of what Jev cannot do**, separates **type-safety from correctness**, and lays out the **evaluation discipline** you need before production: state hygiene, calibration measurement, threshold tuning, observability, anti-patterns, and a decision flowchart for when *not* to use Jev. Read [README.md](../README.md) first for the overall context of Module XIV — Jev & System One Models.

---

## 1. What Jev Can't Do

> **📌 Core Concept**
>
> **Definition:** Jev is a **System One Model** — fast, typed, calibrated *decisions*. It is **not an LLM**: no text/token generation, no visible explanations or reasoning chain, no tool-argument synthesis, no file reading, no images. Arithmetic, counting, and date comparison belong in **code**. Context window: **64k tokens** (32k state + longest question); beyond that → `ModelHTTPError` (`max_tokens_exceeded`).
> **Analogy:** **Jev is a traffic light, not a tour guide.** It tells you *go / stop / which lane* in milliseconds — it will never narrate the route, fold a map, or do your arithmetic at the destination.
> **Why it matters:** Teams waste cycles trying to coax explanations or generation out of a model that structurally cannot produce them — or worse, assume "it answered, therefore it explained/verified". Knowing the boundary up front routes every task correctly the first time.

### 1.1 The Limits Table

| Capability | Jev | What to use instead |
|------------|-----|---------------------|
| Text / token generation | ❌ None | LLM |
| Explanations / visible reasoning | ❌ None — you get probabilities, not prose | LLM (still uncalibrated) |
| Tool argument synthesis | ❌ No args — no-arg tools only, or fallback | LLM (`FallbackModel`) |
| Reading files / tool access | ❌ None — state is **provided** to it | Your code gathers state |
| Images / multimodal input | ❌ Text (string/JSON/array) state only | Multimodal LLM |
| Arithmetic / counting | ❌ Not its job | Code (`int`, `sum`, SQL) |
| Date comparison / math | ❌ Not its job | Code (`datetime`) |
| Long context | ⚠️ 64k total (32k state + longest question) → `ModelHTTPError: max_tokens_exceeded` | Chunk + map-reduce; LLM for long prose |
| Open-ended questions | ❌ Needs bounded schemas (≤255 options; 2–10 levels; yes/no) | LLM |

### 1.2 The Easy Way to Read It

```
 ┌──────────────────────────────────────────────────────────────┐
 │                     JEV IS…              NOT…                │
 │                                                              │
 │  a traffic light                   a tour guide              │
 │  a calibrated dial                 an essayist               │
 │  a gate with a threshold           a safety guarantee        │
 │  a classifier with a distribution  a reason-giving oracle    │
 │                                                              │
 │  state IN  ──►  typed decision OUT                           │
 │  prompt IN ──►  (nothing — it doesn't converse)              │
 └──────────────────────────────────────────────────────────────┘
```

> If the task needs **words back**, it's an LLM. If it needs a **decision back**, it's Jev. If it needs **1 + 1 = 2**, it's code.

---

## 2. Type-Safety ≠ Correctness

> **📌 Core Concept**
>
> **Definition:** A closed answer space (Choice/Score/Noul) guarantees the output is **one of the options you defined** — it closes the *shape* of the answer. It does **not** guarantee the selected option is the *right* one. Jev can still pick a wrong in-schema answer, **sometimes with high confidence**. Type safety ≠ factual correctness — confirmed publicly by CEO Diogo Almeida (Hacker News).
> **Analogy:** Like a **multiple-choice exam with a fixed answer sheet**: the pencil can only fill bubbles A–D (type-safe), but the chosen bubble can still be wrong — and the student can still feel very sure.
> **Why it matters:** This is the single most dangerous misconception about decision models. Teams treat `selected ∈ options` as a correctness guarantee, remove their fallbacks, and ship a system that is *consistently wrong within its schema*.

> **"A closed answer space stops out-of-schema invention. It does not guarantee the selected category is correct."**

### 2.1 What You Get vs What You Don't

```
        YOU GET                              YOU DON'T GET
 ┌────────────────────────────┐      ┌─────────────────────────────────┐
 │ • selected ∈ options       │      │ • proof the selection is right  │
 │ • full distribution        │      │ • immunity from wrong answers   │
 │ • calibrated confidence    │      │ • safety when confidence is high│
 │ • deterministic schema     │      │ • a replacement for evals       │
 └────────────────────────────┘      └─────────────────────────────────┘
              │                                    │
              ▼                                    ▼
   GREAT for gating, routing            STILL need: labelled evals,
   classification, verification         thresholds, fallbacks, humans
```

### 2.2 The High-Confidence Wrong Answer

From [04 — Calibration](../04-calibration/): confidence = distribution concentration. A peaked distribution on the **wrong** option yields confidence ≈ 1.0. Mitigations:

| Mitigation | Mechanism |
|------------|-----------|
| Fallback on every gate | Low *and* high stakes: something else can catch the error |
| Verify against ground truth where possible | Outcome logging → measure real error rate |
| Per-question thresholds from labels | High-stakes questions get high bars |
| Parallel Noul cross-check | Two questions can disagree → escalate |

---

## 3. State Hygiene

> **📌 Core Concept**
>
> **Definition:** **Accuracy falls as unrelated detail grows in `state`.** State hygiene is the discipline of building a **small, relevant** state slice — within the latency budget — rather than dumping everything you have into the request.
> **Analogy:** Like a **witness statement**: a tight, relevant account helps the jury; a 40-page autobiography with unrelated details *hurts* — buried facts get overlooked. The model reads the equivalent of one glance.
> **Why it matters:** Two failure modes share one root cause: (1) irrelevant context dilutes the signal → wrong answers; (2) huge context → 64k ceiling → `ModelHTTPError`. State hygiene fixes both, and *reduces cost and latency at the same time*.

### 3.1 Build the Right Context Slice

```
 WHAT YOU HAVE                    WHAT YOU SEND (state)
 ┌───────────────────────┐        ┌─────────────────────────┐
 │ full ticket history   │        │ subject + last message   │
 │ all user attributes   │   ──►  │ customer tier            │
 │ irrelevant metadata   │        │ (only fields the        │
 │ 40k tokens of logs    │        │  question needs)         │
 └───────────────────────┘        │ ~small, < 32k budget     │
                                  └─────────────────────────┘
```

| Do ✅ | Don't ❌ |
|-------|---------|
| Include fields the question actually uses | Dump entire records "just in case" |
| Truncate prose to the discriminating part | Paste full logs into state |
| Keep state well under 32k tokens | Approach the 64k ceiling and hope |
| Prefer derived features (tier, counts-in-code) | Ask Jev to count across a huge dump |
| Re-slice when a question changes | Reuse a stale kitchen-sink state |

> **Latency budget matters too:** small state = faster turns = you can afford *more* questions per pass, which is where Jev's parallel evaluation pays off.

---

## 4. Evaluate Before Production

> **📌 Core Concept**
>
> **Definition:** Build an **evaluation set from your own labelled examples** and measure: actual **calibration** (stated probability vs outcome), **per-class accuracy**, and **threshold behavior** (precision/recall of your gate at candidate thresholds). Defaults from other people's data are not your data.
> **Analogy:** Like **calibrating a scale with known weights** before weighing patients — you don't assume the pharmacy scale is accurate because it's expensive.
> **Why it matters:** Every production guarantee (auto-act bands, tool-call thresholds) is an empirical claim about *your* traffic. Ship without the eval and you're shipping an unmeasured claim — the `0.6` default was chosen on a **small internal support-ticket set**, explicitly *not validated* as universal.

### 4.1 Build the Eval Set

```
 your production / staging examples
            │
            ▼
   human-label the correct answer per question
            │
            ▼
   split: threshold-tuning set  +  held-out eval set
            │
            ▼
   run Jev on state (as it will be in prod) → record p, selected, confidence
            │
            ▼
   compare predictions vs labels → calibration + accuracy + threshold curves
```

### 4.2 Metrics Table

| Metric | What it tells you | How |
|--------|-------------------|-----|
| **Calibration (prob vs outcome)** | Does 0.8 mean ~80% correct? | Bucket by stated p; plot actual accuracy per bucket |
| **Per-class accuracy** | Which classes are systematically confused? | Confusion matrix on `selected` vs label |
| **Gate precision/recall at τ** | What does auto-act *actually* catch/miss? | Sweep threshold over labelled set |
| **Escalation rate** | What % of traffic hits humans? | Count below-threshold decisions |
| **Latency distribution** | Does your state fit the budget? | p50/p95 of response times per payload size |
| **Error rate by state size** | Is hygiene degrading accuracy? | Slice accuracy vs token count |

> **Note:** list fan-out and nested accuracy are **not yet officially measured** — treat any numbers you see for those as anecdotal and **validate on your own data**.

### 4.3 Minimal Eval Harness

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from collections import defaultdict
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"


def evaluate( labelled: list[dict],
              questions: dict,
              model: str = "jev-latest",
            ) -> dict:
    """labelled = [{"state": ..., "answers": {"q": "billing"}}, ...]"""
    buckets = defaultdict(lambda: [0, 0])          # p_bucket -> [stated, n]
    per_class = defaultdict(lambda: [0, 0])        # class -> [correct, n]
    gate = []                                      # (p, correct)

    for row in labelled:
        r = httpx.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": model, "state": row["state"], "questions": questions},
            timeout=10.0,
        )
        r.raise_for_status()
        res = r.json()["results"]

        for q, gold in row["answers"].items():
            pred = res[q]
            p = pred["probabilities"].get(pred["selected"], 0.0)
            correct = pred["selected"] == gold

            b = round(p, 1)                        # 0.0, 0.1, … 1.0
            buckets[b][0] += int(correct)
            buckets[b][1] += 1

            per_class[gold][0] += int(correct)
            per_class[gold][1] += 1

            gate.append((p, correct))

    calibration = {b: c / n for b, (c, n) in sorted(buckets.items()) if n}
    acc_by_class = {k: c / n for k, (c, n) in per_class.items()}

    # sweep thresholds → pick YOUR operating point
    sweeps = {}
    for tau in [0.5, 0.6, 0.7, 0.8, 0.9]:
        auto = [(p, ok) for p, ok in gate if p >= tau]
        sweeps[tau] = {
            "coverage": len(auto) / len(gate),
            "auto_acc": (sum(ok for _, ok in auto) / len(auto)) if auto else None,
        }

    return {"calibration": calibration,
            "per_class_accuracy": acc_by_class,
            "threshold_sweep": sweeps}
```

</details>

---

## 5. Tuning Thresholds

> **📌 Core Concept**
>
> **Definition:** `typesafe_tool_call_threshold = 0.6` is a **starting point, not a validated value** — originally picked on a small internal support-ticket set. Set every threshold from **your** labelled examples, per question, and re-tune when data or model version changes.
> **Analogy:** Like a **thermostat set by the previous tenant** — 21°C might be fine in their house; yours has different windows. It's a number, not a law.
> **Why it matters:** The threshold *is* your risk policy expressed as a float. A misplaced threshold silently changes how often you auto-act vs escalate — usually discovered only after the incident review.

### 5.1 The Tradeoff

> **Higher threshold → hands off less, and is right more often when it does.**

```
 threshold τ ──────────────────────────────────────────►

 auto-act volume:   ████████████████░░░░░░░░░░░░░░░░░   high → low
 accuracy when
   auto-acting:     ░░░░░░░░░░░░░░████████████████████   low  → high

 sweet spot = YOUR cost of a wrong auto-act
              vs YOUR cost of an unnecessary escalation
```

| Wrong auto-action expensive (gating, charges) | Escalation expensive (high-volume triage) |
|-----------------------------------------------|-------------------------------------------|
| Push τ higher; accept more escalations | Lower τ; invest in review tooling for the residual |

### 5.2 Tuning Procedure

1. Collect **labelled** examples representative of production (state shape included).
2. Run Jev; record `selected`, probabilities, confidence per question.
3. **Sweep τ** — plot coverage vs accuracy of auto-acted decisions (see [§4.3](#43-minimal-eval-harness)).
4. Pick τ where your cost tradeoff is met — **per question**, not globally.
5. Hold out a test slice; confirm the chosen τ there.
6. Re-run whenever: model version changes, question wording changes, state shape changes, traffic mix drifts.

---

## 6. Observability in Production

> **📌 Core Concept**
>
> **Definition:** Every decision emits an audit record — `request_id`, question names, probabilities, confidence, threshold applied, model version, outcome — while the **state stays out of logs** (PII). Monitor **confidence drift** as an early-warning signal.
> **Analogy:** Like a **flight data recorder**: it doesn't record the passengers' conversations (privacy), it records the *instrument readings and inputs* — enough to reconstruct exactly why the plane did what it did.
> **Why it matters:** Thresholds change, models ship new versions, traffic shifts. Without this trail you cannot debug a bad week of decisions, prove what policy was in force, or safely retune anything.

### 6.1 Log Fields

| Field | Example | Why |
|-------|---------|-----|
| `request_id` | `req_8f2a…` | Correlate with downstream action |
| question names | `["route_ticket", "priority"]` | Which gate fired — not the payload |
| probabilities | `{billing: .91, infra: .04, …}` | Enables offline re-thresholding |
| confidence | `0.87` | Distribution concentration at decision time |
| threshold | `0.80` | Policy *as applied then* |
| model version | `jev-1.13.0` | Version drift detection |
| outcome | `acted / escalated`, later `right / wrong` | Feeds calibration monitoring |

**Never log:** raw `state`, full request bodies, auth headers.

### 6.2 Confidence Drift

```
 calibration dashboards to watch:

  stated p bucket     actual accuracy (rolling)
  ───────────────     ─────────────────────────
  0.9                 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ~90%  ✅ stable
  0.8                 ▓▓▓▓▓▓▓▓▓▓▓▓▓     ~80%  ✅
  0.7                 ▓▓▓▓▓▓▓▓▓         ~65%  ⚠ investigate
                          ▲
                          └── was ~75% last month → DRIFT
                              (state changed? model updated? traffic mix?)
```

- **Confidence distribution shifting** (suddenly everything is 0.95) → suspect state or model change.
- **Calibration sliding** (0.8 bucket now 65% accurate) → re-tune thresholds; consider rollback.

### 6.3 Decision Audit Trail

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │  DECISION AUDIT TRAIL                                               │
 │                                                                     │
 │  time │ request_id │ questions      │ probabilities │ thr │ verdict │
 │  ─────┼────────────┼────────────────┼───────────────┼─────┼───────  │
 │  09:01│ req_8f2a…  │ route_ticket   │ bill .91 …    │ .85 │ ACT ✅  │
 │  09:02│ req_8f3b…  │ authorize_del  │ yes .58 …     │ .90 │ ESC ⛔  │
 │  09:04│ req_8f4c…  │ verify_draft   │ pass .77 …    │ .90 │ CONF 🔎 │
 │                                                                     │
 │  + model_version, final outcome    − state omitted (PII)            │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Anti-Patterns

> **📌 Core Concept**
>
> **Definition:** These are the **recurring, recognizable ways** teams misuse Jev — each one looks reasonable in design review and fails (or quietly degrades) in production. Name them in your design docs so reviewers can point at them.
> **Analogy:** Like **pilot error checklists** — the mistakes are classic precisely because the wrong action feels natural under pressure ("just ask the model to explain itself").
> **Why it matters:** Most incidents in hybrid Jev/LLM systems trace to one of these eight, not to exotic model behavior.

| # | Anti-pattern | Why it fails | Fix |
|---|--------------|--------------|-----|
| 1 | **Using Jev as an oracle** | In-schema ≠ correct; high-confidence wrong answers happen | Evals + fallbacks ([§2](#2-type-safety--correctness)) |
| 2 | **Demanding explanations** | It has no text generation or visible reasoning — you'll get nothing or a fake | Log probabilities; explain in *your* code/dashboard |
| 3 | **Multi-factor questions** | "Score urgency×impact×effort" returns a plausible number with **low confidence** — blends don't live in one Score | Separate questions per factor; combine in code |
| 4 | **Writing questions into the prompt** | The LLM judges a question embedded in prose — uncalibrated, slow | State = material; `questions` = Jev's field ([06 anti-patterns](../06-jev-and-llm/)) |
| 5 | **Blind trust in high confidence** | Confidence is clarity, not correctness | Keep fallback even above threshold ([04](../04-calibration/)) |
| 6 | **No fallback on low confidence** | Escalate path missing → flat distribution silently degrades output | Three-band policy: act / confirm / escalate |
| 7 | **Skipping eval** | Copied `0.6`, never measured on your data | [§4 Evaluate Before Production](#4-evaluate-before-production) |
| 8 | **Ignoring state hygiene** | Unrelated detail → accuracy drop; oversized state → `ModelHTTPError` | [§3 State Hygiene](#3-state-hygiene) |
| 9 | **Letting a no-arg side-effect tool fire without approval** | "No-arg" ≠ "no risk" — an email/charge tool may take no *LLM-synthesized* args yet still need human authorization | Noul gate + approval workflow before execution ([06 §3](../06-jev-and-llm/)) |

---

## 8. When NOT to Use Jev

> **📌 Core Concept**
>
> **Definition:** A three-way routing rule: **need text → LLM**; **exact rule → code**; **fast judgment within a known schema → Jev**. Most real systems need all three, wired in that order of checks.
> **Analogy:** Like a **toolbox triage**: hammer for nails, screwdriver for screws, spanner for nuts — the skill is classifying the fastener, not swinging harder.
> **Why it matters:** Wrong-tool selection is the most expensive design error in this module: Jev on prose stalls outright, LLM on gates burns latency and calibration, and code on semantic judgment produces brittle string matching.

### 8.1 The Decision Flowchart

```
                 ┌──────────────────────────┐
                 │  What does this step need?│
                 └────────────┬─────────────┘
                              │
              ┌───────────────┼───────────────────┐
              ▼               ▼                   ▼
      NEED TEXT back?   EXACT RULE over      FAST JUDGMENT within
      (draft, explain,  known values?        a KNOWN SCHEMA?
       summarize, chat) (status==500,        (classify, route, gate,
              │          sum, date diff)      verify, rank)
              │               │                   │
              ▼               ▼                   ▼
      ┌──────────────┐  ┌────────────┐     ┌──────────────┐
      │     LLM      │  │   CODE     │     │     JEV      │
      │ writes text  │  │ deterministic│    │ typed result │
      │ slow·costly  │  │ free·exact │     │ 70–500ms     │
      └──────────────┘  └────────────┘     │ calibrated p │
                                            └──────┬───────┘
                                                   ▼
                                            threshold band
                                            act / confirm / escalate
```

### 8.2 Quick Reference

| Signal in the requirement | Route to |
|---------------------------|----------|
| "write", "explain", "summarize", "respond", "reason step by step" | **LLM** |
| "compare dates", "count", "sum", "exact match", "sort by field" | **Code** |
| "classify", "route", "is this authorized?", "does this pass?", "rank these" | **Jev** |
| "and also write a paragraph about it" | **Both** — Jev decides, LLM writes ([06](../06-jev-and-llm/)) |

> **Bottom line:** Jev earns its place on the *decision* steps — everywhere else, reach for the tool whose job it actually is.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [06 — Jev + LLM](../06-jev-and-llm/) · Next: back to [Module XIV overview](../README.md)*
