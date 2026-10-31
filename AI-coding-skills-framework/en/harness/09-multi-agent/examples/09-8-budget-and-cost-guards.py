class SpawnBudget:
    def __init__(self, run_cap: int = 20_000, max_spawns: int = 3):
        self.spent = 0
        self.spawns = 0
        self.run_cap, self.max_spawns = run_cap, max_spawns
    def request(self, tokens: int) -> bool:
        if self.spawns >= self.max_spawns or self.spent + tokens > self.run_cap:
            return False
        self.spawns += 1
        self.spent += tokens
        return True
