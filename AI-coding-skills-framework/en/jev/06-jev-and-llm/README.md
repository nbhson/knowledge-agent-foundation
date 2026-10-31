# 🤝 06. Jev + LLM — Division of Labor

> This section shows **how to pair Jev with LLMs without mixing up their jobs**: the two-brain idea ("Jev decides, LLM writes"), picking models, guarding tool calls, the Pydantic AI FallbackModel setup, and where Jev fits into harnesses, loops, and graphs — plus the **common traps** that break mixed setups. See [README.md](../README.md) for the big picture of Module XIV — Jev & System One Models.

---

## 1. The Two-Brain Model

> **📌 Core Concept**
>
> **Definition:** **"Jev decides, LLM writes."** Jev is a *semantic decision layer*: state in → bounded typed result out → code acts. The LLM is a *language engine*: prompts in → text out. Each system does the one thing it is actually good at. (Plain words: Jev = a fast judge that answers from a fixed menu of options; "typed" = the answer is a structured value like `billing` or `0.87`, never free text; LLM = the writer that turns words into words.)
> **Analogy:** Like a **newsroom**: the editor makes the calls (which story runs, which headline angle, kill or keep) and the reporter writes the prose. Asking the reporter to also be the editor — or the editor to type every caption — is how you get slow, expensive, inconsistent papers.
> **Why it matters:** LLMs are slow, expensive, and unreliable at *typed* judgment; Jev cannot generate text at all. Hybrid systems fail when the roles blur: prose tasks routed to Jev stall immediately, and gate decisions left to an LLM burn 2–10 s and tokens on a coin flip. (Gate decision = a yes/no safety check before an action runs, like "may this tool delete these files?")

This section explains the split of jobs — because mixing them up is the #1 cause of slow, costly hybrid systems.

### 1.1 Role Table

How to read it: each row is one kind of task; **Owner** names who should do it. For instance, "Classify / route / gate / verify" = small judgment questions (is this ticket billing? is this allowed?) — Jev answers those in 70–500 ms (ms = thousandths of a second). "Bounded schema" = a fixed answer menu defined in advance.

| Concern | Owner | Why |
|---------|-------|-----|
| Classify / route / gate / verify (bounded schema) | **Jev** | 70–500 ms, calibrated probabilities, typed output |
| Draft / explain / summarize / converse | **LLM** | Only it can produce language |
| Execute the decision (call tool, write DB, send) | **Code** | Deterministic, auditable, free |
| Judge whether a side-effect tool is *safe* to run | **You / policy engine** | Jev only *classifies*; approval policy is not a prediction |

(Glossary: *calibrated probabilities* = a confidence number that matches reality, e.g. 0.8 really means ~80% correct; *side-effect tool* = a tool that changes something outside the chat, like sending an email or deleting files.)

```
                    ┌───────────────────────────────────┐
   decision?        │          TWO BRAINS               │
  ──────────────►   │  JEV (System One)   LLM (System    │
   language?        │  fast · typed       Two-ish) slow  │
  ──────────────►   │  calibrated         fluent        │
                    │     │                   │          │
                    │     ▼                   ▼          │
                    │  CODE ACTS          TEXT RETURNS    │
                    └───────────────────────────────────┘
```

> **One-line summary:** Jev decides, the LLM writes, code executes, and humans own the approval policy.

### 1.2 Ask Always vs Ask Only for Text

How to read it: this table compares the two systems on cost, speed, and usage policy. "Ask always" = you can afford to query Jev on every single decision because it is cheap; "ask only for text" = call the LLM only when the output must be prose.

| | Jev | LLM |
|--|-----|-----|
| Cost | $0.042/1M input tokens, **free output** | tokens in *and* out |
| Latency | 70–500 ms; 40–200× faster; ~2 orders of magnitude more efficient | seconds per step |
| Policy | **Ask always** — decisions are cheap enough to check every time | **Ask only when text is required** |

("2 orders of magnitude" = about 100×; latency = the waiting time for one answer.)

> Because added questions barely change latency, the default posture is: *when in doubt, add a Jev question*. The expensive mistake is the opposite — routing a gate decision through an LLM because "it's smarter", and paying seconds + tokens for an uncalibrated verdict.

> **One-line summary:** Jev questions are cheap enough to ask every time; spend LLM tokens only when the output must be text.

> **One-line summary:** Let the fast, cheap judge (Jev) decide and the fluent writer (LLM) write — never swap their jobs.

---

## 2. Model Routing

