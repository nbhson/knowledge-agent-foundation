# 🧰 Tools — Công Cụ Thực Thi Hỗ Trợ Harness & Loop

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Tools Quan Trọng?](#tại-sao-tools-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã thiết kế một harness hoàn chỉnh — tools, memory, context, guardrails — và bạn đã viết những vòng lặp (loops) tự triage, tự verify. Nhưng có một vấn đề âm thầm: **mỗi lần agent chạy `ls`, `cat`, `git status`, `cargo test`... nó nhận về hàng trăm dòng output**, ngốn hết context window, và trong đống noise đó agent dễ bỏ lỡ chính dòng lỗi quan trọng nhất.

> *"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."*

**Harness Engineering** dạy bạn thiết kế môi trường xung quanh AI. **Tools** là nơi chứa những công cụ thực thi cụ thể — phần mềm bạn cài đặt và cấu hình — để hiện thực hóa lý thuyết đó trong môi trường thật.

Công cụ đầu tiên trong thư mục này là **RTK (Rust Token Killer)** — một CLI proxy giúp cắt tới 90% bash output trước khi nó chạm vào LLM context.

### Tại Sao Tools Quan Trọng?

> **"Một harness lý thuyết hay mà không có công cụ thực thi thì chỉ là slide."**

#### 3 Lý Do Phải Có Tools Directory

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Harness cần "hiện thực hóa"** | Các module trong `harness/` dạy *cách xây dựng* (context compression, tool design...). Tools như RTK là *thứ có sẵn để dùng ngay*, không phải tự code. |
| 2 | **Tiết kiệm token tức thì** | Một lần cài RTK có thể giảm 40-90% token cho các lệnh bash lặp lại — đúng mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md. |
| 3 | **Tách kiến thức khỏi công cụ** | Giữ `harness/` thuần kiến thức (documentation, labs), `loop/` thuần vòng lặp, và `tools/` cho các binary/CLI/plugins hỗ trợ — mỗi nhánh một vai trò rõ ràng. |

## Tổng Quan

**Tools** là nhánh thứ ba của framework, song song với `harness/` (kiến thức) và `loop/` (vòng lặp). Mỗi công cụ là một thư mục con với tutorial riêng, bắt chước cùng convention: `README.md` tổng quan + lộ trình học + các chuyên đề đánh số.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI CODING SKILLS FRAMEWORK                   │
│                                                                     │
│  harness/      → Kiến thức: 7 components, 12 modules (01–12)       │
│  loop/         → Vòng lặp: concepts, patterns, safety, operating   │
│  tools/        → ❯ Công cụ thực thi (binary/CLI/plugins)           │
│     └── rtk/   →   ❯ Rust Token Killer — cắt 90% bash output      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
tools/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + references
└── rtk/                 ← Tutorial RTK (Rust Token Killer)
    ├── README.md        ←   Tổng quan RTK: là gì, quan hệ với harness, lộ trình học
    ├── 01-concepts/     ←   Kiến trúc RTK: hook system, 4 chiến lược nén, luồng dữ liệu
    ├── 02-setup/        ←   Cài đặt + tích hợp từng AI tool (Claude, Cline, Gemini...)
    ├── 03-patterns/     ←   Các pattern sử dụng, mỗi pattern một file
    │   ├── README.md    ←     Pattern picker + bảng tổng hợp
    │   ├── git-speedup.md
    │   ├── test-only-failures.md
    │   ├── file-smart-read.md
    │   └── build-lint-compact.md
    ├── 04-savings/      ←   Đo lường: rtk gain, discover, session — token saved
    └── 05-troubleshooting/ ← Xử lý sự cố, failure modes & mitigations
```

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/` và `loop/`.

### Lộ Trình Đề Xuất

```
Bước 1: Đọc tools/rkt/README.md để hiểu RTK là gì và quan hệ với harness
   ↓
Bước 2: 01-concepts/ — hiểu kiến trúc hook + 4 chiến lược nén hoạt động ra sao
   ↓
Bước 3: 02-setup/ — cài đặt + tích hợp vào AI tool bạn đang dùng (Cline/Claude Code)
   ↓
Bước 4: 03-patterns/ — áp dụng pattern đầu tiên (gợi ý: git-speedup)
   ↓
Bước 5: 04-savings/ — đo lường token đã tiết kiệm bằng `rtk gain`
   ↓
Bước 6: 05-troubleshooting/ — khi có sự cố hoặc lệnh bị rewrite sai
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu RTK hoạt động thế nào | [01-concepts](rtk/01-concepts/) |
| Cài đặt + tích hợp vào AI tool | [02-setup](rtk/02-setup/) |
| Chọn pattern nào dùng trước | [03-patterns](rtk/03-patterns/) — pattern picker |
| Làm git nhanh hơn | [03-patterns/git-speedup.md](rtk/03-patterns/git-speedup.md) |
| Chỉ xem test failures | [03-patterns/test-only-failures.md](rtk/03-patterns/test-only-failures.md) |
| Đo token đã tiết kiệm | [04-savings](rtk/04-savings/) |
| Xử lý lệnh bị rewrite sai | [05-troubleshooting](rtk/05-troubleshooting/) |

---

## Case Studies Thực Tế

### 1. RTK — Eat Its Own Dogfood

Repo `rtk-ai/rtk` chính là một harness engineering case study: nó hỗ trợ **16 AI coding tools** thông qua cơ chế hook/plugin khác nhau:

| AI Tool | Phương thức tích hợp | Level |
|---------|---------------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

### 2. Kết Quả Đo Lường

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` (45 lines) | 45 lines | 12 lines (tree + file counts) | ~73% |
| `git push` (15 lines) | 15 lines | `ok main` (1 line) | ~93% |
| `cargo test` (200+ lines fail) | 200+ | `FAILED: 2/15 tests` + details | ~90% |
| `docker ps` | Nhiều cột | Essential fields only | ~70%+ |
| `ruff check` | Nhiều dòng | Grouped by rule/file | ~80% |

---

## Tài Liệu Tham Khảo

### Công Cụ Trong Nhánh Này

- **[RTK — Rust Token Killer](rtk/)** — CLI proxy nén bash output trước khi vào LLM context. Repo: https://github.com/rtk-ai/rtk · Website: https://www.rtk-ai.app

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../HARNESS_ENGINEERING.md) — 7 components của harness
- [harness/02-build-context](../harness/02-build-context/) — Context Management (nơi RTK đóng vai trò)
- [harness/06-decide-tools-mcp](../harness/06-decide-tools-mcp/) — Tool design & permissions
- [harness/11-evaluation](../harness/11-evaluation/) — Đo lường hiệu quả
- [loop/](../loop/) — Vòng lặp tự duy trì được hưởng lợi từ context nhẹ hơn

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools*