class AgentState:
    """
    Manage state across agent execution steps
    
    Supports: state persistence, checkpointing, rollback, versioning
    """
    
    def __init__(self):
        self.state = {}
        self.history = []
        self.checkpoints = []
        self.version = 0
    
    def set(self, key, value):
        """Set state value with versioning"""
        old_value = self.state.get(key)
        self.state[key] = value
        self.version += 1
        
        self.history.append({
            "action": "set",
            "key": key,
            "old": old_value,
            "new": value,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get(self, key, default=None):
        """Get state value"""
        return self.state.get(key, default)
    
    def checkpoint(self):
        """Save current state snapshot"""
        self.checkpoints.append({
            "state": dict(self.state),
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
        return len(self.checkpoints) - 1
    
    def rollback(self, checkpoint_id=None):
        """Rollback to checkpoint"""
        if checkpoint_id is None:
            checkpoint_id = len(self.checkpoints) - 1
        
        if 0 <= checkpoint_id < len(self.checkpoints):
            self.state = dict(self.checkpoints[checkpoint_id]["state"])
            self.version = self.checkpoints[checkpoint_id]["version"]
            return True
        return False
    
    def to_context(self):
        """Convert state to context string for LLM"""
        lines = [f"{k}: {v}" for k, v in self.state.items()]
        return "\n".join(lines)
    
    def diff(self, checkpoint_id):
        """Compare current state with checkpoint"""
        if 0 <= checkpoint_id < len(self.checkpoints):
            old = self.checkpoints[checkpoint_id]["state"]
            current = self.state
            
            changes = {
                "added": {k: v for k, v in current.items() if k not in old},
                "removed": {k: v for k, v in old.items() if k not in current},
                "modified": {k: (old.get(k), current.get(k)) 
                           for k in current if k in old and current[k] != old[k]},
            }
            return changes
        return {}
    
    def reset(self):
        """Clear all state"""
        self.state = {}
        self.version = 0
