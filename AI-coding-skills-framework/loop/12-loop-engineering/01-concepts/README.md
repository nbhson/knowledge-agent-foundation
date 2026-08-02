# 🔬 01. Khái Niệm Cốt Lõi — Loop Engineering

> Phần này giải thích **Loop Engineering là gì**, **5 building blocks + memory** cấu thành mọi loop, **anatomy of a loop**, **mức tự chủ L1–L3**, và **taxonomy các vòng lặp lồng nhau**. Đọc [README.md](../README.md) trước để có bối cảnh tổng quan.

---

## 1. Loop Engineering Là Gì?

### 1.1 Từ Prompt Đến Loop

Cách sử dụng AI coding agent điển hình ngày nay là *ad-hoc prompting*: bạn mở agent, gõ lệnh, chờ kết quả. Mỗi lần bắt đầu từ đầu, không có trạng thái, không có lịch sử, không có kiểm chứng có hệ thống.

Loop Engineering đảo ngược điều đó:

```
AD-HOC PROMPTING:
  Bạn ──prompt──► Agent ──kết quả──► Bạn (đọc, đánh giá)
  Bạn ──prompt──► Agent ──kết quả──► Bạn (đọc, đánh giá)
  ... lặp lại vô tận, không hệ thống

LOOP ENGINEERING:
  Scheduler ──fire──► Triage Skill ──đọc/write──► STATE / Memory
       │                                              │
       ▼                                              ▼
  Isolated Worktree ◄──── Implementer ──patch──► Verifier
       │                                              │
       ▼                                              ▼
  MCP / Git / Tickets ◄──── Human Gate? ──► Commit / PR / Escalate
```

**Vai trò của bạn thay đổi**: từ *người gõ prompt* thành *kỹ sư thiết kế vòng lặp*. Bạn viết skill (kiến thức), định nghĩa state schema, chọn cadence, và giữ lại quyền quyết định ở các **human gates**.

### 1.2 Harness vs Loop

Một khái niệm thường bị nhầm lẫn. Harness và Loop không giống nhau:

```
Harness = single session setup
  → tools, context, permissions, rules mà MỘT agent có trong MỘT phiên

Loop    = harness + schedule + state + verification chain
  → hệ thống điều phối NHIỀU harness runs theo thời gian
```

Module VII-XI trong framework này xây dựng các thành phần của harness. Module XII này (loop) **điều phối chúng theo thời gian**: lịch chạy, trạng thái bền vững, và chuỗi kiểm chứng.

### 1.3 Loop Là Một Recursive Goal

Một loop là một **mục tiêu đệ quy**: định nghĩa mục đích, để agent tự lặp (với sub-agents và memory ngoài) cho đến khi **hoàn thành hoặc loop leo thang lên con người**.

```
Loop = Define purpose → Iterate → Done / Escalate to human
```

---

## 2. Năm Building Blocks + Memory

Đây là các **nguyên khối (primitives)** cấu thành mọi loop. Khả năng thực sự quan trọng hơn tên sản phẩm — mỗi nguyên khối đều có mapping ở các tool khác nhau (Grok, Claude Code, Codex, Cursor, Opencode, ...).

| Primitive | Job trong Loop |
|-----------|----------------|
| **Automations / Scheduling** | Phát hiện + triage theo nhịp |
| **Worktrees** | Thực thi song song an toàn |
| **Skills** | Kiến thức dự án bền vững |
| **Plugins & Connectors** | Vươn vào tools thật (MCP) |
| **Sub-agents** | Tách maker / checker |
| **+ Memory / State** | Xương sống bền vững ngoài mọi hội thoại |

```
┌───────────────────────────────────────────────────────────────┐
│               NĂM BUILDING BLOCKS + MEMORY                     │
│                                                               │
│  ┌─────────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ Automations │ │ Worktrees │ │  Skills  │ │Plugins & Conn│ │
│  │ / Scheduling│ │ (cô lập)  │ │(knowledge)│ │  (MCP)       │ │
│  └──────┬──────┘ └─────┬─────┘ └────┬─────┘ └──────┬───────┘ │
│         └───────────────┼────────────┼──────────────┘        │
│                         ▼            ▼                        │
│              ┌────────────────────────────────────┐          │
│              │   SUB-AGENTS (Maker / Checker)      │          │
│              └────────────────────────────────────┘          │
│                         │                                     │
│                         ▼                                     │
│              ┌────────────────────────────────────┐          │
│              │   MEMORY / STATE (bền vững)         │          │
│              └────────────────────────────────────┘          │
└───────────────────────────────────────────────────────────────┘
```

