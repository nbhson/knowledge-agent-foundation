// Planning System Interface — Tích hợp hoàn chỉnh với Harness
interface PlanningSystem {
  // Các năng lực lập kế hoạch cốt lõi
  decompose: (task: Task) => Promise<DecomposedPlan>;
  replan: (task: Task, failure: FailureInfo) => Promise<DecomposedPlan>;
  estimateComplexity: (task: Task) => ComplexityEstimate;
  
  // Quản lý trạng thái (State management)
  getState: () => AgentState;
  checkpoint: () => number;
  rollback: (checkpointId: number) => boolean;
  
  // Các điểm tích hợp
  tools: ToolRegistry;
  memory: MemorySystem;
  guardrails: GuardrailSystem;
  feedback: FeedbackSystem;
}

interface DecomposedPlan {
  rootTask: Task;
  subtasks: Task[];
  executionOrder: ExecutionStep[];
  estimatedTokens: number;
  estimatedTime: number;
  requiredTools: string[];
}

interface ExecutionStep {
  taskId: string;
  agentId: string;
  dependencies: string[];
  timeoutMs: number;
  tokenBudget: number;
  requiredPermissions: string[];
}

// Bộ lập kế hoạch tích hợp Harness hoàn chỉnh
class HarnessPlanner implements PlanningSystem {
  private tools: ToolRegistry;
  private memory: MemorySystem;
  private guardrails: GuardrailSystem;
  private feedback: FeedbackSystem;
  private state: AgentState;
  
  async decompose(task: Task): Promise<DecomposedPlan> {
    // 1. Kiểm tra tính hợp lệ của đầu vào
    const inputCheck = await this.guardrails.validateInput(task);
    if (!inputCheck.valid) {
      throw new Error(`Task validation failed: ${inputCheck.reason}`);
    }
    
    // 2. Kiểm tra Memory cho các tác vụ tương tự trong quá khứ
    const similarTasks = await this.memory.longTerm.search(
      `task: ${task.description}`,
      { limit: 3 }
    );
    
    // 3. Phân chia tác vụ với Context từ kinh nghiệm quá khứ
    const plan = await this.decomposeWithMemory(task, similarTasks);
    
    // 4. Kiểm tra kế hoạch đối chiếu với Guardrails
    const planValidation = await this.guardrails.validatePlan(plan);
    if (!planValidation.valid) {
      throw new Error(`Plan validation failed: ${planValidation.reason}`);
    }
    
    // 5. Ghi log phục vụ phản hồi
    await this.feedback.logPlan(task, plan);
    
    return plan;
  }
  
  async replan(task: Task, failure: FailureInfo): Promise<DecomposedPlan> {
    // Học hỏi từ thất bại
    await this.memory.longTerm.add(
      `Failed task: ${task.name}, Error: ${failure.error}`,
      { type: 'failure_pattern', task: task.name }
    );
    
    // Lập lại kế hoạch với Context thất bại
    const plan = await this.decompose(task);
    
    // Điều chỉnh dựa trên thất bại
    plan.executionOrder = plan.executionOrder.map(step => ({
      ...step,
      timeoutMs: step.timeoutMs * 1.5, // Tăng thời gian chờ (timeout)
      tokenBudget: step.tokenBudget * 1.2, // Tăng ngân sách Token
    }));
    
    return plan;
  }
  
  estimateComplexity(task: Task): ComplexityEstimate {
    const depth = this.getDepth(task);
    const breadth = this.getBreadth(task);
    
    return {
      score: Math.min(10, depth * 2 + breadth),
      depth,
      totalSubtasks: breadth,
      complexity: depth <= 1 ? 'simple' : depth <= 2 ? 'medium' : 'complex',
      recommendedApproach: breadth > 10 ? 'multi-agent' : 'single-agent',
    };
  }
  
  getState(): AgentState { return this.state; }
  checkpoint(): number { return this.state.checkpoint(); }
  rollback(id: number): boolean { return this.state.rollback(id); }
  
  private async decomposeWithMemory(task: Task, memories: any[]): Promise<DecomposedPlan> {
    // Triển khai sử dụng Memory của các tác vụ quá khứ
    // để nâng cao chất lượng phân chia tác vụ
    return { /* ... */ } as DecomposedPlan;
  }
  
  private getDepth(task: Task): number { /* ... */ return 0; }
  private getBreadth(task: Task): number { /* ... */ return 0; }
}
