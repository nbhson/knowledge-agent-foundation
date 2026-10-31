if any(k in task.description.lower() for k in ["fix", "bug", "refactor"]):
    task.category = TaskCategory.MODIFICATION
task.priority = 5        # 1 = cao nhất, 10 = thấp nhất
