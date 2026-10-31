# ❓ FAQ — Graph Reasoning (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets). Each answer has four parts: **What you see** (the symptom), **Why** (the cause), **What to do** (the fix), and **Verify** (how to confirm the fix worked).

---

## Q1. The traversal returns the wrong team — Dave disappeared and nobody knows why [→ §1 Traversal Strategies]

**What you see**

You run one traversal and print the results:

```
['Alice', 'Bob']                            (hops=1, conf=0.95)
['Alice', 'Bob', 'Carol']                   (hops=2, conf=0.90)
['Alice', 'Bob', 'Phoenix']                 (hops=2, conf=0.85)
```

Dave is gone. He is a direct colleague of Alice, connected by `Alice —[KNOWS, conf=0.60]→ Dave`. Nothing crashed, no error, no log line — the answer is just quietly incomplete, and a chatbot built on top of it says "Alice has nobody else on her team" with total confidence.

**Why**

Two silent filters did it. `allowed_edge_types={"MANAGES", "WORKS_ON"}` drops `KNOWS` because a "team" is built from authority edges, not acquaintance edges — correct by design. `min_confidence=0.7` then drops Dave anyway, because his only edge sits at **0.60** (confidence = a 0-to-1 score for "how sure the extraction was that this edge is real"). Extraction pipelines routinely emit low-confidence edges for the messy cases (same name, two people, inferred from an email signature), so a confidence floor is healthy — but it is a **floor nobody declared**, so the graph silently answers a different question than you asked.

**What to do**

1. Decide what "team" means *before* you traverse, then encode it in the edge types. Authority chain (`MANAGES`, `REPORTS_TO`) and collaboration (`WORKS_ON`, `KNOWS`) are different questions.
2. Set `min_confidence` deliberately and write the number in the answer: "traversing MANAGES/WORKS_ON at confidence ≥ 0.7".
3. Log what the filters removed. One line is enough — `filtered: 1 edge (type=KNOWS, conf=0.60) Dave`.
4. When the filtered node matters, lower the floor for that one query instead of globally.
5. If the target is a property (`domain="AI"`) rather than the node name, filter on the property — never on `"AI" in target`, which matches any project whose name contains the letters.

> 📄 **Example code:** [`examples/01-q1-the-traversal-returns-the-wrong-team-dave.py`](examples/01-q1-the-traversal-returns-the-wrong-team-dave.py)

**Verify**

Run the same traversal with `min_confidence=0.0` and diff the two node lists. Any node that disappears must appear in the answer as an explicit exclusion. Lab 1 does this properly: compare unconstrained BFS against constrained BFS on a 1K-node / 5K-edge graph and check both *nodes visited* and *time*.

> **One-line summary:** Filters silently remove nodes — decide edge types and the confidence floor deliberately, then log everything the filters drop.

---

## Q2. The same traversal worked on 20 demo nodes and now it hangs on the real graph — why? [→ §1.2 Sampling for Large Graphs]

**What you see**

Your demo graph has 6 nodes. Your production graph has over **1 million nodes**. A 3-hop BFS from one person expands into hundreds of thousands of intermediate nodes, and the request either times out or returns more rows than you can put in a prompt. Someone suggests "just increase `max_hops` to 5" — which is exactly backwards.

**Why**

BFS cost grows with *breadth*, not depth. (BFS = Breadth-First Search — visiting neighbors level by level, like ripples spreading on water.) A person with 40 direct contacts, each of whom has 40, is already 1,600 nodes at 2 hops and **64,000 at 3 hops**. You cannot prompt your way out of this: the failure is fan-out (each node multiplying the number of nodes to visit), and more hops make it exponentially worse. The demo hid the problem because a 6-node graph has no fan-out.

**What to do**

