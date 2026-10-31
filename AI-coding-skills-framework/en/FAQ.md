# ❓ FAQ — AI Coding Skills Framework (Real Stories, Plain and Friendly Language)

This file collects the questions real beginners asked, with answers in plain words. If a question feels unclear, open the section named in brackets — it points you to the right file.

> **How to read it:** each answer has four parts. **What you see** = what you notice first. **Why** = the reason behind it. **What to do** = the concrete steps. **Verify** = how to check you succeeded.

---

## AI_AGENT_FRAMEWORK.md

### Q1. Framework này thực chất là cái gì — khác gì dùng ChatGPT bình thường? [→ § 🧠 Understanding This Framework]

**What you see**

You clone the repo (clone = download a full copy so you can run it locally) and open `AI_AGENT_FRAMEWORK.md` (1,195 lines, one line = one row of text). It names three subfolders: `harness/` (15 modules), `graph/` (9 modules), `loop/` (7 parts). A module = one self-contained folder that teaches one skill. The doc's first line says it clearly: this teaches you to **build** an agent, not to use a normal chat AI. The table "Which parts need a model?" is the surprise: `BM25 Search` ❌, `Prompt Building` ❌, `Workflow` ❌, `CI/CD Automation` ❌. Only `Vector Search` needs an embedding model (a model that turns text into number lists so similar texts sit close together), and only `Generate Answer` needs an LLM (Large Language Model, e.g. GPT-4o — the AI that writes text).

**Why**

The doc calls the framework the "coordination brain" and the AI model just the "reasoning brain" — one piece of the puzzle. By the doc's own estimate, **~60% of the framework is plain code that needs no model**, ~40% needs one. The "too much" feeling usually comes from counting the AI-free parts as AI work.

**What to do**

1. Open `⚡ Quick Reference` and pick **one** row that matches what you plan to build — do not read all 13 sections in order.
2. Set up your environment once; reuse it for every module.
3. Start with `harness/01-retrieve-memory-knowledge` and `harness/02-build-context`: the Module → Project matrix shows these serve 15/20 and 12/20 of the doc's projects (matrix = a table mapping each module to which projects use it).
4. You do not need to buy an API yet: Ollama (a free tool that runs AI models on your own machine) covers all of Phases 1–6.

> 📄 **Example code:** [`examples/01-q1-framework-nay-thuc-chat-la-cai-gi.sh`](examples/01-q1-framework-nay-thuc-chat-la-cai-gi.sh)

**Verify**

Run `curl -s http://localhost:11434/api/tags` (curl = send a web request from the command line; this one asks Ollama which models are installed) — it must list both model names. Load 10 markdown files into module 01, ask one English question, and the answer must quote the exact passage you loaded. If it cannot quote, the problem is at the model layer — you have not touched the framework layer yet.

> **One-line summary:** This framework is mostly glue code (~60%) around a small AI core — start with one Quick Reference row and two modules, and a free local model is enough to learn.

---

### Q2. Mới vào, tôi nên bắt đầu từ đâu? [→ § 🛠️ How to Use + Lộ Trình Học]

**What you see**

You face 15 modules in `harness/`, then `loop/`, then `graph/` — too many doors. The 6-phase roadmap in the doc looks chaotic too: Phase 1 is `01 Retrieve Memory → 02 Build Context`, but Phase 2 jumps to `05 Prompt Builder ← 06 Decide Tools`, then Phase 3 goes back to `03 Update Memory → 04 Plan`. (Roadmap = a suggested learning order.)

**Why**

The first two modules are the data intake pipe — if nothing goes into the context, nothing else matters. The roadmap deliberately interleaves so you see one full loop (fetch data → build context → generate an answer) before adding memory and planning. The doc also ships a 26-week plan if you want to go all the way — but its own Tips section still says "START SMALL".

**What to do**

