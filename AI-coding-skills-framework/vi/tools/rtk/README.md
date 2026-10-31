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

Phần này giải thích RTK là gì và vì sao nó tồn tại — để bạn hiểu bối cảnh trước khi cài.

Hãy hình dung thế này: harness của bạn đã có đủ tools, memory, context — nhưng vẫn còn một kẻ ngốn context thầm lặng: **bash output**. Mỗi lần agent chạy `git status` (báo file nào đã sửa), `cargo test` (chạy test Rust) hay `ls` (liệt kê file), nó mang về hàng trăm dòng noise (phần rác không có thông tin) — rồi ngụp lặn trong đó tới mức trôi mất đúng dòng lỗi cần sửa.

**RTK (Rust Token Killer)** là một CLI proxy (chương trình đứng giữa agent và shell command) viết bằng Rust, đứng chen vào giữa agent và shell command để gọt tới **90% bash output** trước khi nó chui vào LLM context (ngữ cảnh mà mô hình ngôn ngữ đọc được). Chỉ một binary duy nhất (một file chương trình), cân 100+ commands, overhead dưới 10ms (độ trễ thêm vào, không đáng kể).

> __RTK là một phần của hệ sinh thái harness — nó là công cụ hiện thực hóa `harness/02-build-context`, nằm trong `tools/rtk/`.__ Nó không phải component trong `harness/`, mà `tools/` giờ là chỗ gom đầy đủ đồ nghề giúp bạn biến cả 7 components của harness thành hàng thật.

> **Tóm gọn 1 câu:** RTK cắt bớt output lệnh shell trước khi nó ngập context của model — như một chiếc phin lọc đặt giữa agent và terminal.

---

### RTK Có Phải Là Một Phần Của Harness Không?

Phần này trả lời câu hỏi RTK đứng ở đâu trong hệ thống — để bạn không tìm nhầm chỗ hay kết luận thiếu tài liệu.

### ✅ **CÓ — về mặt khái niệm.**

Theo [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md), harness gồm **7 components** (thành phần). RTK nằm ở **Component #3 — Context Management** (quản lý ngữ cảnh đưa vào model), trong nhánh Context Optimization / Token Reduction (tối ưu context / giảm token), rồi liên quan thêm một chút tới **Tools** (#1) và **Evaluation**:

Cách đọc bảng này: cột **Component** là thành phần của harness; cột **Vai trò** là nhiệm vụ của nó; cột **RTK liên quan?** cho biết mức dính dáng — 🟢 trực tiếp, 🟡 gián tiếp.

| Component | Vai trò | RTK liên quan? |
|-----------|---------|----------------|
| **Context Management** (Hệ tuần hoàn) | AI luôn có đúng thông tin đúng lúc | 🟢 **TRỰC TIẾP** — nén Immediate Context (Level 5) |
| **Tools** (Tay chân) | Định nghĩa AI có thể làm gì | 🟡 Gián tiếp — RTK là tool proxy quanh shell |
| **Evaluation** | Đo lường hiệu quả | 🟡 Gián tiếp — `rtk gain` đo token saved |

Giải nghĩa vài ô: "Immediate Context (Level 5)" = tầng context gần nhất, thứ model đọc trực tiếp mỗi lượt suy nghĩ. "tool proxy" = người đứng giữa thay agent gọi lệnh. "token saved" = số token đã bớt.

**Mapping với thư mục `harness/`:**

Cách đọc bảng này: cột **Module** là module kiến thức trong `harness/`; cột **Liên quan** là mức độ liên quan tới RTK; cột **Lý do** giải thích vì sao. Ví dụ dòng đầu: `02-build-context` là module chính mà RTK hiện thực hóa.

| Module | Liên quan | Lý do |
|--------|-----------|-------|
| `harness/02-build-context` | 🟢 **Chính** | Context compression ở tầng Immediate Context |
| `harness/06-decide-tools-mcp` | 🟡 Phụ | Tool proxy design |
| `harness/11-evaluation` | 🟡 Phụ | `rtk gain` / `rtk discover` |

Giải nghĩa: "Context compression" = nén ngữ cảnh để model đọc ít mà vẫn đủ. "Tool proxy design" = cách thiết kế công cụ đứng giữa. `rtk gain`/`rtk discover` = hai lệnh đo số liệu tiết kiệm.