1. Cap the frontier, not the depth: `max_neighbors_per_hop=10` keeps each expansion bounded regardless of graph size.
2. Choose the sampling strategy deliberately. `random` is unbiased but may drop the very person you need; `top-confidence` keeps the 10 best-supported edges; `pagerank` keeps the 10 most important.
3. Start at `max_hops=2` and add a hop only when a real question needs it. Most "who is related to X" questions die at 2 hops.
4. Put the cap in the query, not in your head — return the count of *visited* nodes alongside the count of *returned* nodes.
5. If a question genuinely needs the whole neighbourhood (community detection, centrality), that is a different tool — see Q5's neighbours and §4.

> 📄 **Example code:** [`examples/02-q2-the-same-traversal-worked-on-20-demo.py`](examples/02-q2-the-same-traversal-worked-on-20-demo.py)

**Verify**

Log `max_neighbors_per_hop`, `visited_count` and `returned_count` on every call. If `visited_count` grows by more than ~10× when you go from 1 hop to 2, the node you're starting from is a hub (a node with very many connections) — treat that as a finding, and sample around it.

> **One-line summary:** Cap the number of neighbors expanded per hop, not the depth — fan-out, not hop count, is what makes big traversals explode.

---

## Q3. The model gives one confident path and it's the wrong path — should I return shortest path or all paths? [→ §2 Path Finding]

**What you see**

Question: *"How is Bob connected to Project Atlas?"* You return `nx.shortest_path(...)` and it gives `Alice → Bob → Carol → Atlas`. The model writes a clean paragraph: "Bob reaches Atlas through Carol." But the graph also contains `Alice → Bob → Phoenix → Atlas` and `Alice → Dave → Carol → Atlas`. Your answer is defensible, unverifiable, and hides the fact that several routes existed.

**Why**

Each path-finding kind answers a different question: **shortest path** = fewest steps, **all paths** = what exists (up to N hops), **K-shortest** = the top-K alternatives, **weighted shortest** (Dijkstra, a classic algorithm whose weight = 1/confidence here, so weak edges cost more) = most trustworthy, **constrained** = only through specific edge types. Handing the model a single path removes its ability to reason; it can only narrate what you already chose. Multi-hop reasoning on a graph is reported to lift accuracy by **27%** over single-hop retrieval on HotpotQA (a public benchmark of questions that need chaining two facts) — but only if the alternatives are actually in front of the model.

**What to do**

1. If you don't know how far the graph stretches, start with shortest path.
2. If you want the model to *weigh* options, return all paths up to a cutoff and put them all in the prompt: `nx.all_simple_paths(G, "Bob", "Atlas", cutoff=4)`.
3. If a specific route must be defensible, use weights = `1/confidence` and Dijkstra, so a shaky `KNOWS` edge costs more than a strong `MANAGES` edge.
4. Always attach the evidence — for each hop, the edge type and its confidence. Evidence is what turns a path into a proof.
5. In Cypher, bound it in the query itself: `[:MANAGES|WORKS_ON*1..4]` plus `WHERE all(r in relationships(path) WHERE r.confidence > 0.7)`, then `ORDER BY length(path) LIMIT 5`.

> 📄 **Example code:** [`examples/03-q3-the-model-gives-one-confident-path-and.py`](examples/03-q3-the-model-gives-one-confident-path-and.py)

**Verify**

Ask the question twice — once with the shortest path only, once with all paths — and check whether the answer changes. If it does, the single path was hiding a real ambiguity and your original answer was luck, not reasoning.

> **One-line summary:** Return several paths with their evidence instead of one shortest path — a single path forces the model to narrate your choice rather than reason.

---

## Q4. The system says "Alice manages Carol" but no such edge exists — is that a hallucination? [→ §3 Inference Rules & Reasoning]

**What you see**

The graph has `Alice —MANAGES→ Bob —MANAGES→ Carol`. Nothing connects Alice to Carol. Then the answer comes back: *"Alice has authority over Carol."* You grep the graph for an `INDIRECTLY_MANAGES` edge and find nothing. It looks exactly like a model hallucinating.

**Why**

