// Tool Decision System — Full Harness Integration
interface ToolDecisionSystem {
  // Tool management
  registerTool: (tool: ToolDefinition) => void;
  getTool: (name: string) => ToolDefinition | null;
  listTools: (category?: string) => ToolDefinition[];
  searchTools: (query: string) => ToolDefinition[];
  
  // Classification
  classifyIntent: (query: string) => IntentResult;
  
  // Execution
  executeTool: (name: string, params: Record<string, any>, userId?: string) => ToolResult;
  executeChain: (steps: ToolChainStep[]) => ChainResult;
  executeParallel: (calls: ToolCall[]) => ParallelResult;
  
  // Guardrails
  checkPermission: (userId: string, permission: string) => boolean;
  checkRateLimit: (toolName: string) => boolean;
  
  // Metrics
  getStats: () => ToolStats;
}

interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, ParameterDef>;
  category: string;
  version: string;
  requiresAuth: boolean;
  requiresPermission: string;
  rateLimitPerMinute: number;
  timeoutSeconds: number;
  maxRetries: number;
  costPerCall: number;
}

interface ToolResult {
  success: boolean;
  result?: any;
  error?: string;
  attempts: number;
  elapsedMs: number;
  cost: number;
}

interface IntentResult {
  intent: string;
  tools: string[];
  confidence: number;
  method: string;
}

// Complete Harness Tool Decision System
class HarnessToolDecisionSystem implements ToolDecisionSystem {
  private registry: ToolRegistry;
  private classifier: IntentClassifier;
  private executor: ToolExecutor;
  private permissionChecker: ToolPermissionChecker;
  private rateLimiter: RateLimiter;
  private metricsCollector: MetricsCollector;
  
  constructor(config: HarnessConfig) {
    this.registry = new ToolRegistry();
    this.classifier = new IntentClassifier(config.llm);
    this.executor = new ToolExecutor(this.registry);
    this.permissionChecker = new ToolPermissionChecker();
    this.rateLimiter = new RateLimiter();
    this.metricsCollector = config.metrics;
  }
  
  async executeTool(name: string, params: Record<string, any>, userId?: string): Promise<ToolResult> {
    // 1. Check permission
    const tool = this.registry.getTool(name);
    if (tool && userId) {
      const permCheck = this.permissionChecker.check(userId, tool.requiresPermission);
      if (!permCheck.allowed) {
        return { success: false, error: permCheck.reason, attempts: 0, elapsedMs: 0, cost: 0 };
      }
    }
    
    // 2. Check rate limit
    const rateCheck = this.rateLimiter.check(name);
    if (!rateCheck.allowed) {
      return { success: false, error: `Rate limited. Retry after ${rateCheck.retryAfter}s`, attempts: 0, elapsedMs: 0, cost: 0 };
    }
    
    // 3. Execute with tracking
    const result = this.executor.execute(name, params, userId);
    
    // 4. Report metrics
    this.metricsCollector.track('tool_executed', {
      tool: name,
      success: result.success,
      latency_ms: result.elapsed_ms,
    });
    
    return result;
  }
  
  // ... other interface implementations
}
