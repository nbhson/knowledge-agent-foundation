# Real-world example: How a team evaluates their AI coding agent

class ProductionEvaluator:
    """
    Production evaluation pipeline được dùng hàng ngày.
    
    Context: Team 20 developers sử dụng AI coding agent
    daily. Pipeline chạy mỗi đêm để monitor quality.
    """
    
    def __init__(self):
        self.benchmark_suite = BenchmarkSuite("daily")
        self.regression_suite = RegressionTestSuite("production")
        self.reporter = EvaluationReporter()
    
    def setup_daily_benchmarks(self):
        """Setup benchmark tasks cho daily run"""
        
        # 10 representative tasks cho team's domain
        self.benchmark_suite.add_task(
            "fix-001", "Fix null pointer in UserService.getProfile",
            validator=lambda out: "null check" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "feat-001", "Add pagination to ProductController.list",
            validator=lambda out: "offset" in str(out).lower() or 
                                   "limit" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "test-001", "Write unit tests for PaymentService.charge",
            validator=lambda out: "assert" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "refactor-001", "Extract database queries to repository pattern",
            validator=lambda out: "Repository" in str(out)
        )
        
        self.benchmark_suite.add_task(
            "security-001", "Fix SQL injection in UserDAO.findByEmail",
            validator=lambda out: "parameterized" in str(out).lower() or
                                   "prepared" in str(out).lower()
        )
    
    def run_daily_evaluation(self, agent_func: Callable) -> Dict:
        """Chạy evaluation hàng ngày"""
        
        # 1. Run benchmarks
        summary = self.benchmark_suite.run(agent_func)
        
        # 2. Check regression
        reg_result = self.regression_suite.run_and_check(agent_func)
        
        # 3. Generate report
        report = self.reporter.generate_markdown_report(
            [],  # Would pass actual results
            summary
        )
        
        # 4. Alert if regression detected
        if reg_result["has_regression"]:
            self._send_alert(reg_result)
        
        # 5. Track trend
        return {
            "summary": summary,
            "regression": reg_result,
            "report": report,
        }
    
    def _send_alert(self, reg_result: Dict):
        """Gửi alert khi regression detected"""
        regressions = reg_result["regressions"]
        message = f"⚠️ REGRESSION DETECTED!\n"
        message += f"Score delta: {reg_result['score_delta']:.1f}%\n"
        for reg in regressions:
            message += f"  - {reg['id']}: {reg['baseline']:.0f} → {reg['current']:.0f}\n"
        
        # Would send to Slack, email, etc.
        print(message)
