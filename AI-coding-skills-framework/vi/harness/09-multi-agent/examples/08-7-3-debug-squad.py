class DebugSquad:
    """
    Multi-agent debugging:
    1. Debugger reproduces and investigates
    2. Coder implements fix
    3. Tester verifies fix + regression tests
    4. Reviewer ensures fix quality
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.SEQUENTIAL
        )
        
        self.orchestrator.register_agent(
            "debugger", AgentRole.DEBUGGER
        )
        self.orchestrator.register_agent(
            "coder", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "tester", AgentRole.TESTER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
    
    def debug_and_fix(self, error_report: str) -> Dict:
        """Debug và fix issue"""
        tasks = [
            {
                "id": "investigate",
                "type": "debug",
                "input": {"error": error_report},
                "depends_on": [],
            },
            {
                "id": "fix",
                "type": "code",
                "input": {"action": "implement_fix"},
                "depends_on": ["investigate"],
            },
            {
                "id": "test-fix",
                "type": "test",
                "input": {"action": "regression_test"},
                "depends_on": ["fix"],
            },
            {
                "id": "review-fix",
                "type": "review",
                "input": {"action": "review_fix"},
                "depends_on": ["test-fix"],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
