# ❓ FAQ — Jev + LLM: Division of Labor (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I asked Jev to write a reply to a customer and it came back with no text at all — is the API broken? [→ §1, §7]

**What you see**

You send state plus a question to `https://api.typesafe.ai/v1/systemone` and the answer contains only `selected`, `probabilities`, and `confidence`. No sentences, no draft, nothing to send. Meanwhile the same call cost $0.042 per 1M input tokens, returned in 70–500 ms, and output was free — which is exactly the pricing of a classifier, not a writer.

**Why**

Jev cannot generate language. It is a decision layer: state goes in, a bounded typed result comes out, and code acts on it. Only the LLM can turn instructions into prose. Think of a newsroom: the editor decides which story runs and kills or keeps it, the reporter writes the words. Ask the reporter to also be the editor — or the editor to type every caption — and the paper gets slow, expensive, and inconsistent.

**What to do**

Split the work before you call anything. Ask Jev *always* for classify / route / gate / verify, because those questions cost almost nothing in time. Ask the LLM only when text is required. Let ordinary code execute the decision — it is deterministic, free, and auditable.

```python
if task_needs_text(task):                 # "draft", "summarize", "explain"
    return call_llm(task)                 # only the LLM produces language
verdict = jev.ask(state, questions=q)     # typed, 70-500 ms
return code_acts(verdict)                 # code executes, never Jev
```

Use the rule of thumb from §5: if a branch condition is about *meaning* ("is this error transient?"), it is a Jev question; if it is about *values* (`status == 500`), it is code.

**Verify**

Grep your pipeline for task labels containing write, draft, summarize, or explain and confirm none of them hit Jev. Every path should end in one of three places: a typed result, generated text, or an executed action. A draft request that returns probabilities and no text is a routing bug, not an outage.

---

## Q2. I put my routing question inside the LLM prompt and now everything got slower and vaguer — what did I break? [→ §2, §7]

**What you see**

The prompt says *"Which of these three steps should run next: retry, refetch, escalate? Answer in JSON."* The model replies with a friendly paragraph that argues for retry. Each step now costs seconds and tokens, and there is nothing to store in agent state: no `selected`, no `probabilities`, no `confidence` — so you cannot audit which route was chosen or how sure the system was.

**Why**

State is the material; questions belong in Jev's `questions` field. A question placed in the prompt gets judged by the LLM instead of Jev, and the LLM has no calibrated probabilities to give you. That is anti-pattern #2 in §7: it looks identical in the editor and behaves completely differently at run time.

**What to do**