> **📌 Core Concept**
>
> **Definition:** Use Jev (a **Choice** question about task difficulty/type) to **pick which LLM** should handle the actual generation — cheap-fast vs capable — as middleware in front of the model call. (Choice = Jev's multiple-choice question type, where the answer must be one option you defined; middleware = a small component that sits between two others and decides which one runs.)
> **Analogy:** Like a **dispatcher at a taxi rank**: easy ride → nearest ordinary car; airport run with luggage → the big car. The dispatcher decides in a second; the driver does the driving.
> **Why it matters:** Most production traffic is easy. Paying frontier-model prices for "summarize this bullet list" is pure waste; a calibrated Jev router keeps the capable model for the cases that need it — and the probabilities (kept in agent state) tell you how sure the router was. (Frontier model = the biggest, most expensive AI model; agent state = the small data bundle describing the current case.)

Signpost: this section answers "which of my models should handle this request?" — because sending every request to the biggest model is the most common way to burn money for nothing.

### The Routing Flow

How to read the diagram: each request first passes a Jev Choice question about difficulty; the answer picks one of three model tiers; the probabilities are stored for later auditing.

```
 user request ──► Jev Choice: difficulty = [trivial, moderate, hard]
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      trivial       moderate        hard
     cheap-fast     mid model     capable model
          │             │             │
          └─────────────┴──────┬──────┘
                               ▼
                    probabilities stored in
                      AGENT STATE (for audit)
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-the-routing-flow.py`](examples/01-the-routing-flow.py)

</details>

> **One-line summary:** One Jev Choice question sorts each request into three model tiers, with the probabilities saved for audit.

> **One-line summary:** Ask Jev one cheap "how hard is this?" question, then send easy work to the cheap model and only hard work to the expensive one.

---

## 3. Tool-Call Gateway

> **📌 Core Concept**
>
> **Definition:** Jev **gates before a tool executes**: a Noul (or Choice) question decides whether the call proceeds; calls **below threshold are blocked** and routed to approval. The gateway sits between the LLM's proposed tool call and the actual side effect. (Noul = Jev's yes/no/unknown question type; threshold = the cut-off confidence number, e.g. only proceed when confidence ≥ 0.9; side effect = a change to the real world, like deleting files or charging money.)
> **Analogy:** Like an **airport access gate** between the terminal and the jetway — passengers can *request* boarding, but the gate controller is a separate system with its own list and threshold.
> **Why it matters:** The LLM proposes; something else must *permit*. A typed, logged, calibrated gateway is auditable in a way that "the model decided it was fine" never is. (Auditable = you can later reconstruct exactly why the action was allowed.)

Signpost: this section covers the safety checkpoint between "the LLM wants to run a tool" and "the tool actually runs" — the single most important guard in a hybrid setup.

### Gateway Flow

How to read it: the LLM only *proposes* the call; the Jev gate compares its confidence against the threshold; above → run and log, below → block and ask a human.

```
 LLM: "call delete_files(args…)"          (proposal only)
              │
              ▼
 ┌────────────────────────────┐
 │  JEV GATE                  │   Noul: "does the user authorize
 │  P(yes) vs threshold       │   deleting these files?"
 └──────┬──────────────┬──────┘
   above │              │ below
         ▼              ▼
    EXECUTE tool    BLOCK → approval / human / ask user
         │                    │
         ▼                    ▼
    log outcome          log outcome
 (request_id, p, thr, model version — never the raw state)
```

How to read the settings table: each row is one knob of the gateway. "Threshold high for destructive tools" = a tool that deletes or charges must clear a stricter confidence bar than one that only reads.

| Setting | Guidance |
|---------|----------|
| Threshold | High for destructive tools; tune from labelled examples |
| Below → | Block + tie into **auth/approval systems** (human gate, allowlist) |
| Scope | Gate *classification* ("authorized?") — policy of *what is allowed* lives in code/auth |
| Integrations | LangChain **AutoModeMiddleware** (gates risky tool calls); Pydantic AI `typesafe_tool_call_threshold` |

