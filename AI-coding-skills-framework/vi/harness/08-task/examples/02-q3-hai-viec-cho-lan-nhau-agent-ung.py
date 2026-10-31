if len(order) != len(self.tasks):
    raise ValueError("Cycle detected in task dependencies")
