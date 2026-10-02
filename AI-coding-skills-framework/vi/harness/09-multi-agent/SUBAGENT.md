# Sub-Agent — Spec vòng đời, spawn, quyền và ngân sách

> Companion của `README.md` (đặc biệt §16 Chịu lỗi/Messaging/Isolation).
> Tổng hợp các quy ước sub-agent đang rải rác ở `loop/01-concepts` (§2.5 Maker/Checker),
> `loop/02-patterns/*` (verifier/reviewer), `loop/04-operating` (cost guard),
> `loop/06-anti-patterns` và ví dụ Claude Code ở `README.md §16.5`.

## 1. Định nghĩa

* **Agent**: thực thể chạy full vòng harness (01→11), sở hữu task và memory.
* **Sub-agent**: agent con được agent cha (hoặc orchestrator) spawn cho **một task hẹp**,
  chạy cùng harness nhưng với **context cắt gọn + tool thu hẹp + budget riêng + lease**.
* **Loop**: vòng lặp định kỳ (cron) có thể spawn sub-agents mỗi run (`loop/05-multi-loop`).

Quy tắc phân biệt: nếu không có lease + deadline + budget riêng + tool allow-list riêng,
đó không phải sub-agent mà chỉ là một function call.

## 2. Taxonomy vai trò

| Vai trò | Việc | Không được làm |
|---|---|---|
| `implementer` / `maker` | Viết code trong worktree được giao | Tự merge, tự verify cuối |
| `verifier` / `checker` | Chạy test, gates, chấm rubric (mặc định stance REJECT) | Sửa code trực tiếp (chỉ comment) |
| `reviewer` | Review diff, severity Blocker/Major/Minor | Chạy shell, ghi file ngoài comment |
| `researcher` / `triage` | Đọc code/docs, trả về facts + citations `file:line` | Đổi behavior, ghi memory dài hạn |

Anti-pattern cấm (`loop/06-anti-patterns`): cùng một agent vừa implement vừa verify
→ confirmation bias, test yếu bị rubber-stamp.

## 3. Vòng đời

```text
spawn (kèm spec §4) → heartbeat 5s → progress stream
  → done (trả artifact + transcript gọn)
  → fault: DEAD (mất heartbeat >15s) / TIMED_OUT (quá deadline) / SUSPECT (sống nhưng không tiến triển >60s)
  → requeue (fencing token++, attempt++, đính kèm transcript cũ) → quá 3 attempts → escalate human / fail closed
```

* Mỗi task có `lease_id + deadlineMs + max_attempts` (mặc định deadline 300s, max 3).
* Supervisor phi trạng thái, backed by queue (Redis/BullMQ); worker phải idempotent
  để requeue retry an toàn. Quorum judges/voters: 2f+1 chịu f lỗi, cần majority (vd 2/3).
* Chi tiết implementation: `README.md §16.1–16.2` (code mẫu heartbeat + reassignment).

## 4. Spawn API (contract tối thiểu)

```typescript
interface SubAgentSpec {
  role: "implementer" | "verifier" | "reviewer" | "researcher";
  taskId: string;            // link tới TaskNode ở 08-task
  goal: string;              // hẹp, một việc, có definition of done
  context: {                 // KHÔNG dump toàn bộ context cha
    files: string[];         // allow-list đường dẫn
    artifactRefs: { path: string; hash: string }[]; // payload lớn → ref, không inline
    parentSummary: string;   // transcript cha đã rút gọn, không raw log
  };
  tools: string[];           // allow-list thu hẹp từ ma trận role ở 12-sandbox §6
  worktree?: string;         // BẮT BUỘC với code-editing sub-agents (isolation)
  budget: { maxTokens: number; maxSteps: number; timeoutMs: number };
  lease: { leaseId: number; deadlineMs: number; maxAttempts: number };
  secrets?: { scope: string; ttlMinutes: number }; // 5–15p, env injection, redact trước khi log
}
```

Quy tắc spawn (`loop/04-operating`): triage rẻ trước, chỉ spawn khi state báo actionable;
watchlist rỗng → exit <5k tokens, không spawn. **Tối đa 3 sub-agents/run** mặc định.

## 5. Context và memory

* **Riêng tư theo mặc định:** mỗi sub-agent có scratchpad riêng; chỉ publish diff/fact
  lên blackboard chung qua `blackboard.write(key, value, expectedVersion)` (CAS, đọc lại + merge
  khi lệch version, không ghi đè mù).
* **Single-writer:** orchestrator gán quyền sở hữu file/section (vd chỉ `coder` ghi `auth.ts`).
* **Namespace:** key theo `agent_id/task_id/*`; đọc chéo qua projection trong allow-list,
  không rò prompt/secret thô (`README.md §16.3`).

## 6. Cách ly và secret

* Cơ chế tier/controls/runner thuộc `12-sandbox-execution` §2–§6; riêng multi/sub-agent
  bổ sung: **tool tối thiểu theo role** (reviewer chỉ FS đọc, không shell; coder shell
  sandbox không net), tra cứu cùng ma trận role để solo và swarm phân giải ra cùng policy
  (lệch là bug leo thang đặc quyền).
* Secret là **lease theo từng agent** (token ngắn hạn theo scope), supervisor redact
  `sk-*, ghp_*, AWS_*` khỏi log/transcript; secret của agent này không bao giờ xuất hiện
  trong context agent khác (`README.md §16.4`).
* Egress chặn mặc định, allow-list domain từng agent; mọi I/O tool audit kèm
  `agent_id + lease_id`.
* Code-editing sub-agents: `isolation: worktree` + lock/queue trong state
  (`"PR #1234 — worktree in progress"`) để tránh hai sub-agents sửa cùng files.

## 7. Gộp kết quả

* Maker/checker: implementer xong → verifier độc lập chạy test/gates; verdict mặc định REJECT
  cho tới khi bằng chứng đủ (build OK, test OK, AC trace).
* Quorum: reviewer vote 2-of-3; một voter crash không chặn merge.
* Payload: header 64KB + body 512KB; lớn hơn → artifact ref. Message có `msg_id`
  (dedupe), FIFO theo từng task (từ chối `seq` sai thứ tự), request/reply timeout 30s.

## 8. Checklist khi dùng

[ ] Spec đủ §4 (role hẹp, context cắt gọn, tool allow-list, worktree nếu sửa code,
budget/timeout/lease) [ ] heartbeat + deadline + detector treo [ ] fencing token khi requeue
[ ] max 3 attempts + đường escalate [ ] CAS + single-writer + namespace [ ] secret lease ngắn +
redaction + không leak chéo [ ] max 3 spawns/run + kill switch chi phí [ ] verifier độc lập,
không tự verify.
