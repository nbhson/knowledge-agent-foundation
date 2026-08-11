# 🛠️ 05. Troubleshooting — Xử Lý Sự Cố

> Các sự cố thường gặp khi dùng RTK, cách chẩn đoán và khắc phục. Bao gồm failure modes, quy tắc exclude, và khi nào nên tắt RTK.

## Bảng Failure Modes & Mitigations

| Sự cố | Nguyên nhân | Giải pháp |
|-------|-------------|-----------|
| Lệnh bash không được rewrite | Chưa restart AI tool sau `rtk init` | Restart tool và test lại `git status` |
| Taigoài hook: built-in tools (`Read`/`Grep`/`Glob`) bypass | Dùng shell commands hoặc gọi `rtk read`/`rtk grep` trực tiếp |
| `Binary 'rg' not found on PATH` | Thiếu ripgrep — một số filters cần `rg` | `brew install ripgrep` / `winget install BurntSushi.ripgrep.MSVC` |
| `rtk gain` fail sau `cargo install` | Cài nhầm package "Rust Type Kit" (crates.io collision) | `cargo install --git https://github.com/rtk-ai/rtk` |
| Lệnh quan trọng bị nén quá mức | Filter quá aggressive | Thêm vào `exclude_commands` trong `config.toml` |
| Output bị mất context khi pipeline (`\| grep`) | Format nén không parse được | Kiểm tra pipeline; gọi lệnh gốc trực tiếp nếu cần |
| Chi phí token vẫn cao | Chưa dùng hết RTK features | `rtk discover` tìm lệnh 0% reduction; thêm custom TOML filters |
| Trên Windows: legacy shell hook | Bản < 0.37.2 | Chạy lại `rtk init -g` để migrate native binary hook |
| Filter không áp dụng cho project cụ thể | Cần per-project config | Xem Configuration guide (per-project filters) |

## Quy Tắc Exclude — Khi Nào Giữ Lệnh Gốc

Thêm lệnh vào `exclude_commands` nếu:

- Cần output **đầy đủ chính xác** (ví dụ `git diff` chi tiết, `terraform plan`).
- Lệnh đó **không nên bị rewrite** để tránh nguy hiểm (curl tải nhị phân, playwright).
- Pipeline/script phụ thuộc format output gốc.

```toml
# ~/.config/rtk/config.toml
[hooks]
exclude_commands = ["curl", "playwright", "terraform plan"]
```

## Lưu Ý An Toàn (liên kết harness Guardrails)

| Nguyên tắc | Áp dụng RTK |
|------------|-------------|
| Theo nguyên tắc guardrails của harness | RTK rewrite là transparent — agent vẫn có thể gọi lệnh gốc. Luôn kiểm tra output quan trọng trước khi agent hành động theo nó. |
| Tee recovery | Khi lệnh fail, RTK lưu full output — agent nên đọc log đầy đủ trước khi quyết định sửa. |
| Privacy by default | Telemetry mặc định tắt. AWS filters chủ động strip secrets. Cấu hình `RTK_TELEMETRY_DISABLED=1` nếu muốn chặn tuyệt đối. |

## Khi Nào Nên Tắt RTK

- Đang debug output chính xác của một tool cụ thể và cần bản raw.
- Lệnh có side-effects quan trọng mà bạn muốn thấy đầy đủ log.
- Pipeline/CI script parse output theo định dạng gốc.

```bash
rtk init -g --uninstall   # Gỡ hoàn toàn hook
```

Hoặc dùng `exclude_commands` cho từng lệnh thay vì tắt hẳn.

---

*Trở về [rtk/README.md](../)* · Trước: [04 — Savings](../04-savings/)