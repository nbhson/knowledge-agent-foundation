# 🗜️ RTK (Rust Token Killer) — Tool Tối Ưu Context Cho Harness

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [RTK Có Phải Là Một Phần Của Harness Không?](#rtk-có-phải-là-một-phần-của-harness-không)
> - [Tại Sao RTK Quan Trọng?](#tại-sao-rtk-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Harness của bạn đã có tools, memory, context — nhưng có một kẻ ngốn context âm thầm: **bash output**. Mỗi lần agent chạy `git status`, `cargo test`, hay `ls`, nó nhận về hàng trăm dòng noise — và trong đống noise đó, agent dễ bỏ lỡ chính dòng lỗi cần sửa.

**RTK (Rust Token Killer)** là một CLI proxy viết bằng Rust, chèn mình vào giữa agent và shell command, cắt tới **90% bash output** trước khi nó chạm vào LLM context. Một binary duy nhất, hỗ trợ 100+ commands, overhead <10ms.

---

### RTK Có Phải Là Một Phần Của Harness Không?

### ✅ **CÓ — về mặt khái niệm.**

Theo [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md), harness gồm **7 components**. RTK thuộc **Component #3 — Context Management** (nhánh Context Optimization / Token Reduction), và liên quan phụ tới **Tools** (#1) và **Evaluation**:

| Component | Vai trò | RTK liên quan? |
|-----------|---------|----------------|
| **Context Management** (Hệ tuần hoàn) | AI luôn có đúng thông tin đúng lúc | 🟢 **TRỰC TIẾP** — nén Immediate Context (Level 5) |
| **Tools** (Tay chân) | Định nghĩa AI có thể làm gì | 🟡 Gián tiếp — RTK là tool proxy quanh shell |
| **Evaluation** | Đo lường hiệu quả | 🟡 Gián tiếp — `rtk gain` đo token saved |

**Mapping với thư mục `harness/`:**

| Module | Liên quan | Lý do |
|--------|-----------|-------|
| `harness/02-build-context` | 🟢 **Chính** | Context compression ở tầng Immediate Context |
| `harness/06-decide-tools-mcp` | 🟡 Phụ | Tool proxy design |
| `harness/11-evaluation` | 🟡 Phụ | `rtk gain` / `rtk discover` |

> **Phân biệt**: RTK là **công cụ thực thi cụ thể** (Rust binary), KHÔNG phải knowledge module như `harness/01-11` — nên nó sống trong nhánh `tools/`, cùng convention với `harness/` và `loop/`.

### Tại Sao RTK Quan Trọng?

> **"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."**

| # | Lý do | Bằng chứng |
|---|-------|------------|
| 1 | **Context Management** | RTK cắt tới 90% output `cargo test`/`git push` — agent có thêm không gian để reasoning trên đúng phần quan trọng |
| 2 | **Harness Evaluation** | `rtk gain` cung cấp số liệu token saved — ăn khớp mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md |
| 3 | **Hiện thực hóa lý thuyết** | Kỹ thuật "giới hạn output tool" trong module `06` được RTK hiện thực hóa ở tầng bash |

## Tổng Quan

RTK intercept shell commands và nén output bằng **4 chiến lược**:

| # | Chiến lược | Ví dụ |
|---|------------|-------|
| 1 | **Smart Filtering** (bỏ noise) | `git push` → `ok main` |
| 2 | **Grouping** (gom tương tự) | `ls` → tree với file counts |
| 3 | **Truncation** (giữ phần quan trọng) | `git diff` → bỏ headers |
| 4 | **Deduplication** (gộp log lặp) | `docker logs` → `×42 repeated line` |

Hỗ trợ **16 AI coding tools** qua hook/plugin: Claude Code, Cline, Copilot VS Code, Gemini CLI, Codex, Cursor, Windsurf, OpenCode...

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
rtk/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + case studies
├── 01-concepts/         ← Kiến trúc: hook system, 4 chiến lược nén, tee recovery
├── 02-setup/            ← Cài đặt + tích hợp từng AI tool (16 tools)
├── 03-patterns/         ← 4 production patterns, mỗi pattern một file
│   ├── README.md        ←   Pattern picker + bảng tổng hợp
│   ├── git-speedup.md
│   ├── test-only-failures.md
│   ├── file-smart-read.md
│   └── build-lint-compact.md
├── 04-savings/          ← Đo lường: rtk gain, discover, session
└── 05-troubleshooting/  ← Failure modes & mitigations
```

> Mỗi thư mục chứa `README.md` — đồng nhất với convention của `harness/` và `loop/`.

### Lộ Trình Đề Xuất

```
Bước 1: Đọc README này để hiểu bối cảnh
   ↓
Bước 2: 01-concepts/ — hiểu kiến trúc hook + 4 chiến lược nén
   ↓
Bước 3: 02-setup/ — cài đặt + tích hợp vào AI tool của bạn
   ↓
Bước 4: 03-patterns/ — bắt đầu với Git Speedup
   ↓
Bước 5: 04-savings/ — đo token đã tiết kiệm bằng `rtk gain`
   ↓
Bước 6: 05-troubleshooting/ — khi có sự cố
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu RTK hoạt động thế nào | [01-concepts](01-concepts/) |
| Cài đặt + tích hợp tool | [02-setup](02-setup/) |
| Chọn pattern nào dùng trước | [03-patterns](03-patterns/) — pattern picker |
| Làm git nhanh hơn | [03-patterns/git-speedup.md](03-patterns/git-speedup.md) |
| Chỉ xem test failures | [03-patterns/test-only-failures.md](03-patterns/test-only-failures.md) |
| Đo token đã tiết kiệm | [04-savings](04-savings/) |
| Xử lý lệnh bị rewrite sai | [05-troubleshooting](05-troubleshooting/) |

---

## Case Studies Thực Tế

Repo `rtk-ai/rtk` tự dogfood — hỗ trợ 16 AI tools với các cơ chế tích hợp khác nhau:

| AI Tool | Phương thức | Level |
|---------|-------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

**Kết quả đo lường:**

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `docker ps` | Nhiều cột | Essential only | ~70%+ |
| `ruff check` | Nhiều dòng | Grouped by rule | ~80% |

---

## Tài Liệu Tham Khảo

- https://github.com/rtk-ai/rtk — Repo chính
- https://www.rtk-ai.app/guide — Full user guide (installation, supported agents, configuration, troubleshooting)
- [ARCHITECTURE.md](https://github.com/rtk-ai/rtk/blob/master/docs/contributing/ARCHITECTURE.md) — System design & technical decisions
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — 7 components của harness
- [tools/README.md](../README.md) — Nhánh Tools tổng quan
- [loop/](../../loop/) — Vòng lặp hưởng lợi từ context nhẹ hơn

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*Bài viết thuộc [AI Coding Skills Framework](../../..) — nhánh Tools · RTK*