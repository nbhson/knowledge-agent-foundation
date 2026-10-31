const cursorPrompt = {
  // Dynamic context injection
  context: {
    currentFile: editor.getActiveDocument(),
    selection: editor.getSelection(),
    diagnostics: diagnostics.getForFile(currentFile),
    relatedFiles: await findRelatedFiles(currentFile),
    gitDiff: await git.getDiff(),
  },
  
  // Task-specific instructions
  instructions: `Based on the context above:
${userInstruction}
  
Consider:
- The selected code and its surrounding context
- Existing code style and patterns
- Related files and their imports
- Recent git changes`,
};
