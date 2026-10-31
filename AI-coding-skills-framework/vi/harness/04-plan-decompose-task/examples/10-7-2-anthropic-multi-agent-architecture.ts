// Bộ lập kế hoạch → Bộ tạo → Bộ đánh giá (Planner → Generator → Evaluator)
class AnthropicPlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  async plan(task: string): Promise<Plan> {
    // 1. Phân tích độ phức tạp của tác vụ
    const complexity = await this.estimateComplexity(task);
    
    // 2. Tạo kế hoạch theo từng bước
    const steps = await this.generateSteps(task, complexity);
    
    // 3. Thêm đồ thị phụ thuộc (dependency graph)
    const graphedSteps = this.addDependencies(steps);
    
    return {
      steps: graphedSteps,
      estimatedComplexity: complexity,
      parallelizableGroups: this.findParallelGroups(graphedSteps),
    };
  }
  
  private findParallelGroups(steps: Step[]): Step[][] {
    // Tìm các bước có thể chạy song song (không có phụ thuộc lẫn nhau)
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