1. Do project #1 Personal Knowledge Base first — 2–3 days, only modules 01, 03, 06. It just needs ChromaDB (a small local database for vector search), `nomic-embed-text` (a small embedding model), and a simple Python command-line tool.
2. Then project #2 Document Q&A Chatbot — 3–5 days, adding modules 02 and 05. Expected result: a chatbot that answers from your internal documents instead of making things up.
3. Combine later: #1 + #2 = #6 Enterprise RAG Platform (RAG = Retrieval-Augmented Generation, i.e. answer questions by first searching your documents).
4. Measure each step (count of correct answers) before adding a new module. At intermediate level, project #6 is listed as 2–3 weeks for an MVP (Minimum Viable Product = the smallest version that works).

> 📄 **Example code:** [`examples/02-q2-moi-vao-toi-nen-bat-au-tu.sh`](examples/02-q2-moi-vao-toi-nen-bat-au-tu.sh)

**Verify**

The `curl` command returns 768 floating-point numbers (one vector = one list of 768 numbers describing your text). The command `pkb search "cách deploy Docker"` must find the right note among ~1,000 notes. If it does not, fix the **search** step (BM25 + vector) — do not touch the prompt builder.

> **One-line summary:** Start with the two intake modules and one tiny project (Personal Knowledge Base), measure it, and only then grow — the messy phase order is intentional.

---

### Q3. Module 12 là Sandbox, nhưng "Part XII" lại là Loop — tôi bị lừa ở đâu? [→ § Learning Structure]

**What you see**

In `AI_AGENT_FRAMEWORK.md`, "Part XII" is Loop Engineering and "Part XIII" is Graph Engineering. But in the `harness/` folder, module `12` is Sandbox Execution, `13` is Trajectory & Observability, `14` is Compaction & Context, `15` is Approval Gates. A beginner who searches "12" lands in `loop/` by mistake.

**Why**

Two numbering systems coexist: the numbers `01`–`15` count **modules in the folder**, while the labels `Part I`–`Part XIII` count **sections of the document**. The doc itself warns about this right under the Quick Reference table.

**What to do**

1. Count by **path**, not by label: `harness/12-sandbox-execution` is always the sandbox (sandbox = an isolated area where the agent can run commands without touching the rest of your machine), never the loop.
2. Use the three files at the repo root as your map: `AI_AGENT_FRAMEWORK.md` (the front page), `HARNESS_ENGINEERING.md`, `GRAPH_ENGINEERING.md`.
3. Modules 12–15 are not on the learning path because they are not **stages** of the pipeline — they are the foundation every stage 01–11 stands on.
4. Want the agent to improve over time? That is `loop/`, not `harness/12`.

How to read the table below: the left column is what you are looking for in plain words; the right column is the exact folder that contains it.

| You are looking for | Correct path |
|---|---|
| Isolate the code where the agent runs commands | `harness/12-sandbox-execution/` |
| Replay a run that already happened | `harness/13-trajectory-observability/` |
| Keep context from growing without limit | `harness/14-compaction-context/` |
| Ask a human to approve irreversible actions | `harness/15-approval-gates/` |

> 📄 **Example code:** [`examples/03-q3-module-12-la-sandbox-nhung-part-xii.sh`](examples/03-q3-module-12-la-sandbox-nhung-part-xii.sh)

**Verify**

Count the folders: `harness/` has 15 modules, `graph/` has 9, `loop/` has 7 parts. Open `harness/12-sandbox-execution/README.md`; the opening must talk about isolation and execution boundaries (rules for where the agent may run things), not about improvement loops.

> **One-line summary:** "Module 12" and "Part XII" are two different numbering systems — trust folder paths over document labels, and remember modules 12–15 are the foundation, not a stage.

---

### Q4. Tôi có phải mua model đắt tiền không, và model 12 tỉ tham số có nặng máy không? [→ § Hands-on Environment + 2 loại model]

**What you see**

The doc lists `gemma3:12b` and `nomic-embed-text` running through Ollama, then a salary table showing 30–80 million VND/month for AI Engineers. Beginners ask: do I need to buy `GPT-4o` or `Claude`, and can a 12-billion-parameter model (parameters = the learned weights inside a model; more usually means smarter but heavier) even run on a laptop?

