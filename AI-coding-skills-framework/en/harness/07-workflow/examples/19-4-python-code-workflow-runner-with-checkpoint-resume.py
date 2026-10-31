import json, time, random
from pathlib import Path
from typing import Callable, Dict, List

class CheckpointRunner:
    """Workflow runner với checkpoint/resume — crash không phải chạy lại từ đầu."""

    def __init__(self, name: str, checkpoint_dir: str = "./checkpoints",
                 max_retries: int = 3):
        self.name = name
        self.max_retries = max_retries
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        return self.checkpoint_dir / f"{run_id}.json"

    def _load(self, run_id: str) -> Dict:
        """Load checkpoint nếu có — đây là chìa khóa của resume."""
        p = self._path(run_id)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return {"completed": [], "results": {}}

    def _save(self, run_id: str, state: Dict) -> None:
        self._path(run_id).write_text(
            json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def _run_step(self, step: Callable) -> object:
        """Chạy 1 step với retry + exponential backoff (max 3 lần)."""
        for attempt in range(1, self.max_retries + 1):
            try:
                return step()
            except Exception as e:
                if attempt == self.max_retries:
                    raise  # hết lượt — ném lên trên cho agent quyết định
                wait = 2 ** attempt + random.random()  # 2s, 4s, 8s + jitter
                print(f"    ⚠️ Lần {attempt}/{self.max_retries} fail: {e} — retry sau {wait:.1f}s")
                time.sleep(wait)

    def run(self, run_id: str, steps: List[Dict]) -> Dict:
        """steps: [{"name": ..., "func": Callable}] — chạy tuần tự, checkpoint mỗi step."""
        state = self._load(run_id)
        done, results = set(state["completed"]), state["results"]
        print(f"[{self.name}] run={run_id}: {len(done)}/{len(steps)} step đã xong trước đó")

        for i, step in enumerate(steps):
            name = step["name"]
            if name in done:
                print(f"  ↷ Bỏ qua '{name}' (đã xong — từ checkpoint)")
                continue
            print(f"  ▶ Chạy '{name}'...")
            results[name] = self._run_step(step["func"])
            done.add(name)
            self._save(run_id, {"completed": sorted(done), "results": results})  # checkpoint!

        print(f"[{self.name}] ✅ Hoàn tất run {run_id}")
        return results

# ---- Demo ----
if __name__ == "__main__":
    runner = CheckpointRunner("demo")
    # Giả sử lần trước crash ở bước 3 — chạy lại vẫn resume đúng chỗ
    out = runner.run("run-42", [
        {"name": "parse",     "func": lambda: "parsed_data"},
        {"name": "analyze",   "func": lambda: {"score": 42}},
        {"name": "build",     "func": lambda: "artifact.bin"},  # crash ở đây lần trước
        {"name": "test",      "func": lambda: "all_passed"},
    ])
    print("Kết quả:", out)
