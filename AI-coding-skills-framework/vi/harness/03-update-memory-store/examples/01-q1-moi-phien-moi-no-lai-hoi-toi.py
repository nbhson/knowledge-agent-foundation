profile = self.entity_store.get(f"user_{user_id}", {"attributes": {}})
profile["attributes"].update({"occupation": "freelancer", "location": "HCM"})
self._log_event("update_profile", {"user_id": user_id, "updates": updates})
