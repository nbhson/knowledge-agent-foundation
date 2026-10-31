# 🧠 Memory & Context trong AI — Hướng Dẫn Học Tập

> **Framework này giúp bạn TỰ TAY XÂY AI AGENT** — từ thiết kế bộ nhớ, xử lý context, lập kế hoạch, phối hợp nhiều agent, cho tới tự động hoá và đánh giá. Đây không phải kiểu hướng dẫn dùng AI thông thường đâu nhé.

---

## 🎯 Đối Tượng

> **Cách đọc bảng này:** cột **Nhóm** là nghề của bạn; cột **Mục đích** là bạn sẽ dùng framework đó để làm gì.
> Ví dụ: nếu bạn là Backend Developer, hãy đọc kỹ các phần về LLM và RAG (tìm kiếm tri thức).
> "LLM" = Large Language Model, tức mô hình ngôn ngữ lớn như GPT, Claude. "RAG" = Retrieval-Augmented Generation,
> tức cách cho AI tra cứu tài liệu trước khi trả lời.

| Nhóm | Mục đích |
|------|----------|
| **AI Engineers** | Thiết kế và triển khai AI Agent systems |
| **Backend Developers** | Tích hợp LLM + RAG vào ứng dụng |
| **DevOps / SRE** | Triển khai và monitor AI pipelines |
| **Tech Leads** | Đánh giá và chọn kiến trúc AI phù hợp |
| **Researchers** | Tham khảo pattern và best practices |

> **Tóm gọn 1 câu:** Ai cũng học được — từ kỹ sư AI tới DevOps — tùy vai trò mà bạn tập trung vào phần khác nhau.

## 📋 Tiên Quyết

> **Cách đọc bảng này:** cột **Kiến thức** là những gì bạn cần biết trước; cột **Mức độ** cho biết cần sâu đến đâu
> (Cơ bản = biết khái niệm là đủ); cột **Ghi chú** giải thích vì sao cần.
> Ví dụ: bạn không cần giỏi Python — chỉ cần đọc hiểu code và chạy được script.

| Kiến thức | Mức độ | Ghi chú |
|-----------|--------|---------|
| Python | Cơ bản → Trung bình | Ngôn ngữ chính của framework |
| LLM Concepts | Cơ bản | Transformer, Token, Prompt |
| REST API | Cơ bản | Giao tiếp với Ollama, MCP servers |
| Git | Cơ bản | Quản lý code và automation |

> **Giải nghĩa nhanh:** *Token* = đơn vị nhỏ nhất mà AI đọc được, khoảng một từ hoặc vài ký tự.
> *Prompt* = câu lệnh/dối thoại bạn đưa cho AI. *REST API* = cách hai phần mềm gọi nhau qua HTTP.
> *Ollama* = phần mềm chạy AI ngay trên máy bạn, miễn phí. *MCP server* = "cổng cắm tool" chuẩn để agent gọi công cụ bên ngoài.

> **Tóm gọn 1 câu:** Bạn chỉ cần Python cơ bản + khái niệm LLM là đủ bắt đầu — phần còn lại framework sẽ dạy dần.

## 🛠️ Cách Sử Dụng

Phần này nói về **cách bắt đầu dùng framework**: cài gì trước, học theo thứ tự nào, và thực hành ra sao.

### Bước 1: Cài đặt môi trường

<details>
<summary><b>Bước 1: Cài đặt môi trường (Click to expand/collapse)</b></summary>


> 📄 **Code ví dụ:** [`examples/01-buoc-1-cai-at-moi-truong.sh`](examples/01-buoc-1-cai-at-moi-truong.sh)

> **Ghi chú Oct-2026.** Hai dòng `ollama pull` trên chỉ là ví dụ hồi Jul-2026 thôi,
> bạn đổi model khác vẫn chạy đúng pattern. (`ollama pull` = tải model AI về máy,
> ví dụ `ollama pull gemma3:12b` tải model Gemma kích thước 12 tỷ tham số.)
> Một số lựa chọn mới:
> `qwen3.6`, `deepseek-v4-flash/pro (context tới 1M)`, `gemma4 26B-A4B`, `gpt-oss:20b/120b (nhẹ nhờ MXFP4)`,
> `muse-glimmer 30b`, `minimax-m3`, `glm-5.2`, `granite4.2`. Nhớ dùng Ollama bản mới (>=0.6) nhé.
> (MXFP4 = định dạng nén số 4-bit, giúp model chạy nhẹ hơn trên máy thường.)

</details>

> **Tóm gọn 1 câu:** Bước 1 chỉ là chạy script cài Ollama và tải một model về máy — file cài mẫu nằm trong examples/.

### Bước 2: Học theo lộ trình
Bắt đầu từ **Phase 1** (Core Skills) rồi học dần lên **Phase 6** (Evaluation) nhé. ("Phase" = giai đoạn.)
Mỗi module đều có README riêng kèm code mẫu để bạn vừa đọc vừa làm theo. (README = file giới thiệu đi kèm thư mục.)

> **Tóm gọn 1 câu:** Học theo thứ tự Phase 1 → 6, mỗi module đều có hướng dẫn và code đi kèm.

### Bước 3: Thực hành
- Clone repo về rồi chạy thử code mẫu trong từng module nhé ("clone" = tải bản sao repo về máy)
- Thử chỉnh parameters xem kết quả thay đổi ra sao ("parameters" = các thông số cấu hình, ví dụ nhiệt độ sinh câu chữ)
- Cuối cùng ghép các module lại với nhau thành một pipeline hoàn chỉnh ("pipeline" = chuỗi bước nối tiếp nhau)

> **Tóm gọn 1 câu:** Chạy code mẫu, chỉnh thông số xem kết quả đổi ra sao, rồi ghép các module thành pipeline hoàn chỉnh.

> **Tóm gọn 1 câu:** Cài Ollama + model, học tuần tự Phase 1 → 6, rồi tự tay chạy và chỉnh code mẫu ở từng module.

## ⚡ Quick Reference

> **Cách đọc bảng này:** cột trái là **cái bạn muốn làm**, cột phải là **module cần học** (bấm link để nhảy tới).
> Ví dụ: muốn AI tìm thông tin trong docs hay database → học module 01 "Retrieve Memory".
> "Module" = một bài học độc lập kèm code. "Context window" = bộ nhớ tạm AI đọc được trong một lần trả lời.

