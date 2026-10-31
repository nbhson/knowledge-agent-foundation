# 🔬 01. Core Concepts — Jev & System One Models

> This section covers **what Jev is**, **the fast/slow thinking split** behind it, **the short story of TypeSafe and Jev's name**, **the big-picture design**, **why skipping text generation is actually a strength**, **when to use it (and when not to)**, and **where Jev fits in your agent setup**. Start with [README.md](../README.md) for the full picture.

---

## 1. What Is Jev?

This section defines Jev and explains why "no text generation" is the whole point. Every later section leans on these words, so read them first.

> **📌 Core Concept**
>
> **Definition:** Jev is TypeSafe's first public model — a **System One Model**: a transformer-based model (transformer = the neural-network design behind GPT) that does **not generate text**. You send unstructured state (raw material: a ticket, a log line) plus named, typed questions; it returns typed answers (`Choice`, `Score`, `Noul`) with full probability distributions (how likely each possible answer is) and confidence, evaluated in parallel in one pass.
> **Analogy:** Like a **reflex arc** — you don't write an essay about whether the stove is hot; your hand just *moves*. Jev is that reflex for software: state in, decision out, no prose in between. The LLM (large language model — a GPT-style text generator) is the **inner narrator** who explains everything (beautifully, slowly, and sometimes incorrectly).
> **Why it matters:** Most software decisions — classify, rate, confirm — need a *value*, not a *paragraph*. Generating text to get that value costs tokens (billed word-pieces), latency (waiting time), parse failures, and calibration you never had. Jev turns the decision into a function call.

TypeSafe's own one-liner:

```
"Jev is a frontier-intelligence function call:
 unstructured state in → typed probabilistic decisions out."
```

### 1.1 Definition Card

How to read it: each row is one fact about Jev; the "Value" column is the fact itself. For instance, "Base" says what the model is built on, and "Latency" is how long one call takes.

