# 🔌 MCP Ecosystem — Giao Thức Kết Nối AI ↔ Tools

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao MCP Quan Trọng?](#tại-sao-mcp-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Phần này giải thích MCP là gì và vì sao nó ra đời. Đọc xong bạn sẽ hiểu bức tranh lớn trước khi vào chi tiết.

`harness/06-decide-tools-mcp` chỉ bạn **nên xài tool nào** — nhưng câu hỏi tiếp theo mới nhức đầu: *"cắm chúng vào harness bằng cách nào?"*

Hồi chưa có MCP, mỗi AI app phải tự viết integration (bộ nối riêng) cho từng tool: một adapter cho GitHub, một adapter cho database, một adapter cho file system... Cứ lặp đi lặp lại, mỗi chỗ một kiểu khác nhau. Adapter = mảnh code trung gian, dịch lời gọi của app sang ngôn ngữ của tool.

> *"MCP is the USB-C of AI tools — one standard, every device."*

Câu này nghĩa là: MCP giống cổng USB-C — một chuẩn cắm chung, mọi thiết bị đều dùng được, khỏi cần mỗi máy một loại sạc.

**MCP (Model Context Protocol)** — protocol mở do Anthropic phát hành — đứng ra chuẩn hóa cách AI app bắt tay với tools và data bên ngoài. Protocol = bộ quy tắc nói chuyện chung, như luật giao thông giữa app và tool. Thay vì viết N integration, bạn chỉ viết **một server**, rồi **mọi client tương thích MCP** (Cline, Claude, VS Code...) đều xài được.

> **Tóm gọn 1 câu:** MCP là chuẩn kết nối chung giúp AI app xài mọi tool qua một cách cắm duy nhất, thay vì tự viết phần nối riêng cho từng tool.

### Tại Sao MCP Quan Trọng?

Cách đọc bảng này: cột # là số thứ tự, cột "Lý do" nêu điểm mạnh, cột "Giải thích" nói rõ điểm đó nghĩa là gì trong thực tế.

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Chuẩn hóa** | Một protocol (JSON-RPC) cho mọi tool/dữ liệu — không còn integration thủ công rời rạc |
| 2 | **Mở rộng liền mạch** | Thêm tool = thêm MCP server — harness/06 registry dễ dàng đăng ký tool mới |
| 3 | **Đã có sẵn trong repo** | `MCP_SETUP.md` cấu hình GitHub MCP server sẵn — dùng được ngay |
| 4 | **Harness/06 là "bộ não"** | `harness/06` quyết định *dùng tool nào* — MCP là *hạ tầng kết nối* để chạy quyết định đó |

Ví dụ cho dòng 1: JSON-RPC là cách gửi tin nhắn dạng JSON (văn bản có cấu trúc) để yêu cầu server chạy một hàm, ví dụ "list các pull request của tôi".

> **Tóm gọn 1 câu:** MCP đáng dùng vì nó thay hàng chục cách nối thủ công bằng một chuẩn duy nhất, và repo này đã cấu hình sẵn một server dùng được ngay.

### Quan Hệ Với Harness

Phần này định vị MCP trong bộ máy harness: MCP là **đường ống** chạy lệnh, còn harness/06 là **người ra quyết định** dùng lệnh nào.

```
┌────────────────────────────────────────────────────────────┐
│  MCP ECOSYSTEM MAP VS HARNESS COMPONENTS                   │
│                                                            │
│  harness/06-decide-tools-mcp → quyết định dùng MCP nào     │
│  harness/06 tool registry   → đăng ký tools từ MCP servers│
│  MCP_SETUP.md (instruction/)    → cấu hình GitHub MCP server  │
│  mcp-ecosystem/ (đây)       → tổng quan protocol + build  │
└────────────────────────────────────────────────────────────┘
```

Sơ đồ trên: mỗi dòng là một thành phần và vai trò của nó. "Registry" = danh mục các tool mà agent được phép gọi, như menu nhà hàng.

```
Harness Tool Pipeline (harness/06):
  User Query → Intent → Tool Selector → chọn từ registry
      ↓
  Registry có tools từ 2 nguồn:
    ├─ Built-in tools   (file I/O, execute, search...)
    └─ MCP servers      (GitHub MCP, vector-db MCP, custom MCP...)
      → Tool Executor → Result Processor
```

Đọc đường ống này từ trên xuống: câu hỏi của user → đo ý định → chọn tool trong registry → chạy tool → xử lý kết quả. Registry lấy tool từ 2 nguồn: tool có sẵn và tool qua MCP server.

> **Tóm gọn 1 câu:** MCP không thay harness/06 — nó là hạ tầng nối giúp harness/06 chạy được quyết định "dùng tool nào".

## Tổng Quan

Phần này định nghĩa các khái niệm cốt lõi của MCP, mỗi khái niệm một dòng.

### MCP Là Gì?

**Model Context Protocol** — một giao thức mở để AI app kết nối với tools và data bên ngoài qua cùng một chuẩn chung:

Cách đọc bảng này: cột "Khái niệm" là thuật ngữ, cột "Vai trò" giải thích nó làm gì kèm ví dụ cụ thể.

| Khái niệm | Vai trò |
|-----------|---------|
| **MCP Server** | Cung cấp tools + resources (ví dụ: GitHub MCP server) |
| **MCP Client** | Ứng dụng AI tiêu thụ (Cline, Claude Desktop, VS Code...) |
| **Tools** | Hành động server thực thi — agent gọi như function |
| **Resources** | Dữ liệu server phơi bày — context cho agent |

Hiểu nhanh: server = người phục vụ (nắm tool và dữ liệu); client = khách (app AI gọi nhờ); tool = hành động (tạo issue, đọc file); resource = dữ liệu được đọc (danh sách repo).

> **Tóm gọn 1 câu:** MCP có 4 khái niệm chính — server nắm tool, client là app AI gọi, tool là hành động, resource là dữ liệu.

### GitHub MCP Server (từ MCP_SETUP.md)

Phần này giới thiệu server đã cấu hình sẵn trong repo — bạn dùng được ngay, không cần cài thêm.

Repo này đã cấu hình sẵn GitHub MCP server tại `MCP_SETUP.md`:

> 📄 **Code ví dụ:** [`examples/01-github-mcp-server-tu-mcp-setup-md.json`](examples/01-github-mcp-server-tu-mcp-setup-md.json)

**Khả năng**: quản lý repository, issues & PRs, GitHub Actions, code security, projects, discussions, gists, notifications... Tức là gần như mọi việc bạn làm trên GitHub đều gọi được qua MCP.

```text
Ví dụ:
  "List my open pull requests"              → pull_request_read
  "Create an issue with title 'Bug: ...'"   → issue_write
  "Search Python repos about ML"            → search_repositories
```

Đọc ví dụ: câu trái là lời bạn nói với agent, mũi tên phải là tên tool MCP mà agent sẽ gọi. `issue_write` = tool ghi (tạo/sửa issue); `search_repositories` = tool tìm kiếm repo.

> **Tóm gọn 1 câu:** Repo này có sẵn GitHub MCP server, cho agent làm được mọi việc trên GitHub — từ đọc PR đến tạo issue — qua các tool có tên rõ ràng.

### Nhanh Chóng Thêm MCP Server Khác

Phần này trỏ tới file cấu hình mẫu để bạn cắm thêm server ngoài GitHub.

> 📄 **Code ví dụ:** [`examples/02-nhanh-chong-them-mcp-server-khac.json`](examples/02-nhanh-chong-them-mcp-server-khac.json)

> **Tóm gọn 1 câu:** Thêm một MCP server mới chỉ là thêm một mục cấu hình JSON theo mẫu có sẵn.

## Lộ Trình Học (Cấu Trúc Thư Mục)

Phần này vẽ bản đồ thư mục và gợi ý thứ tự đọc, để bạn không lạc đường.

```
mcp-ecosystem/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Protocol, server/client, tools/resources, JSON-RPC
├── 02-setup/            ← (TODO) Cấu hình thêm MCP servers, auth, scopes
├── 03-patterns/         ← (TODO) Tool registry + MCP adapter, mixed built-in/MCP
├── 04-savings/          ← (TODO) Giảm code integration, shareable tools
└── 05-troubleshooting/  ← (TODO) Auth failures, server timeout, tool name conflicts
```

Mỗi thư mục con là một chủ đề; TODO nghĩa là chưa viết xong. `auth` = đăng nhập xác thực; `scopes` = giới hạn quyền được làm gì; `adapter` = mảnh code nối tool vào registry.

### Lộ Trình Đề Xuất

Đây là thứ tự đọc từng bước, từ hiểu quyết định tới tự xây server.

```
Bước 1: Đọc harness/06-decide-tools-mcp — hiểu tool registry & quyết định
   ↓
Bước 2: Đọc MCP_SETUP.md — chạy thử GitHub MCP server hiện có
   ↓
Bước 3: Hiểu khái niệm protocol (server, client, tools, resources)
   ↓
Bước 4: Cấu hình thêm MCP server cho vector-db / custom tool (02-setup)
   ↓
Bước 5: Build MCP server riêng cho tool nội bộ (03-patterns)
```

Cách đọc bảng này: cột "Bạn muốn..." là mục tiêu của bạn, cột "Đọc" là file nên mở. Ví dụ, muốn biết agent chọn tool thế nào thì mở `harness/06-decide-tools-mcp`.

| Bạn muốn... | Đọc |
|-------------|-----|
| Quyết định dùng tool nào | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Cấu hình GitHub MCP server | [MCP_SETUP.md](../../../../instruction/MCP_SETUP.md) |
| Tools registry & guardrails | [tools/guardrails](../guardrails/) |
| Vector DB qua MCP | [tools/vector-db](../vector-db/) |
| Xây harness bằng MCP tools | [tools/langchain](../langchain/) |

Guardrails = "lan can an toàn" — bộ luật chặn agent gọi tool sai cách. Vector DB = cơ sở dữ liệu tìm kiếm theo ý nghĩa (không phải theo từ khóa đúng từng chữ).

> **Tóm gọn 1 câu:** Đọc theo 5 bước từ harness/06 → MCP_SETUP.md → khái niệm → thêm server → tự viết server; bảng cuối trỏ nhanh tới đúng file theo nhu cầu.

## Case Studies Thực Tế

Phần này cho thấy MCP chạy thật trong hai tình huống phổ biến.

### 1. GitHub MCP Trong Harness Loop

Loop = vòng lặp agent chạy tự động nhiều bước. Case này: agent tự phân loại issue trên GitHub.

```
Loop "issue-triage" (từ loop/02-patterns):
  → MCP tool: list_issues        (đọc issues mở)
  → MCP tool: issue_read         (đọc chi tiết)
  → LLM phân loại severity/label
  → MCP tool: issue_write        (gán label, assignee)
  → MCP tool: add_issue_comment  (thông báo)
```

Đọc từ trên xuống: đọc danh sách issue → đọc chi tiết → mô hình LLM (cỗ máy ngôn ngữ) gắn nhãn mức độ nghiêm trọng → ghi nhãn và người phụ trách → bình luận báo lại. Triage = phân loại ưu tiên, như y tá xếp lượt bệnh nhân.

> **Tóm gọn 1 câu:** Một loop xử lý issue chỉ gồm 4 tool MCP và 1 bước LLM phân loại — đó là minh họa nhỏ gọn nhất cho "harness + MCP".

### 2. Registry Kết Hợp Built-in + MCP

Case này cho thấy registry gộp cả tool có sẵn lẫn tool từ MCP server trong một danh sách duy nhất.

> 📄 **Code ví dụ:** [`examples/03-2-registry-ket-hop-built-in-mcp.py`](examples/03-2-registry-ket-hop-built-in-mcp.py)

Built-in = tool nằm sẵn trong harness (đọc file, chạy lệnh). Agent không cần biết tool nào đến từ nguồn nào — nó chỉ gọi tên.

> **Tóm gọn 1 câu:** Registry gộp built-in và MCP thành một menu duy nhất, nên agent gọi tool mà không cần biết nguồn gốc.

## Tài Liệu Tham Khảo

Phần này liệt kê link gốc để đọc sâu hơn ngoài repo.

- **MCP Protocol**: https://modelcontextprotocol.io
- **MCP Spec (GitHub)**: https://github.com/modelcontextprotocol
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **Cline MCP Docs**: https://docs.cline.bot/features/mcp

Spec = tài liệu đặc tả chính thức, quy định protocol phải hoạt động ra sao.

> **Tóm gọn 1 câu:** Link gốc đáng đọc nhất là modelcontextprotocol.io (spec chính thức) và repo github-mcp-server đang dùng trong repo này.

### Liên Kết Sang Nhánh Khác

Cách đọc: mỗi dòng là một file liên quan và nó giải quyết việc gì.

- [MCP_SETUP.md](../../../../instruction/MCP_SETUP.md) — Cấu hình GitHub MCP server (instruction/)
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool decision & registry
- [tools/guardrails](../guardrails/) — An toàn tool calls từ MCP
- [tools/vector-db](../vector-db/) — Kết nối vector DB như MCP resource
- [tools/loop-cli](../loop-cli/) — Scaffold loops dùng MCP tools

Scaffold = khung code mẫu sinh sẵn để bạn điền vào, không phải viết từ đầu.

> **Tóm gọn 1 câu:** Các link này nối MCP với các mảnh còn lại của hệ thống — quyết định tool (harness/06), an toàn (guardrails), dữ liệu (vector-db) và loop tự động.

---

> **"MCP turns tools from hardcoded integrations into pluggable capabilities."**

Dịch ý: MCP biến tool từ phần nối cứng (viết chặt vào app) thành thứ cắm rời được (cắm vào là chạy, rút ra là hết).

---

## ⚠️ Cập nhật 10/2026: MCP Spec 2026-07-28

Phần này tóm tắt bản spec mới nhất — những thay đổi bạn cần biết nếu cấu hình MCP từ đầu.

Spec MCP mới nhất (2026-07-28) có thay đổi lớn:

- **Streamable HTTP thay SSE:** HTTP+SSE (2024-11-05) deprecated. Streamable HTTP là transport chuẩn — stateless, request/response trên HTTP POST. Deprecated = chính thức khuyến khích bỏ; transport = cách dữ liệu di chuyển giữa client và server; stateless = server không nhớ phiên trước.
- **Stateless (bỏ handshake):** Không còn `initialize`/`notifications/initialized` handshake. Server không dùng session nữa. Handshake = bước chào hỏi thiết lập kết nối đầu tiên.
- **Protocol version header bắt buộc:** Mọi request HTTP phải có header `MCP-Protocol-Version: 2026-07-28`. Header = dòng thông tin gửi kèm mỗi request.
- **Elicitation:** Client có thể gửi request cho user input nhúng trong tool call. Nghĩa là giữa chừng tool có thể hỏi lại người dùng.
- **Sampling:** Server có thể yêu cầu client tạo LLM response (server-side sampling). Nghĩa là server mượn "bộ não" LLM của client để xử lý.
- **Registry spec:** Danh sách MCP servers có thể discover qua centralized registry. Discover = tự tìm và nhận ra server có sẵn.

Ref: https://modelcontextprotocol.io/specification/2026-07-28/

> **Tóm gọn 1 câu:** Bản spec 2026-07-28 đơn giản hóa kết nối (bỏ handshake, dùng Streamable HTTP stateless) và thêm tính năng mới (elicitation, sampling, registry).

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — MCP Ecosystem*
