# ❓ FAQ — RTK — Cài đặt (Câu hỏi thật, dễ hiểu)

Nếu câu hỏi chưa rõ, đọc phần được nêu trong ngoặc vuông ở `../README.md`.

---

## 02-setup/README.md

### Q8. Cài RTK bằng cách nào cho đúng, rồi kiểm tra thế nào là biết thành công? [→ Cài Đặt, Kiểm Tra Cài Đặt]

**Bạn sẽ thấy**

Có bốn đường cài, và chỉ một số bị lỗi ngay từ đầu. Trên macOS, Homebrew là cách được khuyến nghị: `brew install rtk`. Cách nhanh cho cả Linux/macOS là chạy script tải về — nó cài vào `~/.local/bin`, nên nếu `~/.local/bin` chưa nằm trong `PATH` (danh sách thư mục mà terminal tìm file) thì lệnh sẽ không chạy. Với Rust thì `cargo install --git https://github.com/rtk-ai/rtk`. Trên Windows, tải file `rtk-x86_64-pc-windows-msvc.zip` từ trang releases, giải nén, đặt `rtk.exe` vào PATH và chạy từ Command Prompt/PowerShell/Windows Terminal — **không double-click** file `.exe`.

**Vì sao**

Một số bộ lọc của RTK gọi ripgrep (`rg`), một công cụ tìm kiếm nhanh. Nếu máy bạn chưa có, agent sẽ gặp lỗi `Binary 'rg' not found on PATH`. Ripgrep là phụ thuộc riêng, không tự đi kèm khi cài RTK.

**Làm gì**

1. Chọn đúng một đường cài theo hệ điều hành; đừng cài cả ba cùng lúc.
2. Nếu dùng script tải về, thêm PATH vào `~/.zshrc`:

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

3. Kiểm tra bằng hai lệnh: `rtk --version` phải hiện `rtk 0.x.x`, `rtk gain` phải mở dashboard tiết kiệm token.
4. Thấy lỗi `rg` thì cài ripgrep: `brew install ripgrep` (macOS) hoặc `winget install BurntSushi.ripgrep.MSVC` (Windows).

**Kiểm tra**

Mở terminal mới sau khi sửa `~/.zshrc`, chạy `which rtk` (phải trỏ đúng file binary) rồi `rtk --version`. Cài ripgrep nếu bất kỳ lệnh nào báo thiếu `rg`.

---

### Q9. Tôi `cargo install` xong mà `rtk gain` báo lỗi — có phải cài nhầm package không? [→ Troubleshooting Cài Đặt Nhanh]

**Bạn sẽ thấy**

Bạn chạy `cargo install rtk`, cài thành công, gọi `rtk gain` thì fail hoặc báo lệnh không hợp lệ. Kiểu cài này rất dễ gặp vì tên gói trùng nhau.

**Vì sao**

Trên crates.io có **một project khác cũng tên "rtk" — Rust Type Kit**, hoàn toàn không liên quan. Cài bằng `cargo install rtk` là cài nhầm project đó. Đây là lỗi tên trùng (name collision), không phải lỗi cài đặt.

**Làm gì**

1. Gỡ package sai, rồi cài đúng bản từ Git:

```bash
cargo uninstall rtk
cargo install --git https://github.com/rtk-ai/rtk
```

2. Trên macOS bạn có thể cài `brew install rtk` cho gọn hơn, nhưng nhớ chỉ chọn một nguồn.
3. Không dùng `cargo install rtk` (không có cờ `--git`) ở bất kỳ máy nào trong CI.

**Kiểm tra**

`rtk --version` phải hiện `rtk 0.x.x` theo định dạng của RTK, không phải số version của Rust Type Kit. Sau đó chạy `rtk gain` — dashboard phải mở được.

---

### Q10. Tôi chạy `rtk init -g` xong rồi sao agent vẫn chạy lệnh thô, không thấy RTK ở đâu? [→ Tích Hợp Vào AI Coding Tool]

**Bạn sẽ thấy**

Lệnh `rtk init -g` chạy xong, không có báo lỗi. Nhưng bạn bảo agent chạy `git status` và output vẫn y hệt trước đây — 15 dòng thay vì `ok main`. Đây là lỗi phổ biến nhất sau khi cài.

**Vì sao**

Ba nguyên nhân thường gặp. Một: **phải khởi động lại AI tool** sau khi `init`, hook mới được nạp. Hai: agent đang dùng tool built-in (`Read`/`Grep`/`Glob`) chứ không đi qua bash — như xem ở Q4. Ba: chọn sai biến thể `init` cho tool của bạn. RTK có hai chế độ: **hook rewrite** (intercept trước khi lệnh chạy, `git status` → `rtk git status`, agent không biết) và **plugin/rule-based** (agent đọc file rules rồi tự gọi `rtk <cmd>`). Codex dùng AGENTS.md + RTK.md; Cline/Roo Code dùng `.clinerules`.

**Làm gì**

1. Chạy đúng lệnh cho tool của bạn:

```bash
rtk init -g                 # Claude Code / GitHub Copilot (global)
rtk init -g --gemini        # Gemini CLI
rtk init -g --codex         # Codex (OpenAI)
rtk init --agent cline      # Cline / Roo Code → .clinerules
```

