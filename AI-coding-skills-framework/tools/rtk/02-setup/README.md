# 🔧 02. Cài Đặt & Tích Hợp RTK

> Hướng dẫn cài đặt RTK vào máy và tích hợp vào AI coding tool bạn đang dùng. Sau bước này, các lệnh bash của agent sẽ tự động được rewrite qua RTK.

## Cài Đặt

### macOS (Homebrew — khuyến nghị)

```bash
brew install rtk
```

### Linux/macOS (Quick Install)

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
# Cài vào ~/.local/bin — thêm vào PATH nếu cần:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### Cargo

```bash
cargo install --git https://github.com/rtk-ai/rtk
```

> ⚠️ **Name collision**: Có một project khác tên "rtk" (Rust Type Kit) trên crates.io. Nếu `rtk gain` fail, bạn đã cài nhầm package — dùng `cargo install --git` phía trên thay thế.

### Windows

Tải binary `rtk-x86_64-pc-windows-msvc.zip` từ [releases](https://github.com/rtk-ai/rtk/releases), giải nén, đặt `rtk.exe` vào PATH. Chạy từ Command Prompt/PowerShell/Windows Terminal — không double-click `.exe`.

### Kiểm Tra Cài Đặt

```bash
rtk --version   # # Nên hiện "rtk 0.x.x"
rtk gain        # Nên mở dashboard tiết kiệm token
```

## Tích Hợp Vào AI Coding Tool

Chạy lệnh tương ứng với tool bạn dùng:

```bash
# Hook-based (transparent rewrite — khuyến nghị)
rtk init -g                     # Claude Code / GitHub Copilot (default)
rtk init -g --gemini            # Gemini CLI
rtk init -g --codex             # Codex (OpenAI)
rtk init -g --agent cursor      # Cursor
rtk init -g --agent windsurf    # Windsurf
rtk init -g --opencode          # OpenCode
rtk init -g --agent pi          # Pi
rtk init -g --agent droid       # Factory Droid

# Plugin / Rule-based (project-scoped)
rtk init --agent cline          # Cline / Roo Code  ← dùng .clinerules
rtk init --agent kilocode       # Kilo Code
rtk init --agent antigravity    # Google Antigravity
rtk init --agent kimi           # Kimi AI
rtk init --agent hermes         # Hermes
```

Sau khi cài **khởi động lại AI tool**, rồi test:

```bash
git status  # Sẽ tự động được rewrite thành "rtk git status"
```

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

```toml
[hooks]
exclude_commands = ["curl", "playwright"]  # skip rewrite cho các lệnh này

[tee]
enabled = true          # lưu raw output khi fail (default: true)
mode = "failures"       # "failures", "always", hoặc "never"
```

### Global Flags

```bash
-u, --ultra-compact    # ASCII icons, inline format (giảm output thêm nữa)
-v, --verbose          # Tăng verbosity (-v, -vv, -vvv)
```

## Gỡ Cài Đặt

```bash
rtk init -g --uninstall     # Gỡ hook, RTK.md, settings.json entry
cargo uninstall rtk          # Gỡ binary (nếu cài qua cargo)
brew uninstall rtk           # Gỡ qua Homebrew (nếu cài brew)
```

## Troubleshooting Cài Đặt Nhanh

| Triệu chứng | Nguyên nhân | Fix |
|-------------|-------------|-----|
| `rtk gain` fail sau `cargo install` | Cài nhầm package "Rust Type Kit" | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Thiếu ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Lệnh bash không được rewrite | Chưa restart AI tool, hoặc dùng built-in tool (`Read`/`Grep`) | Restart tool; dùng shell command hoặc gọi `rtk read`/`rtk grep` trực tiếp |
| Trên Windows sau upgrade < 0.37.2 | Vẫn dùng legacy `rtk-rewrite.sh` | Chạy lại `rtk init -g` để migrate sang native binary hook |

---

*Trở về [rtk/README.md](../)* · Trước: [01 — Concepts](../01-concepts/) · Tiếp theo: [03 — Patterns](../03-patterns/)