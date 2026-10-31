# ⚡ Git Speedup Pattern

**Goal**: Giảm tới 93% output từ các lệnh git quen thuộc (`status`, `log`, `diff`, `push`, `add`, `commit`), giúp agent nhìn thấy trạng thái repo ngay lập tức thay vì đọc hàng chục dòng.

> Phần này giải thích: pattern nào dùng cho lệnh git nào, và output được gọt thế nào. Đây là pattern nền tảng — nên bật đầu tiên.

**Giải thích nhanh các từ khóa**: `git status` = báo file nào đã sửa/chưa commit. `git log` = lịch sử commit. `git diff` = phần khác nhau giữa code hiện tại và lần commit trước. Output "compact" = bản rút gọn chỉ còn thông tin cần thiết. Hook = cái chặn tự động đổi lệnh `git ...` thành `rtk git ...` khi agent chạy.

## Dùng Khi Nào

- Mọi phiên làm việc với git — đây là pattern nền tảng nên bật trước tiên.
- Agent liên tục gọi `git status`, `git log`, `git diff` để hiểu state repo. (state repo = tình trạng hiện tại: file nào đổi, commit nào mới.)

> **Tóm gọn 1 câu:** Agent dùng git hàng chục lần mỗi phiên — nén output git là chỗ tiết kiệm lớn nhất và an toàn nhất.

## Lệnh & Mức Giảm

Cách đọc bảng này: cột **Lệnh gốc** là lệnh git thường dùng; cột **RTK** là lệnh thay thế; cột **Output** là RTK trả về dạng gì; cột **Giảm** là % số dòng được cắt. Ví dụ dòng `git push`: bản gốc in 15 dòng tiến trình, bản RTK chỉ còn 1 dòng `ok main` — bớt ~93%.

| Lệnh gốc | RTK | Output | Giảm |
|----------|-----|--------|------|
| `git status` | `rtk git status` | Compact stat, grouped by state | ~80% |
| `git log -n 10` | `rtk git log -n 10` | Hash + author + subject only | ~70% |
| `git diff` | `rtk git diff` | Reduced context, headers stripped | ~75% |
| `git add` | `rtk git add` | `ok` | ~95% |
| `git commit -m "msg"` | `rtk git commit -m "msg"` | `ok abc1234` | ~95% |
| `git push` | `rtk git push` | `ok main` | ~93% |
| `git pull` | `rtk git pull` | `ok 3 files +10 -2` | ~90% |

Giải nghĩa vài ô trong bảng: `-n 10` = lấy 10 commit gần nhất. Hash = mã định danh commit (ví dụ `abc1234`). `+10 -2` = thêm 10 dòng, bỏ 2 dòng. Các lệnh `add`/`commit`/`push` bản gốc in cả tiến trình dài dòng, nhưng agent chỉ cần biết "thành công chưa" — nên RTK trả về `ok`.

> **Tóm gọn 1 câu:** Lệnh git đổi trạng thái (add/commit/push/pull) chỉ cần câu trả lời `ok` — bản gốc in cả quá trình là noise thuần túy.

## Ví Dụ Thực Tế

```
# git push (15 lines)                    # rtk git push (1 line)
Enumerating objects: 5, done.             ok main
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
...
```

Cách đọc ví dụ: cột trái là output gốc — đếm object, nén delta (kiểu nén dữ liệu git dùng khi push), v.v. — là chi tiết nội bộ của git. Cột phải là dòng duy nhất agent cần: push thành công lên nhánh `main`.

> **Tóm gọn 1 câu:** `ok main` = "đã đẩy lên nhánh main thành công" — 15 dòng tiến trình rút thành 1 dòng.

## Lưu Ý

- `git diff` bị nén — nếu agent cần chi tiết diff đầy đủ, agent có thể gọi `git diff` trực tiếp (không qua RTK) hoặc thêm vào `exclude_commands` khi cần. (`exclude_commands` = danh sách lệnh được miễn nén, khai báo trong `config.toml`.)
- Pipelines như `git diff | grep foo` có thể bị ảnh hưởng bởi format nén — kiểm tra nếu agent cần parse output. (Pipeline `|` = lấy output lệnh trước làm input lệnh sau; parse = đọc output theo máy — script cần đúng định dạng gốc.)

> **Tóm gọn 1 câu:** Nén git rất an toàn, trừ hai chỗ: khi cần diff đầy đủ chi tiết và khi script phụ thuộc đúng định dạng gốc.

---

*Trở về [03 — Patterns](../03-patterns/)*
