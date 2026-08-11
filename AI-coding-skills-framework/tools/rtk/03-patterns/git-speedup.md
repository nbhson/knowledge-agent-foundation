# ⚡ Git Speedup Pattern

**Goal**: Giảm tới 93% output từ các lệnh git quen thuộc (`status`, `log`, `diff`, `push`, `add`, `commit`), giúp agent nhìn thấy trạng thái repo ngay lập tức thay vì đọc hàng chục dòng.

## Dùng Khi Nào

- Mọi phiên làm việc với git — đây là pattern nền tảng nên bật trước tiên.
- Agent liên tục gọi `git status`, `git log`, `git diff` để hiểu state repo.

## Lệnh & Mức Giảm

| Lệnh gốc | RTK | Output | Giảm |
|----------|-----|--------|------|
| `git status` | `rtk git status` | Compact stat, grouped by state | ~80% |
| `git log -n 10` | `rtk git log -n 10` | Hash + author + subject only | ~70% |
| `git diff` | `rtk git diff` | Reduced context, headers stripped | ~75% |
| `git add` | `rtk git add` | `ok` | ~95% |
| `git commit -m "msg"` | `rtk git commit -m "msg"` | `ok abc1234` | ~95% |
| `git push` | `rtk git push` | `ok main` | ~93% |
| `git pull` | `rtk git pull` | `ok 3 files +10 -2` | ~90% |

## Ví Dụ Thực Tế

```
# git push (15 lines)                    # rtk git push (1 line)
Enumerating objects: 5, done.             ok main
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
...
```

## Lưu Ý

- `git diff` bị nén — nếu agent cần chi tiết diff đầy đủ, agent có thể gọi `git diff` trực tiếp (không qua RTK) hoặc thêm vào `exclude_commands` khi cần.
- Pipelines như `git diff | grep foo` có thể bị ảnh hưởng bởi format nén — kiểm tra nếu agent cần parse output.

---

*Trở về [03 — Patterns](../03-patterns/)*