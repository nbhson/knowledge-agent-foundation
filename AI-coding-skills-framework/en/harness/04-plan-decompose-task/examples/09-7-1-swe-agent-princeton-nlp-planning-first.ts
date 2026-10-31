// Harness planning for SWE-agent
const swePlanner = {
  async plan(issue: string, codebase: CodebaseInfo) {
    // 1. Analyze the issue
    const analysis = await analyzeIssue(issue);
    
    // 2. Find relevant files (DO NOT read everything)
    const relevantFiles = await findRelevantFiles(analysis, codebase);
    
    // 3. Build the execution plan
    return {
      steps: [
        { action: "read_file", path: relevantFiles[0], reason: "understand context" },
        { action: "search_code", pattern: analysis.functionName, reason: "find implementation" },
        { action: "edit_file", path: relevantFiles[0], changes: analysis.suggestedFix },
        { action: "run_tests", suite: "relevant", reason: "verify fix" },
      ],
      estimatedTokens: 15000,
      maxRetries: 2,
    };
  }
};
