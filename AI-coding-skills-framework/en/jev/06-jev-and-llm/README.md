# 🤝 06. Jev + LLM — Division of Labor

> This section explains **how to combine Jev with LLMs without muddling their roles**: the two-brain model ("Jev decides, LLM writes"), model routing, tool-call gateways, the Pydantic AI FallbackModel pattern, and where Jev slots into harnesses, loops, and graphs — plus the **anti-patterns** that break hybrid systems. Read [README.md](../README.md) first for the overall context of Module XIV — Jev & System One Models.

---

## 1. The Two-Brain Model

> **📌 Core Concept**
>
> **Definition:** **"Jev decides, LLM writes."** Jev is a *semantic decision layer*: state in → bounded typed result out → code acts. The LLM is a *language engine*: prompts in → text out. Each system does the one thing it is actually good at.
> **Analogy:** Like a **newsroom**: the editor makes the calls (which story runs, which headline angle, kill or keep) and the reporter writes the prose. Asking the reporter to also be the editor — or the editor to type every caption — is how you get slow, expensive, inconsistent papers.
> **Why it matters:** LLMs are slow, expensive, and unreliable at *typed* judgment; Jev cannot generate text at all. Hybrid systems fail when the roles blur: prose tasks routed to Jev stall immediately, and gate decisions left to an LLM burn 2–10 s and tokens on a coin flip.

### 1.1 Role Table

| Concern | Owner | Why |
|---------|-------|-----|
| Classify / route / gate / verify (bounded schema) | **Jev** | 70–500 ms, calibrated probabilities, typed output |
| Draft / explain / summarize / converse | **LLM** | Only it can produce language |
| Execute the decision (call tool, write DB, send) | **Code** | Deterministic, auditable, free |
| Judge whether a side-effect tool is *safe* to run | **You / policy engine** | Jev only *classifies*; approval policy is not a prediction |

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

### 1.2 Ask Always vs Ask Only for Text

| | Jev | LLM |
|--|-----|-----|
| Cost | $0.042/1M input tokens, **free output** | tokens in *and* out |
| Latency | 70–500 ms; 40–200× faster; ~2 orders of magnitude more efficient | seconds per step |
| Policy | **Ask always** — decisions are cheap enough to check every time | **Ask only when text is required** |

> Because added questions barely change latency, the default posture is: *when in doubt, add a Jev question*. The expensive mistake is the opposite — routing a gate decision through an LLM because "it's smarter", and paying seconds + tokens for an uncalibrated verdict.

---

## 2. Model Routing

> **📌 Core Concept**
>
> **Definition:** Use Jev (a **Choice** question about task difficulty/type) to **pick which LLM** should handle the actual generation — cheap-fast vs capable — as middleware in front of the model call.
> **Analogy:** Like a **dispatcher at a taxi rank**: easy ride → nearest ordinary car; airport run with luggage → the big car. The dispatcher decides in a second; the driver does the driving.
> **Why it matters:** Most production traffic is easy. Paying frontier-model prices for "summarize this bullet list" is pure waste; a calibrated Jev router keeps the capable model for the cases that need it — and the probabilities (kept in agent state) tell you how sure the router was.

### The Routing Flow

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

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
MODELS = {
    "trivial":   "fast-model",     # cheapest, fastest
    "moderate":  "mid-model",
    "hard":      "capable-model",  # expensive — reserve for hard
}
ROUTING_THRESHOLD = 0.70