> **Phân biệt cho dễ nhớ**: RTK là **đồ nghề chạy được thật** (Rust binary — file chương trình), KHÔNG phải module kiến thức như `harness/01-11` — nên nó ở trong nhánh `tools/`, chung nếp với `harness/` và `loop/`.

> **Tóm gọn 1 câu:** RTK thuộc hệ sinh thái harness về khái niệm (Component #3 — Context Management), nhưng về cấu trúc nó là công cụ thực thi nên nằm trong `tools/`, không phải `harness/`.

### Tại Sao RTK Quan Trọng?

Phần này cho ba lý do nên dùng RTK, kèm bằng chứng cụ thể cho từng lý do.

> **"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."**
>
> Dịch thẳng: token đầu vào là tiền tệ của việc suy nghĩ của agent — đừng tiêu nó vào output rác của shell.

Cách đọc bảng này: cột **#** là số thứ tự; cột **Lý do** là tên lý do; cột **Bằng chứng** là sự kiện chứng minh. Ví dụ dòng 1: RTK cắt 90% output test/push — đó là bằng chứng cho lý do "Context Management".

| # | Lý do | Bằng chứng |
|---|-------|------------|
| 1 | **Context Management** | RTK cắt tới 90% output `cargo test`/`git push` — agent có thêm không gian để reasoning trên đúng phần quan trọng |
| 2 | **Harness Evaluation** | `rtk gain` cung cấp số liệu token saved — ăn khớp mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md |
| 3 | **Hiện thực hóa lý thuyết** | Kỹ thuật "giới hạn output tool" trong module `06` được RTK hiện thực hóa ở tầng bash |

> **Tóm gọn 1 câu:** RTK đáng dùng vì nó giúp agent bỏ ít token vào output rác, cho số đo tiết kiệm được, và biến lý thuyết trong tài liệu thành công cụ chạy thật.

## Tổng Quan

Phần này giải thích cách RTK hoạt động bên trong — nén output bằng 4 chiến lược nào.

Cách RTK làm cũng đơn giản: chặn shell commands rồi nén output bằng **4 chiến lược**:

Cách đọc bảng này: cột **#** là số thứ tự chiến lược; cột **Chiến lược** là tên gọi; cột **Ví dụ** là lệnh thực tế minh họa. Ví dụ dòng 1: `git push` in 15 dòng, RTK lọc còn 1 dòng `ok main`.

| # | Chiến lược | Ví dụ |
|---|------------|-------|
| 1 | **Smart Filtering** (bỏ noise) | `git push` → `ok main` |
| 2 | **Grouping** (gom tương tự) | `ls` → tree với file counts |
| 3 | **Truncation** (giữ phần quan trọng) | `git diff` → bỏ headers |
| 4 | **Deduplication** (gộp log lặp) | `docker logs` → `×42 repeated line` |

Giải nghĩa vài ô: "Smart Filtering" = chỉ giữ dòng có thông tin, bỏ dòng tiến trình. "Grouping" = gom file/thư mục thành cây kèm số lượng. "Truncation" = cắt phần lặp lại như headers (dòng tiêu đề). "Deduplication" = 42 dòng giống nhau gộp thành 1 dòng kèm ×42. `docker logs` = nhật ký của container.

Hỗ trợ **16 AI coding tools** qua hook/plugin (cơ chế gắn tự động): Claude Code, Cline, Copilot VS Code, Gemini CLI, Codex, Cursor, Windsurf, OpenCode...

> **Tóm gọn 1 câu:** RTK nén output bằng 4 cách: lọc rác, gom nhóm, cắt thừa, gộp dòng lặp — gắn được vào 16 AI tool phổ biến.

## Lộ Trình Học (Cấu Trúc Thư Mục)

Phần này vẽ bản đồ các thư mục tài liệu — để bạn biết đọc gì trước, gì sau.

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

Giải nghĩa vài dòng trong sơ đồ: "hook system" = cơ chế chặn tự đổi lệnh. "tee recovery" = cơ chế lưu output đầy đủ ra log khi lệnh fail. "pattern" = mẫu dùng cho một tình huống cụ thể. "Failure modes & mitigations" = các lỗi hay gặp và cách sửa.

> Mỗi thư mục chứa `README.md` — đồng nhất với convention của `harness/` và `loop/`.

### Lộ Trình Đề Xuất

Phần này cho thứ tự đọc 6 bước — làm đúng thứ tự thì không bỏ sót nền tảng.

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

Sau khi cài xong (bước 3), dùng bảng này để chọn đúng tài liệu cho việc đang làm:

Cách đọc bảng này: cột **Bạn muốn...** là việc bạn cần; cột **Đọc** là link cần mở. Ví dụ dòng cuối: lệnh bị đổi sai thì mở `05-troubleshooting/`.

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu RTK hoạt động thế nào | [01-concepts](01-concepts/) |
| Cài đặt + tích hợp tool | [02-setup](02-setup/) |
| Chọn pattern nào dùng trước | [03-patterns](03-patterns/) — pattern picker |
| Làm git nhanh hơn | [03-patterns/git-speedup.md](03-patterns/git-speedup.md) |
| Chỉ xem test failures | [03-patterns/test-only-failures.md](03-patterns/test-only-failures.md) |
| Đo token đã tiết kiệm | [04-savings](04-savings/) |
| Xử lý lệnh bị rewrite sai | [05-troubleshooting](05-troubleshooting/) |

> **Tóm gọn 1 câu:** Đọc theo thứ tự 6 bước (hiểu → cài → áp → đo → sửa lỗi), hoặc tra bảng trên theo việc đang cần làm.

---

## Case Studies Thực Tế

Phần này cho thấy RTK được tích hợp thế nào vào từng AI tool thật, và số đo kết quả.

Vui là repo `rtk-ai/rtk` tự mình ăn "dogfood" (dùng chính sản phẩm của mình hàng ngày) — hỗ trợ tới 16 AI tools, mỗi tool một kiểu tích hợp khác nhau:

Cách đọc bảng này: cột **AI Tool** là tên công cụ; cột **Phương thức** là cách RTK gắn vào nó; cột **Level** là mức can thiệp. Ví dụ dòng đầu: Claude Code gắn qua PreToolUse hook (chặn trước khi lệnh chạy) — lệnh được đổi trong suốt.

| AI Tool | Phương thức | Level |
|---------|-------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

Giải nghĩa vài ô: "Transparent rewrite" = lệnh bị đổi tự động, agent không phải làm gì. "Rule-based rewrite" = đổi theo quy tắc viết trong file `.clinerules` của project. "Instruction-based" = không chặn lệnh, chỉ hướng dẫn AI qua file `AGENTS.md`/`RTK.md` hãy dùng `rtk ...`.

**Kết quả đo lường:**

Cách đọc bảng này: cột **Command** là lệnh đo; cột **Output thô** là số dòng chạy trực tiếp; cột **Output RTK** là số dòng khi qua RTK; cột **Giảm** là % cắt bớt. Ví dụ dòng `cargo test` (fail): từ hơn 200 dòng xuống ~20 dòng — bớt ~90%.

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `docker ps` | Nhiều cột | Essential only | ~70%+ |
| `ruff check` | Nhiều dòng | Grouped by rule | ~80% |

Giải nghĩa vài ô: `ls -la` = liệt kê file kèm quyền/dung lượng. `docker ps` = liệt kê container đang chạy, "Essential only" = chỉ giữ cột cần thiết. `ruff check` = kiểm tra code Python, "Grouped by rule" = gom lỗi theo từng loại vi phạm.

> **Tóm gọn 1 câu:** 16 AI tool đều gắn được RTK (qua hook, quy tắc hoặc hướng dẫn), và số đo thật cho mức giảm 70-93% output.

---

## Tài Liệu Tham Khảo

Phần này gom các link để đọc sâu hơn khi cần.

- https://github.com/rtk-ai/rtk — Repo chính
- https://www.rtk-ai.app/guide — Full user guide (installation, supported agents, configuration, troubleshooting)
- [ARCHITECTURE.md](https://github.com/rtk-ai/rtk/blob/master/docs/contributing/ARCHITECTURE.md) — System design & technical decisions
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — 7 components của harness
- [tools/README.md](../README.md) — Nhánh Tools tổng quan
- [loop/](../../loop/) — Vòng lặp hưởng lợi từ context nhẹ hơn

> **Tóm gọn 1 câu:** Muốn sâu hơn thì đọc guide chính thức và ARCHITECTURE.md; muốn đặt RTK vào bức tranh tổng thì đọc HARNESS_ENGINEERING.md và tools/README.md.

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**
>
> Dịch thẳng: model chỉ tốt bằng đúng thông tin nó đọc được lúc suy nghĩ — và mỗi token lãng phí là một phần thông tin agent không còn chỗ để suy nghĩ.

---

*Bài viết thuộc [AI Coding Skills Framework](../../..) — nhánh Tools · RTK*
