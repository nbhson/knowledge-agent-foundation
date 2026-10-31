TASK_TEMPLATES = {
    "bug_fix": {
        "title": "Fix: {bug_description}",
        "subtasks": [
            {"title": "Reproduce the bug", "tokens": 500},
            {"title": "Read and understand affected code", "tokens": 1000},
            {"title": "Identify root cause", "tokens": 800},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Write regression test", "tokens": 1000},
            {"title": "Verify fix in all scenarios", "tokens": 500},
        ],
        "estimated_total_tokens": 5300,
    },
    
    "new_feature": {
        "title": "Feature: {feature_name}",
        "subtasks": [
            {"title": "Analyze requirements", "tokens": 500},
            {"title": "Read existing code patterns", "tokens": 1000},
            {"title": "Design approach", "tokens": 800},
            {"title": "Implement core logic", "tokens": 3000},
            {"title": "Add error handling", "tokens": 800},
            {"title": "Write tests", "tokens": 1500},
            {"title": "Update documentation", "tokens": 500},
        ],
        "estimated_total_tokens": 8100,
    },
    
    "code_review": {
        "title": "Review: {target}",
        "subtasks": [
            {"title": "Read all changed files", "tokens": 2000},
            {"title": "Check code style & conventions", "tokens": 500},
            {"title": "Analyze logic & correctness", "tokens": 1500},
            {"title": "Review for security issues", "tokens": 1000},
            {"title": "Write review comments", "tokens": 1000},
        ],
        "estimated_total_tokens": 6000,
    },
    
    "refactor": {
        "title": "Refactor: {target_module}",
        "subtasks": [
            {"title": "Analyze current structure", "tokens": 1000},
            {"title": "Identify code smells", "tokens": 800},
            {"title": "Plan refactoring steps", "tokens": 500},
            {"title": "Extract functions/classes", "tokens": 2000},
            {"title": "Update imports & references", "tokens": 1000},
            {"title": "Run existing tests", "tokens": 500},
            {"title": "Verify behavior unchanged", "tokens": 500},
        ],
        "estimated_total_tokens": 6300,
    },
    
    "debug_investigation": {
        "title": "Debug: {issue_description}",
        "subtasks": [
            {"title": "Gather error info and logs", "tokens": 800},
            {"title": "Read stack trace and affected files", "tokens": 1500},
            {"title": "Add strategic logging/breakpoints", "tokens": 1000},
            {"title": "Reproduce with minimal test case", "tokens": 800},
            {"title": "Identify root cause", "tokens": 1000},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Add regression test", "tokens": 800},
        ],
        "estimated_total_tokens": 7400,
    },
    
    "performance_optimization": {
        "title": "Optimize: {target}",
        "subtasks": [
            {"title": "Profile current performance", "tokens": 1000},
            {"title": "Identify bottlenecks", "tokens": 800},
            {"title": "Research optimization strategies", "tokens": 1000},
            {"title": "Implement optimizations", "tokens": 2000},
            {"title": "Benchmark before/after", "tokens": 800},
            {"title": "Verify no regressions", "tokens": 500},
        ],
        "estimated_total_tokens": 6100,
    },
    
    "migration": {
        "title": "Migrate: {source} → {target}",
        "subtasks": [
            {"title": "Analyze source and target", "tokens": 1500},
            {"title": "Create migration plan", "tokens": 800},
            {"title": "Write migration scripts", "tokens": 2000},
            {"title": "Test migration on sample data", "tokens": 1000},
            {"title": "Run full migration", "tokens": 1500},
            {"title": "Verify and cleanup", "tokens": 800},
        ],
        "estimated_total_tokens": 7600,
    },
}


def create_task_from_template(template_name: str, **kwargs) -> Task:
    """Tạo task từ template"""
    template = TASK_TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")
    
    title = template["title"].format(**kwargs)
    
    return Task(
        id=f"task-{hash(title) % 10000:04d}",
        title=title,
        description=f"Task from template: {template_name}",
        category=TaskCategory.UNKNOWN,
        estimated_tokens=template["estimated_total_tokens"],
    )
