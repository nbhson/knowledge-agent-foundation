# ❓ FAQ — Knowledge Graph Construction (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The LLM misses most entities in long documents — how do I actually get them all? [→ §2 Entity Extraction]

**What you see**

You extract a 20-page vendor contract in one shot and get back 12 entities. The customer company named on page 14 is not among them, and the clause naming the signing date is missing. You re-read the text — it is clearly there. Worse, the same document gives you 12 entities on Monday and 15 on Tuesday, so you cannot tell whether coverage improved or the model just felt different that day.

**Why**

One LLM call over a long text behaves like a tired reader: it keeps the first pages sharp and drifts by the end. Extraction quality sets most of the GraphRAG ceiling — the Microsoft GraphRAG paper (2024) puts it at ~80% of final answer quality, so a missed entity (entity = a real-world thing named in text: person, company, date, contract) is a question you will never be able to answer later.

How to read this table: each row is one extraction method. **Precision** = of what it finds, how much is correct; **Recall** = of what exists, how much it finds. High precision + low recall = careful but incomplete.

| Method | Precision | Recall | Best for |
|---|---|---|---|
| Rule-based (regex) | high | low | contract codes like `C-2024`, dates |
| NER (spaCy/BERT) | high-ish | medium | Person / Org / Location |
| LLM single call | medium | high | any entity type, context-aware |
| LLM + gleaning | high | high | GraphRAG full coverage |

**What to do**

1. Split the document first — `chunk_size=1000` (each piece ≈ 1000 characters), `overlap=100` (neighbouring pieces share 100 characters so nothing falls on a boundary), and extract per chunk instead of over the whole file.
2. Run multiple **gleaning** rounds (gleaning = re-asking "anything you missed?", like re-reading a page for highlights). Each round re-sends the text plus the names already found, and asks "anything left?" Microsoft measured **+25% entity coverage** over a single pass.
3. Cap it at `max_gleanings=2` and stop early the moment a round adds zero new entities — that is your signal that nothing is left.
4. Force `"format": "json"` and handle a parse failure as "no new entities" rather than crashing.
5. Add regex for the fixed shapes an LLM always misses (contract codes, invoice numbers).

> 📄 **Example code:** [`examples/01-q1-the-llm-misses-most-entities-in-long.py`](examples/01-q1-the-llm-misses-most-entities-in-long.py)

**Verify**

Run the same 5 documents twice: `max_gleanings=0` vs `max_gleanings=2`, and diff the entity name lists. Then hand-check the diff — every added name should be real, and the run should print `+0 entities` on the last round. That zero is your coverage receipt.

> **One-line summary:** Chunk the document, run 2 gleaning rounds ("anything left?"), add regex for fixed codes — that combination recovers the entities a single LLM pass drops.

---

## Q2. I have three separate "Alice" nodes and every query returns half an answer [→ §4 Entity Resolution & Deduplication]

**What you see**

The graph contains `Nguyen Van A` (from doc 1), `Alice Nguyen` (doc 2), `A. Nguyen` (doc 3) — all typed `Person`. Ask "who does Tran Thi B manage?" and you get one name, because the other two Alices are on disconnected islands. Then a second symptom: after merging, a query returns a self-loop, one person approving their own contract.

**Why**

Extraction runs per chunk, so the same human arrives spelled three ways. Dedup is a *post-extraction* step — nothing prevents the fragments from being born. Embedding-similarity dedup alone is reported to cut duplicate nodes by ~40% (LangChain eval, 2025), so this is the single highest-leverage fix in the pipeline.

**What to do**

1. Match in three escalating levels: text normalization (lowercase, strip diacritics) → fuzzy (Levenshtein / TF-IDF — edit-distance and word-overlap scores that catch near-misses like `Nguyen Van An` vs `Nguyen Van A`) → embedding similarity (`nomic-embed-text` + cosine — comparing meaning-vectors, catches `CTO Alice` vs `Alice, the technology director`).
2. Only compare entities **of the same type** — never merge a `Project` into a `Person` just because the words look alike.
3. Keep the mapping `old_name -> canonical_name`; without it, every relation still points at the old node and you have rebuilt the problem.
4. After remapping, drop relations where source equals target — that is exactly the self-loop the merge created.
5. Set the threshold high (0.85) and keep the mapping so a bad merge can be split back. Merging too eagerly fuses the HR Alice with the CTO Alice, and that error is invisible.