### 2.1 Automations / Scheduling

Nhịp đập của loop. **Không có scheduling, bạn chỉ có một agent run một lần.**

Các hiện thực phổ biến:
- `/loop [interval] <prompt>` (Grok, Claude Code)
- Scheduled tasks / cron trong Claude Code
- GitHub Actions + repository dispatch
- `/goal` — chạy cho đến khi một điều kiện kiểm chứng được thoả
- Custom harness schedulers

Các thuộc tính quan trọng: **interval, fire-immediately, recurring vs one-shot, durable (sống sót restart).**

### 2.2 Worktrees

Song song mà không hỗn loạn.

Khi hai agents cùng sửa một file cùng lúc, bạn có merge hell. Git worktrees (hoặc isolated checkout tương đương) cho mỗi agent một **working directory riêng** — chia sẻ lịch sử nhưng không chia sẻ working tree.

```
Agent A (worktree 1)  ──►  sửa fix/ci-auth-refresh
Agent B (worktree 2)  ──►  sửa fix/issue-1241
         └────── cùng chia sẻ history ──────┘
```

**Cleanup rất quan trọng** — loop phải xoá worktree khi task xong hoặc bàn giao. Tool `loop-worktree` làm điều này thành cơ chế: một worktree cho mỗi lần thử, theo dõi trong manifest, dọn khi reject hoặc escalate.

### 2.3 Skills

Bộ nhớ bền vững của **ý định** (intent).

Một skill (thường là `SKILL.md` + scripts/references) mã hoá:
- Quy ước dự án
- "Chúng tôi không làm theo cách này vì sự cố X"
- Lệnh build/test/lint
- Tiêu chuẩn review
- Kiến thức domain

**Không có skills**, loop tự suy ra mọi thứ từ đầu ở mỗi lần chạy → **intent debt**.

```
Skills = "Conventions viết một lần, đọc mọi lần chạy"
```

### 2.4 Plugins & Connectors (MCP)

Một loop chỉ đọc được filesystem là rất giới hạn.

Connectors cho phép loop:
- Đọc/cập nhật tickets Linear / Jira
- Đăng lên Slack / Discord
- Query databases / internal APIs
- Tạo branch và PR trên GitHub
- Trigger deploys / runbooks

**MCP (Model Context Protocol)** đã trở thành substrate chung — connectors viết cho tool này thường chạy được ở tool khác.

### 2.5 Sub-agents — Maker / Checker Split

**Pattern cấu trúc quan trọng nhất** cho loops đáng tin cậy.

Agent viết code là một người chấm điểm tệ cho chính tác phẩm của mình. Một agent thứ hai (đôi khi model mạnh hơn, luôn khác instructions) thực hiện việc **kiểm chứng**.

```
Implementer (Maker) ──patch──► Verifier (Checker) ──approve/reject──►
   Không bao giờ tự chấm         "Tìm lý do để REJECT"              Commit / PR
   điểm chính mình
```

Các split phổ biến:
- Explorer → Implementer → Verifier
- Implementer → Security reviewer
- Implementer → Test writer + runner

Trong loops **không người giám sát** (unattended), verifier chính là thứ cho phép bạn rời đi mà vẫn có chút tin tưởng.

### 2.6 Memory / State

Mô hình không có trí nhớ dài hạn xuyên suốt các turn hay sessions riêng biệt.

Loop **bắt buộc** phải đọc và ghi vào thứ gì đó bền vững:
- `STATE.md` hoặc `LOOP-STATE.json` trong repo
- Một section riêng của Linear board / GitHub Project
- Một row database nhỏ

State tốt trả lời được:
- Chúng ta đang làm gì?
- Lần trước thử gì, kết quả ra sao?
- Cái gì đang chờ con người?

> **State file thường là artifact quan trọng nhất mà loop tạo ra.**

