# 📝 Changelog Drafter Loop

**Goal**: Tự động draft release notes từ merge history — giảm đau đầu "release sắp tới có những gì?".

## Scheduling

**Khuyên dùng**:
- `/loop 1d` trong release prep
- Manual hoặc tag-triggered khi chuẩn bị release
- GitHub Action `changelog-drafter.yml` (VD: mỗi Thứ Hai, mở release-prep issue)

## Required Skills

- `changelog-draft` — Đọc merge history (commits, PRs, issues), nhóm theo category, tạo draft
- Project conventions skill — Biết cách project của bạn phân loại changes (breaking/feature/fix)

## State

`changelog-drafter-state.md` hoặc section trong `STATE.md`:

```markdown
# Changelog Drafter State

Last run: 2026-06-09 09:00 UTC

## Since last tag: v1.4.0
- Merged PRs: 42
- Breaking: 2
- Features: 15
- Fixes: 20
- Draft: RELEASE_NOTES_DRAFT.md (chờ human approve)
```

## How the Loop Runs (Typical Cycle)

1. Xác định mốc cuối (last tag / last release).
2. Thu thập merged PRs + commits từ mốc đó.
3. Nhóm theo category (breaking, feature, fix, docs, deps).
4. Draft `RELEASE_NOTES_DRAFT.md` (hoặc section cho GitHub release).
5. **Human approve trước khi publish hoặc cập nhật CHANGELOG** — không auto-publish.

## Verification Strategy

- Level **L1 draft only** — human review trước khi publish.
- Draft phải traceable: mỗi entry trỏ về PR/issue.
- **Không auto-publish** — đây là read-mostly pattern, rủi ro thấp nhưng không tự xuất bản.

## Human Handoff Points

- Approve draft trước khi publish/CHANGELOG update
- Quyết định version bump (major/minor/patch)
- Breaking changes cần highlight

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Draft thiếu entries | Verify count merged PRs vs draft entries |
| Phân loại sai (breaking vs fix) | Human review; conventions skill rõ ràng |
| Publish nhầm | Không auto-publish; human gate bắt buộc |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| Draft | ~30k | Đọc merge history + phân loại |
| No-op | ~3k | Không có commits mới |

**Cadence**: 1d hoặc tag · **Tier**: low · **Suggested daily cap**: 50k tokens

```bash
npx @cobusgreyling/loop cost --pattern changelog-drafter --cadence 1d --level L1
```

## Success Metrics

- Time từ "release prep" đến "draft sẵn sàng"
- % draft entries chính xác (không phải sửa lại)
- Giảm câu hỏi "release này có gì?"

> **Excellent low-risk companion** cho Post-Merge Cleanup — chạy an toàn cùng các loops khác.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
