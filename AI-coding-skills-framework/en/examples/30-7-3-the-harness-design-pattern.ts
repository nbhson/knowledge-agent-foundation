// Template for designing any harness
class HarnessDesignPattern {
  // 1. Define what AI CAN do
  defineCapabilities() {
    return {
      tools: [...],
      permissions: {...}
    };
  }
  
  // 2. Define what AI CANNOT do
  defineConstraints() {
    return {
      guardrails: [...],
      validators: [...]
    };
  }
  
  // 3. Define what AI SHOULD remember
  defineMemory() {
    return {
      shortTerm: {...},
      longTerm: {...},
      working: {...}
    };
  }
  
  // 4. Define how AI SHOULD learn
  defineFeedback() {
    return {
      onSuccess: () => {},
      onError: () => {},
      metrics: [...]
    };
  }
  
  // 5. Define how components WORK TOGETHER
  defineOrchestration() {
    return {
      workflow: [...],
      errorHandling: {...}
    };
  }
}
