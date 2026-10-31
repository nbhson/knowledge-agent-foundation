# 🔧 02. Cài Đặt & Tích Hợp RTK

> Ở đây mình sẽ cài RTK vào máy rồi cắm vào AI coding tool bạn đang dùng. Xong bước này là các lệnh bash của agent sẽ tự động được rewrite qua RTK.

## Cài Đặt

Phần này cài RTK vào máy. Chọn **một** đường cài theo hệ điều hành của bạn, đừng cài cả ba.

### macOS (Homebrew — khuyến nghị)

Homebrew = trình quản lý cài phần mềm phổ biến nhất trên macOS; khuyến nghị vì cập nhật và gỡ dễ nhất.

> 📄 **Code ví dụ:** [`examples/01-macos-homebrew-khuyen-nghi.sh`](examples/01-macos-homebrew-khuyen-nghi.sh)

### Linux/macOS (Quick Install)

Cách nhanh: chạy script tải về. Script cài vào `~/.local/bin` — nếu thư mục này chưa nằm trong PATH (danh sách thư mục terminal tìm lệnh), bạn phải thêm vào `~/.zshrc`.

> 📄 **Code ví dụ:** [`examples/02-linux-macos-quick-install.sh`](examples/02-linux-macos-quick-install.sh)

### Cargo

Cargo = trình cài package của Rust, cho ai đã có môi trường Rust.

> 📄 **Code ví dụ:** [`examples/03-cargo.sh`](examples/03-cargo.sh)

> ⚠️ **Name collision**: Có một project khác tên "rtk" (Rust Type Kit) trên crates.io. Nếu `rtk gain` fail, bạn đã cài nhầm package — dùng `cargo install --git` phía trên thay thế.

### Windows

