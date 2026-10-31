# 🧹 Post-Merge Cleanup Loop

**Goal**: Dọn TODOs, cleanup, và merge debt sau khi merge — giữ repo sạch mà không đụng vào việc quan trọng đang triển khai.

**Đọc Goal thế nào**: "TODO/FIXME" = ghi chú bỏ dở trong code kiểu "cần sửa chỗ này sau". "Merge debt" = rác tích tụ sau khi gộp code: nhánh cũ chưa xoá, code chết, TODO để lại. Loop này chạy lúc vắng người để quét rác đó, nhưng chỉ dọn việc **nhỏ và rõ ràng**.

## Scheduling

**Phần này giải thích**: chạy lúc nào cho an toàn.

**Khuyên dùng**:
- `/loop 1d–6h` vào **off-peak** (VD: `22:00`, cuối tuần) — "off-peak" = giờ thấp điểm, ít người đang code; dọn lúc đó thì ít va chạm với người thật.
- Không chạy cùng lúc với PR Babysitter (Post-Merge chạy off-peak only) — hai loop cùng đụng PR dễ giẫm chân nhau.

## Required Skills

**Phần này giải thích**: loop cần kỹ năng (skill = bộ chỉ thị đóng gói cho agent) nào.

- `merge-cleanup` — Đọc recent merges, tìm TODOs/FIXMEs, dead code, leftover branches. "Dead code" = code không còn ai gọi tới; "leftover branches" = nhánh git còn sót sau khi đã gộp.
- `minimal-fix` — Small fixes only. Skill này bị giới hạn: chỉ sửa lỗi nhỏ, không refactor (viết lại code lớn).

## State

**Phần này giải thích**: file ghi nhớ giữa các lần chạy, để loop không quên việc dở dang.

`post-merge-state.md`:

```markdown
# Post-Merge Cleanup State

Last run: 2026-06-09 22:00 UTC

## Cleanup Backlog
- [ ] PR #1255 để lại TODO trong `auth/service.py` (3 TODOs)
  Loop action: Draft fix proposed. Waiting human review.
- [ ] Branch fix/ci-auth-refresh chưa xoá sau merge
  Loop action: Suggest delete.

## Resolved (last 7d)
- PR #1240 — cleanup logs merged
```

Cách đọc ví dụ: mục đầu nghĩa là PR #1255 để lại 3 ghi chú TODO trong file `auth/service.py`; loop đã soạn bản sửa (draft) và đang chờ người duyệt, chưa tự merge. "Backlog" = danh sách việc tồn đọng.

## How the Loop Runs (Typical Cycle)

**Phần này giải thích**: một lượt chạy gồm các bước nào.

1. Đọc recent merges + `git log` — xem vừa gộp những gì. `git log` = lệnh xem lịch sử commit.
2. Tìm TODO/FIXME mới, dead code, branches stale sau merge — "stale" = nhánh cũ, không còn giá trị.
3. Với cleanup nhỏ, rõ ràng: worktree → implementer → verifier → PR. Dịch từng bước: làm trong **worktree** (bản sao tạm của repo, hỏng cũng không ảnh hưởng bản chính) → **implementer** (agent viết bản sửa) → **verifier** (agent riêng kiểm chứng) → tạo pull request chờ người duyệt.
4. Với thứ mơ hồ: ghi vào backlog, flag cho human — không tự đoán, để lại cho người quyết.
5. Prune resolved items — "prune" = dọn bỏ khỏi danh sách những việc đã xong, để state không phình to.

> **Tóm gọn 1 câu:** Loop này chạy giờ vắng người, quét rác để lại sau mỗi lần merge và tự sửa những việc nhỏ rõ ràng — còn lại thì ghi vào danh sách chờ người.

## Verification Strategy

**Phần này giải thích**: làm sao chắc cleanup không phá code đang chạy tốt.

- Small fixes only — không refactor, không đổi behavior. "Behavior" = hành vi của chương trình; sửa rác mà thay đổi cách app chạy là hỏng, không phải dọn.
- Verifier kiểm tra "smallest possible diff" — không đụng file không liên quan. "Diff" = tập thay đổi; bản sửa phải chạm đúng những file cần dọn.
- Off-peak — không đụng vào release/maintenance window. "Release window" = khung giờ tung bản mới ra người dùng, lúc này không ai được động vào repo.

## Human Handoff Points

**Phần này giải thích**: lúc nào loop phải dừng và giao cho người.

- Cleanup cần thay đổi behavior hoặc > N files — dọn dẹp mà phải đổi cách app chạy hoặc sửa nhiều file thì đó không còn là "dọn rác nhỏ".
- Dead code xoá mà không chắc còn dùng — xoá nhầm code đang được dùng ở chỗ khác là sự cố; không chắc thì hỏi người.
- Branches cần force-delete — "force-delete" = xoá cưỡng bức nhánh, vượt qua lớp bảo vệ mặc định của git; việc này cần người ra quyết định.

## Failure Modes & Mitigations

**Cách đọc bảng này**: cột "Failure" = lỗi loop hay mắc; cột "Mitigation" = cách phòng chống. Ví dụ dòng 1: loop dọn vào đúng code người khác đang sửa → phòng bằng verifier kiểm tra behavior không đổi.

| Failure | Mitigation |
|---------|------------|
| Cleanup đụng code đang hoạt động | Verifier kiểm tra behavior không đổi; small fixes only |
| TODO cleanup phá logic | Chỉ xoá TODO khi context rõ ràng; human gate |
| Chạy nhầm giờ | Off-peak scheduling bắt buộc |

## Cost Profile

**Cách đọc bảng này**: "Scenario" = tình huống; "Tokens/run" = số token (đơn vị tính tiền mô hình) mỗi lượt; "Notes" = giải thích. "No-op" = lượt chạy không có việc gì; "L1→L2" = loop nâng từ mức báo cáo lên mức tự sửa nhỏ.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có cleanup cần làm |
| Cleanup (L1→L2) | ~100k | Scan merges + small fixes |

**Cadence**: 1d–6h off-peak · **Tier**: low · **Suggested daily cap**: 200k tokens — "Tier" = mức rủi ro; "daily cap" = trần token mỗi ngày, vượt thì dừng.

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

## Success Metrics

**Phần này giải thích**: đo gì để biết loop có ích.

- Số TODO/FIXME mới mỗi ngày (trend giảm = cleanup hoạt động) — rác sinh ra ít dần nghĩa là loop và team đang dọn kịp.
- % cleanup merged không cần sửa lại — bản dọn được duyệt ngay, không bị đòi sửa lần nữa.
- Repo "sạch" score (ít stale branches, dead code) — thước đo chung: repo càng ít rác càng sạch.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
