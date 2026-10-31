/**
 * Minimal Benchmark Harness
 * 
 * Core Philosophy:
 * - "Less is More" — Chỉ 2 tools: bash + editor
 * - Clean isolation — No LLM-powered tools, no search, no memory
 * - Deterministic — Container-based isolation for reproducibility
 * - Unbiased — LLM không thể "cheat" bằng cách dùng tools nâng cao
 * 
 * Repo: DeepSeek Harness (internal)
 * Used for: SWE-bench, LiveCodeBench, custom benchmarks
 */

// ═══════════════════════════════════════════════
// 1. HARNESS ARCHITECTURE
// ═══════════════════════════════════════════════

interface MinimalHarnessConfig {
  // Isolation settings
  isolation: 'container' | 'vm' | 'process';
  containerImage?: string;      // e.g., 'ubuntu:22.04' with dev tools
  workingDir: string;           // Project directory
  
  // Tool restrictions — ONLY these 2
  allowedTools: ['bash', 'editor'];
  
  // Resource limits
  limits: {
    cpuCores: number;
    memoryMB: number;
    diskMB: number;
    timeoutSeconds: number;
    networkAccess: boolean;
  };
  
  // Evaluation settings
  evaluation: {
    suite: string;              // 'swe-bench', 'livecodebench', 'custom'
    dataset: string;            // Path to dataset
    split: 'train' | 'test' | 'dev';
    maxInstances?: number;
  };
  
  // LLM settings (agent under test)
  llm: {
    model: string;
    temperature: number;
    maxTokens: number;
    systemPrompt: string;
  };
}

interface BenchmarkInstance {
  id: string;                   // e.g., 'django__django-12345'
  repo: string;                 // Repository name
  baseCommit: string;           // Commit to start from
  problemStatement: string;     // Issue description
  hints?: string;               // Optional hints
  testPatch: string;            // Tests that should pass after fix
  envSetup?: string;            // Setup commands
}

interface BenchmarkResult {
  instanceId: string;
  status: 'resolved' | 'failed' | 'error' | 'timeout';
  patch?: string;               // Generated patch/diff
  testsPassed: number;
  testsTotal: number;
  executionTimeMs: number;
  tokensUsed: number;
  toolsUsed: string[];          // Should only be ['bash', 'editor']
  errorMessage?: string;
  trajectory: TrajectoryEvent[]; // For debugging
}

// ═══════════════════════════════════════════════
// 2. TWO TOOLS ONLY
// ═══════════════════════════════════════════════

/**
 * Tool 1: BASH
 * Execute shell commands in the container
 */
interface BashTool {
  type: 'bash';
  command: string;              // Shell command to execute
  timeout?: number;             // Override default timeout
  workdir?: string;             // Working directory
}

// Returns:
interface BashResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  durationMs: number;
}

/**
 * Tool 2: EDITOR
 * File operations: read, write, edit
 */
interface EditorTool {
  type: 'editor';
  action: 'read' | 'write' | 'edit' | 'list' | 'grep';
  path: string;                 // File or directory path
  content?: string;             // For write/edit
  oldString?: string;           // For edit
  newString?: string;           // For edit
  pattern?: string;             // For grep
}

// Returns:
interface EditorResult {
  success: boolean;
  content?: string;             // For read
  files?: string[];             // For list
  matches?: GrepMatch[];        // For grep
  error?: string;
}

interface GrepMatch {
  file: string;
  line: number;
  content: string;
}

// ═══════════════════════════════════════════════
// 3. EXECUTION LOOP
// ═══════════════════════════════════════════════

class MinimalBenchmarkHarness {
  private config: MinimalHarnessConfig;
  private container: ContainerRuntime;
  private trajectory: TrajectoryEvent[] = [];
  
  constructor(config: MinimalHarnessConfig) {
    this.config = config;
    this.container = this.createContainer();
  }
  
