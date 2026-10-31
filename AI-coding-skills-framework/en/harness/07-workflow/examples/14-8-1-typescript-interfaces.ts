// Workflow Engine — Full Harness Integration
interface WorkflowEngine {
  // Workflow management
  createWorkflow: (config: WorkflowConfig) => Workflow;
  getWorkflow: (id: string) => Workflow | null;
  
  // Execution
  execute: (workflowId: string, input: any) => Promise<WorkflowResult>;
  pause: (workflowId: string) => void;
  resume: (workflowId: string) => void;
  cancel: (workflowId: string) => void;
  
  // State management
  getState: (workflowId: string) => WorkflowState;
  getHistory: (workflowId: string) => WorkflowStep[];
  
  // Observability
  getTrace: (workflowId: string) => TraceData;
  getMetrics: (workflowId: string) => WorkflowMetrics;
  
  // Error recovery
  retry: (workflowId: string) => void;
  rollback: (workflowId: string) => void;
}

interface WorkflowConfig {
  name: string;
  steps: WorkflowStepDef[];
  triggers: TriggerDef[];
  errorPolicy: ErrorPolicy;
  timeout: number;
  maxRetries: number;
}

interface WorkflowStepDef {
  name: string;
  type: 'transform' | 'action' | 'condition' | 'parallel' | 'sub_workflow';
  handler: string;
  dependsOn: string[];
  timeout: number;
  retryPolicy: RetryPolicy;
}

interface WorkflowResult {
  success: boolean;
  output: any;
  duration: number;
  stepsExecuted: number;
  errors: WorkflowError[];
  traceId: string;
}

interface WorkflowMetrics {
  totalRuns: number;
  successRate: number;
  avgDuration: number;
  p95Duration: number;
  errorRate: number;
  stepMetrics: Record<string, StepMetrics>;
}

interface StepMetrics {
  runs: number;
  success: number;
  failed: number;
  avgDurationMs: number;
  lastRun: string;
}

// Complete Harness Workflow Engine
class HarnessWorkflowEngine implements WorkflowEngine {
  private workflows: Map<string, Workflow>;
  private tracer: Tracer;
  private metrics: MetricsCollector;
  private logger: WorkflowLogger;
  
  constructor(config: HarnessConfig) {
    this.workflows = new Map();
    this.tracer = new Tracer();
    this.metrics = new MetricsCollector();
    this.logger = new WorkflowLogger('harness');
  }
  
  async execute(workflowId: string, input: any): Promise<WorkflowResult> {
    const traceId = this.tracer.startTrace(`workflow_${workflowId}`);
    
    using span = this.tracer.span('execute', { workflowId });
    
    try {
      const workflow = this.workflows.get(workflowId);
      if (!workflow) throw new Error(`Workflow ${workflowId} not found`);
      
      const startTime = Date.now();
      const output = await workflow.run(input);
      const duration = Date.now() - startTime;
      
      this.metrics.counter('workflow.success');
      this.metrics.histogram('workflow.duration', duration);
      
      return {
        success: true,
        output,
        duration,
        stepsExecuted: workflow.getStepsExecuted(),
        errors: [],
        traceId,
      };
    } catch (error) {
      this.metrics.counter('workflow.error');
      return {
        success: false,
        output: null,
        duration: 0,
        stepsExecuted: 0,
        errors: [{ message: error.message }],
        traceId,
      };
    }
  }
  
  getMetrics(workflowId: string): WorkflowMetrics {
    return this.metrics.getSummary() as WorkflowMetrics;
  }
  
  // ... other interface implementations
}