> 📄 **Example code:** [`examples/02-q2-i-have-three-separate-alice-nodes-and.py`](examples/02-q2-i-have-three-separate-alice-nodes-and.py)

**Verify**

Sweep `threshold` at 0.80, 0.85, 0.90 and watch two numbers: how many canonical `Person` nodes remain (canonical = the one surviving merged name), and how many relations were dropped as self-loops. You want exactly one Alice and zero self-loops. If 0.80 fuses two real people and 0.90 lets duplicates through, the answer is a type/property constraint, not a wider threshold.

> **One-line summary:** The same person arrives spelled three ways; merge with normalization → fuzzy match → embedding similarity, same type only, and always keep the mapping for undo.

---

## Q3. My graph is a hairball and the model invents relations that don't type-check [→ §1 Ontology & Schema Design, §3 Relation Extraction]

**What you see**

Five different things are all called "team". Your validator reports `Edge APPROVES requires Person -> Document, got Project -> Person`. Someone asks who approved the Phoenix budget and the graph cheerfully answers with a Project node. A `MANAGES` edge also appears pointing from a person to themselves. And low-confidence guesses are being stored alongside solid facts with nothing to tell them apart.

**Why**

Open (schema-free) extraction lets the model invent its own vocabulary, and every invented label becomes a query you can never write. Schema-first construction is measured to cut invalid relations by ~60% versus open extraction (Stanford KB Construction, 2024) — because "invalid" is defined by you, in advance, not discovered later.

**What to do**

1. Write `ontology.yaml` before touching a document: node types with `required`, `enum`, `format` and `indexes` (`Person.name` is `unique: true` — it is your merge key; enum = a fixed list of allowed values).
2. Pin direction for every edge — `from: Person, to: Document` for `APPROVES` — so a mismatched pair fails immediately instead of landing in the graph.
3. Encode the rules you would otherwise enforce by hand: `Person -[MANAGES]-> Person (cannot manage yourself)`, `Project.budget > 0`.
4. Adopt the hybrid route: core schema + validation, and anything unknown goes to a **pending** queue for periodic human review instead of being dropped or accepted blindly.
5. Gate on confidence: the ontology constraint `APPROVES.confidence >= 0.7` and the same `0.7` cutoff in `filter_by_confidence`. Store the number on every edge so you can re-tune later without re-extracting.

> 📄 **Example code:** [`examples/03-q3-my-graph-is-a-hairball-and-the.py`](examples/03-q3-my-graph-is-a-hairball-and-the.py)

**Verify**

`build_knowledge_graph` already prints the funnel — `Raw: X entities, Y relations` then `After validation: X', Y'`. Compare the two pairs every run and plot the drop rate; a sudden jump means the model started improvising. Alert on any non-empty pending queue, and re-run validation in CI (CI = the automated build/test pipeline that runs on every code change) so a schema-breaking extraction fails the build.

> **One-line summary:** Write the schema first, pin every edge's direction and confidence cutoff, and route anything unknown to a human-reviewed pending queue.

---

## Q4. The graph asserts something and I cannot prove it — where did this fact come from? [→ §2.4 Claims Extraction]

**What you see**

Someone asks "is the 20% budget cut real?" and the agent answers confidently. There is no sentence, no document, no paragraph behind the answer — the graph holds `the department —CUT_BUDGET→ 20%` and nothing else. You cannot tell whether the model read it in the document or invented it, so you end up re-reading 1,000 documents by hand.

**Why**

Entities plus relations store **structure**, not **assertions** (assertion = a claim that something is true, e.g. "the department is cutting its budget 20%"). Microsoft's GraphRAG extracts a third kind — **claims**: a single fact worth keeping, carrying the period it applies to and the chunk it came from. Without that link, evidence provenance (provenance = the documented origin of a fact) is lost at extraction time and cannot be recovered later.

