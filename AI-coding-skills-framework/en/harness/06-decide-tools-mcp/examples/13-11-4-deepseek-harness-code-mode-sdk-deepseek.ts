/**
 * DeepSeek Harness - Code Mode SDK
 * 
 * Core philosophy: "Batch everything, execute once"
 * Single-turn script execution instead of multi-turn agent loop.
 * 
 * Package: @deepseek-ai/dsh
 * Runtime: Node.js vm sandbox (isolated, no network)
 */

// ═══════════════════════════════════════════════
// 1. CODE MODE SDK INTERFACE
// ═══════════════════════════════════════════════

interface CodeModeConfig {
  /** Maximum execution time in milliseconds */
  timeoutMs: number;
  
  /** Allow network access (default: false for isolation) */
  allowNetwork: boolean;
  
  /** Allowed built-in modules */
  allowedModules: string[];
  
  /** Custom globals injected into sandbox */
  globals: Record<string, any>;
  
  /** Tool batching configuration */
  batching: {
    /** Batch multiple tool calls into single execution */
    enabled: boolean;
    /** Max tools per batch */
    maxBatchSize: number;
    /** Max wait time for batching (ms) */
    maxWaitMs: number;
  };
  
  /** Memory limit (MB) */
  memoryLimitMb: number;
}

interface ToolBatch {
  calls: ToolCall[];
  sessionId: string;
  timestamp: number;
}

interface ToolCall {
  id: string;
  name: string;
  args: Record<string, any>;
  /** For batched execution: resolve all at once */
  resolve: (result: any) => void;
  reject: (error: Error) => void;
}

// ═══════════════════════════════════════════════
// 2. SANDBOX EXECUTOR (vm-based isolation)
// ═══════════════════════════════════════════════

class CodeModeSandbox {
  private vm: import('vm').Context;
  private config: CodeModeConfig;
  private toolRegistry: Map<string, ToolFunction>;
  private batchQueue: ToolCall[] = [];
  private batchTimer: NodeJS.Timeout | null = null;
  
  constructor(config: Partial<CodeModeConfig> = {}) {
    this.config = {
      timeoutMs: 30000,
      allowNetwork: false,
      allowedModules: ['fs', 'path', 'crypto', 'util'],
      globals: {},
      batching: { enabled: true, maxBatchSize: 10, maxWaitMs: 50 },
      memoryLimitMb: 128,
      ...config
    };
    
    this.toolRegistry = new Map();
    this.setupSandbox();
  }
  
  private setupSandbox(): void {
    // Create isolated vm context
    const sandboxGlobals = {
      console: this.createSafeConsole(),
      setTimeout,
      clearTimeout,
      setInterval,
      clearInterval,
      ...this.config.globals
    };
    
    // Add allowed modules
    for (const mod of this.config.allowedModules) {
      try {
        sandboxGlobals[mod] = require(mod);
      } catch {
        // Module not available
      }
    }
    
    // Inject tool caller
    sandboxGlobals.callTool = this.createToolCaller();
    sandboxGlobals.batchTools = this.createBatchCaller();
    
    this.vm = import('vm').createContext(sandboxGlobals);
  }
  
  private createSafeConsole() {
    return {
      log: (...args: any[]) => { /* captured */ },
      error: (...args: any[]) => { /* captured */ },
      warn: (...args: any[]) => { /* captured */ },
    };
  }
  
  private createToolCaller() {
    return async (name: string, args: Record<string, any>) => {
      const tool = this.toolRegistry.get(name);
      if (!tool) throw new Error(`Tool not found: ${name}`);
      return await tool(args);
    };
  }
  
  private createBatchCaller() {
    return (calls: Array<{name: string, args: Record<string, any>}>) => {
      return this.executeBatch(calls);
    };
  }
  
  registerTool(name: string, fn: ToolFunction): void {
    this.toolRegistry.set(name, fn);
  }
  
  // ═══════════════════════════════════════════════
  // 3. BATCHED EXECUTION (Core optimization)
  // ═══════════════════════════════════════════════
  
  async executeScript(script: string): Promise<ExecutionResult> {
    const startTime = Date.now();
    const scriptId = `script_${startTime}_${Math.random().toString(36).slice(2)}`;
    
    // Wrap script with error handling and result capture
    const wrappedScript = `
      (async () => {
        try {
          const result = await (async () => {
            ${script}
          })();
          return { success: true, result, scriptId: "${scriptId}" };
        } catch (error) {
          return { success: false, error: error.message, stack: error.stack, scriptId: "${scriptId}" };
        }
      })()
    `;
    
    try {
      const result = await import('vm').runInContext(wrappedScript, this.vm, {
        timeout: this.config.timeoutMs,
        displayErrors: true
      });
      
      // Flush any pending batch
      await this.flushBatch();
      
      return {
        success: result.success,
        result: result.success ? result.result : undefined,
        error: result.success ? undefined : result.error,
        durationMs: Date.now() - startTime,
        scriptId
      };
      
    } catch (error: any) {
      return {
        success: false,
        error: error.message,
        durationMs: Date.now() - startTime,
        scriptId
      };
    }
  }
  
