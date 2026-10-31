@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable  # Rollback function
    max_retries: int = 3

class SagaOrchestrator:
    """
    Saga Pattern — phân phối transaction qua nhiều services.
    
    Nếu step nào fail → compensating transactions chạy ngược
    để undo các step đã thành công trước đó.
    
    Flow:
    1. Step A (success) → Step B (success) → Step C (FAIL)
    2. Compensation: undo B → undo A
    """
    
    def __init__(self, name: str = "saga"):
        self.name = name
        self.steps: List[SagaStep] = []
        self.completed_steps: List[Dict] = []
        self.history: List[Dict] = []
    
    def add_step(self, name: str, action: Callable, compensation: Callable):
        self.steps.append(SagaStep(name=name, action=action, compensation=compensation))
        return self
    
    def execute(self, initial_data: Any = None) -> Dict:
        data = initial_data
        compensated = False
        
        for step in self.steps:
            try:
                result = step.action(data)
                self.completed_steps.append({
                    "name": step.name,
                    "result": result,
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                })
                data = result
            except Exception as e:
                self.history.append({
                    "failed_step": step.name,
                    "error": str(e),
                    "compensating": True,
                    "timestamp": datetime.now().isoformat(),
                })
                
                # Compensate in reverse order
                for completed in reversed(self.completed_steps):
                    try:
                        completed["compensation"]()
                        self.history.append({
                            "compensated": completed["name"],
                            "status": "success",
                            "timestamp": datetime.now().isoformat(),
                        })
                    except Exception as comp_e:
                        self.history.append({
                            "compensation_failed": completed["name"],
                            "error": str(comp_e),
                            "timestamp": datetime.now().isoformat(),
                        })
                
                compensated = True
                return {
                    "success": False,
                    "failed_step": step.name,
                    "error": str(e),
                    "compensated": True,
                    "compensation_history": [
                        h for h in self.history if "compensated" in h
                    ],
                }
        
        return {
            "success": True,
            "completed_steps": [s["name"] for s in self.completed_steps],
            "result": data,
        }
