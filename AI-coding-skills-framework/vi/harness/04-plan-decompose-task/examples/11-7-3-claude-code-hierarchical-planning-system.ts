// Hierarchical Planning — 3 cấp độ
class ClaudePlanningSystem {
  // Cấp độ 1: Lập kế hoạch chiến lược (Strategic Planning - cấp độ tác vụ)
  async strategicPlan(goal: string): Promise<StrategicPlan> {
    return {
      approach: await this.selectApproach(goal),
      phases: await this.definePhases(goal),
      estimatedTime: await this.estimateTime(goal),
      checkpoints: await this.defineCheckpoints(goal),
    };
  }
  
  // Cấp độ 2: Lập kế hoạch chiến thuật (Tactical Planning - cấp độ giai đoạn)
  async tacticalPlan(phase: Phase): Promise<TacticalPlan> {
    return {
      steps: await this.breakDownPhase(phase),
      tools: await this.selectTools(phase),
      parallelizable: await this.findParallelSteps(phase),
      rollbackPoints: await this.identifyRollbackPoints(phase),
    };
  }
  
  // Cấp độ 3: Lập kế hoạch vận hành (Operational Planning - cấp độ bước)
  async operationalPlan(step: Step): Promise<OperationalPlan> {
    return {
      action: await this.defineAction(step),
      parameters: await this.extractParameters(step),
      validation: await this.defineValidation(step),
      errorHandling: await this.defineErrorHandling(step),
    };
  }
}
