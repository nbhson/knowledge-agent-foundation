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
