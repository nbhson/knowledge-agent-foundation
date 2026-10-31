# 🧹 CI Sweeper Loop

**Goal**: Phản ứng nhanh với CI failing trên main hoặc active branches — chẩn đoán, propose minimal fixes, và escalate khi loop không tự tin resolve.

> **Tóm gọn ý nghĩa:** CI = Continuous Integration, hệ thống tự chạy test mỗi khi có code mới (CI "đỏ" = test đang thất bại). Loop này như "thợ trực ca CI": thấy đỏ là chạy tới, chẩn đoán lỗi, đề xuất sửa nhỏ nhất — nhưng chỉ tự sửa những gì nó chắc chắn, còn lại thì kêu người.

## Scheduling

**Khuyên dùng**:
- `/loop 15m` trong active development (Grok, Claude Code) — `/loop 15m` = tự chạy lại mỗi 15 phút
- `/loop 5m` khi main đỏ và bạn đang ship (main = nhánh chính của repo)
- GitHub Action trên `workflow_run` failure (event-driven, tốt hơn polling — nghĩa là "CI hỏng thì được báo ngay" thay vì "đứng hỏi hoài có hỏng chưa")

Cadence chậm hơn qua đêm (30–60m) cũng ổn khi không ai theo dõi (cadence = nhịp chạy).

> **Tóm gọn 1 câu:** Chạy mỗi 5–15 phút khi đang ship, nới ra 30–60 phút ban đêm; hay nhất là dùng event CI hỏng để kích hoạt thay vì hỏi đều đều.

## Required Skills

Skill = file hướng dẫn gói sẵn một kỹ năng cho agent.

- `ci-triage` — Parse CI logs, xác định failing job/step, classify failure type (flake, regression, env, config). Flake = lỗi chập chờn hên xui; regression = lỗi do code mới gây ra; env/config = lỗi môi trường hay cấu hình, không phải do code.
- `minimal-fix` — Thay đổi nhỏ nhất giải quyết failure cụ thể
- `loop-guard` — Circuit breaker: log mỗi attempt vào `loop-ledger.json`; escalate thay vì loop trên cùng failure. Circuit breaker = "cầu dao": cùng một lỗi lặp quá N lần thì ngắt, đừng thử mãi.
- Project test/lint skill — Build + test commands cho stack của bạn (lint = công cụ quét lỗi phong cách code)

> **Tóm gọn 1 câu:** Cần 4 skill: đọc log CI và xếp loại lỗi, đề xuất sửa nhỏ nhất, cầu dao chống lặp vô hạn, và biết lệnh build/test của dự án.

## State

`ci-sweeper-state.md` hoặc section trong `STATE.md`:

```markdown
## CI Sweeper — Active Failures

Last run: 2026-06-09 14:30 UTC

### main @ abc1234
- Job: test-auth
- Failure: AssertionError trong test_refresh_token_expiry
- Attempts: 1/3
- Last action: Minimal fix proposed trong worktree fix/ci-auth-refresh
- Status: Waiting for verifier + human

### Resolved (last 7d)
- main @ def5678 — lint fix merged qua PR #1250
```

Đọc state này thế nào: `abc1234` là mã commit đang hỏng; `Attempts: 1/3` nghĩa là đã thử sửa 1 trên tối đa 3 lần; `Waiting for verifier + human` nghĩa là bản sửa đang chờ agent kiểm tra và người duyệt. Section "Resolved" ghi các lỗi đã xử lý trong 7 ngày gần nhất — nó là biên bản để tránh xử lý trùng.

Track: commit SHA, failing job, attempt count, worktree/PR link, outcome.

> **Tóm gọn 1 câu:** State ghi mỗi lỗi đang hỏng: ở commit nào, đã thử mấy lần, bản sửa nằm đâu — để lần chạy sau tiếp đúng chỗ, không làm lại từ đầu.

## How the Loop Runs (Typical Cycle)

