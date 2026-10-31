// Claude Code tự động re-plan khi gặp vấn đề
class DynamicReplanner {
  async handleFailure(
    failedStep: Step, 
    error: Error, 
    currentPlan: Plan
  ): Promise<Plan> {
    // 1. Phân tích lỗi
    const analysis = await this.analyzeFailure(failedStep, error);
    
    // 2. Thử sửa lỗi trong phạm vi kế hoạch hiện tại
    if (analysis.canFixInPlace) {
      return this.adjustStep(failedStep, analysis.fix);
    }
    
    // 3. Lập lại kế hoạch từ điểm này
    const remainingSteps = currentPlan.steps.filter(
      s => !s.dependencies.includes(failedStep.id)
    );
    
    return this.replan(remainingSteps, analysis.context);
  }
}