---

## 3. Anatomy of a Loop

Một loop cycle hoàn chỉnh có dạng:

```
┌──────────────────────────────────────────────────────────────────────┐
│ Schedule / Automation ──► Triage Skill                               │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                   Read + Write STATE / Memory                  │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Isolated Worktree                             │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Implementer Sub-agent                         │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Verifier Sub-agent (tests + gates)            │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  MCP / Git / Tickets                           │
│     │                          │                                     │
│     │                          ▼                                     │
│     │                  Human Gate?                                   │
│     └── safe/allowlisted ──► Commit / PR / Action                    │
│     └── risky/ambiguous ────► Escalate to human (full context)       │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.1 Vòng Đời Một Run

Mỗi run được lên lịch đi qua các trạng thái sau, kết thúc bằng một log entry bền vững:

```
Scheduled → LoadingContext → RunningTriage → WorkingInWorktree → Verifying
     │              │              │
     │              ├──► BlockedBudget (budget exceeded)
     │              └──► RunningTriage
     │                              └──► IdleNoop (không có gì để làm)
     │
     Verifying → AwaitingHumanGate → Applied / Rejected
           │            └──► Failed
           │
           └──► (mọi trạng thái cuối) → Logged → [*]
```

**Điểm then chốt**: `IdleNoop` phải là một nhánh bình thường — loop nên **thoát gọn (< 5k tokens)** khi watchlist rỗng, không phải chạy full sub-agent chain.

### 3.2 Loop Orchestration Engine

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time


@dataclass
class RunOutcome:
    """Kết quả một vòng loop."""
    run_id: str
    pattern: str
    duration_s: float
    items_found: int
    actions_taken: int
    escalations: int
    tokens_estimate: int
    outcome: str  # success / idle / failed / budget_blocked


class LoopOrchestrator:
    """
    Loop Orchestration Engine — điều phối toàn bộ vòng lặp.

    Anatomy of a Loop:
      Schedule → Triage → State → Worktree → Implementer → Verifier → Gate
    """

    def __init__(self, pattern: str = "daily-triage"):
        self.pattern = pattern
        self.state: Dict[str, Any] = {}
        self.run_log: List[RunOutcome] = []
        self._attempt_count = 0
        self._max_attempts = 3  # Hard cap → escalate, không loop vô hạn

    def read_state(self, path: str) -> Dict:
        """Đọc state bền vững từ đầu mỗi run."""
        # In production: đọc STATE.md / LOOP-STATE.json
        self.state = {"last_run": None, "high_priority": [], "watch_list": []}
        return self.state

    def triage(self) -> List[str]:
        """
        Triage skill — phát hiện việc cần làm.
        Output phải CÓ CẤU TRÚC (không phải narrative):
        - High Priority items (loop đang xử lý / chờ human)
        - Watch List (đang theo dõi)
        - Recent Noise (bỏ qua lần này)
        """
        # In production: gọi $loop-triage skill → parse CI, issues, commits, chat
        findings = []
        if not self.state.get("high_priority"):
            # Early exit khi không có gì đáng làm
            self._log(RunOutcome(
                run_id=self._new_run_id(), pattern=self.pattern,
                duration_s=0.1, items_found=0, actions_taken=0,
                escalations=0, tokens_estimate=5_000, outcome="idle",
            ))
        return findings

    def run_worktree(self, task: str, implementer: Callable, verifier: Callable) -> Dict:
        """
        Maker/Checker split trong worktree cô lập.

        Rules:
        - Implementer KHÔNG được tự chấm "done".
        - Verifier phải chạy tests trong worktree trước khi approve.
        - Nếu verifier REJECT → dọn worktree, ghi attempt, escalate sau max.
        """
        self._attempt_count += 1

        # In production: `loop-worktree create --run-id <id> --pattern <p>`
        worktree_path = f".worktrees/fix-{self._attempt_count}"

        # Implementer tạo patch trong worktree
        patch = implementer(task, worktree_path)

        # Verifier độc lập — mặc định stance là REJECT
        verdict = verifier(patch)

        if verdict.get("pass"):
            return {"verdict": "PASS", "patch": patch, "attempts": self._attempt_count}

        # Verifier REJECT → không merge, không retry vô hạn
        if self._attempt_count >= self._max_attempts:
            self.escalate_to_human(patch, verdict.get("reason"))
            return {"verdict": "ESCALATED", "attempts": self._attempt_count}

        return {"verdict": "RETRY", "attempts": self._attempt_count}

    def escalate_to_human(self, patch: Any, reason: str):
        """Escalate với FULL context — không để human phải tìm lại."""
        # In production: ghi vào STATE.md "High Priority (waiting on human)"
        # + connector ping (Slack, Linear comment) khi max attempts
        self.state["high_priority"].append({
            "item": str(patch)[:100], "reason": reason,
            "attempts": self._attempt_count,
        })

    def update_state(self, path: str):
        """Ghi outcome + timestamp + prune resolved items cuối mỗi run."""
        # Prune merged/closed items — chống State Rot
        self.state["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # In production: write STATE.md

    def _log(self, outcome: RunOutcome):
        """Append-only run log — để debug "tại sao nó làm vậy hôm thứ Ba?"."""
        self.run_log.append(outcome)

    def _new_run_id(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def run_cycle(self, path: str = "STATE.md") -> Dict:
        """Một vòng lặp hoàn chỉnh."""
        self.read_state(path)
        findings = self.triage()
        # ... implementer/verifier cho từng actionable item ...
        self.update_state(path)
        return {"pattern": self.pattern, "state": self.state, "log": self.run_log}
```

