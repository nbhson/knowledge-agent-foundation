# 🧠 01. Kiến Trúc RTK — Concepts

> Hiểu RTK chạy ra sao sẽ giúp bạn cấu hình cho chuẩn, tránh mấy lỗi kinh điển, và biết khi nào RTK đành bó tay (ví dụ Claude Code `Read`/`Grep`/`Glob` built-in tools bypass hook).

## Cách RTK Can Thiệp Vào Luồng Lệnh

Phần này cho thấy RTK đứng ở đâu trong luồng: nó chen vào giữa agent và lệnh, lọc output trước khi trả về. Đọc sơ đồ: bên trái là không có RTK — agent nhận nguyên output thô của git; bên phải là có RTK — output đi qua bộ lọc, agent chỉ nhận bản gọn (compact = rút gọn).

```
  Không có rtk:                                    Có rtk:

  Claude  --git status-->  shell  -->  git         Claude  --git status-->  RTK  -->  git
    ^                                   |            ^                      |          |
    |         full raw output           |            |  compact output      | filter   |
    +-----------------------------------+            +------- (filtered) ---+----------+
```

Đọc sơ đồ: bên trái là không có RTK — agent nhận nguyên output thô của git. Bên phải là có RTK — output đi qua bộ lọc, agent chỉ nhận bản gọn (compact = rút gọn).

Nói ngắn gọn, RTK đứng chen vào **giữa agent và shell command**. Agent gọi `git status` → hook (móc chặn tự động chạy trước lệnh) viết lại thành `rtk git status` → RTK chạy lệnh thật, lọc/nén output → agent chỉ nhận về bản đã gọn nhẹ.

> **Tóm gọn 1 câu:** RTK là bộ lọc đứng giữa agent và lệnh shell — lệnh thật vẫn chạy, chỉ có output được nén trước khi agent đọc.

## Hai Chế Độ Hoạt Động

Phần này giải thích hai cách cắm RTK vào AI tool — chọn đúng cách theo tool bạn dùng. Hook rewrite: agent gọi `git status`, hệ thống tự đổi thành `rtk git status`; rule-based: agent đọc `AGENTS.md` rồi tự thêm tiền tố `rtk` vào lệnh. Giải nghĩa: intercept = chặn lấy trước; transparent = trong suốt, agent không nhận ra; rules = file chỉ dẫn mà agent đọc rồi tự làm theo.

Cách đọc bảng này: cột "Chế độ" là tên cách hoạt động; "Cách hoạt động" giải thích nó làm gì; "AI Tools" liệt kê tool hỗ trợ. Ví dụ, Claude Code thuộc hàng hook rewrite, Cline thuộc hàng rule-based.

| Chế độ | Cách hoạt động | AI Tools |
|--------|----------------|----------|
| **Hook rewrite** | Intercept trước khi lệnh chạy, rewrite `git status` → `rtk git status`. Transparent, agent không biết | Claude Code, Copilot VS Code, Gemini CLI, Cursor... |
| **Plugin / Rule-based** | Agent đọc rules (`.clinerules`, `AGENTS.md`, `RTK.md`) và tự gọi `rtk <cmd>` | Cline/Roo Code (`.clinerules`), Codex (AGENTS.md + RTK.md), Windsurf... |

Giải nghĩa: intercept = chặn lấy trước; transparent = trong suốt, agent không nhận ra; rules = file chỉ dẫn mà agent đọc rồi tự làm theo.

> **Tóm gọn 1 câu:** RTK cắm vào tool theo 2 cách — hook tự chặn lệnh ngầm (không cần agent biết) hoặc agent tự đọc file rules rồi gọi `rtk` thủ công.

## Bốn Chiến Lược Nén (Core của RTK)

Phần này là trái tim của RTK: bốn cách cắt gọn output, mỗi cách xử lý một loại rác.

Cách đọc bảng này: cột "Chiến lược" là tên cách nén; "Làm gì" nói nó bỏ/giữ gì; "Ví dụ" cho thấy kết quả thật. Ví dụ, `git push` in 15 dòng nhưng chỉ cần biết "đã xong" — Smart Filtering còn lại `ok main`. Noise = rác không mang thông tin; whitespace = khoảng trắng; boilerplate = dòng mẫu lặp máy móc; redundancy = phần lặp lại không cần thiết.

| # | Chiến lược | Làm gì | Ví dụ |
|---|------------|--------|-------|
| 1 | **Smart Filtering** | Loại bỏ noise: comments, whitespace, boilerplate | `git push` → chỉ còn `ok main` |
| 2 | **Grouping** | Gom các mục tương tự (file theo thư mục, lỗi theo loại) | `ls` → tree với file counts |
| 3 | **Truncation** | Giữ phần quan trọng, cắt redundancy | `git diff` → bỏ headers |
| 4 | **Deduplication** | Gộp log lặp lại thành count | `docker logs` → `×42 repeated line` |

> 📌 **Mấu chốt:** RTK **không phải tokenizer** — nó ước lượng `bytes / 4`. Tỷ lệ phần trăm (giảm 90%) đáng tin cậy, nhưng con số token tuyệt đối chỉ là xấp xỉ. Tokenizer = máy đếm token thật của mô hình.

