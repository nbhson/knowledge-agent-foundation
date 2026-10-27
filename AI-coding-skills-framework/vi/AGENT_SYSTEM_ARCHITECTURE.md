# Xây Dựng Kiến Trúc Hệ Thống Agent — Hướng Dẫn Toàn Diện 2026

> **Mục đích:** Tài liệu này trả lời câu hỏi cốt lõi nhất — **"Làm sao xây dựng một hệ thống agent hoàn chỉnh?"** — dựa trên kiến thức nền tảng đã có (`HARNESS_ENGINEERING.md`, `AI_AGENT_FRAMEWORK.md`, `GRAPH_ENGINEERING.md`) và các nghiên cứu / tài liệu chính thức mới nhất tính đến **10/2026**.
>
> **Nguồn chính (đã verify trực tiếp 10/2026):**
> - [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) (12/2024, cập nhật 2026)
> - [Effective Harnesses for Long-Running Agents — Anthropic](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) (11/2025)
> - [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (09/2025)
> - [How we built our multi-agent research system — Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) (06/2025)
> - [Agent Skills — Anthropic](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) (10/2025, open standard tại [agentskills.io](https://agentskills.io) từ 12/2025)
> - [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
> - [Model Context Protocol — MCP spec 2026-07-28](https://modelcontextprotocol.io/)
> - [A2A Protocol — Linux Foundation](https://a2a-protocol.org) (2026, đã vào Agentic AI Foundation 08/2026)

---

## Mục Lục

- [1. Bức Tranh Toàn Cảnh 2026](#1-bức-tranh-toàn-cảnh-2026)
- [2. Phân Biệt Workflow vs Agent vs Multi-Agent](#2-phân-biệt-workflow-vs-agent-vs-multi-agent)
- [3. Kiến Trúc Tổng Hợp — 8 Layer](#3-kiến-trúc-tổng-hợp--8-layer)
- [4. Các Mẫu Kiến Trúc Đã Chứng Minh Trong Production](#4-các-mẫu-kiến-trúc-đã-chứng-minh-trong-production)
- [5. So Sánh Framework & SDK Xây Dựng Agent](#5-so-sánh-framework--sdk-xây-dựng-agent)
- [6. Quy Trình Xây Dựng Thực Tế (Build Checklist)](#6-quy-trình-xây-dựng-thực-tế-build-checklist)
- [7. Kết Nối Với Framework Có Sẵn Trong Repo](#7-kết-nối-với-framework-có-sẵn-trong-repo)
- [8. Tài Liệu Tham Khảo](#8-tài-liệu-tham-khảo)

---

## 1. Bức Tranh Toàn Cảnh 2026

Điểm mấu chốt mà toàn bộ các nguồn chính thức đều khẳng định:

> **Agent = LLM tự chủ sử dụng tools trong một vòng lặp (loop).**
> Định nghĩa tối giản đang được toàn ngành hội tụ về (Anthropic, Simon Willison):
> *"An agent is an LLM autonomously using tools in a loop."*

Điều này nghĩa là: **kiến trúc hệ thống agent KHÔNG phải là chọn model giỏi nhất**, mà là thiết kế **vòng lặp + môi trường + kiểm soát** xung quanh LLM. Ba trụ cột:

```
┌────────────────────────────────────────────────────────────────┐
│                    AGENT = MODEL + HARNESS                      │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────────┐         ┌──────────────────────────────┐   │
│   │  MODEL (LLM)  │         │  HARNESS (bạn sở hữu phần này)│   │
│   │  — suy nghĩ   │◄───────►│  — tools                     │   │
│   │  — không kiểm │         │  — context management        │   │
│   │    soát được  │         │  — memory / persistence      │   │
│   └───────────────┘         │  — guardrails / permissions  │   │
│                              │  — orchestration / evaluation│   │
│                              └──────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

**Kết luận nghiên cứu quan trọng nhất (Princeton NLP — SWE-agent):** chỉ thay đổi ACI (Agent-Computer Interface) — cách thiết kế môi trường cho agent — đã tăng success rate **+64%** mà không đổi model. Khi model đã trở thành commodity (2026), **harness chính là con hào cạnh tranh**.

### Các mốc mới nhất (2024 → 10/2026)

| Thời điểm | Sự kiện | Ý nghĩa kiến trúc |
|-----------|---------|-------------------|
| 12/2024 | Anthropic — *Building Effective Agents* | Chuẩn hoá vocabulary: workflows vs agents, 5 workflow patterns |
| 12/2024 | MCP ra mắt | Chuẩn hoá agent↔tool ("USB-C cho AI") |
| 2025 | Google donate A2A cho Linux Foundation | Chuẩn hoá agent↔agent |
| 06/2025 | Anthropic multi-agent research system | Orchestrator-worker production: +90.2% vs single agent (research eval) |
| 09/2025 | Context engineering trở thành discipline chính | Compaction, note-taking, sub-agent = 3 đòn bẩy context |
| 10/2025 | Agent Skills (open standard 12/2025) | Đóng gói chuyên môn thành SKILL.md — progressive disclosure |
| 11/2025 | Anthropic — long-running agent harness | Initializer agent + coding agent; feature-list JSON; incremental progress |
| 2025–2026 | OpenAI Agents SDK v2 (Swarm → production) | Primitives: Agents, Handoffs, Guardrails, Sessions, Sandbox agents, Tracing |
| 07/2026 | MCP spec `2026-07-28` + MCP Apps | MCP ecosystem: build-once-integrate-everywhere |
| 08/2026 | A2A gia nhập **Agentic AI Foundation** (Linux Foundation) | Chuẩn hoá agent↔agent: MCP (agent→tool) + A2A (agent→agent) bổ sung nhau |

---

## 2. Phân Biệt Workflow vs Agent vs Multi-Agent

Đây là quyết định kiến trúc **số 1** — sai từ bước này thì mọi layer sau đều sai theo (Anthropic):

| Loại | Định nghĩa | Điều khiển bởi | Khi nào dùng |
|------|-----------|---------------|--------------|
| **Workflow** | LLM + tools chạy theo code path định trước | **Code của bạn** | Task cố định, cần predictability & consistency |
| **Agent** | LLM **tự điều hướng** quy trình + tool usage trong loop | **Model** | Bài toán mở, không đoán được số bước |
| **Multi-agent** | Nhiều agent (mỗi agent = LLM + tools trong loop) phối hợp | Orchestrator + model | Breadth-first, parallelizable, vượt 1 context window |

**Nguyên tắc vàng (đừng bỏ qua):**
1. Tìm giải pháp **đơn giản nhất** trước — nhiều ứng dụng chỉ cần tối ưu 1 lần gọi LLM + retrieval + few-shot.
2. Agentic systems **đánh đổi latency và cost** lấy chất lượng — chỉ thêm complexity khi đo được lợi ích.
3. Workflow cho task well-defined; agent cho bài toán open-ended cần model tự quyết.

---

## 3. Kiến Trúc Tổng Hợp — 8 Layer

Tổng hợp từ HARNESS_ENGINEERING (repo này) + các nguồn 2025–2026, một hệ thống agent hoàn chỉnh gồm **8 layer** xếp lớp như sau:

```
┌─────────────────────────────────────────────────────────────────┐
│  L8  EVALUATION & FEEDBACK   (evals, LLM-judge, regression)    │
├─────────────────────────────────────────────────────────────────┤
│  L7  SAFETY: Guardrails + Permissions + Approval + Sandbox       │
├─────────────────────────────────────────────────────────────────┤
│  L6  MEMORY: short-term / long-term / episodic / notes           │
├─────────────────────────────────────────────────────────────────┤
│  L5  ORCHESTRATION: single → orchestrator-workers → A2A mesh     │
├─────────────────────────────────────────────────────────────────┤
│  L4  TOOL ECOSYSTEM: MCP servers + Agent Skills + code execution │
├─────────────────────────────────────────────────────────────────┤
│  L3  CONTEXT ENGINEERING: assembly, compaction, just-in-time     │
├─────────────────────────────────────────────────────────────────┤
│  L2  HARNESS: retrieval → context → plan → prompt → tools →      │
│      workflow → task → eval → memory write-back (+ 12–15)        │
├─────────────────────────────────────────────────────────────────┤
│  L1  MODEL: LLM (augmented: retrieval + tools + memory)          │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1. Layer 1 — LLM với Augmentations

Đây là **nền tảng vật lý**. Không cần model "tốt nhất", cần model phù hợp:

| Model tier | Use case | Tradeoff |
|------------|----------|----------|
| Haiku 4.5 | Routing, classification, guardrails | Rẻ, nhanh, chính xác cho task đơn giản |
| Sonnet 4.5 | Coding, multi-tool, mainstream agentic | Tốt nhất cost/quality |
| Opus 4.5 | Orchestrator, complex reasoning, planning | Đắt nhưng xử lý bài toán phức tạp nhất |
| o1/o3 (OpenAI) | Hard reasoning, eval judgment | Reasoning model, không cần CoT trong prompt |

**Lưu ý quan trọng (Anthropic 09/2025):** Model càng thông minh → càng ít cần "hướng dẫn bắt buộc" → càng tự chủ được nhiều hơn. Điều này thay đổi cách thiết kế harness: với model yếu cần nhiều rules và workflow encode cứng; với frontier model chỉ cần tool tốt + guardrails.

**Augmentation = model sử dụng tích cực, không phải chỉ nhận input:**

- **Retrieval:** model tự generate search queries → call retrieval → dùng kết quả
- **Tools:** model tự quyết định dùng tool nào, khi nào
- **Memory:** model tự quyết thông tin nào đáng giữ (write-back)

### 3.2. Layer 2 — Harness (7 thành phần xung quanh LLM)

Đây là phần quan trọng nhất và đã có chi tiết trong `HARNESS_ENGINEERING.md` (repo này). Ở đây chỉ tóm tắt mapping với kiến thức mới 2025–2026:

| Thành phần | Nội dung mới (2025–2026) | Module tương ứng |
|-----------|--------------------------|-----------------|
| **Tools** | MCP chuẩn hoá; Agent Skills cho chuyên môn; Tool descriptions = docstring | `06-decide-tools-mcp/` |
| **Memory** | Note-taking (Claude Plays Pokemon); Memory tool (Anthropic Platform); Agent Skills | `01-retrieve`, `03-update`, `09-multi-agent` |
| **Context** | Compaction (tool-result clearing); 5 cấp độ context; just-in-time vs pre-computed | `02-build-context/` |
| **Guardrails** | Guardrails chạy song song với execution (không block); Risk tier ở plan time; Tool guardrails | `05-prompt-builder/`, `15-approval-gates/` |
| **Feedback** | Eval-first development; LLM-judge với rubric; production tracing | `07-workflow/`, `11-evaluation/` |
| **Permissions** | Sandbox agents (OpenAI SDK); Manifest-defined files; RBAC + Approval gates | `06`, `12-sandbox`, `15-approval` |
| **Orchestration** | Orchestrator-worker; Handoffs; A2A; async vs sync tradeoffs | `07-workflow/`, `09-multi-agent/` |

### 3.3. Layer 3 — Context Engineering

**Context rot** là hiện tượng nền tảng (Chroma research): càng nhiều token trong context window → khả năng recall chính xác càng giảm. LLM có **attention budget** hữu hạn (cấu trúc transformer: n² pairwise relationships cho n tokens).

> Nguyên tắc chỉ đạo: **"Tìm tập hợp token nhỏ nhất, signal cao nhất, tối đa hoá khả năng đạt kết quả mong muốn."**

**Ba đòn bẩy cho long-horizon tasks (Anthropic 09/2025):**

| Kỹ thuật | Cách hoạt động | Khi nào dùng |
|---------|---------------|--------------|
| **Compaction** | Tóm tắt conversation khi gần giới hạn context → khởi động context mới với summary | Task cần nhiều back-and-forth. Claude Code giữ architectural decisions + bugs + impl details, bỏ tool outputs cũ |
| **Structured note-taking** | Agent tự ghi NOTES.md / todo-list ra ngoài context window → đọc lại sau | Iterative development có milestones rõ ràng. Ví dụ: Claude Plays Pokemon duy trì map + chiến lược qua hàng nghìn steps |
| **Sub-agent architecture** | Sub-agent làm việc sâu với context riêng sạch → trả về **summary 1,000–2,000 tokens** | Research/analysis phức tạp có parallelization. Lead agent tổng hợp, sub-agent đào sâu |

**Just-in-time vs Pre-computed retrieval:**

| Chiến lược | Ưu | Nhược |
|-----------|-----|-------|
| Pre-computed (RAG truyền thống) | Nhanh, deterministic | Stale index, đắt tiền để update, chunk-level thu hẹp liên kết |
| Just-in-time (agentic search) | Fresh data, flexible, progressive disclosure | Chậm hơn, cần agent biết cách explore |
| **Hybrid (khuyến nghị)** | Fast + flexible. Claude Code: CLAUDE.md (static) + glob/grep (dynamic) | Cần thiết kế tools tốt để agent không đi lạc |

### 3.4. Layer 4 — Tool Ecosystem (MCP + Skills + Code Execution)

#### MCP — "USB-C cho AI" (spec `2026-07-28`)

MCP chuẩn hoá kết nối agent ↔ external systems (data sources, tools, workflows). Được hỗ trợ rộng rãi: Claude, ChatGPT, VS Code, Cursor, và nhiều clients khác.

```
Agent ──MCP──► Tools / APIs / Resources
```

- MCP = chuẩn hoá **agent-to-tool**
- Client kết nối tới các MCP servers (local files, DB, search engines, APIs)
- Giảm phát triển lặp: build server 1 lần → mọi MCP client dùng được

#### Agent Skills (open standard từ 12/2025)

**Skill = directory có `SKILL.md`** (YAML frontmatter: `name` + `description`) + resources kèm theo.

**Progressive disclosure 3 cấp:**

1. Metadata (`name`, `description`) — load sẵn vào system prompt lúc startup, đủ để biết *khi nào* dùng skill
2. Body của SKILL.md — chỉ load khi agent quyết skill liên quan đến task
3. Files kèm thêm (`reference.md`, `forms.md`, scripts...) — agent tự navigate theo nhu cầu

**Lợi ích:** context có thể "unbounded" vì agent chỉ load phần cần. Skills có thể kèm **scripts** — agent chạy code thay vì generate tokens (sorting list bằng code rẻ hơn nhiều lần so với dùng LLM).

#### Code execution với MCP

Anthropic (11/2025): thay vì expose hàng chục tools qua MCP (mỗi tool chiếm context + token overhead), cho agent **viết code gọi MCP tools** — code chạy trong sandbox, chỉ kết quả tổng hợp mới về context. Giảm token + latency đáng kể với nhiều MCP servers.

#### Tool design (ACI — Agent-Computer Interface)

Quy tắc từ Anthropic (SWE-bench):

- Đầu tư vào tool design **nhiều như HCI** — tool descriptions chính là "docstring cho junior dev"
- Format gần với text tự nhiên model đã học (diff khó hơn full-file rewrite; markdown dễ hơn JSON-escaped code)
- Đủ tokens để model "think" trước khi bị chính format kẹt lại
- **Poka-yoke** tools: thiết kế params để khó sai (vd: bắt buộc absolute path sau khi agent đổi thư mục)
- Test tool với nhiều inputs thật → quan sát model sai ở đâu → iterate
- Tránh bloated toolset: nếu human engineer không quyết được tool nào cho tình huống X, agent cũng không thể

### 3.5. Layer 5 — Agent Orchestration

#### Single agent → Orchestrator-workers → A2A

**Bước 1 — Single agent:** LLM + tools trong loop, đủ cho phần lớn use case.

**Bước 2 — Orchestrator-workers (multi-agent pattern phổ biến nhất):**

```
                 ┌─────────────┐
   User query ──►│ Lead agent  │──► plan + save plan to Memory
                 │ (Opus)      │
                 └──────┬──────┘
                        │ spawn
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     ┌────────┐   ┌────────┐   ┌────────┐
     │Subagent│   │Subagent│   │Subagent│   ← parallel, context riêng
     │(Sonnet)│   │(Sonnet)│   │(Sonnet)│   ← interleaved thinking
     └───┬────┘   └───┬────┘   └───┬────┘
         └────────────┼────────────┘
                      ▼
              Lead synthesizes
                      ▼
              CitationAgent (nếu cần)
                      ▼
              Answer + citations
```

**Số liệu thực tế (Anthropic 06/2025):**
- Multi-agent (Opus lead + Sonnet subagents) **+90.2%** vs single-agent Opus 4 trên research eval
- Token usage giải thích **80% variance** hiệu năng trên BrowseComp
- **Chi phí:** chat thường 1×; agent đơn ~4×; multi-agent ~15× tokens
- Multi-agent chỉ đáng tiền khi: task giá trị cao, parallelizable, vượt 1 context window, nhiều tools phức tạp
- **KHÔNG phù hợp:** coding (ít parallelizable thật sự), task cần shared context chặt, real-time coordination (LLM còn kém)

**Prompt engineering cho multi-agent (8 nguyên tắc Anthropic):**

1. **Think like your agents** — simulate từng step, xem failure modes thật
2. **Teach the orchestrator how to delegate** — mỗi subtask cần: objective + output format + tool guidance + task boundaries. Instruction mơ hồ → subagents duplicate work
3. **Scale effort to query complexity** — embed rules: fact-finding = 1 agent/3–10 tool calls; comparison = 2–4 subagents/10–15 calls; complex research = 10+ subagents
4. **Tool design and selection are critical** — heuristic rõ: examine all tools first, match tool to intent, prefer specialized over generic
5. **Let agents improve themselves** — Claude 4 có thể tự viết lại tool descriptions; tool-testing agent giúp giảm 40% task completion time
6. **Start wide, then narrow down** — prompt agents chống lại xu hướng query dài + cụ thể quá sớm
7. **Guide the thinking process** — extended thinking = controllable scratchpad; interleaved thinking sau mỗi tool result
8. **Parallel tool calling** — 3–5 subagents parallel + 3+ tools parallel mỗi subagent → giảm tới 90% research time

**Bước 3 — A2A Protocol (agent↔agent, Linux Foundation 2026):**

- **MCP** = agent→tool; **A2A** = agent→agent. Bổ sung, không cạnh tranh.
- A2A cho phép agents ở **khác framework/vendor** (LangGraph, CrewAI, ADK, custom) discover + delegate + share results — mà **không chia sẻ memory/tools/logic nội bộ** (opaque, secure).
- SDK chính thức: Python, JS, Java, .NET, Go, Rust + A2A CLI (10/2026).
- A2A **không phải**: development kit, sub-agent protocol (sub-agent trong 1 hệ thống dùng native primitives), hay thay thế MCP.

**Sync vs async:** Anthropic hiện chạy subagents **synchronously** (lead đợi subagents xong). Đơn giản nhưng tạo bottleneck (lead không steer được subagent giữa chừng). Async cho phép parallelism cao hơn nhưng phức tạp hơn nhiều về result coordination + state consistency + error propagation.

### 3.6. Layer 6 — Memory Architecture

Hệ thống memory cho agent production cần 3 loại:

| Loại | Ví dụ | Cơ chế | Đặc điểm |
|------|-------|--------|----------|
| **Short-term (working)** | Message history, current context | Trong context window | Bị clear khi context đầy |
| **Session** | Memory tool (Anthropic Platform) | File-based, persistent across turns | Cho phép agent nhớ giữa các summarization |
| **Long-term (knowledge)** | Vector DB + Graph DB + Agent Skills | Chunk-based + structured | Cần retrieval, consolidation, versioning |

**Memory pattern đã chứng minh hiệu quả:**

```
Claude Code Memory flow:
1. Agent viết NOTES.md khi làm task
2. Task dài → context compaction (tóm tắt + giữ 5 files gần nhất)
3. Session mới → agent đọc NOTES.md + git log + CLAUDE.md → lấy bearings
4. NOTES.md + CLAUDE.md + feature_list.json = persistent context
```

**Event sourcing cho memory (repo này — `03-update-memory-store/`):**
Mỗi lần agent hoàn thành task → phát ra `TrajectoryEvent` (append-only) → sau đó chạy consolidation/compaction → giữ facts đáng giá, bỏ noise.

### 3.7. Layer 7 — Safety, Guardrails & Permissions

**Ba mặt của safety cần xử lý đồng thời:**

| Mặt | Nội dung | Cơ chế |
|-----|----------|--------|
| **Input guardrails** | Prompt injection, content filter, rate limiting | Run trước khi prompt đến LLM |
| **Output guardrails** | Sensitive data leak, toxicity, quality check | Run sau khi nhận output từ LLM |
| **Behavioral guardrails** | Max iterations, timeout, allowed domains, forbidden actions | Run song song với execution |

**Guardrails chạy song song, không block (OpenAI SDK 2026):**
- Guardrails check đồng thời khi agent chạy
- Nếu guardrail fail → fail-fast ngay (không đợi hết loop)
- Nhiều guardrails chạy song song, mỗi cái kiểm tra 1 khía cạnh

**Approval gates (Anthropic long-running agent research):**

```
Task có risk → risk tier (từ plan time, Module 15)
    → User nhận gate payload (mô tả hành động + hậu quả)
    → User approve / reject / modify
    → Timeout-deny (không phản hồi = tự động từ chối)
    → Audit trail ghi lại phán quyết
```

**Sandbox execution:**
- OpenAI Agents SDK có **Sandbox agents**: manifest-defined files + sandbox clients + resumable sandbox sessions
- Repo này có `12-sandbox-execution/` — threat model, blast radius, 5 controls bắt buộc
- Agent SkillsSecurity: chỉ cài skills từ trusted sources; audit kỹ code dependencies + external network calls trong skill

### 3.8. Layer 8 — Evaluation & Feedback

**Nguyên tắc eval-first (Anthropic multi-agent 06/2025):**
- **Bắt đầu eval ngay với sample nhỏ** — 20 queries là đủ thấy tác động của thay đổi lớn (30% → 80%)
- **LLM-as-judge** với rubric: factual accuracy, citation accuracy, completeness, source quality, tool efficiency. 1 LLM call, 1 prompt, score 0.0–1.0 + pass/fail — đơn giản nhất mà align nhất với human judgement
- **Human evaluation bắt edge cases** mà evals bỏ sót — vd: SEO content farms được chọn hơn academic sources
- **End-state evaluation** cho agent mutate state: đánh giá **trạng thái cuối** thay vì từng step — vì agents có thể tìm đúng kết quả bằng nhiều paths khác nhau

**Production reliability (bài học production từ Anthropic Research):**
- Agents are **stateful** — lỗi nhỏ compounding thành disaster. Không restart từ đầu; **resume từ checkpoint**
- **Rainbow deployments** — chuyển traffic dần từ version cũ → mới, giữ cả 2 chạy song song, vì agents có thể đang chạy giữa chừng khi deploy
- **Production tracing** — quan sát decision patterns + interaction structures (không nội dung conversation) để debug root cause

---

## 4. Các Mẫu Kiến Trúc Đã Chứng Minh Trong Production

### 4.1. Single Agent (Minimal) — "Đủ cho phần lớn use case"

```
User → [Retrieval → Context → Prompt → LLM → Tools (MCP) → Result] → User
       ↑                                          │
       └──────────────────────────────────────────┘ (loop cho tới stop condition)
```

**Khi nào đủ:**
- Task ngắn, well-defined steps
- Chỉ cần 1–2 tools
- Độ phức tạp thấp

**Minimal stack:** LLM API + MCP servers + Session memory + basic guardrails.

### 4.2. Orchestrator-Workers (Multi-Agent)

Phổ biến nhất trong production, phù hợp:
- Coding products (sửa nhiều files, mỗi file nature khác nhau)
- Search/analysis (nhiều nguồn độc lập)
- Customer support (qualify → resolve → escalate)

**Anti-pattern phổ biến:** spawn 50 subagents cho query đơn giản. Fix: scale effort to query complexity (section 3.5 nguyên tắc 3).

### 4.3. Long-Running Agent (Initializer + Coding Agent)

Từ Anthropic 11/2025, dùng cho task kéo dài nhiều context windows:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LONG-RUNNING AGENT ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Session 1: Initializer Agent                                      │
│  ─────────────────────────────────────────────────────────────     │
│  User prompt → Analyze requirements                                │
│           → Write feature_list.json (200+ features, JSON, all     │
│             marked "passes: false")                                │
│           → Write init.sh (run dev server)                         │
│           → Create git repo + initial commit                       │
│           → Write claude-progress.txt (initial state)             │
│                                                                     │
│  Session N (N >= 2): Coding Agent (mỗi session chạy 1 feature)      │
│  ─────────────────────────────────────────────────────────────     │
│  1. Run pwd (xác định working directory)                           │
│  2. Read claude-progress.txt + git log (lấy bearings)              │
│  3. Read feature_list.json → chọn feature chưa done                │
│  4. Read init.sh → chạy dev server                                │
│  5. Test basic features (puppeteer MCP) → verify không có bug mới   │
│  6. Implement 1 feature                                          │
│  7. Test end-to-end (browser automation)                           │
│  8. Mark feature as "passes: true"                                │
│  9. git commit + update claude-progress.txt                       │
│  10. Exit (context window reset)                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Bài học:** Claude có 2 failure modes chính:
- "One-shot" app (cố làm tất cả 1 lần) → context overflow → phải đoán gì đã xảy ra
- "Declare victory prematurely" sau khi thấy vài features đã làm

**Fix = 3 cơ chế:**
- Feature list JSON (không sửa/remove tests = unacceptable)
- Incremental progress (1 feature mỗi session)
- Structured cleanup (git commit + progress notes cuối mỗi session)

### 4.4. Multi-Agent Research System

Dành cho bài toán mở, breadth-first, nhiều directions độc lập:

```
User query → LeadResearcher (Opus 4.5)
    ├── Thinking (extended) → save plan to Memory
    ├── Spawn Subagent A (Sonnet) → search "aspect 1"
    ├── Spawn Subagent B (Sonnet) → search "aspect 2"
    ├── Spawn Subagent C (Sonnet) → search "aspect 3"
    │   (each subagent: interleaved thinking after each tool result)
    │
    Lead synthesizes → decide if more research needed
        ├── If yes → spawn more subagents or refine
        └── If no → CitationAgent (process docs → cite sources)
                         ↓
                   Final answer + citations
```

**Token economics:** multi-agent ~15× tokens vs chat thường. Chỉ dùng khi task value đủ cao để trả.

### 4.5. Hybrid Retrieval → Agent (RAG + Agent)

```
Query → [Hybrid Search] → [Context Assembly] → [Agent Loop] → Answer
              ↑                    ↑
         Vector DB          + Prompt + Memory
         + Graph DB         + Tools
```

**Điểm mới 2026:** thay vì pre-compute tất cả context trước → kết hợp **just-in-time retrieval** (agent chủ động explore) + static CLAUDE.md. Claude Code dùng pattern này: CLAUDE.md dropped vào context upfront; glob/grep cho progressive disclosure.

---

## 5. So Sánh Framework & SDK Xây Dựng Agent

| Tiêu chí | Claude Agent SDK | OpenAI Agents SDK | LangGraph | CrewAI | ADK (Google) | Strands (AWS) |
|----------|-----------------|-------------------|-----------|--------|-------------|--------------|
| **Maturity** | Stable (Anthropic) | Production (OpenAI) | Very mature | Mature | GA (Google) | Stable (AWS) |
| **Primitives** | Agent + tools + MCP + memory | Agents + handoffs + guardrails + sessions + sandbox | Graph state machine + nodes/edges | Agent + crew + process | Agent + tool + task | Agent + tools |
| **Multi-agent** | Handoffs / sub-agents | Handoffs (chính); multi-agent orchestration | Native DAG/HSM | Native Crew (roles + sequential/parallel) | Native (TaskGraph) | Built-in |
| **Context management** | Compaction + memory tool | Sessions (SQLite, Redis, MongoDB, Dapr) | Manual | Manual | Manual | Manual |
| **MCP** | Native | Native MCP server manager | Native | Via LangChain MCP | Via extensions | Via integrations |
| **A2A** | Via custom | Via custom | Via LangGraph A2A nodes | Via custom | Via ADK A2A | Via custom |
| **Sandbox** | Via code execution | **Sandbox agents** (workspace isolation, manifest, resumable) | Via LangChain | Via custom | Via Vertex AI | Via AWS |
| **Tracing** | Console tracing | Built-in + OpenAI eval/fine-tune | LangSmith | Weights & Biases | Vertex AI | CloudWatch |
| **Guardrails** | Input/output validation | Guardrails (parallel, fast-fail) | Via LangChain LCEL | Via code | Via decorators | Via config |
| **Điểm mạnh** | Frontier model integration, Skills | Simple primitives, sandbox agents, 3 loại agents (text/voice/realtime) | Full flexibility, production-tested | Fast prototyping | Google ecosystem | AWS ecosystem |
| **Điểm yếu** | Vendor lock-in | Chủ yếu OpenAI models | Phức tạp cho task đơn giản | ít control low-level | GCP only | AWS only |
| **Khuyến nghị** | Dùng Claude model; cần frontier quality | Dùng OpenAI; cần sandbox + handoffs | Muốn full control; workflow phức tạp | Prototype nhanh; team nhỏ | Google Cloud; Vertex AI | AWS; Bedrock |

**Lời khuyên từ Anthropic:** Bắt đầu với LLM API trực tiếp — nhiều patterns chỉ cần vài dòng code. Dùng framework khi hiểu rõ underlying code; sai assumption về abstraction là nguồn lỗi phổ biến nhất.

**MCP + A2A = combo chuẩn hoá (2026):**

```
Agent (bất kỳ framework nào)
    ├── MCP client ──► MCP servers (tools, data, APIs)
    └── A2A client ──► A2A servers (other agents)

A2A và MCP giải quyết 2 bài toán KHÁC nhau, bổ sung nhau.
MCP: "agent cần làm gì" (tools/resources)
A2A: "agent cần trao đổi với ai" (collaboration, handoffs)
```

---

## 6. Quy Trình Xây Dựng Thực Tế (Build Checklist)

### Phase 1: Xác định yêu cầu kiến trúc

- [ ] Task có well-defined steps không? → dùng **workflow** (không cần agent)
- [ ] Cần bao nhiêu model tiers? → chỉ cần Sonnet cho task thường; dùng Opus cho orchestrator
- [ ] Token budget cho phép multi-agent? → budget đủ → multi-agent; không → single agent
- [ ] Task chạy bao lâu? → < 1 session → simple; nhiều context windows → long-running pattern

### Phase 2: Thiết kế Layer 1–2 (Model + Tools)

- [ ] Chọn model tiers phù hợp với task complexity
- [ ] Danh sách tools — tối thiểu nhưng đủ chức năng (nếu human không phân biệt được tool X vs Y → tách ra)
- [ ] Viết tool descriptions như docstring cho junior dev (name + description + examples + edge cases + boundaries)
- [ ] Triển khai MCP servers cho external tools (build-once, use everywhere)
- [ ] Đăng ký tools vào MCP manager / registry

### Phase 3: Thiết kế Layer 3 (Context Engineering)

- [ ] Chọn retrieval strategy: pre-computed (RAG), just-in-time, hay hybrid
- [ ] Thiết lập context budget (token limit mỗi turn)
- [ ] Triển khai compaction (trigger ở ~70% capacity, không đợi 90%)
- [ ] Quyết định memory layer: file-based (NOTES.md), database (SQLite/Redis), hay vector
- [ ] Nếu dùng Agent Skills: thiết kế SKILL.md với progressive disclosure

### Phase 4: Thiết kế Layer 4–5 (Orchestration + Multi-agent)

- [ ] Single agent đủ? → implement loop đơn giản
- [ ] Cần multi-agent? → thiết kế orchestrator-worker pattern:
  - [ ] Mỗi subagent: specialized prompt + output format + task boundaries
  - [ ] Effort scaling rules trong prompt (fact-finding vs research vs complex)
  - [ ] Parallelization: 3–5 subagents + mỗi subagent 3+ tools parallel
  - [ ] Extended thinking cho lead; interleaved thinking cho subagents
- [ ] Cần A2A? → thiết kế task handoff, shared results, không shared memory

### Phase 5: Safety & Guardrails

- [ ] Input guardrail: prompt injection detection + content filter
- [ ] Output guardrail: sensitive data + quality check
- [ ] Behavioral guardrail: max iterations + timeout + allowed domains
- [ ] Risk tier: gắn khi plan (04), gate payload cho human, timeout-deny
- [ ] Sandbox: isolation tier (language → container → syscall filter)
- [ ] Rainbow deployment cho production agents (giữ cả 2 versions chạy song song)

### Phase 6: Evaluation

- [ ] Bắt đầu eval ngay với 20 test cases nhỏ
- [ ] LLM-as-judge với rubric: accuracy + completeness + tool efficiency + source quality
- [ ] Human evaluation để catch edge cases
- [ ] End-state eval cho agent mutate state (check final state, không từng step)
- [ ] Regression test sau mỗi deploy

### Phase 7: Observability & Debugging

- [ ] Production tracing: agent decision patterns, interaction structures (không nội dung)
- [ ] Session-level event log (TrajectoryEvent: append-only)
- [ ] Error recovery: checkpoint + resume (không restart from scratch)
- [ ] Metrics: success rate, avg response time, token usage, error types

---

## 7. Kết Nối Với Framework Có Sẵn Trong Repo

Document này là **tổng hợp và cập nhật** — không thay thế, mà bổ sung các tài liệu đã có:

| File trong repo | Vai trò | Kết nối với tài liệu này |
|----------------|---------|--------------------------|
| `AI_AGENT_FRAMEWORK.md` | Bản đồ toàn cục 15 modules + 6 phases | Đây là "tổng quan"; architecture này = cách xây cụ thể |
| `HARNESS_ENGINEERING.md` | 7 components của harness, 10 commandments, case studies | Layer 2 của kiến trúc này = phần triển khai của harness |
| `GRAPH_ENGINEERING.md` | Knowledge graph cho AI agents | Bổ sung Layer 1 (RAG/Retrieval) — Graph không thay thế Vector, kết hợp |
| `loop/01-concepts/` → `loop/07-tools/` | Loop Engineering — vòng lặp tự duy trì | Layer 5 (Orchestration) dùng loop patterns cho single + multi-agent |
| `harness/01-retrieve-memory-knowledge/` | Retrieve Memory | Layer 3 (Context) bắt đầu từ retrieval |
| `harness/03-update-memory-store/` | Write-back + Event sourcing + Trajectory | Layer 6 (Memory) của kiến trúc này |
| `harness/06-decide-tools-mcp/` | Tool selection + MCP + ACI design | Layer 4 (Tool Ecosystem) dựa trên module này |
| `harness/07-workflow/` | Pipeline design, state machine, error recovery | Layer 5 (Orchestration) dùng workflow patterns |
| `harness/09-multi-agent/` | Agent roles, communication, shared memory | Layer 5 (Orchestration) + A2A section bổ sung protocol mới |
| `harness/11-evaluation/` | Rubric, benchmarks, LLM-judge | Layer 8 (Evaluation) của kiến trúc này |
| `harness/12-sandbox-execution/` | Sandboxing + threat model | Layer 7 (Safety) dùng cơ chế sandbox này |
| `harness/13-trajectory-observability/` | Event stream, join keys, retention | Observability phần của Phase 7 checklist |
| `harness/14-compaction-context/` | Compaction trigger, pin set, summarization | Layer 3 (Context Engineering) dùng trực tiếp |
| `harness/15-approval-gates/` | Risk tier, gate payload, audit | Layer 7 (Safety) dùng trực tiếp |

**Sơ đồ mối quan hệ:**

```
AGENT_SYSTEM_ARCHITECTURE.md (tổng hợp + cập nhật 2026)
    │
    ├── HARNESS_ENGINEERING.md → Layer 2 (Harness 7 components)
    ├── GRAPH_ENGINEERING.md  → Layer 1 supplement (Graph + Vector)
    ├── AI_AGENT_FRAMEWORK.md → Phase map (01-15 modules)
    │
    └── loop/ + harness/ + graph/
        → Chi tiết từng module phía dưới
        → 12-15 = cross-cutting (safety, obs, context, approvals)
```

---

## 8. Tài Liệu Tham Khảo

### Nghiên cứu chính thức (2024–2026, đã verify trực tiếp)

| Nguồn | Năm | Chủ đề |
|-------|-----|--------|
| [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | 12/2024 | Workflows vs agents, 5 workflow patterns, ACI design |
| [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 09/2025 | Context rot, compaction, note-taking, sub-agent architectures |
| [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 06/2025 | Orchestrator-worker production: +90.2% vs single agent, 8 prompting principles |
| [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | 11/2025 | Initializer + coding agent, feature list JSON, incremental progress |
| [Agent Skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) | 10/2025 | SKILL.md format, progressive disclosure 3 levels, open standard |
| [Code Execution with MCP](https://www.anthropic.com/research/code-execution-with-mcp) | 11/2025 | Thay vì expose nhiều tools, agent viết code gọi MCP |
| [Claude Managed Agents](https://www.anthropic.com/engineering/managed-agents) | 2026 | Production managed agent infrastructure |

### Nguồn gốc kiến trúc (trong repo này)

- `HARNESS_ENGINEERING.md` — 7 components, SOLID, 10 commandments, case studies
- `GRAPH_ENGINEERING.md` — Knowledge graph cho AI agents, GraphRAG, 9 modules
- `AI_AGENT_FRAMEWORK.md` — 15 modules, 6 phases, 27 project ideas
- `harness/ARCHITECTURE.md` — Kiến trúc tổng harness, 3 contracts chia sẻ
- `loop/` — Loop Engineering: concepts, patterns, safety, anti-patterns
- `harness/09-multi-agent/SUBAGENT.md` — Sub-agent spec: lifecycle, spawn, budget
- `harness/03-update-memory-store/trajectory-fork-replay.md` — Event stream, fork/replay/resume
- `harness/11-evaluation/minimal-benchmark-harness.md` — Eval harness isolation

### Protocols & Standards

| Protocol | Năm | Mục đích |
|---------|-----|---------|
| [MCP spec 2026-07-28](https://modelcontextprotocol.io/) | 2024-2026 | Agent→tool: chuẩn hoá tools, data, resources |
| [A2A Protocol](https://a2a-protocol.org) | 2026 | Agent→agent: handoff, delegation, collaboration |
| [Agent Skills (open standard)](https://agentskills.io/) | 12/2025 | SKILL.md: đóng gói chuyên môn cho agents |
| DeepLearning.AI — [Intro to A2A](https://goo.gle/dlai-a2a) | 2026 | Course giới thiệu A2A protocol |

### SDKs & Frameworks

| SDK | Điểm mạnh |
|-----|----------|
| [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) | Frontier models, Skills, long-running |
| [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | Sandbox agents, handoffs, sessions, guardrails, tracing |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Full flexibility, state machine, production |
| [CrewAI](https://docs.crewai.com/) | Fast prototyping, roles + processes |
| [Google ADK](https://adk.dev/) | Google ecosystem, Vertex AI |
| [AWS Strands](https://strandsagents.com/latest/) | AWS + Bedrock ecosystem |

### Blogs & Key Principles

- **"Agents" — Simon Willison** (2025): định nghĩa đang hội tụ: *"LLMs autonomously using tools in a loop"*
- **"Context rot" — Chroma Research**: attention budget giảm khi context tăng
- **Harness Engineering quote — Mitchell Hashimoto**: *"Mỗi khi agent mắc lỗi, bạn không cầu nguyện — bạn xây giải pháp hệ thống"*
- **Agentic AI Foundation (Linux Foundation)**: MCP + A2A governance + open standards

---

*Bài viết thuộc [AI Coding Skills Framework](./AI_AGENT_FRAMEWORK.md) — Agent System Architecture Track*

<!-- BUILD-DONE -->