**Why**

The framework needs exactly **two kinds of model**: one embedding model for search, one LLM to generate answers. In the doc's first RAG example, only 2 lines of code call the model; the chunk splitting, vector storage, and cosine scoring (cosine = a similarity score between two vectors) are plain Python.

**What to do**

1. Use free local Ollama to learn: `nomic-embed-text` is only 768 dimensions (768 numbers per text — a small, cheap vector), far cheaper than paying for an API.
2. Switch to a paid API only when you need higher quality — change exactly **one** line of code, keep the rest.
3. Measure cost before scaling: the harness saves 40–60% of token spend by compressing context and checking outputs.

How to read the table below: each row is one kind of model; "local" means free on your machine, "paid" means a cloud API.

| Model type | Its job | Runs locally | Runs as paid API |
|---|---|---|---|
| Embedding model (turns text into searchable vectors) | converts text to vectors for search | `nomic-embed-text` | `text-embedding-3-small` |
| LLM (writes the final answer) | generates answers | `gemma3:12b` | `GPT-4o`, `Claude` |

> 📄 **Example code:** [`examples/04-q4-toi-co-phai-mua-model-at-tien.py`](examples/04-q4-toi-co-phai-mua-model-at-tien.py)

**Verify**

`ollama list` must show `gemma3:12b`. Ask the same question on local and on the API: if local is right and the API is wrong, the problem is the context you sent, not the model.

> **One-line summary:** You need only two models — one small embedder and one LLM — and a free local Ollama setup is enough to learn; upgrade to a paid API later by changing a single line.

---

## GRAPH_ENGINEERING.md

### Q1. Tôi đang ở tầng truy xuất nào — keyword, vector, hay đã cần graph? [→ § 3 Three Stages of Retrieval Evolution]

**What you see**

You just finished vector search, and now you hear you must "go graph" — but which tier do your users' real questions live in? This section explains the three retrieval tiers and helps you pick.

How to read the table below: each row is a retrieval tier (a generation of search technology). The last column, control level, is what the doc claims, shown with stars — more stars = more control. It is not a performance score.

| Tier | What you use | Questions it answers well | Control level |
|---|---|---|---|
| 2020-2022 | BM25, inverted index | exact keywords (contract codes) | ⭐ low |
| 2023-2025 | embeddings + vector DB | reworded questions | ⭐⭐⭐ medium |
| 2026+ | knowledge graph + GraphRAG | multi-step relations | ⭐⭐⭐⭐⭐ high |

Gloss: BM25 = classic keyword matching with an inverted index (a word → documents lookup, like a book index). Vector DB = stores text as number vectors so differently-worded questions still match. Knowledge graph + GraphRAG = entities and their relations, so multi-hop questions work (multi-hop = an answer that needs 2+ linked facts, e.g. "who funded the startup founded by X's PhD advisor?").

**Why**

The three tiers **stack**, they do not replace each other. The doc says it plainly: you still need BM25 for contract codes, you still need vectors for reworded questions, and you add a graph only for multi-hop and global sensemaking (global sensemaking = questions that need the whole corpus, e.g. "what are the main themes across all reports?").

**What to do**

1. Take 20 real user questions, and label each one local / global / multi-hop using the doc's table (local = one specific fact; global = a theme across many documents).
2. Open `graph/` only if the errors cluster in the global or multi-hop group.
3. If the errors are local ("what does clause 5 of contract X say"), fix your chunking (chunking = how you cut documents into pieces) instead of buying a new database.
4. Record which questions the graph still **cannot** answer — those belong to BM25 and vectors.

> 📄 **Example code:** [`examples/05-q1-toi-ang-o-tang-truy-xuat-nao.py`](examples/05-q1-toi-ang-o-tang-truy-xuat-nao.py)

**Verify**

Re-run those 20 questions after wiring in the graph. If the count of correct answers does not rise, review your relation-extraction quality (how well you pull relations out of text) — do not rush to change databases.

> **One-line summary:** The three retrieval tiers stack rather than replace each other — label your real questions local/global/multi-hop first, and only add a graph if your failures are multi-hop or global.

