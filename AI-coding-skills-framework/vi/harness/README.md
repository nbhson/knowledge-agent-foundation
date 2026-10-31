# Kiến Trúc Harness — Toàn Cảnh (01–15)

> Coi file này như tấm bản đồ xưởng: mỗi thư mục nằm ở đâu trong một harness thật, đi đường nào cho khỏi lạc.
> Muốn đọc lý thuyết gốc thì mở `../HARNESS_ENGINEERING.md`; muốn xem code tay thì vào `01/`–`15/`.
> Các modules `01–11` là từng chặng trên dây chuyền; `12–15` là lớp bao ngoài, chặng nào cũng chạm tới.

## 1. Harness Là Gì, Trong Một Sơ Đồ

Phần này định nghĩa "harness" bằng một sơ đồ — mọi phần sau đều dựa trên ý này.

Nếu gọi LLM một phát ăn ngay giống như hỏi đường người lạ — nhanh nhưng hên xui,
thì harness là **cả bộ máy dựng quanh LLM** để biến một câu hỏi lẻ
`prompt → completion` thành một kết quả có kiểm chứng, đi được tới nơi tới chốn:
`request → verified outcome` (yêu cầu người dùng → kết quả đã được kiểm chứng).

```
┌──────────────────────── VÒNG ĐỜI HARNESS THẬT ───────────────────────────────┐
│                                                                              │
│  User request                                                                │
│      │                                                                       │
│      ▼                                                                       │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │01 Retri│─▶│02 Build│─▶│04 Plan │─▶│05 Promp│─▶│06 Tools│─▶│ LLM    │        │
│  │eve     │  │Context │  │Decompo │  │Builder │  │Decide  │  │ call   │        │
│  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘  └────┬───┘        │
│       ▲                                                        │              │
│       │                                                   tool outputs        │
│       │                                                        │              │
│       │         ┌────────┐  ┌────────┐  ┌────────┐  ┌────────▼───┐            │
│       │         │03 Updat│◀─│11 Evalu│◀─│07 Workf│◀─│08 Task     │            │
│       │         │e Memory│  │ate     │  │low     │  │Execute    │            │
│       │         └────────┘  └────────┘  └────────┘  └────────────┘            │
│       │              ▲            ▲            │                              │
│       │              │            │            ▼                              │
│       │         ┌────┴────────────┴─────┐  ┌────────┐  ┌────────┐             │
│       └─────────│09 Multi-Agent (mở    │  │10 Autom│  │Guardrai│             │
│                 │   rộng khi cần)      │  │ation   │  │ls+Perms│             │
│                 └──────────────────────┘  └────────┘  │ (mọi   │             │
│                                                       │ bước)  │             │
│                                                       └────────┘             │
└──────────────────────────────────────────────────────────────────────────────┘
```

Nói nôm na có hai vòng quay lồng nhau. Vòng trong (mấy tool như Claude Code / opencode lo giùm bạn — agent tự gọi công cụ rồi tự đọc kết quả):
`LLM → tool_call → observation → LLM → … → stop`.
Vòng ngoài (việc của bạn, người thiết kế loop — lập kế hoạch rồi kiểm tra kết quả):
`plan → execute → validate → fix → persist → evaluate`.

> **Tóm gọn 1 câu:** Harness là bộ máy quanh LLM biến "gọi mô hình một lần" thành "hệ thống làm việc có kiểm chứng", gồm hai vòng lặp: vòng trong agent tự chạy, vòng ngoài bạn thiết kế.

## 2. Map 7 Components → 15 Modules

Về mặt logic, harness chỉ có 7 mảnh ghép. Repo này chẻ ra thành 11 modules theo chặng
cộng thêm 4 modules bao ngoài, để mỗi phần học riêng, test riêng cho đỡ rối.

Cách đọc bảng này: cột **#** là số thứ tự; cột **Thư mục module** là tên folder; cột **Component harness** là vai trò logic; cột **Trả lời câu hỏi** là vấn đề module đó giải quyết. Ví dụ, module 08 trả lời câu hỏi "một đơn vị việc track được là gì" — là module mỏng nhất nên nên bắt đầu đọc ở đây nếu lạc.

