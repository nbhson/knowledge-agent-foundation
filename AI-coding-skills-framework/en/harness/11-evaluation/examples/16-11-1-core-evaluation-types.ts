// ═══════════════════════════════════════════════════════════════
// EVALUATION TYPES — Production-grade interfaces for evaluation systems
// ═══════════════════════════════════════════════════════════════

/**
 * Benchmark definition — How to structure an evaluation benchmark
 */
interface BenchmarkConfig {
  name: string;
  description: string;
  version: string;
  tasks: BenchmarkTask[];
  metrics: MetricDefinition[];
  settings: BenchmarkSettings;
}

interface BenchmarkTask {
  id: string;
  name: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  category: string;
  input: TaskInput;
  expectedOutput?: TaskOutput;
  testCases: TestCase[];
  timeout: number;        // ms
  tokenBudget?: number;   // max tokens
}

interface TaskInput {
  prompt: string;
  context?: string;
  files?: FileReference[];
  language?: string;
}

interface TaskOutput {
  code: string;
  explanation?: string;
  filesModified?: string[];
}

interface TestCase {
  id: string;
  name: string;
  input: any;
  expectedOutput: any;
  type: 'unit' | 'integration' | 'e2e' | 'edge_case';
  weight: number;  // 0-1, importance in scoring
}

interface BenchmarkSettings {
  maxRetries: number;
  timeoutPerTask: number;       // ms
  tokenBudgetPerTask: number;
  parallelism: number;
  temperature: number;
  randomSeed?: number;
  modelConfig: ModelConfig;
}

interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'ollama' | 'custom';
  model: string;
  maxTokens: number;
  temperature: number;
  topP?: number;
}

/**
 * Evaluation results
 */
interface EvaluationResult {
  benchmarkName: string;
  model: string;
  timestamp: string;
  summary: EvaluationSummary;
  taskResults: TaskResult[];
  metrics: Record<string, number>;
  cost: CostBreakdown;
}

interface EvaluationSummary {
  totalTasks: number;
  passed: number;
  failed: number;
  errored: number;
  passRate: number;
  avgScore: number;
  avgDuration: number;
  avgTokens: number;
  totalTokens: number;
  totalCost: number;
}

interface TaskResult {
  taskId: string;
  status: 'passed' | 'failed' | 'error' | 'timeout';
  score: number;           // 0-1
  duration: number;        // ms
  tokensUsed: number;
  output?: string;
  error?: string;
  testResults: TestCaseResult[];
}

interface TestCaseResult {
  testCaseId: string;
  passed: boolean;
  actual: any;
  expected: any;
  duration: number;
}

interface CostBreakdown {
  inputTokens: number;
  outputTokens: number;
  inputCost: number;
  outputCost: number;
  totalCost: number;
  costPerTask: number;
  costPerPassingTask: number;
}

/**
 * Quality metrics
 */
interface QualityMetrics {
  correctness: CorrectnessMetrics;
  efficiency: EfficiencyMetrics;
  safety: SafetyMetrics;
  maintainability: MaintainabilityMetrics;
}

interface CorrectnessMetrics {
  passRate: number;
  edgeCaseHandling: number;
  errorHandling: number;
  regressionRate: number;
}

interface EfficiencyMetrics {
  timeComplexity: string;      // e.g., "O(n log n)"
  memoryUsage: number;         // bytes
  tokenEfficiency: number;     // tokens per correct answer
  responseTime: number;        // ms
}

interface SafetyMetrics {
  securityScore: number;       // 0-100
  vulnerabilityCount: number;
  inputValidationScore: number;
  dataLeakage: boolean;
}

interface MaintainabilityMetrics {
  codeComplexity: number;      // cyclomatic complexity
  documentationCoverage: number;  // %
  testCoverage: number;        // %
  duplicationRatio: number;    // 0-1
}

/**
 * Continuous improvement tracking
 */
interface ImprovementTracking {
  version: string;
  timestamp: string;
  previousVersion?: string;
  metrics: Record<string, number>;
  regressions: Regression[];
  improvements: Improvement[];
}

interface Regression {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

interface Improvement {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

/**
 * A/B Testing
 */
interface ABTestConfig {
  name: string;
  variants: Variant[];
  sampleSize: number;
  significanceLevel: number;  // typically 0.05
  metrics: string[];
}

interface Variant {
  id: string;
  name: string;
  description: string;
  config: ModelConfig;
  promptTemplate?: string;
  weight: number;  // traffic split (0-1)
}

interface ABTestResult {
  config: ABTestConfig;
  results: VariantResult[];
  winner?: string;
  pValue: number;
  significant: boolean;
}

interface VariantResult {
  variantId: string;
  sampleSize: number;
  metrics: Record<string, number>;
  confidenceInterval: [number, number];
}

/**
 * Harness quality evaluation — Evaluating the evaluation itself
 */
interface HarnessQualityMetrics {
  /** How well does the benchmark correlate with human judgment? */
  humanCorrelation: number;  // 0-1, Pearson correlation
  /** Are benchmark scores stable across runs? */
  testRetestReliability: number;  // 0-1
  /** Does the benchmark discriminate between good and bad? */
  discriminativePower: number;  // 0-1
  /** How much does it cost to run? */
  costPerRun: number;
  /** How long does a full evaluation take? */
  durationMinutes: number;
  /** Coverage of task types and difficulties */
  coverageScore: number;  // 0-1
}