  async runInstance(instance: BenchmarkInstance): Promise<BenchmarkResult> {
    const startTime = Date.now();
    const tokensUsed = 0;
    const toolsUsed: string[] = [];
    
    try {
      // 1. Setup environment
      await this.setupEnvironment(instance);
      
      // 2. Run agent loop
      const patch = await this.runAgentLoop(instance);
      
      // 3. Apply patch and run tests
      const testResult = await this.runTests(instance, patch);
      
      return {
        instanceId: instance.id,
        status: testResult.allPassed ? 'resolved' : 'failed',
        patch,
        testsPassed: testResult.passed,
        testsTotal: testResult.total,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        trajectory: this.trajectory,
      };
      
    } catch (error) {
      return {
        instanceId: instance.id,
        status: 'error',
        testsPassed: 0,
        testsTotal: 0,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        errorMessage: error.message,
        trajectory: this.trajectory,
      };
    }
  }
  
  private async runAgentLoop(instance: BenchmarkInstance): Promise<string> {
    const messages = [
      { role: 'system', content: this.config.llm.systemPrompt },
      { role: 'user', content: this.formatProblem(instance) },
    ];
    
    let patch = '';
    const maxTurns = 20;
    
    for (let turn = 0; turn < maxTurns; turn++) {
      // Call LLM
      const response = await this.callLLM(messages);
      messages.push({ role: 'assistant', content: response });
      
      // Parse tool calls
      const toolCalls = this.parseToolCalls(response);
      
      if (toolCalls.length === 0) {
        // No tool calls = agent thinks it's done
        patch = this.extractPatch(response);
        break;
      }
      
      // Execute tools (ONLY bash or editor)
      for (const call of toolCalls) {
        if (!['bash', 'editor'].includes(call.type)) {
          throw new Error(`Tool ${call.type} not allowed in minimal harness`);
        }
        
        toolsUsed.push(call.type);
        
        const result = await this.executeTool(call);
        
        // Record trajectory
        this.trajectory.push({
          turn,
          type: 'tool-call',
          tool: call.type,
          input: call,
          output: result,
          timestamp: Date.now(),
        });
        
        // Add result to messages
        messages.push({
          role: 'tool',
          tool_call_id: call.id,
          content: JSON.stringify(result),
        });
      }
    }
    
    return patch;
  }
  
  private async executeTool(call: ToolCall): Promise<any> {
    switch (call.type) {
      case 'bash':
        return await this.container.exec(call.command, {
          timeout: call.timeout || this.config.limits.timeoutSeconds * 1000,
          workdir: call.workdir || this.config.workingDir,
        });
      
      case 'editor':
        return await this.container.fileOp(call);
      
      default:
        throw new Error(`Unknown tool: ${call.type}`);
    }
  }
  