| # | Thư mục module | Component harness | Trả lời câu hỏi |
|---|----------------|-------------------|-----------------|
| 01 | `01-retrieve-memory-knowledge/` | Memory (đọc) | Agent nhớ gì cho relevant? Embedding, chunking, hybrid vector + BM25, rerank, các biến thể RAG. |
| 02 | `02-build-context/` | Context management | Nhồi gì vào token window, thứ tự nào, budget nào? Hierarchy 5 tầng, compression, routing, caching. |
| 03 | `03-update-memory-store/` | Memory (ghi) | Giữ lại gì sau task? Write-back, consolidation, versioning, audit. Đọc kèm: `trajectory-fork-replay.md`. |
| 04 | `04-plan-decompose-task/` | Orchestration (plan) | Chia mục tiêu lớn thành bước nhỏ verify được thế nào? Decomposition patterns, ReAct/ReWOO/ToT, replanning. |
| 05 | `05-prompt-builder/` | Guardrails (nắn input) | Ghép prompt cuối an toàn thế nào? Template, few-shot, CoT, schema enforcement, chống injection. |
| 06 | `06-decide-tools-mcp/` | Tools + Permissions | Agent được làm gì, qua tool nào? Registry, intent classification, MCP client, RBAC, sandbox. Đọc kèm: `code-mode-sdk.md`. |
| 07 | `07-workflow/` | Orchestration (run) | Bước chạy thứ tự nào, retry, bù lỗi ra sao? Sequential/parallel/DAG/HSM, saga, circuit breaker, tracing. Đọc kèm: `cordis-kernel-plugin.md`. |
| 08 | `08-task/` | Orchestration (đơn vị việc) | Một đơn vị track được là gì? Lifecycle, DAG deps, priority, budget, timeout/cancel. Module mỏng nhất — nếu lạc thì bắt đầu ở đây. |
| 09 | `09-multi-agent/` | Orchestration (scale-out) | Khi nào 1 agent thành 1 team? Role, protocol, shared memory, conflict resolution. Chỉ cần khi 04+07 quá tải. |
| 10 | `10-automation/` | Feedback (chạy định kỳ) | Cái gì chạy mà không cần human hỏi? CI/CD, scheduler, self-healing loop có guard iteration/cost. |
| 11 | `11-evaluation/` | Feedback (đo lường) | Có thực sự work không? Rubric, trajectory metrics, LLM-judge, regression, benchmark. Đọc kèm: `minimal-benchmark-harness.md`. |
| 12 | `12-sandbox-execution/` | **Cross-cutting: thực thi** | Code không tin cậy chạy ở đâu? Tầng cách ly, 5 controls bắt buộc, ma trận theo role. Nhà chính của khái niệm sandbox. |
| 13 | `13-trajectory-observability/` | **Cross-cutting: quan sát** | Mọi run ghi lại thế nào? Event contract, session stream, fork/replay/resume, join key. Bản đồ tới `03/.../trajectory-fork-replay.md` (engine). |
| 14 | `14-compaction-context/` | **Cross-cutting: context** | Run dài sống sót qua trần token thế nào? Policy 70%, pruning, contract memory, prompt compaction-safe. |
| 15 | `15-approval-gates/` | **Cross-cutting: kiểm soát** | Ai duyệt hành động không đảo ngược? Risk tier, gate payload, timeout-deny, pause/resume, audit. |

Nhớ một ý này là đủ: Guardrails + Permissions **không phải một chặng đứng riêng** — nó như lớp bảo vệ
bọc quanh mọi mũi tên trong sơ đồ trên (soi đầu vào, duyệt lúc gọi tool, chấm lại đầu ra).

> **Tóm gọn 1 câu:** 15 module = 11 chặng trên dây chuyền (nhớ → dựng ngữ cảnh → lập kế hoạch → công cụ → chạy → đo) cộng 4 lớp bao ngoài (sandbox, quan sát, nén, duyệt); guardrails và phân quyền là lớp bọc quanh mọi chặng chứ không phải một chặng.