Tải binary `rtk-x86_64-pc-windows-msvc.zip` từ [releases](https://github.com/rtk-ai/rtk/releases), giải nén, đặt `rtk.exe` vào PATH. Chạy từ Command Prompt/PowerShell/Windows Terminal — không double-click `.exe`.

### Kiểm Tra Cài Đặt

Hai lệnh kiểm tra: `rtk --version` phải hiện `rtk 0.x.x`, và `rtk gain` phải mở dashboard (bảng thống kê tiết kiệm token).

> 📄 **Code ví dụ:** [`examples/04-kiem-tra-cai-at.sh`](examples/04-kiem-tra-cai-at.sh)

> **Tóm gọn 1 câu:** Chọn một trong ba đường cài (Homebrew / script / cargo) hoặc zip cho Windows, rồi xác nhận bằng `rtk --version` và `rtk gain`.

## Tích Hợp Vào AI Coding Tool

Phần này cắm RTK vào tool AI bạn đang dùng — xong là các lệnh bash của agent tự được nén.

Chạy đúng lệnh ứng với tool bạn đang dùng:

> 📄 **Code ví dụ:** [`examples/05-tich-hop-vao-ai-coding-tool.sh`](examples/05-tich-hop-vao-ai-coding-tool.sh)

Cài xong thì **khởi động lại AI tool**, rồi test nhanh:

> 📄 **Code ví dụ:** [`examples/06-tich-hop-vao-ai-coding-tool.sh`](examples/06-tich-hop-vao-ai-coding-tool.sh)

Restart là bắt buộc: hook chỉ được nạp khi tool khởi động lại.

> **Tóm gọn 1 câu:** Chạy lệnh `rtk init` đúng cờ cho tool của bạn, khởi động lại tool, rồi test bằng một lệnh git.

## Bảng Tích Hợp Từng Tool

Cách đọc bảng này: cột "AI Tool" là tên tool; "Lệnh init" là lệnh cần gõ (cờ khác nhau mỗi tool); "Phương thức" cho biết RTK cắm bằng hook (chặn lệnh ngầm) hay file rules (agent tự đọc); "Loại sống" cho biết cài global (mọi repo) hay project (chỉ repo này). Ví dụ, hàng Claude Code chỉ cần `rtk init -g`.

| AI Tool | Lệnh init | Phương thức | Loại sống |
|---------|-----------|-------------|-----------|
| **Claude Code** | `rtk init -g` | PreToolUse hook (native binary) | Global |
| **GitHub Copilot (VS Code)** | `rtk init -g --copilot` | PreToolUse hook — transparent rewrite | Global |
| **GitHub Copilot CLI** | `rtk init -g --copilot` | PreToolUse deny-with-suggestion (CLI limit) | Global |
| **Cursor** | `rtk init -g --agent cursor` | preToolUse hook (hooks.json) | Global |
| **Gemini CLI** | `rtk init -g --gemini` | BeforeTool hook | Global |
| **Codex** | `rtk init -g --codex` | AGENTS.md + RTK.md instructions | Global |
| **Windsurf** | `rtk init -g --agent windsurf` | `.windsurfrules` | Project |
| **Cline / Roo Code** | `rtk init --agent cline` | `.clinerules` | Project |
| **OpenCode** | `rtk init -g --opencode` | Plugin TS (tool.execute.before) | Global |
| **OpenClaw** | `openclaw plugins install ./openclaw` | Plugin TS (before_tool_call) | Global |
| **Pi** | `rtk init -g --agent pi` | TypeScript extension (tool_call) | Global |
| **Hermes** | `rtk init --agent hermes` | Python plugin adapter (`rtk rewrite`) | Project |
| **Mistral Vibe** | `rtk init -g --agent vibe` | `pre_tool` hook (hooks.toml) | Global |
| **Kilo Code** | `rtk init --agent kilocode` | `.kilocode/rules/rtk-rules.md` | Project |
| **Google Antigravity** | `rtk init --agent antigravity` | `.agents/rules/antigravity-rtk-rules.md` | Project |
| **Kimi AI** | `rtk init --agent kimi` | AGENTS.md | Project |
| **Factory Droid** | `rtk init -g --agent droid` | PreToolUse hook trong `~/.factory/hooks.json` | Global |

Giải nghĩa các thuật ngữ trong bảng: PreToolUse hook = móc chặn chạy trước khi tool thực thi; transparent rewrite = đổi lệnh ngầm, agent không hay biết; deny-with-suggestion = chặn và gợi ý cách chạy đúng; Plugin TS = plugin viết bằng TypeScript; `.clinerules` và tương tự = file rules nằm trong repo mà agent đọc. Hàng "deny-with-suggestion" có nghĩa Copilot CLI bị giới hạn nên RTK chỉ chặn lệnh rồi gợi ý, không tự đổi được.

> **Tóm gọn 1 câu:** Tra đúng cờ `init` theo tool trong bảng — hook-based cài global, rule-based ghi file rules vào repo và phải commit cho cả nhóm.

## Cấu Hình

Phần này chỉ chỗ chỉnh RTK sau khi cài: file cấu hình chính và các cờ dùng chung.

### Cấu hình chính: `~/.config/rtk/config.toml`

macOS: `~/Library/Application Support/rtk/config.toml`

> 📄 **Code ví dụ:** [`examples/07-cau-hinh-chinh-config-rtk-config-toml.toml`](examples/07-cau-hinh-chinh-config-rtk-config-toml.toml)

### Global Flags

Global flags = các cờ dùng được với mọi lệnh `rtk`, ví dụ bật log chi tiết (-v).

> 📄 **Code ví dụ:** [`examples/08-global-flags.sh`](examples/08-global-flags.sh)

> **Tóm gọn 1 câu:** Chỉnh RTK qua file `config.toml` trong thư mục home, còn các cờ dùng chung xem trong ví dụ global flags.

## Gỡ Cài Đặt

Gỡ theo thứ tự: gỡ tích hợp trước (`rtk init -g --uninstall`), xoá file rules còn sót trong repo, rồi mới gỡ binary.

> 📄 **Code ví dụ:** [`examples/09-go-cai-at.sh`](examples/09-go-cai-at.sh)

> **Tóm gọn 1 câu:** Gỡ bằng `rtk init -g --uninstall` trước, sau đó dò và xoá tay các file rules còn sót trong repo.

## Troubleshooting Cài Đặt Nhanh

Cách đọc bảng này: cột "Triệu chứng" là lỗi bạn thấy; "Nguyên nhân" là vì sao; "Fix" là lệnh xử lý. Ví dụ, `rtk gain` fail sau `cargo install` nghĩa là bạn cài nhầm package trùng tên.

| Triệu chứng | Nguyên nhân | Fix |
|-------------|-------------|-----|
| `rtk gain` fail sau `cargo install` | Cài nhầm package "Rust Type Kit" | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Thiếu ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Lệnh bash không được rewrite | Chưa restart AI tool, hoặc dùng built-in tool (`Read`/`Grep`) | Restart tool; dùng shell command hoặc gọi `rtk read`/`rtk grep` trực tiếp |
| Trên Windows sau upgrade < 0.37.2 | Vẫn dùng legacy `rtk-rewrite.sh` | Chạy lại `rtk init -g` để migrate sang native binary hook |

Legacy = bản cũ; migrate = chuyển sang bản mới.

> **Tóm gọn 1 câu:** Bốn lỗi cài thường gặp đều có lệnh fix cụ thể trong bảng — phổ biến nhất là quên restart tool và thiếu ripgrep.

---

*Trở về [rtk/README.md](../)* · Trước: [01 — Concepts](../01-concepts/) · Tiếp theo: [03 — Patterns](../03-patterns/)
