# 🏗️ Build & Lint Compact Pattern

**Goal**: Nén output build/lint — chỉ giữ lỗi và cảnh báo quan trọng, gom theo file/rule. Giúp agent thấy "cái gì đang hỏng" thay vì đọc hàng trăm dòng output compiler.

## Dùng Khi Nào

- Build thường xuyên (`cargo build`, `npm run build`, `next build`).
- Lint/type-check mỗi lần sửa code (`tsc`, `ruff`, `clippy`, `eslint`).
- CI đang đỏ do compile/lint errors.

## Lệnh & Mức Giảm

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

## Ví Dụ Thực Tế

```
# tsc (nhiều dòng)                      # rtk tsc
src/harness/context.ts(42,9):            src/harness/context.ts
  error TS2322: Type 'string' ...          L42  TS2322  Type mismatch
src/harness/loop.ts(18,5):                 src/harness/loop.ts
  error TS2554: Expected 2 args ...          L18  TS2554  Expected 2 args
```

## Lưu Ý

- Các linter cần output JSON (`ruff`, `golangci-lint`, `rubocop`) — RTK parse JSON nên dùng đúng formatter.
- `next build` có nhiều giai đoạn — RTK giữ log fail ở các bước quan trọng.
- Một số filters shell-out tới ripgrep (`rg`) — đảm bảo `rg` có trong PATH.

---

*Trở về [03 — Patterns](../03-patterns/)*