---

### Q2. Tôi không biết trước cần những quan hệ nào — có phải vẽ schema trước không? [→ § 8.2 The 8 Commandments of Graph Engineering]

**What you see**

You have 500 contract files and internal emails. An expert says you need an "ontology" (a rulebook of which entity types and relation types are allowed — e.g. Person, Project, Company as nodes; WORKS_ON as an edge/relationship). It sounds like you must know everything up front. Otherwise, the doc warns, the graph becomes a "hairball" (a tangled mess you cannot query).

**Why**

The doc's rule #1 is **Schema First, Data Second**: define the ontology before loading data. Rule #2 is **Every Edge Has Provenance** (provenance = where a fact came from): every relation must carry `source`, `confidence`, `timestamp`. That trio is exactly what turns an answer into a checkable answer — you can trace it back.

**What to do**

1. Start with just 3 node types and 5 edge types — these numbers come straight from the doc's advice.
2. Put the ontology in a `data/ontology.yaml` file, separate from code.
3. Load data in batches with checkpoints (a saved point you can roll back to), never the whole corpus at once.
4. Block wrong-type relations before writing: never allow `Person -[EATS]-> Project` (a person "eats" a project — nonsense the validator should reject).
5. Record each relation's source at extraction time, not when answering.

> 📄 **Example code:** [`examples/06-q2-toi-khong-biet-truoc-can-nhung-quan.yaml`](examples/06-q2-toi-khong-biet-truoc-can-nhung-quan.yaml)

**Verify**

After the first batch: every edge has all three fields `source`, `confidence`, `timestamp`, and a question that spans 2 documents gets answered with its evidence path. If a field is missing, patch the extraction script (the code that pulls relations from text) — do not fix answers one by one.

> **One-line summary:** Define a small ontology first (3 node types, 5 edge types), stamp every relation with source + confidence + timestamp, and load in batches — that prevents the unqueryable hairball.

---

### Q3. Muốn thử trong một tuần mà chưa mua gì — bắt đầu từ đâu? [→ § 10 Tools and Frameworks + § 11.3 Advice]

**What you see**

You want to see whether a graph really solves your problem, with a budget of $0 and 7 days. The doc's tool table has 6 database rows; picking the wrong one wastes the whole week.

**Why**

The bottleneck is not storage — it is **building the graph**: every relation-extraction round costs LLM tokens, and extraction quality decides everything downstream. So the starting volume must be small.

**What to do**

1. Follow the doc's closing advice: start with **100 documents, 3 node types, 5 edge types**. Do not try to build a Wikipedia-scale graph on day one.
2. Pick a store by real scale: `Kuzu` (embedded in Python, no server) or `NetworkX` (an in-memory Python library) for experiments; `Neo4j` (a full graph database server) for production.
3. Build from ready-made templates: `docker-compose.yml` starts Neo4j, `scripts/extract_graph.py` extracts, `scripts/query_graph.py` queries, `scripts/evaluate.py` measures.
4. Cap `max_hops` at 2–3 (max_hops = how many relationship steps one query may follow), or queries will explode in cost.
5. Skip `graph/07-gnn` at first — the doc treats it as **learning on graphs** (GNN = Graph Neural Network, a model that learns patterns from graph structure), not a requirement for your first answer.

> 📄 **Example code:** [`examples/07-q3-muon-thu-trong-mot-tuan-ma-chua.sh`](examples/07-q3-muon-thu-trong-mot-tuan-ma-chua.sh)

**Verify**

After 100 documents, a local question must be answered correctly even without the graph, and a multi-hop question must print its evidence path (the chain of nodes and edges that justifies the answer). If accuracy does not beat plain vector search, add data instead of changing architecture.

> **One-line summary:** Pilot cheap and small — 100 docs, 3 node types, 5 edge types, an embedded database, max_hops 2–3 — because extraction, not storage, is where the money and quality go.

---

### Q4. `graph/` khác `harness/` và `loop/` ở chỗ nào? [→ § 6 Integration With Harness and Loop]

