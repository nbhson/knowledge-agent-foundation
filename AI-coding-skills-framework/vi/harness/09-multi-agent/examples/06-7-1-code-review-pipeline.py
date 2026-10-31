class CodeReviewPipeline:
    """
    Multi-agent code review pipeline:
    1. Git Manager collects changed files
    2. Coder provides context
    3. Reviewer analyzes code
    4. Security Auditor checks vulnerabilities
    5. Orchestrator merges feedback
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.SEQUENTIAL
        )
        
        # Register agents
        self.orchestrator.register_agent(
            "git-mgr", AgentRole.GIT_MANAGER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
        self.orchestrator.register_agent(
            "security", AgentRole.SECURITY_AUDITOR
        )
        self.orchestrator.register_agent(
            "perf", AgentRole.PERFORMANCE_ANALYST
        )
    
    def review(self, pr_description: str, 
               changed_files: List[str]) -> Dict:
        """Execute full code review pipeline"""
        tasks = [
            {
                "id": "collect-context",
                "type": "code",
                "input": {
                    "action": "read_files",
                    "files": changed_files,
                },
                "depends_on": [],
            },
            {
                "id": "code-review",
                "type": "review",
                "input": {"description": pr_description},
                "depends_on": ["collect-context"],
            },
            {
                "id": "security-review",
                "type": "security",
                "input": {"files": changed_files},
                "depends_on": ["collect-context"],
            },
            {
                "id": "perf-review",
                "type": "review",
                "input": {"target": "performance"},
                "depends_on": ["collect-context"],
            },
            {
                "id": "merge-feedback",
                "type": "plan",
                "input": {
                    "combine": [
                        "code-review",
                        "security-review",
                        "perf-review"
                    ]
                },
                "depends_on": [
                    "code-review", 
                    "security-review", 
                    "perf-review"
                ],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
