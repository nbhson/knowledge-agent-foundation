import unittest

class TestSequentialWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = SequentialWorkflow("test_seq")
        self.workflow.add_step("step1", lambda x: x * 2)
        self.workflow.add_step("step2", lambda x: x + 10)
        self.workflow.add_step("step3", lambda x: x ** 2)
    
    def test_basic_run(self):
        result = self.workflow.run(5)
        self.assertEqual(result, 400)  # (5*2 + 10)^2 = 400
    
    def test_history_recorded(self):
        self.workflow.run(5)
        history = self.workflow.get_history()
        self.assertEqual(len(history), 3)
        self.assertTrue(all(h["status"] == "success" for h in history))
    
    def test_error_handling(self):
        workflow = SequentialWorkflow("test_error")
        workflow.add_step("fail", lambda x: 1/0)
        
        with self.assertRaises(WorkflowError):
            workflow.run(1)
        
        self.assertEqual(workflow.state["status"], "failed")
    
    def test_summary(self):
        self.workflow.run(5)
        summary = self.workflow.get_summary()
        self.assertEqual(summary["total_steps"], 3)
        self.assertEqual(summary["successful"], 3)
        self.assertEqual(summary["status"], "completed")


class TestDAGWorkflow(unittest.TestCase):
    def test_linear_dag(self):
        dag = DAGWorkflow("test_linear")
        dag.add_node("A", lambda x: 1)
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        dag.add_node("C", lambda x: 3, depends_on=["B"])
        
        result = dag.run()
        self.assertEqual(result["total_nodes"], 3)
        self.assertEqual(result["successful"], 3)
    
    def test_parallel_dag(self):
        dag = DAGWorkflow("test_parallel")
        dag.add_node("A", lambda x: 10)
        dag.add_node("B", lambda x: 20)
        dag.add_node("C", lambda x: 30, depends_on=["A", "B"])
        
        result = dag.run()
        self.assertEqual(result["total_nodes"], 3)
    
    def test_cycle_detection(self):
        dag = DAGWorkflow("test_cycle")
        dag.add_node("A", lambda x: 1, depends_on=["C"])
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        dag.add_node("C", lambda x: 3, depends_on=["B"])
        
        validation = dag.validate()
        self.assertFalse(validation["valid"])
    
    def test_validation(self):
        dag = DAGWorkflow("test_valid")
        dag.add_node("A", lambda x: 1)
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        
        validation = dag.validate()
        self.assertTrue(validation["valid"])


class TestCircuitBreaker(unittest.TestCase):
    def setUp(self):
        self.cb = CircuitBreaker(failure_threshold=3, recovery_timeout=0.1)
    
    def test_normal_flow(self):
        result = self.cb.call(lambda: "ok")
        self.assertEqual(result, "ok")
        self.assertEqual(self.cb.state, CircuitState.CLOSED)
    
    def test_trips_after_failures(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        self.assertEqual(self.cb.state, CircuitState.OPEN)
    
    def test_rejects_when_open(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        
        with self.assertRaises(CircuitOpenError):
            self.cb.call(lambda: "ok")
    
    def test_half_open_recovery(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        
        time.sleep(0.15)
        result = self.cb.call(lambda: "recovered")
        self.assertEqual(result, "recovered")


class TestSagaOrchestrator(unittest.TestCase):
    def test_successful_saga(self):
        saga = SagaOrchestrator("test_saga")
        saga.add_step("step1", lambda x: "result1", lambda: None)
        saga.add_step("step2", lambda x: "result2", lambda: None)
        
        result = saga.execute()
        self.assertTrue(result["success"])
    
    def test_compensation_on_failure(self):
        compensated = []
        
        saga = SagaOrchestrator("test_compensate")
        saga.add_step("step1", lambda x: "ok", lambda: compensated.append("undo1"))
        saga.add_step("step2", lambda x: 1/0, lambda: compensated.append("undo2"))
        saga.add_step("step3", lambda x: "ok", lambda: compensated.append("undo3"))
        
        result = saga.execute()
        self.assertFalse(result["success"])
        self.assertTrue(result["compensated"])
        self.assertIn("undo1", compensated)


class TestTracer(unittest.TestCase):
    def test_trace_creation(self):
        tracer = Tracer()
        trace_id = tracer.start_trace("test_trace")
        self.assertIn(trace_id, tracer.traces)
    
    def test_span_nesting(self):
        tracer = Tracer()
        trace_id = tracer.start_trace("test")
        
        with tracer.span("parent") as parent:
            with tracer.span("child") as child:
                pass
        
        trace = tracer.get_trace(trace_id)
        self.assertEqual(len(trace), 2)


if __name__ == "__main__":
    unittest.main()
