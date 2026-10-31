class Blackboard:
    def __init__(self):
        self.store: dict[str, tuple[int, str]] = {}  # key -> (version, value)
        self.owners: dict[str, str] = {}             # file/section -> agent_id
    def claim(self, resource: str, agent_id: str) -> bool:
        if resource in self.owners:
            return False
        self.owners[resource] = agent_id
        return True
    def write(self, key: str, value: str, expected_version: int, agent_id: str) -> bool:
        ver, _ = self.store.get(key, (0, ""))
        ns_ok = key.startswith(f"{agent_id}/") or key.startswith("shared/")
        if not ns_ok or ver != expected_version:
            return False  # version cũ → đọc lại + merge, không ghi đè mù
        self.store[key] = (ver + 1, value)
        return True
