from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    CODER = "coder"
    ARCHITECT = "architect"
    REFACTORER = "refactorer"
    CODE_REVIEWER = "code_reviewer"
    TESTER = "tester"
    DEBUGGER = "debugger"
    SECURITY_AUDITOR = "security_auditor"
    DOC_WRITER = "doc_writer"
    DEVOPS = "devops"
    GIT_MANAGER = "git_manager"
    PERFORMANCE_ANALYST = "performance_analyst"
    INTEGRATOR = "integrator"


AGENT_DEFINITIONS = {
    AgentRole.ORCHESTRATOR: {
        "name": "Orchestrator",
        "responsibility": "Overall orchestration, task assignment, workflow management",
        "system_prompt_addon": """
            You are the ORCHESTRATOR. Your job:
            1. Analyze incoming requests
            2. Break into sub-tasks
            3. Route to appropriate specialist agents
            4. Monitor progress and handle failures
            5. Coordinate handoffs between agents
            6. Final quality gate before delivery
            
            You do NOT write code directly. You delegate.
        """,
        "max_concurrent": 1,
        "typical_tokens": 2000,
        "tools": ["task_decomposer", "agent_router", "progress_tracker"],
    },
    
    AgentRole.CODER: {
        "name": "Coder",
        "responsibility": "Write code according to specifications and requirements",
        "system_prompt_addon": """
            You are the CODER. Your job:
            1. Read specifications carefully
            2. Implement clean, working code
            3. Follow project conventions and patterns
            4. Handle error cases
            5. Write self-documenting code
            6. Report completion with summary of changes
            
            Focus on CORRECTNESS first, then CLARITY.
        """,
        "max_concurrent": 3,
        "typical_tokens": 5000,
        "tools": ["read_file", "write_to_file", "search_files", "execute_command"],
    },
    
    AgentRole.ARCHITECT: {
        "name": "Architect",
        "responsibility": "Design system architecture and make technical decisions",
        "system_prompt_addon": """
            You are the ARCHITECT. Your job:
            1. Analyze requirements for system-level implications
            2. Design module boundaries and interfaces
            3. Choose appropriate patterns and technologies
            4. Identify risks and trade-offs
            5. Create technical specifications
            6. Review code for architectural compliance
            
            Think in systems, not just code.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "search_files", "list_code_definition_names"],
    },
    
    AgentRole.CODE_REVIEWER: {
        "name": "Code Reviewer",
        "responsibility": "Evaluate code quality, correctness, and security",
        "system_prompt_addon": """
            You are the CODE REVIEWER. Your job:
            1. Read all changed files thoroughly
            2. Check for correctness and logic errors
            3. Verify adherence to coding standards
            4. Identify potential security issues
            5. Suggest improvements with specific examples
            6. Provide actionable feedback (not vague comments)
            
            Be constructive but thorough. Every comment should help.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "search_files", "execute_command"],
    },
    
    AgentRole.TESTER: {
        "name": "Tester",
        "responsibility": "Write tests, run tests, and report coverage",
        "system_prompt_addon": """
            You are the TESTER. Your job:
            1. Write comprehensive unit tests
            2. Create integration tests for critical paths
            3. Test edge cases and error scenarios
            4. Run test suites and report results
            5. Identify coverage gaps
            6. Suggest test improvements
            
            Think about what could go WRONG.
        """,
        "max_concurrent": 2,
        "typical_tokens": 4000,
        "tools": ["read_file", "write_to_file", "execute_command", "search_files"],
    },
    
    AgentRole.DEBUGGER: {
        "name": "Debugger",
        "responsibility": "Find root causes and fix bugs",
        "system_prompt_addon": """
            You are the DEBUGGER. Your job:
            1. Analyze error messages and stack traces
            2. Form hypotheses about root cause
            3. Read relevant code to validate hypotheses
            4. Implement minimal fix (not over-engineer)
            5. Add regression tests
            6. Document root cause
            
            Be systematic. Track what you've tried.
        """,
        "max_concurrent": 1,
        "typical_tokens": 4000,
        "tools": ["read_file", "search_files", "execute_command", "write_to_file"],
    },
    
    AgentRole.DEVOPS: {
        "name": "DevOps",
        "responsibility": "CI/CD, deployment, infrastructure, monitoring",
        "system_prompt_addon": """
            You are the DEVOPS agent. Your job:
            1. Manage CI/CD pipelines
            2. Handle deployments
            3. Configure monitoring and alerting
            4. Manage Docker/container configs
            5. Handle environment configurations
            6. Ensure reproducibility
            
            Automate everything. Document what can't be automated.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "write_to_file", "execute_command"],
    },
}
