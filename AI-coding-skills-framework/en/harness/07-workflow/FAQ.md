# ❓ FAQ — Workflow & Micro-Kernel Plugin (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` or in `cordis-kernel-plugin.md` (same folder) — named in brackets after each question.

---

## README.md

## Q1. My agent restarted from step 1 and already deployed twice — how do I make it resume instead? [→ §13.2 Checkpoint-Resume (Across Restart)]

This section explains checkpoint-resume — saving progress so a crash does not mean starting over.

**What you see**

The process dies halfway through (killed with `kill -9` = the force-kill command that gives the process no chance to clean up, container evicted, laptop closed). You restart it and it begins again from the first step. The result: the card is charged twice, the migration runs twice, the same build is published twice — and no error message, because the agent simply starts over.

**Why**

State lives only in memory (RAM — wiped when the process dies). In the reference code the state is `self.state`, `self.context` and an in-memory `idemStore` — nothing is written to disk, so there is no "last good point" to come back to. This is the gap that two design principles close: state externalization (state stored outside memory, so you can resume from a checkpoint) and idempotency (idempotent = running a step again has no extra effect, like a "set" operation rather than "add").

**What to do**

1. Checkpoint after every step: append `{seq, stepId, inputHash, status, outputRef}` to a write-ahead log (write-ahead log = a file you append to *before* doing the work, so a crash leaves a trail), and take an atomic snapshot (atomic = written in one go, never half-finished) every N steps.
2. Give every mutating step (mutating = changes something outside itself, like a charge or a deploy) an idempotency key — `stepId + inputHash` — and store `Map<key, resultRef>` with a time-to-live (TTL = how long the record is kept). Reads do not need one.
3. On boot: load snapshot → replay the log tail → skip completed steps → resume the pending one. Keep `runId` (the run's identifier) stable across restarts.
4. Keep outputs over 64KB out of the log line — store them in an artifact store (a file/object storage) and leave only a reference.

> 📄 **Example code:** [`examples/01-q1-my-agent-restarted-from-step-1-and.ts`](examples/01-q1-my-agent-restarted-from-step-1-and.ts)

**Verify**

Kill the process mid-run, then start again with the same `runId`. The deploy step logs "already done, skipping", nothing is published twice, and `checkpoints.jsonl` contains exactly one `ok` line per step.

> **One-line summary:** Write a checkpoint log before every mutating step, make steps idempotent, and on restart replay the log instead of starting from zero.

---

## Q2. One step hangs and the whole workflow sits there forever — where is the timeout? [→ §4.2 Circuit Breaker Pattern]

This section explains deadlines — why a stuck step needs a time limit, not just an iteration count.

**What you see**

The run reaches `RUNNING_TESTS` and never comes back. No exception, no log line after the last "start" entry, memory slowly climbs as more work piles up. The state machine's `run(task, max_iterations=50)` does not help: it counts *transitions* (state changes), not time, so a single stuck step burns no iterations and the loop never trips.

**Why**

Timeouts were treated as an afterthought. `check_timeout()` only fires if you first call `sm.set_timeout(state, seconds)`, and nothing in the default orchestrator sets one. A step with no deadline of its own inherits "forever" from the service it is waiting on.

**What to do**

1. Compute one `deadlineAt` per run, once, and give every step `remaining = deadlineAt - Date.now() - 500`, passed down as `AbortSignal.timeout(remaining)` (AbortSignal = the standard way to cancel a pending operation when time runs out).
2. Never extend a deadline silently. A retry that restarts the clock hides a stuck service indefinitely.
3. Bound concurrency: one global semaphore with `maxParallel = 4–8` (semaphore = a counter that only lets N tasks run at once), a per-step queue cap around 100. `enqueue` throws `BackpressureError` when full, and the caller retries with jitter instead of letting memory grow.
4. Also set a per-state timeout so the state machine itself notices: `sm.set_timeout(AgentState.RUNNING_TESTS, 120)`.

> 📄 **Example code:** [`examples/02-q2-one-step-hangs-and-the-whole-workflow.ts`](examples/02-q2-one-step-hangs-and-the-whole-workflow.ts)

**Verify**

A step that sleeps 10 minutes under `deadlineMs = 120_000` fails in about 2 minutes with `deadline exceeded`. Submit 50 tasks to a gate with `maxParallel = 4` and confirm only 4 run at a time; the 101st enqueue throws `BackpressureError`.

> **One-line summary:** One shared deadline per run, passed to every step as an abort signal, plus a bounded queue — a stuck step fails in minutes, not never.

---

## Q3. All my agents retry at exactly the same second and I get rate-limited — is jitter the fix? [→ §4.1 Retry Strategies]

This section explains retries, jitter, and circuit breakers — the three tools for surviving a failing service.

**What you see**

200 agents call the same API. It answers `429 Too Many Requests` (the server's "slow down" reply). Every client waits exactly 1s, then 2s, then 4s — so all of them wake at the same instant and hit again at the same instant. Without a second layer, each retry still costs money and the slowness spreads into the steps behind it.

**Why**

Exponential backoff on its own synchronises clients; this is called a thundering herd (a stampede of clients all retrying at the same moment). Retry answers "this one call failed, try again". A circuit breaker answers the different question "this service is down" — it stops sending traffic altogether instead of paying for every rejection.

**What to do**

1. Add randomness to every wait: `wait = backoff_factor * 2**(attempt-1) * (0.5 + random.random())`, then cap it with `min(wait, max_backoff)` where `max_backoff = 60.0` (the randomness is the jitter).
2. Bound the attempts at `max_attempts = 3`, then raise `RetryExhausted("All 3 attempts failed. Last error: ...")` instead of looping.
3. Wrap external services in a breaker with `failure_threshold = 5` and `recovery_timeout = 30`. After 5 failures the state goes CLOSED → OPEN (CLOSED = normal traffic, OPEN = refuse calls) and every call raises `CircuitOpenError` without touching the network.
4. Let exactly one probe through when it reopens: OPEN → HALF_OPEN after 30s, `half_open_max_calls = 1`, two successes close it again.
5. Retry only transient failures — timeouts, 429, and 5xx (server errors). A malformed request will fail identically forever.

> 📄 **Example code:** [`examples/03-q3-all-my-agents-retry-at-exactly-the.py`](examples/03-q3-all-my-agents-retry-at-exactly-the.py)

**Verify**

Run 200 clients through the retry decorator and check the logged waits — no two identical. The breaker history shows `CLOSED → OPEN` at `failure_count: 5`; a call during OPEN raises `CircuitOpenError: Circuit is OPEN. Retry after Ns`; after 30s the next call succeeds and the state returns to CLOSED.

> **One-line summary:** Add random jitter to every retry, cap the attempts, and put a circuit breaker in front so a dead service gets no traffic at all.

---

## Q4. Step 3 failed but step 1 already charged the card and step 2 already sent the email — how do I undo it? [→ §4.3 Saga Pattern]

This section explains the Saga pattern — undoing completed steps when a later step fails.

**What you see**

An order flow runs ReserveInventory → ChargePayment → ShipOrder. `ShipOrder` fails. The customer is charged, stock is held, and nothing tells them. Restarting the whole flow charges them a second time.

**Why**

Retry is only safe when a step is idempotent (idempotent = safe to run twice with the same result). Charging a card and reserving stock are not, so the recovery action must be a **compensation** (compensation = a separate undo step, like a refund) — not another attempt. This is the Saga pattern, the same shape Temporal (a workflow engine) uses for durable multi-service work.

**What to do**

1. Pair every forward action with its compensation at registration time: `saga.add_step("charge", charge_card, refund_card)`.
2. On failure, run compensations in reverse order of the steps that already succeeded, and record each one.
3. Report what happened instead of raising a bare error: `failed_step`, `compensated: True`, and the compensation history.
4. If a compensation itself fails, log `compensation_failed` and alert a human. A failed undo is worse than a failed action, because now nobody knows the real state.
5. Still add idempotency keys to mutating steps, so compensation and retry can both be attempted safely.

> 📄 **Example code:** [`examples/04-q4-step-3-failed-but-step-1-already.py`](examples/04-q4-step-3-failed-but-step-1-already.py)

**Verify**

The included test `test_compensation_on_failure` fails step 2 and asserts `undo1` ran. In a live run the compensation history lists the undo of step 2 before step 1, and the refund shows up in the payment provider's own log — not just in yours.

> **One-line summary:** For steps that cannot run twice, register an undo action with each step and run the undos in reverse order when something fails.

---

## cordis-kernel-plugin.md

## Q5. I get `Service tools not found in Kernel Context` — why can't my plugin find the service? [→ cordis-kernel-plugin.md §Service Resolution]

This section explains service registration — why a plugin cannot find another plugin's service.

**What you see**

Boot fails, or the first tool call throws `Error: Service tools not found in Kernel Context`, raised from `ctx.inject('tools')` (`inject` = asking the kernel "give me the service named tools"). The same code runs fine in a colleague's project, and the plugin that defines the service is definitely in the folder.

**Why**

Nothing registers services automatically. A plugin only exists once its `apply(ctx)` has actually run, and `apply` runs only when the plugin is handed to the kernel (registered with `kernel.plugin(...)`). Order matters too: a plugin that injects before the provider's `apply` has run finds an empty registry — nothing retries for it.

**What to do**

1. Register every plugin on the kernel before anything uses it: `kernel.plugin(MCPToolPlugin)` then `kernel.plugin(LoggerPlugin)`.
2. The provider must publish inside `apply` with `ctx.provide('tools', {...})`. A module-level variable is not a service and is never visible to other plugins.
3. Depend on the service *name*, never on another plugin's import — that keeps plugins loosely coupled (loosely coupled = changeable independently).
4. Read the boot log: each registration prints `[Kernel] Mounting Plugin: mcp-tool-plugin`.
5. If the service is genuinely optional, guard the lookup and degrade, rather than throwing on a missing capability.

> 📄 **Example code:** [`examples/05-q5-i-get-service-tools-not-found-in.ts`](examples/05-q5-i-get-service-tools-not-found-in.ts)

**Verify**

Booting prints a mount line for each plugin, and `kernel.services.has('tools')` is `true` before the first `inject` call. Delete the `plugin(...)` line and confirm the error returns — that proves registration is the missing step.

> **One-line summary:** A service only exists after its plugin is registered and its `apply` runs — register first, provide inside `apply`, and depend on names, not imports.

---

## Q6. Should my feature live inside the kernel file, or as a plugin of its own? [→ cordis-kernel-plugin.md §Plugin Anatomy]

This section explains the micro-kernel split — what belongs in the core and what belongs in a plugin.

**What you see**

The kernel file has grown to 800 lines and now contains a git wrapper, a sandbox launcher, and a memory writer. Two features overwrite the same variable, nothing can be switched off alone, and no part of it can be tested without booting the whole thing.

**Why**

That is exactly the two anti-patterns the file names: a **monolithic kernel** (business logic pushed into the core instead of plugins — monolith = everything in one big block) and **global state pollution** (writing global variables instead of using `ctx.provide()`). The kernel's job stays small on purpose — lifecycle, the service registry, and events for middleware. The reference kernel is about 2KB gzipped.

**What to do**

1. One plugin, one job: `GitPlugin`, `DockerSandboxPlugin`, `MemoryPlugin`.
2. Publish with `ctx.provide(name, service)`, consume with `ctx.inject(name)`. Plugins never import each other.
3. Make every plugin removable: register cleanup with `ctx.onDispose(...)`, so `dispose()` releases the services it provided.
4. Declare `provides` and `consumes` so the kernel, not the order of lines in your file, decides load order.
5. Treat "Can I delete this plugin and still boot?" as the review question for any kernel change.

> 📄 **Example code:** [`examples/06-q6-should-my-feature-live-inside-the-kernel.ts`](examples/06-q6-should-my-feature-live-inside-the-kernel.ts)

**Verify**

The kernel file contains only `provide` / `inject` / `on` / `emit` / `plugin` and no business logic. Remove any one plugin and the rest still boot. `kernel.stop()` prints every registered dispose message, in reverse order.

> **One-line summary:** The kernel stays tiny — lifecycle, registry, events — and every feature becomes a removable, single-job plugin.

---

## Q7. My plugin works alone but breaks when I add a second one — is load order the problem? [→ cordis-kernel-plugin.md §Load Order]

This section explains plugin load order — why declared dependencies, not file order, decide what loads first.

**What you see**

With only `runtime-modes` loaded, everything runs. Add `trajectory-recorder` — which consumes `memory-store` and `event-bus` — restart, and you get `undefined` where a service should be, or a handler that never fires.

**Why**

A plugin passes through three phases: mount (`apply`), execute (listen to events), unmount (`dispose`). The kernel resolves the order from declared dependencies; when you declare none, the order is just the order you happened to write the lines in, and a consumer can attach before its provider exists.

**What to do**

1. Declare it: `consumes: ['memory-store', 'event-bus']` for soft dependencies (nice to have), and `requires: ['memory-store']` when the plugin cannot start without the other.
2. Do the real work in the attach phase, and treat `ctx.get('x')` as possibly `undefined` while you are there.
3. Register event handlers in `apply`, so listeners exist before the first event is emitted.
4. Shrink the reproduction: boot a kernel with only the two plugins. If that passes, add the third back — you have found the interaction.
5. Remember that automatic cleanup only covers what you registered. Manual listeners, open files, and child processes need their own `ctx.onDispose`.

> 📄 **Example code:** [`examples/07-q7-my-plugin-works-alone-but-breaks-when.ts`](examples/07-q7-my-plugin-works-alone-but-breaks-when.ts)

**Verify**

A two-plugin kernel prints both mount lines, and the first tool call prints the event line. Then swap the registration order, add `requires`, and confirm the failure disappears — that is your regression test.

> **One-line summary:** Declare `requires`/`consumes` so the kernel orders plugins for you, and register all listeners inside `apply`.

---

## Q8. My agent scores 62% in my own harness but 31% on SWE-bench — what am I actually measuring? [→ §7. Workflow Testing]

This section explains benchmarking modes — why your score and a public score measure different things.

**What you see**

The same model fixes 62% of tasks inside your harness and 31% on SWE-bench (SWE-bench = a public benchmark of real GitHub software bugs). Your team starts arguing about whether the model, the prompts, or the tools are at fault.

**Why**

Minimal Mode exists precisely to make that comparison honest: it opens exactly two tools (`bash` = the shell, and `editor` = file editing) and removes the whole complex system prompt, so the score reflects the model's raw reasoning. Standard Mode ships the full toolset — file system, search, git, web browser, MCP — and a long prompt. Every extra tool is another chance to pick the wrong action, and the number stops measuring the model.

**What to do**

1. Report two numbers and label them: your harness score (what users actually experience) and Minimal Mode score (what the model can do unaided). Never quote the second as the first.
2. Compare like with like — same task set, same preset, same limits on both sides.
3. Keep the benchmark harness deterministic and isolated: container isolation, exactly `bash` and `editor`, no extra prompt text.

| Mode | Tools | Isolation | Use it for |
|---|---|---|---|
| Standard | full set | process | everyday agent work |
| Code | bash, editor, llm_complete | VM sandbox | speed (70–90% less latency) |
| Benchmark | `bash`, `editor` only | container | unbiased model score |
| Creator | all, plus timeline and presets | process | debugging, preset authoring |

How to read it: each row is one of the four runtime modes. "Tools" is what the agent gets, "Isolation" is how far the run is sealed off from your machine, and "Use it for" tells you when to pick that mode. For instance, Benchmark mode strips everything down so the score measures the model, not your tooling.

4. If latency is the complaint, look at Code Mode instead: it swaps per-call JSON tool definitions for generated TypeScript/Python run through the `@deepseek-ai/dsh` SDK, batched in one round trip.

**Verify**

Run 20 tasks in Minimal Mode and check the tool list printed at boot is exactly `bash` and `editor` with no system prompt attached. Confirm switching modes requires only registering a different plugin — no code change — which is the real reason to keep these four modes separate.

> **One-line summary:** Your harness score and a benchmark score measure different things — report both, labeled, and strip the toolset down when you want to measure the model alone.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, cordis-kernel-plugin.md.*
