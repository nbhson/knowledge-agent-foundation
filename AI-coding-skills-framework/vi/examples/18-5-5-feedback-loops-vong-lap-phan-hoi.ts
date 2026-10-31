interface FeedbackSystem {
  // Automatic feedback
  onSuccess: (task: Task, result: any) => void;
  onError: (task: Task, error: Error) => void;
  onTimeout: (task: Task) => void;
  
  // Metrics tracking
  metrics: {
    successRate: number;
    avgResponseTime: number;
    tokenUsage: number;
    errorTypes: Map<string, number>;
  };
  
  // Auto-optimization
  optimizer: {
    analyzePatterns: () => Insights;
    suggestImprovements: () => Suggestion[];
    autoAdjust: (metric: string) => void;
  };
}