</details>

---

## 4. Mức Tự Chủ L1 → L2 → L3

Không ai nên bật loop **unattended** từ ngày một. Ba mức tự chủ là một lộ trình có kiểm chứng:

```
L1 REPORT-ONLY ──► L2 ASSISTED ──► L3 UNATTENDED
  Triage → state     Small auto-fixes   Chạy không có bạn theo dõi
  Không auto-action  Với verifier       Cần denylist + budget + gates
  Tuần 1 đầu tiên    + worktree         + max attempts
```

| Level | Mô tả | Checklist |
|-------|-------|-----------|
| **L0 — Draft** | Chỉ có ý định được ghi chép | §1 (purpose & scope) |
| **L1 — Report** | Triage → state, không auto-action | §1–3, §5 |
| **L2 — Assisted** | Auto-fix nhỏ với verifier | §1–7 |
| **L3 — Unattended** | Chạy không cần bạn nhìn | Tất cả sections |

**Quy tắc vàng**: đừng bao giờ nhảy lên L3 cho một pattern mới trên production repo.

```
L1 ──► L2: audit score lên + human OK
L2 ──► L3: denylist + budget + gates đã chứng minh
L3 ──► L2: incident hoặc cost spike
L2 ──► L1: kill switch
```

---

## 5. Loop Taxonomy — Các Vòng Lặp Lồng Nhau

Ở mức thiết kế hệ thống, mỗi loop lớn chứa các vòng lặp nhỏ hơn. Hiểu taxonomy này giúp bạn biết **vòng lặp nào cần guardrail nào**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  OUTER LOOP (cross-task, ngày/tuần)                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LEARNING LOOP (per-task, giờ)                                 │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  EXECUTION LOOP (per-action, giây)                      │  │  │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │  │
│  │  │  │  INNER LOOP (per-step, ms)                        │  │  │  │
│  │  │  │  Think ──► Act ──► Observe ──► Reflect            │  │  │  │
│  │  │  │     ▲                              │              │  │  │  │
│  │  │  │     └──────────────────────────────┘              │  │  │  │
│  │  │  │                                                   │  │  │  │
│  │  │  │  Execute ──► Retry ──► Verify ──► Escalate        │  │  │  │
│  │  │  └───────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  Task 1 ──► Task 2 ──► Task 3 ──► ... ──► Optimize           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.1 Inner Loop

Vòng lặp nhanh nhất — xảy ra trong suy nghĩ của agent. Agent "nói chuyện với chính mình" trước khi hành động: Think → Act → Observe → Reflect.

### 5.2 Execution Loop

Xử lý lỗi trong quá trình thực thi — đảm bảo agent không bỏ cuộc quá sớm nhưng cũng **không retry vô hạn**. Các pattern chính: retry with backoff, circuit breaker, timeout. Guardrail then chốt: **hard cap số attempts → escalate**.

