# 🧩 03. Bốn Pattern Sử Dụng RTK

> Đây là **4 pattern sử dụng RTK** phổ biến và hữu ích nhất khi làm việc với AI coding agents. Mỗi pattern trả lời: dùng khi nào, lệnh nào, mức giảm output, và lưu ý.

## Bảng Tổng Hợp

| Pattern | Dùng khi nào | Giảm output | Token cost trước |
|---------|--------------|-------------|------------------|
| [Git Speedup](git-speedup.md) | Làm việc với git mỗi ngày | ~70-93% | High (status/log/diff dài) |
| [Test Only Failures](test-only-failures.md) | Chạy test, debug failures | ~90% | Very high (test output khổng lồ) |
| [File Smart Read](file-smart-read.md) | Đọc file lớn để hiểu code | ~60-90% | High (file dài) |
| [Build & Lint Compact](build-lint-compact.md) | Build/lint hàng ngày | ~75-85% | Medium-High |

## Pattern Picker — Chọn Pattern Nào?

```
What hurts right now?
  ├── Git status/log/diff ngốn context? ──► Git Speedup
  ├── Test output dài, agent lạc trong noise? ──► Test Only Failures
  ├── Agent đọc cả file lớn thay vì phần cần? ──► File Smart Read
  ├── Build/lint/output dài dòng? ──► Build & Lint Compact
  └── Bạn dùng tất cả? ──► Cài hook (`rtk init -g`) — nó tự áp dụng hết
```

### Cost-aware Picks

| Tình huống | Nên chọn | Tránh |
|------------|----------|-------|
| Token budget eo hẹp | Git Speedup (git push/status) | Test Only Failures trên mọi lần chạy |
| CI đang đỏ | Test Only Failures | Full test output mỗi lần |
| Repo lớn, ít quen thuộc | File Smart Read | `cat` toàn bộ file |
| Build thường xuyên | Build & Lint Compact | Giữ nguyên output verbose |

## Overlap Rules

| Combination | Rule |
|-------------|------|
| Git Speedup + Test Only Failures | Both work fine — RTK tự routing theo command |
| File Smart Read + Git Speedup | `rtk read` cho file, `rtk git` cho git — không xung đột |
| Tất cả patterns | Chỉ cần hook bật — agent không cần gọi thủ công |

## First Pattern Recommendation

Nếu mới bắt đầu, hãy bật **Git Speedup** trước — nó an toàn, dễ verify (`git status` → `rtk git status`), và áp dụng cho mọi phiên làm việc với git.

## Cách Dùng Một Pattern

1. **Chọn pattern**: xem bảng trên hoặc decision tree.
2. **Bật bằng hook**: `rtk init -g` cho tool của bạn (xem [02-setup](../02-setup/)).
3. **Verify**: chạy thử command và so sánh output thô vs output RTK.
4. **Đo lường**: `rtk gain` để xem token đã tiết kiệm (xem [04-savings](../04-savings/)).
5. **Tinh chỉnh**: thêm `exclude_commands` trong `config.toml` nếu lệnh nào bị rewrite không mong muốn.

> **Quy tắc vàng**: RTK rewrite là transparent — nếu một lệnh quan trọng cần output đầy đủ, thêm nó vào `exclude_commands` thay vì tắt hẳn hook.

---

*Trở về [rtk/README.md](../)* · Trước: [02 — Setup](../02-setup/) · Tiếp theo: [04 — Savings](../04-savings/)