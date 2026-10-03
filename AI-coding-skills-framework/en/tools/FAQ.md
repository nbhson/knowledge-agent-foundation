# ❓ FAQ — Tools Directory (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Bash output is eating my whole context window — which directory actually fixes that today? [→ Directory Structure Across 4 Groups]

**What you see**

Every agent turn the model runs `ls`, `cat`, `git status`, `cargo test` — and gets back hundreds of lines. The measured cases in this README: `ls -la` returns 45 lines, `cargo test` returns 200+ when something fails, `docker ps` returns many columns. The model then misses the one line that mattered, because the important error is buried in noise it has to pay for twice — once in tokens, once in attention.

**Why**

This is the opening problem the whole `tools/` directory exists to solve. Input tokens are the currency of agent reasoning, and the fix is a **CLI** (command-line interface) proxy that rewrites command output before it enters the model's context. That tool is **RTK — Rust Token Killer**, in `tools/rtk/`.

**What to do**

1. Install RTK and wire it into your agent's hook system — that is stage 1 of the six-stage roadmap, because the saving is immediate.
2. Start with the `git-speedup` pattern in `rtk/03-patterns/`; it is the one the roadmap itself recommends first.
3. Measure before and after with the tools in `rtk/04-savings/`, rather than trusting the headline number.

| Command | Raw output | After RTK | Reduction |
|---|---|---|---|
| `ls -la` | 45 lines | 12 lines (tree + counts) | ~73% |
| `git push` | 15 lines | `ok main` (1 line) | ~93% |
| `cargo test` | 200+ failing | `FAILED: 2/15 tests` | ~90% |

**Verify**

Run the same `ls -la` and `cargo test` before and after installing. If the line counts do not drop, the hook is not attached — RTK integrates through different mechanisms per agent, from a native `PreToolUse` hook to plain instruction files, so check the integration table in the case studies.

---

## Q2. Do I have to install all ten of these directories, or can I start with two? [→ Learning Roadmap (Recommended Roadmap)]

**What you see**

You look at the tree and see ten directories across four groups plus a security layer and a quality layer: `rtk`, `loop-cli`, `langchain`, `autogen`, `crewai`, `vector-db`, `mcp-ecosystem`, `guardrails`, `observability`, `evaluation`. The honest reaction is: I do not have a month for this.

**Why**

You do not need it. The roadmap in this README is deliberately sequenced as six stages, and the order is by return, not by completeness. Nobody installs ten things on day one. The same README gives a second, cheaper entry point: a "by need" table that maps each symptom to exactly one directory — cut bash token costs now means `rtk/`, automate loops safely means `loop-cli/`, nothing more.

**What to do**

1. Stage 1 — install RTK and apply one pattern. Payback is immediate, and the README claims it cuts 40-90% of tokens for repetitive bash commands.
2. Stage 2 — pick **one** framework (`langchain/` for graphs, or `autogen/` + `crewai/` for multi-agent) and add `vector-db/` for memory and retrieval.
3. Stages 3 to 6 — connect tools (`mcp-ecosystem/`), make calls safe (`guardrails/`), measure (`observability/`, `evaluation/`), then automate (`loop-cli/`).
4. Resist the urge to jump to stage 6 because automation looks impressive. `loop-cli/` is last in the roadmap for a reason.

**Verify**

After stage 2 you should have a harness that runs end to end: a framework orchestrating, a vector store answering queries, and one compression layer in front of the shell. If you cannot name which single stage gave you the biggest drop in tokens per run, you installed out of order.

One more thing to know before you plan: every subdirectory follows one convention — an overview `README.md` plus numbered topics — and only `rtk/` is complete today. The rest ship the overview alone.

---

## Q3. LangChain, AutoGen or CrewAI — do I need all three frameworks? [→ Group 2 — Framework (Building harness orchestration)]

**What you see**

Three framework directories side by side, all described as "multi-agent harness", and you cannot tell whether they are alternatives or layers. Meanwhile every tutorial you find online seems to use a different one.

**Why**

They are **alternatives**, not layers. The README groups them under one heading only because they all materialize the same seven harness components into code. Each takes a different shape, and each shapes your code differently once chosen. The cost of choosing badly is real: a framework rewrite late in a project is far more expensive than a slow afternoon reading three overviews. Note that only `langchain/` carries a full subdirectory README here — `autogen/` and `crewai/` ship the overview only, so plan to read them upstream.

**What to do**

1. If you think in states, transitions and cycles, use `langchain/` — LangGraph's `StateGraph` models the seven components directly, with a `ToolNode` for tool calls and retrieval-augmented generation (RAG) built in.
2. If you think in conversations between specialists, use `autogen/` — the `UserProxyAgent` plays the harness role and `GroupChat` orchestrates.
3. If you think in named roles with a chain of tasks, use `crewai/` — `Agent` / `Task` / `Crew`, with `Process.sequential` or `Process.hierarchical`.
4. Pick one, write ten lines against it, then commit. Comparing on paper is cheap; comparing on a live harness is not.

