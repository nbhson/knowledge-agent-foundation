// Lập kế hoạch Harness cho SWE-agent
const swePlanner = {
  async plan(issue: string, codebase: CodebaseInfo) {
    // 1. Phân tích issue
    const analysis = await analyzeIssue(issue);
    
    // 2. Tìm files liên quan (KHÔNG đọc toàn bộ)
    const relevantFiles = await findRelevantFiles(analysis, codebase);
    
    // 3. Lập kế hoạch thực thi
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
