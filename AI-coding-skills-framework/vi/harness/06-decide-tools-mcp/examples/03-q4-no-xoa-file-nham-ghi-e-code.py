role = self.user_roles.get(user_id, "guest")
perms = set(ROLE_PERMISSIONS.get(role, ["public"]) + custom.get(user_id, []))
return {"allowed": required_permission in perms}
