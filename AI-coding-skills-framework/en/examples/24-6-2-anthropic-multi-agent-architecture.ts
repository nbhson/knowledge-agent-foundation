// PLANNER AGENT
class PlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  tools = []; // No tools, pure planning
}

// GENERATOR AGENT
class GeneratorAgent {
  systemPrompt = `
    You are a code generator.
    Implement exactly what is asked in the step.
    Use provided tools to write and test code.
  `;
  
  tools = [
    writeFile,
    readFile,
    executeCode,
    installPackage
  ];
}

// EVALUATOR AGENT
class EvaluatorAgent {
  systemPrompt = `
    You are a quality evaluator.
    Check if the implementation meets requirements.
    Test for bugs, edge cases, and completeness.
    Decide: PASS or FAIL with specific feedback.
  `;
  
  tools = [
    runTests,
    checkSyntax,
    analyzeCode
  ];
}
