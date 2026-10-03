# ❓ FAQ — Evaluation for GraphRAG (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My GraphRAG gave a wrong answer — is the graph bad, the search bad, or the model bad? [→ §1 Graph Quality, §2 Retrieval, §3 Generation]

**What you see**

You demo it, the boss asks 3 questions. Budget → "500 million" ✅. Who approved → "Alice" ✅ but confidence 0.6. Team size → "15 people" ❌ (the document says 10). Now you have no idea what percentage of your answers are right, what percentage is invented, or where to even start.

**Why**

Because you are measuring one end-to-end score for three different systems. RAGAS's finding in the source: separating faithfulness (generation) from context relevance (retrieval) cuts debug time by 50%. One number cannot tell you which stage to open.

**What to do**

1. Always run the four stages in the same order: graph quality → retrieval → generation → KG completion.
2. Stop at the **first** stage that fails. If Invalid Edge Rate is not 0% or Isolated Nodes are above 5%, nothing downstream is worth measuring — bad data in, bad answer out.
3. Only when retrieval passes, look at generation. Hallucination Rate = 1 − Faithfulness.
4. Write all stages into one JSON record so two runs can be diffed.

```python
gq = 1 - isolated_rate - invalid_rate   # graph
rm = retrieval["MRR"]                    # retrieval
gm = generation["faithfulness"]          # generation
overall = mean([s for s in (gq, rm, gm) if s > 0])
```

**Verify**

Every run prints three labelled lines (Nodes/Edges/Connectivity/Isolated, then P@5 R@5 MRR, then Faithfulness/Hallucination) plus one `⭐ Overall Score`. Change nothing, fix one thing, and whichever line moves is the stage you touched. If two runs have the same overall score but Faithfulness differs by 0.4, you were reading the wrong line.

---

## Q2. How do I know if the graph itself is the problem? [→ §1 Graph Quality Metrics]

**What you see**

5,000 nodes imported from your documents, and queries still miss facts you personally know are in there. Or the phone-book problem: the graph holds both "Nguyen Van A" and "NV A", so one person becomes two nodes and a query about them returns half an answer.

**Why**

Coverage loss compounds, and bad structure makes some questions physically unanswerable. Miss 30% of the knowledge and you can only get about 70% of the answers right. A graph broken into separate fragments means multi-hop queries cannot reach the other fragment.

**What to do** — check these eight bars before touching the model:

| Check | Bar |
|---|---|
| Node Coverage / Edge Coverage | > 80% / > 70% |
| Duplicate Rate | < 5% |
| Connectivity (share of nodes in the largest component) | > 90% |
| Avg Degree | 3–10 for enterprise |
| Isolated Nodes | < 5% |
| Invalid Edge Rate | 0% |
| Temporal Freshness (edges not expired) | > 95% |

Density is `2|E| / |V|(|V|-1)` and is domain-dependent — do not set a target for it.

**Verify**

Run `evaluate_graph_quality` on the demo karate-club graph: 34 nodes, 78 edges, density 0.139, avg_degree 4.59, connectivity 1.0, isolated_rate 0.0. Then run `evaluate_coverage(["Alice","Bob","Phoenix","Alice Nguyen"], ["Alice","Bob","Phoenix","Atlas"])` — it returns precision 0.75, recall 0.75, `missed: ['atlas']`, `hallucinated: ['alice nguyen']`. That last entry is your duplicate, not a hallucination. Any real graph reporting connectivity 1.0 and zero isolates is suspect: nothing was ever deleted.

---

## Q3. My retrieval returns 5 documents and only 2 are right — which knob do I turn? [→ §2 Retrieval Evaluation]

**What you see**

```text
retrieved = ["doc_1","doc_3","doc_5","doc_7","doc_9"]
relevant  = ["doc_1","doc_5","doc_10"]
P@5 = 0.40   R@5 = 0.67   MRR = 1.00
```

MRR = 1.00 looks great and is misleading: the single hit `doc_1` sat at rank 1, so it flatters the score while two of the three relevant documents were never returned at all.

**Why**

Precision and Recall are two different failures. Precision = of the fish in the basket, how many are the ones you wanted. Recall = of the fish that exist, how many you caught. Raising `k` lifts recall and drags precision down — one knob cannot fix both.

**What to do**

