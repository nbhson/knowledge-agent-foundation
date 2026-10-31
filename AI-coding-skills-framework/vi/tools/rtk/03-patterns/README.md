# 🧩 03. Bốn Pattern Sử Dụng RTK

> Đây là **4 pattern dùng RTK** phổ biến và đáng tiền nhất khi làm việc với AI coding agents. Mỗi pattern trả lời gọn: dùng khi nào, xài lệnh nào, giảm được bao nhiêu output, và cần lưu ý gì.

## Bảng Tổng Hợp

Pattern = kiểu dùng RTK cho một nhóm lệnh cụ thể (git, test, đọc file, build). Cách đọc bảng này: mỗi dòng là một pattern; cột "Dùng khi nào" cho biết tình huống nên bật; "Giảm output" là mức nén bạn có thể kỳ vọng; "Token cost trước" mô tả mức ngốn token khi chưa có RTK. Ví dụ, Test Only Failures giảm ~90% vì các test pass bị gom thành một con số.

| Pattern | Dùng khi nào | Giảm output | Token cost trước |
|---------|--------------|-------------|------------------|
| [Git Speedup](git-speedup.md) | Làm việc với git mỗi ngày | ~70-93% | High (status/log/diff dài) |
| [Test Only Failures](test-only-failures.md) | Chạy test, debug failures | ~90% | Very high (test output khổng lồ) |
| [File Smart Read](file-smart-read.md) | Đọc file lớn để hiểu code | ~60-90% | High (file dài) |
| [Build & Lint Compact](build-lint-compact.md) | Build/lint hàng ngày | ~75-85% | Medium-High |

> **Tóm gọn 1 câu:** Bốn pattern phủ bốn loại lệnh ngốn token nhất (git, test, đọc file, build/lint) — mỗi dòng trong bảng nói dùng lúc nào và nén được bao nhiêu.

## Pattern Picker — Chọn Pattern Nào?

Phần này là cây quyết định: trả lời câu hỏi "cái gì đang ngốn của bạn lúc này", chọn đúng một nhánh.

```
What hurts right now?
  ├── Git status/log/diff ngốn context? ──► Git Speedup
  ├── Test output dài, agent lạc trong noise? ──► Test Only Failures
  ├── Agent đọc cả file lớn thay vì phần cần? ──► File Smart Read
  ├── Build/lint/output dài dòng? ──► Build & Lint Compact
  └── Bạn dùng tất cả? ──► Cài hook (`rtk init -g`) — nó tự áp dụng hết
```

Đọc từ trên xuống: mỗi nhánh là một loại "đau" và pattern chữa nó. Hàng cuối: cài hook một lần là RTK tự chọn pattern theo từng lệnh, khỏi cần chọn tay.

### Cost-aware Picks

Phần này ghép tình huống với lựa chọn nên dùng và thứ nên tránh.

Cách đọc bảng này: cột "Tình huống" là bối cảnh của bạn; "Nên chọn" là pattern hợp; "Tránh" là cách làm tốn token trong tình huống đó (CI = hệ chạy test tự động khi có code mới; verbose = dài dòng chi tiết). Ví dụ, CI đang đỏ thì bật Test Only Failures, đừng để agent xem full test output mỗi lần.

| Tình huống | Nên chọn | Tránh |
|------------|----------|-------|
| Token budget eo hẹp | Git Speedup (git push/status) | Test Only Failures trên mọi lần chạy |
| CI đang đỏ | Test Only Failures | Full test output mỗi lần |
| Repo lớn, ít quen thuộc | File Smart Read | `cat` toàn bộ file |
| Build thường xuyên | Build & Lint Compact | Giữ nguyên output verbose |

> **Tóm gọn 1 câu:** Chọn pattern theo thứ đang "đau": git → Git Speedup, test → Test Only Failures, file lớn → File Smart Read, build → Build & Lint Compact; dùng hết thì cài hook một lần.

## Overlap Rules

Phần này trả lời lo lắng "bật nhiều pattern có xung đột nhau không" — câu trả lời là không.

Cách đọc bảng này: cột "Combination" là các pattern chạy cùng nhau; "Rule" nói chúng ứng xử thế nào (routing = RTK tự chọn pattern phù hợp theo từng lệnh được gọi). Ví dụ, `rtk read` lo file còn `rtk git` lo git, hai cái không tranh nhau.

| Combination | Rule |
|-------------|------|
| Git Speedup + Test Only Failures | Both work fine — RTK tự routing theo command |
| File Smart Read + Git Speedup | `rtk read` cho file, `rtk git` cho git — không xung đột |
| Tất cả patterns | Chỉ cần hook bật — agent không cần gọi thủ công |

> **Tóm gọn 1 câu:** Các pattern không xung đột — hook bật một lần là RTK tự định tuyến từng lệnh đến pattern đúng.

## First Pattern Recommendation

Nếu mới bắt đầu, bạn cứ bật **Git Speedup** trước — vừa an toàn, vừa dễ kiểm chứng (`git status` → `rtk git status`), lại dùng được cho mọi phiên làm việc với git.

> **Tóm gọn 1 câu:** Người mới nên bật Git Speedup trước: an toàn, dễ so sánh kiểm chứng, và áp dụng cho mọi phiên có git.

## Cách Dùng Một Pattern

Phần này là 5 bước quy trình: chọn, bật, kiểm chứng, đo, tinh chỉnh.

1. **Chọn pattern**: xem bảng trên hoặc decision tree.
2. **Bật bằng hook**: `rtk init -g` cho tool của bạn (xem [02-setup](../02-setup/)).
3. **Verify**: chạy thử command và so sánh output thô vs output RTK.
4. **Đo lường**: `rtk gain` để xem token đã tiết kiệm (xem [04-savings](../04-savings/)).
5. **Tinh chỉnh**: thêm `exclude_commands` (danh sách lệnh bị loại khỏi nén) trong `config.toml` nếu lệnh nào bị rewrite không mong muốn.

> **Quy tắc vàng**: RTK rewrite chạy ngầm trong suốt — nếu lệnh nào quan trọng cần giữ nguyên output đầy đủ, bạn thêm nó vào `exclude_commands` thay vì tắt hẳn cả hook.

> **Tóm gọn 1 câu:** Quy trình 5 bước: chọn pattern → bật hook → so sánh output → đo bằng `rtk gain` → loại lệnh nhạy cảm bằng `exclude_commands` thay vì tắt hook.

---

*Trở về [rtk/README.md](../)* · Trước: [02 — Setup](../02-setup/) · Tiếp theo: [04 — Savings](../04-savings/)
