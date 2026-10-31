// Planner → Generator → Evaluator
class AnthropicPlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  async plan(task: string): Promise<Plan> {
    // 1. Analyze the complexity of the task
    const complexity = await this.estimateComplexity(task);
    
    // 2. Create the step-by-step plan
    const steps = await this.generateSteps(task, complexity);
    
    // 3. Add the dependency graph
    const graphedSteps = this.addDependencies(steps);
    
    return {
      steps: graphedSteps,
      estimatedComplexity: complexity,
      parallelizableGroups: this.findParallelGroups(graphedSteps),
    };
  }
  
  private findParallelGroups(steps: Step[]): Step[][] {
    // Find steps that can run in parallel (no dependencies on each other)
    const groups: Step[][] = [];
    const remaining = [...steps];
    
    while (remaining.length > 0) {
      const group = remaining.filter(s => 
        s.dependencies.every(dep => 
          groups.some(g => g.some(gs => gs.id === dep))
        )
      );
      groups.push(group);
      remaining.splice(0, group.length);
    }
    
    return groups;
  }
}
