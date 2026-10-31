// ═══════════════════════════════════════════════════════════════
// AUTOMATION TYPES — Production-grade interfaces cho automation systems
// ═══════════════════════════════════════════════════════════════

/**
 * Pipeline configuration — How an automation pipeline is structured
 */
interface PipelineConfig {
  name: string;
  description: string;
  version: string;
  steps: PipelineStepConfig[];
  triggers: TriggerConfig[];
  gates: QualityGateConfig[];
  notifications: NotificationConfig;
  settings: PipelineSettings;
}

interface PipelineStepConfig {
  id: string;
  name: string;
  type: 'build' | 'test' | 'deploy' | 'security' | 'custom';
  handler: string;  // function reference or module path
  timeout: number;  // milliseconds
  retries: number;
  retryDelay: number;
  rollback?: string;
  dependencies: string[];  // step IDs this depends on
  condition?: StepCondition;
  artifacts?: ArtifactConfig[];
}

interface TriggerConfig {
  type: 'push' | 'pull_request' | 'schedule' | 'webhook' | 'manual';
  branches?: string[];
  paths?: string[];
  schedule?: string;  // cron expression
  webhookUrl?: string;
  events?: string[];
}

interface QualityGateConfig {
  name: string;
  type: 'coverage' | 'complexity' | 'security' | 'performance' | 'custom';
  threshold: number;
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq';
  failPipeline: boolean;
  description: string;
}

interface PipelineSettings {
  parallel: boolean;
  maxConcurrency: number;
  timeout: number;  // overall pipeline timeout
  allowFailure: boolean;
  cacheEnabled: boolean;
  cacheStrategy: 'none' | 'dependencies' | 'full';
  environment: Record<string, string>;
}

/**
 * Execution tracking — Monitor pipeline runs
 */
interface PipelineRun {
  id: string;
  pipelineId: string;
  status: 'pending' | 'running' | 'success' | 'failed' | 'cancelled' | 'timeout';
  trigger: TriggerConfig;
  steps: StepRun[];
  startedAt: string;
  finishedAt?: string;
  duration?: number;
  triggeredBy: string;
  metadata: Record<string, any>;
}

interface StepRun {
  stepId: string;
  status: 'pending' | 'running' | 'success' | 'failed' | 'skipped' | 'timeout';
  startedAt?: string;
  finishedAt?: string;
  duration?: number;
  output?: string;
  error?: string;
  artifacts: string[];
  retryCount: number;
}

/**
 * Monitoring types
 */
interface MetricDefinition {
  name: string;
  type: 'counter' | 'gauge' | 'histogram' | 'summary';
  description: string;
  labels: string[];
  buckets?: number[];  // for histogram
}

interface AlertConfig {
  name: string;
  metric: string;
  condition: 'gt' | 'lt' | 'eq' | 'ne';
  threshold: number;
  duration: string;  // e.g., "5m" for 5 minutes
  severity: 'info' | 'warning' | 'critical' | 'page';
  channels: string[];
  runbook?: string;
}

/**
 * Self-healing types
 */
interface SelfHealingConfig {
  healthCheck: HealthCheckConfig;
  autoRestart: AutoRestartConfig;
  circuitBreaker: CircuitBreakerConfig;
  rateLimit: RateLimitConfig;
}

interface HealthCheckConfig {
  endpoint: string;
  interval: number;
  timeout: number;
  unhealthyThreshold: number;
  healthyThreshold: number;
}

interface AutoRestartConfig {
  enabled: boolean;
  maxRestarts: number;
  restartWindow: number;  // ms — window for counting restarts
  backoff: 'linear' | 'exponential';
  maxBackoff: number;
}

interface CircuitBreakerConfig {
  enabled: boolean;
  failureThreshold: number;
  successThreshold: number;
  timeout: number;  // ms — time to wait before half-open
}

interface RateLimitConfig {
  enabled: boolean;
  maxRequests: number;
  windowMs: number;
  strategy: 'sliding' | 'fixed';
}

// ═══════════════════════════════════════════════════════════════
// GUARDRAILS — Safety patterns cho AI automation
// ═══════════════════════════════════════════════════════════════

interface GuardrailConfig {
  /** Maximum number of AI-generated files per task */
  maxFilesPerTask: number;
  /** Maximum lines of code per AI generation */
  maxLinesPerGeneration: number;
  /** Require human approval for production deploys */
  requireApprovalForProduction: boolean;
  /** Allowed file extensions for AI modification */
  allowedFileExtensions: string[];
  /** Blocked paths that AI cannot modify */
  blockedPaths: string[];
  /** Maximum token budget per automation run */
  maxTokenBudget: number;
  /** Rollback policy on failure */
  rollbackPolicy: 'auto' | 'manual' | 'never';
  /** Maximum retries before escalation */
  maxRetriesBeforeEscalation: number;
}

interface DeploymentGuardrails {
  /** Maximum change size in lines */
  maxChangeSize: number;
  /** Require test coverage for changed files */
  requireTestCoverage: boolean;
  /** Minimum test coverage threshold */
  minTestCoverage: number;
  /** Require security scan */
  requireSecurityScan: boolean;
  /** Blocked paths for auto-deploy */
  blockedDeployPaths: string[];
  /** Environment-specific restrictions */
  environmentRestrictions: Record<string, DeploymentRestriction>;
}

interface DeploymentRestriction {
  requireApproval: boolean;
  approvers: string[];
  allowedHours?: { start: number; end: number };
  allowedDays?: number[];  // 0=Sunday, 6=Saturday
  maxDeployFrequency?: number;  // per hour
}