  private async executeBatch(calls: Array<{name: string, args: any}>): Promise<any[]> {
    if (!this.config.batching.enabled) {
      // Sequential fallback
      return Promise.all(calls.map(c => this.callTool(c.name, c.args)));
    }
    
    // Queue for batching
    const promises = calls.map(call => new Promise((resolve, reject) => {
      this.batchQueue.push({
        id: uuid(),
        name: call.name,
        args: call.args,
        resolve,
        reject
      });
    }));
    
    // Schedule flush
    if (this.batchTimer) clearTimeout(this.batchTimer);
    this.batchTimer = setTimeout(() => this.flushBatch(), this.config.batching.maxWaitMs);
    
    // Flush immediately if batch full
    if (this.batchQueue.length >= this.config.batching.maxBatchSize) {
      await this.flushBatch();
    }
    
    return Promise.all(promises);
  }
  
  private async flushBatch(): Promise<void> {
    if (this.batchQueue.length === 0) return;
    
    const batch = this.batchQueue.splice(0, this.config.batching.maxBatchSize);
    if (this.batchTimer) {
      clearTimeout(this.batchTimer);
      this.batchTimer = null;
    }
    
    // Execute all tools in parallel
    const results = await Promise.allSettled(
      batch.map(async call => {
        const tool = this.toolRegistry.get(call.name);
        if (!tool) throw new Error(`Tool not found: ${call.name}`);
        return await tool(call.args);
      })
    );
    
    // Resolve/reject promises
    for (let i = 0; i < batch.length; i++) {
      const call = batch[i];
      const result = results[i];
      if (result.status === 'fulfilled') {
        call.resolve(result.value);
      } else {
        call.reject(result.reason);
      }
    }
  }
  
  async callTool(name: string, args: Record<string, any>): Promise<any> {
    const tool = this.toolRegistry.get(name);
    if (!tool) throw new Error(`Tool not found: ${name}`);
    return await tool(args);
  }
}

// ═══════════════════════════════════════════════
// 4. HIGH-LEVEL SDK API (@deepseek-ai/dsh)
// ═══════════════════════════════════════════════

class DeepSeekHarnessSDK {
  private sandbox: CodeModeSandbox;
  private sessionId: string;
  