(Glossary: *labelled examples* = past cases where a human wrote down the correct answer; *human gate* = a step where a person must click "approve"; *allowlist* = "whitelist" — a list of the only things that are permitted, e.g. the only folders a tool may touch.)

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-gateway-flow.py`](examples/02-gateway-flow.py)

</details>

> **One-line summary:** Proposals pass the Jev gate only above threshold; below it, the call is blocked and routed to approval.

> **One-line summary:** The LLM may *propose* a risky tool call, but a separate Jev gate — not the LLM — decides whether it runs, and low confidence always routes to a human.

---

## 4. Fallback Model (Pydantic AI)

> **📌 Core Concept**
>
> **Definition:** Pydantic AI's **TypeSafeModel** (Jev) + **FallbackModel** (LLM) combo: a structured `output_type` becomes Jev's `questions`; a **no-arg tool** is called on Jev's pick, while a **tool that needs arguments** raises `ToolCallProposed` (`ModelAPIError`) so the **FallbackModel (LLM) takes over the whole step**. The threshold knob is `typesafe_tool_call_threshold` (**default 0.6** — a starting point, not validated). (Pydantic AI = a Python framework for calling AI models; *no-arg tool* = a tool that needs no extra details, like `retry_last_build()`; *args* = the details/parameters a tool needs, e.g. *which* file to delete; fallback = the backup path that takes over when the first system can't handle it.)
> **Analogy:** Like a **bouncer with a co-worker**: the bouncer handles every case he can judge from the guest list at the door (no-arg tools — he points, it happens); when the case needs an actual conversation with details (args), he steps aside and the co-worker works the whole interaction.
> **Why it matters:** This is the cleanest packaged expression of the division of labor: Jev answers what it can, in-schema, fast; anything requiring *language or argument synthesis* is delegated — not improvised by half a model. (Argument synthesis = writing out the details a tool needs, from natural language.)

Signpost: this section shows the packaged, ready-made version of the split — use it instead of hand-wiring your own.

### 4.1 How the Handoff Works

How to read the diagram: left path = Jev picks a tool and it runs directly; right path = the tool needs written-out details, so Jev raises an error and the LLM (FallbackModel) takes over the entire step.

```
                    TypeSafeModel (Jev)
                    output_type → questions
                    field description → question text
                    docstring/instructions → framing
                           │
        ┌──────────────────┼──────────────────────┐
        ▼                                       ▼
  no-arg tool                            tool WITH args
  "Jev picks a tool"                     needs argument synthesis
        │                                       │
        ▼                                       ▼
  call tool on Jev's pick               ToolCallProposed
  (threshold: typesafe_tool_call_       (ModelAPIError)
   threshold, default 0.6)                     │
        │                                      ▼
        ▼                              FallbackModel (LLM)
  TOOL RUNS                                handles the WHOLE step
  (code acts)                              (LLM writes args / decides)
```

(Glossary: `output_type` = the Python class describing the expected answer; each *field description* becomes one Jev question; *framing* = the short context that tells Jev how to judge.)

> **One-line summary:** No-argument tools run on Jev's pick; tools needing arguments hand the whole step to the LLM fallback.

### 4.2 Mapping: Pydantic → Jev Questions

How to read it: left column = the Pydantic AI piece you already wrote; right column = what it turns into for Jev. For instance, `output_type` — the class listing your answer fields — becomes Jev's `questions` list.

| Pydantic AI construct | Becomes |
|-----------------------|---------|
| `output_type` (model/fields) | Jev `questions` |
| field `description` | the question text |
| model docstring / instructions | framing for the pass |
| extra tool awareness | additional question: *"which of these does the text call for?"* |
| `typesafe_tool_call_threshold` | gate on the pick (default **0.6**) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-4-2-mapping-pydantic-jev-questions.py`](examples/03-4-2-mapping-pydantic-jev-questions.py)

</details>

| Setting | Guidance |
|---------|----------|
| `typesafe_tool_call_threshold` | **0.6 default = starting point** (small internal support-ticket set), *not validated* — set from your labelled data |
| no-arg tools | Fast path — Jev's pick executes directly |
| arg tools | LLM fallback owns the entire step (not just the args) |
| Always | Keep the fallback even when thresholds look good |

How to read it: the first row is the main warning — 0.6 came from someone else's data, so treat it as a guess until you measure on your own.

> **One-line summary:** Each Pydantic field maps to a Jev question; the 0.6 threshold is a starting guess and the fallback always stays.

> **One-line summary:** Jev answers the simple in-schema cases directly; anything needing written-out arguments is handed wholesale to the LLM fallback — and 0.6 is a starting guess, not a validated number.

---

## 5. Jev Inside a Harness

> **📌 Core Concept**
>
> **Definition:** A harness is the environment one agent runs in (tools, context, permissions). Jev slots into harness steps as **typed checkpoints**: after retrieval (which docs?), before tools (which tool? authorized?), and along the workflow (**fuzzy if-statements** — decisions too semantic for `if`/`else` on strings). (Checkpoint = a fixed decision point; retrieval = fetching the relevant documents; fuzzy if-statement = a branch like "is this error transient?" that no plain string comparison can answer.)
> **Analogy:** Like **checkpoints on a mountain trail** — the trail (harness) exists regardless; the checkpoints are where a ranger makes a fast typed call (open/closed, which route) before you continue.
> **Why it matters:** Harnesses are full of implicit decisions currently made by the LLM (slowly, uncalibrated) or by brittle string matching (fastly, badly). Jev gives those points a proper decision primitive without adding an LLM round-trip.

