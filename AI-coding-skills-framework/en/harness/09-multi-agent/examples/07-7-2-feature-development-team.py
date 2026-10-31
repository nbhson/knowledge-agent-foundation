class FeatureDevTeam:
    """
    Multi-agent feature development:
    1. Architect designs the approach
    2. Coder implements (parallel for independent modules)
    3. Tester writes & runs tests
    4. Reviewer validates quality
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.HIERARCHICAL
        )
        
        self.orchestrator.register_agent(
            "architect", AgentRole.ARCHITECT
        )
        self.orchestrator.register_agent(
            "coder-1", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "coder-2", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "tester", AgentRole.TESTER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
    
    def develop_feature(self, feature_spec: str) -> Dict:
        """Develop a feature with a multi-agent team"""
        tasks = [
            {
                "id": "design",
                "type": "architect",
                "input": {"spec": feature_spec},
                "depends_on": [],
            },
            {
                "id": "implement-core",
                "type": "code",
                "input": {"module": "core"},
                "depends_on": ["design"],
            },
            {
                "id": "implement-api",
                "type": "code",
                "input": {"module": "api"},
                "depends_on": ["design"],
            },
            {
                "id": "write-tests",
                "type": "test",
                "input": {"target": "all"},
                "depends_on": ["implement-core", "implement-api"],
            },
            {
                "id": "review",
                "type": "review",
                "input": {},
                "depends_on": ["write-tests"],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
