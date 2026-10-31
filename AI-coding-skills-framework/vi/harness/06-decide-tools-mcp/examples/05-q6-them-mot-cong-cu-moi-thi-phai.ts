interface ToolDefinition {
  name: string; description: string;
  parameters: Record<string, ParameterDef>;
  requiresPermission: string;
  rateLimitPerMinute: number; timeoutSeconds: number;
  maxRetries: number; costPerCall: number;
}
