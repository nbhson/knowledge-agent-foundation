# 🔧 VI. Decide Tools / MCP Calls

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Tool Selection Patterns](#1-tool-selection-patterns)
>   - [1.1 Tool Registry](#11-tool-registry)
>   - [1.2 Example Tools — Extended Set](#12-example-tools-extended-set)
> - [2. Intent Classification](#2-intent-classification)
>   - [2.1 Multi-Strategy Intent Classifier](#21-multi-strategy-intent-classifier)
> - [3. MCP Protocol](#3-mcp-protocol)
>   - [3.1 MCP Architecture Deep Dive](#31-mcp-architecture-deep-dive)
>   - [3.2 MCP Client Implementation](#32-mcp-client-implementation)
> - [4. Tool Executor](#4-tool-executor)
> - [5. Function Calling](#5-function-calling)
> - [6. Tool Decision Pipeline](#6-tool-decision-pipeline)
> - [7. Tool Composition](#7-tool-composition)
> - [8. Permission System](#8-permission-system)
> - [9. Rate Limiting](#9-rate-limiting)
> - [10. Harness Integration](#10-harness-integration)
>   - [10.1 TypeScript Interfaces](#101-typescript-interfaces)
> - [11. Case Studies](#11-case-studies)
>   - [11.1. SWE-agent — Tool-Use for Software Engineering](#111-swe-agent-tool-use-for-software-engineering)
>   - [11.2. Claude Code — Hierarchical Tool Access](#112-claude-code-hierarchical-tool-access)
>   - [11.3. Cursor IDE — Context-Aware Tool Selection](#113-cursor-ide-context-aware-tool-selection)
> - [12. Design Principles](#12-design-principles)
>   - [12.1 SOLID Cho Tools](#121-solid-cho-tools)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do)
>   - [13.2 DON'T ❌](#132-dont)
> - [14. Testing](#14-testing)
> - [15. Advanced Patterns](#15-advanced-patterns)
>   - [15.1 Tool Learning](#151-tool-learning)
> - [16. Tương Lai](#16-tương-lai)
>   - [16.1 Xu Hướng 2026-2028](#161-xu-hướng-2026-2028)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks & Tools](#frameworks-tools)
>
---

### Câu Chuyện Mở Đầu

Hãy tưởng tượng bạn ghé vào một **tiệm sửa xe** đầy ắp đồ nghề: cờ lê, tua vít, máy khoan, máy hàn... Bác thợ lâu năm liếc qua là biết ngay phải cầm món nào. Còn anh học việc mới vào nghề thì lóng ngóng — có khi lại mang **máy khoan ra vặn con ốc nhỏ**, tệ hơn là **vác búa gõ vào lốc máy**.

**Agent AI mà thiếu khả năng chọn tool khôn ngoan thì cũng y hệt như vậy.**

Mô hình ngôn ngữ thì "biết" gọi tool đấy, nhưng khi trong tay có tới **50+ tools**, chỉ cần chọn nhầm một cái hay truyền sai tham số là đủ rắc rối: tốn token vô ích, nhận về kết quả sai bét, hoặc tệ nhất là gây ra **hậu quả khó cứu vãn** — như xóa nhầm file quan trọng, gửi nhầm email, hay châm ngòi cho một hành động không thể quay lại.

**Cách gỡ rối**: dựng một quy trình chọn tool rõ ràng từng bước — **nghe xem user thật sự muốn gì → chọn tool hợp nhất → kiểm tra tham số cho kỹ → chạy thử → ngó lại kết quả xem ổn không**.

> **Tóm gọn 1 câu:** Agent có 50+ tool trong tay mà chọn nhầm hoặc truyền sai tham số thì đốt token, ra kết quả sai, thậm chí gây hậu quả không cứu được — nên phải có quy trình chọn tool từng bước có kiểm soát.

### Tại Sao Tool Decision Quan Trọng?

> *"Có 50 cái tool trong tay mà chọn sai thì cũng như có cả hộp búa nhưng lại mang búa ra đập kính."*

#### 3 Bằng Chứng Khoa Học

*Cách đọc bảng này: mỗi dòng là một nghiên cứu thật; cột "Phát Hiện Quan Trọng" nói lên nghiên cứu đo được con số gì. Ví dụ, dòng 1 nghĩa là: chỉ cần cho agent quy trình chọn tool có cấu trúc, tỉ lệ gọi tool hỏng giảm 60%.*

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Anthropic MCP Research (2025)** | Agent sử dụng structured tool selection giảm **60% failed tool calls** so với unstructured approach |
| 2 | **LangChain Benchmark (2025)** | Tool selection accuracy tăng từ **65% lên 92%** khi sử dụng intent classification trước tool routing |
| 3 | **Princeton SWE-agent (2024)** | Giới hạn 50 search results + tool validation tăng **64% success rate** |

*Ghi chú thuật ngữ: "failed tool call" = lần gọi tool bị lỗi hoặc trả về kết quả vô dụng; "structured tool selection" = có quy trình chọn tool từng bước thay vì để model đoán mò; "intent classification" = bước đoán ý user trước khi chọn tool; "success rate" = tỉ lệ task giải xong trọn vẹn.*

#### Triết lý cốt lõi:

```
Tool Selection = Intent Classification → Tool Matching → Parameter Validation → Execution → Result Validation
```

**Nói cho dễ nhớ**: chọn tool cũng như bác sĩ kê đơn — phải bắt đúng bệnh (intent), bốc đúng thuốc (tool), dặn đúng liều (parameters), rồi còn hẹn tái khám xem thuốc có hợp không (result validation).

**Nếu làm ẩu bước này**: gọi nhầm tool là mất tiền token, nhận kết quả trật lất, thậm chí rước họa (xóa nhầm file, gửi nhầm mail...).

> **Tóm gọn 1 câu:** Nghiên cứu thật cho thấy chọn tool có quy trình (đoán ý → chọn → kiểm tra → chạy → soát lại) giảm hẳn lỗi và tăng tỉ lệ xong việc — như bác sĩ bắt bệnh rồi mới kê đơn.

## Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Decision là lúc agent quyết định "giờ dùng món nào, xài ra sao" — từ đọc đề bài, lựa tool, gọi API cho tới xử lý kết quả trả về.
>
> **Hình dung vui:** Module này là đôi "tay chân" của agent: mọi kế hoạch hay ho trong đầu (planning) muốn thành việc thật đều phải qua đây, giống cánh tay robot nghe lệnh từ bộ não (LLM) nhưng luôn có dây an toàn đi kèm.
>
> **Sao phải quan tâm:** Chọn đúng người, đúng việc, đúng cách thì xong việc; chọn ẩu là hỏng việc.

Nói ngắn gọn, agent lúc nào cũng quanh quẩn với hai câu hỏi: **việc này nên dùng tool nào?** và **gọi nó thế nào cho đúng?** Toàn bộ quá trình gói trong một vòng: đọc task → chọn tool → gọi API → xử gọn kết quả.

Trong Harness Engineering, Tool Decision chính là **"đôi tay"** biến kế hoạch trên giấy thành hành động thật. Tool nào muốn chạy cũng phải đi qua cổng kiểm soát, kiểm tra hợp lệ và ghi log đầy đủ.

```
┌──────────────────────────────────────────────────────────────────┐
│                 DECIDE TOOLS / MCP CALLS                          │
│                                                                  │
│  User Query                                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────┐                                             │
│  │  INTENT        │  Phân tích ý định user                     │
│  │  CLASSIFIER    │  "search" / "calculate" / "code" / ...     │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Chọn tool phù hợp từ danh sách            │
│  │  SELECTOR      │  "vector_search" / "calculator" / ...      │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  PARAMETER     │  Trích xuất & validate parameters           │
│  │  EXTRACTOR     │  query="BHYT", top_k=5, ...                │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  GUARDRAILS    │  Validate permission, safety, rate limit    │
│  │  CHECK         │                                             │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Gọi tool (function call / MCP)             │
│  │  EXECUTOR      │  Handle errors, timeout, retry              │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  RESULT        │  Parse kết quả → Format → Trả lời          │
│  │  PROCESSOR     │                                             │
│  └────────────────┘                                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Memory ←→ Guardrails ←→ Feedback ←→ Permissions          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

*Cách đọc sơ đồ: câu hỏi của user đi từ trên xuống qua 6 trạm — đoán ý (Intent Classifier) → chọn tool (Tool Selector) → nắn tham số (Parameter Extractor) → gác cổng an toàn (Guardrails Check) → chạy tool (Tool Executor) → xử lý kết quả (Result Processor). Mỗi trạm chỉ làm một việc và có thể chặn lại nếu bước trước không đạt.*

> **Tóm gọn 1 câu:** Tool Decision là "đôi tay" của agent: biến kế hoạch thành hành động thật qua 6 trạm kiểm soát, tool nào muốn chạy cũng phải qua cổng soát quyền và ghi log.

## Nội Dung

*Cách đọc bảng này: đây là mục lục chi tiết của cả bài; cột "Chủ đề" dẫn tới đúng mục, cột "Mô tả" tóm tắt mục đó nói về gì. Ví dụ, dòng 3 nghĩa là: mục MCP Protocol giải thích chi tiết chuẩn kết nối Model Context Protocol.*

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Tool Selection Patterns](#1-tool-selection-patterns) | Registry, search, categories |
| 2 | [Intent Classification](#2-intent-classification) | Rule-based & LLM-based |
| 3 | [MCP Protocol](#3-mcp-protocol) | Model Context Protocol chi tiết |
| 4 | [Tool Executor](#4-tool-executor) | Error handling, retries, logging |
| 5 | [Function Calling](#5-function-calling) | OpenAI style + parallel calls |
| 6 | [Tool Decision Pipeline](#6-tool-decision-pipeline) | End-to-end pipeline |
| 7 | [Tool Composition](#7-tool-composition) | Chain & parallel tool calls |
| 8 | [Permission System](#8-permission-system) | RBAC cho tools |
| 9 | [Rate Limiting](#9-rate-limiting) | Token/usage quotas |
| 10 | [Harness Integration](#10-harness-integration) | TypeScript interfaces |
| 11 | [Case Studies](#11-case-studies) | SWE-agent, Claude Code, Cursor |
| 12 | [Design Principles](#12-design-principles) | SOLID cho tools |
| 13 | [Best Practices](#13-best-practices) | DO/DON'T chi tiết |
| 14 | [Testing](#14-testing) | Unit & integration tests |
| 15 | [Advanced Patterns](#15-advanced-patterns) | Tool learning, dynamic tools |
| 16 | [Tương Lai](#16-tương-lai) | Xu hướng 2026-2028 |

> **Tóm gọn 1 câu:** Bài gồm 16 chủ đề xếp theo đúng vòng đời của một lần gọi tool — từ chọn tool, đoán ý, chuẩn MCP, chạy tool, tới phân quyền, test và xu hướng tương lai.

---

## 1. Tool Selection Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Selection Patterns là mấy "chiêu" chọn tool của agent khi đứng trước cả một kho tool (registry, tìm kiếm, phân loại theo nhóm) — gặp việc nào thì rút món nào cho hợp.
>
> **Hình dung vui:** Như bác thợ sửa xe đứng trước tủ đồ nghề đầy ắp: người lành nghề chẳng cần đọc hướng dẫn từng cây cờ lê mà liếc con ốc là biết phải cầm cây nào.
>
> **Sao phải quan tâm:** Chọn trúng ngay từ đầu thì đỡ tốn token, tránh gây chuyện ngoài ý muốn và tăng khả năng làm xong việc.

> **Tóm gọn 1 câu:** Tool Selection Patterns là bộ chiêu chọn tool đúng việc trong kho hàng chục món — chọn trúng thì tiết kiệm token và ít gây sự cố hơn.

### 1.1 Tool Registry

Mục này là cuốn "danh bạ" của cả nhà tool. `ToolDefinition` là tờ lý lịch của từng tool (tên gì, làm được gì, cần tham số nào, cần quyền gì, giới hạn gọi, timeout, chi phí...); còn `ToolRegistry` là bác quản thủ thư viện lo việc đăng ký, tìm kiếm, lọc theo nhóm, đánh dấu tool hết hạn và theo dõi xem tool nào chạy ngon, tool nào hay hỏng. Đọc thì cứ xem tờ lý lịch `ToolDefinition` trước, rồi ngó các hàm của `ToolRegistry` để biết "bác thủ thư" làm được những gì.

*Hình dung vui:* Như tủ thuốc dán nhãn cẩn thận — mỗi lọ ghi rõ công dụng (description), liều dùng (parameters), hạn dùng (deprecation date); còn registry là người giữ tủ, hỏi lọ nào là chỉ đúng ngăn đó.

> **Tóm gọn 1 câu:** Tool Registry là "danh bạ" quản lý mọi tool — mỗi tool có tờ lý lịch (`ToolDefinition`) ghi rõ làm được gì, cần tham số và quyền gì, còn registry lo đăng ký, tìm kiếm và theo dõi tool khỏe hay hỏng.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-tool-registry.py`](examples/01-1-1-tool-registry.py)

</details>

### 1.2 Example Tools — Extended Set

Mục này bày sẵn cho bạn một bộ tool "mở tủ là xài". Hàm `create_default_tools()` lần lượt đăng ký từng `ToolDefinition` vào `ToolRegistry` kèm tên, mô tả, tham số, nhóm và thẻ gợi nhớ. Để ý mấy tool nhạy cảm như `sql_query`, `execute_python`, `write_file` bị dán nhãn `requires_permission="elevated"` — tức là muốn chạy phải có quyền cao hơn mới được. Bộ tool này sẽ được xài chung cho các phần sau (phân loại ý định, chạy tool, viết test).

*Hình dung vui:* Như bộ hộp đồ nghề đóng sẵn cho người mới: khỏi phải đi chợ mua lẻ từng món, mở nắp ra là đủ đồ chơi cho hầu hết việc thường ngày.

> **Tóm gọn 1 câu:** Đây là bộ tool mẫu dựng sẵn qua `create_default_tools()`; tool nhạy cảm (viết file, chạy code, truy SQL) bị gắn cờ `requires_permission="elevated"` — nghĩa là phải có quyền cao hơn mới được chạy.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-1-2-example-tools-extended-set.py`](examples/02-1-2-example-tools-extended-set.py)

</details>

---

## 2. Intent Classification

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Intent Classification là bước "đoán ý" user: chỉ cần nghe câu hỏi là biết họ muốn tìm kiếm, tính toán, viết code hay lưu ghi nhớ... rồi dẫn tới đúng nhóm tool. Thường kết hợp hai kiểu: rule-based (soi từ khóa, nhanh mà rẻ) với embedding/LLM-based (hiểu sâu hơn, tốn kém hơn) để vừa nhanh vừa trúng.
>
> **Hình dung vui:** Như chị lễ tân khách sạn nghe khách mở miệng một câu là đoán được họ cần đặt phòng, gọi xe hay hỏi giờ ăn sáng, rồi chuyển máy đúng bộ phận.
>
> **Sao phải quan tâm:** Đoán sai ý là gọi sai tool, vừa đốt token vừa trả lời lạc đề; đoán trúng là đặt nền móng cho mọi bước sau.

> **Tóm gọn 1 câu:** Intent Classification là bước "đoán ý" user trước khi chọn tool — kết hợp soi từ khóa (nhanh, rẻ) và nhờ LLM đọc kỹ (chính xác, đắt) để vừa nhanh vừa trúng.

### 2.1 Multi-Strategy Intent Classifier

Mục này là bộ máy đoán ý ba tầng, đọc hiểu để xài lại. Tầng 1 là soi từ khóa (rule-based): thấy chữ "tìm", "tính", "đọc" là khoanh vùng ngay. Tầng 2 là nhờ LLM đọc kỹ rồi phán. Tầng 3 là chế độ auto: nếu rule đã chắc ăn (confidence từ 0.7 trở lên) thì tin luôn, còn lấn cấn mới gọi LLM cho chắc. Hàm `classify_multi_intent()` còn tách được câu dài nhiều ý, ví dụ "Đọc file và chạy test" thì tách thành hai ý [read, test].

*Hình dung vui:* Như quầy lễ tân có sẵn sổ kịch bản (rule) để trả lời nhanh mấy câu quen thuộc; chỉ khi gặp câu khoai mới nhấc máy gọi quản lý (LLM) xuống xử lý.

> **Tóm gọn 1 câu:** Bộ phân loại 3 tầng: soi từ khóa trước, LLM xử khi lấn cấn — rule đã chắc (confidence ≥ 0.7, tức độ tin cậy từ 70%) thì khỏi gọi LLM, còn `classify_multi_intent()` tách được câu nhiều ý ("Đọc file và chạy test" → [read, test]).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-1-multi-strategy-intent-classifier.py`](examples/03-2-1-multi-strategy-intent-classifier.py)

</details>

---

## 3. MCP Protocol

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** MCP Protocol (Model Context Protocol) là "ngôn ngữ chung" dựa trên JSON-RPC 2.0 để bất kỳ LLM nào cũng bắt chuyện được với tool bên ngoài: muốn biết có gì thì hỏi (tools/list), muốn xài thì gọi (tools/call), kèm theo resources và prompts — một chuẩn xài chung cho mọi nhà.
>
> **Hình dung vui:** Như cổng sạc USB-C: ngày xưa mỗi hãng một kiểu cáp riêng, giờ một chuẩn cắm được hết. MCP là "chuẩn cắm chung" để AI gắn tool của bất kỳ ai mà khỏi viết code riêng cho từng loại.
>
> **Sao phải quan tâm:** Không có chuẩn chung thì cứ mỗi cặp LLM-tool lại phải viết một cầu nối riêng; có chuẩn rồi thì hệ sinh thái tool lớn nhanh gấp bội.

> **Tóm gọn 1 câu:** MCP là "chuẩn cắm chung" kiểu USB-C giúp mọi LLM nói chuyện với mọi tool qua JSON-RPC 2.0 (giao thức nhắn tin dạng JSON) — hỏi có gì bằng `tools/list`, gọi tool bằng `tools/call`.

### 3.1 MCP Architecture Deep Dive

Đọc sơ đồ này ra sao? Có ba tầng rõ ràng. Tầng trên là HOST (nơi LLM chạy: Claude Desktop, app GPT, agent nhà trồng...); tầng dưới là các SERVERS (GitHub, Database, File, Web Search, Slack...) chuyên cung cấp tool. Ở giữa là đường dây JSON-RPC qua stdio/SSE/HTTP — như một tổng đài điện thoại chuẩn. Luồng chạy rất đời thường: LLM hỏi server "bên bạn có món gì hay" (tools/list), rồi gọi đúng món mình cần (tools/call). Dải cuối sơ đồ liệt kê hết các tính năng: thống nhất khả năng hỗ trợ (capabilities negotiation), đọc resource, dùng prompt mẫu, sampling và ghi log.

*Hình dung vui:* Như tổng đài điều xe: hãng xe (host) gọi theo đúng quy chuẩn tổng đài (protocol) tới các bác tài (servers), ai rảnh thì nhận cuốc — khỏi cần quen riêng từng bác tài.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MCP (MODEL CONTEXT PROTOCOL)                     │
│                                                                  │
│  MCP là giao thức chuẩn để LLM giao tiếp với tools bên ngoài  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    HOST (Client)                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ Claude   │  │ GPT-4    │  │ Custom   │              │   │
│  │  │ Desktop  │  │ App      │  │ Agent    │              │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │   │
│  │       └──────────────┼──────────────┘                    │   │
│  │                      ▼                                    │   │
│  │              MCP Client SDK                              │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │ JSON-RPC 2.0                           │
│                         │ (stdio/SSE/HTTP)                       │
│  ┌──────────────────────┴───────────────────────────────────┐   │
│  │                    SERVERS                                │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  GitHub     │  │  Database   │  │  File       │     │   │
│  │  │  Server     │  │  Server     │  │  Server     │     │   │
│  │  │  ─────────  │  │  ─────────  │  │  ─────────  │     │   │
│  │  │  - search   │  │  - query    │  │  - read     │     │   │
│  │  │  - create   │  │  - insert   │  │  - write    │     │   │
│  │  │  - update   │  │  - update   │  │  - delete   │     │   │
│  │  │  - delete   │  │  - schema   │  │  - list     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Web Search │  │  Slack      │  │  Custom     │     │   │
│  │  │  Server     │  │  Server     │  │  API Server │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Protocol Features:                                              │
│  ├── Capabilities negotiation                                   │
│  ├── Tool discovery (tools/list)                                │
│  ├── Tool execution (tools/call)                                │
│  ├── Resource access (resources/read)                           │
│  ├── Prompt templates (prompts/list, prompts/get)              │
│  ├── Sampling (sampling/createMessage)                          │
│  └── Logging (logging/setLevel)                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Kiến trúc MCP gồm 3 tầng — HOST (nơi LLM chạy), đường dây JSON-RPC (qua stdio/SSE/HTTP), và SERVERS (GitHub, Database, File...) — LLM hỏi "bên bạn có gì" (`tools/list`) rồi gọi đúng món cần (`tools/call`).

### 3.2 MCP Client Implementation

Mục này tặng bạn một client MCP đầy đủ để mang về xài ngay: `connect()` bắt tay với server và thống nhất khả năng hỗ trợ, `list_tools()` lấy danh sách tool về cache, `call_tool()` gọi tool có timeout và xử lý lỗi đàng hoàng, `read_resource()` đọc resource. Hàm `format_tools_for_llm()` biến tool MCP thành đúng "khẩu vị" từng nhà (OpenAI kiểu `type: function`, Anthropic kiểu khác). Lớp `MultiServerMCPManager` ở cuối lo quản nhiều server cùng lúc: gom tool về một mối, server này sập thì tự chuyển sang server khác. Nhớ bốn chữ để sống sót trong production: cache, timeout, định tuyến và dự phòng (fallback).

*Hình dung vui:* Như cô tổng đài viên dày dạn: thuộc lòng số máy nào giải quyết được việc gì; số này bận thì bấm ngay sang số dự phòng (failover).

> **Tóm gọn 1 câu:** Client MCP mẫu có đủ 4 thứ cần cho production: cache danh sách tool, timeout mỗi cuộc gọi, định tuyến tới đúng server, và fallback (server chính sập thì chuyển server dự phòng).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-3-2-mcp-client-implementation.py`](examples/04-3-2-mcp-client-implementation.py)

</details>

---

## 4. Tool Executor

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Executor là "người trực bếp" chuyên bấm nút chạy tool cho an toàn: kiểm tra tham số, soát quyền và giới hạn lượt gọi, chạy có hẹn giờ (timeout), hỏng thì thử lại theo kiểu backoff, và ghi log từng lần gọi — nằm giữa khâu chọn tool và kết quả trả về.
>
> **Hình dung vui:** Như anh bồi bàn kỹ tính: trước khi đưa order xuống bếp phải ngó lại — món này quán có bán không (tool tồn tại), còn nguyên liệu không (parameters), bếp có nhận không (permission, rate limit) — rồi mới đưa phiếu và đứng canh tới khi món ra lò (timeout, retry).
>
> **Sao phải quan tâm:** Đa số pha "toang" của agent đều từ tool gọi hỏng; executor là chỗ gom hết mớ rắc rối đó về một mối để xử lý gọn, dễ soi, không làm sập cả bữa ăn.

> **Tóm gọn 1 câu:** Tool Executor là "người trực bếp" chạy tool an toàn: kiểm tra tham số và quyền, chạy có hẹn giờ (timeout), hỏng thì thử lại kiểu backoff (chờ càng lúc càng lâu), và ghi log từng lần gọi.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-4-tool-executor.py`](examples/05-4-tool-executor.py)

</details>

---

## 5. Function Calling

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Function Calling là cách để LLM không chỉ "nói suông" mà còn biết "ra toa" hẳn hoi theo mẫu có sẵn — ví dụ gọi `calculator` kèm `{"expression": "2+3"}` — lại còn gọi nhiều tool một lượt (parallel calls) cho nhanh, đỡ phải chờ từng cái.
>
> **Hình dung vui:** Như bác sĩ kê toa thay vì kể chuyện: model "viết toa" (tool call kèm JSON) để dược sĩ (executor) bốc đúng thuốc đúng liều, thay vì để bệnh nhân tự về nhà sắc thuốc.
>
> **Sao phải quan tâm:** Đây là tiếng nói chung giữa LLM và code — nền tảng của mọi agent hiện đại, cũng là cách LLM "thò tay" ra thế giới bên ngoài.

> **Tóm gọn 1 câu:** Function Calling là cách LLM "ra toa" theo mẫu có sẵn (ví dụ `calculator` kèm `{"expression": "2+3"}`) và gọi nhiều tool cùng lúc (parallel calls) thay vì chỉ nói suông.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-5-function-calling.py`](examples/06-5-function-calling.py)

</details>

---

## 6. Tool Decision Pipeline

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Decision Pipeline là đường ống khép kín từ lúc nghe câu hỏi → đoán ý → lựa tool → nắn tham số cho chuẩn → chạy thử → soi lại kết quả, bước nào cũng có người gác cổng và sổ ghi chép.
>
> **Hình dung vui:** Như dây chuyền trong xưởng: đầu vào phân loại nguyên liệu (intent classification), giữa chuyền chọn máy và nạp liệu (tool matching + parameters), cuối chuyền kiểm hàng trước khi đóng thùng (result validation).
>
> **Sao phải quan tâm:** Gom hết chuyện chọn tool vào một ống duy nhất thì muốn gắn thêm chốt an toàn cũng dễ, muốn tìm chỗ hỏng cũng nhanh, muốn mở rộng cũng không sợ bung các chỗ khác.

> **Tóm gọn 1 câu:** Tool Decision Pipeline là đường ống khép kín: nghe câu hỏi → đoán ý → chọn tool → nắn tham số → chạy → soi lại kết quả, mỗi bước đều có người gác cổng.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-6-tool-decision-pipeline.py`](examples/07-6-tool-decision-pipeline.py)

</details>

---

## 7. Tool Composition

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tool Composition là nghệ thuật xâu nhiều tool lại với nhau — nối đuôi (chain), chạy song song (parallel), rẽ nhánh theo điều kiện (conditional) hay tỏa ra rồi gom lại (fan-out/fan-in) — để xử những việc khó mà một tool đơn lẻ làm không xuể.
>
> **Hình dung vui:** Như nấu một mâm cơm: nhiều đồ nghề bếp (thái, luộc, xào) phải chạy đúng thứ tự, có món làm song song (vừa luộc rau vừa nấu canh), có lúc lại rẽ nhánh tùy xem nếm thử mặn nhạt ra sao.
>
> **Sao phải quan tâm:** Việc đời thực hiếm khi xong bằng một tool; biết ghép tool thành quy trình là bước từ "chạy vặt từng món" lên "đứng bếp cả mâm".

> **Tóm gọn 1 câu:** Tool Composition là ghép nhiều tool thành quy trình — nối đuôi (chain), chạy song song, rẽ nhánh, tỏa ra rồi gom lại — để làm việc khó mà một tool không xuể.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-7-tool-composition.py`](examples/08-7-tool-composition.py)

</details>

---

## 8. Permission System

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Permission System là bộ phận "gác cổng" theo vai vế (RBAC): ai được đụng vào tool nào, theo vai (guest/user/power_user/admin) và theo mức (public/standard/elevated/admin), lần nào cho qua hay chặn lại cũng ghi sổ (audit log).
>
> **Hình dung vui:** Như thẻ ra vào công ty: khách chỉ loanh quanh được ở sảnh, nhân viên vào được văn phòng, còn phòng máy chủ thì chỉ quản lý mới có vân tay — mà mỗi lần quẹt thẻ đều để lại dấu vết.
>
> **Sao phải quan tâm:** Mấy tool như `write_file` hay `execute_python` mà xài bừa là gây chuyện khó cứu; phân quyền là hàng rào chắn mấy pha "táy máy" ngoài ý muốn của agent.

> 🔑 **Điểm cần nhớ về Policy / Permission:** đây là **ngã ba quyết định policy & permission** — vai trò (role) dẫn tới mức quyền → cho qua hay chặn lại + ghi audit. Muốn xem thi hành thật thì ghé `12-sandbox-execution` (§6 ma trận policy), muốn xem người duyệt thì ghé `15-approval-gates`, còn kiểm tra ngay trước giờ chạy thì nằm ở `tools/guardrails`.

> **Tóm gọn 1 câu:** Permission System gác cổng theo vai vế (RBAC = phân quyền theo vai trò, ví dụ guest/user/admin) và theo mức nhạy cảm của tool, mỗi lần cho qua hay chặn đều ghi sổ (audit log = nhật ký ai làm gì).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-8-permission-system.py`](examples/09-8-permission-system.py)

</details>

---

## 9. Rate Limiting

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Rate Limiting là cái "van tiết lưu" giới hạn số lần gọi tool trong một khoảng thời gian (ví dụ tối đa 60 lần/phút), với đủ kiểu van như fixed window, sliding window hay token bucket — để giữ ngân sách token, chặn phá hoại và giữ hệ thống khỏi quá tải.
>
> **Hình dung vui:** Như van giảm áp của bình nước: nước vẫn chảy đều nhưng không bao giờ xối xả — một vòi không thể hút cạn cả bể (abuse) và đường ống cũng khỏi lo bị vỡ (overload).
>
> **Sao phải quan tâm:** Agent mà loop cả trăm lần gọi tool trong một phút thì rate limit chính là phao cứu sinh cho ví tiền và sức khỏe hệ thống.

> **Tóm gọn 1 câu:** Rate Limiting là "van tiết lưu" chặn gọi tool quá nhiều trong một khoảng thời gian (ví dụ 60 lần/phút) — giữ ngân sách token, chống phá hoại và chống quá tải hệ thống.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-9-rate-limiting.py`](examples/10-9-rate-limiting.py)

</details>

---

## 10. Harness Integration

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Harness Integration là chấu cắm nối module chọn tool với cả nhà Harness — Memory, Guardrails, Feedback, Permissions — qua mấy bản interface TypeScript xài chung.
>
> **Hình dung vui:** Như đầu nối chuẩn của máy hút bụi đa năng: dù là bàn chải, đầu hút hay ống mềm, cứ đúng cỡ là cắm vào chạy được — interface TypeScript chính là cái cỡ chuẩn để các module gắn vào nhau.
>
> **Sao phải quan tâm:** Module hay mấy mà cắm không vừa harness thì cũng để ngắm; có interface chung thì cắm nhanh, test riêng từng món cũng dễ, món này đổi cũng không làm bung món kia.

> **Tóm gọn 1 câu:** Harness Integration là chấu cắm nối module chọn tool với Memory, Guardrails, Feedback, Permissions qua interface TypeScript dùng chung — cắm đúng chuẩn là harness nhận ngay.

### 10.1 TypeScript Interfaces

Mục này là tờ "hợp đồng mẫu" bằng TypeScript, ghi rõ một hệ thống chọn tool muốn chơi với harness thì phải có mặt mũi ra sao: đăng ký/lấy/liệt kê/tìm tool, `classifyIntent`, `executeTool`/`executeChain`/`executeParallel`, thêm `checkPermission`/`checkRateLimit` và `getStats`. Đọc thì cứ xem `interface` là điều khoản bắt buộc, còn class `HarnessToolDecisionSystem` là một bản làm mẫu cho thấy một lần gọi tool ngoài đời chạy qua các cửa nào: soát quyền → soát lượt gọi → bấm chạy → ghi sổ đo đạc. Sau này bạn viết module riêng, chỉ cần đúng hợp đồng là harness nhận ngay.

*Hình dung vui:* Như hợp đồng thuê văn phòng: interface là điều khoản chung ai cũng phải theo, class là cách từng bên tự trang trí văn phòng của mình.

> **Tóm gọn 1 câu:** Interface TypeScript là "hợp đồng mẫu" ghi rõ module chọn tool phải có những hàm gì (đăng ký, đoán ý, chạy tool, soát quyền, thống kê); class `HarnessToolDecisionSystem` là bản làm mẫu cho thấy một lần gọi chạy qua các cửa nào.

<details>
<summary><b>10.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/11-10-1-typescript-interfaces.ts`](examples/11-10-1-typescript-interfaces.ts)

</details>

---

## 11. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies là mấy câu chuyện người thật việc thật: mổ xẻ xem các sản phẩm AI xịn (SWE-agent, Claude Code, Cursor IDE, DeepSeek Harness) đang xài tool ra sao, để mình học lỏm chiêu hay về áp dụng.
>
> **Hình dung vui:** Như đọc chuyện nghề của đầu bếp nổi tiếng: không phải để bê nguyên công thức về, mà để ngấm cái nguyên tắc (thứ tự, an toàn, hợp ngữ cảnh) rồi tự nêm nếm cho vừa bếp nhà mình.
>
> **Sao phải quan tâm:** Mấy sản phẩm này đã trả học phí bằng tiền thật và người dùng thật để tối ưu; học họ thì mình khỏi phải phát minh lại cái bánh xe méo.

> **Tóm gọn 1 câu:** Case Studies mổ xẻ cách SWE-agent, Claude Code, Cursor IDE và DeepSeek Harness chọn tool thật — để học nguyên tắc thay vì phát minh lại từ đầu.

### 11.1. SWE-agent — Tool-Use for Software Engineering

*(Signpost: mục này xem SWE-agent — agent chuyên sửa code của Princeton — làm gì để gọi tool ít mà trúng.)*

**Chiêu dùng tool**: ít mà chất, tool nào cũng mô tả rõ ràng dễ hiểu.

```
Tools: read_file, search_code, edit_file, run_command

Key insight: "Read before edit" — SWE-agent always reads files first
to understand context before making changes.
```

**Kết quả**: tỉ lệ thành công 20.5% trên SWE-bench (+64% so với cách làm cũ)

*SWE-bench = kỳ thi chuẩn cho agent sửa code thật trên GitHub; "+64%" nghĩa là so với cách chọn tool cũ thì tỉ lệ giải xong bài tăng 64% (tương đối).*

> **Tóm gọn 1 câu:** SWE-agent dùng ít tool nhưng mô tả cực rõ và luôn "đọc file trước khi sửa" (read before edit) — giúp tăng 64% tỉ lệ giải bài trên SWE-bench.

### 11.2. Claude Code — Hierarchical Tool Access

*(Signpost: mục này xem Claude Code chia tool thành 4 tầng quyền, càng nguy hiểm càng khó đụng tới.)*

**Chiêu dùng tool**: phân quyền theo tầng, tool ghép được với nhau.

```
Layer 1 (always available): read_file, search_code
Layer 2 (standard): write_file, run_tests
Layer 3 (elevated): execute_command, delete_file
Layer 4 (admin): push_code, deploy
```

*Cách đọc: càng xuống dưới, tool càng nguy hiểm và càng khó được gọi — đọc file thì lúc nào cũng được, còn push code hay deploy (đem code lên môi trường thật) thì cần quyền admin.*

> **Tóm gọn 1 câu:** Claude Code xếp tool theo 4 tầng quyền — đọc/ tìm kiếm luôn mở, còn chạy lệnh, xóa file, deploy chỉ dành cho quyền cao — càng nguy hiểm càng gác chặt.

### 11.3. Cursor IDE — Context-Aware Tool Selection

**Chiêu dùng tool**: nhìn ngữ cảnh trong editor mà chọn tool (đang mở file gì, đang bôi đen đoạn nào...).

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/12-11-3-cursor-ide-context-aware-tool-selection.ts`](examples/12-11-3-cursor-ide-context-aware-tool-selection.ts)

</details>

> **Tóm gọn 1 câu:** Cursor chọn tool dựa trên ngữ cảnh editor — đang mở file gì, user đang bôi đen đoạn nào — thay vì chỉ dựa vào câu hỏi.

---

### 11.4. DeepSeek Harness — Code Mode SDK (`@deepseek-ai/dsh`)

**Bối cảnh**: DeepSeek Harness có một chế độ chạy gọi là **Code Mode** — sinh ra để xử nhanh gọn mấy task code chỉ cần chạy một lượt. Bạn dùng SDK `@deepseek-ai/dsh` để chạy code trong sandbox `vm` của Node.js, gom nhiều thao tác tool thành từng mẻ (batch) nên **nhẹ hơn hẳn 70-90% cả thời gian chờ lẫn tiền token** so với kiểu agent hỏi-đáp nhiều vòng.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/13-11-4-deepseek-harness-code-mode-sdk-deepseek.ts`](examples/13-11-4-deepseek-harness-code-mode-sdk-deepseek.ts)

</details>

**Mấy điểm ăn tiền**:

1. ✅ **Chạy một lượt là xong** — Cả task gói trong 1 script, khỏi vòng lặp LLM nhiều lượt
2. ✅ **Gom mẻ mà chạy** — `batchTools([...])` dồn nhiều tool calls vào 1 lần chạy, **đỡ chờ 70-90% thời gian**
3. ✅ **Nhốt trong sandbox VM** — Node.js `vm` context, không mạng, không thò tay ra ngoài chỗ cho phép
4. ✅ **Chạy lại y hệt** — Cùng script + cùng input là ra cùng output. Debug, test, CI/CD đều khỏe
5. ✅ **Đỡ tốn token** — Khỏi gửi kết quả tool về cho LLM tính bước tiếp. LLM chỉ cần gọi 1 lần (có khi 0 lần nếu code thuần)
6. ✅ **Song song mặc định** — `batchTools` cho mọi tool chạy cùng lúc tự động

**Code Mode so với kiểu thường**:

*Cách đọc bảng: so sánh hai cách agent chạy tool — kiểu cũ hỏi-đáp nhiều vòng (Standard Mode) và kiểu mới viết code chạy một mạch (Code Mode). Ví dụ, dòng "Token Cost": kiểu cũ tốn nhiều vì mỗi vòng gửi lại cả ngữ cảnh, kiểu mới đỡ 70-90%.*

| Aspect | Standard Mode | Code Mode (`@deepseek-ai/dsh`) |
|--------|---------------|-------------------------------|
| **Turns** | Multi-turn (5-20+) | Single-turn (1) |
| **Latency** | High (sequential LLM calls) | Low (batched, parallel) |
| **Token Cost** | High (full context each turn) | **70-90% less** |
| **Tools** | All tools | `bash`, `editor`, `llm_complete` only |
| **Isolation** | Process-level | VM sandbox (stronger) |
| **Determinism** | Non-deterministic | Deterministic (script-based) |
| **Use Case** | Open-ended tasks | Well-defined coding tasks |

**Đọc thêm code thật ở đâu**: xem chi tiết implementation trong [`code-mode-sdk.md`](code-mode-sdk.md)

> **Tóm gọn 1 câu:** Code Mode gói cả task vào 1 script chạy trong sandbox VM (Node.js `vm` — môi trường nhốt code không mạng, không đụng ngoài vùng cho phép): gom mẻ tool chạy song song, đỡ 70-90% thời gian và token so với kiểu hỏi-đáp nhiều vòng.

---

## 12. Design Principles

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ "luật làng" về kiến trúc phần mềm — ở đây là mang nguyên lý SOLID vào áp cho hệ thống quản lý và điều phối tools.
>
> **Hình dung vui:** Như quy hoạch khu phố trước khi cấp phép xây nhà: không cần biết từng căn sẽ sơn màu gì, nhưng móng, đường, điện nước ai cũng theo một chuẩn thì phố mới không thành mớ bòng bong.
>
> **Sao phải quan tâm:** Nhà tool nay nở mai thêm món mới liên tục; làm theo SOLID thì thêm món mới mà không làm sập món cũ.

> **Tóm gọn 1 câu:** Design Principles là "luật làng" kiến trúc — áp nguyên lý SOLID vào hệ thống tool để thêm tool mới không làm hỏng tool cũ.

### 12.1 SOLID Cho Tools

**1. Single Responsibility — Mỗi tool một nghề**
- Mỗi tool chỉ nhận một việc rõ ràng
- Đừng nhét cả tìm kiếm + ghi file vào chung một tool

**2. Open/Closed — Dễ thêm, khó vỡ**
- Thoải mái đăng ký tool mới (register)
- Hạn chế đụng chạm tool đang chạy ổn

**3. Liskov Substitution — Hàng nào cũng vừa khay**
- Tool nào cũng nói chung một interface
- Đổi tool này bằng tool khác mà chỗ cắm vẫn vừa

**4. Interface Segregation — Ai lo việc nấy**
- Tờ khai tool (definition) để riêng với người chạy tool (execution)
- Người gác cổng quyền (permission checker) để riêng với người chạy (executor)

**5. Dependency Inversion — Nhờ vào hợp đồng, đừng bám vào ruột**
- Tool nào cũng dựa vào abstraction `ToolRegistry`
- Đừng hardcode ruột gan từng tool vào code

*(SOLID là 5 nguyên tắc viết code dễ bảo trì; mỗi mục ở trên là cách hiểu nôm na của một chữ cái, ví dụ "hardcode" = ghi cứng chi tiết vào code khiến sau này khó thay.)*

> **Tóm gọn 1 câu:** SOLID cho tools: mỗi tool một nghề, thêm mới không phá cũ, mọi tool cùng một interface, tách rõ khai báo với thực thi, và nhờ vào hợp đồng chung thay vì ghi cứng chi tiết.

---

## 13. Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là cuốn "bí kíp" rút ra từ bao pha toát mồ hôi: việc nên làm (DO), việc nên tránh (DON'T) và mẹo tối ưu khi dựng hệ thống chọn tool.
>
> **Hình dung vui:** Như bảng nội quy an toàn trong xưởng: ghi rõ thao tác chuẩn (DO) và việc cấm tiệt (DON'T) để người mới vào không phải trả giá bằng đồ hỏng.
>
> **Sao phải quan tâm:** Đa số pha hỏng của hệ tool đều là lỗi hoàn toàn tránh được; đọc trước bảng này là hưởng ké bài học xương máu của người đi trước.

> **Tóm gọn 1 câu:** Best Practices là bảng nên làm (DO) và nên tránh (DON'T) rút ra từ lỗi thật: kiểm tra tham số, đặt timeout, ghi log, soát quyền — và đừng bao giờ chạy tool nguy hiểm mà không xin phép.

### 13.1 DO ✅

- **Kiểm tra tham số trước khi chạy**: chặn lỗi từ trong trứng
- **Thử lại theo kiểu backoff (càng lúc chờ càng lâu)**: đừng nện liên tục vào service đang ốm
- **Ghi log mọi lần gọi tool**: sau này debug hay tối ưu đều cần
- **Đặt timeout**: đừng để một cuộc gọi treo cả hệ thống
- **Soát quyền trước**: an toàn là trên hết
- **Theo dõi chi phí mỗi lần gọi**: giữ hầu bao cho chặt
- **Viết mô tả tool cho rõ ràng**: LLM cũng như người mới — mô tả ú ớ là làm sai
- **Xài song song cả rule-based lẫn LLM-based**: vừa nhanh vừa chắc
- **Cache danh sách tool**: đừng lần nào cũng đi hỏi lại từ đầu
- **Có tool dự phòng**: món chính hỏng thì còn món thay thế

> **Tóm gọn 1 câu:** Nên làm: kiểm tra trước khi chạy, retry kiểu backoff, đặt timeout, ghi log, soát quyền, mô tả tool rõ ràng, cache và có tool dự phòng.

### 13.2 DON'T ❌

- **Đừng bỏ qua kiểm tra tham số**: tham số bậy là sập ngay
- **Đừng coi thường rate limit**: bị khóa API là chuyện có thật
- **Đừng ghi cứng đường dẫn tool trong code**: cứ đi qua registry
- **Đừng quên xử lý lỗi**: tool nào cũng có ngày dở chứng
- **Đừng viết mô tả tool chung chung**: LLM không đoán mò giùm bạn đâu
- **Đừng cho thử lại vô hạn**: đặt trần số lần retry
- **Đừng chạy tool nguy hiểm mà không xin phép**: lúc nào cũng phải kiểm tra quyền
- **Đừng lờ tool đã deprecated**: dắt user sang tool mới cho nhẹ nhàng

*(deprecated = tool đã bị đánh dấu "cũ, sắp bỏ", không nên dùng nữa.)*

> **Tóm gọn 1 câu:** Không nên: bỏ qua kiểm tra tham số, lơ rate limit, ghi cứng đường dẫn tool, xử lý lỗi qua loa, retry vô hạn, hay chạy tool nguy hiểm không xin phép.

---

## 14. Testing

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing là khâu "tổng duyệt": viết unit test soi từng món (chọn tool, đoán ý, chạy tool, phân quyền, giới hạn lượt gọi) rồi viết integration test cho cả pipeline chạy liền một mạch.
>
> **Hình dung vui:** Như buổi tổng duyệt trước đêm diễn: từng diễn viên thoại riêng (unit test), rồi cả đoàn chạy liền vở (integration test) để bắt lỗi trước khi mở màn trước khán giả (production).
>
> **Sao phải quan tâm:** Tool gọi hỏng ngoài production là lỗi đắt nhất; bắt được lúc còn trên bàn test thì tiền sửa gần như bằng không.

> **Tóm gọn 1 câu:** Testing là "tổng duyệt" trước khi lên sóng: unit test soi từng món (chọn tool, đoán ý, phân quyền...), integration test cho cả pipeline chạy liền mạch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/14-14-testing.py`](examples/14-14-testing.py)

</details>

---

## 15. Advanced Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Advanced Patterns là mấy chiêu nâng cao như Tool Learning — để agent tự học cách xài tool mới ngay trong lúc chạy — cùng kiểu đăng ký tool động (dynamic registration).
>
> **Hình dung vui:** Như bạn nhân viên bán hàng mới: tuần đầu việc gì cũng phải giở sổ hướng dẫn, vài tháng sau tự biết món nào bán chạy, khâu nào dễ mất khách — càng làm càng thuộc bài mà chẳng cần ai sửa code giùm.
>
> **Sao phải quan tâm:** Hệ thống chạy càng lâu càng tự khôn ra — trúng nhiều hơn, chờ ít hơn, mà khỏi cần người canh chỉnh tay.

> **Tóm gọn 1 câu:** Advanced Patterns là mấy chiêu nâng cao: agent tự học cách dùng tool từ lịch sử chạy thật và hệ thống tự đăng ký tool mới (dynamic registration) mà không cần sửa code.

### 15.1 Tool Learning

Mục này chạy được trò gì? `ToolLearner` cặm cụi ghi sổ mỗi lần agent gọi tool: việc thuộc loại nào, xài tool nào, thành hay bại, chờ bao lâu (hàm `record`). Tới lúc cần chọn tool, hàm `recommend()` xếp hạng ứng viên theo tỉ lệ thành công rồi trừ điểm mấy anh chậm chạp; tool nào chưa từng xài thì cho điểm giữa giữa 0.5. Chiêu đơn giản mà là nền móng để agent tự khôn lên: rút kinh nghiệm từ sổ cũ thay vì chờ người sửa code.

*Hình dung vui:* Như app gọi xe nhớ mặt bác tài nào hay đón đúng giờ, chạy êm — lần sau ưu tiên gán xe của bác đó cho bạn.

> **Tóm gọn 1 câu:** `ToolLearner` ghi sổ mọi lần gọi tool rồi xếp hạng ứng viên theo tỉ lệ thành công (`recommend()`); tool chưa từng xài được điểm khởi đầu 0.5 — agent tự khôn lên từ dữ liệu cũ, không cần sửa code.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/15-15-1-tool-learning.py`](examples/15-15-1-tool-learning.py)

</details>

---

## 16. Tương Lai

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tương Lai là mục ngó trước mấy con sóng lớn của làng tool decision và MCP giai đoạn 2026-2028: chuẩn hóa giao thức, agent tự mò ra tool mới và tự gói wrapper, rồi chia sẻ tool giữa nhiều agent.
>
> **Hình dung vui:** Như coi dự báo thời tiết trước chuyến đi xa: không ai dám chắc 100%, nhưng ngó trước thì soạn hành lý (kiến trúc) mới đúng hướng.
>
> **Sao phải quan tâm:** Cách đặt móng hôm nay quyết định hai ba năm nữa bạn ung dung lướt sóng hay phải đập đi xây lại từ đầu.

> **Tóm gọn 1 câu:** Mục Tương Lai ngó trước 5 con sóng 2026-2028: agent tự mò tool, tự ghép tool, tool xài chéo mọi nơi, đoán trước nhu cầu, và tool an toàn kiểu zero-trust.

### 16.1 Xu Hướng 2026-2028

*(Signpost: mục này liệt kê 5 xu hướng, mỗi xu hướng kèm 3 việc sẽ xảy ra — đọc để biết mình nên đặt móng về hướng nào.)*

**1. Tự mò ra tool (Auto Tool Discovery)**
- Agent tự lần ra tool từ các MCP servers
- Tự gói wrapper cho tool lạ chưa gặp bao giờ
- Ghép tool theo nghĩa (semantic matching)

**2. AI tự ghép tool (Tool Composition AI)**
- Agent tự xâu tool thành quy trình
- Học chuỗi tool ngon từ lịch sử chạy thật
- Pipeline tự tối ưu dần

**3. Tool xài chéo mọi nơi (Cross-Platform Tools)**
- Tool mang từ agent này sang agent khác vẫn chạy
- Chợ tool theo chuẩn chung
- Một interface xài cho mọi nhà

**4. Đoán trước để dọn sẵn (Predictive Tool Use)**
- Đoán trước sẽ cần tool nào
- Hâm nóng kết nối từ sớm
- Lấy sẵn dữ liệu chờ đó

**5. Tool an toàn hơn (Tool Security)**
- Chạy tool kiểu zero-trust (không tin ai sẵn)
- Nhốt tool trong sandbox
- Việc nào cũng để lại vết audit

> **Tóm gọn 1 câu:** 5 xu hướng 2026-2028: tự mò tool, AI tự ghép tool, tool chạy chéo mọi nền tảng, đoán trước để dọn sẵn, và bảo mật zero-trust (không tin sẵn ai, nhốt sandbox, ghi vết từng việc).

## 17. Củng Cố Production: MCP, Ranh Giới Thực Thi, Memoization

> **Ghi chú sở hữu.** Mục này phụ trách phần **tầng tool** sở hữu: MCP client, các khai báo
> năng lực mà một tool phải công bố, và memoization. **Chính sách cách ly** (tier, 5 control
> bắt buộc, runner đã harden) do [`12-sandbox-execution`](../12-sandbox-execution/README.md) sở hữu;
> **phán quyết của con người** (risk tier, payload cổng, timeout-deny) do
> [`15-approval-gates`](../15-approval-gates/README.md) sở hữu. Cả hai là module cross-cutting
> bao quanh mọi tool call. Module này khai báo *tool cần gì*; 12 và 15 quyết định *tool có được không*.

*(Đọc chú thích này thế nào: mỗi mục trong tài liệu có "chủ sở hữu" — tức module chịu trách nhiệm chính. Sandbox và duyệt người thuộc module khác, nên ở đây chỉ nhắc tên để dẫn đường, không lặp lại nội dung.)*

> **Tóm gọn 1 câu:** Mục 17 lo ba thứ production: MCP client bền bỉ, tool phải khai báo "bán kính ảnh hưởng" (ghi đâu, gọi mạng đâu, irreversible không), và memoization (cache kết quả) — còn sandbox và phê duyệt thuộc module 12 và 15.

### 17.1 Định nghĩa

*Cách đọc bảng: cột "Thuật ngữ" là từ khóa, cột "Định nghĩa" giải thích ngắn, cột "Chủ sở hữu" chỉ module nào quản cái đó (mũi tên → nghĩa là thuộc module khác). Ví dụ, dòng Sandbox: tool/code không tin cậy phải chạy trong hộp kín Docker/microVM với allowlist FS (chỉ được ghi trong thư mục được phép) và không có mạng.*

| Thuật ngữ | Định nghĩa | Chủ sở hữu |
|------|------------|-------|
| Sandbox | Tool/code không tin cậy chạy trong Docker/microVM/gVisor với allowlist FS, mặc định không net, timeout+kill, không chứa secret env | → `12-sandbox-execution` |
| MCP client production | Auth (OAuth/xoay key), ghim `protocolVersion` + cache capability có TTL, `tools/list` ETag, giới hạn kích thước kết quả + cắt ngắn | module này |
| Cổng op nguy hiểm | Ghi/chạy/mạng/publish cần bản ghi approval tường minh (ai, cái gì, diff, hết hạn) | → `15-approval-gates` |
| Memoization | `(tool, args_hash)` giống nhau trong TTL trả kết quả cache; streaming nhả chunk một phần có trần | module này |

*(Ghi chú thuật ngữ: `args_hash` = "vân tay" của tham số gọi tool; TTL = time-to-live, thời hạn sống của cache; streaming = trả kết quả dần từng phần (chunk) thay vì gộp một lần; trần = giới hạn tối đa.)*

> **Tóm gọn 1 câu:** Bốn thuật ngữ nền: sandbox (nhốt code lạ), MCP client production (bền, có auth và cache), cổng op nguy hiểm (phải xin duyệt), memoization (cache kết quả theo TTL).

### 17.2 Ranh Giới Thực Thi — Phần Module Này Sở Hữu

Tool registry là nơi một tool *công bố* bán kính ảnh hưởng của nó; `12-sandbox-execution` là
nơi bản công bố đó được *cưỡng chế*. Việc của module này là giữ cho bản công bố đó trung thực:

1. **Mọi tool phải công bố năng lực, không chỉ tham số.** Cùng với `path`/`query`, một tool
   khai báo `net: ["api.example.com"]`, `allowWrite: ["src/**"]`, `secrets: ["EXAMPLE_API_KEY"]`
   và `irreversible: boolean`. Tool không khai báo gì sẽ nhận profile từ chối mặc định.
2. **Bản khai báo được version và có thể review.** Đổi `irreversible: false → true` là một
   diff có ý nghĩa bảo mật và phải qua cùng quy trình review với code; các tier cổng trong
   `15-approval-gates` được định khoá theo chính các field này.
3. **Executor từ chối mở rộng quyền.** Nếu runtime của tool yêu cầu nhiều hơn điều nó đã khai
   báo (ghi ngoài `allowWrite`, egress ra host không có trong `net`), harness chặn lời gọi và
   phát `tool_result` với `error: "capability-escalation"` — không cho qua trong im lặng.
4. **Rate limit và timeout cũng là phần khai báo của tool** (`rate_limit_per_minute`,
   `timeout_seconds` trong `ToolDefinition` ở trên), và deadline sandbox ở `12` phải
   `≥` timeout của tool để deadline ngoài không bao giờ nổ trước deadline trong.

Bộ quy tắc đầy đủ — tier cách ly, allowlist filesystem, network deny-by-default,
deadline + process-group kill, trần output, giữ secret, ma trận policy theo role,
và runner đã harden với image ghim theo digest — nằm ở
[`12-sandbox-execution`](../12-sandbox-execution/README.md). Hãy đọc module đó trước khi
viết bất kỳ dòng code nào spawn subprocess.

*(Gloss nhanh: "công bố năng lực" = tool tự khai báo được ghi file nào, gọi host nào, cần secret gì; `irreversible` = hành động không thể hoàn tác; "capability-escalation" = tool đòi quyền nhiều hơn đã khai báo; spawn subprocess = bật tiến trình con để chạy lệnh; image ghim theo digest = cố định đúng phiên bản container theo mã băm, không bị thay phiên âm thầm.)*

> **Tóm gọn 1 câu:** Mỗi tool phải khai báo năng lực (`net`, `allowWrite`, `secrets`, `irreversible`) ngay trong registry, khai báo thiếu hoặc đòi thêm quyền là bị chặn — còn quy tắc cách ly chi tiết thuộc module `12-sandbox-execution`.

### 17.3 Quy Tắc MCP Trong Production

> **Oct-2026:** spec stateless `2026-07-28` là bản mới nhất rồi nhé.
> Cách chuyển chi tiết từng bước xem ở [`2026-07-28-migration.md`](./2026-07-28-migration.md).
> Kiểu chào hỏi `initialize` và `Mcp-Session-Id` cũ bỏ hẳn.

1. Ghim `protocolVersion` **theo từng request** (`_meta` + header `MCP-Protocol-Version`, mặc định `"2026-07-28"`, giữ shim tương thích `"2025-06-18"`); cache `tools/list` theo `ttlMs/cacheScope` (fallback 5–15 phút); gặp `426`/tool lạ/`UnsupportedProtocolVersionError` thì vô hiệu ngay.
2. Auth: OAuth2 bearer có refresh + scope tối thiểu; xoay key; không bao giờ log token (redact `Bearer`).
3. Trần: `timeout 30s`, `kết quả ≤128KB`, `args ≤32KB`, validate args theo schema trước khi gửi.
4. Streaming: chuyển tiếp chunk `content` khi tới, áp trần tổng + idle timeout (10s); hủy khi client cancel.

*(Gloss nhanh: "ghim protocolVersion" = chốt cứng phiên bản giao thức từng request, không để server tự đổi; shim = lớp tương thích với bản cũ; cache theo TTL = giữ tạm danh sách tool vài phút rồi hỏi lại; `426` = mã HTTP "Upgrade Required" khi version không khớp; xoay key = định kỳ đổi khóa truy cập; redact = che thông tin nhạy cảm trước khi ghi log; idle timeout = ngắt nếu im lặng quá 10 giây.)*

> **Tóm gọn 1 câu:** MCP trong production có 4 luật: ghim phiên bản giao thức từng request, auth có xoay key và không log token, đặt trần (30s timeout, 128KB kết quả), và stream có giới hạn + ngắt khi im lặng.

<details>
<summary>TypeScript Code — Gọi MCP + Memoization (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/16-17-3-quy-tac-mcp-trong-production.ts`](examples/16-17-3-quy-tac-mcp-trong-production.ts)

> Runner subprocess có sandbox từng nằm ở đây đã chuyển sang
> [`12-sandbox-execution` §4.2](../12-sandbox-execution/README.md), nơi ghim image theo digest,
> chặn path traversal qua `realpath`, ép idle timeout, và redact secret khỏi output.
> Đừng đưa lại runner gắn tag `:latest` vào đây.

</details>

### 17.4 UX Approval Cho Op Nguy Hiểm

Taxonomy tier, payload cổng bắt buộc có bằng chứng, timeout-deny (fail closed), và audit
trail `approval_request` / `approval_verdict` đều do
[`15-approval-gates`](../15-approval-gates/README.md) sở hữu. Phần thuộc về đây là
**UX đồng ý phía tool**, vì tool definition chính là nơi người duyệt biết mình đang duyệt cái gì:

- **Hiển thị từ bản khai báo, không phải từ args thô.** Cổng hiện `command`, `cwd`, các file
  chạm tới, egress mạng, và cờ `irreversible` — tất cả đến từ năng lực tool đã khai báo (§17.2),
  không phải từ việc phân tích lại `args` tại thời điểm duyệt.
- **Tool không khai báo năng lực gì sẽ hiện thành bán kính ảnh hưởng không xác định**, điều này
  ép lên tier cao nhất. Không bao giờ để một tool có vẻ an toàn hơn thực tế.
- **Một click cho `write/exec`, gõ xác nhận cho `publish/delete/auth-change`** — nhưng cửa sổ
  hết hạn và luật hai-người đến từ `15`, không từ đây.
- **Tool MCP nhận nhãn server** trong prompt đồng ý. Duyệt một lời gọi tới MCP server từ xa
  là quyết định tin cậy khác hẳn việc duyệt một subprocess cục bộ.

*(Gloss nhanh: "payload cổng" = những gì hiện lên màn hình duyệt (command, file, mạng...); timeout-deny / fail closed = hết giờ chờ duyệt thì tự chặn, không tự cho qua; audit trail = vết ghi chép ai xin duyệt, ai phán quyết.)*

> **Tóm gọn 1 câu:** Phần UX duyệt của module này: hiện thông tin duyệt từ bản khai báo năng lực của tool (không đoán lại từ tham số), tool giấu năng lực thì xếp tier cao nhất, còn luật hết hạn và hai-người thuộc `15-approval-gates`.

### 17.5 Checklist

- [ ] Mọi tool có khai báo `net` / `allowWrite` / `secrets` / `irreversible`? Không khai báo = từ chối mặc định?
- [ ] Control sandbox đã đối chiếu với `12-sandbox-execution` (tắt net, allowlist FS, timeout+SIGKILL, trần output, không secret env, image ghim digest)?
- [ ] MCP: ghim version, cache giới hạn có TTL + vô hiệu, auth xoay vòng, trần kích thước/timeout?
- [ ] Op nguy hiểm qua cổng với xem trước diff + bản ghi approval hết hạn, theo `15-approval-gates`?
- [ ] Memo cuộc gọi giống nhau theo hash args chuẩn có TTL; streaming có trần?

> **Tóm gọn 1 câu:** Checklist 5 câu hỏi để tự soát trước khi lên production: khai báo năng lực đủ chưa, sandbox đúng chuẩn 12 chưa, MCP ghim version + trần chưa, op nguy hiểm có qua cổng duyệt, và memo/streaming có trần chưa.

---

## Tài Liệu Tham Khảo

*(Phần này liệt kê nguồn đọc thêm: bài nghiên cứu gốc và các framework/tool phổ biến — dùng khi muốn đào sâu hơn nội dung trong bài.)*

### Papers & Research

*(Cách đọc: mỗi mục gồm tên bài báo, tác giả + năm, và link arXiv — kho lưu trữ bài nghiên cứu mở miễn phí. Ví dụ, mục 1 là bài Toolformer, công trình đầu tiên chỉ ra LLM tự học dùng tool được.)*

1. **Toolformer: Language Models Can Teach Themselves to Use Tools**
   - Schick et al., 2023
   - https://arxiv.org/abs/2302.04761

2. **Gorilla: Large Language Model Connected with Massive APIs**
   - Patil et al., 2023
   - https://arxiv.org/abs/2305.15334

3. **API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs**
   - Li et al., 2023
   - https://arxiv.org/abs/2304.08354

4. **NexusRaven: Function Calling for LLMs**
   - Nexusflow, 2023
   - https://arxiv.org/abs/2312.15933

> **Tóm gọn 1 câu:** 4 bài nghiên cứu nền móng về LLM dùng tool: Toolformer (tự học), Gorilla (gọi API khổng lồ), API-Bank (đo chuẩn), NexusRaven (function calling).

### Frameworks & Tools

*(Cách đọc: đây là các bộ công cụ thật dùng ngay được — MCP là chuẩn kết nối, OpenAI/Anthropic là API của hai nhà cung cấp model lớn, LangChain và Semantic Kernel là framework dựng agent.)*

1. **MCP (Model Context Protocol)** - https://modelcontextprotocol.io
2. **OpenAI Function Calling** - https://platform.openai.com/docs
3. **Anthropic Tool Use** - https://docs.anthropic.com
4. **LangChain Tools** - https://langchain.com
5. **Semantic Kernel** - https://learn.microsoft.com/semantic-kernel

> **Tóm gọn 1 câu:** 5 công cụ/thư viện dùng thật: chuẩn MCP, function calling của OpenAI và Anthropic, framework LangChain và Semantic Kernel.

---

*Tài liệu: VI. Decide Tools / MCP Calls — HARNESS ENGINEERING EDITION*
*Ngày cập nhật: 16/10/2026 (stateless 2026-07-28: xem 2026-07-28-migration.md)*
*Ngày cập nhật: 10/2026 — MCP Ecosystem & Code Execution Pattern*

---

## Cập nhật 10/2026 — MCP Ecosystem & Code Execution Pattern

> **📌 Tóm tắt**
>
> Tháng 10/2026, hệ sinh thái MCP đã phát triển vượt bậc: spec `2026-07-28` hoàn thiện, hàng loạt AI clients hỗ trợ (Claude, ChatGPT, VS Code, Cursor, MCPJam...), và quan trọng nhất — mô hình **code execution với MCP** (Anthropic 11/2025) giúp agent viết code gọi MCP tools thay vì expose hàng chục tools riêng lẻ, giảm token và latency đáng kể.

> **Tóm gọn 1 câu:** Cập nhật 10/2026: hệ sinh thái MCP lớn mạnh (spec `2026-07-28`, nhiều client hỗ trợ) và xu hướng mới — agent viết code gọi tool theo mẻ thay vì lộ hàng chục tool riêng lẻ, tiết kiệm token và thời gian.

### 1. MCP Ecosystem 2026 — "USB-C cho AI"

**MCP** (Model Context Protocol) ngày càng trở thành chuẩn kết nối tool cho AI agents. Spec `2026-07-28` hoàn thiện nhiều tính năng mới:

*Cách đọc bảng: tóm tắt hiện trạng hệ sinh thái MCP — "Spec" là bản đặc tả (bản quy tắc giao thức) mới nhất, "MCP Apps" là loại ứng dụng chạy trong client AI, "Hỗ trợ rộng" là các phần mềm đã chơi được với MCP.*

| Thành phần | Mô tả |
|---|---|
| **Spec** | `2026-07-28` — định nghĩa đầy đủ tools, resources, prompts, sampling |
| **MCP Apps** | Các ứng dụng chạy trong AI clients (Cursor, VS Code, Claude Desktop...) |
| **Hỗ trợ rộng** | Claude, ChatGPT, VS Code, Cursor, MCPJam, nhiều nhà khác |
| **Mô tả gốc** | MCP = "USB-C cho AI" — kết nối unified thay vì mỗi nhà một kiểu |

> **Phân biệt MCP vs A2A:** Hai giao thức bổ sung nhau:
> - **MCP** (Model Context Protocol): Agent → Tool (gọi tool/services)
> - **A2A** (Agent-to-Agent): Agent → Agent (giao tiếp giữa các agents với nhau)
>
> A2A đã được tích hợp vào [Agentic AI Foundation 08/2026](https://github.com/agentprotocol/A2A) — Layer 4. MCP và A2A cùng tồn tại, phục vụ hai nhu cầu khác nhau.

> **Tóm gọn 1 câu:** MCP ("USB-C cho AI") là chuẩn kết nối agent ↔ tool, A2A là chuẩn kết nối agent ↔ agent — hai giao thức bổ sung nhau, không thay thế nhau.

### 2. Code Execution Pattern với MCP (Anthropic 11/2025)

**Bài toán cũ:** Khi agent kết nối nhiều MCP servers (mỗi server có 5-10 tools), tổng cộng có thể lên tới 50-100 tools. Mỗi tool description phải nằm trong context của mỗi LLM call → tốn **token + latency**.

**Giải pháp — Agent viết code gọi MCP tools:**

```
┌─────────────────────────────────────────────────────────────┐
│              CODE EXECUTION WITH MCP                        │
│                                                             │
│  Agent viết code:                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ # Agent viết code để gọi tool                       │   │
│  │ results = await mcp_batch([                          │   │
│  │   {"server": "filesystem", "tool": "read",           │   │
│  │    "args": {"path": "/data/a.txt"}},                │   │
│  │   {"server": "web", "tool": "search",                │   │
│  │    "args": {"query": "bug fixes"}},                 │   │
│  │   {"server": "db", "tool": "query",                 │   │
│  │    "args": {"sql": "SELECT * FROM logs"}},          │   │
│  │ ])                                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                    │
│       ▼                                                    │
│  Sandbox executor chạy code → gọi MCP servers              │
│       │                                                    │
│       ▼                                                    │
│  Chỉ TRẢ VỀ KẾT QUẢ TỔNG HỢP cho context                  │
│       (giảm token đáng kể so với expose 50+ tools)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**So sánh hai cách tiếp cận:**

*Cách đọc bảng: đối chiếu kiểu cũ (mỗi tool một mục riêng trong context) với kiểu mới (agent viết code gọi `mcp_batch_execute` một lần). Ví dụ, dòng "Token cost": kiểu cũ tốn nhiều token vì mô tả 50-100 tool luôn nằm trong context, kiểu mới chỉ gửi về kết quả tổng hợp.*

| Tiêu chí | Expose mỗi tool riêng lẻ | Code execution pattern |
|---|---|---|
| Số tools trong context | 50-100 tool descriptions | 1 tool `mcp_batch_execute` |
| Token cost | Cao (mỗi tool × mỗi call) | Thấp (chỉ kết quả aggregate) |
| Latency | Tăng theo số tools | Tương đương 1 tool call |
| Phù hợp | < 20 tools | Nhiều MCP servers, nhiều tools |
| Code complexity | Thấp | Trung bình (cần sandbox executor) |

> **Tóm gọn 1 câu:** Code execution pattern: thay vì nhét 50-100 mô tả tool vào context, agent viết một đoạn code gọi tool theo mẻ rồi chỉ trả kết quả tổng hợp — đỡ token, đỡ chờ, hợp hệ nhiều server.

### 3. Tool Design — Action Centered Intelligence (ACI)

Tool descriptions cần viết như **docstring cho junior developer** — rõ ràng, đầy đủ, không mơ hồ:

> 📄 **Code ví dụ:** [`examples/17-3-tool-design-action-centered-intelligence-aci.py`](examples/17-3-tool-design-action-centered-intelligence-aci.py)

**4 nguyên tắc ACI Tool Design:**

1. **Descriptions = docstring cho junior dev** — mô tả rõ input/output/error, không viết tắt
2. **Format gần text tự nhiên** — tool name dùng underscores, mô tả dạng câu
3. **Poka-yoke params** — dùng absolute paths, enums thay vì free-form strings, defaults rõ ràng
4. **Test tool với inputs thật** — đừng chỉ viết mô tả; phải chạy thử, nhất là edge cases

**Tránh bloated toolset:** 10 tool chất lượng tốt hơn 50 tool "cũng được".

*(Gloss nhanh: ACI = "trí tuệ đặt hành động làm trung tâm" — thiết kế tool để model dùng đúng ngay lần đầu; poka-yoke = kỹ thuật "chống nhầm" lấy từ sản xuất, ví dụ bắt dùng đường dẫn tuyệt đối thay vì để gõ tự do; bloated toolset = kho tool phình to nhưng rác, làm model khó chọn.)*

> **Tóm gọn 1 câu:** Thiết kế tool tốt = viết mô tả như docstring cho junior dev (rõ input/output/lỗi), tham số chống nhầm (enums, đường dẫn tuyệt đối), và test với dữ liệu thật — 10 tool ngon hơn 50 tool dở.

### 4. Python — Sandbox Executor Pattern

> 📄 **Code ví dụ:** [`examples/18-4-python-sandbox-executor-pattern.py`](examples/18-4-python-sandbox-executor-pattern.py)

> **Tóm gọn 1 câu:** Sandbox Executor Pattern bằng Python: chạy code agent sinh ra trong hộp kín có kiểm soát — mẫu thực thi an toàn cho code execution với MCP.

### 5. Cross-links

*(Phần này dẫn tới hai tài liệu liên quan: kiến trúc tổng thể của hệ thống và đặc tả Agent Skills.)*

- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)
- [agent-skills-spec.md](../05-prompt-builder/agent-skills-spec.md) — Agent Skills Open Standard (agentskills.io)

> **Tóm gọn 1 câu:** Đọc tiếp ở hai tài liệu: kiến trúc tổng thể (`AGENT_SYSTEM_ARCHITECTURE.md`) và chuẩn mở Agent Skills (`agent-skills-spec.md`).

*Tác giả: AI Knowledge Repository*