**What to do**

1. Extract claims alongside entities and relations, one fact per claim: `{subject, predicate, object, description}` — for example `{subject: the department, predicate: CUT_BUDGET, object: 20%, period: next quarter, source_chunk: "doc #3"}`.
2. Stamp `source_chunk_id` on every claim at write time. That single field is what makes an answer checkable.
3. Store the quoted `evidence` string on each relation too, so a human can see the original sentence without a second lookup.
4. Change the answering rule: cite a claim as the evidence instead of restating a fact. This is what enables "which regulation / which evidence says X?"
5. Never let a claim lose its source chunk during dedup or merge — carry the id along with the canonical entity.

> 📄 **Example code:** [`examples/04-q4-the-graph-asserts-something-and-i-cannot.py`](examples/04-q4-the-graph-asserts-something-and-i-cannot.py)

**Verify**

Take 10 answers the system produced and require each to name a chunk id you can open and read. Then a stronger test: delete the source chunk from the store and confirm the answer disappears instead of being repeated from memory. If any answer survives its evidence, it came from the model's parameters, not your graph.

> **One-line summary:** Extract claims — each fact stamped with `source_chunk_id` — so every answer can be traced to the exact sentence it came from.

---

## Q5. One new contract arrives — do I rebuild the whole graph, and is the agent approach worth 2–3× the cost? [→ §5 Incremental KG Updates, §7 Agentic Construction]

**What you see**

A production KG gets a new document daily. Two bad options: rerun the full pipeline over all 1,000 documents every morning (slow, expensive, and the answer churns), or append blindly and end up with a person who `MANAGES` both their old team and their new one, plus nodes nobody can delete. Meanwhile a team tries the fancier agentic approach and its bill triples.

**Why**

The batch pipeline in §6 is one-way: text → extract → merge, with no idempotent write (idempotent = running the same write twice changes nothing the second time; Cypher `MERGE` is the create-or-update form of this) and no history. The agentic alternative closes the loop — read → write → check → fix — and tags every triplet (triplet = one `(subject, predicate, object)` fact) with its `source_chunk`, but 2025–2026 work (KnoBuilder, KG-Agent, RAGA) reports **2–3× higher cost** for significantly fewer incorrect triplets.

How to read this table: it compares the two construction styles row by row — how they flow, how they handle errors, whether evidence is kept, and what they cost.

| | Batch pipeline | Agentic agent |
|---|---|---|
| Flow | one-way | read → write → check → fix |
| Errors | re-run the pipeline | decides UPDATE/DELETE itself |
| Evidence | not stored | every triplet has `source_chunk` |
| Cost | moderate | 2–3× higher |

**What to do**

1. Ingest per event, not per rebuild: extract → dedup → upsert, one document at a time.
2. Use `MERGE` on the unique key and always set `updated_at`, so re-ingesting the same document changes nothing.
3. Soft delete instead of hard delete — `SET n.deleted = true, n.deleted_at = datetime()` — so history and provenance survive.
4. Tag provenance on create with `ON CREATE SET s.source_chunk = $chunk`, and also `SET r.source_chunk = $chunk` on the relation.
5. Pick the engine by scale: batch for large volume, agentic for small graphs where accuracy and self-adjusting schemas matter more than unit cost.

> 📄 **Example code:** [`examples/05-q5-one-new-contract-arrives-do-i-rebuild.py`](examples/05-q5-one-new-contract-arrives-do-i-rebuild.py)

**Verify**

Ingest the same document twice — the entity and relation counts printed by `process_new_document` must be identical the second time, and no duplicate `Person` node may appear. Then check the temporal question directly: does the graph now show both the old and the new `MANAGES` edge with their `since` dates, or did one silently overwrite the other?

> **One-line summary:** Ingest per document with `MERGE` + soft delete + provenance tags, so re-running changes nothing and old facts keep their history; pay 2–3× for the agentic approach only when accuracy beats unit cost.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*