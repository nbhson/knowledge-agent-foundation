class HarnessOrchestrator {
  async execute(userRequest: string): Promise<Result> {
    // 1. Validate input
    const inputCheck = await this.guardrails.validateInput(userRequest);
    if (!inputCheck.valid) {
      return { error: inputCheck.reason };
    }
    
    // 2. Build context
    const context = await this.contextManager.buildContext(userRequest);
    
    // 3. Check permissions
    const action = await this.planner.plan(userRequest);
    if (!this.permissions.allows(action)) {
      return { error: 'Permission denied' };
    }
    
    // 4. Execute with tools
    const result = await this.agent.execute(action, context);
    
    // 5. Validate output
    const outputCheck = await this.guardrails.validateOutput(result);
    if (!outputCheck.valid) {
      return await this.retry(action); // Retry logic
    }
    
    // 6. Update memory & feedback
    await this.memory.update(result);
    await this.feedback.log(action, result);
    
    return result;
  }
}
