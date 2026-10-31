class ToolPermissionChecker:
    """
    Role-Based Access Control (RBAC) for tools
    
    Permission levels:
    - public: Anyone can use
    - standard: Authenticated users
    - elevated: Users with elevated privileges
    - admin: System admin only
    """
    
    ROLE_PERMISSIONS = {
        "guest": ["public"],
        "user": ["public", "standard"],
        "power_user": ["public", "standard", "elevated"],
        "admin": ["public", "standard", "elevated", "admin"],
    }
    
    def __init__(self):
        self.user_roles: Dict[str, str] = {}
        self.custom_permissions: Dict[str, List[str]] = {}
        self.audit_log: List[Dict] = []
    
    def set_user_role(self, user_id: str, role: str):
        """Set role for a user"""
        if role not in self.ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {role}. Valid: {list(self.ROLE_PERMISSIONS.keys())}")
        self.user_roles[user_id] = role
    
    def grant_permission(self, user_id: str, permission: str):
        """Grant additional permission to user"""
        if user_id not in self.custom_permissions:
            self.custom_permissions[user_id] = []
        if permission not in self.custom_permissions[user_id]:
            self.custom_permissions[user_id].append(permission)
    
    def check(self, user_id: str, required_permission: str) -> Dict:
        """Check if user has required permission"""
        role = self.user_roles.get(user_id, "guest")
        role_perms = self.ROLE_PERMISSIONS.get(role, ["public"])
        custom_perms = self.custom_permissions.get(user_id, [])
        
        all_perms = set(role_perms + custom_perms)
        allowed = required_permission in all_perms
        
        # Log audit trail
        self.audit_log.append({
            "user_id": user_id,
            "required_permission": required_permission,
            "user_role": role,
            "allowed": allowed,
            "timestamp": datetime.now().isoformat(),
        })
        
        if allowed:
            return {"allowed": True}
        else:
            return {
                "allowed": False,
                "reason": f"Role '{role}' does not have '{required_permission}' permission",
                "required": required_permission,
                "current_permissions": list(all_perms),
            }
