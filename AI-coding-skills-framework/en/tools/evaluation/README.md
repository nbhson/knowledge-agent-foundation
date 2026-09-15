# 🧪 Evaluation — Measuring Harness Quality

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

You change the system prompt from "you are a helpful assistant" to "you are a senior engineer". Quality goes up — or down? You say the harness is "better", but **where's the proof?** You add RAG with top-5 chunks — does it actually improve answer accuracy, or does it just burn more tokens?

> *"If you ship prompt changes without evaluation, you're gambling — not engineering."*

**Evaluation (Eval)** is the way to turn "feels better" into **measurable numbers**: score responses, compare across prompt/model versions, and catch regressions before they reach production.

### Why Evaluation Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Evidence instead of feeling** | Measure accuracy, faithfulness, relevance with numbers |
| 2 | **Regression detection** | Catch that a new prompt degraded quality before deploy |
| 3 | **Comparable** | A/B between models, prompts, retrieval strategies |
| 4 | **The execution partner of harness/11** | Harness/11 teaches *how* to evaluate — these tools provide the *tooling* for evaluation |

### Relationship to the Harness

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

## Overview of the Tools

| Tool | Main purpose | Standout features |
|------|--------------|-------------------|
| **PromptFoo** | Comprehensive LLM app eval | Config-driven, datasets + assertions, runs locally |
| **Deepeval** | Eval pipelines + unit tests | Pytest-style, LLM-as-judge metrics |
| **Ragas** | RAG-specific evaluation | Measures faithfulness, relevancy, context precision |

### PromptFoo — Config-Driven Eval

```yaml
# promptfooconfig.yaml
prompts:
  - "Summarize: {{input}}"
  - "Provide a concise summary: {{input}}"

providers:
  - openai:gpt-4
  - anthropic:claude-3-5-sonnet

tests:
  - vars:
      input: "Long technical document..."
    assert:
      - type: contains
        value: "key concept"
      - type: cost
        threshold: 0.05  # each prompt ≤ $0.05
```

```bash
promptfoo eval   # run the whole test suite
promptfoo view   # view the comparison table of providers + prompts
```

### Deepeval — Pytest-Style Eval

```python
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

def test_harness_answer():
    test_case = LLMTestCase(
        input="For whom is BHYT applicable?",
        actual_output=harness.run("For whom is BHYT applicable?"),
        retrieval_context=retrieved_chunks,
    )
    assert_test(test_case, [AnswerRelevancyMetric(), FaithfulnessMetric()])
```

### Ragas — RAG-Specific Metrics

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

dataset = load_your_qa_dataset()
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])

# faithfulness        → is the answer consistent with the context
# answer_relevancy    → is the answer relevant to the question
# context_precision   → are the retrieved chunks sufficient/correct
```

## Learning Roadmap (Directory Structure)

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

| If you want to... | Read |
|-------------------|------|
| Understand the evaluation component | [harness/11-evaluation](../../harness/11-evaluation/) |
| Prompt engineering | [harness/05-prompt-builder](../../harness/05-prompt-builder/) |
| Context building | [harness/02-build-context](../../harness/02-build-context/) |
| Observability metrics | [tools/observability](../observability/) |
| RAG retrieval | [tools/vector-db](../vector-db/) |

## Real-World Case Studies

### 1. Regression Detection in CI

```yaml
# .github/workflows/evals.yml
steps:
  - run: promptfoo eval --share   # run the eval suite
  - run: promptfoo regression-check  # compare against the baseline
  # fail CI if accuracy drops by more than 5%
```

### 2. Comparing Prompt Engineering Changes

```
Baseline:  "You are a helpful assistant" → accuracy 82%
New:       "You are a senior engineer, write production-ready code" → accuracy 88% ✅
New2:      "You always answer with as much detail as possible" → accuracy 74% ❌ (verbose, off-topic)

→ Make the decision based on numbers, not on feeling.
```

## Reference Materials

- **PromptFoo**: https://www.promptfoo.dev
- **Deepeval**: https://github.com/confident-ai/deepeval
- **Ragas**: https://docs.ragas.io
- **LLM-as-judge paper**: https://arxiv.org/abs/2306.05685

### Links to Other Branches

- [harness/11-evaluation](../../harness/11-evaluation/) — The evaluation component
- [harness/05-prompt-builder](../../harness/05-prompt-builder/) — Prompt variants to eval
- [tools/observability](../observability/) — Runtime metrics
- [tools/vector-db](../vector-db/) — RAG evaluation with Ragas
- [AI_AGENT_FRAMEWORK.md](../../AI_AGENT_FRAMEWORK.md) — The overall framework

---

> **"The goal of evaluation is not to prove your harness is good — it's to catch when it gets worse."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — evaluation*
