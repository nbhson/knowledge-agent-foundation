# 📖 File Smart Read Pattern

**Goal**: Đọc file "thông minh" — lấy signatures và structure thay vì toàn bộ nội dung. Giúp agent hiểu file lớn (1000+ dòng) chỉ trong vài chục token, đúng triết lý "Tầng 5 — Immediate Context" của harness.

## Dùng Khi Nào

- Agent cần hiểu cấu trúc một file lớn trước khi sửa.
- Repo lớn, agent hay `cat` cả file chỉ để tìm một function.
- Explore codebase nhanh: `rtk find` + `rtk grep` + `rtk smart`.

## Lệnh & Mức Giảm

| Lệnh gốc | RTK | Mục đích | Giảm |
|----------|-----|----------|------|
| `cat file.rs` | `rtk read file.rs` | Smart file reading — signatures/structure | ~60-90% |
| `cat file.rs` | `rtk read file.rs -l aggressive` | Chỉ signatures, strip bodies | ~90%+ |
| `head file.rs` | `rtk smart file.rs` | 2-line heuristic code summary | ~95% |
| `find` | `rtk find "*.rs" .` | Compact find results | ~70% |
| `grep -r` | `rtk grep "pattern" .` | Grouped search results | ~75% |
| `diff file1 file2` | `rtk diff file1 file2` | Condensed diff (exit 1 nếu khác) | ~75% |

## Ví Dụ Thực Tế

```
# rtk read file.rs -l aggressive
File: src/harness/context.rs (1,240 lines)
  pub struct ContextManager            // L42
    fn build(&mut self, ctx: Ctx)      // L45
    fn compress(&self) -> Result       // L210
    fn limit(&self) -> TokenBudget     // L390
...
```

## Lưu Ý

- **Không tương đương với `cat`**: `rtk read` trả về structure, không phải nội dung đầy đủ. Nếu agent cần chính xác nội dung (ví dụ để sửa một dòng cụ thể), agent vẫn nên dùng `cat`/`read_file` trực tiếp.
- **Liên kết harness**: pattern này chính là hiện thực hóa kỹ thuật "trích xuất chữ ký function" trong module `02-build-context` — chỉ đưa vào context phần cần thiết.

---

*Trở về [03 — Patterns](../03-patterns/)*