**What you see**

Three sibling folders, each with children: `harness/` (15 modules), `graph/` (9 modules), `loop/` (7 parts). No file states who serves whom, so you do not know whether to learn Graph before Harness.

**Why**

The doc draws the three-way relationship exactly: **Harness** (`harness/01-11`) gives tools, memory, context, and guardrails for **one run** of the agent. **Graph** (`graph/01-09`) supplies the **knowledge layer**, replacing a plain vector database. **Loop** (`loop/01-07`) coordinates **many** Harness runs over time (guardrails = automatic limits that stop unsafe behavior).

**What to do**

1. Follow the flow already in the doc: doc → `graph/02` (build the KG) → `graph/03` (storage) → `graph/05` (GraphRAG) → `harness/02` (merge into context) → model. (KG = knowledge graph, a database of entities and relations.)
2. Map the 7 components onto the 9 modules before opening code: node/edge → `01`, ontology → `02`, storage → `03`, embeddings → `04`, GraphRAG → `05`, reasoning → `06`, GNN → `07`, pipeline → `08`, evaluation → `09`.
3. Update incrementally with `graph/08` — do not rebuild the whole graph when one new document arrives.
4. Want to go deeper? Read each folder's own FAQ: `graph/FAQ.md`, `harness/FAQ.md`, `loop/FAQ.md`.

How to read the table below: the left column is your need in one sentence; the right column is the folder to open.

| You want | Open folder |
|---|---|
| One agent run that needs tools, permissions, logs | `harness/` |
| Answers that need relations and proof paths | `graph/` |
| An agent that improves across many runs | `loop/` |

**Verify**

Run `MATCH (n) RETURN count(n)` on your graph store (a Cypher query — Cypher is the query language for Neo4j-style graphs — and this one counts all nodes). The number must not be 0. Add one new document, re-run `scripts/query_graph.py`: the node count goes up, and the old question's answer stays **unchanged** — that is incremental update working correctly.

> **One-line summary:** Harness powers one run, Graph supplies the knowledge layer, Loop coordinates runs over time — learn them in that order: Harness → Graph → Loop.

---

## HARNESS_ENGINEERING.md

### Q1. Thêm harness tốn công hơn không — có đáng không, và tiền thì thế nào? [→ § 4.1 + § 4.5 Why Is Harness Engineering Important?]

**What you see**

You are building an agent that fixes bugs. Writing your own check layer, permission layer, and logging layer means 2–3 extra weeks before any visible feature. Your boss wants results this week. You wonder if it is worth it. (Harness = the scaffolding around the model: tool interfaces, limits, logging, checks.)

**Why**

The doc cites measured results, not beliefs: the Princeton NLP SWE-agent study shows that just by redesigning the interface between the agent and the computer, success rate went from **12.5% to 20.5%** — a 64% gain with **no change to the model**. The model was not weak; the environment was not designed. (SWE-agent = an agent that resolves real GitHub software issues.)

**What to do**

1. Start with the minimal version: cap tool output length, run a linter on every file write (a linter = a tool that flags code style/syntax problems), compress conversation history. These three changes cost far less than rewriting the system.
2. Enforce one non-negotiable rule: **no saving a file if the linter reports an error**.
3. Log 3 numbers from day one: success rate, time to resolve one issue, tokens per run.

> 📄 **Example code:** [`examples/08-q1-them-harness-ton-cong-hon-khong-co.ts`](examples/08-q1-them-harness-ton-cong-hon-khong-co.ts)

**Verify**

Run the same 20 GitHub issues on the old and new setups. If the pass rate rises without touching the model, that is proof of the environment layer's value. The doc's example saves $30,000 → $12,000 in 3 months (−60%), but you must measure on your own system — do not copy the number.

> **One-line summary:** Yes, it pays: a better environment lifted SWE-agent success 64% with no model change — start with output caps, linter gates, and history compression, and measure from day one.

---

### Q2. Nghe nói "Prompt Engineering đã chết" — vậy tôi còn viết prompt không? [→ § 3 Three Evolution Phases of AI Engineering]

