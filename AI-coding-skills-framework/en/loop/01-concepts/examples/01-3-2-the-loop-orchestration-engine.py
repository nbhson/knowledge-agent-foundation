from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time


@dataclass
class RunOutcome:
    """The outcome of one loop cycle."""
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
    The Loop Orchestration Engine — orchestrates the entire loop.

    Anatomy of a Loop:
      Schedule → Triage → State → Worktree → Implementer → Verifier → Gate
    """

    def __init__(self, pattern: str = "daily-triage"):
        self.pattern = pattern
        self.state: Dict[str, Any] = {}
        self.run_log: List[RunOutcome] = []
        self._attempt_count = 0
        self._max_attempts = 3  # Hard cap → escalate, no infinite loops

    def read_state(self, path: str) -> Dict:
        """Read durable state at the start of every run."""
        # In production: read STATE.md / LOOP-STATE.json
        self.state = {"last_run": None, "high_priority": [], "watch_list": []}
        return self.state

    def triage(self) -> List[str]:
        """
        Triage skill — discovers the work to do.
        Output must be STRUCTURED (not narrative):
        - High Priority items (loop is handling / waiting on human)
        - Watch List (being monitored)
        - Recent Noise (ignored this time)
        """
        # In production: call the $loop-triage skill → parse CI, issues, commits, chat
        findings = []
        if not self.state.get("high_priority"):
            # Early exit when there is nothing to do
            self._log(RunOutcome(
                run_id=self._new_run_id(), pattern=self.pattern,
                duration_s=0.1, items_found=0, actions_taken=0,
                escalations=0, tokens_estimate=5_000, outcome="idle",
            ))
        return findings

    def run_worktree(self, task: str, implementer: Callable, verifier: Callable) -> Dict:
        """
        Maker/Checker split in an isolated worktree.

        Rules:
        - The implementer must NOT self-grade "done".
        - The verifier must run tests in the worktree before approving.
        - If the verifier REJECTS → clean up the worktree, record the attempt, escalate after max.
        """
        self._attempt_count += 1

        # In production: `loop-worktree create --run-id <id> --pattern <p>`
        worktree_path = f".worktrees/fix-{self._attempt_count}"

        # The implementer produces the patch inside the worktree
        patch = implementer(task, worktree_path)

        # Independent verifier — default stance is REJECT
        verdict = verifier(patch)

        if verdict.get("pass"):
            return {"verdict": "PASS", "patch": patch, "attempts": self._attempt_count}

        # Verifier REJECTS → no merge, no infinite retries
        if self._attempt_count >= self._max_attempts:
            self.escalate_to_human(patch, verdict.get("reason"))
            return {"verdict": "ESCALATED", "attempts": self._attempt_count}

        return {"verdict": "RETRY", "attempts": self._attempt_count}

    def escalate_to_human(self, patch: Any, reason: str):
        """Escalate with FULL context — don't make the human re-hunt for it."""
        # In production: write to STATE.md under "High Priority (waiting on human)"
        # + a connector ping (Slack, Linear comment) at max attempts
        self.state["high_priority"].append({
            "item": str(patch)[:100], "reason": reason,
            "attempts": self._attempt_count,
        })

    def update_state(self, path: str):
        """Write outcome + timestamp + prune resolved items at the end of each run."""
        # Prune merged/closed items — prevents State Rot
        self.state["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
        # In production: write STATE.md

    def _log(self, outcome: RunOutcome):
        """Append-only run log — for debugging "why did it do that on Tuesday?"."""
        self.run_log.append(outcome)

    def _new_run_id(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")

    def run_cycle(self, path: str = "STATE.md") -> Dict:
        """One complete loop cycle."""
        self.read_state(path)
        findings = self.triage()
        # ... implementer/verifier for each actionable item ...
        self.update_state(path)
        return {"pattern": self.pattern, "state": self.state, "log": self.run_log}