Signpost: this section shows where, inside an existing agent setup, you slot in Jev questions.

### Where Jev Slots In

How to read it: left column = a normal harness step; right column = the typed question Jev answers at that step. "Score" = Jev's 0–1 rating question type.

```
 HARNESS STEP                          JEV'S JOB
 ─────────────────────────────────────────────────────────
 retrieve  ──► rank/filter chunks      Score / Choice (which docs?)
     │
 decide tools ──► pick tool + gate     Choice + Noul (which? authorized?)
     │
 workflow  ──► fuzzy if-statements     Choice / Score / Noul per branch
     │
 act       ──► code executes           (Jev does not execute)
```

> **One-line summary:** Each harness step gets one typed Jev question — ranking, tool choice, gate, semantic branch — while execution itself stays in code.

### Cross-Links in This Framework

How to read it: where each harness step is documented elsewhere in this repo, and what Jev does there. (MCP = Model Context Protocol, the standard way agents connect to tools.)

| Harness step | Where it lives | Jev's role there |
|--------------|----------------|------------------|
| Decide tools (MCP) | `harness/06-decide-tools-mcp` | Choice: which tool; Noul: gate |
| Workflow as fuzzy if-statements | `harness/07-workflow` | One typed question per branch |
| Retrieve/rank | harness retrieval steps | Score candidates, filter by floor |

> **Rule of thumb:** if a harness branch condition is about *meaning* ("is this error transient?"), it's a Jev question; if it's about *values* (`status == 500`), it's code.

> **One-line summary:** Meaning-based branch conditions become Jev questions; value comparisons stay as plain code.

> **One-line summary:** Inside a harness, put a fast typed Jev question at every decision point — ranking, tool choice, gate, semantic branch — and keep plain value checks in code.

---

## 6. Jev Inside Loops & Graphs

> **📌 Core Concept**
>
> **Definition:** Loops (Module XII) and graphs (Module XIII) supply **structure and context**; Jev supplies **fast typed decisions at specific steps** — triage at loop start, verification at loop end, node classification on graph context. (Triage = sorting incoming items by priority; node classification = labeling a point in a network, e.g. "this user is a bot".)
> **Analogy:** Like a **factory line with inspection gates**: the line's schedule and layout are the loop/graph; each gate is a Jev call — quick, typed, recorded — that decides continue/reject without stopping the plant for a lecture.
> **Why it matters:** Decision steps are exactly the "decision steps in workflows" workload. Inserting an LLM where a Jev question fits turns a 400 ms gate into a 4 s, token-burning, uncalibrated one — and slows the entire loop cadence. (Cadence = how often the loop runs and how fast it cycles.)

### 6.1 Decision Steps in a Loop

How to read it: the box is one pass of an execution loop; JEV marks the two decision steps — triage at the top, verify at the bottom — while the LLM only does the writing (Implementer).

```
 ┌─────────────────── EXECUTION LOOP (see loop/01-concepts) ──────────────────┐
 │                                                                             │
 │  Schedule ──► TRIAGE (Jev: which items? priority?)                         │
 │                    │                                                        │
 │                    ▼                                                        │
 │              State ──► Worktree ──► Implementer (LLM writes code)           │
 │                    │                                                        │
 │                    ▼                                                        │
 │              VERIFY (Jev: does the diff match intent? Noul)                 │
 │                    │                                                        │
 │              pass ─┴─► Commit / next item                                   │
 │              fail ────► retry (cap) / escalate                              │
 └─────────────────────────────────────────────────────────────────────────────┘
```

(Glossary: *worktree* = an isolated copy of the repo checkout where one agent works without touching others; *diff* = the set of changes made; *escalate* = hand the problem to a human.)

- **Triage at the top:** Choice + Score per candidate item → only actionable work enters the loop ([05 — Routing](../05-patterns/)).
- **Verify at the bottom:** Noul against intent/policy → pass/fail feeds the verifier role.
- Cross-link: [loop/01-concepts](../../loop/01-concepts/) — execution loop, anatomy, autonomy levels.

> **One-line summary:** Jev triages at loop start and verifies at loop end, while the LLM only writes code in between.

### 6.2 Verified-Cascade Loop Pattern

How to read it: a draft is written by the LLM, checked by Jev, and only passed drafts ship; failed ones go back for a bounded number of retries before a human sees them. ("Verified cascade" = draft → check → retry chain.)