## 3. Lifecycle Của Một Request, End to End

Phần này đi qua 10 chặng bằng một ví dụ thật, để bạn thấy các module ghép vào nhau ra sao.

Lấy ví dụ gần gũi là request *"Fix login bug"* — khách báo không đăng nhập được, mình lần theo từng chặng xem harness làm gì:

1. **Retrieve (01).** Mang câu hỏi đi embed (embed = biến câu hỏi thành dãy số để máy so độ giống nghĩa),
    lục cả kho vector lẫn BM25 kiểu lai (BM25 = thuật toán tìm theo từ khóa chính xác),
    rồi xếp hạng lại để lấy top-k. Kết quả là mấy đoạn chunks có điểm số. Trường hợp tìm không ra gì thì có đường dự phòng.
2. **Build context (02).** Gom hết đồ nghề vào một giỏ token (ví dụ 100k): lời dặn hệ thống + mục tiêu task + chunks
    mới tìm được + tóm tắt đoạn hội thoại trước + mấy file đang mở. Cái nào ít quan trọng thì bỏ trước. Nội dung lạ, chưa tin được thì dán nhãn riêng.
3. **Plan (04) → Task graph (08).** Chẻ việc lớn thành sơ đồ DAG dễ kiểm từng bước (DAG = sơ đồ việc, việc sau chỉ chạy khi việc trước xong):
    `reproduce → locate → patch → test`. Mỗi task có id, đầu vào, ngân sách,
    timeout, cờ báo có cần duyệt không.
4. **Build prompt (05).** Với từng task, đổ prompt ra từ template đã chốt version,
    kèm vài ví dụ mẫu, kèm luôn khung output phải theo.
5. **Decide tools (06).** Bộ phân loại ý định chọn xem task này xài tool nào
    (`read_file`, `run_tests`, …). Rồi soát quyền: task này có được ghi
    ra ngoài `src/` không? Gặp thao tác nguy hiểm thì dừng lại xin người duyệt.
6. **Execute workflow (07).** Cho DAG chạy. Việc nào dính nhau thì chạy nối tiếp, việc nào độc lập
    thì chạy song song. Lỗi thì thử lại kiểu backoff (nghỉ lâu dần giữa các lần thử), hỏng liên tục thì ngắt mạch (circuit breaker = hỏng liên tục thì dừng gọi, khỏi đốt tài nguyên), dở dang một nửa
    thì có cơ chế đền bù kiểu saga (saga = làm dở nửa chừng thì tự hoàn tác phần đã làm).
7. **Inner tool loop.** LLM gọi tools, harness cho chạy trong sandbox rồi trả
    kết quả quan sát về. Cuộc gọi nào giống nhau thì lấy từ cache, kết quả trả về quá to thì cắt bớt.
8. **Validate (11).** Soi lại: cú pháp ổn không, test có xanh không, chấm theo rubric bằng LLM-judge,
    đo thêm chỉ số đường chạy (bao nhiêu bước, gọi tool chuẩn không, tự phục hồi tốt không). Rớt thì quay lại lập kế hoạch
    hoặc đẩy lên người xử lý.
9. **Persist (03).** Cái gì đáng nhớ thì cất vào kho: mẹo làm đúng, fact mới biết,
    tóm tắt file. Có đánh version. Mấy thứ linh tinh, dùng một lần thì bỏ.
10. **Automate (10) / Scale out (09) — optional.** Muốn thì hẹn lịch chạy regression định kỳ (regression = chạy lại bộ test cũ để chắc không phá gì), hoặc
     tách team reviewer/tester cùng xài chung trí nhớ.

> **Tóm gọn 1 câu:** Một yêu cầu chạy qua 10 chặng — tìm dữ liệu, dựng ngữ cảnh, lập kế hoạch, dựng prompt, chọn công cụ, chạy workflow, gọi tool trong sandbox, kiểm chứng, ghi nhớ, tự động hoá — và mỗi chặng đều ghi lại sự kiện để tua lại được.