| Property | Value |
|----------|-------|
| **Maker** | TypeSafe AI — AI lab in stealth ~2 years, founded 2024, San Francisco |
| **Model** | Jev — first public model; current version **jev-1.13.0** (alias **jev-latest**) |
| **Category** | First **"System One Model"** (after Kahneman's *Thinking, Fast and Slow*) |
| **Base** | Transformer-based; **no text/token generation** |
| **Training** | Exclusively **synthetic data** via **RLCD** (Reinforcement Learning for Calibrated Decisions) |
| **Preference** | Probabilities optimized against **outcomes** — *not* human preference (unlike RLHF) |
| **Weights / paper** | **None published** |
| **Latency** | End-to-end **70–500ms** (40–200× faster than frontier LLMs on System One-shaped tasks) |
| **Price** | **$0.042 per million input tokens**; output free |
| **Interface** | `POST https://api.typesafe.ai/v1/systemone` with Bearer API key |
| **Primitives** | **Choice** · **Score** · **Noul** |

> **One-line summary:** Jev is a transformer that returns typed, calibrated decisions instead of text — fast, cheap, and shaped like a function call.

### 1.2 What It Is NOT

This list sets the boundaries: what Jev cannot do, so you never ask it to.

```
Jev is NOT an LLM.
  ✗ does not generate text or tokens
  ✗ cannot write tool arguments, read files, or explain itself
  ✗ cannot do reliable arithmetic / counting / date comparison (keep those in code)
  ✗ cannot go beyond 64k total context (32k state + longest question)
```

Gloss: 64k total context = the model can only "see" about 64,000 tokens (word-pieces) at once — 32k for the state plus the longest question. Tool arguments = the parameters an agent fills in when calling a function.

It *looks* like an LLM call (JSON over HTTPS, bearer key, model name) and *behaves* like a calibrated decision function. Hold both facts at once and the rest of this module becomes easy.

> **One-line summary:** Jev is not an LLM — it returns typed decisions only; writing, arithmetic, and file reading belong elsewhere.

---

## 2. System One vs System Two (Kahneman)

This section explains the psychology behind the name. Knowing the split tells you which questions belong to Jev and which belong to an LLM.

> **📌 Core Concept**
>
> **Definition:** Daniel Kahneman's dual-process theory (his model of how minds work in two modes): **System 1** is fast, automatic, intuitive pattern-matching ("2+2", recognizing a face); **System 2** is slow, deliberate, effortful reasoning ("17 × 24", planning a budget). Jev is explicitly named for **System 1** — fast, structured, no explanation required.
> **Analogy:** Touch a hot pan → your hand jerks back **before** you consciously think "that is hot; I should let go." System 1 is the jerk; System 2 is the afterward narration. Software needs both: the reflex (Jev) and the narrator (LLM).
> **Why it matters:** The industry spent 2023–2026 routing *everything* through System 2 — a slow, expensive, deliberative engine — even for reflex-shaped questions like "is this a refund request?". System One Models exist so you stop paying System 2 prices for System 1 work.

### 2.1 The Split

Read the diagram left to right: Kahneman's two thinking modes on the left, their software stand-ins on the right.

```
HUMAN COGNITION                 SOFTWARE ANALOG
─────────────────               ─────────────────────────────
System 1  fast, intuitive  ──►  Jev: typed decisions + odds
          automatic, no         (Choice / Score / Noul)
          explanation

System 2  slow, deliberate ──►  LLM: text, code, explanations
          effortful,            (and occasionally hallucinations)
          narrative
```

> **One-line summary:** System 1 = fast reflex (Jev); System 2 = slow narration (LLM) — match the question to the mode.

### 2.2 Big Comparison: LLM vs Jev

How to read it: each row compares the two models on one dimension; the Jev column is what you gain. For instance, "Sampling" means how answers are produced — an LLM writes one word-piece at a time, Jev grades all questions at once.

| Dimension | Frontier LLM | Jev (System One Model) |
|-----------|--------------|------------------------|
| **Main job** | Generate text for people | Return typed decisions for software |
| **Post-training** | RLHF — optimized on *human preference* | **RLCD** — optimized on *outcomes*, calibrated probabilities |
| **Sampling** | Autoregressive token-by-token | Parallel evaluation of all questions in **one pass** |
| **Output** | Strings (you parse them) | `Choice` / `Score` / `Noul` + distribution + confidence |
| **Shape guarantee** | Schema is a *hope* (prompting, constrained decoding) | Closed answer space — **cannot leave the schema** |
| **Uncertainty** | "High confidence" as prose (unmeasured) | Real distribution; ~80% of 0.8s are right |
| **Latency** | 3–329s on decision-shaped tasks | **70–500ms** end-to-end |
| **Price** | Frontier token pricing (output billed) | **$0.042 / M input**, output free |
| **Best fit** | Writing, coding, explaining, open-ended reasoning | Classify, rate, gate, verify — narrow semantic judgment |

**Key row to memorize:** *Shape guarantee*. An LLM asked for JSON can give you `"urgency": "high!!"` at 2 a.m. — a string value outside your allowed list of values (your enum). Jev asked for a `Score` with levels 1–5 **must** return a score in that scale — because the answer space is closed by construction.

> **One-line summary:** The core difference: an LLM's output shape is a hope; Jev's shape is guaranteed by a closed answer space.

---

## 3. History & Naming

This section covers who built Jev, when it shipped, and why the names. The names encode the whole pitch, so they are worth remembering.

> **📌 Core Concept**
>
> **Definition:** The short story of TypeSafe and Jev — who built it, how they trained it, when it shipped, and why "Jev" and "System One" are the names. Facts, not mythology.
> **Analogy:** Like learning a tool's provenance (where a tool comes from): knowing a knife was forged for fishmongers tells you how to hold it. Knowing Jev was born from **RLHF veterans who wanted calibrated decisions** tells you exactly what it optimizes.
> **Why it matters:** The naming encodes the thesis — *efficiency gains drive wider use* (Jevons) and *fast thinking deserves its own model* (Kahneman). If you remember the names, you remember the pitch.

### 3.1 TypeSafe AI

How to read it: company facts in two columns; "Founders" names the people, "Funding" names the money behind the lab.

| Fact | Detail |
|------|--------|
| **Company** | TypeSafe AI — AI lab in **stealth ~2 years**, **founded 2024**, **San Francisco** |
| **Founders** | **Diogo Almeida** (CEO, ex-OpenAI — worked on RLHF, InstructGPT, ChatGPT, GPT-4), **Erik Gafni**, **Sasha Sheng** |
| **Team pedigree** | OpenAI, Google Brain, Meta/FAIR, Stripe, Airbnb, Plaid, Docker |
| **Funding** | **$40M seed led by DCVC**, announced at launch |

> **One-line summary:** TypeSafe = an OpenAI-heavy founding team, $40M seed, about two years in stealth.

### 3.2 Release Timeline

Read top to bottom: each arrow is one step in time, from founding to today's version.

```
2024          TypeSafe founded (stealth, San Francisco)
  │           team assembled from OpenAI / Google Brain / Meta FAIR /
  │           Stripe / Airbnb / Plaid / Docker
  │
  ▼
~2 years      stealth R&D → RLCD, synthetic-data training
in stealth
  │
  ▼
Sept 15/2026  Jev early access opens
  │
  ▼
Sept 20/2026  Jev open to ALL developers, NO waitlist
  │
  ▼
today         jev-1.13.0  (alias: jev-latest)
```

> **One-line summary:** Founded 2024, two years of quiet research, open to everyone since Sept 2026 — current version jev-1.13.0.

### 3.3 Why "Jev"? — Jevons Paradox

**William Stanley Jevons** was a 19th-century economist. The **Jevons paradox** (his observation): when something becomes more efficient, people use *more* of it, not less. Cheaper coal → more coal burned.

TypeSafe applies the same logic to intelligence: **cheaper machine intelligence → far wider deployment**. A decision model that is 40–200× faster and ~400× cheaper doesn't replace the expensive model — it *increases the total amount of intelligence in the system*, because decisions that weren't worth asking before are now free to ask.

> **One-line summary:** Cheaper decisions get asked more often — efficiency grows total usage, not less (the Jevons paradox).

### 3.4 Why "System One Model"?

Named after Daniel Kahneman's **Thinking, Fast and Slow**: System 1 = fast, intuitive; System 2 = slow, deliberate. LLMs were built as System 2 engines (chain-of-thought, deliberation, reflection). Jev is branded as the model for **System 1** — the questions you shouldn't need to think hard about, but software still has to answer thousands of times an hour.

> **One-line summary:** Named for fast thinking: thousands of small judgments per hour deserve their own model.

---

## 4. High-Level Architecture

This section shows the request/response pipeline end to end. It explains *why* adding questions is cheap and why output costs nothing.

> **📌 Core Concept**
>
> **Definition:** Jev's request/response pipeline — `state` + `questions` go in; a transformer trained on synthetic data via RLCD evaluates **every question in parallel in one pass**; typed answers with distributions and confidence come out. No autoregressive text loop (no writing one word-piece at a time, each waiting for the last).
> **Analogy:** Like a **bank teller with ten windows open at once** — an LLM tells you a story while slowly counting one bill at a time; Jev reads your slip and answers all ten windows simultaneously, because there is no "next token" to wait for.
> **Why it matters:** Parallel one-pass evaluation is *why* adding questions barely changes latency (see [02-primitives](../02-primitives/)) and why output is free — there is no token stream to bill.

```
┌────────────────────────────────────────────────────────────────────┐
│                     JEV REQUEST PIPELINE                           │
│                                                                    │
│  state: string | JSON object | array of text                      │
│  questions: { name: {type, options|levels|criteria, ...} }        │
│       │                                                            │
│       ▼                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  TRANSFORMER BACKBONE                                        │  │
│  │  trained exclusively on SYNTHETIC DATA                       │  │
│  │  post-trained with RLCD (Reinforcement Learning for         │  │
│  │  Calibrated Decisions) — outcomes, not human preference      │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 ▼                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ONE PASS · ALL QUESTIONS IN PARALLEL                        │  │
│  │  closed answer space per question (≤255 options / 2–10       │  │
│  │  levels / binary) — cannot escape the schema                 │  │
│  └──────────────────────────────┬───────────────────────────────┘  │
│                                 ▼                                  │
│  answers.<name>.choice | .score | .noul                           │
│  + probabilities (full distribution)                              │
│  + confidence (concentration for Choice/Score; |p−0.5|×2 for Noul)│
│                                                                    │
│  End-to-end: 70–500ms · $0.042 / M input tokens · output free    │
└────────────────────────────────────────────────────────────────────┘
```

Gloss: RLCD = Reinforcement Learning for Calibrated Decisions — training that rewards honest probabilities, not human approval. One pass = all questions answered at once, not one after another.

### 4.1 The Request Contract (Preview)

> 📄 **Example code:** [`examples/01-4-1-the-request-contract-preview.json`](examples/01-4-1-the-request-contract-preview.json)

Three questions, **one** HTTP call, **one** model pass. Details in [02-primitives](../02-primitives/) and [03-api](../03-api/).

> **One-line summary:** state + questions in → typed answers + probabilities + confidence out, all questions in one parallel pass.

---

## 5. Why Give Up Text Generation?

This section explains the central trade: Jev *cannot* write sentences, and that refusal is exactly what makes it reliable.

> **📌 Core Concept**
>
> **Definition:** The deliberate sacrifice at Jev's core — it *cannot* generate strings, and that refusal is the source of its superpowers: type-safe output (answers always fit your declared shape), one-pass parallelism, calibrated distributions, and zero parsing.
> **Analogy:** A **cargo ship that only carries containers**. A cruise ship (LLM) can carry anything — passengers, pets, a piano — but every item is hand-loaded and can fall overboard. Containers are boring and impenetrable; that's the point.
> **Why it matters:** Teams try to bolt schema onto LLMs after the fact (JSON mode, tool calling, retries). Jev *is* schema from training onward. "Giving up strings gives superpowers" is the trade you should be able to defend in a design review.

### 5.1 The Cost of Strings

Strings are maximally flexible — and that flexibility is the problem. Each row below is one price you pay when a model answers in free text.

| Cost of strings | What goes wrong |
|-----------------|-----------------|
| **Tokens** | Every explanation, hedge, and newline is billed (output is the expensive half) |
| **Latency** | Autoregression: one token at a time, 3–329s to reach a boolean |
| **Parse errors** | Trailing commas, single quotes, markdown fences, `"urgency": "high!!"` |
| **Hallucinated values** | An LLM can invent a 6th severity level that isn't in your enum |
| **Fake calibration** | "I'm highly confident" is a *string*, not a probability |

Gloss: autoregression = generating one token at a time, each waiting for the previous one — that's the latency bill.

> **One-line summary:** Free-text answers cost tokens, seconds, parse failures, invented values, and fake confidence.

### 5.2 Giving Up Strings Gives Superpowers

Read the diagram as a trade: surrender the left column, receive the right column.

```
SURRENDER ONE THING              GAIN FOUR THINGS
────────────────────             ─────────────────────────────────────
"No text generation"      ──►   Type-safe output (in-schema by construction)
                                Parallelism (all questions, one pass)
                                Calibration (RLCD: 0.8 ≈ 80% correct)
                                No parsing (typed fields arrive typed)
```

You trade the ability to write poetry for the ability to **act without guessing**. For the 99% of decisions where poetry was never the ask, that is the trade of the decade.

> **One-line summary:** Give up text generation, gain type safety, parallelism, calibration, and zero parsing.

---

## 6. When to Use / When NOT

This section is the routing table for the model choice itself — which engine deserves which question.

> **📌 Core Concept**
>
> **Definition:** The routing table for *model choice itself* — which engine deserves your question. Jev for narrow, closed-set, high-volume semantic judgment; LLM for open-ended language; plain code for anything deterministic (same input → same output, every time).
> **Analogy:** **Hammer, screwdriver, power drill.** Knowing Jev exists doesn't mean every problem is a Jev problem — a date diff is a screwdriver (code), a bug explanation is a drill (LLM), a "is this spam?" is a hammer (Jev).
> **Why it matters:** The expensive mistake is using a System 2 engine for System 1 work — and the subtle mistake is using Jev where determinism (code) or open language (LLM) was actually required. Limits live in [07-limits-and-evaluation](../07-limits-and-evaluation/).

### 6.1 The Big Table

How to read it: "Situation" is a task you might have; "Use" names the right engine; "Why" explains the match. For example, "is this spam?" → Jev; "write an email" → LLM; "add these dates" → code.

| Situation | Use | Why |
|-----------|-----|-----|
| Classify text into a fixed set of teams/categories | **Jev** (Choice) | Closed set, high volume, schema must hold |
| Rate severity / sentiment on an ordinal scale | **Jev** (Score) | Ordered levels, want distribution not adjectives |
| Yes/no gate, policy check, verification | **Jev** (Noul) | P(yes) with real calibration |
| Verify LLM output against a rubric | **Jev + LLM** | LLM writes, Jev verifies |
| Map-reduce over 100k rows ("which bucket?") | **Jev** | 70–500ms × cheap × parallel questions |
| Real-time user-facing decision (<500ms budget) | **Jev** | 70–500ms end-to-end |
| Write an email, explain a stack trace, draft code | **LLM** | Needs language |
| Open-ended reasoning with no closed answer set | **LLM** | Nothing to put in a distribution |
| Arithmetic, counting, date comparison | **Code** | Jev is explicitly not reliable here |
| Deterministic transform (parse, format, validate syntax) | **Code** | No judgment involved |

> **One-line summary:** Narrow judgment → Jev; open language → LLM; mechanical math → plain code.

### 6.2 Easy Way to Read It

Three lines, three rules of thumb:

```
Question has a FINITE answer set and repeats often?     → Jev
Question needs SENTENCES or open invention?             → LLM
Question is MECHANICAL (math, dates, parsing)?          → plain code
```

**The 4 target workloads** (where Jev was built to win):

```
1. Decision steps inside workflows     (triage, route, approve)
2. Map-reduce over large datasets      (classify 100k rows cheaply)
3. Real-time applications              (70–500ms budget)
4. Verification of LLM output          (Jev checks what the LLM wrote)
```

> **One-line summary:** Finite answer set plus frequent repetition = Jev's home turf.

### 6.3 State Hygiene — A Concept You'll Reuse

This section introduces a habit you will reuse in every later module: keep the state clean.

> *"Accuracy falls when the state carries unrelated detail."*

Jev judges **the state you send**. Dumping an entire log file because "more context is better" actively hurts: build a **small, relevant state** inside the latency budget. Think exhibit, not archive (state hygiene = send only the evidence the decision needs). This principle recurs across [02-primitives](../02-primitives/) and [06-jev-and-llm](../06-jev-and-llm/).

> **One-line summary:** Jev judges exactly what you send — small, relevant state in, accurate answers out.

---

## 7. Place in the Agent Ecosystem

This section locates Jev among its two neighbors: plain code and the LLM. It matters because misplacing Jev is how systems get slow or unsafe.

> **📌 Core Concept**
>
> **Definition:** Jev sits on a **capability continuum** between deterministic code and open language: code (mechanical, exact) → **Jev** (narrow semantic judgment, typed + calibrated) → LLM (language, open-ended). Jev is the **semantic decision layer** inside software — not a replacement for either neighbor.
> **Analogy:** A **traffic light** (Jev — instant, typed, everyone obeys) versus a **tour guide** (LLM — narrates and wanders) versus a **rail timetable** (code — exact, no judgment). A city needs all three; nobody asks the tour guide when the light turns red.
> **Why it matters:** Frameworks of this repository already have places to *put* decisions: the harness executes them, the loop repeats them, the graph grounds them. Jev is what fills the `decide()` slot inside those machines.

### 7.1 The Continuum

Read left to right: exact code, then Jev's typed judgment, then the LLM's open language.

```
DETERMINISTIC          SEMANTIC DECISION           LANGUAGE
CODE                   LAYER (Jev)                 LLM
─────────────          ─────────────────           ──────────────
if x > 0:              "which team?"  Choice       "explain this bug"
regex parse            "how urgent?"  Score        "write the migration"
date diff               "pass/fail?"   Noul        "draft the reply"

exact · free           typed · calibrated          fluent · flexible
no judgment            70–500ms · $0.042/M         slow-ish · expensive
zero ambiguity         closed answer space         occasional hallucination
```

> **One-line summary:** Jev is the middle layer: typed semantic judgment between exact code and open language.

### 7.2 Jev Inside This Framework's Modules

How to read it: each row names one module of this repository, what that module does, and where Jev's decisions plug in. Harness = the environment one agent runs in; Loop = the repeating schedule + verification cycle; Graph = the durable knowledge store.

| Module | Role | How Jev plugs in |
|--------|------|------------------|
| **Harness** (VII–XI) | Environment one agent runs in | Gate tool calls (`AutoModeMiddleware`), classify intent before routing |
| **Loop** (XII) | Schedule + state + verification | Triage each iteration, score readiness, verify each pass with Noul gates |
| **Graph** (XIII) | Durable knowledge substrate | Classify extracted entities/relations into a fixed ontology (Choice), edge confidence (Score) |

The division of labor sentence again, because it is the module's thesis:

```
Jev routes and verifies things → while the LLM provides the language.
```

**Easy way to read it:** The LLM is the **writer on staff**; Jev is the **reflex judge at the door**. The writer drafts; the judge admits, rates, and sends back. Software that confuses the two pays twice — once in tokens, once in latency — and still doesn't know whether its 0.8 means anything.

> **One-line summary:** Jev routes and verifies; the LLM provides the language.

---

*Back to [README](../README.md) — Module XIV overview*
