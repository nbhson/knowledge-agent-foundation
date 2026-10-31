import unittest

class TestTaskPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = TaskPlanner()
    
    def test_simple_decomposition(self):
        """Simple task → 1-3 subtasks"""
        task = Task(id="t1", name="Fix typo", description="Fix typo in README")
        plan = self.planner.decompose("Fix typo in README")
        self.assertLessEqual(len(plan), 3)
    
    def test_complex_decomposition(self):
        """Complex task → multiple subtasks"""
        plan = self.planner.decompose(
            "Build a complete RAG system with vector search, "
            "chunking, embedding, and query processing"
        )
        self.assertGreater(len(plan), 3)
    
    def test_complexity_estimation(self):
        """Estimate complexity correctly"""
        task = Task(id="t1", name="Simple", description="Simple task")
        estimate = self.planner.estimate_complexity(task)
        self.assertIn(estimate["complexity"], ["simple", "medium", "complex"])
    
    def test_dependency_detection(self):
        """Verify dependency-based execution order"""
        t1 = Task(id="t1", name="Setup DB", dependencies=[])
        t2 = Task(id="t2", name="Create schema", dependencies=["t1"])
        t3 = Task(id="t3", name="Insert data", dependencies=["t2"])
        
        completed = set()
        # t1 phải có thể thực thi trước
        self.assertTrue(t1.can_execute(completed))
        
        # t2 CHƯA ĐƯỢC thực thi
        self.assertFalse(t2.can_execute(completed))
        
        # Sau khi t1 hoàn thành
        completed.add("t1")
        self.assertTrue(t2.can_execute(completed))
    
    def test_max_depth_limit(self):
        """Verify decomposition respects max depth"""
        plan = self.planner.decompose(
            "Build: a → b → c → d → e → f",
            max_depth=2
        )
        depth = self.planner._get_depth(
            Task(id="root", subtasks=plan)
        )
        self.assertLessEqual(depth, 2)
    
    def test_retry_logic(self):
        """Test task retry on failure"""
        task = Task(id="t1", name="Flaky task", max_retries=3)
        
        # Thất bại lần đầu
        task.mark_failed("timeout")
        self.assertTrue(task.can_retry())
        
        # Sau 3 lần thử lại (retries)
        task.retry_count = 3
        self.assertFalse(task.can_retry())

class TestTokenBudget(unittest.TestCase):
    def setUp(self):
        self.budget_manager = TokenBudgetManager(totalBudget=50000)
    
    def test_allocation_within_budget(self):
        """Allocate within budget"""
        result = self.budget_manager.allocate("task1", 20000)
        self.assertTrue(result)
    
    def test_allocation_exceeds_budget(self):
        """Allocation exceeds budget"""
        self.budget_manager.allocate("task1", 30000)
        result = self.budget_manager.allocate("task2", 25000)
        self.assertFalse(result)
    
    def test_usage_tracking(self):
        """Track token usage per task"""
        self.budget_manager.allocate("task1", 10000)
        self.budget_manager.report("task1", 5000)
        
        self.assertTrue(self.budget_manager.canContinue("task1"))
        
        self.budget_manager.report("task1", 4500)
        self.assertFalse(self.budget_manager.canContinue("task1"))

class TestAgentState(unittest.TestCase):
    def setUp(self):
        self.state = AgentState()
    
    def test_set_and_get(self):
        self.state.set("key1", "value1")
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_checkpoint_and_rollback(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.assertEqual(self.state.get("key1"), "value2")
        
        self.state.rollback(cp)
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_diff(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.state.set("key2", "value3")
        
        changes = self.state.diff(cp)
        self.assertIn("key2", changes["added"])
        self.assertIn("key1", changes["modified"])

if __name__ == "__main__":
    unittest.main()
