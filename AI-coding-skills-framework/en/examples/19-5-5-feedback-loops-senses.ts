class FeedbackLoop {
  async handleTaskCompletion(task: Task, result: TaskResult) {
    // 1. Log metrics
    await this.logMetrics({
      taskType: task.type,
      duration: result.duration,
      tokensUsed: result.tokensUsed,
      success: result.success
    });
    
    // 2. Analyze for patterns
    if (result.success) {
      await this.memory.longTerm.add(
        `Successful ${task.type}: ${result.approach}`,
        { type: 'success_pattern', task: task.type }
      );
    } else {
      await this.memory.longTerm.add(
        `Failed ${task.type}: ${result.error}`,
        { type: 'failure_pattern', task: task.type }
      );
    }
    
    // 3. Auto-adjust if needed
    if (this.metrics.successRate < 0.7) {
      await this.optimizer.suggestImprovements();
    }
  }
}
