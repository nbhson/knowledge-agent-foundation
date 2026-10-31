class ClaudeToolPermissions {
  // Each tool has its own permissions
  toolPermissions = {
    'read_file': {
      allowedPaths: ['/workspace/**'],
      deniedPaths: ['/workspace/.env', '/workspace/secrets/**'],
      requireApproval: false
    },
    
    'write_file': {
      allowedPaths: ['/workspace/src/**', '/workspace/test/**'],
      deniedPaths: ['/workspace/config/**'],
      requireApproval: true, // Requires user confirmation
      maxFileSize: 100000 // 100KB
    },
    
    'execute_command': {
      allowedCommands: ['npm', 'git', 'python', 'node'],
      deniedCommands: ['rm -rf', 'sudo', 'chmod'],
      requireApproval: true,
      timeout: 30000 // 30s
    },
    
    'web_search': {
      allowedDomains: ['github.com', 'stackoverflow.com', 'docs.*'],
      rateLimitperHour: 50
    }
  };
  
  async checkPermission(tool: string, params: any): Promise<PermissionResult> {
    const perm = this.toolPermissions[tool];
    
    // Check path restrictions
    if (tool.includes('file')) {
      if (!this.isPathAllowed(params.path, perm)) {
        return { allowed: false, reason: 'Path not allowed' };
      }
    }
    
    // Check if approval is needed
    if (perm.requireApproval) {
      const approved = await this.requestUserApproval(tool, params);
      if (!approved) {
        return { allowed: false, reason: 'User denied' };
      }
    }
    
    return { allowed: true };
  }
}