```
 LLM drafts ──► JEV verifies ──► pass? ──► done
                  (Noul/Choice)    │
                                   └── no ──► fallback / re-draft ──► JEV again
                                       (bounded retries → escalate)
```

Each iteration is: **LLM writes → Jev decides → code branches**. The loop's attempt cap and escalation (from Loop Engineering) still apply — Jev is the verifier's *instrument*, not a replacement for the cap.

> **One-line summary:** Draft → Jev check → pass ships, fail retries with a cap, then escalates to a human.

### 6.3 Graph as Context Provider

Signpost: this explains what a knowledge graph contributes — not decisions, but the right context for Jev's decisions.

Graphs shine at **assembling the right state** for Jev: neighbors, paths, and community labels become a small relevant slice fed as `state`. Jev then makes the typed call (classify node, choose next hop among bounded options); the graph stores the result as new structure. (Neighbors = the items directly connected to the current one; next hop = the next step in a path.)

```
 GRAPH ──context slice──► STATE ──► JEV ──typed result──► GRAPH update
  (who/what is near)              (one pass)             (labels, edges)
```

Cross-link: [graph/01-foundations](../../graph/01-foundations/) — the context structures you assemble.

> **One-line summary:** Graphs assemble the right context slice; Jev turns it into a typed decision the graph stores back.

> **One-line summary:** Loops and graphs provide the schedule and the context; Jev drops in the fast typed decisions at triage, verification, and classification points.

---

## 7. Anti-Patterns When Combining

> **📌 Core Concept**
>
> **Definition:** Anti-patterns are **recurring ways to wire Jev and an LLM together that look reasonable and fail in production**. Learn them by name before you design the first hybrid pipeline. (Anti-pattern = a known mistake pattern — named so you can spot and avoid it.)
> **Analogy:** Like **mixing up the instruments in an orchestra** — each musician is excellent; assigning the flute the percussion part ruins the piece regardless of talent.
> **Why it matters:** Every item below has a cheap early symptom and an expensive late one. Catching them at design time costs a sentence; catching them after an incident costs a rollback. (Rollback = undoing a released change.)

How to read the table: column **#** is just an index; **Anti-pattern** = the mistake; **Symptom** = what you observe when it happens; **Fix** = what to do instead. For instance, #1 means: asking Jev to write text can never work — Jev returns only typed decisions, no sentences.

| # | Anti-pattern | Symptom | Fix |
|---|--------------|---------|-----|
| 1 | **Use Jev for tasks needing text** | Jev returns no text at all — generation is impossible | Route prose to the LLM; decisions to Jev ([07 Limits](../07-limits-and-evaluation/)) |
| 2 | **Write questions into the LLM prompt** | The LLM answers *your* question in prose, uncalibrated, inside the prompt | State is the material; send questions to Jev's `questions` field — *a question placed in the prompt gets judged by the LLM instead of Jev* |
| 3 | **Blind trust in high confidence** | Wrong in-schema answer auto-executed with confidence ≈ 1.0 | Confidence is clarity, not correctness ([04](../04-calibration/)) — keep a fallback |
| 4 | **Skip evaluation** | Thresholds copied from defaults; no idea of real error rate | Build a labelled eval before production ([07](../07-limits-and-evaluation/)) |
| 5 | **Let the LLM make gate decisions** | Seconds of latency + tokens + uncalibrated verdicts on every tool call | Noul gate via middleware ([§3](#3-tool-call-gateway)) |
| 6 | **Ask the LLM for probabilities it doesn't have** | Verbal confidence unrelated to error rates | Use Jev's distribution — it's calibrated on outcomes |
| 7 | **Drop the fallback** | One low-confidence edge case executes unreviewed | FallbackModel / human path always present ([§4](#4-fallback-model-pydantic-ai)) |
| 8 | **Jargle state into every call** | Accuracy degrades; PII leaks into logs | Small relevant state; never log state ([07 State Hygiene](../07-limits-and-evaluation/)) |

(Glossary: *in-schema* = within the defined answer menu; *eval* = a test set with known right answers; *verbal confidence* = "I'm quite sure", which no one can measure; *PII* = personally identifiable information, e.g. names or emails; *"jargle"* = cramming an oversized, messy state bundle into the call.)

> **The short version:** give Jev the *decision*, give the LLM the *language*, give code the *action* — and never let confidence stand in for evaluation.

> **One-line summary:** Keep the roles strictly separate — decisions to Jev, prose to the LLM, actions to code — and never drop the fallback or skip evaluation.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [05 — Production Patterns](../05-patterns/) · Next: [07 — Limits & Evaluation](../07-limits-and-evaluation/)*
