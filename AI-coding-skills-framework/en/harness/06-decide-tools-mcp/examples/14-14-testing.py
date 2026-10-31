import unittest

class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
    
    def test_register_and_get(self):
        tool = self.registry.get_tool("calculator")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "calculator")
    
    def test_search(self):
        results = self.registry.search("find")
        self.assertGreater(len(results), 0)
    
    def test_category_filter(self):
        tools = self.registry.list_tools(category="search")
        for tool in tools:
            self.assertEqual(tool.category, "search")
    
    def test_deprecation(self):
        tool = self.registry.get_tool("calculator")
        self.assertFalse(tool.is_deprecated())

class TestIntentClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = IntentClassifier()
    
    def test_search_intent(self):
        result = self.classifier.classify("Find information about health insurance")
        self.assertEqual(result["intent"], "search")
        self.assertGreater(len(result["tools"]), 0)
    
    def test_calculate_intent(self):
        result = self.classifier.classify("Calculate 15% of 5000000")
        self.assertEqual(result["intent"], "calculate")
    
    def test_chat_fallback(self):
        result = self.classifier.classify("Hello!")
        self.assertEqual(result["intent"], "chat")
    
    def test_multi_intent(self):
        intents = self.classifier.classify_multi_intent("Read the file and run the tests")
        self.assertGreaterEqual(len(intents), 2)

class TestToolExecutor(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
        self.executor = ToolExecutor(self.registry)
    
    def test_successful_execution(self):
        result = self.executor.execute("calculator", {"expression": "2+3"})
        self.assertTrue(result["success"])
    
    def test_missing_tool(self):
        result = self.executor.execute("nonexistent", {})
        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"])
    
    def test_missing_required_param(self):
        result = self.executor.execute("vector_search", {})
        self.assertFalse(result["success"])
        self.assertIn("Invalid parameters", result["error"])
    
    def test_stats(self):
        self.executor.execute("calculator", {"expression": "1+1"})
        self.executor.execute("calculator", {"expression": "2+2"})
        stats = self.executor.get_stats()
        self.assertEqual(stats["total_calls"], 2)
        self.assertEqual(stats["successful"], 2)

class TestPermissionSystem(unittest.TestCase):
    def setUp(self):
        self.checker = ToolPermissionChecker()
        self.checker.set_user_role("user1", "user")
        self.checker.set_user_role("admin1", "admin")
    
    def test_standard_permission(self):
        result = self.checker.check("user1", "standard")
        self.assertTrue(result["allowed"])
    
    def test_elevated_denied(self):
        result = self.checker.check("user1", "elevated")
        self.assertFalse(result["allowed"])
    
    def test_admin_has_all(self):
        result = self.checker.check("admin1", "admin")
        self.assertTrue(result["allowed"])
    
    def test_custom_grant(self):
        self.checker.grant_permission("user1", "elevated")
        result = self.checker.check("user1", "elevated")
        self.assertTrue(result["allowed"])

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.limiter = RateLimiter(strategy="sliding_window")
        self.limiter.set_limit("api_call", max_calls=3, window_seconds=60)
    
    def test_within_limit(self):
        for _ in range(3):
            result = self.limiter.check("api_call")
            self.assertTrue(result["allowed"])
    
    def test_exceeds_limit(self):
        for _ in range(3):
            self.limiter.check("api_call")
        result = self.limiter.check("api_call")
        self.assertFalse(result["allowed"])
        self.assertIn("retry_after", result)

class TestToolComposer(unittest.TestCase):
    def setUp(self):
        self.registry = create_default_tools()
        self.executor = ToolExecutor(self.registry)
        self.composer = ToolComposer(self.executor)
    
    def test_chain(self):
        steps = [
            {"tool": "calculator", "params": {"expression": "2+3"}, "output_key": "result"},
        ]
        result = self.composer.chain(steps)
        self.assertTrue(result["success"])

if __name__ == "__main__":
    unittest.main()
