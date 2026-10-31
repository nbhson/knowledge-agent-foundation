# 📦 Dependency Sweeper Loop

**Goal**: Xử lý outdated packages / CVE alerts một cách an toàn — patch các phiên bản low-risk, escalate majors và denylisted packages cho human.

> **Tóm gọn ý nghĩa:** Dependency = thư viện bên ngoài mà code bạn dùng (package); "outdated" = phiên bản cũ; CVE = mã số của một lỗ hổng bảo mật được công bố. Loop này như "thợ bảo trì kho": thấy thư viện cũ hoặc có lỗ hổng thì vá các bản vá nhỏ tự động, còn bản nâng cấp lớn hay rủi ro thì dừng lại kêu người.

## Scheduling

**Khuyên dùng**:
- `/loop 6h–1d` (Grok, Claude Code) — tự chạy lại mỗi 6 giờ đến 1 ngày một lần
- GitHub Action cron daily
- Dependabot cho phần discovery; sweeper cho phần patch + verify (Dependabot = bot của GitHub tự báo thư viện cũ; discovery = phát hiện)

> **Tóm gọn 1 câu:** Nhịp chạy thưa (6 giờ tới 1 ngày) là đủ — việc vá thư viện không gấp bằng việc dập CI đỏ; để Dependabot phát hiện, loop chỉ lo vá và kiểm.

## Required Skills

- `dep-triage` — Đọc Dependabot alerts / `npm audit` / CVE feeds, classify severity + risk (`npm audit` = lệnh quét lỗ hổng của Node.js; severity = mức nghiêm trọng)
- `minimal-fix` — Patch nhỏ nhất cho CVE thấp rủi ro
- Project test skill — Full build + test để verify

> **Tóm gọn 1 câu:** Ba skill: đọc báo cáo lỗ hổng và xếp mức rủi ro, vá nhỏ nhất có thể, và build + test đầy đủ để xác nhận không hỏng gì.

## State

`dependency-sweeper-state.md`:

```markdown
# Dependency Sweeper State

Last run: 2026-06-09 16:00 UTC

## In-flight
- lodash 4.17.20 → 4.17.21 (CVE-2023-XXXX, low) — worktree open — verifier PASS — PR #1260

## Denylisted (human required)
- openssl 1.1 → 3.0 (major, breaking) — waiting human decision
```

Đọc state này thế nào: "In-flight" = đang xử lý — ví dụ thư viện lodash nâng từ 4.17.20 lên 4.17.21 để vá một CVE mức thấp, bản vá đã qua kiểm tra và đang là PR #1260 chờ merge. "Denylisted" = danh sách đen, các thư viện loop bị cấm tự đụng (như openssl vì nó nằm ở tầng bảo mật lõi) — phải chờ người quyết.

> **Tóm gọn 1 câu:** State có 2 ngăn: "đang vá" ghi tiến độ từng bản vá, "danh sách đen" ghi thứ nào bắt buộc người quyết.

## How the Loop Runs (Typical Cycle)

1. Đọc dependency alerts (Dependabot, `npm audit`, `pip-audit`, ...).
2. Với mỗi alert:
   - **Low-risk CVE, patch-only trong 30 ngày đầu**: worktree → implementer patch → verifier `npm ci && npm test` (`npm ci` = cài lại sạch thư viện đúng theo file khóa phiên bản).
   - **Major hoặc breaking**: không tự patch — escalate cho human (major = nâng số phiên bản lớn, thường kèm thay đổi làm hỏng code cũ).
   - **Denylisted package** (VD: `openssl`, `auth`, `payments` libs): escalate.
3. Mở PR với patch verified; human merge.
4. Prune resolved alerts (prune = dọn bỏ khỏi danh sách).

> **Tóm gọn 1 câu:** Luật ba nhánh: CVE nhỏ thì tự vá có kiểm tra, nâng cấp lớn hoặc thư viện nằm danh sách đen thì kêu người — và dù thế nào, người mới là người bấm merge.

## Verification Strategy

- Verifier = **full `npm ci && npm test`** (hoặc build + test tương đương) trong worktree. "Full" nghĩa là không test tắt — build lại từ đầu như CI làm.
- Không patch package mà không verify build — dependency thay đổi thường phá build ngầm (ví dụ: thư viện A được nâng lên kéo theo thư viện B không còn tương thích).
- Human gate trên **majors và denylisted packages** (human gate = cổng dừng bắt buộc có người duyệt).

> **Tóm gọn 1 câu:** Chưa build + test đầy đủ thì chưa coi là vá xong, vì nâng thư viện hay phá build một cách âm thầm.

## Human Handoff Points

- Major version bumps (breaking changes)
- Packages thuộc denylist (security, auth, payments, infra)
- CVEs không có patch rõ ràng
- Alerts đòi hỏi thay đổi code (không chỉ bump version — bump = chỉ nâng số phiên bản)

> **Tóm gọn 1 câu:** Bốn thứ thuộc tay người: nâng lớn, thư viện nhạy cảm, lỗ hổng chưa có bản vá, và bản vá đòi sửa code.

## Failure Modes & Mitigations

**Cách đọc bảng này:** cột "Failure" là sự cố loop có thể gây ra; cột "Mitigation" là màng lưới phòng nó. Ví dụ, dòng 1: nâng cấp lớn làm hỏng app mà không ai để ý → vì vậy mọi major bump đều bắt buộc qua cổng duyệt của người.

| Failure | Mitigation |
|---------|------------|
| Breaking upgrade không ai để ý | Human gate bắt buộc cho majors |
| Patch phá build | Verifier chạy full build + test |
| Chạy cùng lúc với CI đỏ | Pause Dependency Sweeper khi CI red trên main |
| Overwhelm với nhiều CVEs | Ưu tiên theo severity; batch theo tuần |

> **Tóm gọn 1 câu:** Rủi ro lớn nhất của pattern này là "vá lành lề mang rách" — phòng bằng full test sau mỗi bản vá và tạm dừng khi CI chính đang đỏ.

## Cost Profile

**Cách đọc bảng này:** mỗi dòng là một tình huống và giá token. Ví dụ, ngày không có alert mới (no-op) chỉ tốn ~5k token; một lần vá + kiểm đầy đủ tốn ~150k vì phải dựng worktree và build/test toàn bộ.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có alert mới |
| Triage alerts | ~20k | Đọc feeds + classify |
| Patch + verify (L2) | ~150k | Worktree + patch + full build/test |

**Cadence**: 6h–1d · **Tier**: medium · **Suggested daily cap**: 500k tokens

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **Tóm gọn 1 câu:** Chi phí trung bình: rẻ khi chỉ quét, đắt (~150k) khi thật sự vá — trần 500k token/ngày là mức an toàn.

## Success Metrics

- Time từ CVE alert đến patch merged
- % alerts resolved không cần human (low-risk only)
- Số lần patch phá build (mục tiêu: 0)

> **Tóm gọn 1 câu:** Đo 3 con số: vá nhanh bao lâu, bao nhiêu % tự xử được (chỉ đếm phần rủi ro thấp), và số lần vá làm hỏng build — mục tiêu là 0.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