Vì mỗi chặng đều nhả ra **trajectory events** (xem §4 — trajectory = bản ghi từng bước agent đã làm), nên một lần chạy đều tua lại, rẽ nhánh thử,
hay lôi ra kiểm toán được (`03-update-memory-store/trajectory-fork-replay.md`).

### 3.1. RAG Pipeline Nằm Ở Đâu

Phần này trả lời câu hỏi hay nhầm: "RAG của tôi xong rồi, có cần gì nữa không?"

Pipeline RAG quen thuộc (tìm → xếp hạng lại → dựng context → gọi LLM) thực ra chỉ là
**mấy bước mở màn của lifecycle** — nó dừng ngay ở lần gọi LLM đầu tiên, còn harness
thì chạy tiếp từ đó về sau:

```mermaid
flowchart TD
    Q["🔍 User Query"]

    subgraph RET["① RETRIEVE = 01"]
        direction TB
        HS["HYBRID SEARCH"]
        SS["Semantic Search<br/>(vector DB)"] -->|matches by meaning| HS
        KS["Keyword Search<br/>(BM25)"] -->|exact keyword match| HS
        HS -->|RRF fusion merges results| COMB["Combined results"]
        KG["Knowledge Graph<br/>Retrieval"] -->|traverses entities + rels| COMB
        WS["Web/DB Search"] -->|searches external| COMB
    end

    Q --> RET
    COMB -->|"top-50 docs (raw)"| RERANK

    subgraph RERANK["② RE-RANKING = cuối 01"]
        direction TB
        SC1["(query, doc_1) → score 0.92 ✓ keep"]
        SC2["(query, doc_2) → score 0.87 ✓ keep"]
        SC3["(query, doc_3) → score 0.45 ✗ drop"]
        GOAL["Increase precision — keep only the top-K most accurate docs"]
    end

    RERANK -->|"top-5 docs (properly ranked)"| BUILD

    subgraph BUILD["③ BUILD CONTEXT = 02 + 05"]
        direction TB
        CONCAT["Concatenate top-K chunks into the prompt"]
        SYS["Add system instructions"]
        CMP["Compress if needed"]
        CONCAT --> SYS --> CMP
    end

    BUILD --> LLM["🧠 LLM (context augmented)"]
    LLM --> HARNESS["⇣ harness tiếp tục: 04 plan → 06 tools → 07 workflow → 08 task → 11 eval → 03 persist"]
```

Cách đọc bảng này: cột **Stage RAG** là bước nào trong pipeline RAG; cột **Module harness** là module sở hữu bước đó; cột **Ghi chú** là chi tiết thêm. Ví dụ, bước ① Retrieve (tìm tài liệu) thuộc module 01.

| Stage RAG | Module harness | Ghi chú |
|-----------|----------------|---------|
| ① Retrieve (hybrid + KG + web, top-50) | `01-retrieve-memory-knowledge` | Embedding, chunking, hybrid + RRF fusion, biến thể GraphRAG, nguồn external |
| ② Re-ranking (cross-encoder, top-5) | Cuối `01` (đầu vào `02`) | Chỉ lọc precision — chưa có gì vào prompt |
| ③ Build context (concat + system + compress) | `02-build-context` (+ `05-prompt-builder` render) | Merge system/goal/chunks/history/immediate vào token budget, đánh dấu untrusted content |
| 🧠 LLM | Inner tool loop (`06` → `07` → `08`) | RAG kết thúc ở đây; vòng harness (plan → execute → validate → persist) tiếp quản |

Chỗ này dễ hiểu nhầm nên nhấn mạnh: RAG **không phải làm một lần cho xong**. Cứ mỗi task mới, mỗi vòng
lặp trong mà câu hỏi đổi (ví dụ `04` lập lại kế hoạch → `01` đi tìm lại) là RAG chạy lại.
Chỉ có RAG không thì được con chatbot trả lời một câu cho hay; còn muốn agent làm trọn gói từ đầu tới cuối
thì phải có nốt phần còn lại của lifecycle.