def route_model(task: str, agent_state: dict) -> tuple[str, dict]:
    """Middleware: Jev picks the LLM; probabilities stay in agent state."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {"task": task, "repo_context": agent_state.get("context", "")},
            "questions": {
                "difficulty": {
                    "type": "choice",
                    "options": ["trivial", "moderate", "hard"],
                }
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    d = r.json()["results"]["difficulty"]
    pick = d["selected"]

    # keep the full distribution in agent state — the audit signal later
    agent_state["model_route"] = {
        "selected": pick,
        "probabilities": d["probabilities"],
        "confidence": d["confidence"],
        "threshold": ROUTING_THRESHOLD,
    }

    # low confidence → don't gamble on the cheap model for a hard task
    if d["confidence"] < ROUTING_THRESHOLD:
        return MODELS["hard"], agent_state["model_route"]

    return MODELS.get(pick, "mid-model"), agent_state["model_route"]


# usage: model_id, route_info = route_model(task, agent_state)
#         response = call_llm(model_id, task)
```

</details>

---

## 3. Tool-Call Gateway

> **📌 Core Concept**
>
> **Definition:** Jev **gates before a tool executes**: a Noul (or Choice) question decides whether the call proceeds; calls **below threshold are blocked** and routed to approval. The gateway sits between the LLM's proposed tool call and the actual side effect.
> **Analogy:** Like an **airport access gate** between the terminal and the jetway — passengers can *request* boarding, but the gate controller is a separate system with its own list and threshold.
> **Why it matters:** The LLM proposes; something else must *permit*. A typed, logged, calibrated gateway is auditable in a way that "the model decided it was fine" never is.

### Gateway Flow

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

| Setting | Guidance |
|---------|----------|
| Threshold | High for destructive tools; tune from labelled examples |
| Below → | Block + tie into **auth/approval systems** (human gate, allowlist) |
| Scope | Gate *classification* ("authorized?") — policy of *what is allowed* lives in code/auth |
| Integrations | LangChain **AutoModeMiddleware** (gates risky tool calls); Pydantic AI `typesafe_tool_call_threshold` |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
DESTRUCTIVE = {"delete_files", "charge_account", "send_email"}
AUTHORIZE_THRESHOLD = 0.80


def tool_gateway(proposed_tool: str, args: dict, agent_state: dict) -> dict:
    """Jev gates side-effecting tool calls before execution."""
    if proposed_tool not in DESTRUCTIVE:
        return {"allow": True, "gate": "passthrough"}

    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {
                "user_request": agent_state.get("last_user_message", ""),
                "tool": proposed_tool,
                "target_summary": args.get("summary", str(args))[:500],
            },
            "questions": {"authorized": {"type": "noul"}},
        },
        timeout=5.0,
    )
    r.raise_for_status()
    p_yes = r.json()["results"]["authorized"]["probability"]

    allow = p_yes >= AUTHORIZE_THRESHOLD
    log_decision(proposed_tool, {"p_yes": p_yes,
                                 "threshold": AUTHORIZE_THRESHOLD,
                                 "model": "jev-latest"})
    if not allow:
        return {"allow": False, "gate": "blocked",
                "next": "request_approval"}   # tie into auth/approval system
    return {"allow": True, "gate": "authorized"}
```

</details>

---

## 4. Fallback Model (Pydantic AI)

> **📌 Core Concept**
>
> **Definition:** Pydantic AI's **TypeSafeModel** (Jev) + **FallbackModel** (LLM) combo: a structured `output_type` becomes Jev's `questions`; a **no-arg tool** is called on Jev's pick, while a **tool that needs arguments** raises `ToolCallProposed` (`ModelAPIError`) so the **FallbackModel (LLM) takes over the whole step**. The threshold knob is `typesafe_tool_call_threshold` (**default 0.6** — a starting point, not validated).
> **Analogy:** Like a **bouncer with a co-worker**: the bouncer handles every case he can judge from the guest list at the door (no-arg tools — he points, it happens); when the case needs an actual conversation with details (args), he steps aside and the co-worker works the whole interaction.
> **Why it matters:** This is the cleanest packaged expression of the division of labor: Jev answers what it can, in-schema, fast; anything requiring *language or argument synthesis* is delegated — not improvised by half a model.

### 4.1 How the Handoff Works

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

### 4.2 Mapping: Pydantic → Jev Questions

| Pydantic AI construct | Becomes |
|-----------------------|---------|
| `output_type` (model/fields) | Jev `questions` |
| field `description` | the question text |
| model docstring / instructions | framing for the pass |
| extra tool awareness | additional question: *"which of these does the text call for?"* |
| `typesafe_tool_call_threshold` | gate on the pick (default **0.6**) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Pydantic AI: TypeSafeModel (Jev) + FallbackModel (LLM)
# pip install pydantic-ai typesafe  (names illustrative)

from enum import Enum
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel
from pydantic_ai.models.fallback import FallbackModel


class Action(str, Enum):
    """Which workflow step should run next?"""
    REFETCH = Field(description="Re-fetch the missing data")
    RETRY = Field(description="Retry the failed operation")
    ESCALATE = Field(description="Escalate to a human")


# Jev path: output_type → questions; docstring → framing
jev_model = TypeSafeModel(
    'jev-latest',
    # default typesafe_tool_call_threshold=0.6 — retune from YOUR labels
)

# LLM path: handles steps Jev cannot (anything proposing arg-taking tools)
llm_model = FallbackModel('gpt-class-model', 'claude-class-model')

agent = Agent(FallbackModel(jev_model, llm_model))


@agent.tool_plain          # NO-ARG tool → called directly on Jev's pick
def escalate() -> str:
    return create_escalation_ticket()


@agent.tool                 # tool WITH args → ToolCallProposed (ModelAPIError)
def retry(operation_id: str, reason: str) -> str:
    return retry_operation(operation_id, reason)


# Flow in practice:
# 1. Jev evaluates questions in parallel; if the pick maps to a no-arg tool
#    above threshold → tool runs immediately (fast, typed, cheap).
# 2. If the step needs an arg-taking tool → ToolCallProposed ModelAPIError
#    → FallbackModel (LLM) takes over THE WHOLE STEP — it decides and writes args.
# 3. Never drop the fallback: Jev can be confidently wrong in-schema (see 04/07).
```

</details>

| Setting | Guidance |
|---------|----------|
| `typesafe_tool_call_threshold` | **0.6 default = starting point** (small internal support-ticket set), *not validated* — set from your labelled data |
| no-arg tools | Fast path — Jev's pick executes directly |
| arg tools | LLM fallback owns the entire step (not just the args) |
| Always | Keep the fallback even when thresholds look good |

---

## 5. Jev Inside a Harness

> **📌 Core Concept**
>
> **Definition:** A harness is the environment one agent runs in (tools, context, permissions). Jev slots into harness steps as **typed checkpoints**: after retrieval (which docs?), before tools (which tool? authorized?), and along the workflow (**fuzzy if-statements** — decisions too semantic for `if`/`else` on strings).
> **Analogy:** Like **checkpoints on a mountain trail** — the trail (harness) exists regardless; the checkpoints are where a ranger makes a fast typed call (open/closed, which route) before you continue.
> **Why it matters:** Harnesses are full of implicit decisions currently made by the LLM (slowly, uncalibrated) or by brittle string matching (fastly, badly). Jev gives those points a proper decision primitive without adding an LLM round-trip.

### Where Jev Slots In

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

### Cross-Links in This Framework

| Harness step | Where it lives | Jev's role there |
|--------------|----------------|------------------|
| Decide tools (MCP) | `harness/06-decide-tools-mcp` | Choice: which tool; Noul: gate |
| Workflow as fuzzy if-statements | `harness/07-workflow` | One typed question per branch |
| Retrieve/rank | harness retrieval steps | Score candidates, filter by floor |

> **Rule of thumb:** if a harness branch condition is about *meaning* ("is this error transient?"), it's a Jev question; if it's about *values* (`status == 500`), it's code.

---

## 6. Jev Inside Loops & Graphs

> **📌 Core Concept**
>
> **Definition:** Loops (Module XII) and graphs (Module XIII) supply **structure and context**; Jev supplies **fast typed decisions at specific steps** — triage at loop start, verification at loop end, node classification on graph context.
> **Analogy:** Like a **factory line with inspection gates**: the line's schedule and layout are the loop/graph; each gate is a Jev call — quick, typed, recorded — that decides continue/reject without stopping the plant for a lecture.
> **Why it matters:** Decision steps are exactly the "decision steps in workflows" workload. Inserting an LLM where a Jev question fits turns a 400 ms gate into a 4 s, token-burning, uncalibrated one — and slows the entire loop cadence.

### 6.1 Decision Steps in a Loop

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

- **Triage at the top:** Choice + Score per candidate item → only actionable work enters the loop ([05 — Routing](../05-patterns/)).
- **Verify at the bottom:** Noul against intent/policy → pass/fail feeds the verifier role.
- Cross-link: [loop/01-concepts](../../loop/01-concepts/) — execution loop, anatomy, autonomy levels.

### 6.2 Verified-Cascade Loop Pattern

```
 LLM drafts ──► JEV verifies ──► pass? ──► done
                  (Noul/Choice)    │
                                   └── no ──► fallback / re-draft ──► JEV again
                                       (bounded retries → escalate)
```

Each iteration is: **LLM writes → Jev decides → code branches**. The loop's attempt cap and escalation (from Loop Engineering) still apply — Jev is the verifier's *instrument*, not a replacement for the cap.

### 6.3 Graph as Context Provider

Graphs shine at **assembling the right state** for Jev: neighbors, paths, and community labels become a small relevant slice fed as `state`. Jev then makes the typed call (classify node, choose next hop among bounded options); the graph stores the result as new structure.

```
 GRAPH ──context slice──► STATE ──► JEV ──typed result──► GRAPH update
  (who/what is near)              (one pass)             (labels, edges)
```

Cross-link: [graph/01-foundations](../../graph/01-foundations/) — the context structures you assemble.

---

## 7. Anti-Patterns When Combining

> **📌 Core Concept**
>
> **Definition:** Anti-patterns are **recurring ways to wire Jev and an LLM together that look reasonable and fail in production**. Learn them by name before you design the first hybrid pipeline.
> **Analogy:** Like **mixing up the instruments in an orchestra** — each musician is excellent; assigning the flute the percussion part ruins the piece regardless of talent.
> **Why it matters:** Every item below has a cheap early symptom and an expensive late one. Catching them at design time costs a sentence; catching them after an incident costs a rollback.

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

> **The short version:** give Jev the *decision*, give the LLM the *language*, give code the *action* — and never let confidence stand in for evaluation.

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [05 — Production Patterns](../05-patterns/) · Next: [07 — Limits & Evaluation](../07-limits-and-evaluation/)*
