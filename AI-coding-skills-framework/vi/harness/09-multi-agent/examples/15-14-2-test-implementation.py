class MultiAgentTestSuite:
    """
    Test suite cho multi-agent systems.
    
    Categories:
    1. Unit tests cho individual agents
    2. Integration tests cho agent interactions
    3. Chaos tests cho failure scenarios
    4. Performance tests cho token/cost efficiency
    """
    
    def __init__(self):
        self.test_results: List[Dict] = []
    
    # === ROUTING TESTS ===
    
    def test_routing_accuracy(self, orchestrator: 'AgentOrchestrator',
                               test_cases: List[Dict]) -> Dict:
        """
        Test: Task types route to correct agents.
        
        test_cases: [{"task_type": str, "expected_role": AgentRole}]
        """
        correct = 0
        total = len(test_cases)
        
        for case in test_cases:
            task = {"id": "test", "type": case["task_type"]}
            agent_id = orchestrator._route_task(task)
            
            if agent_id:
                agent_role = orchestrator.agents[agent_id]["role"]
                if agent_role == case["expected_role"]:
                    correct += 1
                else:
                    self.test_results.append({
                        "test": "routing_accuracy",
                        "task_type": case["task_type"],
                        "expected": case["expected_role"].value,
                        "got": agent_role.value,
                        "status": "FAIL",
                    })
            else:
                self.test_results.append({
                    "test": "routing_accuracy",
                    "task_type": case["task_type"],
                    "expected": case["expected_role"].value,
                    "got": "no_agent",
                    "status": "FAIL",
                })
        
        return {
            "test": "routing_accuracy",
            "passed": correct,
            "total": total,
            "accuracy": correct / total if total else 0,
        }
    
    # === CHAOS TESTS ===
    
    def test_agent_failure_recovery(self, 
                                     orchestrator: 'AgentOrchestrator',
                                     failing_agent: str) -> Dict:
        """
        Test: System vẫn hoạt động khi 1 agent fail.
        """
        # Execute pipeline with failing agent
        tasks = [
            {"id": "task-1", "type": "code", "input": {}},
            {"id": "task-2", "type": "review", "input": {},
             "depends_on": ["task-1"]},
        ]
        
        # Simulate failure for specific agent
        original_status = orchestrator.agents.get(failing_agent, {}).get("status")
        if failing_agent in orchestrator.agents:
            orchestrator.agents[failing_agent]["status"] = "failed"
        
        result = orchestrator.execute_pipeline(tasks)
        
        # Restore
        if failing_agent in orchestrator.agents:
            orchestrator.agents[failing_agent]["status"] = original_status
        
        return {
            "test": "agent_failure_recovery",
            "failing_agent": failing_agent,
            "tasks_completed": result["tasks_completed"],
            "has_graceful_degradation": result["tasks_completed"] > 0,
            "status": "PASS" if result["tasks_completed"] > 0 else "FAIL",
        }
    
    def test_token_budget_enforcement(self, 
                                       orchestrator: 'AgentOrchestrator',
                                       budget: int = 10000) -> Dict:
        """
        Test: Token budget được enforce đúng.
        """
        orchestrator.token_budget = budget
        orchestrator.tokens_used = 0
        
        # Create tasks that would exceed budget
        tasks = [
            {"id": f"task-{i}", "type": "code", 
             "input": {}, "estimated_tokens": budget // 2}
            for i in range(5)
        ]
        
        result = orchestrator.execute_pipeline(tasks)
        
        budget_respected = result["tokens_used"] <= budget
        
        return {
            "test": "token_budget_enforcement",
            "budget": budget,
            "tokens_used": result["tokens_used"],
            "budget_respected": budget_respected,
            "status": "PASS" if budget_respected else "FAIL",
        }
    
    def test_conflict_resolution(self, 
                                  conflict_mgr: 'ConflictResolutionManager') -> Dict:
        """
        Test: Conflicts được resolve đúng.
        """
        # Test file locking
        acquired1 = conflict_mgr.acquire_file_lock("main.py", "agent-a")
        acquired2 = conflict_mgr.acquire_file_lock("main.py", "agent-b")
        
        # Test approach conflict
        resolution = conflict_mgr.resolve_approach_conflict(
            {"id": "agent-a", "approach": "Use ORM", 
             "rationale": "Because it's tested and proven in production"},
            {"id": "agent-b", "approach": "Raw SQL",
             "rationale": "Because trade-off: better performance"},
        )
        
        return {
            "test": "conflict_resolution",
            "file_locking": {
                "first_acquired": acquired1,
                "second_blocked": not acquired2,
                "status": "PASS" if acquired1 and not acquired2 else "FAIL",
            },
            "approach_conflict": {
                "resolved": "winner" in resolution,
                "winner": resolution.get("winner"),
                "status": "PASS" if "winner" in resolution else "FAIL",
            },
        }
    
    def get_summary(self) -> Dict:
        """Tổng hợp kết quả tests"""
        passed = sum(1 for t in self.test_results if t.get("status") == "PASS")
        failed = sum(1 for t in self.test_results if t.get("status") == "FAIL")
        
        return {
            "total": len(self.test_results),
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / len(self.test_results) if self.test_results else 0,
            "failures": [t for t in self.test_results if t.get("status") == "FAIL"],
        }
