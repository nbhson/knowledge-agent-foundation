/**
 * Cordis Micro-Kernel Plugin Engine
 * 
 * Core philosophy: 
 * - "Agent = Model + Harness" — Model provides reasoning, Harness provides tools/workflow
 * - "Everything is a plugin" — all functionality is a plugin
 * - Lightweight kernel: ~2KB gzipped core
 * 
 * Repo: https://github.com/cordisjs/cordis
 * Used by: DeepSeek Harness, Koishi bot framework
 */

// ═══════════════════════════════════════════════
// 1. CORE KERNEL ARCHITECTURE
// ═══════════════════════════════════════════════

interface CordisKernel {
  /** Plugin registry */
  plugins: Map<string, Plugin>;
  
  /** Service registry (dependency injection) */
  services: Map<string, any>;
  
  /** Event bus for inter-plugin communication */
  events: EventEmitter;
  
  /** Lifecycle hooks */
  hooks: {
    init: Hook[];
    attach: Hook[];
    ready: Hook[];
    detach: Hook[];
  };
  
  /** Start kernel and all plugins */
  start(): Promise<void>;
  
  /** Stop kernel gracefully */
  stop(): Promise<void>;
  
  /** Register a plugin */
  plugin(plugin: Plugin | PluginFactory): this;
  
  /** Get service by name */
  getService<T>(name: string): T | undefined;
  
  /** Provide service to registry */
  provide<T>(name: string, service: T): this;
  
  /** Inject service (for plugin constructors) */
  inject<T>(name: string): T | undefined;
}

interface Plugin {
  name: string;
  description?: string;
  version?: string;
  
  /** Dependencies on other plugins */
  requires?: string[];
  
  /** Optional: only load if these plugins are present */
  optional?: string[];
  
  /** Service this plugin provides */
  provides?: string | string[];
  
  /** Service this plugin consumes */
  consumes?: string | string[];
  
  /** Configuration schema */
  config?: Schema;
  
  /** Default config */
  defaultConfig?: any;
  
  /** Lifecycle hooks */
  init?: (ctx: Context) => void | Promise<void>;
  attach?: (ctx: Context) => void | Promise<void>;
  ready?: (ctx: Context) => void | Promise<void>;
  detach?: (ctx: Context) => void | Promise<void>;
}

type PluginFactory = (ctx: Context, config: any) => Plugin | Promise<Plugin>;

// ═══════════════════════════════════════════════
// 2. CONTEXT & DEPENDENCY INJECTION
// ═══════════════════════════════════════════════

class Context {
  private kernel: CordisKernel;
  private plugin: Plugin;
  private services: Map<string, any> = new Map();
  private disposables: (() => void)[] = [];
  
  constructor(kernel: CordisKernel, plugin: Plugin) {
    this.kernel = kernel;
    this.plugin = plugin;
  }
  
  /** Get service from kernel registry */
  get<T>(name: string): T | undefined {
    return this.kernel.getService(name);
  }
  
  /** Provide service to kernel registry */
  provide<T>(name: string, service: T): this {
    this.kernel.provide(name, service);
    this.disposables.push(() => this.kernel.provide(name, undefined));
    return this;
  }
  
  /** Inject service (shorthand for get) */
  inject<T>(name: string): T | undefined {
    return this.get(name);
  }
  
  /** Register disposable for cleanup */
  onDispose(fn: () => void): void {
    this.disposables.push(fn);
  }
  
  /** Dispose all services provided by this plugin */
  dispose(): void {
    for (const fn of this.disposables) {
      fn();
    }
    this.disposables = [];
  }
  
  /** Access plugin config */
  get config(): any {
    return this.kernel.config[this.plugin.name];
  }
  
  /** Access global config */
  get globalConfig(): any {
    return this.kernel.config;
  }
  
  /** Event bus access */
  get event(): EventEmitter {
    return this.kernel.events;
  }
  
  /** Emit event */
  emit(event: string, ...args: any[]): void {
    this.kernel.events.emit(event, ...args);
  }
  
  /** Listen to event */
  on(event: string, listener: (...args: any[]) => void): () => void {
    this.kernel.events.on(event, listener);
    return () => this.kernel.events.off(event, listener);
  }
  
  /** One-time event listener */
  once(event: string, listener: (...args: any[]) => void): void {
    this.kernel.events.once(event, listener);
  }
}

