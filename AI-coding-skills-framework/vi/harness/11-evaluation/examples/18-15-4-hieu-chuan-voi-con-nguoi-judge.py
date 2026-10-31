from dataclasses import dataclass

@dataclass
class Trajectory:
    passed: bool; steps: int; ref_steps_p50: int
    useful_calls: int; total_calls: int; recovered: int; error_episodes: int

def trajectory_score(t: Trajectory) -> dict:
    efficiency = min(1.0, t.ref_steps_p50 / max(t.steps, 1))
    precision = t.useful_calls / max(t.total_calls, 1)
    recovery = t.recovered / max(t.error_episodes, 1) if t.error_episodes else 1.0
    score = 0.5 * float(t.passed) + 0.2 * efficiency + 0.15 * precision + 0.15 * recovery
    return {"score": round(score, 3), "efficiency": round(efficiency, 3),
            "precision": round(precision, 3), "recovery": round(recovery, 3)}

def cost_per_pass_task(total_cost_usd: float, passed: int) -> float:
    return total_cost_usd / max(passed, 1)

print(trajectory_score(Trajectory(True, 42, 12, 8, 30, 1, 3)))   # pass nhưng lãng phí
print(trajectory_score(Trajectory(True, 14, 12, 10, 14, 2, 2)))   # run lành mạnh
print(f"$/pass-task: ${cost_per_pass_task(46.0, 710):.4f}")