2. Khởi động lại AI tool, rồi thử lại `git status`.
3. Nếu trên Windows sau khi nâng cấp lên bản ≥ 0.37.2 mà hook không chạy, do vẫn dùng script cũ `rtk-rewrite.sh` — chạy lại `rtk init -g` để chuyển sang native binary hook.

**Kiểm tra**

Bật `rtk init -g -v` (hoặc `-vv`) để xem log rewrite, rồi chạy `git status` trong agent: log phải ghi lệnh được đổi thành `rtk git status`. Không thấy dòng log nghĩa là hook chưa nạp hoặc tool chưa restart.

---

### Q11. Tôi dùng tool ít phổ biến — Cursor, Windsurf, Cline, Kilo Code — lệnh `init` nào, cài global hay trong project? [→ Bảng Tích Hợp Từng Tool]

**Bạn sẽ thấy**

`rtk init -g` chỉ phủ mặc định (Claude Code / GitHub Copilot). Nếu bạn dùng Cursor, Windsurf, Cline hay Kilo Code thì cần đúng cờ, nếu không sẽ cài xong mà không có tác dụng. Đây là điểm dễ nhầm nhất khi làm việc nhóm: mỗi máy một tool khác nhau.

**Vì sao**

Quy tắc phân biệt rất đơn giản: **hook-based thì thêm `-g` (global, áp dụng mọi project); rule-based thì bỏ `-g` và chạy trong thư mục dự án** — vì cách này ghi file rules vào chính repo, nên phải có project đang mở.

| AI Tool | Lệnh init | Phương thức | Phạm vi |
|---|---|---|---|
| Claude Code | `rtk init -g` | PreToolUse hook (native binary) | Global |
| Cursor | `rtk init -g --agent cursor` | preToolUse hook (hooks.json) | Global |
| Windsurf | `rtk init -g --agent windsurf` | `.windsurfrules` | Project |
| Cline / Roo Code | `rtk init --agent cline` | `.clinerules` | Project |
| Kilo Code | `rtk init --agent kilocode` | `.kilocode/rules/rtk-rules.md` | Project |
| OpenCode | `rtk init -g --opencode` | Plugin TS (tool.execute.before) | Global |

**Làm gì**

1. Tra bảng để lấy đúng lệnh. Ngoài 6 tool trên còn: Codex (`--codex`), Gemini CLI (`--gemini`), Copilot CLI (`--copilot`), Mistral Vibe (`--agent vibe`), Kimi AI (`--agent kimi`), Hermes (`--agent hermes`), Google Antigravity (`--agent antigravity`), Pi (`--agent pi`), Factory Droid (`--agent droid`), OpenClaw (`openclaw plugins install ./openclaw`).
2. Khởi động lại tool sau khi init.
3. Với tool dùng file rules trong repo, nhớ commit file rules đó để cả nhóm dùng chung; với tool global thì mỗi người tự cài.
4. Cài thử trên một project trước khi áp dụng cho cả nhóm.

**Kiểm tra**

Chạy `git status` trong agent sau khi restart: lệnh phải ra dạng `rtk git status`. Với tool rule-based, mở file rules trong repo (`.clinerules`, `AGENTS.md`, `RTK.md`) và xác nhận có nội dung hướng dẫn dùng RTK.

---

### Q12. Cài nhầm hoặc không còn dùng — gỡ RTK sạch sẽ thế nào? [→ Gỡ Cài Đặt]

**Bạn sẽ thấy**

Bạn thử rồi thấy không hợp, hoặc chuyển sang AI tool khác và muốn dọn sạch máy. Điều đáng lo: gỡ sai sẽ để lại hook trong `settings.json` và file rules trong repo — agent của người khác pull về vẫn bị ảnh hưởng.

**Vì sao**

RTK cài ở nhiều chỗ: hook trong `settings.json`, file `RTK.md`, các file rules trong project (`.clinerules`, `.windsurfrules`, `.kilocode/rules/rtk-rules.md`), file cấu hình `~/.config/rtk/config.toml` và log `~/.local/share/rtk/tee/`. Lệnh `rtk init -g --uninstall` chỉ gỡ phần hook + `RTK.md` + entry trong `settings.json`.

**Làm gì**

1. Gỡ phần tích hợp trước, rồi mới gỡ binary:

```bash
rtk init -g --uninstall     # gỡ hook, RTK.md, entry trong settings.json
brew uninstall rtk           # nếu cài bằng Homebrew
cargo uninstall rtk          # nếu cài bằng cargo
```

2. Dò tay các file rules còn sót trong từng project (`git status` sẽ cho bạn thấy những file mới sinh ra).
3. Xoá `~/.config/rtk/config.toml` và thư mục `~/.local/share/rtk/tee/` nếu muốn sạch tuyệt đối.
4. Nếu cài bằng script tải về (`curl | sh`), không dùng được `brew uninstall` hay `cargo uninstall` — phải xoá file binary ở `~/.local/bin/rtk` và bỏ dòng `export PATH="$HOME/.local/bin:$PATH"` trong `~/.zshrc` (lưu ý: dòng PATH này có thể do bạn tự thêm cho mục đích khác).
5. Ripgrep bạn tự cài thì giữ lại được — nhiều công cụ khác còn dùng.

**Kiểm tra**

Chạy `which rtk` (phải báo không tìm thấy) và `rtk --version` (phải báo không có lệnh). Bảo agent chạy `git status`, log hook không được ghi lệnh rewrite nữa; `git status` trong repo không còn file rules lạ.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 02-setup/README.md.*
