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

`harness/06-decide-tools-mcp` dạy bạn **quyết định nên dùng tool nào** — nhưng câu hỏi tiếp theo là *"kết nối chúng vào harness bằng cách nào?"*

Trước MCP, mỗi AI app phải tự viết integration cho từng tool: một adapter cho GitHub, một adapter cho database, một adapter cho file system... Lặp lại vô số lần, mỗi lần mỗi khác.

> *"MCP is the USB-C of AI tools — one standard, every device."*

**MCP (Model Context Protocol)** — protocol mở do Anthropic phát hành — chuẩn hóa cách AI apps kết nối với external tools và data. Thay vì viết N integrations, bạn viết **một server**, và **mọi MCP-compatible client** (Cline, Claude, VS Code...) đều dùng được.

### Tại Sao MCP Quan Trọng?

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Chuẩn hóa** | Một protocol (JSON-RPC) cho mọi tool/dữ liệu — không còn integration thủ công rời rạc |
| 2 | **Mở rộng liền mạch** | Thêm tool = thêm MCP server — harness/06 registry dễ dàng đăng ký tool mới |
| 3 | **Đã có sẵn trong repo** | `MCP_SETUP.md` cấu hình GitHub MCP server sẵn — dùng được ngay |
| 4 | **Harness/06 là "bộ não"** | `harness/06` quyết định *dùng tool nào* — MCP là *hạ tầng kết nối* để chạy quyết định đó |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  MCP ECOSYSTEM MAP VS HARNESS COMPONENTS                   │
│                                                            │
│  harness/06-decide-tools-mcp → quyết định dùng MCP nào     │
│  harness/06 tool registry   → đăng ký tools từ MCP servers│
│  MCP_SETUP.md (repo root)    → cấu hình GitHub MCP server  │
│  mcp-ecosystem/ (đây)       → tổng quan protocol + build  │
└────────────────────────────────────────────────────────────┘
```

```
Harness Tool Pipeline (harness/06):
  User Query → Intent → Tool Selector → chọn từ registry
      ↓
  Registry có tools từ 2 nguồn:
    ├─ Built-in tools   (file I/O, execute, search...)
    └─ MCP servers      (GitHub MCP, vector-db MCP, custom MCP...)
      → Tool Executor → Result Processor
```

## Tổng Quan

### MCP Là Gì?

**Model Context Protocol** — giao thức mở, cho phép AI applications kết nối với external tools và data sources thông qua một chuẩn chung:

| Khái niệm | Vai trò |
|-----------|---------|
| **MCP Server** | Cung cấp tools + resources (ví dụ: GitHub MCP server) |
| **MCP Client** | Ứng dụng AI tiêu thụ (Cline, Claude Desktop, VS Code...) |
| **Tools** | Hành động server thực thi — agent gọi như function |
| **Resources** | Dữ liệu server phơi bày — context cho agent |

### GitHub MCP Server (từ MCP_SETUP.md)

Repo này đã cấu hình sẵn GitHub MCP server tại `MCP_SETUP.md`:

```json
{
  "mcpServers": {
    "github.com/github/github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Khả năng**: quản lý repository, issues & PRs, GitHub Actions, code security, projects, discussions, gists, notifications...

```text
Ví dụ:
  "List my open pull requests"              → pull_request_read
  "Create an issue with title 'Bug: ...'"   → issue_write
  "Search Python repos about ML"            → search_repositories
```

### Nhanh Chóng Thêm MCP Server Khác

```jsonc
// cline_mcp_settings.json — thêm server mới
{
  "mcpServers": {
    "github.com/github/github-mcp-server": { /* ... đã có ... */ },
    "my-custom-tool": {
      "command": "npx",
      "args": ["-y", "@my-org/my-mcp-server"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
mcp-ecosystem/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Protocol, server/client, tools/resources, JSON-RPC
├── 02-setup/            ← (TODO) Cấu hình thêm MCP servers, auth, scopes
├── 03-patterns/         ← (TODO) Tool registry + MCP adapter, mixed built-in/MCP
├── 04-savings/          ← (TODO) Giảm code integration, shareable tools
└── 05-troubleshooting/  ← (TODO) Auth failures, server timeout, tool name conflicts
```

### Lộ Trình Đề Xuất

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

| Bạn muốn... | Đọc |
|-------------|-----|
| Quyết định dùng tool nào | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Cấu hình GitHub MCP server | [MCP_SETUP.md](../../../MCP_SETUP.md) |
| Tools registry & guardrails | [tools/guardrails](../guardrails/) |
| Vector DB qua MCP | [tools/vector-db](../vector-db/) |
| Xây harness bằng MCP tools | [tools/langchain](../langchain/) |

## Case Studies Thực Tế

### 1. GitHub MCP Trong Harness Loop

```
Loop "issue-triage" (từ loop/02-patterns):
  → MCP tool: list_issues        (đọc issues mở)
  → MCP tool: issue_read         (đọc chi tiết)
  → LLM phân loại severity/label
  → MCP tool: issue_write        (gán label, assignee)
  → MCP tool: add_issue_comment  (thông báo)
```

### 2. Registry Kết Hợp Built-in + MCP

```python
registry.register(ToolDefinition(
    name="github_search_code",
    source="mcp:github",          # đến từ MCP server
    description="Tìm code trong GitHub repos",
    parameters={"query": {"type": "string", "required": True}},
    category="search",
    requires_permission="standard",  # guardrails áp dụng như tool thường
    rate_limit_per_minute=30,
))
```

## Tài Liệu Tham Khảo

- **MCP Protocol**: https://modelcontextprotocol.io
- **MCP Spec (GitHub)**: https://github.com/modelcontextprotocol
- **GitHub MCP Server**: https://github.com/github/github-mcp-server
- **Cline MCP Docs**: https://docs.cline.bot/features/mcp

### Liên Kết Sang Nhánh Khác

- [MCP_SETUP.md](../../../MCP_SETUP.md) — Cấu hình GitHub MCP server (repo root)
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool decision & registry
- [tools/guardrails](../guardrails/) — An toàn tool calls từ MCP
- [tools/vector-db](../vector-db/) — Kết nối vector DB như MCP resource
- [tools/loop-cli](../loop-cli/) — Scaffold loops dùng MCP tools

---

> **"MCP turns tools from hardcoded integrations into pluggable capabilities."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — MCP Ecosystem*