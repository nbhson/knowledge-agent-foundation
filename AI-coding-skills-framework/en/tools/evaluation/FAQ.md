# ❓ FAQ — Evaluation (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I changed the system prompt and it "feels" better — how do I prove it? [→ Overview of the Tools]

**What you see**

You swap "you are a helpful assistant" for "you are a senior engineer". Replies look sharper. You tell the team it improved. Nobody can reproduce the claim.

**Why**

"Feels better" is not a measurement. The fix is to score the same questions before and after, on the same dataset, with the same model.

**What to do**

1. Pick **PromptFoo** if you want a config-driven comparison across prompts *and* providers in one run.
2. Write both prompts in one file so the tool scores them side by side.
3. Add a cost assertion so "better" cannot quietly mean "ten times more expensive".

```yaml
prompts:
  - "You are a helpful assistant: {{input}}"
  - "You are a senior engineer: {{input}}"
providers:
  - openai:gpt-4
tests:
  - vars: { input: "Long technical document..." }
    assert: [ { type: cost, threshold: 0.05 } ]
```

**Verify**

Run `promptfoo eval` then `promptfoo view`. The comparison table gives one accuracy number per prompt, and any prompt above $0.05 fails its assertion.

---

## Q2. Which tool fits — PromptFoo, Deepeval or Ragas? [→ Overview of the Tools]

**What you see**

Three tools, three shapes. You cannot tell whether Ragas works on a non-RAG agent, or why Deepeval looks like a test framework.

**Why**

They answer different questions.

| Tool | Main purpose | Use it for |
|---|---|---|
| PromptFoo | whole-app eval from a YAML file | prompt and model A/B tests, runs locally |
| Deepeval | eval as unit tests, "LLM as judge" metrics | teams already living in pytest |
| Ragas | retrieval quality (RAG) | faithfulness, answer relevancy, context precision |

**What to do**

1. Start with PromptFoo for anything you can express as a text file — fastest feedback.
2. Switch to Deepeval when you want eval to run as part of the test suite.
3. Add Ragas only when the agent retrieves documents. It measures the retrieval step, not the answer step.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])
```

**Verify**

A RAG run reports all three metrics separately. If you only care about the final answer, PromptFoo already covers it and Ragas is extra cost.

---

## Q3. I added RAG with top-5 chunks — did accuracy improve or did I just burn tokens? [→ Real-World Case Studies]

**What you see**

Answers sound more grounded. Latency and token cost both went up. You have no idea if the extra chunks did anything.

**Why**

Retrieval quality and answer quality are separate numbers, and only one of them moved in your dashboard.

**What to do**

1. Score the same questions with retrieval off and on.
2. Read `faithfulness` — is the answer actually consistent with the retrieved context?
3. Read `context_precision` — are the five retrieved chunks the right five? If not, you are paying for noise.

**Verify**

Faithfulness rises versus the no-retrieval baseline, and context precision is high enough that dropping to top-3 does not hurt accuracy. If precision is low, fix chunking before you fetch more chunks.

---

## Q4. How big should the first test set be, and where does it live in CI? [→ Learning Roadmap (Directory Structure)]

**What you see**

You want to start evaluating today but the test suite needs data you do not have, so it never starts.

**Why**

The roadmap's answer is deliberately small: **20 to 50 cases** for the main task. A large set is not the goal; a repeatable score is.

**What to do**

1. Write 20 to 50 real user questions for the one task the harness does most.
2. Freeze them as the baseline — this file changes only on purpose.
3. Run the suite on every prompt change in CI, and fail the build on a drop.

```bash
promptfoo eval --share        # run the suite
promptfoo regression-check    # compare against the baseline
```

**Verify**

CI fails when accuracy drops by more than 5% against the stored baseline. The baseline file is in version control, so a failed run can be bisected to the commit that caused it.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*