> **Tóm gọn 1 câu:** RAG chỉ là ba bước mở màn (tìm → xếp hạng → dựng ngữ cảnh) và phải chạy lại mỗi khi câu hỏi đổi; muốn agent làm trọn gói thì cần nốt phần harness phía sau.

## 4. Ba Contract Dùng Chung

Phần này giới thiệu 3 "khung dữ liệu" mà các module phải dùng chung nếu muốn ghép được với nhau (contract = bản cam kết về hình dạng dữ liệu giữa các phần).

Nếu các modules chẳng thống nhất được gì khác, thì ít nhất hãy thống nhất 3 hình dạng này:

**A. Trajectory event** — cuốn sổ cái duy nhất để lần ra lỗi:

> 📄 **Code ví dụ:** [`examples/01-4-ba-contract-dung-chung.ts`](examples/01-4-ba-contract-dung-chung.ts)

**B. Context object** — bên 02 dựng lên, bên 05 mang đi nấu thành prompt:

> 📄 **Code ví dụ:** [`examples/02-4-ba-contract-dung-chung.ts`](examples/02-4-ba-contract-dung-chung.ts)

**C. Task node** — bên 04 đẻ ra, bên 07 cho chạy, bên 08 ngồi theo dõi:

> 📄 **Code ví dụ:** [`examples/03-4-ba-contract-dung-chung.ts`](examples/03-4-ba-contract-dung-chung.ts)

> **Tóm gọn 1 câu:** Dù làm gì, hãy thống nhất 3 khung dữ liệu chung: sự kiện đường chạy (trajectory), đối tượng ngữ cảnh, và node việc — vì chúng là các mối nối giữa các module.

## 5. Đọc Thư Mục Này Thế Nào

Phần này chỉ đường cho ba hoàn cảnh: mới học, muốn ráp nhanh, và đang debug.

- **Mới làm quen harness, chưa biết bắt đầu đâu?** Cứ đi theo lối này cho nhẹ đầu: `08` → `07` → `02` → `06` →
  `01` → `03` → `04` → `05` → `11` → `10` → `09`, rồi tới nhóm bao ngoài:
  `12` → `13` → `14` → `15`.
- **Muốn ráp một harness gọn nhẹ xài được ngay?** Ghép `02 + 05 + 06 + 07 + 11` là đủ chạy.
  Khi nào cần nhớ lâu thì thêm `01/03`, việc rắc rối hơn thì thêm `04/08`, `09/10` để dành cuối cùng.
- **Kẹt ở một lần chạy dở dang, không biết mò từ đâu?** Mở cuốn băng trajectory trước (`03/trajectory-fork-replay.md`),
  rồi lần tiếp: coi chừng `02` nấu context sai không, `06` chọn tool trật không, `11` chấm điểm lệch không.

> **Tóm gọn 1 câu (§5):** Ba lối đọc: mới học đi theo thứ tự 08 → … → 15, muốn chạy nhanh ghép 5 module tối thiểu, đang debug thì mở trajectory trước.

## 6. Docs Đi Kèm

Phần này liệt kê tài liệu chi tiết nằm trong từng thư mục module.

Cách đọc bảng này: cột **File** là đường dẫn; cột **Thêm gì ngoài README của module** là nội dung có trong file đó mà README thường không có.

| File | Thêm gì ngoài README của module |
|------|----------------------------------|
| `03-update-memory-store/trajectory-fork-replay.md` | Session event stream, implementation fork/replay/resume |
| `06-decide-tools-mcp/code-mode-sdk.md` | Pattern Code-mode vs JSON tool-call + sandbox sketch |
| `07-workflow/cordis-kernel-plugin.md` | Micro-kernel + plugin lifecycle, 4 runtime modes |
| `11-evaluation/minimal-benchmark-harness.md` | Harness isolation minimal để eval capability không bias |
| `../HARNESS_ENGINEERING.md` | Lý thuyết đầy đủ: 7 components, SOLID, 10 commandments, case studies (SWE-agent, Anthropic, Claude Code leak, Cursor, DeepSeek) |