  private formatProblem(instance: BenchmarkInstance): string {
    return `## Repository: ${instance.repo}
## Base Commit: ${instance.baseCommit}

## Problem Statement:
${instance.problemStatement}

${instance.hints ? `## Hints:\n${instance.hints}` : ''}

## Task:
Fix the issue described above. You have access to ONLY two tools:
1. **bash** - Execute shell commands
2. **editor** - Read, write, edit, list, or grep files

Your goal is to produce a patch that makes the tests pass.
Explore the codebase first, then implement the fix.

Output format:
1. Use tools to explore and fix
2. When done, provide the final patch in unified diff format`;
  }
}

// ═══════════════════════════════════════════════
// 4. CONTAINER RUNTIME
// ═══════════════════════════════════════════════

interface ContainerRuntime {
  // Lifecycle
  start(): Promise<void>;
  stop(): Promise<void>;
  snapshot(): Promise<string>;    // For fork/resume
  restore(snapshotId: string): Promise<void>;
  
  // Execution
  exec(command: string, options: ExecOptions): Promise<BashResult>;
  fileOp(op: EditorTool): Promise<EditorResult>;
  
  // State
  getFiles(pattern?: string): Promise<string[]>;
  readFile(path: string): Promise<string>;
  writeFile(path: string, content: string): Promise<void>;
}

// Implementation using Docker/Podman
class DockerContainerRuntime implements ContainerRuntime {
  private containerId: string;
  private image: string;
  
  constructor(image: string = 'ubuntu:22.04') {
    this.image = image;
  }
  
  async start(): Promise<void> {
    // docker run -d --cpus=2 --memory=4g --network=none \
    //   -v ${workspace}:/workspace -w /workspace \
    //   ${image} sleep infinity
    this.containerId = await this.dockerRun();
  }
  
  async exec(command: string, options: ExecOptions): Promise<BashResult> {
    const start = Date.now();
    const result = await this.dockerExec(this.containerId, command, options);
    return {
      ...result,
      durationMs: Date.now() - start,
    };
  }
  
  async fileOp(op: EditorTool): Promise<EditorResult> {
    switch (op.action) {
      case 'read':
        return { success: true, content: await this.readFile(op.path) };
      case 'write':
        await this.writeFile(op.path, op.content || '');
        return { success: true };
      case 'edit':
        // Use sed or similar for in-place edit
        const content = await this.readFile(op.path);
        const newContent = content.replace(op.oldString!, op.newString!);
        await this.writeFile(op.path, newContent);
        return { success: true };
      case 'list':
        const files = await this.getFiles(op.path);
        return { success: true, files };
      case 'grep':
        const matches = await this.grep(op.pattern!, op.path);
        return { success: true, matches };
    }
  }
}

// ═══════════════════════════════════════════════
// 5. TRAJECTORY TRACKING
// ═══════════════════════════════════════════════

interface TrajectoryEvent {
  turn: number;
  type: 'tool-call' | 'llm-response' | 'error' | 'test-run';
  tool?: string;
  input?: any;
  output?: any;
  timestamp: number;
}

interface TestResult {
  allPassed: boolean;
  passed: number;
  total: number;
  details: TestDetail[];
}

interface TestDetail {
  name: string;
  status: 'passed' | 'failed' | 'skipped';
  durationMs: number;
  output?: string;
}

// ═══════════════════════════════════════════════
// 6. SWE-BENCH INTEGRATION
// ═══════════════════════════════════════════════

async function runSWEBenchEvaluation(config: {
  model: string;
  dataset: 'lite' | 'verified' | 'full';
  split: 'test' | 'dev';
  maxInstances?: number;
  parallel?: number;
}): Promise<{
  resolved: number;
  total: number;
  resolveRate: number;
  results: BenchmarkResult[];
}> {
  // Load SWE-bench dataset
  const instances = await loadSWEBenchDataset(config.dataset, config.split);
  const limited = config.maxInstances 
    ? instances.slice(0, config.maxInstances) 
    : instances;
  
  const harness = new MinimalBenchmarkHarness({
    isolation: 'container',
    containerImage: 'swebench/ubuntu:22.04',  // Pre-built with Python, etc.
    workingDir: '/workspace',
    allowedTools: ['bash', 'editor'],
    limits: { cpuCores: 2, memoryMB: 4096, diskMB: 10240, timeoutSeconds: 300, networkAccess: false },
    evaluation: { suite: 'swe-bench', dataset: config.dataset, split: config.split },
    llm: { model: config.model, temperature: 0.0, maxTokens: 8192, systemPrompt: SYSTEM_PROMPT },
  });
  
  // Run in parallel
  const results: BenchmarkResult[] = [];
  const semaphore = new Semaphore(config.parallel || 4);
  
  await Promise.all(limited.map(async (instance) => {
    await semaphore.acquire();
    try {
      const result = await harness.runInstance(instance);
      results.push(result);
    } finally {
      semaphore.release();
    }
  }));
  
  const resolved = results.filter(r => r.status === 'resolved').length;
  
  return {
    resolved,
    total: results.length,
    resolveRate: resolved / results.length,
    results,
  };
}

// System prompt for minimal benchmark
const SYSTEM_PROMPT = `You are an expert software engineer. Your task is to fix bugs in a codebase.

You have access to ONLY two tools:
1. **bash** - Execute shell commands (ls, grep, cat, python, pytest, etc.)
2. **editor** - Read, write, edit, list, or grep files

You do NOT have access to:
- Web search
- Code search across repositories
- LLM-powered tools
- Memory/knowledge bases
- Git operations (except via bash)

Workflow:
1. Explore the codebase to understand the problem
2. Find the relevant files
3. Implement the fix
4. Run tests to verify
5. Output the final patch in unified diff format

Be concise. Use tools efficiently.`;
