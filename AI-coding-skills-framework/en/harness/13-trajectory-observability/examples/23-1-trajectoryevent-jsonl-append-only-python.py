from dataclasses import dataclass, field, asdict
from collections import defaultdict
from pathlib import Path
import json, time

@dataclass
class TrajectoryEvent:
    session_id: str
    kind: str                      # prompt | tool_call | tool_result | eval | ...
    payload: dict                  # đã redact; ≤64KB — quá lớn thì thay bằng {"ref": ...}
    id: str = ""                   # ULID — sắp xếp được theo lexicographic (§1.1)
    tokens_in: int = 0
    tokens_out: int = 0
    latency_ms: int = 0
    ts: int = field(default_factory=lambda: int(time.time() * 1000))

class TrajectoryStore:
    """JSONL append-only, một file / session. Dòng đã ghi không bao giờ sửa."""
    def __init__(self, root: str):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)

    def append(self, e: TrajectoryEvent) -> None:
        if not e.id:
            e.id = f"evt_{time.time_ns():024d}"          # thay bằng ULID ở production
        with (self.root / f"{e.session_id}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(e), ensure_ascii=False) + "\n")

    def tail(self, session_id: str, n: int = 20) -> list[TrajectoryEvent]:
        p = self.root / f"{session_id}.jsonl"
        lines = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
        return [TrajectoryEvent(**json.loads(l)) for l in lines[-n:]]
