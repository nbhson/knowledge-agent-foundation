# 🛠️ 05. Troubleshooting — Xử Lý Sự Cố

> Các sự cố thường gặp khi dùng RTK, cách chẩn đoán và khắc phục — gồm failure modes, quy tắc exclude, và khi nào nên tắt RTK.

> Phần này giải thích: lỗi nào hay gặp, nguyên nhân là gì, sửa bằng lệnh nào — và khi nào nên miễn nén hoặc tắt RTK. **Giải thích nhanh các từ khóa**: rewrite = RTK tự đổi lệnh `git ...` thành `rtk git ...` khi agent chạy; hook = cái chặn tự động làm việc đó; `exclude_commands` = danh sách lệnh được miễn nén, khai báo trong `config.toml`; built-in tools = công cụ có sẵn trong AI tool (như `Read`, `Grep`) — chúng không chạy qua bash nên không gặp hook.

## Bảng Failure Modes & Mitigations

Cách đọc bảng này: cột **Sự cố** là hiện tượng bạn thấy; cột **Nguyên nhân** là lý do thật; cột **Giải pháp** là lệnh/cách sửa. Ví dụ dòng đầu: chạy `rtk init` xong mà `git status` vẫn ra bản dài — vì chưa restart AI tool — thì restart và thử lại.

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

Giải nghĩa vài ô trong bảng: dòng "built-in tools" — tool có sẵn của AI tool chạy riêng, không qua bash nên hook chạm không tới; muốn nén thì dùng lệnh shell thay thế. `rg`/ripgrep = công cụ tìm kiếm nhanh, cài bằng `brew` (macOS) hoặc `winget` (Windows). "crates.io collision" = kho package của Rust có gói khác trùng tên `rtk`, nên `cargo install rtk` cài nhầm. "0% reduction" = lệnh chạy qua RTK mà output không bị cắt. `legacy shell hook` = hook kiểu cũ (< 0.37.2), `rtk init -g` chuyển sang hook dùng binary native (chương trình thật thay vì script shell).

> **Tóm gọn 1 câu:** Chín sự cố hay gặp, và đa số sửa bằng một lệnh: restart sau khi init, cài ripgrep, cài lại từ đúng repo, hoặc thêm lệnh vào `exclude_commands`.

## Quy Tắc Exclude — Khi Nào Giữ Lệnh Gốc

Phần này giải thích: lệnh nào nên được miễn nén — tức đưa vào `exclude_commands` trong `config.toml`.

Thêm lệnh vào `exclude_commands` nếu:

- Cần output **đầy đủ chính xác** (ví dụ `git diff` chi tiết, `terraform plan` — bản kế hoạch hạ tầng xem trước khi áp).
- Lệnh đó **không nên bị rewrite** để tránh nguy hiểm (curl tải nhị phân — file thực thi về máy; playwright — điều khiển trình duyệt).
- Pipeline/script phụ thuộc format output gốc. (Pipeline `|` = nối output lệnh trước vào lệnh sau; script đọc theo định dạng gốc nên bị vỡ nếu format đổi.)

> 📄 **Code ví dụ:** [`examples/01-quy-tac-exclude-khi-nao-giu-lenh-goc.toml`](examples/01-quy-tac-exclude-khi-nao-giu-lenh-goc.toml)

> **Tóm gọn 1 câu:** Nếu việc kế tiếp cần đúng từng chữ của output — hay lệnh có tác dụng phụ nguy hiểm — thì miễn nén lệnh đó thay vì chấp nhận rủi ro.

## Lưu Ý An Toàn (liên kết harness Guardrails)

Phần này nối RTK với nguyên tắc an toàn (guardrails = rào chắn bắt agent làm đúng quy trình) của harness.

Cách đọc bảng này: cột **Nguyên tắc** là quy tắc an toàn của harness; cột **Áp dụng RTK** là RTK đáp ứng quy tắc đó thế nào. ("transparent" = trong suốt — nén không cản trở, agent gọi được lệnh gốc bất cứ lúc nào; "Tee recovery" = như nhánh tee của đường nước: output chảy ra màn hình một nhánh, đổ vào file log một nhánh — lệnh fail vẫn còn bản đầy đủ; "Privacy by default" = mặc định không gửi dữ liệu đi đâu, "strip secrets" = tự gỡ các chuỗi bí mật như khóa API khỏi output lệnh AWS.)

| Nguyên tắc | Áp dụng RTK |
|------------|-------------|
| Theo nguyên tắc guardrails của harness | RTK rewrite là transparent — agent vẫn có thể gọi lệnh gốc. Luôn kiểm tra output quan trọng trước khi agent hành động theo nó. |
| Tee recovery | Khi lệnh fail, RTK lưu full output — agent nên đọc log đầy đủ trước khi quyết định sửa. |
| Privacy by default | Telemetry mặc định tắt. AWS filters chủ động strip secrets. Cấu hình `RTK_TELEMETRY_DISABLED=1` nếu muốn chặn tuyệt đối. |

> **Tóm gọn 1 câu:** RTK nén trong suốt, giữ lại bản đầy đủ khi lỗi, và mặc định không gửi số liệu đi đâu — đúng tinh thần guardrails của harness.

## Khi Nào Nên Tắt RTK

Phần này giải thích: ba tình huống hiếm hoi mà nén gây hại nhiều hơn lợi — lúc đó tắt RTK hoặc miễn nén.

- Đang debug output chính xác của một tool cụ thể và cần bản raw. (raw = bản nguyên gốc, chưa cắt.)
- Lệnh có side-effects quan trọng mà bạn muốn thấy đầy đủ log. (side-effect = thay đổi ngoài thế giới thật, như tạo/xóa tài nguyên.)
- Pipeline/CI script parse output theo định dạng gốc. (CI = hệ thống tự chạy kiểm tra sau mỗi lần commit.)

> 📄 **Code ví dụ:** [`examples/02-khi-nao-nen-tat-rtk.sh`](examples/02-khi-nao-nen-tat-rtk.sh)

Hoặc dùng `exclude_commands` cho từng lệnh thay vì tắt hẳn.

> **Tóm gọn 1 câu:** Chỉ tắt hẳn RTK khi cần bản raw để debug — còn lại thì miễn nén từng lệnh là đủ.

---

*Trở về [rtk/README.md](../)* · Trước: [04 — Savings](../04-savings/)
