# 🧪 Test Only Failures Pattern

**Goal**: Chỉ giữ lại **failures** khi chạy test — các tests pass bị gom thành một con số. Giúp agent tập trung vào đúng vấn đề cần sửa thay vì lạc trong hàng trăm dòng `... ok`.

> Phần này giải thích: cách RTK chỉ hiển thị test bị lỗi, dùng cho các framework test nào, và hai điểm cần cẩn thận.

**Giải thích nhanh các từ khóa**: test = bài kiểm tra tự động cho code. Pass = chạy đúng; failure (fail) = chạy sai — đó là thứ cần sửa. Regression = lỗi mới xuất hiện ở chỗ vốn chạy đúng. Traceback = bản in ra cho biết lỗi xảy ra ở dòng nào. CI = hệ thống tự chạy test sau mỗi lần commit; "CI đỏ" = có test đang fail.

## Dùng Khi Nào

- CI đang đỏ, cần agent nhìn ra test nào fail nhanh nhất.
- Debug một thay đổi gây regression hàng loạt tests. (Debug = lần theo dấu tìm nguyên nhân lỗi.)

> **Tóm gọn 1 câu:** Khi có test fail, pattern này lọc sẵn phần lỗi đưa lên — agent không phải lục giữa trăm dòng `ok`.

## Lệnh & Mức Giảm

Cách đọc bảng này: cột **Lệnh gốc** là lệnh chạy test của từng framework; cột **RTK** là lệnh thay thế; cột **Output** là RTK trả về cái gì; cột **Giảm** là % output được cắt. Ví dụ dòng `cargo test`: bản gốc in cả 15 test, bản RTK chỉ in 2 test đang fail — bớt ~90%.

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

Giải nghĩa vài ô trong bảng: "pass collapsed" = toàn bộ test chạy đúng gom lại thành một dòng thống kê, ví dụ `13 passed`. "traceback trimmed" = phần báo lỗi chỉ giữ dòng chỉ ra chỗ sai. NDJSON = format mỗi dòng một JSON riêng (go test dùng). "Generic" = mọi lệnh test khác chưa có bộ lọc riêng vẫn dùng được qua `rtk test <cmd>`. rspec (Ruby) trả về JSON nên mức giảm thấp hơn — JSON cần cả cấu trúc.

> **Tóm gọn 1 câu:** Dù bạn dùng framework nào, RTK đều chỉ đưa phần test fail lên mặt bàn — số lượng chỉ mất một dòng thống kê.

## Ví Dụ Thực Tế

```
# cargo test (200+ lines on failure)     # rtk test cargo test (~20 lines)
running 15 tests                          FAILED: 2/15 tests
test utils::test_parse ... ok               test_edge_case: assertion failed
test utils::test_format ... ok              test_overflow: panic at utils.rs:18
...
```

Cách đọc ví dụ: cột trái in từng test một kèm kết quả `ok` — trăm dòng chỉ để nói "13 test chạy tốt". Cột phải đi thẳng vào vấn đề: 2/15 test fail, mỗi fail một dòng nói lỗi gì và ở đâu (`assertion failed` = kết quả so sánh sai; `panic at utils.rs:18` = chương trình văng lỗi tại dòng 18 file utils.rs).

Khi lệnh fail, RTK lưu toàn bộ output thô:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Giải nghĩa: `~/.local/share/rtk/tee/` là thư mục lưu log; `1707753600` là thời điểm chạy (dạng timestamp). Agent có thể đọc log đầy đủ nếu cần — không cần chạy lại lệnh. (Cơ chế này gọi là tee recovery: như công tắc tee nước — nhánh nhỏ ra màn hình, nhánh đầy đủ đổ vào file.)

> **Tóm gọn 1 câu:** RTK chỉ hiện phần fail, nhưng lưu nguyên bản gốc ra file log — cần chi tiết thì đọc log, không phải chạy lại.

## Lưu Ý

- **Flaky tests**: không nên auto-sửa chỉ dựa trên 1 lần fail — pattern này chỉ giúp *thấy* failures nhanh, quyết định sửa vẫn thuộc agent/human theo nguyên tắc của harness (Feedback Loops & Guardrails). (Flaky test = test lúc pass lúc fail không rõ lý do — thường do trật tự chạy hay dữ liệu trùng, không hẳn do code sai.)
- Với rspec JSON output cần `rspec` đã cấu hình formatter. (formatter = bộ định dạng output; phải bật sẵn JSON formatter thì RTK mới đọc được.)

> **Tóm gọn 1 câu:** Pattern này là kính lọc để thấy lỗi nhanh — còn sửa hay không sửa, và sửa cái gì, vẫn là quyết định của agent/human.

---

*Trở về [03 — Patterns](../03-patterns/)*
