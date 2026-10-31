// 3-Agent Architecture
class MultiAgentHarness {
  agents = {
    planner: new PlannerAgent(),
    generator: new GeneratorAgent(),
    evaluator: new EvaluatorAgent()
  };
  
  async execute(task: string): Promise<Result> {
    // 1. PLANNER: Plan
    const plan = await this.agents.planner.createPlan(task);
    /*
    Output example:
    {
      steps: [
        "1. Create game canvas",
        "2. Implement player movement",
        "3. Add collision detection",
        "4. Implement scoring system"
      ],
      estimatedComplexity: "medium"
    }
    */
    
    // 2. GENERATOR: Execute each step
    const results = [];
    for (const step of plan.steps) {
      const result = await this.agents.generator.generate(step);
      results.push(result);
      
      // 3. EVALUATOR: Evaluate after each step
      const evaluation = await this.agents.evaluator.evaluate(result, step);
      
      if (!evaluation.passed) {
        // Retry with feedback
        const retry = await this.agents.generator.generate(
          step,
          { previousAttempt: result, feedback: evaluation.feedback }
        );
        results[results.length - 1] = retry;
      }
    }
    
    // 4. FINAL EVALUATION
    const finalEval = await this.agents.evaluator.evaluateFinal(results);
    
    return {
      success: finalEval.passed,
      output: results,
      quality: finalEval.quality
    };
  }
}
