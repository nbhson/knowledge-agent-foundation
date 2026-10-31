# 🧪 Evaluation — Measuring Harness Quality

This page explains **evaluation**: scoring your AI agent's answers with numbers so you can prove a change is good — or catch one that is bad — before users see it.

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Evaluation Matters?](#why-evaluation-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of the Tools](#overview-of-the-tools)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section shows the problem evaluation solves: changes that *feel* right can still be wrong.

You change the system prompt (the standing instruction given to the model) from "you are a helpful assistant" to "you are a senior engineer". Is the result better — or worse? You feel the harness (your agent's code skeleton) is "better", but **where is the proof?** You add RAG (Retrieval-Augmented Generation: the agent first *retrieves* documents, then answers from them) with top-5 chunks (chunk = a slice of a document; top-5 = the 5 best matches) — does the answer really get more correct, or does it just use more tokens?

> *"If you ship prompt changes without evaluation, you're gambling — not engineering."*

**Evaluation (Eval)** turns a vague "feels better" into **clear numbers you can check**: it scores answers, compares prompt and model versions, and catches problems before they reach real users.

> **One-line summary:** Evaluation replaces gut feeling with repeatable scores on a fixed test set.

### Why Evaluation Matters?

This section gives four concrete reasons to evaluate.

How to read it: each row is one reason; "Explanation" says in plain words what it buys you. For instance, row 2 means a bad new prompt gets caught by the machine, not by an angry user.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Evidence instead of feeling** | Measure accuracy, faithfulness, and relevance with real numbers |
| 2 | **Regression detection** | Spot when a new prompt makes quality worse, before you ship it |
| 3 | **Comparable** | Compare models, prompts, and retrieval setups side by side |
| 4 | **The execution partner of harness/11** | Harness/11 explains *how* to evaluate — these tools give you the *equipment* to do it |

Glossary for the table: **accuracy** = share of answers that are correct; **faithfulness** = the answer only claims what the source documents say; **regression** = something that used to work now works worse.

> **One-line summary:** Evaluation gives you evidence, catches quality drops early, and makes versions comparable.

### Relationship to the Harness

This section shows where evaluation plugs into the rest of the framework. (The harness = the agent system, split into numbered components like harness/11.)

```
┌────────────────────────────────────────────────────────────┐
│  EVALUATION MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  harness/11-evaluation     → main component (metrics)      │
│  harness/05-prompt-builder → eval different prompts        │
│  harness/02-build-context  → eval retrieval quality (RAGAS)│
│  harness/07-workflow       → eval the end-to-end pipeline  │
└────────────────────────────────────────────────────────────┘
```

How to read the diagram: each line pairs one harness component with an evaluation use. For instance, harness/05 produces prompt variants, and evaluation is what tells you which variant to keep.

> **One-line summary:** Evaluation touches every harness stage — prompts, retrieval, and the full pipeline.

## Overview of the Tools

This section introduces the five evaluation tools covered here, so you can pick one instead of installing all five.

How to read it: "Main purpose" says what the tool was built for; "Standout features" says what makes it different. For instance, PromptFoo is the local, config-file option, while LangSmith is the hosted monitoring option.

| Tool | Main purpose | Standout features |
|------|--------------|-------------------|
| **PromptFoo** | Comprehensive LLM app eval | Config-driven, datasets + assertions, runs locally |
| **Deepeval** | Eval pipelines + unit tests | Pytest-style, LLM-as-judge metrics |
| **RAGAS** | RAG-specific evaluation | Measures faithfulness, relevancy, context precision |
| **LangSmith** | LLM production monitoring | Tracing + evals + datasets, LangChain/Anthropic/OpenAI integration |
| **Giskard** | Open-source ML/LLM testing | Detects bias, hallucination, robustness across models |

Glossary for the table: **config-driven** = you write a YAML file and the tool runs the tests from it; **assertion** = an automatic pass/fail rule (e.g. "cost must stay under $0.05"); **LLM-as-judge** = a second model scores the first model's answers; **hallucination** = the model states false things with confidence; **robustness** = the model stays correct when the input is odd or adversarial.

> **2025-2026 note:** Ragas is now officially **RAGAS** (v2+). LangSmith is the go-to for production monitoring with Anthropic or OpenAI SDK. Giskard is especially useful for open-source, vendor-neutral LLM quality testing.

> **One-line summary:** Pick one tool per need — PromptFoo for quick local comparisons, Deepeval for pytest, RAGAS for retrieval, LangSmith for live monitoring, Giskard for safety scans.

### PromptFoo — Config-Driven Eval

This section points to a working PromptFoo example: prompts and test cases written in one YAML file.

> 📄 **Example code:** [`examples/01-promptfoo-config-driven-eval.yaml`](examples/01-promptfoo-config-driven-eval.yaml)

> 📄 **Example code:** [`examples/02-promptfoo-config-driven-eval.sh`](examples/02-promptfoo-config-driven-eval.sh)

> **One-line summary:** PromptFoo scores prompt versions side by side from a single config file.

### Deepeval — Pytest-Style Eval

This section points to a Deepeval example: evaluation written as ordinary unit tests.

> 📄 **Example code:** [`examples/03-deepeval-pytest-style-eval.py`](examples/03-deepeval-pytest-style-eval.py)

> **One-line summary:** Deepeval makes each evaluation a test your existing test suite already knows how to run.

### Ragas — RAG-Specific Metrics

This section points to a RAGAS example: measuring the retrieval step of a RAG pipeline.

> 📄 **Example code:** [`examples/04-ragas-rag-specific-metrics.py`](examples/04-ragas-rag-specific-metrics.py)

> **One-line summary:** RAGAS tells you whether your retrieved documents — not just your final answer — are any good.

## Learning Roadmap (Directory Structure)

This section maps the folder so you know what to read in which order.

```
evaluation/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) LLM-as-judge, metric types, datasets
├── 02-setup/            ← (TODO) Installing PromptFoo / Deepeval / Ragas
├── 03-patterns/         ← (TODO) Evaling the harness in CI, regression testing
├── 04-savings/          ← (TODO) Eval cost, how often bugs are caught early
└── 05-troubleshooting/  ← (TODO) Judge bias, dataset drift, flaky evals
```

### Recommended Roadmap

This section gives the learning order in five steps, from concept to CI integration.

```
Step 1: Understand harness/11-evaluation — which metrics fit
   ↓
Step 2: Build a small test dataset (20-50 cases) for the main task (02-setup)
   ↓
Step 3: PromptFoo — compare old vs new prompt, model A vs B (03-patterns)
   ↓
Step 4: If using RAG → Ragas measures retrieval quality (03-patterns)
   ↓
Step 5: Integrate eval into CI — block regressions on every prompt change (03-patterns)
```

This table points you to related reading elsewhere in the repo. "If you want to..." names your goal; "Read" names the page for it.

| If you want to... | Read |
|-------------------|------|
| Understand the evaluation component | [harness/11-evaluation](../../harness/11-evaluation/) |
| Prompt engineering | [harness/05-prompt-builder](../../harness/05-prompt-builder/) |
| Context building | [harness/02-build-context](../../harness/02-build-context/) |
| Observability metrics | [tools/observability](../observability/) |
| RAG retrieval | [tools/vector-db](../vector-db/) |

> **One-line summary:** Learn the metrics first, build a small dataset, compare with PromptFoo, then wire evaluation into CI.

## Real-World Case Studies

This section shows evaluation doing its job on two everyday situations.

### 1. Regression Detection in CI

This example fails the build automatically when a prompt change lowers quality.

> 📄 **Example code:** [`examples/05-1-regression-detection-in-ci.yaml`](examples/05-1-regression-detection-in-ci.yaml)

### 2. Comparing Prompt Engineering Changes

This example compares three prompts on the same test set — one wins, one loses, and the numbers decide.

```
Baseline:  "You are a helpful assistant" → accuracy 82%
New:       "You are a senior engineer, write production-ready code" → accuracy 88% ✅
New2:      "You always answer with as much detail as possible" → accuracy 74% ❌ (verbose, off-topic)

→ Make the decision based on numbers, not on feeling.
```

> **One-line summary:** A side-by-side score catches both the winners and the losers before they ship.

## Reference Materials

This section lists the official pages and one research paper behind the tools above.

- **PromptFoo**: https://www.promptfoo.dev
- **Deepeval**: https://github.com/confident-ai/deepeval
- **RAGAS**: https://docs.ragas.io
- **LangSmith**: https://smith.langchain.com
- **Giskard**: https://www.giskard.ai
- **LLM-as-judge paper**: https://arxiv.org/abs/2306.05685

### Links to Other Branches

This section links to the related pages in this repo.

- [harness/11-evaluation](../../harness/11-evaluation/) — The evaluation component
- [harness/05-prompt-builder](../../harness/05-prompt-builder/) — Prompt variants to eval
- [tools/observability](../observability/) — Runtime metrics
- [tools/vector-db](../vector-db/) — RAG evaluation with Ragas
- [AI_AGENT_FRAMEWORK.md](../../AI_AGENT_FRAMEWORK.md) — The overall framework

---

> **"The goal of evaluation is not to prove your harness is good — it's to catch when it gets worse."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — evaluation*
