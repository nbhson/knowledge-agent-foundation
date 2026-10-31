import json
from pathlib import Path
from datetime import datetime

class ProgressStore:
    """Simple file-based progress tracking for long-running agents."""

    def __init__(self, progress_file: str = "claude-progress.json"):
        self.progress_file = Path(progress_file)
        self._init_file()

    def _init_file(self):
        if not self.progress_file.exists():
            self.progress_file.write_text(json.dumps({
                "created_at": datetime.now().isoformat(),
                "features": []
            }, ensure_ascii=False, indent=2), encoding="utf-8")

    def read(self) -> dict:
        return json.loads(self.progress_file.read_text(encoding="utf-8"))

    def write(self, data: dict):
        self.progress_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add_feature(self, name: str, description: str = ""):
        data = self.read()
        data["features"].append({
            "name": name,
            "description": description,
            "status": "pending",
            "passes": False,
            "added_at": datetime.now().isoformat(),
            "completed_at": None
        })
        self.write(data)

    def mark_feature(self, name: str, passes: bool):
        data = self.read()
        for feat in data["features"]:
            if feat["name"] == name:
                feat["passes"] = passes
                feat["status"] = "passed" if passes else "failed"
                feat["completed_at"] = datetime.now().isoformat()
        self.write(data)

    def get_next_feature(self) -> dict | None:
        data = self.read()
        for feat in data["features"]:
            if not feat["passes"]:
                return feat
        return None

# Usage
store = ProgressStore("project/claude-progress.json")
store.add_feature("auth", "Implement JWT authentication")
store.add_feature("api", "Create REST endpoints")
next_f = store.get_next_feature()
print(f"Next: {next_f['name'] if next_f else 'All done'}")
store.mark_feature("auth", passes=True)