**What you see**

One article says prompt engineering is dead; this framework still has `harness/05-prompt-builder` and `harness/11-evaluation`. You do not know whether to stop writing prompts, or keep writing them up to what point.

**Why**

The doc answers directly in its Key Insight: *"Prompt Engineering is not dead, but it is no longer enough."* Three phases stack control — prompt (low) → context (medium) → harness (high). The "Which parts need a model?" table also marks Prompt Building ❌: assembling a prompt is just arranging text, it costs zero API money. The doc's example: the instruction *"Write Python code. Make sure it has no syntax errors"* gets replaced by a 9-line script that checks syntax before returning anything.

**What to do**

1. Keep writing prompts, but do not expect them to hold the system together. A 5-page prompt cannot save one bad tool call (tool call = the model asking your code to run a function).
2. Move the important parts from words to infrastructure: the prompt says "be careful"; the code **refuses** to return broken code.
3. Every time you edit a prompt, re-run the same question set so you know whether the edit helped.

> 📄 **Example code:** [`examples/09-q2-nghe-noi-prompt-engineering-a-chet-vay.js`](examples/09-q2-nghe-noi-prompt-engineering-a-chet-vay.js)

**Verify**

Count how many times you had to fix the prompt in one week. If that number does not fall, you are curing symptoms with more words — add one constraint at the tool layer or the output-check layer instead.

> **One-line summary:** Prompts still matter but cannot carry the system alone — push critical guarantees into code (checks, guards) and use fixed test sets to measure every prompt change.

---

### Q3. Module 12–15 là giai đoạn hay nền? Tôi có thể bỏ qua không? [→ § 🔭 Overview: 7 Components → 15 Modules]

**What you see**

You built modules 01–11; the agent already fixes simple bugs on its own. Now you read `harness/12` to `harness/15` and find them described as "a cross-module control plane", not on the learning path. You are tempted to skip them to hit a deadline.

**Why**

Modules 01–11 are pipeline stages: do them in order and see results immediately. Modules 12–15 are **not** stages — they are the foundation every stage 01–11 depends on, like a spine holding up a body. Skip them and the agent still runs; but when it goes wrong, it cannot stop in the right place, cannot be replayed (replay = re-run the same steps to see what happened), and cannot ask anyone to press "approve".

**What to do**