| Bạn muốn... | Học module |
|-------------|------------|
| Tìm kiếm thông tin từ docs/database | [01 - Retrieve Memory](#part-i-retrieve-memory--knowledge) |
| Quản lý context window của LLM | [02 - Build Context](#part-ii-build-context) |
| Lưu trữ knowledge mới | [03 - Update Memory Store](#part-iii-update-memory--knowledge-store) |
| Phân task và lên kế hoạch | [04 - Plan & Decompose](#part-iv-plan--decompose-task) |
| Viết prompt hiệu quả | [05 - Prompt Builder](#part-v-prompt-builder) |
| Chọn và gọi tools (MCP) | [06 - Decide Tools / MCP](#part-vi-decide-tools--mcp-calls) |
| Tổ chức workflow tự động | [07 - Workflow](#part-vii-workflow) |
| Quản lý task tracking | [08 - Task Management](#part-viii-task-management) |
| Phối hợp nhiều agents | [09 - Multi-Agent](#part-ix-multi-agent-systems) |
| Tự động hóa CI/CD, Git | [10 - Automation](#part-x-automation) |
| Đánh giá hiệu quả | [11 - Evaluation](#part-xi-evaluation) |
| Cách ly thực thi code không tin cậy | [12 - Sandbox Execution](#mặt-phẳng-kiểm-soát-harness-modules-1215) |
| Debug/replay một run sau khi xảy ra | [13 - Trajectory & Observability](#mặt-phẳng-kiểm-soát-harness-modules-1215) |
| Giữ cửa sổ context có giới hạn | [14 - Compaction & Context](#mặt-phẳng-kiểm-soát-harness-modules-1215) |
| Gate thao tác không đảo ngược cho con người | [15 - Approval Gates](#mặt-phẳng-kiểm-soát-harness-modules-1215) |
| **Xây kiến trúc hệ thống agent hoàn chỉnh (8 Layer)** | [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md) |

> **Ghi chú về đánh số.** Module harness là `01`–`15`. ("Harness" = khung vận hành bọc quanh model:
> lo chạy code, gọi tool, ghi log, xin phép — mọi thứ ngoài việc "suy nghĩ".)
> Nhãn `Part` bên dưới (`Part I` … `Part XIII`) đánh số *các phần của framework*, là namespace khác —
> (namespace = "hệ thống đánh số khác", như số nhà và số CCCD cùng chỉ một người)
> đó là lý do `Part XII` là Loop Engineering và `Part XIII` là Graph Engineering,
> trong khi module harness `12` là Sandbox Execution. (Sandbox = "chuồng nhốt" cách ly code khi chạy thử.)
> Loop Engineering nằm ở thư mục `loop/` cấp cao nhất, không nằm trong `harness/`.

> **Tóm gọn 1 câu:** Bảng tra nhanh này cho bạn biết "muốn làm X thì học module nào" — và đừng nhầm số module (01–15) với số Part (I–XIII).

### Giao thức & SDK chuẩn (2026)

> **Mục này nói gì:** các "chuẩn giao tiếp" mà các agent năm 2026 dùng để nói chuyện với tool,
> với nhau, và để đóng gói kỹ năng. Biết 5 cái tên dưới đây là đủ đọc hiểu phần còn lại.

> **Tóm tắt nhanh (chi tiết ở [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md)):**
> - **MCP** (Model Context Protocol, spec `2026-07-28`) — agent↔tool. Mọi module gọi tool nên đi qua MCP.
>   (Nói đơn giản: MCP là "ổ cắm điện chuẩn" — agent cắm tool nào vào cũng chạy, không cần code riêng từng tool.)
> - **A2A** (Agent-to-Agent, Linux Foundation — Google ra mắt 04/2025, donate 06/2025) — agent↔agent, bổ sung cho MCP.
>   (MCP nối agent với tool; A2A nối agent với agent.)
> - **Agent Skills** (open standard 12/2025, [agentskills.io](https://agentskills.io)) — đóng gói chuyên môn thành SKILL.md.
>   (Tức là gói kiến thức nghề nghiệp thành 1 file mô tả để agent đọc và "biện" thêm kỹ năng.)
> - **SDK chính thống**: Claude Agent SDK (trước đây là Claude Code SDK), OpenAI Agents SDK, Google ADK (GA 04/2025), LangGraph, CrewAI, AWS Strands.
>   (SDK = bộ thư viện chính thức giúp bạn code nhanh; GA = General Availability, tức phát hành chính thức.)
> - **GraphRAG 2026**: LazyGraphRAG + LightRAG giảm chi phí ~700× so với GraphRAG gốc (chi tiết ở [GRAPH_ENGINEERING.md](GRAPH_ENGINEERING.md) và `graph/05-graph-rag/`).
>   (GraphRAG = cho AI tra cứu theo "sơ đồ quan hệ" thay vì chỉ tìm văn bản thô.)

> **Tóm gọn 1 câu:** MCP là chuẩn để agent gọi tool, A2A là chuẩn để agent nói chuyện với nhau, Agent Skills là cách đóng gói chuyên môn — biết 3 tên này là đủ.

---

## Cấu Trúc Học Tập

> **Đọc cây này thế nào:** đây là bản đồ thư mục của framework. Số `01`–`15` là module harness
> (mỗi module = 1 bài học kèm code), arrow `←` là chú thích ngắn. Ba nhóm chính:
> `harness/` (kỹ năng lõi + nâng cao + lớp kiểm soát), `loop/` (vòng lặp tự chạy), `graph/` (tri thức dạng đồ thị).

AI/
├── AI_AGENT_FRAMEWORK.md                   ← TRANG CHỦ
├── AGENT_SYSTEM_ARCHITECTURE.md            ← KIẾN TRÚC HỆ THỐNG AGENT (8 Layer, cập nhật 2026)
├── HARNESS_ENGINEERING.md                  ← KIẾN TRÚC HARNESS
├── GRAPH_ENGINEERING.md                    ← KIẾN TRÚC GRAPH
│

├── harness/                                ← HARNESS (7 Components)
│  │
│  │  ── CORE SKILLS (Kỹ Năng Cốt Lõi) ──
│  ├── 01-retrieve-memory-knowledge/         ← ĐỌC
│  ├── 02-build-context/                     ← XỬ LÝ
│  ├── 03-update-memory-store/               ← GHI
│  ├── 04-plan-decompose-task/               ← LẬP KẾ HOẠCH
│  ├── 05-prompt-builder/                    ← XÂY DỰNG PROMPT
│  ├── 06-decide-tools-mcp/                  ← QUYẾT ĐỊNH DỤNG CỤ
│  │
│  │  ── ADVANCED SKILLS (Kỹ Năng Nâng Cao) ──
│  ├── 07-workflow/                          ← QUY TRÌNH
│  ├── 08-task/                              ← QUẢN LÝ TASK
│  ├── 09-multi-agent/                       ← HỆ THỐNG ĐA AGENT
│  ├── 10-automation/                        ← TỰ ĐỘNG HÓA
│  ├── 11-evaluation/                        ← ĐÁNH GIÁ
│  │
│  │  ── MẶT PHẲNG KIỂM SOÁT XUYÊN MODULE ──
│  │  (nền tảng mà mọi module ở trên phụ thuộc)
│  ├── 12-sandbox-execution/                 ← SANDBOX / CÁCH LY
│  ├── 13-trajectory-observability/          ← TRAJECTORY / KIỂM TOÁN
│  ├── 14-compaction-context/                ← NÉN CONTEXT
│  └── 15-approval-gates/                    ← HUMAN-IN-THE-LOOP
│
├── loop/                                    ← LOOP ENGINEERING
│  ├── 01-concepts/  02-patterns/  03-safety/
│  ├── 04-operating/  05-multi-loop/  06-anti-patterns/
│  └── 07-tools/                            ← VÒNG LẶP CẢI THIỆN
│
└── graph/                                   ← GRAPH ENGINEERING (Knowledge Substrate)
   ├── 01-foundations/                       ← NỀN TẢNG GRAPH
   ├── 02-knowledge-graph/                   ← XÂY DỰNG KG
   ├── 03-graph-storage/                     ← LƯU TRỮ & TRUY VẤN
   ├── 04-graph-embeddings/                  ← EMBEDDINGS
   ├── 05-graph-rag/                         ← GRAPH RAG
   ├── 06-graph-reasoning/                   ← SUY LUẬN
   ├── 07-gnn/                               ← GRAPH NEURAL NETWORKS
   ├── 08-graph-workflow/                    ← WORKFLOW & VẬN HÀNH
   └── 09-evaluation/                        ← ĐÁNH GIÁ
```

> **Tóm gọn 1 câu:** Repo chia 3 khu: `harness/` cho kỹ năng lõi và hệ an toàn, `loop/` cho vòng lặp tự chạy, `graph/` cho tri thức dạng đồ thị.

## Lộ Trình Học

> **Đọc sơ đồ này thế nào:** mỗi ô là một module, mũi tên `───►` là thứ tự dữ liệu chảy.
> 6 Phase là 6 giai đoạn học: lấy thông tin → xử lý → lưu trữ → tổ chức → phối hợp → đánh giá.

```
┌──────────────────────────────────────────────────────────────────────┐
│                    AI AGENT LEARNING PATH                             │
│                                                                      │
│  ── CORE SKILLS ────────────────────────────────────────            │
│                                                                      │
│  Phase 1: THU THẬP THÔNG TIN                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 01 Retrieve Memory   │───►│ 02 Build Context     │                │
│  │ & Knowledge          │    │                      │                │
│  └─────────────────────┘    └──────────┬───────────┘                │
│                                         │                            │
│  Phase 2: XỬ LÝ & TRẢ LỜI               │                            │
│                                         ▼                            │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 05 Prompt Builder    │◄───│ 06 Decide Tools /    │                │
│  └─────────────────────┘    └──────────────────────┘                │
│                                                                      │
│  Phase 3: LƯU TRỮ & QUẢN LÝ                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 03 Update Memory     │───►│ 04 Plan & Decompose  │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  ── ADVANCED SKILLS ───────────────────────────────────            │
│                                                                      │
│  Phase 4: TỔ CHỨC & VẬN HÀNH                                      │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 07 Workflow          │───►│ 08 Task Management   │                │
│  │ ─ Pipeline Design    │    │ ─ Classification     │                │
│  │ ─ State Machine      │    │ ─ Decomposition      │                │
│  │ ─ Error Recovery     │    │ ─ Priority/Schedule  │                │
│  │ ─ Observability      │    │ ─ Dependency Graph   │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  Phase 5: PHỐI HỢP & TỰ ĐỘNG                                      │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 09 Multi-Agent       │───►│ 10 Automation        │                │
│  │ ─ Agent Roles        │    │ ─ CI/CD Pipelines    │                │
│  │ ─ Communication      │    │ ─ Code Generation    │                │
│  │ ─ Orchestration      │    │ ─ Git Automation     │                │
│  │ ─ Shared Memory      │    │ ─ Monitoring/Alerts  │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  Phase 6: ĐÁNH GIÁ & CẢI TIẾN                                     │
│  ┌──────────────────────────────────────────────────────┐          │
│  │ 11 Evaluation                                            │          │
│  │ ─ Quality Metrics  ─ Benchmarks  ─ Continuous Improve  │          │
│  └──────────────────────────────────────────────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Học 6 phase theo thứ tự: lấy thông tin → xử lý → lưu trữ → tổ chức → phối hợp → đánh giá.

## Môi Trường Thực Hành

> **Cách đọc bảng này:** cột **Component** là thành phần hệ thống; **Model / Tool** là phần mềm cụ thể dùng cho phần đó;
> cột **Chạy** cho biết chạy ở đâu. Tất cả đều chạy **local** (trên máy bạn, miễn phí) — không bắt buộc dùng dịch vụ đám mây trả phí.
> "Embedding" = biến chữ thành dãy số (vector) để máy so sánh độ giống nhau. "Vector Store" = nơi lưu và tìm các dãy số đó.

| Component | Model / Tool | Chạy |
|-----------|-------------|------|
| LLM | `gemma3:12b` | Local via Ollama |
| Embedding | `nomic-embed-text` (768D) | Local via Ollama |
| Vector Store | FAISS / ChromaDB | Local |
| Graph Store | Neo4j / Kuzu / NetworkX | Local (Docker hoặc embedded) |
| GNN | PyG / DGL | Local (Python) |
| BM25 | Custom Python | Local |
| MCP Server | GitHub MCP, Custom tools | Local |

> **Giải nghĩa vài thuật ngữ trong bảng:** *BM25* = thuật toán tìm kiếm theo từ khóa, đếm từ xuất hiện nhiều.
> *GNN* = Graph Neural Network, mạng nơ-ron học trên dữ liệu dạng đồ thị. *Docker* = công cụ gói app vào "hộp" chạy được mọi máy.
> *Embedded* = chạy ngay trong tiến trình app, không cần cài server riêng.

> **Tóm gọn 1 câu:** Toàn bộ môi trường thực hành chạy miễn phí trên máy bạn bằng Ollama + các thư viện Python, không cần trả tiền cloud.

## Chi Tiết Từng Phần

> **Phần này nói gì:** mỗi `Part` là một nhóm bài học. Mỗi bảng liệt kê các chủ đề trong đó,
> kèm link nhảy thẳng tới README của module tương ứng. Cột **Mô tả** giải thích chủ đề đó xử lý vấn đề gì.

> **Tóm gọn 1 câu:** Đây là mục lục chi tiết: 13 Part = 13 nhóm kỹ năng, mỗi kỹ năng dẫn link tới bài học đầy đủ.

### Part I: Retrieve Memory & Knowledge
> Làm sao tìm đúng thông tin?

| # | Topic | Mô tả |
|---|-------|-------|
| 1.1 | [Vector Search](harness/01-retrieve-memory-knowledge/README.md#1-vector-search) | Semantic similarity với embeddings |
| 1.2 | [BM25 Search](harness/01-retrieve-memory-knowledge/README.md#2-bm25-search) | Keyword matching, term frequency |
| 1.3 | [Hybrid Search](harness/01-retrieve-memory-knowledge/README.md#3-hybrid-search) | Kết hợp Vector + BM25 |
| 1.4 | [Knowledge Graph](harness/01-retrieve-memory-knowledge/README.md#4-knowledge-graph) | Entity relationships, graph traversal |
| 1.5 | [Multi-Source Retrieval](harness/01-retrieve-memory-knowledge/README.md#5-multi-source-retrieval) | Fusing results từ nhiều nguồn |

> **Đọc bảng:** "Semantic similarity" = so sánh **ý nghĩa** câu chữ (AI hiểu "xe hơi" ≈ "automobile").
> "Term frequency" = đếm **từ khóa** xuất hiện mấy lần. Hybrid = làm cả hai rồi gộp kết quả.
> Knowledge Graph = sơ đồ quan hệ dạng "A — làm việc tại → B".

> **Tóm gọn 1 câu:** Phần này dạy 5 cách tìm thông tin: theo ý nghĩa, theo từ khóa, gộp cả hai, theo đồ thị quan hệ, và gộp nhiều nguồn.

### Part II: Build Context
> Làm sao tổ chức thông tin hiệu quả?

| # | Topic | Mô tả |
|---|-------|-------|
| 2.1 | [Context Window Management](harness/02-build-context/README.md#1-context-window-management) | Token limits, sliding window |
| 2.2 | [Context Compression](harness/02-build-context/README.md#2-context-compression) | Tóm tắt, extract key info |
| 2.3 | [Prompt Templates](harness/02-build-context/README.md#3-prompt-templates) | System/user/assistant roles |
| 2.4 | [Hierarchical Context](harness/02-build-context/README.md#4-hierarchical-context) | Summary → Detail structure |
| 2.5 | [Multi-turn Context](harness/02-build-context/README.md#5-multi-turn-context) | Conversation memory management |

> **Đọc bảng:** Context window = "bàn làm việc" của AI — chỗ chứa mọi thứ nó đọc được trong 1 lượt, có giới hạn số token.
> "Sliding window" = giữ phần mới nhất, bỏ phần cũ nhất. "System/user/assistant roles" = 3 vai trò trong prompt: quy định, hỏi, trả lời.

> **Tóm gọn 1 câu:** Phần này dạy cách nhét đúng thông tin, vừa đủ và có tổ chức, vào ô nhớ giới hạn của AI.

### Part III: Update Memory & Knowledge Store
> Làm sao lưu lại thông tin mới?

| # | Topic | Mô tả |
|---|-------|-------|
| 3.1 | [Write-back Memory](harness/03-update-memory-store/README.md#1-write-back-memory) | Ghi sự kiện mới vào memory |
| 3.2 | [Memory Consolidation](harness/03-update-memory-store/README.md#2-memory-consolidation) | Merge, dedupe facts |
| 3.3 | [Report Generation](harness/03-update-memory-store/README.md#3-report-generation) | Tạo output có cấu trúc |
| 3.4 | [KB Maintenance](harness/03-update-memory-store/README.md#4-kb-maintenance) | CRUD knowledge base |
| 3.5 | [Event Sourcing](harness/03-update-memory-store/README.md#5-event-sourcing-pattern) | Full audit trail |

> **Đọc bảng:** "Dedupe" = bỏ trùng lặp (như gộp 2 ghi chú nói cùng một chuyện).
> "CRUD" = 4 thao tác cơ bản: Create, Read, Update, Delete. "Event sourcing" = lưu từng sự kiện theo thứ tự,
> như nhật ký — muốn xem lại lúc nào cũng xem được ("audit trail" = dấu vết kiểm tra đầy đủ).

> **Tóm gọn 1 câu:** Phần này dạy cách ghi thông tin mới vào bộ nhớ dài hạn, dọn trùng lặp, và giữ được nhật ký đầy đủ để tra lại.

### Part IV: Plan & Decompose Task
> Làm sao chia nhỏ task phức tạp?

| # | Topic | Mô tả |
|---|-------|-------|
| 4.1 | [Task Decomposition](harness/04-plan-decompose-task/README.md#1-task-decomposition-patterns) | Sequential, parallel, hierarchical |
| 4.2 | [Planning Algorithms](harness/04-plan-decompose-task/README.md#2-planning-algorithms) | Plan-and-Solve, ToT |
| 4.3 | [Agent Workflows](harness/04-plan-decompose-task/README.md#3-agent-workflows) | ReAct, Multi-agent, State Machine |
| 4.4 | [State Management](harness/04-plan-decompose-task/README.md#4-state-management) | Checkpoint, rollback |
| 4.5 | [ReAct Pattern](harness/04-plan-decompose-task/README.md#5-react-pattern) | Thought → Action → Observation |

> **Đọc bảng:** "Sequential" = làm lần lượt từng việc; "parallel" = làm cùng lúc nhiều việc; "hierarchical" = chia cây: việc lớn thành việc nhỏ.
> ToT = Tree of Thought, tức để AI "suy nghĩ nhiều nhánh" rồi chọn nhánh tốt. ReAct = vòng lặp: nghĩ → làm → xem kết quả → nghĩ tiếp.
> "Checkpoint/rollback" = lưu điểm an toàn để quay lại nếu sai (như nút save trong game).

> **Tóm gọn 1 câu:** Phần này dạy cách bẻ việc lớn thành các việc nhỏ làm được, rồi cho AI chạy theo vòng lặp "nghĩ — làm — kiểm tra".

### Part V: Prompt Builder
> Làm sao viết prompt tốt nhất?

| # | Topic | Mô tả |
|---|-------|-------|
| 5.1 | [Prompt Templates](harness/05-prompt-builder/README.md#1-prompt-templates) | Reusable templates với variables |
| 5.2 | [Few-shot Examples](harness/05-prompt-builder/README.md#2-few-shot-examples) | Dynamic example selection |
| 5.3 | [Chain-of-Thought](harness/05-prompt-builder/README.md#3-chain-of-thought-cot) | CoT variants |
| 5.4 | [Guardrails](harness/05-prompt-builder/README.md#4-guardrails) | Safety filters, validation |
| 5.5 | [Output Format](harness/05-prompt-builder/README.md#5-output-format-control) | JSON, Markdown, Table |

> **Đọc bảng:** Template = mẫu câu có chỗ điền biến, ví dụ "Viết tóm tắt cho file {tên_file}".
> Few-shot = đưa vài ví dụ mẫu vào prompt để AI bắt chước. CoT (Chain-of-Thought) = yêu cầu AI suy nghĩ từng bước thay vì nhảy đến đáp án.
> Guardrails = "lan can an toàn": lọc chặn yêu cầu nguy hiểm và kiểm tra output trước khi dùng.

> **Tóm gọn 1 câu:** Phần này dạy cách viết prompt có mẫu, có ví dụ, có suy luận từng bước, có lan can an toàn, và ra đúng định dạng mong muốn.

### Part VI: Decide Tools / MCP Calls
> Khi nào dùng tool nào?

| # | Topic | Mô tả |
|---|-------|-------|
| 6.1 | [Tool Selection](harness/06-decide-tools-mcp/README.md#1-tool-selection-patterns) | Registry, search, categories |
| 6.2 | [Intent Classification](harness/06-decide-tools-mcp/README.md#2-intent-classification) | Rule-based & LLM-based |
| 6.3 | [MCP Protocol](harness/06-decide-tools-mcp/README.md#3-mcp-model-context-protocol) | Model Context Protocol |
| 6.4 | [Tool Executor](harness/06-decide-tools-mcp/README.md#4-tool-executor-with-error-handling) | Error handling & retry |

> **Đọc bảng:** "Registry" = danh mục tool có sẵn, agent chọn trong đó. "Intent classification" = đoán ý người dùng
> muốn gì — bằng luật cứng (rule-based) hoặc nhờ AI tự phán (LLM-based). "Retry" = thử lại khi tool lỗi, ví dụ gọi API bị timeout thì thử lần 2.

> **Tóm gọn 1 câu:** Phần này dạy cách agent chọn đúng tool cho từng nhu cầu, gọi qua chuẩn MCP, và tự thử lại khi gặp lỗi.

---

### Part VII: Workflow
> Làm sao tổ chức quy trình thực hiện?

| # | Topic | Mô tả |
|---|-------|-------|
| 7.1 | [Workflow Patterns](harness/07-workflow/README.md#1-workflow-patterns) | Sequential, parallel, conditional |
| 7.2 | [Pipeline Design](harness/07-workflow/README.md#2-pipeline-design) | Transform, filter, sink |
| 7.3 | [State Machine](harness/07-workflow/README.md#3-state-machine) | FSM cho agent |
| 7.4 | [Error Recovery](harness/07-workflow/README.md#4-error-recovery) | Retry, circuit breaker |
| 7.5 | [Observability](harness/07-workflow/README.md#5-observability) | Logging, metrics |

> **Đọc bảng:** "Conditional" = rẽ nhánh theo điều kiện (nếu X thì làm A, không thì làm B).
> Pipeline = dây chuyền: dữ liệu vào đầu, từng bước biến đổi (transform), lọc (filter), rồi xuất ra cuối (sink).
> FSM = finite state machine, máy trạng thái: agent chỉ ở 1 trạng thái tại 1 thời điểm (idle → chạy → xong).
> Circuit breaker = "cầu chì": lỗi quá nhiều lần thì ngừng gọi luôn, khỏi đổ thêm tải.

> **Tóm gọn 1 câu:** Phần này dạy cách nối các bước thành dây chuyền có nhánh, có cầu chì chống lỗi, và có log để biết chuyện gì xảy ra.

### Part VIII: Task Management
> Làm sao quản lý và theo dõi tasks?

| # | Topic | Mô tả |
|---|-------|-------|
| 8.1 | [Task Classification](harness/08-task/README.md#1-task-classification) | Phân loại theo category & complexity |
| 8.2 | [Task Decomposition](harness/08-task/README.md#2-task-decomposition) | Feature, layer, file, TDD |
| 8.3 | [Priority & Scheduling](harness/08-task/README.md#3-priority--scheduling) | Eisenhower matrix, token budget |
| 8.4 | [Task State Management](harness/08-task/README.md#4-task-state-management) | Lifecycle, valid transitions |
| 8.5 | [Dependency Management](harness/08-task/README.md#5-dependency-management) | DAG, topological sort |

> **Đọc bảng:** Eisenhower matrix = chia việc theo 4 ô: gấp+quan trọng làm trước, không gấp không quan trọng bỏ.
> Token budget = trạm số token AI được phép tiêu cho task đó. TDD = Test-Driven Development, viết test trước rồi mới viết code.
> DAG = sơ đồ có hướng không vòng lặp — biểu thị "việc B phải chờ việc A xong". Topological sort = xếp thứ tự hợp lý từ DAG đó.

> **Tóm gọn 1 câu:** Phần này dạy cách xếp loại, chia nhỏ, ưu tiên và sắp thứ tự các task sao cho việc nào cũng làm đúng lúc.

### Part IX: Multi-Agent Systems
> Làm sao phối hợp nhiều agents?

| # | Topic | Mô tả |
|---|-------|-------|
| 9.1 | [Agent Roles](harness/09-multi-agent/README.md#1-agent-roles) | Planner, Coder, Reviewer, Tester |
| 9.2 | [Communication Patterns](harness/09-multi-agent/README.md#2-communication-patterns) | Hierarchical, P2P, pipeline |
| 9.3 | [Orchestration](harness/09-multi-agent/README.md#3-orchestration-strategies) | Sequential, parallel, debate, voting |
| 9.4 | [Shared Memory](harness/09-multi-agent/README.md#4-shared-memory) | Versioned, tagged, locked |
| 9.5 | [Conflict Resolution](harness/09-multi-agent/README.md#5-conflict-resolution) | File lock, voting, deadlock detection |

> **Đọc bảng:** Mỗi agent là một AI đảm nhận một vai, như một đội nhóm: Planner chia việc, Coder viết code, Reviewer soi lỗi, Tester chạy test.
> P2P = peer-to-peer, agent nói thẳng với nhau không qua sếp. Debate/voting = cho các agent tranh luận rồi bầu chọn kết quả.
> File lock = khoá file để 2 agent không ghi cùng lúc. Deadlock = hai agent chờ nhau mãi mãi — cần cơ chế phát hiện để thoát.

> **Tóm gọn 1 câu:** Phần này dạy cách chia vai cho nhiều agent, cho chúng giao tiếp, dùng chung bộ nhớ, và xử lý mâu thuẫn khi cùng đụng tới một thứ.

### Part X: Automation
> Làm sao tự động hóa các task lặp đi lặp lại?

| # | Topic | Mô tả |
|---|-------|-------|
| 10.1 | [Automation Patterns](harness/10-automation/README.md#1-automation-patterns) | Event, scheduled, reactive, self-healing |
| 10.2 | [CI/CD Pipelines](harness/10-automation/README.md#2-cicd-pipelines) | GitHub Actions, deploy pipeline |
| 10.3 | [Code Generation](harness/10-automation/README.md#3-code-generation-automation) | Scaffolding, templates |
| 10.4 | [Scheduled Tasks](harness/10-automation/README.md#4-scheduled-tasks) | Cron, interval, daily |
| 10.5 | [Git Automation](harness/10-automation/README.md#5-git-automation) | Hooks, commit conventions |
| 10.6 | [Monitoring & Alerts](harness/10-automation/README.md#6-monitoring--alerts) | Thresholds, dashboards |

> **Đọc bảng:** Event = chạy khi có việc xảy ra (có PR mới → tự review). Scheduled = chạy theo giờ (cron = trình hẹn giờ của Linux).
> Reactive = phản ứng khi có chuyện bất thường. Self-healing = tự sửa lỗi của chính mình.
> CI/CD = dây chuyền tự động build, test, deploy (triển khai) mỗi khi có code mới. Hooks = "móc" tự chạy script tại thời điểm cố định, ví dụ trước mỗi commit.

> **Tóm gọn 1 câu:** Phần này dạy cách cho máy tự làm việc lặp lại: theo giờ, theo sự kiện, kèm tự sửa lỗi và báo động khi có chuyện.

### Part XI: Evaluation
> Làm sao đánh giá hiệu quả AI coding?

| # | Topic | Mô tả |
|---|-------|-------|
| 11.1 | [Evaluation Dimensions](harness/11-evaluation/README.md#1-evaluation-dimensions) | Correctness, quality, safety, speed |
| 11.2 | [Quality Metrics](harness/11-evaluation/README.md#2-quality-metrics) | Complexity, maintainability |
| 11.3 | [Performance Benchmarks](harness/11-evaluation/README.md#3-performance-benchmarks) | Benchmark suite, compare |
| 11.4 | [Evaluation Framework](harness/11-evaluation/README.md#4-evaluation-framework) | Auto-eval pipeline |
| 11.5 | [Continuous Improvement](harness/11-evaluation/README.md#5-continuous-improvement) | Trend analysis, suggestions |
| 11.6 | [Reporting & Dashboards](harness/11-evaluation/README.md#6-reporting--dashboards) | Markdown/JSON reports |

> **Đọc bảng:** Dimensions = các khía cạnh chấm điểm: chạy đúng chưa, code đẹp chưa, an toàn chưa, nhanh chưa.
> Metrics = số liệu đo cụ thể (ví dụ độ phức tạp code). Benchmark = bộ đề thi chuẩn để so AI này với AI khác.
> "Auto-eval pipeline" = dây chuyền chấm điểm tự động, khỏi chấm tay.

> **Tóm gọn 1 câu:** Phần này dạy cách chấm điểm AI theo nhiều khía cạnh, tự động chạy đánh giá, và theo dõi xu hướng để cải tiến liên tục.

### Mặt Phẳng Kiểm Soát (Harness Modules 12–15)
> Làm sao chạy, quan sát, kiểm soát và xin phép người dùng khi giao việc cho agent?

Modules `12`–`15` **không phải bước trong pipeline**. Chúng là lớp nền mà mọi
module ở trên đều dựa vào. (Nói như đời thường: các module 01–11 là "nhân viên làm việc",
còn 12–15 là "hệ thống an toàn của toà nhà" — ai trong toà cũng nhờ nó.)
Mỗi module chuẩn hoá đúng một câu hỏi của nó; các module khác
chỉ trỏ tới chứ không làm lại.

| # | Chủ đề | Mô tả |
|---|-------|-------|
| 12 | [Sandbox Execution](harness/12-sandbox-execution/README.md) | Tier cách ly, threat model, runner harden, ma trận policy theo role |
| 13 | [Trajectory & Observability](harness/13-trajectory-observability/README.md) | Luồng `TrajectoryEvent` append-only, join key, retention, redaction |
| 14 | [Compaction & Context](harness/14-compaction-context/README.md) | Trigger nén, pin set, pruning, khối resume |
| 15 | [Approval Gates](harness/15-approval-gates/README.md) | Risk tier, payload cổng, timeout-deny, phán quyết con người, audit trail |

> **Đọc bảng, giải nghĩa từng dòng:**
> **12** — Sandbox = "chuồng nhốt" cách ly code không tin cậy (chạy trong container, không đụng được ra ngoài).
> Threat model = liệt kê kẻ thù/rủi ro cần phòng. Runner harden = gia cố trình chạy code. Ma trận policy = bảng quy định ai được chạy gì.
> **13** — TrajectoryEvent = bản ghi từng bước agent làm; append-only = chỉ được thêm, không được sửa/xóa (nhật ký kiên cố).
> Retention = giữ bao lâu rồi xóa; redaction = che thông tin nhạy cảm (mật khẩu, token) trước khi lưu.
> **14** — Compaction = nén bớt context khi gần đầy bộ nhớ. Pin set = danh sách nội dung "ghim" không bao giờ bị nén bỏ.
> Pruning = tỉa bớt nội dung kém quan trọng. Khối resume = bản ghi giúp tiếp tục từ điểm dừng.
> **15** — Approval gates = cổng duyệt: thao tác nguy hiểm phải chờ người bấm duyệt. Risk tier = xếp mức rủi ro.
> Timeout-deny = không duyệt trong X giây thì coi như từ chối (an toàn mặc định).

> **Tóm gọn 1 câu:** Bốn module này là hệ an toàn chung: cách ly khi chạy, ghi nhật ký từng bước, nén bộ nhớ khi đầy, và bắt duyệt người thật trước khi làm việc nguy hiểm.

> Nhãn Roman `Part XII`/`XIII` ở dưới thuộc cách chia phần của framework (Loop, Graph).
> Hai nhãn này không liên quan tới số thứ tự module harness.

### Part XII: Loop Engineering
> Làm sao thiết kế vòng lặp tự duy trì cho AI agents?

| # | Topic | Mô tả |
|---|-------|-------|
| 12.1 | [Concepts](loop/01-concepts/README.md) | 5 building blocks + memory, anatomy, L1-L3, taxonomy |
| 12.2 | [Patterns](loop/02-patterns/README.md) | 7 production patterns (daily-triage, pr-babysitter, ci-sweeper...) |
| 12.3 | [Safety](loop/03-safety/README.md) | Loop Design Checklist, denylist, human gates |
| 12.4 | [Operating](loop/04-operating/README.md) | Budget, logging, metrics, pause/kill |
| 12.5 | [Multi-Loop](loop/05-multi-loop/README.md) | Phối hợp khi chạy nhiều loops |
| 12.6 | [Anti-Patterns](loop/06-anti-patterns/README.md) | 10 anti-patterns + failure mode catalog |
| 12.7 | [Tools](loop/07-tools/README.md) | loop-init, loop-audit, loop-cost, ecosystem |

> **Đọc bảng:** Loop = vòng lặp agent tự chạy lặp lại theo lịch (ví dụ: mỗi sáng dò PR mới và nhắc review).
> L1-L3 = 3 mức độ tự chủ: từ chạy có giám sát tới chạy gần như độc lập. Denylist = "danh sách cấm" việc loop không được làm.
> Human gates = điểm bắt buộc dừng chờ người duyệt. Anti-pattern = cách làm nghe hợp lý nhưng thực ra gây hại.
> pr-babysitter = loop "trông nom" pull request tới khi được merge.

> **Tóm gọn 1 câu:** Phần này dạy cách dựng vòng lặp agent tự chạy hằng ngày mà vẫn an toàn: có giới hạn, có log, có người bấm duyệt ở chỗ nguy hiểm.

### Part XIII: Graph Engineering
> Làm sao xây dựng hệ thống tri thức dạng đồ thị cho AI agents?

| # | Topic | Mô tả |
|---|-------|-------|
| 13.1 | [Foundations](graph/01-foundations/README.md) | Graph theory, types, representations, metrics |
| 13.2 | [Knowledge Graph](graph/02-knowledge-graph/README.md) | Entity/relation extraction, ontology, deduplication |
| 13.3 | [Graph Storage](graph/03-graph-storage/README.md) | Neo4j, Cypher, indexing, transactions |
| 13.4 | [Graph Embeddings](graph/04-graph-embeddings/README.md) | Node2Vec, GraphSAGE, hybrid vector+graph search |
| 13.5 | [GraphRAG](graph/05-graph-rag/README.md) | Subgraph retrieval, community summaries, Microsoft pattern |
| 13.6 | [Graph Reasoning](graph/06-graph-reasoning/README.md) | Traversal, path finding, inference rules, temporal reasoning |
| 13.7 | [GNN](graph/07-gnn/README.md) | GNN, link prediction, KG completion, R-GCN |
| 13.8 | [Graph Workflow](graph/08-graph-workflow/README.md) | Pipeline ETL, incremental updates, versioning, orchestration |
| 13.9 | [Evaluation](graph/09-evaluation/README.md) | Coverage, hallucination, path precision, benchmarks |

> **Đọc bảng:** Graph = đồ thị: các điểm (node) nối với nhau bằng cạnh (edge) — ví dụ "An — làm_việc_tại → Công ty X".
> Entity = đối tượng (người, sản phẩm); relation = quan hệ giữa chúng; ontology = "khung phân loại" quy định loại nào nối loại nào.
> Cypher = ngôn ngữ truy vấn của Neo4j (kiểu SQL nhưng cho đồ thị). ETL = Extract-Transform-Load: lấy dữ liệu, biến đổi, nạp vào.
> Link prediction = đoán mối nối còn thiếu ("An có thể biết B không?"). Temporal reasoning = suy luận theo thời gian ("sự kiện này xảy ra trước cái nào?").

> **Tóm gọn 1 câu:** Phần này dạy cách biến tài liệu thành sơ đồ quan hệ (ai nối ai, cái gì thuộc cái gì) rồi cho AI tra cứu và suy luận trên sơ đồ đó.

---

## 🧠 Hiểu Framework Này

> **Mục này nói gì:** câu hỏi quan trọng nhất trước khi học — "vậy model AI nằm ở đâu trong hệ thống?"
> Trả lời: model chỉ là một mảnh; phần lớn hệ thống là code thường mà bạn điều khiển được.

> **Framework này giống như "bộ máy điều phối" — còn AI model chỉ lo phần "suy nghĩ".**

Framework giúp bạn hiểu **cách ráp các mảnh lại với nhau** — model chỉ là một mảnh trong đó thôi. Bạn có thể chạy **Ollama miễn phí ngay trên máy mình** hoặc **gọi API trả phí**, tùy ngân sách của bạn. ("Điều phối" = orchestration: sắp xếp ai làm gì, làm khi nào, như quản đốc nhịp việc của cả đội.)

### Flow minh họa: RAG Chatbot cần gì?

```
Tài liệu của bạn (PDF, docs, DB)
        ↓
   [Module 01] Retrieve — tìm đoạn liên quan
        ↓
   [Module 02] Build Context — sắp xếp thông tin
        ↓
   [Module 05] Prompt Builder — tạo prompt
        ↓
        ↓
   ══════════════════════════════
   ║   AI MODEL (Ollama/GPT)   ║  ← PHẦN CẦN MODEL
   ║   Đọc context + trả lời   ║
   ══════════════════════════════
        ↓
      Câu trả lời
```

> **Tóm gọn 1 câu:** Một chatbot RAG = 3 bước code (tìm → sắp xếp → ghép prompt) + đúng 1 chỗ cần model: đọc context và trả lời.

### Flow minh họa: GraphRAG cần gì?

```
Tài liệu của bạn (PDF, docs, DB)
        ↓
   [Graph 02] Knowledge Graph — trích entities/relations (LLM)
        ↓
   [Graph 03] Graph Storage — lưu vào Neo4j/Kuzu (Cypher)
        ↓
   [Graph 05] GraphRAG — subgraph retrieval + community summaries
        ↓
   [Harness 02] Build Context — gộp graph context + vector context
        ↓
   ══════════════════════════════
   ║   AI MODEL (Ollama/GPT)   ║  ← PHẦN CẦN MODEL
   ║   Đọc graph context + trả lời có citation path ║
   ══════════════════════════════
        ↓
      Câu trả lời + đường dẫn chứng minh (path)
```

> **Tóm gọn 1 câu:** GraphRAG thêm bước dựng "sơ đồ quan hệ" trước khi trả lời — đổi lại bạn nhận được câu trả lời kèm đường dẫn chứng minh.

### Phân biệt rõ: Phần nào cần model?

> **Cách đọc bảng này:** cột giữa trả lời câu hỏi "có cần AI model không?" — dấu ✅ nghĩa là cần, ❌ nghĩa là chỉ code thường là đủ.

| Phần | Cần model? | Mô tả |
|------|-----------|-------|
| **Vector Search** (Module 01) | ✅ Cần **Embedding model** | Biến text thành vector để so sánh |
| **BM25 Search** (Module 01) | ❌ Không cần | Thuần toán học, đếm từ khóa |
| **Generate Answer** (Module 05) | ✅ Cần **LLM** | gemma3:12b, GPT-4o, Claude... |
| **Prompt Building** (Module 05) | ❌ Không cần | Chỉ là sắp xếp text |
| **Workflow** (Module 07) | ❌ Không cần | Chỉ là orchestration logic |
| **CI/CD Automation** (Module 10) | ❌ Không cần | GitHub Actions, scripts |

> **Tóm gọn 1 câu:** Chỉ có 2 chỗ thật sự cần AI model — biến chữ thành vector (embedding) và sinh câu trả lời (LLM); phần còn lại là code thường.

### 2 loại model cần thiết

> **Cách đọc bảng:** framework chỉ cần đúng 2 loại model. Cột "Local" là chạy trên máy bạn (miễn phí), cột "API" là gọi dịch vụ trả phí.

| Loại | Vai trò | Local (miễn phí) | API (trả phí) |
|------|---------|-------------------|---------------|
| **Embedding model** | Biến text thành vector (dùng cho search) | `nomic-embed-text` qua Ollama | OpenAI text-embedding-3-small |
| **LLM** (Large Language Model) | Tạo câu trả lời | `gemma3:12b`, `llama3`, `qwen2.5` qua Ollama | GPT-4o, Claude, Gemini |

> **Tóm gọn 1 câu:** Bạn cần đúng 2 loại model — một loại biến chữ thành số để tìm kiếm, một loại sinh câu trả lời — cả hai đều có bản miễn phí chạy local.

### Tóm lại

- **~60% framework** là code thuần, không cần model (search, workflow, orchestration)
- **~40% framework** mới cần tới model (embedding + sinh câu trả lời)

Nói ngắn gọn: framework giúp bạn **biết cách ráp các mảnh lại với nhau** — model chỉ là một mảnh trong đó. Cứ chạy **Ollama miễn phí trên máy** cho tiết kiệm, hoặc **gọi API trả phí** khi cần mạnh hơn, tùy túi tiền của bạn.

> **Tóm gọn 1 câu:** 6 phần là code thường, 4 phần cần model — và mọi thứ chạy được miễn phí trên máy bạn với Ollama.

---

## 🚀 Sau Khi Học Xong — Dự Án Thực Tế

> **Mục này nói gì:** 20 dự án mẫu xếp theo độ khó, để bạn biết học xong mỗi module thì làm được gì.
> Mỗi dự án ghi rõ: dùng module nào, mất bao lâu, ra kết quả gì.

Với **11 module** bao phủ trọn vẹn từ Retrieval, Context, Memory, Planning, Prompting, Tooling, Workflow, Task Management, Multi-Agent, Automation tới Evaluation — bạn có thể làm được **rất nhiều dự án thực tế**. Dưới đây là **20 dự án** chia theo cấp độ và lĩnh vực để bạn tham khảo dần.

---

### 🟢 Cấp Độ Cơ Bản — Bắt Đầu Ngay (Module 01-05)

> **Từ "Tech Stack" dưới đây nghĩa là "danh sách công nghệ dùng để build"** — ví dụ ChromaDB là một vector database nhúng gọn trong app.

#### 1. 📚 Personal Knowledge Base (PKB)

- **Mô tả**: Hệ thống lưu trữ & tìm kiếm kiến thức cá nhân từ notes, bookmarks, code snippets
- **Tech Stack**: ChromaDB + nomic-embed-text + Python CLI
- **⏱️ Thời gian build**: 2-3 ngày (CLI cơ bản), 1 tuần (có Web UI)
- **Module áp dụng**:
  - Module 01 — Vector Search + Hybrid Search (BM25 + Semantic)
  - Module 03 — Write-back Memory, KB Maintenance (CRUD)
  - Module 06 — Tool Selection (CLI tool, search tool)
- **Tính năng**: Import markdown/notes → Chunk → Embed → Semantic search CLI
  ("Chunk" = cắt tài liệu thành từng đoạn nhỏ; "Embed" = biến mỗi đoạn thành vector; "CLI" = app gõ lệnh trong terminal)
- **Kết quả**: `pkb search "cách deploy Docker"` → tìm đúng trong 1000+ notes

#### 2. 📄 Document Q&A Chatbot

- **Mô tả**: Chatbot trả lời câu hỏi từ tài liệu của riêng bạn (PDF, docs, wiki)
- **Tech Stack**: Ollama (gemma3:12b + nomic-embed-text) + FAISS/ChromaDB + FastAPI
- **⏱️ Thời gian build**: 3-5 ngày (endpoint cơ bản), 1-2 tuần (chat UI + multi-format)
- **Module áp dụng**:
  - Module 01 — Document Processing, Chunking, Vector Search
  - Module 02 — Context Window Management, Prompt Templates
  - Module 05 — Prompt Builder, Output Format Control
- **Tính năng**: Upload PDF → Auto-chunk → Embed → Chat với tài liệu
- **Kết quả**: Chatbot trả lời đúng từ tài liệu nội bộ, giảm hallucination

#### 3. 🔍 Hybrid Search Engine

- **Mô tả**: Search engine kết hợp semantic + keyword search với re-ranking
- **Tech Stack**: BM25 (Python) + FAISS + Cross-encoder reranker
- **⏱️ Thời gian build**: 3-5 ngày (BM25 + Vector), 1 tuần (thêm reranking + optimization)
- **Module áp dụng**:
  - Module 01 — Vector Search, BM25, Hybrid Search, Re-ranking
  - Module 02 — Context Compression (tóm tắt kết quả)
- **Tính năng**: Query → Parallel BM25 + Vector → Merge → Rerank → Top-K
  (Query = câu tìm kiếm; Parallel = chạy song song 2 cách tìm; Rerank = chấm lại điểm kết quả rồi xếp lại hạng; Top-K = lấy K kết quả tốt nhất)
- **Kết quả**: Search chính xác hơn 40% so với chỉ BM25 hoặc chỉ Vector

#### 4. 📊 Markdown to Structured Data

- **Mô tả**: Tự động chuyển đổi tài liệu Markdown thành database có cấu trúc
- **Tech Stack**: LLM (gemma3:12b) + SQLite + Python
- **⏱️ Thời gian build**: 1-2 ngày
- **Module áp dụng**:
  - Module 05 — Prompt Builder, Output Format Control (JSON/Table)
  - Module 03 — Report Generation, Write-back Memory
- **Tính năng**: Input Markdown docs → LLM extract entities/relations → Store as structured data
- **Kết quả**: Tự động tạo database từ docs, hỗ trợ query có cấu trúc

#### 5. 🧪 AI Code Review Bot (Đơn Giản)

- **Mô tả**: Bot review code khi push lên GitHub, gợi ý improvements
- **Tech Stack**: GitHub Webhooks + LLM + Python
- **⏱️ Thời gian build**: 2-3 ngày
- **Module áp dụng**:
  - Module 05 — Prompt Builder (review prompts), Guardrails (safety)
  - Module 10 — Git Automation (hooks, webhooks)
- **Tính năng**: PR created → Bot reviews → Comment suggestions on PR
- **Kết quả**: Auto code review, bắt bugs sớm, gợi ý best practices (best practices = cách làm chuẩn được khuyến khích)

> **Tóm gọn 1 câu:** Năm dự án đầu nhẹ nhàng: mỗi cái chỉ dùng 2-3 module, build trong vài ngày, đủ để hiểu nền tảng.

---

### 🟢 Cấp Độ Daily-Use — Hữu Ích Mỗi Ngày (Module 01-10)

> **Đây là các dự án nhỏ, làm trong 1-3 ngày nhưng xài MỖI NGÀY ở công việc thật.**
> (Các từ như "Webhook" dưới đây: webhook = cơ chế GitHub/Slack tự gọi URL của bạn khi có sự kiện xảy ra.)

#### 6. 📋 Auto Daily Work Log

- **Mô tả**: Tự động ghi nhận công việc hàng ngày từ git commits, Slack messages, calendar — tạo daily report
- **Tech Stack**: LLM + Git API + Calendar API + Markdown/JSON output
- **Module áp dụng**:
  - Module 01 — Multi-Source Retrieval (git, calendar, Slack, Jira)
  - Module 03 — Write-back Memory (lưu daily log), Report Generation
  - Module 05 — Prompt Builder (report template), Output Format (Markdown table)
  - Module 10 — Scheduled Tasks (cron mỗi cuối ngày)
- **Flow**:
  ```
  18:00 PM → Cron trigger
    → Git: List commits today (git log --since="today")
    → Calendar: List meetings attended
    → Jira/Trello: Tasks updated
    → Slack: Key messages summary (optional)
    → LLM: Synthesize into daily report
    → Output: Markdown daily log + Send to Slack/Email
  ```
- **Kết quả**: Không bao giờ quên ghi công việc cuối ngày. Báo cáo tự động, chuyên nghiệp.
- **Sample output**:
  ```markdown
  ## Daily Report — 2025-01-15
  
  ### ✅ Completed
  - [PROJ-123] Fix login bug — 3 commits, merged PR #456
  - [PROJ-124] Implement user search API — 2 commits, PR #457 pending review
  
  ### 📅 Meetings
  - Sprint Planning (10:00-10:30)
  - Code Review with Team (14:00-14:30)
  
  ### 🔄 In Progress
  - [PROJ-125] Dashboard redesign — 60% complete
  
  ### 📌 Blockers
  - Waiting for API credentials from DevOps team
  ```

#### 7. 📝 Smart Standup Bot

- **Mô tả**: Tự động generate câu trả lời standup (What did you do? What will you do? Blockers?) từ dữ liệu real
- **Tech Stack**: LLM + Git + Jira API + Calendar
- **Module áp dụng**:
  - Module 01 — Retrieve hoạt động hôm qua từ nhiều nguồn
  - Module 05 — Prompt Builder (standup template), Chain-of-Thought (summarize)
  - Module 10 — Scheduled Tasks (cron mỗi sáng 9:00)
- **Flow**:
  ```
  09:00 AM → Bot gửi tin nhắn:
    "🌅 Good morning! Here's your standup for today:"
    
    What I did yesterday:
    - Fixed auth bug (commit abc123)
    - Reviewed PR #456
    
    What I'll do today:
    - Continue dashboard redesign (from Jira backlog)
    - Pair programming with @dev2 on API migration
    
    Blockers: None
  ```
- **Kết quả**: Standup trong 30 giây thay vì 15 phút suy nghĩ.

#### 8. 📧 AI Email/Message Drafter

- **Mô tả**: Tạo email nháp từ gạch đầu dòng — giọng chuyên nghiệp, đúng mực, đa ngôn ngữ
- **Tech Stack**: LLM + Gmail API / Slack API
- **Module áp dụng**:
  - Module 05 — Prompt Builder (email templates, tone control), Few-shot Examples
  - Module 02 — Context Window (giữ ngữ cảnh cả chuỗi email)
- **Flow**:
  ```
  User: "draft email to boss: project delayed 2 weeks, need more resources, will update timeline"
    → LLM generates professional email with:
      - Appropriate greeting/closing
      - Structured paragraphs
      - Action items highlighted
      - Diplomatic tone
  ```
- **Kết quả**: Viết email chuyên nghiệp từ vài keywords, tiết kiệm 10-15 phút/email.

#### 9. 🔍 Codebase Q&A (Ask Your Code)

- **Mô tả**: Hỏi đáp với codebase — "function X làm gì?", "tại sao có bug này?", "ở đâu gọi function Y?"
- **Tech Stack**: LLM + AST Parser + Embedding + Code indexing
- **Module áp dụng**:
  - Module 01 — Vector Search (code chunks), Knowledge Graph (call graph)
  - Module 02 — Build Context (code + comments + git history)
  - Module 06 — Tool Selection (read_file, search_code, grep)
- **Flow**:
  ```
  User: "handlePayment() function làm gì và bị gọi ở đâu?"
    → Search: Find handlePayment definition
    → Search: Find all callers
    → Context: Build with code + tests + comments
    → LLM: Explain logic + list callers + potential issues
  ```
- **Kết quả**: Hiểu codebase nhanh hơn 5x, đặc biệt khi onboarding project mới.

#### 10. 📊 PR Summary & Changelog Generator

- **Mô tả**: Tóm tắt PR thành changelog entries, release notes tự động
- **Tech Stack**: LLM + Git diff + GitHub API
- **Module áp dụng**:
  - Module 01 — Retrieve PR context, linked issues
  - Module 05 — Prompt Builder (changelog template), Output Format
  - Module 10 — Git Automation (auto-generate on merge)
- **Flow**:
  ```
  PR merged → Webhook trigger
    → LLM analyzes diff + PR description + linked issues
    → Generates changelog entry:
    
    ### Added
    - User search API with fuzzy matching (#457)
    
    ### Fixed  
    - Login timeout on slow networks (#456)
    
    ### Changed
    - Upgraded auth library to v2.1
  ```
- **Kết quả**: Release notes tự động, không ai phải gõ tay changelog.

#### 11. 🗓️ Meeting Notes → Action Items

- **Mô tả**: Tự động extract action items từ meeting notes/recordings
- **Tech Stack**: LLM + Speech-to-Text (optional) + Task Manager API
- **Module áp dụng**:
  - Module 02 — Context Compression (tóm tắt meeting)
  - Module 05 — Prompt Builder (action item extraction), Output Format (JSON)
  - Module 08 — Task Classification, Priority
- **Flow**:
  ```
  Meeting notes / transcript input
    → LLM extracts:
      - Action items với assignees
      - Decisions made
      - Follow-up topics
      - Deadlines
    → Auto-create tasks in Jira/Trello/Notion
  ```
- **Kết quả**: Không bỏ lỡ action items, mỗi meeting đều có kết quả rõ ràng.

#### 12. 💡 Git Commit Message AI

- **Mô tả**: Tự động tạo commit message chuẩn từ git diff
- **Tech Stack**: LLM + Git hooks (commit-msg)
- **Module áp dụng**:
  - Module 05 — Prompt Builder (Conventional Commits template)
  - Module 10 — Git Automation (pre-commit hooks)
- **Flow**:
  ```
  git commit → pre-commit hook
    → Analyze staged changes (git diff --cached)
    → LLM generates:
      feat(auth): add OAuth2 login with Google
    
      - Add Google OAuth2 provider
      - Store refresh token in session
      - Handle token refresh on expiry
    
      Closes #123
  ```
- **Kết quả**: Commit messages chuẩn, consistent, có linked issues.

#### 13. 📖 Code Review Checklist Generator

- **Mô tả**: Tự động tạo checklist review tùy theo loại thay đổi (API change, DB migration, UI...)
- **Tech Stack**: LLM + Git diff analysis
- **Module áp dụng**:
  - Module 01 — Retrieve past review patterns, team conventions
  - Module 04 — Task Decomposition (break review into checklist items)
  - Module 05 — Prompt Builder (checklist templates)
- **Flow**:
  ```
  PR opened → Analyze changed files
    → Detect: "This PR modifies database schema"
    → Generate targeted checklist:
      ☐ Migration is reversible?
      ☐ Backward compatible?
      ☐ Indexes added for new queries?
      ☐ Seed data updated?
      ☐ Documentation updated?
  ```
- **Kết quả**: Code review toàn diện hơn, không bỏ sót edge cases.

> **Tóm gọn 1 câu:** Tám bot nhỏ phục vụ công việc hằng ngày — từ ghi log, viết standup, tới tóm tắt PR — mỗi cái build chưa tới 3 ngày.

---

### 📊 Tóm Tắt Daily-Use Projects

> **Cách đọc bảng này:** mỗi dòng là một dự án vừa nêu ở trên. "Tần suất dùng" = bạn sẽ dùng nó mấy lần một ngày;
> "Thời gian build" = mất bao lâu để dựng; "Tiết kiệm" = mỗi lần dùng đỡ tốn của bạn bao nhiêu thời gian.

| # | Dự án | Tần suất dùng | Thời gian build | Tiết kiệm |
|---|-------|---------------|-----------------|------------|
| 6 | Auto Daily Work Log | **Mỗi ngày** | 2-3 ngày | 15-20 phút/ngày |
| 7 | Smart Standup Bot | **Mỗi ngày** | 1-2 ngày | 10-15 phút/ngày |
| 8 | AI Email Drafter | **3-5 lần/ngày** | 1 ngày | 10-15 phút/lần |
| 9 | Codebase Q&A | **5-10 lần/ngày** | 2-3 ngày | 5-10 phút/lần |
| 10 | PR Changelog Generator | **Mỗi PR merge** | 1 ngày | 10-15 phút/PR |
| 11 | Meeting Notes → Actions | **Sau mỗi meeting** | 1-2 ngày | 15-20 phút/meeting |
| 12 | Git Commit Message AI | **Mỗi commit** | 0.5 ngày | 2-3 phút/commit |
| 13 | Code Review Checklist | **Mỗi PR** | 1 ngày | 5-10 phút/PR |

> **💰 Tổng thời gian tiết kiệm ước tính: 1-2 GIỜ/ngày** — ~20-40 giờ/tháng!
> 
> Ít nhất 1-2 dự án trong số này sẽ **hoàn lại công sức học framework** ngay trong tuần đầu tiên sử dụng.

> **Tóm gọn 1 câu:** Tám dự án nhỏ, mỗi cái chỉ tốn 0.5–3 ngày build, nhưng gộp lại tiết kiệm 1-2 giờ mỗi ngày cho công việc thật.

---

### 🟡 Cấp Độ Trung Bình — Cần Nhiều Modules (Module 01-08)

> **Mục này nói gì:** các dự án "béo" hơn — cần ghép 4-6 module, chạy production (tức dùng thật cho người dùng thật, không phải demo).

#### 14. 🏗️ Enterprise RAG Platform

- **Mô tả**: Hệ thống RAG production-grade với multi-source retrieval, caching, monitoring
  (production-grade = chất lượng đủ để dùng thật; caching = lưu sẵn kết quả đã tính để trả lời nhanh hơn lần sau)
- **Tech Stack**: Ollama + Qdrant + FastAPI + Redis (cache) + Prometheus
  (Qdrant = vector database; FastAPI = framework Python làm API; Redis = kho cache siêu nhanh; Prometheus = công cụ thu số liệu monitor)
- **⏱️ Thời gian build**: 2-3 tuần (MVP), 4-6 tuần (production-ready với monitoring)
- **Module áp dụng**:
  - Module 01 — Hybrid Search, Multi-Source Retrieval, Knowledge Graph
  - Module 02 — Hierarchical Context, Context Compression, Multi-turn
  - Module 03 — Memory Consolidation, Event Sourcing
  - Module 05 — Prompt Templates, Few-shot Examples, Guardrails
  - Module 07 — Pipeline Design, Error Recovery, Observability
- **Tính năng**: Multi-source ingestion → Hybrid search → Context assembly → Cached responses → Monitored pipeline
  (ingestion = nạp dữ liệu vào; context assembly = ghép các mảnh thông tin thành context hoàn chỉnh)
- **Kết quả**: Production RAG system xử lý 10K+ documents, <200ms latency (latency = thời gian chờ mỗi câu trả lời)

#### 15. 💬 Customer Support AI Agent

- **Mô tả**: Agent hỗ trợ khách hàng với khả năng tra cứu knowledge base, ticket system, escalation
- **Tech Stack**: LLM + Vector DB + Ticket API + WebSocket
- **⏱️ Thời gian build**: 2-3 tuần (basic chat + KB), 4-6 tuần (multi-turn + escalation + ticketing)
- **Module áp dụng**:
  - Module 01 — Retrieve from KB + order history + FAQ
  - Module 02 — Multi-turn Context, Context Window Management
  - Module 04 — Plan & Decompose (phân tích vấn đề → tìm giải pháp)
  - Module 05 — Prompt Builder (customer-facing prompts), Guardrails
  - Module 07 — Workflow (qualification → resolution → follow-up)
- **Tính năng**: Chat → Classify intent → Retrieve relevant docs → Resolve or Escalate
- **Kết quả**: Giải quyết 80% tickets tự động, escalation thông minh

#### 16. 📝 Smart Documentation Generator

- **Mô tả**: Tự động sinh documentation cho codebase từ source code + comments
- **Tech Stack**: LLM + AST Parser + Git + Markdown
- **⏱️ Thời gian build**: 1-2 tuần (single language), 3-4 tuần (multi-language + auto-commit)
- **Module áp dụng**:
  - Module 01 — Retrieve code context, existing docs
  - Module 02 — Build Context (code + comments + usage examples)
  - Module 05 — Prompt Builder (doc generation templates), Output Format
  - Module 10 — Git Automation (auto-commit docs), Code Generation
- **Tính năng**: Scan codebase → Extract API signatures → Generate docs → Auto-commit
- **Kết quả**: Documentation luôn updated, giảm 90% thời gian viết docs

#### 17. 🗓️ AI Task Manager

- **Mô tả**: Hệ thống quản lý task thông minh — phân loại, ưu tiên, decomposition, scheduling
- **Tech Stack**: LLM + SQLite + CLI/Web UI + Calendar API
- **⏱️ Thời gian build**: 1-2 tuần (CLI), 3-4 tuần (Web UI + calendar integration)
- **Module áp dụng**:
  - Module 04 — Task Decomposition, Planning Algorithms (Plan-and-Solve)
  - Module 05 — Prompt Builder (classification prompts)
  - Module 08 — Task Classification, Priority & Scheduling, Dependency Management
- **Tính năng**: Input task description → Auto-classify → Decompose → Prioritize → Schedule → Track
- **Kết quả**: Task phức tạp được tự động chia nhỏ và lên lịch thông minh

#### 18. 🔄 Memory-Augmented Chatbot

- **Mô tả**: Chatbot có bộ nhớ dài hạn — nhớ preferences, lịch sử trò chuyện, facts về user
- **Tech Stack**: LLM + Vector DB + SQLite (fact store) + Session management
- **⏱️ Thời gian build**: 2-3 tuần (basic memory), 4-6 tuần (consolidation + multi-session)
- **Module áp dụng**:
  - Module 02 — Multi-turn Context, Hierarchical Context
  - Module 03 — Write-back Memory, Memory Consolidation (merge/dedupe facts)
  - Module 05 — Prompt Builder (system prompt với remembered context)
- **Tính năng**: Chat → Extract facts → Store → Recall in future conversations
- **Kết quả**: Bot nhớ user preferences, personalize responses theo thời gian

> **Tóm gọn 1 câu:** Cấp trung bình là các hệ thống ghép nhiều module lại, đủ vững để chạy thật với người dùng thật.

---

### 🔴 Cấp Độ Nâng Cao — Hệ Thống Phức Táp (Module 04-11)

> **Mục này nói gì:** các dự án lớn nhất ngoài Expert — agent tự lập kế hoạch, tự code, tự sửa lỗi; cần hiểu chắc cả 11 module.

#### 19. 🤖 AI Coding Agent (Tự Xây Dựng)

- **Mô tả**: Tự xây agent kiểu Cline/Cursor — đọc code, chia task, viết code, review, test, commit
- **Tech Stack**: LLM + MCP Servers + Git + File System + Terminal
- **⏱️ Thời gian build**: 4-6 tuần (MVP đọc + viết code), 2-3 tháng (full pipeline review + test + commit)
- **Module áp dụng**:
  - Module 04 — ReAct Pattern (Thought → Action → Observation loop), Agent Workflows
  - Module 06 — Tool Selection, MCP Protocol, Tool Executor with Error Handling
  - Module 07 — State Machine (idle → planning → coding → reviewing → testing)
  - Module 08 — Task Decomposition, Dependency Management
- **Tính năng**: User request → Plan → Read files → Write code → Run tests → Fix errors → Commit
- **Kết quả**: Agent tự động hoàn thành coding tasks từ description (description = mô tả bằng chữ bạn đưa cho agent)

#### 20. 🏢 Multi-Agent Development Team

- **Mô tả**: Hệ thống nhiều agents phối hợp: Planner → Architect → Coder → Reviewer → Tester → Deployer
- **Tech Stack**: LLM + MCP + Message Queue (Redis/RabbitMQ) + Shared Memory
- **⏱️ Thời gian build**: 2-3 tháng (2 agents cơ bản), 4-6 tháng (full 6-agent pipeline)
- **Module áp dụng**:
  - Module 08 — Task Classification, Decomposition, Priority & Scheduling, Dependency DAG
  - Module 09 — Agent Roles, Communication Patterns, Orchestration, Shared Memory, Conflict Resolution
  - Module 07 — Workflow Patterns, Pipeline Design, Error Recovery
- **Tính năng**: Feature request → Planner decomposes → Architect designs → Coder implements → Reviewer reviews → Tester tests → Deployer deploys
- **Kết quả**: Full development pipeline tự động, mỗi agent là specialist

#### 21. 🔄 Self-Healing CI/CD Pipeline

- **Mô tả**: Pipeline CI/CD tự động — build, test, review, deploy, và tự sửa lỗi khi fail
- **Tech Stack**: GitHub Actions + LLM + Docker + Kubernetes + Prometheus + Grafana
- **⏱️ Thời gian build**: 2-3 tuần (basic auto-fix), 4-6 tuần (full self-healing + monitoring)
- **Module áp dụng**:
  - Module 07 — Error Recovery (retry, circuit breaker), Observability (logging, metrics)
  - Module 10 — CI/CD Pipelines, Git Automation, Monitoring & Alerts, Code Generation
  - Module 11 — Performance Benchmarks, Continuous Improvement
- **Tính năng**: Push → Build → Test → AI Review → Auto-fix failures → Deploy → Monitor → Rollback if needed
- **Kết quả**: Pipeline tự phục hồi 90% failures, giảm downtime

#### 22. 📈 AI-Powered Analytics Dashboard

- **Mô tả**: Dashboard tự động phân tích data, generate insights, cảnh báo anomalous
- **Tech Stack**: LLM + Pandas/SQL + Chart Library + Scheduler
- **⏱️ Thời gian build**: 2-3 tuần (single data source), 4-6 tuần (multi-source + anomaly detection)
- **Module áp dụng**:
  - Module 01 — Multi-Source Retrieval (data from multiple DBs/APIs)
  - Module 03 — Report Generation, Event Sourcing
  - Module 05 — Prompt Builder (analysis prompts), Output Format (charts, tables)
  - Module 10 — Scheduled Tasks, Monitoring & Alerts
  - Module 11 — Quality Metrics, Reporting & Dashboards
- **Tính năng**: Schedule phân tích → Query data → AI generates insights → Dashboard update → Alert on anomalies
- **Kết quả**: Automated business intelligence, proactive anomaly detection

#### 23. 🏥 Domain-Specific Research Assistant (Y tế/Legal/Finance)

- **Mô tả**: Trợ lý nghiên cứu chuyên ngành — trả lời câu hỏi từ papers, regulations, financial reports
- **Tech Stack**: LLM + Vector DB + Knowledge Graph + Citation tracking
- **⏱️ Thời gian build**: 3-4 tuần (basic Q&A), 6-8 tuần (CoT reasoning + citation tracking)
- **Module áp dụng**:
  - Module 01 — Knowledge Graph (entity relationships), Multi-Source Retrieval
  - Module 02 — Hierarchical Context (summary → detail), Context Compression
  - Module 04 — Planning Algorithms (research decomposition)
  - Module 05 — Guardrails (safety filters), Chain-of-Thought (reasoning)
  - Module 11 — Evaluation Dimensions (correctness, safety, faithfulness)
- **Tính năng**: Research question → Decompose sub-questions → Retrieve from papers/docs → Reason with CoT → Answer with citations
- **Kết quả**: Expert-level research assistance với verifiable sources (verifiable = có thể kiểm chứng lại được)

> **Tóm gọn 1 câu:** Cấp nâng cao là các hệ thống phức tạp: agent tự code, đội agent làm thay team, pipeline tự sửa lỗi, và trợ lý chuyên ngành có trích dẫn kiểm chứng được.

---

### 🟣 Cấp Độ Expert — Hệ Thống Tổng Hợp (Tất Cả Modules)

> **Mục này nói gì:** hai dự án "tổng hợp tất cả" — dùng mọi module trong framework, mất từ vài tháng tới cả năm. Là đích đến, không phải chỗ bắt đầu.

#### 24. 🌐 Autonomous AI Development Platform

- **Mô tả**: Nền tảng cho phép người dùng mô tả feature bằng ngôn ngữ tự nhiên, AI tự động phát triển
- **Tech Stack**: Full stack — LLM + MCP + Docker + CI/CD + Monitoring
- **⏱️ Thời gian build**: 3-6 tháng (MVP), 6-12 tháng (production-grade)
- **Module áp dụng**: **TẤT CẢ modules 01-11**
  - 01-03: Knowledge retrieval & memory management
  - 04-05: Planning & prompt engineering
  - 06-07: Tool selection & workflow orchestration
  - 08-09: Task management & multi-agent coordination
  - 10-11: Automation & continuous evaluation
- **Tính năng**: "Build a blog app with auth, posts, comments" → Auto-plan → Auto-code → Auto-test → Auto-deploy
- **Kết quả**: Nền tảng low-code/no-code với AI agent backbone

#### 25. 🧠 Adaptive Learning System

- **Mô tả**: Hệ thống học tập thích ứng — track knowledge gaps, gợi ý nội dung, spaced repetition
- **Tech Stack**: LLM + Vector DB + Scheduler + Analytics
- **⏱️ Thời gian build**: 2-3 tháng (basic tracking), 4-6 tháng (full adaptive + spaced repetition)
- **Module áp dụng**:
  - Module 01 — Retrieve learning materials, knowledge graph
  - Module 02 — Build personalized context for each learner
  - Module 03 — Write-back Memory (track what user learned/forgot)
  - Module 04 — Plan learning paths (adaptive difficulty)
  - Module 08 — Task Management (learning tasks, scheduling)
  - Module 11 — Evaluation (track progress, identify gaps)
- **Tính năng**: User learns → Track mastery → Identify gaps → Suggest next topics → Spaced repetition schedule
- **Kết quả**: Personalized learning path, optimized retention

#### 26. 🔐 AI Security Audit System

- **Mô tả**: Hệ thống audit security tự động — scan code, detect vulnerabilities, suggest fixes
- **Tech Stack**: LLM + SAST tools + Knowledge Graph + CI/CD
- **⏱️ Thời gian build**: 3-4 tuần (single scanner), 2-3 tháng (multi-agent + auto-fix + compliance)
- **Module áp dụng**:
  - Module 01 — Retrieve CVE database, security knowledge
  - Module 05 — Guardrails (safety, prompt injection prevention)
  - Module 07 — Workflow (scan → analyze → report → fix → verify)
  - Module 09 — Multi-agent (Scanner agent + Analyzer agent + Fixer agent)
  - Module 10 — CI/CD integration, Git Automation
  - Module 11 — Evaluation (security metrics, compliance)
- **Tính năng**: Code push → Security scan → AI analysis → Fix suggestions → Auto-PR fixes
- **Kết quả**: Automated security pipeline, compliance reporting

#### 27. 📱 Cross-Platform App Generator

- **Mô tả**: Tạo app đa nền tảng từ spec — Web + Mobile + API từ 1 specification
- **Tech Stack**: LLM + Code generation templates + MCP + Multi-repo management
- **⏱️ Thời gian build**: 2-3 tháng (single platform), 4-6 tháng (multi-platform parallel generation)
- **Module áp dụng**:
  - Module 04 — Plan & Decompose (feature → frontend + backend + API)
  - Module 06 — Tool Selection (choose framework, libraries)
  - Module 07 — Workflow (parallel generation for each platform)
  - Module 09 — Multi-agent (Frontend agent + Backend agent + API agent)
  - Module 10 — Code Generation Automation, Git Automation
- **Tính năng**: App spec → Architect designs API → Parallel code gen → Cross-platform build → Unified test
- **Kết quả**: Tạo MVP cho 3 platforms từ 1 spec trong vài giờ (MVP = bản tối thiểu dùng được; parallel = nhiều agent sinh code cùng lúc)

#### 28. 🏗️ Infrastructure-as-Code AI Assistant

- **Mô tả**: AI assistant cho DevOps — tự động generate Terraform/Docker/K8s configs từ requirements
- **Tech Stack**: LLM + MCP (Docker, K8s, Cloud APIs) + Git + Terraform
- **⏱️ Thời gian build**: 2-3 tháng (single cloud), 4-6 tháng (multi-cloud + validation + apply)
- **Module áp dụng**:
  - Module 01 — Retrieve infrastructure docs, best practices
  - Module 04 — Plan infrastructure (networking → compute → storage → monitoring)
  - Module 05 — Prompt Builder (IaC templates), Guardrails (security policies)
  - Module 06 — Tool Selection (Docker, K8s, AWS/GCP/Azure MCP tools)
  - Module 07 — Workflow (plan → generate → validate → apply → verify)
  - Module 10 — CI/CD for infrastructure, Monitoring
- **Tính năng**: "Deploy a scalable web app" → Generate Terraform + Docker + K8s + CI/CD configs
- **Kết quả**: Dựng hạ tầng tự động, đúng best practices

> **Tóm gọn 1 câu:** Hai dự án Expert dùng trọn 11 module, mất 3-12 tháng — là đích đến của lộ trình, không phải chỗ xuất phát.

---

### 📊 Tổng Quan Dự Án & Module

> **Cách đọc bảng này:** đây là bản liệt kê nhanh cả 20 dự án. Cột **Cấp độ** dùng màu: 🟢 dễ → 🟡 trung bình → 🔴 khó → 🟣 expert.
> Cột **Modules áp dụng** là các module bạn cần học trước. Độ phức tạp (số ⭐) càng nhiều càng khó.
> Lưu ý: số thứ tự trong bảng này khác với phần mô tả chi tiết ở trên (bảng gộp lại theo thứ tự dự án).

| # | Dự án | Cấp độ | Modules áp dụng | Độ phức tạp |
|---|-------|--------|-----------------|-------------|
| 1 | Personal Knowledge Base | 🟢 Cơ bản | 01, 03, 06 | ⭐⭐ |
| 2 | Document Q&A Chatbot | 🟢 Cơ bản | 01, 02, 05 | ⭐⭐ |
| 3 | Hybrid Search Engine | 🟢 Cơ bản | 01, 02 | ⭐⭐⭐ |
| 4 | Markdown to Structured Data | 🟢 Cơ bản | 03, 05 | ⭐⭐ |
| 5 | AI Code Review Bot | 🟢 Cơ bản | 05, 10 | ⭐⭐ |
| 6 | Enterprise RAG Platform | 🟡 Trung bình | 01, 02, 03, 05, 07 | ⭐⭐⭐⭐ |
| 7 | Customer Support AI Agent | 🟡 Trung bình | 01, 02, 04, 05, 07 | ⭐⭐⭐⭐ |
| 8 | Smart Documentation Generator | 🟡 Trung bình | 01, 02, 05, 10 | ⭐⭐⭐ |
| 9 | AI Task Manager | 🟡 Trung bình | 04, 05, 08 | ⭐⭐⭐ |
| 10 | Memory-Augmented Chatbot | 🟡 Trung bình | 02, 03, 05 | ⭐⭐⭐ |
| 11 | AI Coding Agent | 🔴 Nâng cao | 04, 06, 07, 08 | ⭐⭐⭐⭐⭐ |
| 12 | Multi-Agent Dev Team | 🔴 Nâng cao | 07, 08, 09 | ⭐⭐⭐⭐⭐ |
| 13 | Self-Healing CI/CD | 🔴 Nâng cao | 07, 10, 11 | ⭐⭐⭐⭐ |
| 14 | AI Analytics Dashboard | 🔴 Nâng cao | 01, 03, 05, 10, 11 | ⭐⭐⭐⭐ |
| 15 | Domain Research Assistant | 🔴 Nâng cao | 01, 02, 04, 05, 11 | ⭐⭐⭐⭐ |
| 16 | Autonomous Dev Platform | 🟣 Expert | 01-11 (tất cả) | ⭐⭐⭐⭐⭐ |
| 17 | Adaptive Learning System | 🟣 Expert | 01, 02, 03, 04, 08, 11 | ⭐⭐⭐⭐⭐ |
| 18 | AI Security Audit System | 🟣 Expert | 01, 05, 07, 09, 10, 11 | ⭐⭐⭐⭐⭐ |
| 19 | Cross-Platform App Generator | 🟣 Expert | 04, 06, 07, 09, 10 | ⭐⭐⭐⭐⭐ |
| 20 | Infrastructure-as-Code AI | 🟣 Expert | 01, 04, 05, 06, 07, 10 | ⭐⭐⭐⭐⭐ |

> **Tóm gọn 1 câu:** Bảng này là mục lục nhanh của 20 dự án — dùng để chọn dự án theo mức ⭐ và module cần học.

---

### 🗺️ Ma Trận Module → Dự Án

> Mỗi module giúp được bao nhiêu dự án — nhìn vào là bạn thấy ngay phần kiến thức nào đáng học nhất.
>
> **Cách đọc bảng:** cột **Số dự án sử dụng** = trong 20 dự án, có bao nhiêu cái cần module đó.
> Ví dụ "15/20" nghĩa là 15 trên 20 dự án đều dùng module 01 — nên học nó trước tiên.

| Module | Tên Module | Số dự án sử dụng | Dự án tiêu biểu |
|--------|-----------|------------------|-----------------|
| **01** | Retrieve Memory & Knowledge | **15/20** | Enterprise RAG, Research Assistant |
| **02** | Build Context | **12/20** | Customer Support Agent, Memory Chatbot |
| **03** | Update Memory Store | **10/20** | PKB, Memory Chatbot, Analytics Dashboard |
| **04** | Plan & Decompose | **10/20** | AI Coding Agent, Research Assistant |
| **05** | Prompt Builder | **15/20** | Gần như tất cả dự án |
| **06** | Decide Tools / MCP | **7/20** | AI Coding Agent, IaC Assistant |
| **07** | Workflow | **10/20** | Enterprise RAG, Multi-Agent, CI/CD |
| **08** | Task Management | **5/20** | AI Task Manager, Multi-Agent Dev Team |
| **09** | Multi-Agent | **5/20** | Multi-Agent Dev Team, Security Audit |
| **10** | Automation | **9/20** | CI/CD, Code Gen, Git Automation |
| **11** | Evaluation | **6/20** | Self-Healing CI/CD, Research Assistant |

> **Tóm gọn 1 câu:** Module 01 (Retrieve) và 05 (Prompt Builder) được dùng trong 15/20 dự án — học hai cái này trước là ăn chắc phần lớn giá trị.

---

### 📈 Lộ Trình Thực Hành Theo Cấp Độ

> **Mục này nói gì:** nếu chỉ có ~6 tháng rảnh buổi tối, hãy làm các dự án theo đúng thứ tự tuần này tới tuần khác như sơ đồ dưới.
> Số `#1`, `#6`... trỏ tới dự án cùng số ở phần trên.

```
🟢 CẤP ĐỘ CƠ BẢN (1-2 tuần mỗi dự án)
═══════════════════════════════════════
Tuần 1-2:  #1 Personal Knowledge Base
           → Học: Vector Search, Hybrid Search, KB Maintenance
           
Tuần 3-4:  #2 Document Q&A Chatbot
           → Học: Chunking, Embedding, Context Building, Prompt Templates
           
Tuần 5-6:  #3 Hybrid Search Engine
           → Học: BM25 + Vector kết hợp, Re-ranking, Context Compression

───────────────────────────────────────

🟡 CẤP ĐỘ TRUNG BÌNH (2-3 tuần mỗi dự án)
═══════════════════════════════════════
Tuần 7-9:  #6 Enterprise RAG Platform
           → Học: Pipeline Design, Error Recovery, Observability
           
Tuần 10-12: #7 Customer Support AI Agent
           → Học: Multi-turn Context, Planning, Workflow

───────────────────────────────────────

🔴 CẤP ĐỘ NÂNG CAO (3-4 tuần mỗi dự án)
═══════════════════════════════════════
Tuần 13-16: #11 AI Coding Agent
            → Học: ReAct Pattern, MCP Protocol, State Machine
           
Tuần 17-20: #12 Multi-Agent Development Team
            → Học: Agent Roles, Orchestration, Shared Memory

───────────────────────────────────────

🟣 CẤP ĐỘ EXPERT (4-6 tuần mỗi dự án)
═══════════════════════════════════════
Tuần 21-26: #16 Autonomous AI Development Platform
            → Học: Tổng hợp TẤT CẢ modules thành hệ thống hoàn chỉnh
```

> **Tóm gọn 1 câu:** Làm lần lượt 1 dự án nhỏ mỗi 2 tuần, từ dễ tới khó, là bạn phủ được toàn bộ framework trong khoảng nửa năm.

---

### 💼 Cơ Hội Nghề Nghiệp & Mức Lương

> **Cách đọc bảng này:** mỗi dòng là một nghề. Cột giữa cho biết framework dạy bạn đúng kỹ năng nào của nghề đó
> (theo số module). Lương là tham khảo năm 2025 — "M/tháng" = triệu Việt Nam mỗi tháng, "$K/năm" = nghìn đô la Mỹ mỗi năm.

| Vai trò | Kỹ năng cốt lõi từ Framework | Mức lương VN (2025) | Mức lương Global |
|---------|------------------------------|--------------------|--------------------|
| **AI Engineer** | Module 01-07: RAG, Agent, Workflow | 30-80M/tháng | $100K-200K/năm |
| **MLOps / AI Platform Engineer** | Module 07, 10, 11: Pipeline, CI/CD, Monitoring | 25-60M/tháng | $120K-180K/năm |
| **Backend Developer (AI-focused)** | Module 01-06: RAG integration, API design | 20-50M/tháng | $80K-150K/năm |
| **DevOps/SRE with AI** | Module 07, 10, 11: Self-healing, Automation | 25-60M/tháng | $100K-160K/năm |
| **Tech Lead (AI Products)** | Module 04, 08, 09: Planning, Multi-agent orchestration | 40-100M/tháng | $150K-250K/năm |
| **AI Freelancer / Consultant** | Toàn bộ framework: Build custom AI solutions | 50-200M/tháng (project-based) | $100-300/giờ |

> **Tóm gọn 1 câu:** Kỹ năng từ framework mở ra 6 hướng nghề, từ AI Engineer tới freelancer, với mức lương tham khảo 30-80 triệu/tháng ở VN.

---

### 💡 Tips Để Bắt Đầu

> **Mục này nói gì:** 4 nguyên tắc luyện tập để bạn không bỏ cuộc giữa chừng. Đọc sơ đồ dưới như một dàn ý: mỗi nhánh là một mẹo.

```
1. BẮT ĐẦU NHỎ
   ├── Đừng cố build "Autonomous Dev Platform" ngay
   ├── Bắt đầu với #1 (PKB) hoặc #2 (Document Q&A)
   └── Hiểu rõ fundamentals trước khi phức tạp hóa

2. BUILD IN PUBLIC
   ├── Viết blog về quá trình build mỗi dự án
   ├── Share trên GitHub để nhận feedback
   └── Tạo portfolio ấn tượng cho employer

3. ITERATE & COMBINE
   ├── Bắt đầu đơn giản → thêm features theo modules
   ├── Kết hợp 2-3 dự án nhỏ thành dự án lớn hơn
   └── VD: PKB (#1) + Doc Q&A (#2) = Enterprise RAG (#6)

4. FOCUS ON REAL PROBLEMS
   ├── Build giải quyết vấn đề THỰC SỰ của bạn
   ├── VD: Automate docs cho codebase công ty
   ├── VD: Chatbot trả lời câu hỏi từ SRS/PRD
   └── Real problems = Real portfolio = Real job opportunities
```

> **Tóm gọn 1 câu:** Bắt đầu từ dự án nhỏ nhất, làm vấn đề thật của chính mình, khoe tiến độ ra ngoài, rồi ghép dần các dự án nhỏ thành hệ thống lớn.

---

## 💡 Ví Dụ Thực Tế

> **Mục này nói gì:** hai minh họa nhanh cho "ghép module thành hệ thống": một pipeline RAG đơn giản và một đội nhiều agent chia nhau làm code.

### Ví dụ 1: Xây dựng RAG Pipeline đơn giản

<details>
<summary><b>Ví dụ 1: Xây dựng RAG Pipeline đơn giản (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/02-vi-du-1-xay-dung-rag-pipeline-on.py`](examples/02-vi-du-1-xay-dung-rag-pipeline-on.py)

</details>

> **Tóm gọn 1 câu:** Pipeline RAG đơn giản nhất gồm 3 bước: cắt tài liệu, biến thành vector, rồi nhét đoạn liên quan vào prompt cho model trả lời.

### Ví dụ 2: Multi-Agent Workflow

> **Đọc sơ đồ:** công việc chảy từ trái sang phải — Planner chia việc, Coder viết code, Reviewer soi, Tester kiểm tra, cuối cùng Deployer triển khai lên môi trường thật.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MULTI-AGENT CODING WORKFLOW                      │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Planner      │───►│  Coder        │───►│  Reviewer    │       │
│  │  (Phân tích)  │    │  (Viết code)  │    │  (Review)    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                    │                │
│         │                   │                    ▼                │
│         │                   │            ┌──────────────┐        │
│         │                   │            │  Tester       │        │
│         │                   │            │  (Test code)  │        │
│         │                   │            └──────────────┘        │
│         │                   │                    │                │
│         │                   │                    ▼                │
│         │                   │            ┌──────────────┐        │
│         └───────────────────┴───────────►│  Deployer     │        │
│                                         │  (Triển khai) │        │
│                                         └──────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Ghép các module theo đúng trật tự là bạn có ngay chatbot-tra-cứu-tài liệu hoặc cả đội AI chia nhau viết code.

---

## 📊 Tóm Tắt Kiến Thức

> **Cách đọc bảng này:** mỗi dòng là một kỹ năng. Ba cột Level cho thấy cùng một kỹ năng có 3 mức làm:
> Level 1 là cách thô nhất, Level 3 là cách "xịn" nhất. Ví dụ dòng Search: đếm từ khóa → so ý nghĩa → gộp cả hai rồi xếp lại hạng.

| Kỹ năng | Level 1 (Cơ bản) | Level 2 (Trung bình) | Level 3 (Nâng cao) |
|---------|-------------------|----------------------|---------------------|
| **Search** | Keyword search (BM25) | Vector search | Hybrid + Re-ranking |
| **Context** | Simple concatenation | Sliding window | Hierarchical + Compression |
| **Memory** | File-based | Vector store | Event sourcing + Consolidation |
| **Planning** | Sequential tasks | Parallel + Dependencies | Tree of Thought |
| **Tools** | Manual tool call | Rule-based selection | Intent classification + MCP |
| **Workflow** | Linear pipeline | State machine | Error recovery + Observability |
| **Multi-Agent** | Two agents | Orchestrated team | Shared memory + Conflict resolution |
| **Automation** | Simple scripts | CI/CD pipelines | Self-healing systems |
| **Evaluation** | Manual testing | Automated metrics | Continuous improvement loop |

> **Tóm gọn 1 câu:** Cùng một kỹ năng, bạn đi từ cách thô (level 1) tới cách chuẩn production (level 3) — bảng này là bản đồ nâng cấp từng bước.

---

## 🔗 Liên Kết Hữu Ích

> **Cách đọc bảng này:** các công cụ miễn phí hay dùng kèm framework. "Vector database" = nơi lưu và tìm các dãy số biểu diễn ý nghĩa.

| Nguồn | Mô tả |
|-------|-------|
| [Ollama](https://ollama.com) | Chạy LLM & Embedding local |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector search library |
| [ChromaDB](https://www.trychroma.com) | Embedded vector database |
| [MCP Protocol](https://modelcontextprotocol.io) | Model Context Protocol |
| [LangChain](https://langchain.com) | Framework cho LLM applications |
| [LlamaIndex](https://www.llamaindex.ai) | Data framework cho LLM |

> **Tóm gọn 1 câu:** Sáu công cụ nền tảng — Ollama chạy model, FAISS/ChromaDB lưu vector, MCP nối tool, LangChain/LlamaIndex ráp ứng dụng.

---

> **Ghi chú**: Mỗi module đều có README riêng kèm code mẫu. Bạn có thể đọc lẻ từng module, hoặc học lần lượt từ Phase 1 tới Phase 6 đều được.
