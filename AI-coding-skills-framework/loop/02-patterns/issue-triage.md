# 🗂️ Issue Triage Loop

**Goal**: Phân loại noisy issues thành actionable backlog — gợi ý, không tự sửa. Feeder cho Daily Triage.

## Scheduling

**Khuyên dùng**:
- `/loop 2h–1d` (Grok, Claude Code)
- GitHub Action cron nhiều lần/ngày cho repos nhiều issues

## Required Skills

- `loop-triage` — Đọc issues, classify severity/priority, detect duplicates/stale
- `issue-intake` — Handle issues quá mơ hồ: clarify hoặc escalate, không đoán mò

## State

`issue-triage-state.md`:

```markdown
# Issue Triage State

Last run: 2026-06-09 10:00 UTC

## New Issues (last 24h)
- #1310 — bug: auth timeout — [High, actionable] — suggested: reproduce + fix
- #1311 — "app slow" — [Ambiguous] — loop-intake: cần thông tin thêm, đã comment hỏi
- #1312 — duplicate of #1305 — [Dup] — suggested: close

## Needs Human
- #1298 — feature request lớn — cần product decision
```

## How the Loop Runs (Typical Cycle)

1. Đọc open issues mới/updated (last 24h).
2. Với mỗi issue:
   - **Classify**: bug / feature / question / duplicate / stale.
   - **Mơ hồ** (không đủ để verify "done"): loop-intake skill hỏi thêm hoặc escalate — **không đoán mò**.
   - **Actionable**: ghi suggested next action vào state.
3. Cập nhật `issue-triage-state.md` — chỉ gợi ý, không tự sửa (L1 propose-only).
4. High-priority issues trở thành nguồn cho Daily Triage.

## Verification Strategy

- Level **L1 propose-only** — loop chỉ phân loại và gợi ý, không edit code.
- Triage skill **signal only** — không invent architectural work.
- Mỗi finding kèm evidence (link issue, lý do phân loại).

## Human Handoff Points

- Feature requests cần product decision
- Issues mơ hồ sau khi hỏi vẫn chưa rõ
- Issues high-priority + chưa có owner
- Bảo mật/security issues (escalate ngay)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Triage tạo noise | Tighten skill rules; "Noise / Ignore" section |
| Phân loại sai | Evidence cho mỗi finding; human review định kỳ |
| Đoán mò issue mơ hồ | loop-intake: hỏi thêm hoặc escalate, không guess |
| Overwhelm với nhiều issues | Ưu tiên theo severity; giới hạn xử lý mỗi run |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | Không có issue mới |
| Full triage | ~40k | Scan issues + classify |

**Cadence**: 2h–1d · **Tier**: low · **Suggested daily cap**: 100k tokens

```bash
npx @cobusgreyling/loop cost --pattern issue-triage --cadence 2h --level L1
```

## Success Metrics

- Time từ "issue mới" đến "được phân loại + suggested action"
- % phân loại chính xác (không phải re-triage)
- Giảm issue backlog "mồ côi" không ai biết

> **Pair tự nhiên**: Issue Triage (phân loại) → Daily Triage (ưu tiên) → action loops (thực thi). Low risk, excellent first pair với Daily Triage.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
