# 🔧 02. Cài Đặt & Tích Hợp RTK

> Ở đây mình sẽ cài RTK vào máy rồi cắm vào AI coding tool bạn đang dùng. Xong bước này là các lệnh bash của agent sẽ tự động được rewrite qua RTK.

## Cài Đặt

### macOS (Homebrew — khuyến nghị)

> 📄 **Code ví dụ:** [`examples/01-macos-homebrew-khuyen-nghi.sh`](examples/01-macos-homebrew-khuyen-nghi.sh)

### Linux/macOS (Quick Install)

> 📄 **Code ví dụ:** [`examples/02-linux-macos-quick-install.sh`](examples/02-linux-macos-quick-install.sh)

### Cargo

> 📄 **Code ví dụ:** [`examples/03-cargo.sh`](examples/03-cargo.sh)

> ⚠️ **Name collision**: Có một project khác tên "rtk" (Rust Type Kit) trên crates.io. Nếu `rtk gain` fail, bạn đã cài nhầm package — dùng `cargo install --git` phía trên thay thế.

### Windows

Tải binary `rtk-x86_64-pc-windows-msvc.zip` từ [releases](https://github.com/rtk-ai/rtk/releases), giải nén, đặt `rtk.exe` vào PATH. Chạy từ Command Prompt/PowerShell/Windows Terminal — không double-click `.exe`.

### Kiểm Tra Cài Đặt

> 📄 **Code ví dụ:** [`examples/04-kiem-tra-cai-at.sh`](examples/04-kiem-tra-cai-at.sh)

## Tích Hợp Vào AI Coding Tool

Chạy đúng lệnh ứng với tool bạn đang dùng:

> 📄 **Code ví dụ:** [`examples/05-tich-hop-vao-ai-coding-tool.sh`](examples/05-tich-hop-vao-ai-coding-tool.sh)

Cài xong thì **khởi động lại AI tool**, rồi test nhanh:

> 📄 **Code ví dụ:** [`examples/06-tich-hop-vao-ai-coding-tool.sh`](examples/06-tich-hop-vao-ai-coding-tool.sh)

## Bảng Tích Hợp Từng Tool

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

## Cấu Hình

### Cấu hình chính: `~/.config/rtk/config.toml`

macOS: `~/Library/Application Support/rtk/config.toml`

> 📄 **Code ví dụ:** [`examples/07-cau-hinh-chinh-config-rtk-config-toml.toml`](examples/07-cau-hinh-chinh-config-rtk-config-toml.toml)

### Global Flags

> 📄 **Code ví dụ:** [`examples/08-global-flags.sh`](examples/08-global-flags.sh)

## Gỡ Cài Đặt

> 📄 **Code ví dụ:** [`examples/09-go-cai-at.sh`](examples/09-go-cai-at.sh)

## Troubleshooting Cài Đặt Nhanh

| Triệu chứng | Nguyên nhân | Fix |
|-------------|-------------|-----|
| `rtk gain` fail sau `cargo install` | Cài nhầm package "Rust Type Kit" | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Thiếu ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Lệnh bash không được rewrite | Chưa restart AI tool, hoặc dùng built-in tool (`Read`/`Grep`) | Restart tool; dùng shell command hoặc gọi `rtk read`/`rtk grep` trực tiếp |
| Trên Windows sau upgrade < 0.37.2 | Vẫn dùng legacy `rtk-rewrite.sh` | Chạy lại `rtk init -g` để migrate sang native binary hook |

---

*Trở về [rtk/README.md](../)* · Trước: [01 — Concepts](../01-concepts/) · Tiếp theo: [03 — Patterns](../03-patterns/)