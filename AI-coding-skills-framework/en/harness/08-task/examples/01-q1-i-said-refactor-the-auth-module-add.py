# One file = one sub-task, safe to run side by side
SubTask(id=f"{task.id}-f01", order=1, parallel=True,
        files_to_modify=["src/auth.py"],
        estimated_tokens=1000,
        verification_criteria="File src/auth.py updated correctly")
