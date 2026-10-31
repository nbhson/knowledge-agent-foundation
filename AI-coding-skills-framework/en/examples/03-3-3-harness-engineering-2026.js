const harness = new AIHarness({
  model: "claude-3-opus",
  tools: [codeExecutor, fileManager, webSearch],
  memory: {
    shortTerm: conversationHistory,
    longTerm: vectorStore,
    workingMemory: currentContext
  },
  guardrails: {
    maxTokens: 100000,
    allowedDomains: ["github.com", "stackoverflow.com"],
    securityRules: [noSensitiveData, validateOutputs]
  },
  feedback: {
    onError: autoRetry,
    onSuccess: logMetrics
  }
});