// ═══════════════════════════════════════════════
// 3. LIFECYCLE MANAGEMENT
// ═══════════════════════════════════════════════

/**
 * Plugin Lifecycle:
 * 
 * 1. INIT     — Plugin registered, config validated
 *    ↓
 * 2. ATTACH   — Plugin attaches to kernel, provides/consumes services
 *    ↓
 * 3. READY    — All plugins attached, kernel ready for work
 *    ↓
 * 4. RUNNING  — Kernel processing events, handling requests
 *    ↓
 * 5. DETACH   — Graceful shutdown, cleanup services
 */

class CordisKernelImpl implements CordisKernel {
  plugins = new Map<string, Plugin>();
  services = new Map<string, any>();
  events = new EventEmitter();
  hooks = {
    init: [],
    attach: [],
    ready: [],
    detach: [],
  };
  
  private config: Record<string, any> = {};
  private started = false;
  private pluginOrder: string[] = [];
  
  plugin(plugin: Plugin | PluginFactory): this {
    const instance = typeof plugin === 'function' 
      ? plugin(this.createContext({} as Plugin), plugin.defaultConfig || {})
      : plugin;
    
    // Validate config
    if (instance.config) {
      // Schema validation here
    }
    
    this.plugins.set(instance.name, instance);
    this.config[instance.name] = { ...instance.defaultConfig, ...this.config[instance.name] };
    
    return this;
  }
  
  async start(): Promise<void> {
    if (this.started) return;
    this.started = true;
    
    // Resolve dependency order
    this.pluginOrder = this.resolvePluginOrder();
    
    // Phase 1: INIT
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.init) {
        await plugin.init(ctx);
      }
      this.hooks.init.push({ plugin: name, ctx });
    }
    
    // Phase 2: ATTACH
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      // Inject consumed services
      this.injectConsumedServices(plugin, ctx);
      
      if (plugin.attach) {
        await plugin.attach(ctx);
      }
      this.hooks.attach.push({ plugin: name, ctx });
    }
    
    // Phase 3: READY
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.ready) {
        await plugin.ready(ctx);
      }
      this.hooks.ready.push({ plugin: name, ctx });
    }
    
    this.emit('ready');
  }
  
  async stop(): Promise<void> {
    if (!this.started) return;
    
    // Phase 4: DETACH (reverse order)
    for (const name of [...this.pluginOrder].reverse()) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.detach) {
        await plugin.detach(ctx);
      }
      
      // Dispose context (cleanup provided services)
      ctx.dispose();
      
      this.hooks.detach.push({ plugin: name, ctx });
    }
    
    this.started = false;
    this.emit('stop');
  }
  
  private createContext(plugin: Plugin): Context {
    return new Context(this, plugin);
  }
  
  private injectConsumedServices(plugin: Plugin, ctx: Context): void {
    const consumes = Array.isArray(plugin.consumes) ? plugin.consumes : 
                     plugin.consumes ? [plugin.consumes] : [];
    
    for (const serviceName of consumes) {
      const service = this.services.get(serviceName);
      if (service) {
        // Service available in context
        ctx.provide(serviceName, service);
      }
    }
  }
  
  private resolvePluginOrder(): string[] {
    // Topological sort based on requires/optional
    const visited = new Set<string>();
    const order: string[] = [];
    
    const visit = (name: string) => {
      if (visited.has(name)) return;
      visited.add(name);
      
      const plugin = this.plugins.get(name);
      if (!plugin) return;
      
      const requires = plugin.requires || [];
      for (const dep of requires) {
        visit(dep);
      }
      
      order.push(name);
    };
    
    for (const name of this.plugins.keys()) {
      visit(name);
    }
    
    return order;
  }
  
  provide<T>(name: string, service: T): this {
    if (service === undefined) {
      this.services.delete(name);
    } else {
      this.services.set(name, service);
    }
    return this;
  }
  
  getService<T>(name: string): T | undefined {
    return this.services.get(name);
  }
}

// ═══════════════════════════════════════════════
// 4. DEEPSEEK HARNESS PLUGIN EXAMPLES
// ═══════════════════════════════════════════════

/**
 * Example: Code Execution Plugin
 * Provides: code-executor service
 * Consumes: logger, config
 */
