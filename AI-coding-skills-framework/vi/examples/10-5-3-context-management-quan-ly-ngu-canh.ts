interface ContextManager {
  // Level 1: System Instructions
  systemContext: {
    identity: string;
    capabilities: string[];
    limitations: string[];
  };
  
  // Level 2: Task Context
  taskContext: {
    goal: string;
    constraints: string[];
    currentStep: number;
  };
  
  // Level 3: Domain Knowledge
  domainContext: {
    codebase: CodebaseInfo;
    documentation: Document[];
    conventions: Convention[];
  };
  
  // Level 4: Conversation History
  conversationContext: {
    history: Message[];
    summary: string;
  };
  
  // Level 5: Immediate Context
  immediateContext: {
    currentFile: string;
    recentChanges: Change[];
    openFiles: string[];
  };
  
  // Build final context for AI
  buildContext(): string;
}
