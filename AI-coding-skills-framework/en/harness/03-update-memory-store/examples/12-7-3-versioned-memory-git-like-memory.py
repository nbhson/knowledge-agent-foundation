"""
Versioned Memory: Like Git — each change creates a new version.

Enables:
- Time travel: View memory at time T
- Diff: Compare memory between two time points
- Branch: Create alternative versions
- Rollback: Return to a previous version
"""

class VersionedMemory:
    """
    Git-like versioned memory system
    """
    
    def __init__(self):
        self.versions = []  # List of snapshots
        self.current = {}
    
    def set(self, key, value, message=""):
        """Set a value, creating a new version"""
        # Capture previous state
        prev_snapshot = dict(self.current)
        
        # Apply change
        self.current[key] = value
        
        # Record version
        version = {
            "id": len(self.versions),
            "snapshot": dict(self.current),
            "change": {"key": key, "value": value},
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "parent": len(self.versions) - 1 if self.versions else None
        }
        
        self.versions.append(version)
        return version["id"]
    
    def get(self, key, version_id=None):
        """Get value at a specific version"""
        if version_id is None:
            return self.current.get(key)
        
        if version_id >= len(self.versions):
            return None
        
        return self.versions[version_id]["snapshot"].get(key)
    
    def diff(self, v1_id, v2_id):
        """Compare two versions"""
        if v1_id >= len(self.versions) or v2_id >= len(self.versions):
            return {"error": "Invalid version IDs"}
        
        v1 = self.versions[v1_id]["snapshot"]
        v2 = self.versions[v2_id]["snapshot"]
        
        all_keys = set(v1.keys()) | set(v2.keys())
        
        changes = []
        for key in all_keys:
            old = v1.get(key)
            new = v2.get(key)
            
            if old != new:
                if old is None:
                    changes.append({"key": key, "type": "added", "new": new})
                elif new is None:
                    changes.append({"key": key, "type": "removed", "old": old})
                else:
                    changes.append({"key": key, "type": "modified", 
                                   "old": old, "new": new})
        
        return {"changes": changes, "count": len(changes)}
    
    def rollback(self, version_id):
        """Rollback to a previous version"""
        if version_id >= len(self.versions):
            return {"error": "Invalid version ID"}
        
        self.current = dict(self.versions[version_id]["snapshot"])
        
        return {
            "rolled_back_to": version_id,
            "current_state": self.current
        }
    
    def log(self, limit=10):
        """View version history"""
        return [
            {
                "id": v["id"],
                "change": v["change"],
                "message": v["message"],
                "timestamp": v["timestamp"]
            }
            for v in self.versions[-limit:]
        ]
