// Complete Harness Example
const harness = new AIHarness({
  model: "claude-3.5-sonnet",
  
  tools: [fileEditor, codeRunner, webSearch],
  
  memory: {
    shortTerm: { maxMessages: 20 },
    longTerm: { vectorStore: chromaDB },
    workingMemory: { maxSize: 10000 }
  },
  
  contextManager: {
    levels: 5,
    optimization: "smart",
    tokenLimit: 100000
  },
  
  guardrails: {
    input: [promptInjectionFilter, toxicityFilter],
    output: [sensitiveDataFilter, qualityChecker],
    behavioral: { maxIterations: 10, timeoutMs: 30000 }
  },
  
  feedback: {
    autoLog: true,
    metricsTracking: true,
    autoOptimize: true
  },
  
  permissions: {
    files: {
      read: ["/project/**"],
      write: ["/project/src/**"],
      delete: []
    },
    network: {
      allowedDomains: ["github.com", "stackoverflow.com"]
    }
  }
});
