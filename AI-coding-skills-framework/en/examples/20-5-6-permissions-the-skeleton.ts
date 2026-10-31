interface PermissionSystem {
  // Resource permissions
  resources: {
    files: FilePermissions;
    network: NetworkPermissions;
    system: SystemPermissions;
  };
  
  // Time-based permissions
  temporal: {
    allowedHours: TimeRange[];
    maxDuration: number;
  };
  
  // Context-based permissions
  contextual: {
    requireApproval: (action: Action) => boolean;
    escalationRules: EscalationRule[];
  };
}

interface FilePermissions {
  read: string[];      // Allowed paths to read
  write: string[];     // Allowed paths to write
  delete: string[];    // Allowed paths to delete
  maxFileSize: number; // Max file size in bytes
}
