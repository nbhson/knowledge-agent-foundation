class AntiPatternDetector:
    """
    Phát hiện anti-patterns trong task management.
    """
    
    def detect(self, task: Task, context: Dict = None) -> List[Dict]:
        """Kiểm tra task và trả về list anti-patterns"""
        issues = []
        context = context or {}
        
        # Check 1: Killer Task
        if task.estimated_tokens > 20000:
            issues.append({
                "pattern": "KILLER_TASK",
                "severity": "HIGH",
                "message": f"Task estimated {task.estimated_tokens} tokens. "
                          f"Decompose into smaller tasks (< 5K each).",
                "suggestion": "Use TaskDecomposer with 'feature' or 'layer' strategy",
            })
        
        # Check 2: Ambiguous Task
        vague_keywords = [
            "improve", "optimize", "clean", "better",
            "refactor", "make it work", "fix it"
        ]
        if any(kw in task.description.lower() for kw in vague_keywords):
            if not task.verification_criteria:
                issues.append({
                    "pattern": "AMBIGUOUS_TASK",
                    "severity": "MEDIUM",
                    "message": "Task description is vague without clear criteria",
                    "suggestion": "Add specific acceptance criteria and expected outcomes",
                })
        
        # Check 3: Missing Token Estimate
        if task.estimated_tokens == 0:
            issues.append({
                "pattern": "MISSING_ESTIMATE",
                "severity": "LOW",
                "message": "No token estimate provided",
                "suggestion": "Use EffortEstimator to get initial estimate",
            })
        
        # Check 4: Too Many Dependencies
        if len(task.dependencies) > 5:
            issues.append({
                "pattern": "DEPENDENCY_OVERLOAD",
                "severity": "MEDIUM",
                "message": f"Task has {len(task.dependencies)} dependencies",
                "suggestion": "Consider reducing dependencies or splitting task",
            })
        
        # Check 5: No Files Involved (for modification tasks)
        if (task.category == TaskCategory.MODIFICATION 
            and len(task.files_involved) == 0):
            issues.append({
                "pattern": "MISSING_FILE_SCOPE",
                "severity": "MEDIUM",
                "message": "Modification task has no files identified",
                "suggestion": "Scan codebase to identify affected files",
            })
        
        return issues
