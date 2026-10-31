for step in self.steps:
    result = step.action(data)                      # forward
    self.completed_steps.append({"name": step.name})
except Exception as e:
    for completed in reversed(self.completed_steps):
        completed["compensation"]()                 # undo, newest first