### 5.3 Validation Loop

Đảm bảo output của agent **thực sự hoạt động** trước khi được chấp nhận. Write → Test → Fix → Re-test. Trong loop engineering production, điều này nằm ở **verifier sub-agent** chạy tests trong worktree cô lập.

### 5.4 Feedback Loop

Xương sống của loop engineering — kết nối kết quả quá khứ với hành động tương lai. Collect metrics → Analyze → Optimize → Apply. Mỗi run nên ghi **post-run critique**: false positives, items lặp lại, một thay đổi để cải thiện lần sau.

### 5.5 Outer Loop

Chạy ở tần suất thấp (ngày/tuần), tập trung cải thiện **toàn bộ hệ thống**: prompt evolution, pattern learning, metric tracking. Đây là nơi bạn đo "loop có đang tốt lên không".

---

## 6. Concepts & Vocabulary

### 6.1 Intent Debt

Mỗi phiên, agent bắt đầu từ **trạng thái trắng**. Ý định bị thiếu được lấp bằng những suy đoán tự tin — và suy đoán sai. **Skills** là cách trả nợ ý định: quy ước, build steps, "chúng tôi không làm theo cách này" — viết một lần, đọc mọi lần chạy.

### 6.2 Comprehension Debt

Khoảng cách giữa những gì tồn tại trong repo và những gì bạn thực sự hiểu. Loops nhanh hơn ship nhiều code bạn không viết — **comprehension debt tăng trừ khi bạn đọc những gì loop tạo ra**.

> *"Velocity up, but no one can explain recent changes; review becomes rubber-stamp."*

### 6.3 Cognitive Surrender

Cái bẫy để loop chạy trong khi bạn **ngừng có ý kiến**. Thiết kế loop với judgment là liều thuốc; dùng loop để tránh suy nghĩ là chất xúc tác. Cùng một hành động, kết quả ngược nhau.

### 6.4 Orchestration Tax

Chi phí con người khi phối hợp parallel agents: review bandwidth, merge conflicts, context switching. **Worktrees** loại bỏ va chạm cơ học; bạn vẫn là trần nhà về số loop song song bạn hấp thụ được.

### 6.5 Code Agent Orchestra / Adversarial Review

Pattern cấu trúc: các agents khác vai trò (explore, implement, verify). **Implementer không bao giờ tự chấm bài chính mình** — bắt buộc cho loops unattended.

---

## 7. Tương Lai Loop Engineering

### Xu Hướng

```
┌─────────────────────────────────────────────────────────────┐
│                 LOOP ENGINEERING EVOLUTION                    │
│                                                              │
│  2024-2025: Manual prompting → first loops                  │
│       → Ad-hoc agents, no state, no verifiers                │
│                                                              │
│  2025-2026: Production loop frameworks                      │
│       → Patterns, starters, readiness scores                │
│       → Denylist, budget, human gates (loop-engineering)    │
│       → Cross-tool primitives (Grok, Claude, Codex, ...)    │
│                                                              │
│  2027: Self-verifying & self-tuning loops                   │
│       → Loops that adjust cadence by signal quality         │
│       → Cross-task learning at scale                        │
│       → Multi-agent loop coordination (fleet)               │
│                                                              │
│  2028: Autonomous improvement with human governance         │
│       → Loops that design new loops                         │
│       → Human-in-the-loop for strategic decisions only      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Research Directions

1. **Goal vs Loop** — loops phát hiện việc ongoing; goals hoàn thành bounded tasks (`/goal`). Ranh giới mờ dần.
2. **Multi-Agent Loop Coordination** — nhiều agents chia sẻ loop insights, cải thiện tập thể.
3. **Self-Tuning Parameters** — loops tự điều chỉnh cadence/budget theo signal quality.
4. **Loop Compression** — giảm số iterations cần thiết bằng predicted outcomes.
5. **Ethical Loop Constraints** — đảm bảo loops không tạo harmful feedback cycles.

---

*Tiếp theo: [02 — Bảy Production Patterns](../02-patterns/) → [03 — Safety & Loop Design Checklist](../03-safety/)*
