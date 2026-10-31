role = self.user_roles.get(user_id, "guest")   # never skip the check
allowed = required_permission in set(
    self.ROLE_PERMISSIONS.get(role, ["public"]) + custom_perms)
