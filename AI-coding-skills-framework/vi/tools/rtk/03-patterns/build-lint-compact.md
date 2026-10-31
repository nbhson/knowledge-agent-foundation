# 🏗️ Build & Lint Compact Pattern

**Goal**: Nén output build/lint — chỉ giữ lỗi và cảnh báo quan trọng, gom theo file/rule. Giúp agent thấy "cái gì đang hỏng" thay vì đọc hàng trăm dòng output compiler.

Build = bước dịch code thành chương trình chạy được; lint = bước kiểm tra lỗi phong cách/lỗi tiềm ẩn; compiler = chương trình dịch code.

## Dùng Khi Nào

- Build thường xuyên (`cargo build`, `npm run build`, `next build`).
- Lint/type-check mỗi lần sửa code (`tsc`, `ruff`, `clippy`, `eslint`). Type-check = kiểm tra kiểu dữ liệu.
- CI đang đỏ do compile/lint errors. CI đỏ = hệ chạy test tự động báo lỗi; compile errors = lỗi khi dịch code.

> **Tóm gọn 1 câu:** Bật pattern này khi build/lint chạy thường xuyên hoặc CI đỏ vì lỗi compile/lint — nó giữ lại đúng chỗ đang hỏng.

## Lệnh & Mức Giảm

Cách đọc bảng này: cột "Lệnh gốc" là lệnh bạn vẫn gõ; "RTK" là bản đã nén tương ứng; "Output" mô tả bản nén còn lại gì; "Giảm" là mức cắt so với bản gốc. Ví dụ, `tsc` in hàng trăm dòng nhưng `rtk tsc` gom lỗi theo file, giảm ~85%.

| Lệnh gốc | RTK | Output | Giảm |
|----------|-----|--------|------|
| `cargo build` | `rtk cargo build` | Compact build output | ~80% |
| `cargo clippy` | `rtk cargo clippy` | Compact clippy | ~80% |
| `tsc` | `rtk tsc` | TS errors grouped by file | ~85% |
| `eslint` | `rtk lint` | Grouped by rule/file | ~80% |
| `ruff check` | `rtk ruff check` | JSON, grouped by rule/file | ~80% |
| `golangci-lint run` | `rtk golangci-lint run` | JSON | ~85% |
| `rubocop` | `rtk rubocop` | JSON | ~60%+ |
| `next build` | `rtk next build` | Compact | ~75% |
| `prettier --check .` | `rtk prettier --check .` | Files needing formatting | ~75% |
| `sbt compile` | `rtk sbt compile` | Compilation errors only | ~75% |

Giải nghĩa nhanh: `cargo build` = build Rust; `clippy` = linter Rust; `tsc` = trình kiểm tra kiểu TypeScript; `eslint` = linter JavaScript; `ruff` = linter Python; `golangci-lint` = linter Go; `rubocop` = linter Ruby; `prettier` = công cụ chỉnh định dạng; `sbt` = build tool Scala; grouped by file/rule = gom lỗi theo file hoặc theo loại lỗi; JSON = định dạng dữ liệu có cấu trúc.

> **Tóm gọn 1 câu:** Pattern này nén 10 lệnh build/lint với mức giảm ~60–85% — ưu tiên `rtk tsc` và `rtk golangci-lint run` vì giảm mạnh nhất.

## Ví Dụ Thực Tế

```
# tsc (nhiều dòng)                      # rtk tsc
src/harness/context.ts(42,9):            src/harness/context.ts
  error TS2322: Type 'string' ...          L42  TS2322  Type mismatch
src/harness/loop.ts(18,5):                 src/harness/loop.ts
  error TS2554: Expected 2 args ...          L18  TS2554  Expected 2 args
```

Đọc ví dụ: bên trái, mỗi lỗi lặp lại tên file; bên phải, tên file chỉ xuất hiện một lần, dưới nó là số dòng + mã lỗi + mô tả ngắn. `(42,9)` nghĩa là dòng 42, cột 9.

> **Tóm gọn 1 câu:** Bản RTK gom lỗi theo file — tên file một lần, dưới đó là số dòng và mã lỗi, nên ngắn hơn ~85% mà vẫn đủ để sửa.

## Lưu Ý

- Các linter cần output JSON (`ruff`, `golangci-lint`, `rubocop`) — RTK parse JSON nên dùng đúng formatter (parse = đọc hiểu định dạng; formatter = chế độ xuất dữ liệu).
- `next build` có nhiều giai đoạn — RTK giữ log fail ở các bước quan trọng.
- Một số filters shell-out tới ripgrep (`rg`) — đảm bảo `rg` có trong PATH (shell-out = gọi ra lệnh bên ngoài khác).

> **Tóm gọn 1 câu:** Ba điều cần nhớ: linter phải xuất đúng định dạng (JSON), `next build` giữ log fail từng giai đoạn, và ripgrep phải có trong PATH.

---

*Trở về [03 — Patterns](../03-patterns/)*
