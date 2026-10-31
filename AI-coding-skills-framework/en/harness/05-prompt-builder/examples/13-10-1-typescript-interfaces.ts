// Prompt Builder System — Full Harness Integration
interface PromptBuilderSystem {
  // Template management
  render: (name: string, variables: Record<string, any>, version?: string) => string;
  validate: (name: string, variables: Record<string, any>) => ValidationResult;
  
  // Few-shot management
  selectExamples: (query: string, k: number, strategy: string) => FewShotExample[];
  
  // Guardrails
  filterInput: (input: string) => SafetyCheck;
  validateOutput: (output: string, format?: string) => ValidationCheck;
  
  // Versioning
  createVersion: (name: string, template: string) => PromptVersion;
  rollback: (name: string, version: string) => boolean;
  
  // A/B Testing
  startTest: (name: string, variants: PromptVariant[]) => void;
  getTestResults: (name: string) => ABTestResults;
  
  // Optimization
  optimize: (template: string, feedback: FeedbackData) => string;
  evaluate: (template: string, testCases: TestCase[]) => EvaluationResult;
}

interface ValidationResult {
  valid: boolean;
  missing: string[];
  extra: string[];
  coverage: string;
}

interface SafetyCheck {
  safe: boolean;
  reason?: string;
  sanitizedInput?: string;
}

interface ValidationCheck {
  valid: boolean;
  issues: string[];
  output?: any;
}

interface PromptVersion {
  version: string;
  template: string;
  createdAt: string;
  metrics: PromptMetrics;
}

interface PromptMetrics {
  totalCalls: number;
  avgTokens: number;
  avgLatency: number;
  successRate: number;
  avgQuality: number;
}

// Complete Harness Prompt Builder
class HarnessPromptBuilder implements PromptBuilderSystem {
  private registry: PromptRegistry;
  private guardrails: PromptGuardrails;
  private versionManager: Map<string, PromptVersionManager>;
  private abTests: Map<string, PromptABTest>;
  private metricsCollector: MetricsCollector;
  
  constructor(config: HarnessConfig) {
    this.registry = new PromptRegistry();
    this.guardrails = new PromptGuardrails();
    this.versionManager = new Map();
    this.abTests = new Map();
    this.metricsCollector = config.metrics;
  }
  
  async render(name: string, variables: Record<string, any>, version?: string): Promise<string> {
    // 1. Guardrails: filter input
    for (const [key, value] of Object.entries(variables)) {
      if (typeof value === 'string') {
        const safety = this.guardrails.filterInput(value);
        if (!safety.safe) {
          throw new Error(`Unsafe input in variable '${key}': ${safety.reason}`);
        }
      }
    }
    
    // 2. Render template
    const template = this.registry.get(name, version || 'latest');
    const rendered = template.render(variables);
    
    // 3. Metrics tracking
    this.metricsCollector.track('prompt_rendered', {
      template: name,
      version: template.version,
      variableCount: Object.keys(variables).length,
    });
    
    return rendered;
  }
  
  validate(name: string, variables: Record<string, any>): ValidationResult {
    const template = this.registry.get(name);
    return template.validate(variables);
  }
  
  // ... other interface implementations
}
