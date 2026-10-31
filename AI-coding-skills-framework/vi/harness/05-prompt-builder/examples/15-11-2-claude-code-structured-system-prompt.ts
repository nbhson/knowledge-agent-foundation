const claudeCodePrompt = {
  // Hierarchical instructions
  persona: "Expert software engineer",
  rules: [
    "Read files before modifying",
    "Write complete file contents",
    "Follow existing code style",
    "Add comments for complex logic",
  ],
  format: "Output code in markdown blocks with language tags",
  guardrails: [
    "Don't delete without reason",
    "Don't commit unless asked",
    "Ask before destructive operations",
  ],
};
