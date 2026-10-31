class WorkflowOrchestrator:
    """
    Complete workflow orchestration engine combining all patterns:
    - State machine for flow control
    - Pipeline for data processing
    - Saga for error recovery
    - Tracing for observability
    - Metrics for monitoring
    """
    
    def __init__(self, name: str):
        self.name = name
        self.tracer = Tracer()
        self.logger = WorkflowLogger(name)
        self.metrics = MetricsCollector()
        self.state_machine = HierarchicalStateMachine(name)
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.workflows: Dict[str, Callable] = {}
        self._setup_default_transitions()
    
    def _setup_default_transitions(self):
        """Setup default state transitions"""
        sm = self.state_machine
        
        sm.add_transition(Transition(
            from_state=AgentState.IDLE,
            to_state=AgentState.THINKING,
            condition=lambda ctx: ctx.get("task") is not None,
            name="task_received",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.THINKING,
            to_state=AgentState.PLANNING,
            condition=lambda ctx: ctx.get("analysis_done"),
            name="analysis_complete",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.PLANNING,
            to_state=AgentState.READING_CODE,
            condition=lambda ctx: ctx.get("plan_ready"),
            name="plan_approved",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.READING_CODE,
            to_state=AgentState.WRITING_CODE,
            condition=lambda ctx: ctx.get("code_read"),
            name="context_gathered",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.WRITING_CODE,
            to_state=AgentState.RUNNING_TESTS,
            condition=lambda ctx: ctx.get("code_written"),
            name="code_written",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.RUNNING_TESTS,
            to_state=AgentState.DONE,
            condition=lambda ctx: ctx.get("tests_passed"),
            name="tests_passed",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.RUNNING_TESTS,
            to_state=AgentState.FIXING_ERRORS,
            condition=lambda ctx: ctx.get("tests_failed"),
            name="tests_failed",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.FIXING_ERRORS,
            to_state=AgentState.RUNNING_TESTS,
            condition=lambda ctx: True,
            name="fix_applied",
        ))
        
        # Max fix attempts → ROLLBACK
        sm.add_transition(Transition(
            from_state=AgentState.FIXING_ERRORS,
            to_state=AgentState.ROLLING_BACK,
            condition=lambda ctx: ctx.get("fix_attempts", 0) >= 3,
            name="max_fixes_reached",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.ROLLING_BACK,
            to_state=AgentState.ERROR,
            condition=lambda ctx: ctx.get("rollback_done"),
            name="rollback_complete",
        ))
    
    def register_workflow(self, name: str, func: Callable):
        self.workflows[name] = func
        return self
    
    def get_circuit_breaker(self, service: str) -> CircuitBreaker:
        if service not in self.circuit_breakers:
            self.circuit_breakers[service] = CircuitBreaker(
                failure_threshold=5, recovery_timeout=30
            )
        return self.circuit_breakers[service]
    
    def execute(self, task: Dict) -> Dict:
        trace_id = self.tracer.start_trace(f"workflow_{self.name}")
        
        with self.tracer.span("orchestrate", {"task": str(task)[:200]}):
            try:
                self.state_machine.context["task"] = task
                result = self.state_machine.run(task, max_iterations=50)
                
                self.metrics.counter("workflow.success")
                self.metrics.counter(f"workflow.{self.name}.success")
                
                return {
                    "success": True,
                    "result": result,
                    "trace_id": trace_id,
                    "state_path": self.state_machine.get_state_path(),
                    "stats": self.state_machine.get_stats(),
                }
            except Exception as e:
                self.metrics.counter("workflow.error")
                return {
                    "success": False,
                    "error": str(e),
                    "trace_id": trace_id,
                    "state_path": self.state_machine.get_state_path(),
                }
    
    def get_dashboard(self) -> Dict:
        """Get comprehensive dashboard data"""
        return {
            "workflow": self.name,
            "state": self.state_machine.state.value,
            "stats": self.state_machine.get_stats(),
            "circuit_breakers": {
                name: cb.get_state()
                for name, cb in self.circuit_breakers.items()
            },
            "traces_count": len(self.tracer.traces),
            "metrics": self.metrics.get_summary(),
            "history": self.logger.logs[-10:],  # Last 10 logs
        }