1. Low recall → the right subgraph is not in the store. Raise `k`, loosen the fuzzy-match threshold (0.85 is the default), or add the missing hop.
2. Low precision → the filter is too loose, or duplicate entities are flooding it. Score-threshold the paths and dedup before retrieving.
3. Report MRR per query, not only the mean. Rank 1 scores 1.0 but rank 5 scores 0.2, so one lucky query hides a bad set.
4. For multi-hop answers use Path Precision. Two returned paths where one matches ground truth = 0.50.

**Verify**

Run `compare_retrieval` over 20 queries with ground-truth `relevant` lists. It returns vanilla vs graphrag P@5 / R@5 plus a `delta`. Ship only if the delta is positive on multi-hop queries; a negative delta is the signal to stop, not to re-tune the prompt.

---

## Q4. The model said the AI team has 15 people when the document says 10 — is that one bug or two? [→ §3 Generation Evaluation (RAG)]

**What you see**

Bad answer: *"Phoenix's budget is 700 million, approved by Tran Thi B. The AI team has 15 people."* Context: *"budget of 500 million, approved by Nguyen Van A. The AI team has 10 people."* Three false claims. Faithfulness scores 0.0, so the hallucination rate is 1.0 — and you still cannot say what to fix.

**Why**

In a GraphRAG there are two separate places to be wrong. **Graph hallucination**: a triplet was extracted wrongly through bad entity linking, so the model faithfully followed bad data. **Summary hallucination**: a community summary invented detail that is not in the graph at all. Averaging both into one faithfulness number hides which half is broken.

**What to do**

1. Split the answer into individual claims (small statements) and judge each one against the context — never judge the answer as one block.
2. Report Hallucination Rate = 1 − Faithfulness per query, and keep the list of unsupported claims as the bug report.
3. Verify citations against the graph itself by walking each cited path hop by hop.
4. If every claim *is* supported but the answer is still wrong, the graph is wrong. Go back to Q2.

```python
for path in cited_paths:                      # walk each citation
    if not all(graph.has_edge(path[i], path[i+1])
               for i in range(len(path) - 1)):
        valid += 1                            # citation_accuracy drops
```

**Verify**

`citation_accuracy` should be 1.0; below that, the model cites paths that never existed. Then run your 20 QA pairs twice — once with the real context, once with an empty one. With context, faithfulness should be >0.8; without it, the hallucination rate should spike sharply. If it does not spike, your judge is too generous and every number you have is inflated.

---

## Q5. My overall score says 0.9 — can I ship it? [→ §5 Benchmarks & Datasets, §4 KG Completion]

**What you see**

One beautiful number, computed from 20 questions you generated yourself with `create_custom_benchmark` — a function whose own docstring warns that human review is required afterwards. You have no idea whether 0.9 is good, or whether plain vector search beats your whole graph pipeline.

**Why**

Benchmarks from 2025–2026 report that GraphRAG wins on multi-hop and global questions but **loses to vanilla RAG on single-hop / factoid**. One blended score hides exactly that. A self-made benchmark cannot reveal it either, because the questions were generated from the same documents your pipeline already reads well.

**What to do** — match the benchmark to the task:

| Task | Benchmark | Metric |
|---|---|---|
| Multi-hop, 2 hops | HotpotQA | EM, F1 |
| Multi-hop, 2–4 hops | MuSiQue (harder) | EM, F1 |
| Domain KG question answering | GraphRAG-Bench (1018 questions, 5 types) | multi-hop + single-hop + explainability |
| KG hallucination | KGHaluBench | hallucination rate |
| Link prediction | FB15k-237 (310K triples), WN18RR (93K), OGB-WikiKG2 (17M) | Hits@10, MRR — never plain accuracy |

Report three separate tracks — single-hop, multi-hop, global — not one average. For link prediction the bars are Hits@10 > 0.5, MRR > 0.3, MR < 100, AUC > 0.8. A TransE model hitting `Hits@1: 0.15, Hits@10: 0.45, MRR: 0.28, MR: 85.3` is below the bar, and "accuracy" would have hidden that.

**Verify**

Two numbers must agree before you ship: the answer score (EM / F1) and **Evidence Recall** — the share of gold evidence that actually reached the model's context. High EM with low evidence recall means the model bluffed its way to the right answer; the next question will not be so lucky. And when you claim GraphRAG beats vanilla RAG, the LLM-as-judge comparison on comprehensiveness and diversity should reach p<0.01 first.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*