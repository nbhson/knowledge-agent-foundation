# 🧪 Test Only Failures Pattern

**Goal**: Chỉ giữ lại **failures** khi chạy test — các tests pass bị gom thành một con số. Giúp agent tập trung vào đúng vấn đề cần sửa thay vì lạc trong hàng trăm dòng `... ok`.

## Dùng Khi Nào

- CI đang đỏ, cần agent nhìn ra test nào fail nhanh nhất.
- Debug một thay đổi gây regression hàng loạt tests.

## Lệnh & Mức Giảm

| Lệnh gốc | RTK | Output | Giảm |
|----------|-----|--------|------|
| `cargo test` | `rtk cargo test` | Failures only, pass collapsed | ~90% |
| `npm test` | `rtk npm test` | Failures only, pass collapsed | ~90% |
| `pytest` | `rtk pytest` | Failures only, traceback trimmed | ~90% |
| `go test` | `rtk go test` | NDJSON parsed, failures only | ~90% |
| `jest` | `rtk jest` | Failures only | ~90% |
| `vitest` | `rtk vitest` | Failures only | ~90% |
| `rspec` | `rtk rspec` | JSON, failures only | ~60%+ |
| Generic | `rtk test <cmd>` | Failures only | ~90% |

## Ví Dụ Thực Tế

```
# cargo test (200+ lines on failure)     # rtk test cargo test (~20 lines)
running 15 tests                          FAILED: 2/15 tests
test utils::test_parse ... ok               test_edge_case: assertion failed
test utils::test_format ... ok              test_overflow: panic at utils.rs:18
...
```

Khi lệnh fail, RTK lưu toàn bộ output thô:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Agent có thể đọc log đầy đủ nếu cần — không cần chạy lại lệnh.

## Lưu Ý

- **Flaky tests**: không nên auto-sửa chỉ dựa trên 1 lần fail — pattern này chỉ giúp *thấy* failures nhanh, quyết định sửa vẫn thuộc agent/human theo nguyên tắc của harness (Feedback Loops & Guardrails).
- Với rspec JSON output cần `rspec` đã cấu hình formatter.

---

*Trở về [03 — Patterns](../03-patterns/)*