> **Tóm gọn 1 câu:** RTK nén bằng 4 cách (lọc rác, gom nhóm, cắt thừa, gộp lặp) — tin phần trăm giảm, đừng tin số token tuyệt đối vì nó chỉ ước lượng bytes ÷ 4.

## Khi Lệnh Fail: Tee Recovery

Một điểm hay của RTK: khi lệnh fail, nó giữ lại **toàn bộ output thô** để agent đọc lại sau, khỏi phải chạy lại lệnh lần nữa:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Nghĩa là: 2/15 test fail, còn 200+ dòng log gốc nằm trong file được trỏ tới — chạy lại test có thể tốn vài phút, đọc log thì không. Tee = tách một bản sao output sang file, giống lệnh `tee` trong Linux.

Cấu hình trong `config.toml`:

> 📄 **Code ví dụ:** [`examples/01-khi-lenh-fail-tee-recovery.toml`](examples/01-khi-lenh-fail-tee-recovery.toml)

> **Tóm gọn 1 câu:** Lệnh fail thì agent nhận 2 dòng tóm tắt, còn log đầy đủ được lưu sẵn vào `~/.local/share/rtk/tee/` để đọc lại thay vì chạy lại.

## Cấu trúc Binary & Phụ Thuộc

Phần này cho biết RTK gồm những gì trên máy bạn, để biết cần cài thêm gì và dữ liệu nằm ở đâu. Cách đọc bảng: cột "Thành phần" là thứ nằm trên máy; "Ghi chú" giải thích nó làm gì — ví dụ, thiếu ripgrep thì một số bộ lọc sẽ báo lỗi. Binary = một file chạy được duy nhất; overhead = thời gian chờ thêm; PATH = danh sách thư mục terminal dùng để tìm lệnh.

| Thành phần | Ghi chú |
|------------|---------|
| Single Rust binary | Hiệu năng cao, overhead <10ms |
| 100+ commands được hỗ trợ | git, cargo, npm, pytest, docker, kubectl, aws... |
| ripgrep (`rg`) | Một số filters gọi `rg` — cần cài và giữ trong PATH |
| `~/.config/rtk/config.toml` | Cấu hình chính (macOS: `~/Library/Application Support/rtk/config.toml`) |
| `~/.local/share/rtk/tee/` | Nơi lưu full output khi lệnh fail |

> **Tóm gọn 1 câu:** RTK là một file chạy duy nhất, nhanh (<10ms), hỗ trợ 100+ lệnh, cần ripgrep cài riêng — cấu hình và log nằm trong thư mục home của bạn.

## Cấu Hình Cơ Bản

> 📄 **Code ví dụ:** [`examples/02-cau-hinh-co-ban.toml`](examples/02-cau-hinh-co-ban.toml)

Xem thêm cấu hình đầy đủ (env vars = biến môi trường, per-project filters = bộ lọc riêng từng dự án) tại [Configuration guide](https://www.rtk-ai.app/guide/getting-started/configuration).

> **Tóm gọn 1 câu:** Cấu hình RTK nằm trong file `config.toml` — cài cơ bản theo ví dụ mẫu, chi tiết sâu xem guide chính thức.

## Giới Hạn Quan Trọng (Scope)

Phần này nêu ranh giới của RTK — đọc trước để không mong đợi sai.

- **Hook chỉ chạy trên Bash tool calls.** Claude Code built-in tools (`Read`, `Grep`, `Glob`) **không** đi qua hook → không bị auto-rewrite. Nghĩa là lệnh của tool đọc file có sẵn không được nén.
- Với các workflow đó: dùng shell commands (`cat`/`head`/`tail`, `rg`/`grep`, `find`) hoặc gọi trực tiếp `rtk read`, `rtk grep`, `rtk find`.
- RTK đo **bash output reduction**, không phải giảm hóa đơn token toàn phần (input tokens chỉ là một phần của bill). Nghĩa là nó nén output của lệnh, còn prompt dài hay lịch sử trò chuyện dài vẫn tốn token như cũ.

> **Tóm gọn 1 câu:** RTK chỉ nén được lệnh bash — tool `Read`/`Grep`/`Glob` của Claude Code nằm ngoài tầm, muốn nén thì dùng lệnh shell hoặc `rtk read`/`rtk grep`.

## Câu Hỏi Thường Gặp (Concepts Level)

**Q: RTK có thay được việc tự code context compression không?**
A: Không hẳn. RTK chỉ lo **tầng Immediate Context** (output command). Mấy tầng còn lại (system instructions, task context, domain knowledge, conversation history) vẫn là việc của harness — như module `02-build-context` lo. Compression = nén dữ liệu cho vừa bộ nhớ ngữ cảnh.

**Q: RTK có an toàn với data nhạy cảm không?**
A: Có. RTK không thu thập source code, file paths, secrets, env vars (telemetry mặc định đã tắt). Mấy filter AWS còn chủ động strip secrets khỏi output cho bạn yên tâm.

> **Tóm gọn 1 câu:** RTK chỉ nén tầng output lệnh (không thay được hệ nén context tổng thể) và không thu thập dữ liệu nhạy cảm.

---

*Trở về [rtk/README.md](../)* · Tiếp theo: [02 — Setup](../02-setup/)
