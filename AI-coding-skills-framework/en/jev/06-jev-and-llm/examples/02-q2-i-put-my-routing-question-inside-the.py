payload = {
  "model": "jev-latest",
  "state": {"task": task, "repo_context": ctx},
  "questions": {"difficulty": {"type": "choice",
                "options": ["trivial", "moderate", "hard"]}},
}
