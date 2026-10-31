WORKFLOW_TEMPLATES = {
    "feature_pipeline": {
        "description": "Full feature development automation",
        "steps": [
            {"name": "lint", "command": "ruff check .", "gate": True},
            {"name": "typecheck", "command": "mypy src/", "gate": True},
            {"name": "unit_tests", "command": "pytest tests/unit/ -v", "gate": True},
            {"name": "integration_tests", "command": "pytest tests/integration/ -v", "gate": True},
            {"name": "build", "command": "docker build -t app .", "gate": True},
            {"name": "deploy_staging", "command": "kubectl apply -f k8s/staging/", "gate": False},
            {"name": "smoke_test", "command": "curl -f http://staging/health", "gate": True},
            {"name": "deploy_prod", "command": "kubectl apply -f k8s/prod/", "gate": True},
        ],
    },
    
    "hotfix_pipeline": {
        "description": "Emergency hotfix — fast track",
        "steps": [
            {"name": "lint", "command": "ruff check .", "gate": True},
            {"name": "quick_test", "command": "pytest tests/unit/ -x -q", "gate": True},
            {"name": "deploy_prod", "command": "kubectl apply -f k8s/prod/", "gate": True},
            {"name": "verify", "command": "curl -f http://prod/health", "gate": True},
            {"name": "notify", "command": "echo 'Hotfix deployed'", "gate": False},
        ],
    },
    
    "nightly_maintenance": {
        "description": "Nightly maintenance tasks",
        "steps": [
            {"name": "backup_db", "command": "pg_dump app > backup.sql", "gate": True},
            {"name": "cleanup_logs", "command": "find /var/log -mtime +30 -delete", "gate": False},
            {"name": "security_scan", "command": "safety check", "gate": False},
            {"name": "dependency_update", "command": "pip install --upgrade -r requirements.txt", "gate": False},
            {"name": "full_test_suite", "command": "pytest --cov=src/", "gate": False},
        ],
    },
    
    "pr_quality_check": {
        "description": "Automated PR quality gate",
        "steps": [
            {"name": "lint", "command": "ruff check --output-format=github", "gate": True},
            {"name": "format_check", "command": "ruff format --check", "gate": True},
            {"name": "type_check", "command": "mypy src/", "gate": True},
            {"name": "unit_tests", "command": "pytest tests/unit/ --cov=src/ --cov-fail-under=80", "gate": True},
            {"name": "security_scan", "command": "bandit -r src/", "gate": False},
        ],
    },
}
