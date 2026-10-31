# 🛑 07. Limits & Evaluation

> This section draws a clear line around **what Jev can't do**, explains why **safe output shape is not the same as a right answer**, and lays out the **simple checklist** you need before you ship: tidy state, checking calibration, setting limits, keeping logs, avoiding common traps, and knowing when *not* to use Jev. See [README.md](../README.md) for the big picture of Module XIV — Jev & System One Models.

---

## 1. What Jev Can't Do

> **📌 Core Concept**
>
> **Definition:** Jev is a **System One Model** — fast, typed, calibrated *decisions*. It is **not an LLM**: no text/token generation, no visible explanations or reasoning chain, no tool-argument synthesis, no file reading, no images. Arithmetic, counting, and date comparison belong in **code**. (Plain words: typed = the answer is a fixed structured value like `billing`, never prose; calibrated = its confidence number matches reality; tool-argument synthesis = writing out the details a tool needs, e.g. *which* file to delete.) Context window: **64k tokens** (32k state + longest question); beyond that → `ModelHTTPError` (`max_tokens_exceeded`). (Context window = how much text fits in one request; 64k tokens ≈ 100 pages.)
> **Analogy:** **Jev is a traffic light, not a tour guide.** It tells you *go / stop / which lane* in milliseconds — it will never narrate the route, fold a map, or do your arithmetic at the destination.
> **Why it matters:** Teams waste cycles trying to coax explanations or generation out of a model that structurally cannot produce them — or worse, assume "it answered, therefore it explained/verified". Knowing the boundary up front routes every task correctly the first time.

Signpost: this section sets the hard boundary of the tool — most failed Jev projects started by asking it for something it structurally cannot do.

### 1.1 The Limits Table

How to read it: each row is one capability. The **Jev** column says whether Jev can do it (❌ = no, ⚠️ = only partly); the last column names the tool that *should* do it. For instance, "text generation" = writing sentences — Jev can't, so use an LLM.

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

(Glossary: *no-arg tools* = tools that need no written-out details; *fallback* = a backup model or human path; *multimodal* = accepting images/audio too; *map-reduce* = split into chunks, process each, merge results; *bounded schema* = a fixed answer menu, e.g. at most 255 options.)

> **One-line summary:** Nine capabilities Jev can't do — each row names the tool that should do it instead.

### 1.2 The Easy Way to Read It

How to read it: the left side of each pair is what Jev **is**; the right side is what people wrongly expect it to be.

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

(Glossary: *classifier with a distribution* = it outputs one option plus a probability for every option; *oracle* = an all-knowing answer machine — Jev is not one.)

> If the task needs **words back**, it's an LLM. If it needs a **decision back**, it's Jev. If it needs **1 + 1 = 2**, it's code.

> **One-line summary:** Left side = what Jev is; right side = what people wrongly expect it to be.

> **One-line summary:** Jev only turns a small text state into a typed decision — text goes to the LLM, math to code, and anything over 64k tokens fails outright.

---

## 2. Type-Safety ≠ Correctness

> **📌 Core Concept**
>
> **Definition:** A closed answer space (Choice/Score/Noul) guarantees the output is **one of the options you defined** — it closes the *shape* of the answer. It does **not** guarantee the selected option is the *right* one. Jev can still pick a wrong in-schema answer, **sometimes with high confidence**. Type safety ≠ factual correctness — confirmed publicly by CEO Diogo Almeida (Hacker News). (Closed answer space = the model can only return values from your menu; Choice = pick-one, Score = 0–1 rating, Noul = yes/no/unknown; in-schema = inside the menu.)
> **Analogy:** Like a **multiple-choice exam with a fixed answer sheet**: the pencil can only fill bubbles A–D (type-safe), but the chosen bubble can still be wrong — and the student can still feel very sure.
> **Why it matters:** This is the single most dangerous misconception about decision models. Teams treat `selected ∈ options` as a correctness guarantee, remove their fallbacks, and ship a system that is *consistently wrong within its schema*. (Fallback = a backup path — human or another system — that catches errors.)

> **"A closed answer space stops out-of-schema invention. It does not guarantee the selected category is correct."**

### 2.1 What You Get vs What You Don't

How to read it: the left box = guarantees you actually get; the right box = protections people wrongly assume they get.

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

(Glossary: *full distribution* = the probability for every option, not just the winner; *deterministic schema* = the output structure never surprises you; *labelled evals* = test sets where a human wrote down the right answer.)

> **One-line summary:** You get shape guarantees, not correctness — evals, thresholds, and humans are still required.

### 2.2 The High-Confidence Wrong Answer

Signpost: this explains the scariest failure — the model being confidently wrong — and what blunts it.

