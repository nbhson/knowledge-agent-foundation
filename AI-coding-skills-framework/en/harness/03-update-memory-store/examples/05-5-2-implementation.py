class EventSourcedMemory:
    """
    Memory system with full event sourcing
    All changes are stored as events, state is derived
    """
    
    def __init__(self):
        self.events = []
        self.state = {}  # Derived from events
    
    def record_event(self, event_type, data):
        """Record a new event"""
        event = {
            "id": len(self.events),
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self.events.append(event)
        
        # Update state
        self._apply_event(event)
        
        return event["id"]
    
    def _apply_event(self, event):
        """Apply event to update current state"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["object"]
        
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["new_object"]
        
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            self.state.pop(key, None)
        
        elif etype == "set_profile":
            self.state[("profile", data["user_id"])] = data["attributes"]
    
    def get_state(self):
        """Get current state"""
        return dict(self.state)
    
    def get_state_at(self, event_id):
        """Get state at a specific point in time (time travel)"""
        state = {}
        for event in self.events[:event_id + 1]:
            self._apply_event_to(state, event)
        return state
    
    def _apply_event_to(self, state, event):
        """Apply event to a specific state dict"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["object"]
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["new_object"]
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            state.pop(key, None)
    
    def get_event_history(self, event_type=None):
        """Get event history, optionally filtered by type"""
        if event_type:
            return [e for e in self.events if e["type"] == event_type]
        return list(self.events)
    
    def undo_last(self):
        """Undo the last event"""
        if not self.events:
            return None
        
        event = self.events.pop()
        # Rebuild state from remaining events
        self.state = {}
        for e in self.events:
            self._apply_event(e)
        
        return event
