// Hierarchical Planning — 3 levels
class ClaudePlanningSystem {
  // Level 1: Strategic planning (task level)
  async strategicPlan(goal: string): Promise<StrategicPlan> {
    return {
      approach: await this.selectApproach(goal),
      phases: await this.definePhases(goal),
      estimatedTime: await this.estimateTime(goal),
      checkpoints: await this.defineCheckpoints(goal),
    };
  }
  
  // Level 2: Tactical planning (phase level)
  async tacticalPlan(phase: Phase): Promise<TacticalPlan> {
    return {
      steps: await this.breakDownPhase(phase),
      tools: await this.selectTools(phase),
      parallelizable: await this.findParallelSteps(phase),
      rollbackPoints: await this.identifyRollbackPoints(phase),
    };
  }
  
  // Level 3: Operational planning (step level)
  async operationalPlan(step: Step): Promise<OperationalPlan> {
    return {
      action: await this.defineAction(step),
      parameters: await this.extractParameters(step),
      validation: await this.defineValidation(step),
      errorHandling: await this.defineErrorHandling(step),
    };
  }
}