From [04 — Calibration](../04-calibration/): confidence = distribution concentration. A peaked distribution on the **wrong** option yields confidence ≈ 1.0. (Peaked = nearly all probability on one option.) Mitigations:

| Mitigation | Mechanism |
|------------|-----------|
| Fallback on every gate | Low *and* high stakes: something else can catch the error |
| Verify against ground truth where possible | Outcome logging → measure real error rate |
| Per-question thresholds from labels | High-stakes questions get high bars |
| Parallel Noul cross-check | Two questions can disagree → escalate |

How to read it: **Mitigation** = the defense you add; **Mechanism** = how it protects you. For example, the *parallel Noul cross-check* means asking a second yes/no question — if the two answers disagree, escalate to a human.

> **One-line summary:** A peaked but wrong distribution reads as near-certain confidence; fallbacks and cross-checks blunt it.

> **One-line summary:** Type-safety only guarantees the answer's shape, never its truth — so keep fallbacks, thresholds from your own data, and a cross-check question even when confidence looks perfect.

---

## 3. State Hygiene

> **📌 Core Concept**
>
> **Definition:** **Accuracy falls as unrelated detail grows in `state`.** State hygiene is the discipline of building a **small, relevant** state slice — within the latency budget — rather than dumping everything you have into the request. (State = the input data bundle you send; latency budget = the maximum waiting time you can afford per request.)
> **Analogy:** Like a **witness statement**: a tight, relevant account helps the jury; a 40-page autobiography with unrelated details *hurts* — buried facts get overlooked. The model reads the equivalent of one glance.
> **Why it matters:** Two failure modes share one root cause: (1) irrelevant context dilutes the signal → wrong answers; (2) huge context → 64k ceiling → `ModelHTTPError`. State hygiene fixes both, and *reduces cost and latency at the same time*.

Signpost: this section explains how to build the input — because the same model gets better *and* cheaper when you send less.

### 3.1 Build the Right Context Slice

How to read it: left box = everything you *have*; right box = the small slice you actually *send*. (Context slice = the trimmed portion of data relevant to one question.)

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

How to read it: left column = the habit to adopt; right column = the habit to drop. For example, *"discriminating part"* = the text that actually tells your options apart, e.g. the error message itself, not the whole log file.

> **Latency budget matters too:** small state = faster turns = you can afford *more* questions per pass, which is where Jev's parallel evaluation pays off.

> **One-line summary:** Trim state to the fields the question reads — small input means faster, cheaper, more accurate calls.

> **One-line summary:** Send only the small, relevant slice — under 32k tokens — because extra detail both slows the call and quietly lowers accuracy.

---

## 4. Evaluate Before Production

> **📌 Core Concept**
>
> **Definition:** Build an **evaluation set from your own labelled examples** and measure: actual **calibration** (stated probability vs outcome), **per-class accuracy**, and **threshold behavior** (precision/recall of your gate at candidate thresholds). Defaults from other people's data are not your data. (Labelled = a human wrote down the correct answer; calibration = 0.8 confidence really means ~80% correct; precision/recall = of what your gate auto-approves, how much is right / how much of the right stuff it catches.)
> **Analogy:** Like **calibrating a scale with known weights** before weighing patients — you don't assume the pharmacy scale is accurate because it's expensive.
> **Why it matters:** Every production guarantee (auto-act bands, tool-call thresholds) is an empirical claim about *your* traffic. Ship without the eval and you're shipping an unmeasured claim — the `0.6` default was chosen on a **small internal support-ticket set**, explicitly *not validated* as universal. (Auto-act band = the confidence zone where the system acts without asking.)

Signpost: this section is the pre-flight checklist — measure on your own data before letting the model act by itself.

### 4.1 Build the Eval Set

How to read it: this is the assembly line for a test set, top to bottom: take real examples → label them → split → run → compare.

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

(Glossary: *held-out* = kept aside, never used for tuning, so it measures honestly; *p* = the probability of the chosen answer.)

> **One-line summary:** Label real examples, split them, and compare predictions to labels — that's the whole eval set.

### 4.2 Metrics Table

How to read it: each row is one number to track, what question it answers, and how to compute it. For instance, "calibration" answers: when the model says 0.8, is it right ~80% of the time?

| Metric | What it tells you | How |
|--------|-------------------|-----|
| **Calibration (prob vs outcome)** | Does 0.8 mean ~80% correct? | Bucket by stated p; plot actual accuracy per bucket |
| **Per-class accuracy** | Which classes are systematically confused? | Confusion matrix on `selected` vs label |
| **Gate precision/recall at τ** | What does auto-act *actually* catch/miss? | Sweep threshold over labelled set |
| **Escalation rate** | What % of traffic hits humans? | Count below-threshold decisions |
| **Latency distribution** | Does your state fit the budget? | p50/p95 of response times per payload size |
| **Error rate by state size** | Is hygiene degrading accuracy? | Slice accuracy vs token count |