> **Tóm gọn 1 câu (§6):** Mỗi thư mục module có thêm 1-2 tài liệu chuyên sâu (trajectory engine, code-mode SDK, micro-kernel, benchmark harness) — tra bảng trên để tìm đúng file.

## 7. Gap Đã Biết (Welcome Contributions)

Phần này liệt kê những việc chưa module nào nhận phụ trách — biết trước để khỏi tưởng đã phủ hết.

Mấy lỗ hổng bao ngoài hồi trước giờ đã có chỗ ở mới: sandbox dọn qua `12`, trajectory qua `13`,
compaction qua `14`, approval qua `15`. Còn mấy món chưa ai nhận: lọc PII/secret trong pipeline (PII = Personally Identifiable Information, thông tin nhận diện cá nhân; secret = mật khẩu, khoá API),
cách ly tenant cho sạch (cách ly dữ liệu giữa các khách hàng), trần chi phí tính theo task (SLO cost-per-task = cam kết trần chi phí cho mỗi nhiệm vụ). Còn gap lẻ của từng module
thì nằm trong mục bổ sung ở README của module đó.

> **Tóm gọn 1 câu:** Ba việc còn trống: dò-xoá dữ liệu cá nhân/mật khẩu, cách ly dữ liệu giữa các khách hàng, và cam kết trần chi phí theo nhiệm vụ — chỗ nào có thể đóng góp.

## 8. AI Coding Workflow Hiện Đại (2026)

Phần này cho thấy harness trong repo không phải lý thuyết suông: nó là cách các AI coding tool đang chạy thật.

Harness trong repo này không phải lý thuyết suông — nó chính là cách các AI coding tool đang chạy thật trong IDE:

Cách đọc bảng này: cột **Tool** là tên công cụ; cột **Harness trong đó** là các thành phần harness mà tool đó đang dùng thật.

| Tool | Harness trong đó |
|------|-----------------|
| **Claude Code** | Agentic loop + Agent Skills (SKILL.md) + compaction + subagents. Có SDK chính thức (**Claude Agent SDK**, trước đây là Claude Code SDK — đổi tên 09/2025) để embed loop này vào app riêng. |
| **GitHub Copilot (agent mode)** | 2025-2026: từ autocomplete → agent mode sửa nhiều file, chạy terminal, tự verify; Copilot coding agent nhận issue → mở PR. |
| **Cursor** | Multi-tab agent, Composer chạy nhiều file song song, background agents. |
| **opencode / OSS harness** | Pattern tương tự: MCP tools + approval gates + session trajectories. |

**Điểm chung 2026 (từ Anthropic, OpenAI, IBM, Google):**
1. **Multi-agent orchestration** là pattern chủ đạo — lead agent + subagents (xem `09-multi-agent/`), mỗi subagent có context riêng, trả về summary ngắn.
2. **Agent control plane**: một nơi điều phối nhiều agent chạy song song trên nhiều môi trường (browser, editor, CI) — hướng tới "Agentic OS".
3. **Giao thức chuẩn hoá**: MCP (agent↔tool, spec `2026-07-28`) + A2A (agent↔agent, Linux Foundation) — coding agent nào cũng chạy cả hai.
4. **Trust by Design**: security + approval gates wire vào mọi layer ngay từ đầu, thay vì audit sau (xem `15-approval-gates/`).

> **Tóm gọn 1 câu:** Các AI coding tool 2026 đều đang chạy đúng pattern harness này: multi-agent orchestration, control plane điều phối, giao thức chuẩn MCP/A2A, và bảo vệ-cổng duyệt cài từ đầu.

> Muốn hiểu sâu từng phần: `09-multi-agent/` cho orchestration, `10-automation/` cho loop tự chạy trong CI, `06-decide-tools-mcp/` cho MCP.
