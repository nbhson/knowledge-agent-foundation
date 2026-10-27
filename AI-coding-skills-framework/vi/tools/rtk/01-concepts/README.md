# 🧠 01. Kiến Trúc RTK — Concepts

> Hiểu RTK chạy ra sao sẽ giúp bạn cấu hình cho chuẩn, tránh mấy lỗi kinh điển, và biết khi nào RTK đành bó tay (ví dụ Claude Code `Read`/`Grep`/`Glob` built-in tools bypass hook).

## Cách RTK Can Thiệp Vào Luồng Lệnh

```
  Không có rtk:                                    Có rtk:

  Claude  --git status-->  shell  -->  git         Claude  --git status-->  RTK  -->  git
    ^                                   |            ^                      |          |
    |         full raw output           |            |  compact output      | filter   |
    +-----------------------------------+            +------- (filtered) ---+----------+
```

Nói ngắn gọn, RTK đứng chen vào **giữa agent và shell command**. Agent gọi `git status` → hook viết lại thành `rtk git status` → RTK chạy lệnh thật, lọc/nén output → agent chỉ nhận về bản đã gọn nhẹ.

## Hai Chế Độ Hoạt Động

| Chế độ | Cách hoạt động | AI Tools |
|--------|----------------|----------|
| **Hook rewrite** | Intercept trước khi lệnh chạy, rewrite `git status` → `rtk git status`. Transparent, agent không biết | Claude Code, Copilot VS Code, Gemini CLI, Cursor... |
| **Plugin / Rule-based** | Agent đọc rules (`.clinerules`, `AGENTS.md`, `RTK.md`) và tự gọi `rtk <cmd>` | Cline/Roo Code (`.clinerules`), Codex (AGENTS.md + RTK.md), Windsurf... |

## Bốn Chiến Lược Nén (Core của RTK)

| # | Chiến lược | Làm gì | Ví dụ |
|---|------------|--------|-------|
| 1 | **Smart Filtering** | Loại bỏ noise: comments, whitespace, boilerplate | `git push` → chỉ còn `ok main` |
| 2 | **Grouping** | Gom các mục tương tự (file theo thư mục, lỗi theo loại) | `ls` → tree với file counts |
| 3 | **Truncation** | Giữ phần quan trọng, cắt redundancy | `git diff` → bỏ headers |
| 4 | **Deduplication** | Gộp log lặp lại thành count | `docker logs` → `×42 repeated line` |

> 📌 **Mấu chốt:** RTK **không phải tokenizer** — nó ước lượng `bytes / 4`. Tỷ lệ phần trăm (giảm 90%) đáng tin cậy, nhưng con số token tuyệt đối chỉ là xấp xỉ.

## Khi Lệnh Fail: Tee Recovery

Một điểm hay của RTK: khi lệnh fail, nó giữ lại **toàn bộ output thô** để agent đọc lại sau, khỏi phải chạy lại lệnh lần nữa:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Cấu hình trong `config.toml`:

```toml
[tee]
enabled = true          # save raw output on failure (default: true)
mode = "failures"       # "failures", "always", or "never"
```

## Cấu trúc Binary & Phụ Thuộc

| Thành phần | Ghi chú |
|------------|---------|
| Single Rust binary | Hiệu năng cao, overhead <10ms |
| 100+ commands được hỗ trợ | git, cargo, npm, pytest, docker, kubectl, aws... |
| ripgrep (`rg`) | Một số filters gọi `rg` — cần cài và giữ trong PATH |
| `~/.config/rtk/config.toml` | Cấu hình chính (macOS: `~/Library/Application Support/rtk/config.toml`) |
| `~/.local/share/rtk/tee/` | Nơi lưu full output khi lệnh fail |

## Cấu Hình Cơ Bản

```toml
# ~/.config/rtk/config.toml (macOS: ~/Library/Application Support/rtk/config.toml)
[hooks]
exclude_commands = ["curl", "playwright"]  # skip rewrite cho các lệnh này

[tee]
enabled = true
mode = "failures"
```

Xem thêm cấu hình đầy đủ (env vars, per-project filters) tại [Configuration guide](https://www.rtk-ai.app/guide/getting-started/configuration).

## Giới Hạn Quan Trọng (Scope)

- **Hook chỉ chạy trên Bash tool calls.** Claude Code built-in tools (`Read`, `Grep`, `Glob`) **không** đi qua hook → không bị auto-rewrite.
- Với các workflow đó: dùng shell commands (`cat`/`head`/`tail`, `rg`/`grep`, `find`) hoặc gọi trực tiếp `rtk read`, `rtk grep`, `rtk find`.
- RTK đo **bash output reduction**, không phải giảm hóa đơn token toàn phần (input tokens chỉ là một phần của bill).

## Câu Hỏi Thường Gặp (Concepts Level)

**Q: RTK có thay được việc tự code context compression không?**
A: Không hẳn. RTK chỉ lo **tầng Immediate Context** (output command). Mấy tầng còn lại (system instructions, task context, domain knowledge, conversation history) vẫn là việc của harness — như module `02-build-context` lo.

**Q: RTK có an toàn với data nhạy cảm không?**
A: Có. RTK không thu thập source code, file paths, secrets, env vars (telemetry mặc định đã tắt). Mấy filter AWS còn chủ động strip secrets khỏi output cho bạn yên tâm.

---

*Trở về [rtk/README.md](../)* · Tiếp theo: [02 — Setup](../02-setup/)