1. Discover CI failures trên watched branches (main, release/*, active PRs).
2. Với mỗi failure mới:
   - **Classify**: flake vs real regression vs infra — xếp loại trước, vì cách xử lý mỗi loại khác nhau.
   - **Nếu flake** (đã thấy trước, intermittent): thêm vào Watch, **không auto-fix** (intermittent = thi thoảng hỏng thi thoảng không).
   - **Nếu actionable**: mở worktree → implementer draft fix (worktree = bản sao working directory riêng để sửa không đụng nhánh chính).
3. Verifier sub-agent kiểm tra: fix giải quyết failure, không có thay đổi không liên quan, tests pass locally.
4. Mở PR hoặc comment trên PR hiện có với proposed fix (PR = pull request, đề nghị gộp code).
5. Trước mỗi retry, `loop-guard` chạy circuit breaker. Nếu cùng failure tái diễn N lần hoặc attempts > max (vd 3): **trip → escalate** với pruned context summary (escalate = chuyển cho người; pruned = đã cắt bớt cho gọn).
6. Prune resolved failures khỏi active list (prune = dọn bỏ khỏi danh sách).

> **Tóm gọn 1 câu:** Vòng chạy là: phát hiện lỗi → xếp loại → chỉ tự sửa lỗi thật (không đụng flake) → agent khác kiểm → đề xuất PR → thử quá 3 lần thì kêu người.

## Verification Strategy

- Verifier **bắt buộc** chạy tests trong worktree trước khi approve.
- Implementer không được merge — chỉ propose (merge = gộp code vào nhánh chính).
- **Flake detection**: nếu cùng test failed rồi pass khi retry mà không có code change → không auto-fix. Đây là dấu hiệu lỗi chập chờn, sửa code là sai hướng.

> **Tóm gọn 1 câu:** Ai viết sửa không được tự gộp; agent kiểm tra phải chạy test thật trong worktree, và lỗi hên xui thì không sửa code.

## Human Handoff Points

Những tình huống loop phải dừng và bàn giao cho người:

- Infrastructure failures (runner OOM, registry down, secrets missing) — OOM = hết bộ nhớ; registry = kho lưu trữ package; secrets = biến môi trường chứa mật khẩu
- Failures chạm > 5 files hoặc core architecture
- Security-sensitive test failures
- Max attempts exceeded trên cùng failure
- Intermittent flakes cần quarantine, không phải code changes (quarantine = cách ly test đó ra khỏi bộ chạy chính)

> **Tóm gọn 1 câu:** Phần máy móc tự lo được có giới hạn: lỗi hạ tầng, đụng nhiều file/hạ tầng lõi, bảo mật, thử quá số lần — mọi chuyện giao người.

## Failure Modes & Mitigations

**Cách đọc bảng này:** cột "Failure" là cách loop hay hỏng; cột "Mitigation" là màng lưới phòng chống. Ví dụ, dòng 1: loop hay "đỡ đầu gối đau chân" — sửa cho CI xanh chứ không sửa gốc bệnh; màng lưới là bắt verifier phải kiểm tra nguyên nhân gốc.

| Failure | Mitigation |
|---------|------------|
| Fix-the-symptom loops | Verifier kiểm tra root cause, không chỉ CI xanh |
| Fighting flakes với retries | Classify flakes; quarantine hoặc skip với ticket |
| Token burn trên red main | Pause loop sau N failures; batch fixes |
| Wrong branch targeted | Explicit branch allowlist trong skill (allowlist = danh sách các nhánh được phép đụng tới) |

> **Tóm gọn 1 câu:** Bốn kiểu hỏng kinh điển: sửa triệu chứng, vật lộn với flake, đốt token vô ích, sửa nhầm nhánh — mỗi cái có một màng lưới riêng.

## Cost Profile

**Cách đọc bảng này:** mỗi dòng là một tình huống và giá token của nó. Ví dụ, khi CI xanh (no-op) chỉ tốn ~5k token, nhưng một lần "tìm ra và sửa được lỗi" (fix attempt) tốn tới ~200k — vì phải dựng worktree + agent viết + agent kiểm.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (CI green) | ~5k | **Required** — không chạy full sweeper khi xanh |
| Triage / classify | ~50k | Log parse + failure classification |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: very-high · **Suggested daily cap**: 1M tokens · **Early exit required** (early exit = thoát sớm ngay khi thấy không có việc)

> 📄 **Code ví dụ:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> ⚠️ Ở cadence 15m mà không early-exit, worst-case spend vượt 5M tokens/ngày. Không bao giờ chạy full action paths trên mỗi tick.

> **Tóm gọn 1 câu:** Đây là pattern đắt nhất trong 7 pattern — chỉ an toàn khi có early exit: CI xanh thì thoát ngay sau vài nghìn token.

## Success Metrics

- Mean time đến first proposed fix sau khi CI đỏ
- % failures resolved không cần human intervention (trivial cases only)
- Repeat failure rate (cùng job failing lại trong 48h)

> **Best entry loop** cho teams mới học loop engineering — high frequency, bounded scope, clear verification.

> **Tóm gọn 1 câu:** Đo bằng 3 con số: bao lâu thì có bản sửa đầu tiên, bao nhiêu % lỗi tự xử được, và bao nhiêu % lỗi tái diễn trong 48 giờ.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
