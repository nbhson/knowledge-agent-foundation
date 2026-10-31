# 📝 Changelog Drafter Loop

**Goal**: Tự động draft release notes từ merge history — giảm đau đầu "release sắp tới có những gì?".

> **Tóm gọn ý nghĩa:** Loop này là "thư ký ghi biên bản release" — nó đọc lịch sử merge (các PR đã gộp vào nhánh chính) rồi viết sẵn bản nhái release notes, chờ bạn duyệt. Mức rủi ro thấp nhất trong cả 7 pattern vì nó hầu như chỉ đọc, không tự xuất bản gì.

## Scheduling

**Khuyên dùng**:
- `/loop 1d` trong release prep (`/loop 1d` = lệnh bảo agent tự chạy lại mỗi 1 ngày một lần)
- Manual hoặc tag-triggered khi chuẩn bị release (tag = nhãn đánh dấu phiên bản, ví dụ `v1.4.0`)
- GitHub Action `changelog-drafter.yml` (VD: mỗi Thứ Hai, mở release-prep issue)

> **Tóm gọn 1 câu:** Chọn nhịp chạy mỗi ngày một lần hoặc mỗi khi gắn tag phiên bản mới.

## Required Skills

- `changelog-draft` — Đọc merge history (commits, PRs, issues), nhóm theo category, tạo draft (draft = bản nháp chưa chính thức)
- Project conventions skill — Biết cách project của bạn phân loại changes (breaking/feature/fix; "breaking" = thay đổi làm hỏng người dùng cũ)

> **Tóm gọn 1 câu:** Cần 2 skill: một skill đọc lịch sử merge và nhóm thay đổi, một skill biết quy ước phân loại của dự án.

## State

State = sổ ghi trạng thái mà loop đọc và ghi lại mỗi lần chạy, để lần sau nhớ việc cũ.

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

Đọc state này thế nào: "Since last tag: v1.4.0" nghĩa là "tính từ phiên bản v1.4.0 trở đi"; 42 PR đã gộp, trong đó 2 cái breaking, 15 tính năng, 20 sửa lỗi; bản nháp nằm trong file `RELEASE_NOTES_DRAFT.md` và đang chờ người duyệt.

> **Tóm gọn 1 câu:** State ghi lại "từ tag cuối đã có gì" để lần chạy sau biết lấy từ đâu, khỏi thu thập trùng.

## How the Loop Runs (Typical Cycle)

1. Xác định mốc cuối (last tag / last release) — mốc = điểm bắt đầu đếm thay đổi mới.
2. Thu thập merged PRs + commits từ mốc đó (commit = một lần lưu thay đổi trong git).
3. Nhóm theo category (breaking, feature, fix, docs, deps).
4. Draft `RELEASE_NOTES_DRAFT.md` (hoặc section cho GitHub release).
5. **Human approve trước khi publish hoặc cập nhật CHANGELOG** — không auto-publish (publish = đăng bản chính thức cho mọi người thấy).

> **Tóm gọn 1 câu:** Loop đọc lịch sử merge từ tag cuối, nhóm theo loại, viết bản nháp — và luôn dừng chờ người duyệt trước khi đăng.

## Verification Strategy

- Level **L1 draft only** — human review trước khi publish (L1 = mức tự chủ thấp nhất: chỉ báo cáo, không tự hành động).
- Draft phải traceable: mỗi entry trỏ về PR/issue (traceable = truy ngược được nguồn, biết entry nào đến từ PR nào).
- **Không auto-publish** — đây là read-mostly pattern, rủi ro thấp nhưng không tự xuất bản.

> **Tóm gọn 1 câu:** Loop chỉ được viết nháp, không được đăng; mỗi dòng nháp phải chỉ ra được nguồn PR/issue gốc.

## Human Handoff Points

Handoff = điểm loop dừng lại và bàn giao cho con người quyết.

- Approve draft trước khi publish/CHANGELOG update
- Quyết định version bump (major/minor/patch — tăng số phiên bản lớn/nhỏ/vá lỗi)
- Breaking changes cần highlight (highlight = làm nổi bật để người đọc thấy ngay)

> **Tóm gọn 1 câu:** Ba việc người quyết: duyệt bản nháp, chọn số phiên bản tăng thế nào, và làm nổi các thay đổi breaking.

## Failure Modes & Mitigations

**Cách đọc bảng này:** cột "Failure" là kiểu loop hỏng; cột "Mitigation" là cách phòng hỏng đó. Ví dụ, dòng đầu: nếu bản nháp bị thiếu PR nào đó, hãy đếm số PR đã gộp và đối chiếu với số mục trong nháp.

| Failure | Mitigation |
|---------|------------|
| Draft thiếu entries | Verify count merged PRs vs draft entries |
| Phân loại sai (breaking vs fix) | Human review; conventions skill rõ ràng |
| Publish nhầm | Không auto-publish; human gate bắt buộc |

> **Tóm gọn 1 câu:** Ba rủi ro chính là thiếu mục, phân loại sai, và đăng nhầm — phòng bằng đối chiếu số đếm, review người, và cấm auto-publish.

## Cost Profile

**Cách đọc bảng này:** "Tokens/run" là lượng token (đơn vị tính chi phí mô hình) tiêu mỗi lần chạy. Ví dụ, một lần chạy có thay đổi mới tốn ~30k token, còn lần chạy không có gì mới chỉ tốn ~3k.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| Draft | ~30k | Đọc merge history + phân loại |
| No-op | ~3k | Không có commits mới |

**Cadence**: 1d hoặc tag · **Tier**: low · **Suggested daily cap**: 50k tokens (cap = trần chi phí không được vượt mỗi ngày)

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **Tóm gọn 1 câu:** Đây là loop rẻ nhất bảng: thường dưới 50k token/ngày, có ngày gần như miễn phí (no-op).

## Success Metrics

Metrics = chỉ số đo loop có làm tốt không.

- Time từ "release prep" đến "draft sẵn sàng"
- % draft entries chính xác (không phải sửa lại)
- Giảm câu hỏi "release này có gì?"

> **Excellent low-risk companion** cho Post-Merge Cleanup — chạy an toàn cùng các loops khác.

> **Tóm gọn 1 câu:** Đo loop tốt không bằng "nó chạy chưa" mà bằng "bản nháp ra nhanh không, đúng không, và có ai còn phải hỏi 'release này có gì' nữa không".

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
