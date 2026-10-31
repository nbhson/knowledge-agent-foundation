# 📖 File Smart Read Pattern

**Goal**: Đọc file "thông minh" — lấy signatures và structure thay vì toàn bộ nội dung. Giúp agent hiểu file lớn (1000+ dòng) chỉ trong vài chục token, đúng triết lý "Tầng 5 — Immediate Context" của harness.

> Phần này giải thích: smart read là gì, khi nào nên dùng, và mỗi lệnh cắt bớt được bao nhiêu output.

**Giải thích nhanh các từ khóa**: signature = dòng khai báo hàm (tên, tham số, kiểu trả về) — không có thân hàm. Structure = bản đồ file: có những struct/hàm nào, nằm ở dòng nào. Harness = bộ khung điều khiển agent. "Tầng 5 — Immediate Context" = tầng context gần nhất, thứ model đọc trực tiếp mỗi lượt suy nghĩ.

## Dùng Khi Nào

- Agent cần hiểu cấu trúc một file lớn trước khi sửa.
- Repo lớn, agent hay `cat` cả file chỉ để tìm một function. (`cat` = in nguyên cả file ra terminal — tốn token nhất.)
- Explore codebase nhanh: `rtk find` + `rtk grep` + `rtk smart`. (find = tìm file theo tên; grep = tìm dòng chứa chữ cần.)

> **Tóm gọn 1 câu:** Cần nắm "file này có gì, ở đâu" thì dùng smart read; cần đọc đúng từng chữ thì mới dùng `cat`.

## Lệnh & Mức Giảm

Cách đọc bảng này: cột **Lệnh gốc** là lệnh bash quen thuộc; cột **RTK** là lệnh thay thế; cột **Mục đích** nói RTK trả về cái gì; cột **Giảm** là phần trăm output được cắt. Ví dụ dòng đầu: thay vì `cat file.rs` in cả file, `rtk read file.rs` chỉ trả về signatures nên bớt ~60-90%.

| Lệnh gốc | RTK | Mục đích | Giảm |
|----------|-----|----------|------|
| `cat file.rs` | `rtk read file.rs` | Smart file reading — signatures/structure | ~60-90% |
| `cat file.rs` | `rtk read file.rs -l aggressive` | Chỉ signatures, strip bodies | ~90%+ |
| `head file.rs` | `rtk smart file.rs` | 2-line heuristic code summary | ~95% |
| `find` | `rtk find "*.rs" .` | Compact find results | ~70% |
| `grep -r` | `rtk grep "pattern" .` | Grouped search results | ~75% |
| `diff file1 file2` | `rtk diff file1 file2` | Condensed diff (exit 1 nếu khác) | ~75% |

Giải nghĩa vài ô trong bảng: `-l aggressive` = chế độ cắt mạnh nhất, chỉ giữ dòng khai báo. `head` = in vài dòng đầu file. `diff` = so sánh hai file, in phần khác nhau; "exit 1" = mã thoát khác 0, tức là có khác biệt — script dùng để kiểm tra tự động.

> **Tóm gọn 1 câu:** Mỗi lệnh RTK ở trên thay một lệnh bash "nói nhiều" bằng bản gọn, cắt từ 60% tới hơn 90% output.

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

Cách đọc ví dụ: agent nhận về 1 dòng tên file + 4-5 dòng danh sách struct/hàm, kèm vị trí dòng (L42 = dòng 42, L210 = dòng 210). Toàn bộ thân hàm bị bỏ. Agent thấy ngay file có gì, nằm ở đâu — như đọc mục lục thay vì đọc cả cuốn sách.

> **Tóm gọn 1 câu:** File 1.240 dòng chỉ còn vài dòng mục lục hàm kèm số dòng — agent tìm đúng chỗ rồi mới đọc phần đó.

## Lưu Ý

- **Không tương đương với `cat`**: `rtk read` trả về structure, không phải nội dung đầy đủ. Nếu agent cần chính xác nội dung (ví dụ để sửa một dòng cụ thể), agent vẫn nên dùng `cat`/`read_file` trực tiếp.
- **Liên kết harness**: pattern này chính là hiện thực hóa kỹ thuật "trích xuất chữ ký function" trong module `02-build-context` — chỉ đưa vào context phần cần thiết.

> **Tóm gọn 1 câu:** Smart read là bản đồ, không phải nguyên bản file — sửa chính xác từng dòng thì vẫn phải mở file thật.

---

*Trở về [03 — Patterns](../03-patterns/)*