const codeExecutionPlugin: Plugin = {
  name: 'code-executor',
  description: 'Execute code in isolated sandbox',
  version: '1.0.0',
  provides: 'code-executor',
  consumes: ['logger', 'config'],
  config: {
    timeout: { type: 'number', default: 30000 },
    memoryLimit: { type: 'number', default: 128 },
  },
  
  init(ctx) {
    ctx.get('logger')?.info('[code-executor] Initializing...');
  },
  
  attach(ctx) {
    const logger = ctx.get('logger');
    const config = ctx.get('config');
    
    // Provide the code execution service
    ctx.provide('code-executor', {
      async execute(script: string, options?: { timeout?: number }) {
        logger?.info('[code-executor] Executing script...');
        // Implementation using VM sandbox
        return { success: true, result: 'output' };
      },
      
      async executeBatch(calls: Array<{tool: string, args: any}>) {
        // Batched execution for Code Mode
        return Promise.all(calls.map(c => this.execute(c.tool, c.args)));
      },
    });
  },
  
  ready(ctx) {
    ctx.get('logger')?.info('[code-executor] Ready!');
  },
  
  detach(ctx) {
    ctx.get('logger')?.info('[code-executor] Shutting down...');
  },
};

/**
 * Example: Trajectory Recorder Plugin
 * Provides: trajectory service
 * Consumes: memory-store, event-bus
 */
const trajectoryPlugin: Plugin = {
  name: 'trajectory-recorder',
  description: 'Record and replay agent trajectories',
  version: '1.0.0',
  provides: 'trajectory',
  consumes: ['memory-store', 'event-bus'],
  
  init(ctx) {
    // Setup trajectory schema
  },
  
  attach(ctx) {
    const memory = ctx.get('memory-store');
    const events = ctx.get('event-bus');
    
    ctx.provide('trajectory', {
      record(event: TrajectoryEvent) {
        // Append to session event stream
        return memory.append('trajectory', event);
      },
      
      replay(sessionId: string, toStep?: number) {
        // Replay trajectory to specific step
        return memory.query('trajectory', { sessionId, step: toStep });
      },
      
      fork(sessionId: string, fromStep: number) {
        // Fork trajectory from step
        return memory.fork('trajectory', { sessionId, fromStep });
      },
      
      search(query: TrajectoryQuery) {
        // Search trajectory events
        return memory.search('trajectory', query);
      },
    });
    
    // Listen to agent events
    events.on('agent:tool-call', (data) => {
      this.record({ type: 'tool-call', ...data, timestamp: Date.now() });
    });
  },
};

/**
 * Example: Runtime Mode Plugin
 * Manages 4 runtime modes: Standard, Code, Minimal Benchmark, Creator Inspector
 */
const runtimeModePlugin: Plugin = {
  name: 'runtime-modes',
  description: 'Manage 4 runtime modes',
  version: '1.0.0',
  provides: 'runtime-mode',
  consumes: ['code-executor', 'trajectory', 'logger'],
  
  init(ctx) {
    ctx.get('logger')?.info('[runtime-modes] Available modes: standard, code, benchmark, creator');
  },
  
  attach(ctx) {
    const executor = ctx.get('code-executor');
    const trajectory = ctx.get('trajectory');
    const logger = ctx.get('logger');
    
    const modes = {
      standard: {
        name: 'Standard Mode',
        description: 'Full agent with all tools',
        tools: ['read', 'write', 'search', 'execute', 'llm', 'memory', ...],
        isolation: 'process',
      },
      
      code: {
        name: 'Code Mode (@deepseek-ai/dsh)',
        description: 'Single-turn script execution, batched tools',
        tools: ['bash', 'editor', 'llm_complete'],
        isolation: 'vm-sandbox',
        batching: true,
        latencyReduction: '70-90%',
      },
      
      benchmark: {
        name: 'Minimal Benchmark Harness',
        description: 'Clean isolation for SWE-bench evaluation',
        tools: ['bash', 'editor'],
        isolation: 'container',
        deterministic: true,
      },
      
      creator: {
        name: 'Creator Inspector',
        description: 'Visual timeline, presets, debugging',
        tools: ['all'],
        features: ['timeline', 'presets', 'time-travel', 'fork'],
        isolation: 'process',
      },
    };
    
    ctx.provide('runtime-mode', {
      getMode(name: string) {
        return modes[name] || modes.standard;
      },
      
      listModes() {
        return Object.entries(modes).map(([key, m]) => ({ key, ...m }));
      },
      
      async execute(modeName: string, task: any) {
        const mode = modes[modeName] || modes.standard;
        logger?.info(`[runtime-modes] Executing in ${mode.name}`);
        
        switch (modeName) {
          case 'code':
            return await executor.executeBatch(task.script);
          case 'benchmark':
            return await executor.execute(task.script, { isolation: 'container' });
          default:
            return await this.executeStandard(task);
        }
      },
    });
  },
};