  constructor(config?: Partial<CodeModeConfig>) {
    this.sandbox = new CodeModeSandbox(config);
    this.sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2)}`;
    this.registerDefaultTools();
  }
  
  private registerDefaultTools(): void {
    // File operations
    this.sandbox.registerTool('read_file', async ({path, encoding = 'utf-8'}) => {
      return await fs.promises.readFile(path, encoding);
    });
    
    this.sandbox.registerTool('write_file', async ({path, content, mode = 'overwrite'}) => {
      if (mode === 'append') {
        await fs.promises.appendFile(path, content);
      } else {
        await fs.promises.writeFile(path, content);
      }
      return { success: true, path };
    });
    
    this.sandbox.registerTool('list_files', async ({path = '.', recursive = false}) => {
      const files = await glob('**/*', { cwd: path, nodir: !recursive });
      return files;
    });
    
    // Code execution
    this.sandbox.registerTool('execute_command', async ({command, cwd, timeout = 30000}) => {
      const { execFile } = require('child_process');
      return new Promise((resolve, reject) => {
        const proc = execFile(command, { cwd, timeout }, (err, stdout, stderr) => {
          if (err) reject(err);
          else resolve({ stdout, stderr, code: 0 });
        });
      });
    });
    
    // Search
    this.sandbox.registerTool('search_code', async ({query, path = '.', filePattern}) => {
      // Use ripgrep or similar
      const results = await ripgrep(query, { path, filePattern });
      return results;
    });
    
    // LLM call (for code generation within script)
    this.sandbox.registerTool('llm_complete', async ({prompt, model = 'deepseek-coder'}) => {
      const response = await callLLM(prompt, model);
      return response;
    });
  }
  
  /**
   * Main entry point: Execute a coding task in single turn
   * 
   * Example:
   * ```typescript
   * const sdk = new DeepSeekHarnessSDK();
   * const result = await sdk.execute(`
   *   const files = await list_files({path: './src'});
   *   const content = await read_file({path: files[0]});
   *   const fixed = await llm_complete({prompt: \`Fix bugs in: \${content}\`});
   *   await write_file({path: files[0], content: fixed});
   * `);
   * ```
   */
  async execute(script: string): Promise<ExecutionResult> {
    return await this.sandbox.executeScript(script);
  }
  
  /**
   * Execute with pre-defined tools (for structured tasks)
   */
  async executeWithTools(
    script: string, 
    tools: Record<string, ToolFunction>
  ): Promise<ExecutionResult> {
    for (const [name, fn] of Object.entries(tools)) {
      this.sandbox.registerTool(name, fn);
    }
    return await this.execute(script);
  }
  
  /**
   * Get session metrics
   */
  getMetrics(): SessionMetrics {
    return {
      sessionId: this.sessionId,
      toolsRegistered: this.sandbox.toolRegistry.size,
      // ... more metrics
    };
  }
}

// ═══════════════════════════════════════════════
// 5. USAGE EXAMPLES
// ═══════════════════════════════════════════════

/**
 * Example 1: Refactor a TypeScript file
 */
async function exampleRefactor() {
  const sdk = new DeepSeekHarnessSDK({
    timeoutMs: 60000,
    allowedModules: ['fs', 'path', 'typescript'],
    batching: { enabled: true, maxBatchSize: 20, maxWaitMs: 100 }
  });
  
  const result = await sdk.execute(`
    // 1. Find all TS files
    const files = await list_files({path: './src', recursive: true});
    const tsFiles = files.filter(f => f.endsWith('.ts'));
    
    // 2. Read all files in parallel (BATCHED!)
    const contents = await batchTools(
      tsFiles.map(f => ({name: 'read_file', args: {path: f}}))
    );
    
    // 3. Analyze with LLM (single call)
    const analysis = await llm_complete({
      prompt: \`Analyze these files for code smells:\n\${contents.map((c,i) => \`// \${tsFiles[i]}\n\${c}\`).join('\n\n')}\`
    });
    
    // 4. Apply fixes (batched writes)
    const fixes = JSON.parse(analysis);
    await batchTools(
      fixes.map(f => ({name: 'write_file', args: {path: f.path, content: f.fixedCode}}))
    );
    
    return { fixed: fixes.length, files: tsFiles.length };
  `);
  
  console.log(result); // { success: true, result: { fixed: 5, files: 12 }, durationMs: 2340 }
}

/**
 * Example 2: Run tests and fix failures
 */
async function exampleTestFix() {
  const sdk = new DeepSeekHarnessSDK();
  
  const result = await sdk.execute(`
    // Run tests
    const testResult = await execute_command({
      command: 'npm test',
      cwd: '.'
    });
    
    if (testResult.code !== 0) {
      // Parse failures
      const failures = parseTestFailures(testResult.stdout);
      
      // For each failure, read file and fix
      for (const fail of failures) {
        const content = await read_file({path: fail.file});
        const fixed = await llm_complete({
          prompt: \`Fix this test failure:\nFile: \${fail.file}\nError: \${fail.error}\nCode:\n\${content}\`
        });
        await write_file({path: fail.file, content: fixed});
      }
      
      // Re-run tests
      const retry = await execute_command({command: 'npm test'});
      return { fixed: failures.length, passed: retry.code === 0 };
    }
    
    return { fixed: 0, passed: true };
  `);
  
  return result;
}

/**
 * Example 3: Code generation from spec
 */
async function exampleCodeGen() {
  const sdk = new DeepSeekHarnessSDK({
    globals: { SPEC: loadSpec('./spec.yaml') }
  });
  
  return await sdk.execute(`
    // Generate API routes from OpenAPI spec
    const routes = generateRoutes(SPEC);
    
    // Write all files in one batch
    await batchTools(
      routes.map(r => ({name: 'write_file', args: r}))
    );
    
    // Run linter
    await execute_command({command: 'npm run lint'});
    
    return { generated: routes.length };
  `);
}

interface ToolFunction {
  (args: Record<string, any>): Promise<any>;
}

interface ExecutionResult {
  success: boolean;
  result?: any;
  error?: string;
  durationMs: number;
  scriptId: string;
}

interface SessionMetrics {
  sessionId: string;
  toolsRegistered: number;
  totalExecutions: number;
  totalDurationMs: number;
  avgDurationMs: number;
  batchedCalls: number;
  estimatedTokenSavings: number;
}

function uuid(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
