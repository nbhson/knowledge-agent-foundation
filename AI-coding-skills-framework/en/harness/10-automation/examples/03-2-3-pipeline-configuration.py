from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CIPipelineConfig:
    """Configuration for a CI/CD pipeline"""
    
    # Language / Framework
    language: str = "python"
    python_version: str = "3.11"
    
    # Quality Gates
    lint_enabled: bool = True
    type_check_enabled: bool = True
    min_test_coverage: float = 80.0
    max_complexity: int = 10
    
    # Security
    security_scan: bool = True
    dependency_audit: bool = True
    
    # Build
    docker_enabled: bool = True
    docker_registry: str = "ghcr.io"
    
    # Deploy
    deploy_staging: bool = True
    deploy_production: bool = True
    canary_percentage: int = 10
    canary_duration_minutes: int = 5
    
    # Notifications
    slack_notify: bool = True
    email_on_failure: bool = True
    
    def to_github_actions(self) -> str:
        """Generate GitHub Actions workflow YAML"""
        lines = [
            "name: CI/CD Pipeline",
            "on:",
            "  push:",
            "    branches: [main]",
            "  pull_request:",
            "    branches: [main]",
            "",
            "jobs:",
            "  quality-gate:",
            "    runs-on: ubuntu-latest",
            "    steps:",
            "      - uses: actions/checkout@v4",
        ]
        
        if self.language == "python":
            lines.extend([
                f"      - uses: actions/setup-python@v5",
                f"        with:",
                f"          python-version: '{self.python_version}'",
                "      - run: pip install -e '.[dev]'",
            ])
            
            if self.lint_enabled:
                lines.append("      - run: ruff check .")
            if self.type_check_enabled:
                lines.append("      - run: mypy src/")
            
            lines.extend([
                f"      - run: pytest --cov=src/ --cov-fail-under={self.min_test_coverage}",
            ])
        
        return "\n".join(lines)