1. Prioritize by the coverage numbers the doc lists: `01-retrieve-memory` 85%, `07-workflow` 80%, `06-decide-tools` 75%, but `08-task` only 45% (coverage = how many of the doc's 20 projects use that module).
2. Wire in `12-sandbox-execution` **early** — as soon as the agent runs real commands on your machine, not at project end.
3. Turn on `13-trajectory-observability` before scaling to many agents: without logs there is no debugging.
4. Put `15-approval-gates` on exactly the irreversible actions (deploy, delete data, mass email). Approval gate = a checkpoint where a human must say yes before the action runs.

> 📄 **Example code:** [`examples/10-q3-module-12-15-la-giai-oan-hay.sh`](examples/10-q3-module-12-15-la-giai-oan-hay.sh)

**Verify**

Run end-to-end: your documents get loaded, one question is answered correctly with no prompt editing. If you are not logging time, tokens, and error rate, you have no harness — you only have a long prompt.

> **One-line summary:** Modules 12–15 are the foundation, not a stage — skip them and the agent runs, but you lose replay, control, and human approval; add sandbox and logging early.

---

### Q4. Tôi đã có code tìm kiếm rồi — làm sao cho nó tự chạy giữa prompt và LLM? [→ § 5.3 Where Does the Intervention Happen?]

**What you see**

You already wrote and tested a context-retrieval function; run by hand, it returns exactly 2 relevant passages. But when you type in the chat UI, the answer is still generic — because the app calls `localhost:11434` (Ollama's default address) directly, bypassing your code entirely.

**Why**

Nobody calls your code automatically. You must stand in the middle: intercept the question (intercept = catch the request before it reaches the model), fetch context, inject it into the prompt, then send. The doc shows these 4 steps and gives 4 ways to install them.

**What to do**

1. Pick one of the four ways: **proxy server** (any chat app — a middleman program your requests pass through), **function wrapper** (your own Python code), **Open WebUI** (no code needed), **LangChain/LlamaIndex** (production frameworks).
2. Fastest path: stand up a proxy and change the app's address from `localhost:11434` to `localhost:5000/api/chat`.
3. Always print how many context passages were injected — that is proof you did not skip the middle step.

How to read the table below: each row is one integration method; "Độ khó" (difficulty) uses stars — more stars = harder.

| Cách | Dùng khi | Độ khó |
|---|---|---|
| Proxy server | any chat app (web, mobile, desktop) | ⭐⭐ |
| Function wrapper | a Python app you wrote yourself | ⭐ |
| Open WebUI | you already use Open WebUI | ⭐ no code needed |

> 📄 **Example code:** [`examples/11-q4-toi-a-co-code-tim-kiem-roi.py`](examples/11-q4-toi-a-co-code-tim-kiem-roi.py)

**Verify**

Open the proxy log, type one question in the UI: the log must show context passages assembled **before** the request to Ollama. No such log line means the app still calls the model directly.

> **One-line summary:** Your search code only helps if the request passes through it — stand in the middle with a proxy or wrapper, and prove it by logging the injected context.

---

### Q5. MCP và A2A khác nhau thế nào — và GraphRAG 2026 có gì mới? [→ AGENT_SYSTEM_ARCHITECTURE.md §3.4-3.5 + graph/05-graph-rag]

**What you see**

The docs mention two acronyms, MCP and A2A; then the graph docs add GraphRAG, LazyGraphRAG, LightRAG — and you cannot tell how they relate. This section sorts them out.

**Why**

The three concepts solve three different problems:

How to read the table below: each row is one protocol or technology; the middle column says who talks to whom; the last column says what it standardizes.

| Protocol / Technology | Who talks to whom | What it standardizes |
|----------------------|---------------------|-----------------|
| **MCP** (Model Context Protocol) | Agent → Tools / Data / APIs | "What the agent does" — tools, resources, prompts |
| **A2A** (Agent-to-Agent, Linux Foundation 2025) | Agent → Agent (different framework/vendor) | "Who the agent talks to" — handoffs, collaboration, results |
| **GraphRAG** | Agent → Knowledge Graph | "What the agent asks" — multi-hop and global queries, with citations |

Gloss: MCP = a shared plug standard so an agent can use any tool or data source. A2A = a shared protocol so agents from different vendors can talk to each other (handoff = passing a task from one agent to another). GraphRAG = answering questions by walking a knowledge graph, with citations.

**MCP + A2A = complementary:** An agent uses both — MCP to call tools, A2A to delegate to another agent.

**GraphRAG news, 2025–2026:**
- **LazyGraphRAG** (Microsoft, 2024-2025): indexing cost drops to plain vector-RAG level, quality on par with full GraphRAG, queries ~700× cheaper. Integrated into Microsoft Discovery.
- **LightRAG** (EMNLP 2025): dual-layer graph + vector, incremental update.
- **Gartner 2026**: GraphRAG listed in "Top Trends in D&A" for complex AI use cases.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026).

**What to do**

1. MCP is mandatory — every agent needs to call tools (see `06-decide-tools-mcp/`).
2. A2A when you must combine agents from **multiple frameworks** (Claude + LangGraph + ADK) — see `09-multi-agent/`.
3. GraphRAG when answers must be **multi-hop** or **global aggregation** (global aggregation = one answer summarizing many documents) — see `05-graph-rag/`.

> **One-line summary:** MCP standardizes how agents call tools, A2A how agents talk to each other, GraphRAG how agents query knowledge graphs — start with MCP, add the others only when the need appears.

---

*A standalone FAQ file — the source docs were not modified. Sources: AI_AGENT_FRAMEWORK.md, GRAPH_ENGINEERING.md, HARNESS_ENGINEERING.md.*