(Glossary: *confusion matrix* = a table of predicted vs actual category, showing which get mixed up; *τ* = tau, the symbol for a threshold; *p50/p95* = the median and the "worst normal case" response times.)

> **Note:** list fan-out and nested accuracy are **not yet officially measured** — treat any numbers you see for those as anecdotal and **validate on your own data**. (List fan-out = scoring many items in one call.)

> **One-line summary:** Six metrics — calibration, per-class accuracy, gate precision/recall, escalation rate, latency, accuracy by state size — cover production readiness.

### 4.3 Minimal Eval Harness

Signpost: this is the smallest working script that runs the evaluation above — start from it rather than building from zero.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-4-3-minimal-eval-harness.py`](examples/01-4-3-minimal-eval-harness.py)

</details>

> **One-line summary:** Start from this minimal harness script instead of building evaluation from zero.

> **One-line summary:** Before production, measure calibration, per-class accuracy, and threshold behavior on your own labelled examples — other people's defaults are not evidence.

---

## 5. Tuning Thresholds

> **📌 Core Concept**
>
> **Definition:** `typesafe_tool_call_threshold = 0.6` is a **starting point, not a validated value** — originally picked on a small internal support-ticket set. Set every threshold from **your** labelled examples, per question, and re-tune when data or model version changes. (Threshold = the confidence cut-off: above it the system auto-acts, below it the call is blocked or handed to a human.)
> **Analogy:** Like a **thermostat set by the previous tenant** — 21°C might be fine in their house; yours has different windows. It's a number, not a law.
> **Why it matters:** The threshold *is* your risk policy expressed as a float. (Float = a decimal number like 0.6.) A misplaced threshold silently changes how often you auto-act vs escalate — usually discovered only after the incident review.

### 5.1 The Tradeoff

> **Higher threshold → hands off less, and is right more often when it does.**

How to read the picture: sliding the threshold right shrinks the auto-act volume but raises accuracy when it does act — the sweet spot depends on which mistake costs you more.

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

How to read it: the two columns are opposite situations. If a wrong automatic action costs money or safety (e.g. approving refunds), raise the bar; if human review itself is the bottleneck, lower it and build review tooling for what comes through.

> **One-line summary:** Raising the bar trades volume for accuracy; your cost of each mistake picks the spot.

### 5.2 Tuning Procedure

Signpost: this is the step-by-step recipe for finding *your* number.

1. Collect **labelled** examples representative of production (state shape included).
2. Run Jev; record `selected`, probabilities, confidence per question.
3. **Sweep τ** — plot coverage vs accuracy of auto-acted decisions (see [§4.3](#43-minimal-eval-harness)). (Sweep = try a range of values; coverage = the share of cases that clear the threshold.)
4. Pick τ where your cost tradeoff is met — **per question**, not globally.
5. Hold out a test slice; confirm the chosen τ there.
6. Re-run whenever: model version changes, question wording changes, state shape changes, traffic mix drifts.

> **One-line summary:** Sweep thresholds on labelled data, pick per question, confirm on held-out data, and re-tune on every change.

> **One-line summary:** Treat 0.6 as an unvalidated guess — tune one threshold per question from your own labelled data, and re-tune whenever anything about the inputs or the model changes.

---

## 6. Observability in Production

> **📌 Core Concept**
>
> **Definition:** Every decision emits an audit record — `request_id`, question names, probabilities, confidence, threshold applied, model version, outcome — while the **state stays out of logs** (PII). Monitor **confidence drift** as an early-warning signal. (Audit record = a small log line per decision, enough to reconstruct it; PII = personally identifiable information such as names or emails; confidence drift = the confidence numbers slowly moving away from reality.)
> **Analogy:** Like a **flight data recorder**: it doesn't record the passengers' conversations (privacy), it records the *instrument readings and inputs* — enough to reconstruct exactly why the plane did what it did.
> **Why it matters:** Thresholds change, models ship new versions, traffic shifts. Without this trail you cannot debug a bad week of decisions, prove what policy was in force, or safely retune anything.

Signpost: this section covers what to log while the system runs — so a bad week is explainable instead of a mystery.

### 6.1 Log Fields

How to read it: each row is one field to record per decision, with an example and why it matters. For instance, `model version` lets you spot when behavior changed because the model itself was updated.

| Field | Example | Why |
|-------|---------|-----|
| `request_id` | `req_8f2a…` | Correlate with downstream action |
| question names | `["route_ticket", "priority"]` | Which gate fired — not the payload |
| probabilities | `{billing: .91, infra: .04, …}` | Enables offline re-thresholding |
| confidence | `0.87` | Distribution concentration at decision time |
| threshold | `0.80` | Policy *as applied then* |
| model version | `jev-1.13.0` | Version drift detection |
| outcome | `acted / escalated`, later `right / wrong` | Feeds calibration monitoring |

(Glossary: *offline re-thresholding* = re-deciding with a different threshold on saved data, without new model calls; *payload* = the request content; *correlate* = link the log line to the action it caused.)

**Never log:** raw `state`, full request bodies, auth headers.

> **One-line summary:** Log the seven audit fields; never the state itself.

### 6.2 Confidence Drift

How to read the chart: each row groups decisions by stated confidence; the bars show real accuracy for that group. A group sliding downward (like the 0.7 bucket here) is your early warning.

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
- **Calibration sliding** (0.8 bucket now 65% accurate) → re-tune thresholds; consider rollback. (Rollback = revert to the previous model or config.)

> **One-line summary:** A confidence bucket sliding downward — or everything suddenly reading 0.95 — is your early warning to re-tune or roll back.

### 6.3 Decision Audit Trail

How to read it: one row per decision, like a receipt. ESC = escalated to a human, CONF = confirmed. Note that state is deliberately absent — privacy.

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

> **One-line summary:** One row per decision is enough to reconstruct exactly what happened and why.

> **One-line summary:** Log a small audit record for every decision (IDs, probabilities, threshold, model version) but never the state itself — that trail plus drift monitoring makes bad weeks debuggable.

---

## 7. Anti-Patterns

> **📌 Core Concept**
>
> **Definition:** These are the **recurring, recognizable ways** teams misuse Jev — each one looks reasonable in design review and fails (or quietly degrades) in production. Name them in your design docs so reviewers can point at them. (Anti-pattern = a known mistake pattern with a name, so you can spot it fast.)
> **Analogy:** Like **pilot error checklists** — the mistakes are classic precisely because the wrong action feels natural under pressure ("just ask the model to explain itself").
> **Why it matters:** Most incidents in hybrid Jev/LLM systems trace to one of these eight, not to exotic model behavior.

How to read the table: **#** = index; **Anti-pattern** = the mistake; **Why it fails** = the mechanism of the failure; **Fix** = what to do instead. For instance, #3: asking one question to blend several factors ("urgency × impact × effort") returns a vague, low-confidence number — ask one question per factor and combine in code.

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

(Glossary: *oracle* = an all-knowing answer machine; *side-effect tool* = a tool that changes the real world, like sending email or charging money; *no-arg* = needing no LLM-written details; *three-band policy* = act automatically / ask for confirmation / hand to a human.)

---

## 8. When NOT to Use Jev

> **📌 Core Concept**
>
> **Definition:** A three-way routing rule: **need text → LLM**; **exact rule → code**; **fast judgment within a known schema → Jev**. Most real systems need all three, wired in that order of checks.
> **Analogy:** Like a **toolbox triage**: hammer for nails, screwdriver for screws, spanner for nuts — the skill is classifying the fastener, not swinging harder.
> **Why it matters:** Wrong-tool selection is the most expensive design error in this module: Jev on prose stalls outright, LLM on gates burns latency and calibration, and code on semantic judgment produces brittle string matching. (Semantic judgment = deciding based on meaning, not exact characters.)

Signpost: this is the final routing decision — read it before wiring anything, to avoid using Jev where it structurally cannot help.

### 8.1 The Decision Flowchart

How to read it: start at the top with what your step needs; the first matching branch wins — text → LLM, exact rule → code, judgment in a fixed menu → Jev.

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

> **One-line summary:** First match wins: text → LLM, exact rule → code, judgment in a fixed menu → Jev.

### 8.2 Quick Reference

How to read it: find the keyword from your requirement in the left column; the right column names the tool that should do it. For instance, "compare dates" is exact math → your code.

| Signal in the requirement | Route to |
|---------------------------|----------|
| "write", "explain", "summarize", "respond", "reason step by step" | **LLM** |
| "compare dates", "count", "sum", "exact match", "sort by field" | **Code** |
| "classify", "route", "is this authorized?", "does this pass?", "rank these" | **Jev** |
| "and also write a paragraph about it" | **Both** — Jev decides, LLM writes ([06](../06-jev-and-llm/)) |

> **Bottom line:** Jev earns its place on the *decision* steps — everywhere else, reach for the tool whose job it actually is.

> **One-line summary:** Match the tool to the need — the keyword table settles it in seconds.

> **One-line summary:** Route by need — text to the LLM, exact rules to code, and only fast judgments inside a fixed answer menu to Jev.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [06 — Jev + LLM](../06-jev-and-llm/) · Next: back to [Module XIV overview](../README.md)*