1. Send the situation as `state`, the question as `questions`, nothing else.
2. Keep the raw distribution — store `selected`, `probabilities`, `confidence`, and the threshold you used in agent state for the audit trail.
3. Use `choice` for a bounded set of options, `noul` (a yes/no question) for a gate, `score` for ranking candidates.
4. Trim `state` to what the decision needs. Piling everything in degrades accuracy and pushes personal data into logs (anti-pattern #8).

```python
payload = {
  "model": "jev-latest",
  "state": {"task": task, "repo_context": ctx},
  "questions": {"difficulty": {"type": "choice",
                "options": ["trivial", "moderate", "hard"]}},
}
```

**Verify**

The response body has three fields — `selected`, `probabilities`, `confidence` — and `agent_state["model_route"]` holds them after the call. If you get prose back, the question is still in the prompt. Time one decision: about 70–500 ms, not the 2–10 s you were paying.

---

## Q3. Jev answered with confidence 0.99 and the wrong branch ran automatically — can that really happen? [→ §7, §4]

**What you see**

A `choice` question returns `confidence ≈ 1.0`, the code trusts it, and the agent takes the wrong action with no human in the loop. Nothing logged as an error. The team had also copied the threshold straight from the docs — `typesafe_tool_call_threshold` at its default **0.6** — and never built a labelled evaluation set.

**Why**

Confidence is clarity, not correctness (§7, anti-pattern #3). A model can be confidently wrong *inside the schema*, and a high number on a question you never evaluated is a decoration. When thresholds come from defaults instead of your own labelled data, you have no idea of the real error rate (anti-pattern #4).

**What to do**

1. Keep the fallback even when the numbers look great. Pydantic AI's `TypeSafeModel` + `FallbackModel` is the packaged version of this: a no-argument tool runs on Jev's pick, and a tool that needs arguments raises `ToolCallProposed`, handing the **whole step** to the LLM.
2. Treat the 0.6 default as a starting point, not a validated number. Re-tune it from your own labelled support-ticket examples.
3. Build a small labelled evaluation set before production and measure the error rate of the branch you actually rely on.
4. Cap retries and escalate; Jev is the verifier's instrument, not a replacement for the loop's attempt cap (§6.2).

```python
jev_model = TypeSafeModel("jev-latest")       # threshold default 0.6 — retune it
llm_model = FallbackModel("gpt-class", "claude-class")
agent = Agent(FallbackModel(jev_model, llm_model))   # fallback always present
```

**Verify**

Deliberately feed the agent a case where the confident answer is wrong and confirm the fallback takes the step instead of the tool firing. Your evaluation report should show a measured error rate per question, not a threshold copied from documentation.

---

## Q4. The agent deleted files and charged an account without asking anyone — where do I put the approval check? [→ §3, §1.1]

**What you see**

The LLM proposes `call delete_files(args…)` and the tool runs. No prompt, no pause, no log entry explaining why. Later you find `send_email` and `charge_account` in the same category and start wondering how many other side effects went through the same path.

**Why**

The LLM proposes; something else must permit. Approval policy is not a prediction, so it does not belong to Jev as a classifier either — Jev only answers "authorized?", while the list of what is allowed lives in your authorization code. Without a gateway, "the model decided it was fine" is the only audit record you will ever have.

**What to do**

1. Put the gateway between the proposed tool call and the real side effect.
2. Only gate tools that change something. A small `DESTRUCTIVE` set — `delete_files`, `charge_account`, `send_email` — is enough to start; everything else passes through.
3. Ask a `noul` question and compare the probability to a threshold. The reference uses **0.80** for destructive tools — tune it from labelled examples, not from a default.
4. Below threshold → block and hand off to an approval system (human gate, allowlist).
5. Log `request_id`, `p_yes`, threshold, and model version. Never log the raw state.
6. Existing frameworks already have the hook: LangChain's `AutoModeMiddleware`, or Pydantic AI's `typesafe_tool_call_threshold`.

```python
p_yes = jev_noul(state, "does the user authorize this?")   # typed yes/no
if p_yes >= 0.80:
    execute(tool, args)
else:
    return {"allow": False, "next": "request_approval"}
```

**Verify**

Call `delete_files` yourself in a test and confirm it returns `{"allow": False, "gate": "blocked"}` and reaches the approval queue. Check that the audit log holds the four fields and no state. A run with an empty audit record is an unlogged side effect.

---

## Q5. We pay frontier-model prices to summarize five-bullet lists — can a 70 ms classifier really pick the model? [→ §2, §1.2]

**What you see**

Most production traffic is easy, yet every request goes to the most expensive model. The bill says so. Meanwhile a routing question costs 70–500 ms — 40–200× faster than the model it is choosing, about two orders of magnitude more efficient — and its output is free.

**Why**

Model routing treats difficulty as a `choice` question with three options: trivial, moderate, hard. It is a dispatcher at a taxi rank: an easy ride gets an ordinary car, an airport run with luggage gets the big car. The dispatcher decides in a second; the driver does the driving. Jev's cost is $0.042 per 1M input tokens with free output, so the default posture is *when in doubt, add a Jev question*.

**What to do**

1. Ask one `choice` question about difficulty: trivial → fast model, moderate → mid model, hard → capable model.
2. Run it as middleware in front of the model call, not as a separate step the user waits on.
3. If confidence is below **0.70**, do not gamble on the cheap model — escalate to the capable one.
4. Store the full distribution in agent state. The probabilities are the audit signal that tells you how sure the router was.

```python
pick, info = route_model(task, agent_state)   # Jev difficulty question
if info["confidence"] < 0.70:                  # unsure → do not gamble cheap
    return "capable-model", info
return MODELS[pick], info                      # trivial→fast, hard→capable
```

**Verify**

Look at the route distribution over a week of real traffic: most requests should land on the fast model, and hard ones should be a small share. Sample the hard-routed tasks and confirm they genuinely were hard. If nearly everything routes to the capable model, your difficulty question is not discriminating.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*