It is not a hallucination — it's **inference**, and the edge was never written to the graph. `apply_rules` scans for the pattern `A -MANAGES-> B -MANAGES-> C` and derives `A -INDIRECTLY_MANAGES-> C` at confidence **0.80**, carrying its evidence (`Alice -[MANAGES]→ Bob + Bob -[MANAGES]→ Carol`). Real graphs are sparse; storing every derived relation by hand is impossible, so the rule engine keeps them in memory. The danger is that inferred facts and real facts look identical downstream unless you tag them.

**What to do**

1. Tag every inferred edge with the rule name that produced it (`"rule": "transitive_manages"`) and its own confidence — an inference is always less certain than the fact it came from.
2. Propagate confidence along the chain. The README's example: `0.95 × 0.90 = 0.855` with the `product` method; `min` returns `0.90`. Pick one and state which.
3. Keep the evidence strings. Two lines — `Alice -[MANAGES]→ Bob` and `Bob -[MANAGES]→ Carol` — are the difference between a claim and a proof.
4. Filter inferred results out of answers when the user needs ground truth, and say so: "derived by rule `transitive_manages`, not stored in the KG".
5. Watch for false positives from composition rules like `works_on_implies_team` (`MANAGES + WORKS_ON → OVERSEES`, confidence **0.75**) — a manager who once touched a project is not necessarily still overseeing it.

> 📄 **Example code:** [`examples/04-q4-the-system-says-alice-manages-carol-but.py`](examples/04-q4-the-system-says-alice-manages-carol-but.py)

**Verify**

Lab 2: define 5 rules, run `apply_rules` on a 50-node graph, then hand-check every inferred edge for logical correctness and count false positives. A rule with a non-zero false-positive rate is not finished, regardless of how many edges it produced.

> **One-line summary:** It is inference, not hallucination — tag derived edges with rule name, confidence, and evidence so downstream users can tell derived facts from stored ones.

---

## Q5. The answer is right about the person but wrong about the time — "who ran the AI team in Q2?" [→ §5 Temporal Reasoning]

**What you see**

The question is *"Who managed the AI team in Q2/2024?"* The answer confidently names Alice. Alice managed **TeamA until 2024-06-30**, then **TeamB from 2024-07-01**. Querying at `date(2024, 8, 1)` correctly returns TeamB; querying at `date(2024, 3, 1)` correctly returns TeamA. The bug is that the production query **has no date in it at all** — it traverses every `MANAGES` edge ever created and returns both teams.

**Why**

Temporal knowledge graphs report a **35% cut in stale answers** — answers built on facts whose validity period already expired — once queries are time-aware. The fix is structural, not prompt-level: every edge carries `valid_from` and `valid_until` (`None` = still current), and a query is only valid inside that window. `update_temporal_edge` never deletes the old edge; it stamps `valid_until` on the current one and appends the new one, so history stays auditable.

**What to do**

1. Add `valid_from` / `valid_until` to every edge that can change. If a relation can expire, model the expiry.
2. Make the query date mandatory. Treat a missing date as a bug, not a default — "current" is a date, `date.today()`.
3. In Cypher, push the window into the pattern: `WHERE r.valid_from <= date('2024-03-01') <= r.valid_until`.
4. Close the old edge on write (`valid_until = new_valid_from`), never delete it. Deleting history makes "who was accountable then?" unanswerable forever.
5. When a question mixes a person and a period ("who ran X in Q2"), filter by both — edge window *and* node property (`domain="AI"`).

> 📄 **Example code:** [`examples/05-q5-the-answer-is-right-about-the-person.py`](examples/05-q5-the-answer-is-right-about-the-person.py)

**Verify**

Lab 3: build a 20-edge temporal graph and ask *"Who managed team X on 2023-06-01 vs 2024-06-01?"* — the two answers must differ. If they match, your `update_temporal_edge` is not expiring the old edge, and every historical query you serve is quietly wrong.

> **One-line summary:** Every changeable edge needs `valid_from`/`valid_until` and every query needs a date — close old edges on write, never delete them.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*