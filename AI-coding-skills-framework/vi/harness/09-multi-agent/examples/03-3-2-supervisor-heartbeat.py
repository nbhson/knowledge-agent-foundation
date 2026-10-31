import time, dataclasses

@dataclasses.dataclass
class Lease:
    lease_id: int
    deadline_ms: int = 300_000
    max_attempts: int = 3
    fencing_token: int = 0
    last_heartbeat: float = dataclasses.field(default_factory=time.time)
    last_progress: float = dataclasses.field(default_factory=time.time)

    def state(self) -> str:
        now = time.time()
        if (now - self.last_heartbeat) * 1000 > 15_000:
            return "DEAD"
        if self._expired():
            return "TIMED_OUT"
        if now - self.last_progress > 60:
            return "SUSPECT"
        return "RUNNING"

    def _expired(self) -> bool:
        return False  # supervisor so với wall-clock deadlineMs

    def requeue(self) -> "Lease":
        return Lease(self.lease_id, self.deadline_ms, self.max_attempts,
                     fencing_token=self.fencing_token + 1)

def accept_result(token: int, current: int, attempt: int) -> bool:
    if attempt > 3:
        return False  # escalate / fail closed
    return token == current  # token cũ → loại (fencing)
