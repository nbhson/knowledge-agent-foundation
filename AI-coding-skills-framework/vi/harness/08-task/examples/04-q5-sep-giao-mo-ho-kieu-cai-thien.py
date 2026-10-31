vague = ["improve", "optimize", "clean", "better",
         "refactor", "make it work", "fix it"]
if any(k in task.description.lower() for k in vague) and not task.verification_criteria:
    issues.append({"pattern": "AMBIGUOUS_TASK", "severity": "MEDIUM"})
