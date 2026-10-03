# ❓ FAQ — LangChain / LangGraph (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Do I need LangChain at all, or is my own 200-line harness better? [→ Why LangChain Matters?]

**What you see**

You have read `HARNESS_ENGINEERING.md` and understand the seven components: retrieve memory, build context, update memory, plan, prompt builder, tool decision, workflow. Writing that yourself means handling model calls, tool routing, retries, and history — and you are about three weeks from a working version. The README calls LangChain "Option 4 — Professional framework", and you are not sure whether Option 4 is a shortcut or a dependency you will regret.

**Why**

Because LangChain is not an orchestrator you must adopt; it is a **library of the seven components, already built**. The mapping is direct and one-to-one: `ChatOpenAI` for the model, `@langchain/core/tools` for tool calling, `MemorySaver` for memory (01/03), `ContextualCompressionRetriever` for context building (02), `ChatPromptTemplate` for the prompt (05), `ToolNode` for tool execution (06), `StateGraph` for the workflow (07). The claim in the README is literal: every harness concept here has a module that implements it. The cost is 700+ integrations arriving with it, which is a lot of surface you did not write.

**What to do**

1. Use LangChain when you want retries, streaming, and tracing on day one — "production-ready" is the reason to take it, not convenience.
2. Keep the LLM behind a wrapper of your own so switching costs one file.
3. Start with LangChain core only: model + tools + memory. Do not begin with a graph.
4. Move to LangGraph once you have branches and loops you cannot express linearly — that is what it is for.
5. Add tracing early with LangSmith (step 5 of the roadmap), before you have a bug you cannot locate.

```typescript
const harness = {
  llm: new ChatOpenAI({ model: "gpt-4" }),
  tools: [ new DynamicStructuredTool({
    name: "search", description: "Search the web",
    func: async (input) => { /* ... */ }
  })]
};
```

**Verify**

Delete one component from the README's mapping table and replace it with your own code. If your version is longer than the module name and still breaks on retries, use the library for that component.

---

## Q2. My graph runs forever — agent → tools → agent → tools never ends. Where do I put the brake? [→ LangGraph (Orchestration)]

**What you see**

You built the recommended graph and it works: `retrieve → build → agent → tools → agent → tools`. Then on a real task the agent keeps calling tools, gets results, calls tools again. The state object grows, the trace gets longer, and nothing ever reaches `END`. The edge is exactly as documented — and the documentation never says how to leave.

**Why**

Because `graph.add_edge("tools", "agent")` is an **unconditional loop-back**, and the only thing that exits is the `should_continue` function you wrote in `graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})`. If that function is permissive — for example it returns `"tools"` whenever a tool call exists, without checking whether anything was learned — there is no exit in the graph itself. The graph is not stuck; your stop condition is.

**What to do**

1. Write `should_continue` as a budget, not a guess: a step counter on the state, an unchanged-output detector, and "no progress" as reasons to finish.
2. Cap tool iterations explicitly (5–8 is a normal ceiling) and send the model a "you must now answer" instruction on the final pass.
3. Make the loop edge conditional too if you can, so a finished agent never reaches the tools node.
4. Trim the state between rounds — keep the last N tool results, not all of them.
5. Test the stop path deliberately before the happy path.

```python
graph.add_conditional_edges(
    "agent", should_continue, {"tools": "tools", END: END}
)
graph.add_edge("tools", "agent")   # loop, gated by should_continue only
```

**Verify**

Run a task with no possible completion and confirm the graph hits your cap and returns a partial answer rather than running until the process dies. Then run the happy path and confirm it exits early — an early exit is your proof the cap is not the only stop.

---

## Q3. The context keeps overflowing — the retriever returns 40 documents and the prompt dies. [→ Real-World Case Studies]

**What you see**

Your RAG harness works on a small test set and fails on a real one. The retriever returns the top 40 chunks, the `ChatPromptTemplate` gets them all, and the request fails or the model ignores the middle of the prompt. You never had this problem with hand-written code because you always picked 5 documents and summarized them.

**Why**

Because a retriever's job is **relevance ranking, not context budgeting**. `Chroma` returns what matches; how much of that actually fits and is useful is a separate decision. This is why `ContextualCompressionRetriever` exists and why the README maps it to `harness/02-build-context` — a distinct step between retrieval (01) and the prompt (05). Skip step 02 and retrieval output goes straight into your prompt unbounded.

**What to do**

1. Treat retrieval and context building as two different nodes in your graph, not one.
2. Compress before prompting: `ContextualCompressionRetriever` keeps the parts that answer the question and drops the rest.
3. Set an explicit document count and a token budget, and log both per query.
4. Measure whether the dropped documents were ever needed — if recall is fine, you were paying for nothing.
5. Put the retrieved documents in the prompt through `ChatPromptTemplate` with a visible boundary, so the model can tell data from instructions.

**Verify**

Log the number of documents and the token count entering the prompt for ten queries. The maximum must sit under your budget. If the p95 (95th percentile) touches the limit, compression is not working and you need a tighter budget.

---

## Q4. "Stateful graph" — where is the state actually stored, and does it survive a crash? [→ Why LangChain Matters?]

**What you see**

You assume the graph remembers everything because it is called a stateful graph. You run a long task, the process is restarted, and the graph starts from an empty state and re-does the retrieval. Nobody warned you that "stateful" and "durable" are different words.

**Why**

Because the state lives in the **checkpointer you passed in**, not in the graph. `MemorySaver` and `InMemoryChatMessageHistory` are named memory classes — both live inside the running process. When the process dies, they die with it. The graph itself only decides what the state is and where it goes next; persistence is something you add.

**What to do**

1. Know which of the two you need: within a run, `InMemoryChatMessageHistory` is enough; across runs, you need a real store.
2. Give the graph an explicit checkpointer at construction time, not a default you hope exists.
3. Store the things worth resuming — task goal, completed steps, tool results that were accepted — and drop the bulky ones.
4. Log the state size per node; a state that only grows is a state that will eventually overflow the context.
5. Test resume by killing the process mid-run and starting again from a fresh process.

**Verify**

Start a run, kill the process after three nodes, restart with the same checkpointer, and confirm it continues instead of restarting. If it restarts, your state was in memory and you never had persistence.

---

## Q5. A tool call fails and the whole graph dies — where do I even start debugging? [→ LangChain (Core)]

**What you see**

The agent calls your `search` tool, the tool throws, and the exception propagates out of the graph. You get a stack trace ending in LangGraph internals, ten frames deep, with no sign of which of your tools failed. You have no trace, only a stack.

**Why**

Because a tool in LangChain is **a function whose failure is your function's failure**. There is no default error boundary around tool execution — `ToolNode` calls your code, your code throws, and the graph has nothing to catch. Without tracing, the graph tells you where it stopped but not what your code was doing when it stopped, so you are reading a stack trace instead of reading a run.

**What to do**

1. Turn on tracing first (LangSmith, step 5 of the roadmap). A stack trace is not a trace.
2. Wrap each tool so it returns an error string instead of raising; the model can then react to the failure instead of the run dying.
3. Return errors in the same shape as successes, so the model is not confused by a missing field.
4. Log the tool name and the arguments on entry — the wrong argument is the most common cause.
5. Retry only on failures you know are transient; a retry on a bug just doubles the delay.

**Verify**

Make one tool raise on purpose and confirm the graph continues, the error text reaches the model, and the trace shows the tool name and arguments. If the run dies instead, the tool is not wrapped.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*