**Verify**

You should be able to name your process type in one sentence — "sequential", "hierarchical", or "state graph". If you cannot, you have not chosen yet, and building with all three at once is how projects stall.

---

## Q4. I skipped `guardrails/` and `evaluation/` for months because nothing was visibly on fire — was that a mistake? [→ Security Layer / Quality Layer]

**What you see**

Everything works. The agent runs tools, the framework answers questions, tests pass. Then one release ships a change nobody approved, and two weeks later a prompt tweak quietly degrades answer quality and you cannot tell when it happened.

**Why**

Both layers are invisible while nothing is broken — that is what makes them easy to skip. The security layer (`guardrails/` — Guardrails AI, NeMo, LlamaGuard) is the control layer *before* the agent acts: validators, rails, permissions and rate limits. The quality layer (`evaluation/`, `observability/`) is what blocks regressions: eval suites, cost tracking and latency targets. They sit at stages 4 and 5 of the roadmap, after the parts that feel productive — which is exactly why they get deferred.

**What to do**

1. Add `guardrails/` before you add more tool access, not after an incident — it validates every tool call before execution.
2. Put one `evaluation/` suite in CI (continuous integration) early, even a small one. PromptFoo is the README's example for blocking regressions; Deepeval and Ragas cover answer quality and retrieval metrics.
3. Add `observability/` at the same time — LangSmith, Helicone, OpenLLMetry or Weights & Biases — so a failing eval tells you whether it was cost or latency.
4. Budget one day for both layers. They look like overhead until the first incident or the first silent regression, then they are the only reason you can prove what changed.

**Verify**

Break one guardrail on purpose and confirm the tool call is refused. Change one line of a prompt and confirm CI fails on the eval suite. A layer you cannot demonstrate failing is a layer you have not tested.

---

## Q5. Why do I need both a vector database and MCP — aren't those the same "connect stuff" job? [→ Group 3 — Vector DBs / Group 4 — MCP Ecosystem]

**What you see**

You are adding `vector-db/` and `mcp-ecosystem/` in the same stage, and both descriptions say "connect the agent to things", so you install one twice by accident.

**Why**

They solve opposite questions. A vector database (Chroma, Pinecone, Qdrant, Weaviate) stores and retrieves **semantic memory** — text turned into embeddings, then found again by meaning rather than by exact keyword. MCP (Model Context Protocol) is a **protocol**, not a database: it standardizes how an application connects to external tools and data, so a tool server plugs in without custom glue code. The README maps them to different harness components for exactly this reason.

**What to do**

1. Use `vector-db/` when the question is "what do we already know about this?" — it serves the memory tiers and retrieval-augmented generation, including the Tier 2 warm memory pattern.
2. Use `mcp-ecosystem/` when the question is "what can the agent *do*?" — register tool servers into the registry, including the pre-configured GitHub MCP server.
3. Keep them separate in your plan. Combining them makes cost and failure modes impossible to attribute, because a wrong answer and a failed tool call then look identical.
4. Expect one prompt-side benefit from each: the vector store shrinks what you paste into the prompt, the protocol shrinks what you hand-write.

**Verify**

Ask two questions after setup: one semantic lookup that must return stored knowledge, and one MCP tool call that must reach a live external system. If both only work through the same layer, you wired one of them twice.

---

## Q6. Half these directories contain only a `README.md` — am I reading a plan or a finished library? [→ The Complete Directory Tree Summary]

**What you see**

You click into `autogen/`, `crewai/`, `evaluation/`, `guardrails/`, `langchain/`, `mcp-ecosystem/`, `observability/`, `vector-db/` and each one holds a single `README.md`. Only `rtk/` is fully built out, with `01-concepts/`, `02-setup/`, `03-patterns/`, `04-savings/` and `05-troubleshooting/`.

**Why**

It is a map, not a library — and the README says so: this branch holds **knowledge**, the way `harness/` and `loop/` do, while `tools/` holds the binaries, CLIs and plugins you install. The learning roadmap for every subdirectory follows the same convention (an overview README plus numbered topics), but only `rtk/` has filled in its numbered topics so far. Nothing is broken; the directories are simply early.

**What to do**

1. Read the subdirectory README first — it tells you the tool's role, its upstream link, and which harness component it serves.
2. For depth on the one tool that is finished, follow `rtk/03-patterns/` — it already has real files such as `git-speedup.md`, `test-only-failures.md` and `file-smart-read.md`.
3. For ecosystem context this README deliberately does not duplicate, follow the branch links to `harness/` (the seven components) and `loop/07-tools` (the full `loop-*` table).
4. Skip the numbering entirely until you need it. The subdirectory overview is enough to decide *whether* to install; the numbered topics are for *how*.

**Verify**

You can name, for any directory you opened, which harness component it serves — retrieval and memory, context, tools and permissions, workflow, task, multi-agent, automation, or evaluation. A subdirectory you cannot place in that map is one you should not install yet.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*