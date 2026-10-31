# ❓ FAQ — Evaluation (Real Stories, Plain Language)

This file answers real questions about **evaluation** — checking whether your AI agent actually works, using numbers instead of feelings. If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I changed the system prompt and it "feels" better — how do I prove it? [→ Overview of the Tools]

This question is about proving a change works. "Feels better" is an opinion; a measurement is a fact you can show your team.

**What you see**

You swap "you are a helpful assistant" for "you are a senior engineer". (The *system prompt* = the standing instruction you give the model before every request.) Replies look sharper. You tell the team it improved. Nobody can reproduce the claim.

**Why**

"Feels better" is not a measurement. The fix is to score the same questions before and after, on the same dataset (dataset = a fixed list of test questions with expected answers), with the same model.

**What to do**

1. Pick **PromptFoo** (a free, config-file-driven testing tool for LLM apps) if you want a comparison across prompts *and* providers in one run.
2. Write both prompts in one file so the tool scores them side by side.
3. Add a cost assertion (assertion = a pass/fail rule the tool checks automatically) so "better" cannot quietly mean "ten times more expensive".

> 📄 **Example code:** [`examples/01-q1-i-changed-the-system-prompt-and-it.yaml`](examples/01-q1-i-changed-the-system-prompt-and-it.yaml)

**Verify**

Run `promptfoo eval` (score all versions) then `promptfoo view` (open the results page). The comparison table gives one accuracy number per prompt, and any prompt above $0.05 fails its assertion.

> **One-line summary:** Replace "it feels better" with a side-by-side score on a fixed test set, and let an automatic cost rule stop silent overspending.

---

## Q2. Which tool fits — PromptFoo, Deepeval, RAGAS, LangSmith or Giskard? [→ Overview of the Tools]

This question is about picking one tool instead of installing five. They answer different questions, so the choice depends on what you need to check.

**What you see**

Five tools, five shapes. You cannot tell whether RAGAS works on a non-RAG agent, or why LangSmith needs a production trace, or what Giskard actually scans. (RAG = Retrieval-Augmented Generation — the agent first *retrieves* documents, then answers from them.)

**Why**

They answer different questions.

How to read it: each row is one tool; "Main purpose" says what the tool was built for; "Use it for" says when you should pick it. For instance, RAGAS only measures the retrieval step, so it is useless for an agent with no retrieval.

| Tool | Main purpose | Use it for |
|---|---|---|
| PromptFoo | whole-app eval from a YAML file | prompt and model A/B tests, runs locally |
| Deepeval | eval as unit tests, "LLM as judge" metrics | teams already living in pytest |
| RAGAS | retrieval quality (RAG) | faithfulness, answer relevancy, context precision |
| LangSmith | production LLM monitoring | eval on real traces, dataset curation |
| Giskard | open-source ML/LLM testing | bias detection, hallucination, robustness |

Glossary for the table: "LLM as judge" = a second model scores the answers of the first. "Faithfulness" = the answer only claims what the retrieved documents actually say. "Trace" = the recorded step-by-step log of one run.

**What to do**

1. Start with PromptFoo for anything you can express as a text file — fastest feedback.
2. Switch to Deepeval when you want eval to run as part of the test suite (test suite = the automated checks that run with your code, e.g. pytest).
3. Add RAGAS only when the agent retrieves documents. It measures the retrieval step, not the answer step.
4. Add LangSmith when the system runs in production and you want to eval on real traces, not synthetic (made-up) datasets.
5. Add Giskard when you need pre-deployment safety checks — bias, hallucination (the model stating false things with confidence), prompt injection robustness.

> 📄 **Example code:** [`examples/02-q2-which-tool-fits-promptfoo-deepeval-ragas-langsmith.py`](examples/02-q2-which-tool-fits-promptfoo-deepeval-ragas-langsmith.py)

**Verify**

A RAG run reports all three metrics separately. If you only care about the final answer, PromptFoo already covers it and RAGAS is extra cost. LangSmith's evals run on the trace timeline, so you see per-session metrics. Giskard produces a scan report with risk categories before you ship.

> **One-line summary:** Match the tool to the question: PromptFoo for quick comparisons, Deepeval for pytest teams, RAGAS for retrieval, LangSmith for live traffic, Giskard for safety scans.

---

## Q3. I added RAG with top-5 chunks — did accuracy improve or did I just burn tokens? [→ Real-World Case Studies]

This question is about telling a real improvement from a more expensive one. RAG costs extra tokens, so you need to check the extra chunks actually help.

**What you see**

Answers sound more grounded. Latency (response time) and token cost both went up. You have no idea if the extra chunks did anything. (Chunk = a slice of a document stored in the search index; top-5 = the 5 best-matching slices.)

**Why**

Retrieval quality and answer quality are separate numbers, and only one of them moved in your dashboard.

**What to do**

1. Score the same questions with retrieval off and on.
2. Read `faithfulness` — is the answer actually consistent with the retrieved context?
3. Read `context_precision` — are the five retrieved chunks the right five? If not, you are paying for noise.

**Verify**

Faithfulness rises versus the no-retrieval baseline (baseline = the score before the change, kept as reference), and context precision is high enough that dropping to top-3 does not hurt accuracy. If precision is low, fix chunking before you fetch more chunks.

> **One-line summary:** Measure retrieval quality separately from answer quality, or you may pay for extra chunks that add noise instead of accuracy.

---

## Q4. How big should the first test set be, and where does it live in CI? [→ Learning Roadmap (Directory Structure)]

This question is about getting started today. Many teams delay evaluation because they think they need thousands of test cases first.

**What you see**

You want to start evaluating today but the test suite needs data you do not have, so it never starts.

**Why**

The roadmap's answer is deliberately small: **20 to 50 cases** for the main task. A large set is not the goal; a repeatable score is.

**What to do**

1. Write 20 to 50 real user questions for the one task the harness does most.
2. Freeze them as the baseline — this file changes only on purpose.
3. Run the suite on every prompt change in CI (CI = continuous integration, the automated build-and-test pipeline that runs on every commit), and fail the build on a drop.

> 📄 **Example code:** [`examples/03-q4-how-big-should-the-first-test-set.sh`](examples/03-q4-how-big-should-the-first-test-set.sh)

**Verify**

CI fails when accuracy drops by more than 5% against the stored baseline. The baseline file is in version control (version control = git, which records every change), so a failed run can be bisected (bisect = walk back commit-by-commit to find the change that broke it) to the commit that caused it.

> **One-line summary:** Start with 20–50 frozen real questions wired into CI so every prompt change is scored automatically and regressions fail the build.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
