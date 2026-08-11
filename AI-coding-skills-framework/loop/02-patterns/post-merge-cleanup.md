# 🧹 Post-Merge Cleanup Loop

**Goal**: Dọn TODOs, cleanup, và merge debt sau khi merge — giữ repo sạch mà không đụng vào việc quan trọng đang triển khai.

## Scheduling

**Khuyên dùng**:
- `/loop 1d–6h` vào **off-peak** (VD: `22:00`, cuối tuần)
- Không chạy cùng lúc với PR Babysitter (Post-Merge chạy off-peak only)

## Required Skills

- `merge-cleanup` — Đọc recent merges, tìm TODOs/FIXMEs, dead code, leftover branches
- `minimal-fix` — Small fixes only

## State

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

## How the Loop Runs (Typical Cycle)

1. Đọc recent merges + `git log`.
2. Tìm TODO/FIXME mới, dead code, branches stale sau merge.
3. Với cleanup nhỏ, rõ ràng: worktree → implementer → verifier → PR.
4. Với thứ mơ hồ: ghi vào backlog, flag cho human.
5. Prune resolved items.

## Verification Strategy

- Small fixes only — không refactor, không đổi behavior.
- Verifier kiểm tra "smallest possible diff" — không đụng file không liên quan.
- Off-peak — không đụng vào release/maintenance window.

## Human Handoff Points

- Cleanup cần thay đổi behavior hoặc > N files
- Dead code xoá mà không chắc còn dùng
- Branches cần force-delete

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Cleanup đụng code đang hoạt động | Verifier kiểm tra behavior không đổi; small fixes only |
| TODO cleanup phá logic | Chỉ xoá TODO khi context rõ ràng; human gate |
| Chạy nhầm giờ | Off-peak scheduling bắt buộc |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có cleanup cần làm |
| Cleanup (L1→L2) | ~100k | Scan merges + small fixes |

**Cadence**: 1d–6h off-peak · **Tier**: low · **Suggested daily cap**: 200k tokens

```bash
npx @cobusgreyling/loop cost --pattern post-merge-cleanup --cadence 1d --level L1
```

## Success Metrics

- Số TODO/FIXME mới mỗi ngày (trend giảm = cleanup hoạt động)
- % cleanup merged không cần sửa lại
- Repo "sạch" score (ít stale branches, dead code)

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