/**
 * Example: Minimal Benchmark Plugin
 * Clean isolation for SWE-bench evaluation
 */
const minimalBenchmarkPlugin: Plugin = {
  name: 'minimal-benchmark',
  description: 'Minimal harness for unbiased LLM evaluation',
  version: '1.0.0',
  provides: 'benchmark-harness',
  consumes: ['runtime-mode', 'logger'],
  
  attach(ctx) {
    const logger = ctx.get('logger');
    
    ctx.provide('benchmark-harness', {
      async runEvaluation(suite: string, model: string) {
        logger?.info(`[benchmark] Running ${suite} on ${model}`);
        
        // Only bash + editor tools available
        const result = await ctx.get('runtime-mode').execute('benchmark', {
          script: `
            // Isolated evaluation environment
            const fs = require('fs');
            const { execSync } = require('child_process');
            
            // Run test suite
            const result = execSync('npm test', { encoding: 'utf-8' });
            return { passed: result.includes('passed') };
          `,
        });
        
        return result;
      },
    });
  },
};

// ═══════════════════════════════════════════════
// 5. COMPOSING THE HARNESS
// ═══════════════════════════════════════════════

async function createDeepSeekHarness() {
  const kernel = new CordisKernelImpl();
  
  // Core infrastructure plugins
  kernel.plugin({
    name: 'logger',
    init(ctx) {
      ctx.provide('logger', console);
    },
  });
  
  kernel.plugin({
    name: 'config',
    init(ctx) {
      ctx.provide('config', {
        timeout: 30000,
        memoryLimit: 128,
        logLevel: 'info',
      });
    },
  });
  
  kernel.plugin({
    name: 'memory-store',
    provides: 'memory-store',
    attach(ctx) {
      // Implementation using vector DB or file-based
      ctx.provide('memory-store', {
        append: async (collection, data) => { /* ... */ },
        query: async (collection, query) => { /* ... */ },
        fork: async (collection, opts) => { /* ... */ },
        search: async (collection, query) => { /* ... */ },
      });
    },
  });
  
  kernel.plugin({
    name: 'event-bus',
    provides: 'event-bus',
    init(ctx) {
      ctx.provide('event-bus', new EventEmitter());
    },
  });
  
  // Feature plugins (order matters via requires)
  kernel.plugin(codeExecutionPlugin);    // provides: code-executor
  kernel.plugin(trajectoryPlugin);       // provides: trajectory, consumes: memory-store, event-bus
  kernel.plugin(runtimeModePlugin);      // provides: runtime-mode, consumes: code-executor, trajectory
  kernel.plugin(minimalBenchmarkPlugin); // provides: benchmark-harness, consumes: runtime-mode
  
  // Start the kernel
  await kernel.start();
  
  return kernel;
}

// Usage
const harness = await createDeepSeekHarness();

// Execute in Code Mode
const codeExecutor = harness.getService('code-executor');
const result = await codeExecutor.execute(`
  const files = await list_files({path: './src'});
  const content = await read_file({path: files[0]});
  const fixed = await llm_complete({prompt: \`Fix: \${content}\`});
  await write_file({path: files[0], content: fixed});
`);

// Or use Runtime Mode
const runtime = harness.getService('runtime-mode');
const benchmarkResult = await runtime.execute('benchmark', {
  script: 'npm test',
});

// Access trajectory
const trajectory = harness.getService('trajectory');
const events = await trajectory.search({ sessionId: 'abc123' });
await trajectory.replay('abc123', 5);  // Replay to step 5
await trajectory.fork('abc123', 3);    // Fork from step 3

interface TrajectoryEvent {
  type: 'prompt' | 'thought' | 'tool-call' | 'tool-result' | 'error';
  sessionId: string;
  step: number;
  timestamp: number;
  data: any;
}

interface TrajectoryQuery {
  sessionId?: string;
  type?: TrajectoryEvent['type'];
  stepRange?: [number, number];
  timeRange?: [number, number];
}
