# 🧹 CI Sweeper Loop

**Goal**: Phản ứng nhanh với CI failing trên main hoặc active branches — chẩn đoán, propose minimal fixes, và escalate khi loop không tự tin resolve.

## Scheduling

**Khuyên dùng**:
- `/loop 15m` trong active development (Grok, Claude Code)
- `/loop 5m` khi main đỏ và bạn đang ship
- GitHub Action trên `workflow_run` failure (event-driven, tốt hơn polling)

Cadence chậm hơn qua đêm (30–60m) cũng ổn khi không ai theo dõi.

## Required Skills

- `ci-triage` — Parse CI logs, xác định failing job/step, classify failure type (flake, regression, env, config)
- `minimal-fix` — Thay đổi nhỏ nhất giải quyết failure cụ thể
- `loop-guard` — Circuit breaker: log mỗi attempt vào `loop-ledger.json`; escalate thay vì loop trên cùng failure
- Project test/lint skill — Build + test commands cho stack của bạn

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

Track: commit SHA, failing job, attempt count, worktree/PR link, outcome.

## How the Loop Runs (Typical Cycle)

1. Discover CI failures trên watched branches (main, release/*, active PRs).
2. Với mỗi failure mới:
   - **Classify**: flake vs real regression vs infra.
   - **Nếu flake** (đã thấy trước, intermittent): thêm vào Watch, **không auto-fix**.
   - **Nếu actionable**: mở worktree → implementer draft fix.
3. Verifier sub-agent kiểm tra: fix giải quyết failure, không có thay đổi không liên quan, tests pass locally.
4. Mở PR hoặc comment trên PR hiện có với proposed fix.
5. Trước mỗi retry, `loop-guard` chạy circuit breaker. Nếu cùng failure tái diễn N lần hoặc attempts > max (vd 3): **trip → escalate** với pruned context summary.
6. Prune resolved failures khỏi active list.

## Verification Strategy

- Verifier **bắt buộc** chạy tests trong worktree trước khi approve.
- Implementer không được merge — chỉ propose.
- **Flake detection**: nếu cùng test failed rồi pass khi retry mà không có code change → không auto-fix.

## Human Handoff Points

- Infrastructure failures (runner OOM, registry down, secrets missing)
- Failures chạm > 5 files hoặc core architecture
- Security-sensitive test failures
- Max attempts exceeded trên cùng failure
- Intermittent flakes cần quarantine, không phải code changes

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Fix-the-symptom loops | Verifier kiểm tra root cause, không chỉ CI xanh |
| Fighting flakes với retries | Classify flakes; quarantine hoặc skip với ticket |
| Token burn trên red main | Pause loop sau N failures; batch fixes |
| Wrong branch targeted | Explicit branch allowlist trong skill |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op (CI green) | ~5k | **Required** — không chạy full sweeper khi xanh |
| Triage / classify | ~50k | Log parse + failure classification |
| Fix attempt (L2) | ~200k | Worktree + implementer + verifier |

**Cadence**: 5–15m · **Tier**: very-high · **Suggested daily cap**: 1M tokens · **Early exit required**

```bash
npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2
```

> ⚠️ Ở cadence 15m mà không early-exit, worst-case spend vượt 5M tokens/ngày. Không bao giờ chạy full action paths trên mỗi tick.

## Success Metrics

- Mean time đến first proposed fix sau khi CI đỏ
- % failures resolved không cần human intervention (trivial cases only)
- Repeat failure rate (cùng job failing lại trong 48h)

> **Best entry loop** cho teams mới học loop engineering — high frequency, bounded scope, clear verification.

---

*Trở về [02 — Bảy Production Patterns](../02-patterns/)*
