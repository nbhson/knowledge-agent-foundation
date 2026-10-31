class CursorHarness {
  // 1. CONTEXT AWARE - Biết bạn đang làm gì
  async buildContext(): Promise<Context> {
    return {
      // File đang mở
      currentFile: editor.getCurrentFile(),
      
      // Code đang select
      selectedCode: editor.getSelection(),
      
      // Cursor position
      cursorLine: editor.getCursorLine(),
      
      // Recent edits (để hiểu intent)
      recentEdits: this.getRecentEdits(5),
      
      // Related files (import/export)
      relatedFiles: await this.findRelatedFiles(),
      
      // Git context
      gitBranch: await git.getCurrentBranch(),
      uncommittedChanges: await git.getUncommittedChanges()
    };
  }
  
  // 2. SMART SUGGESTIONS
  async getSuggestions(context: Context): Promise<Suggestion[]> {
    // Dựa trên context, đưa ra suggestions phù hợp
    const suggestions = [];
    
    if (context.selectedCode) {
      suggestions.push({
        type: 'refactor',
        action: 'Refactor this code',
        confidence: 0.9
      });
      
      suggestions.push({
        type: 'explain',
        action: 'Explain this code',
        confidence: 0.95
      });
    }
    
    if (context.cursorLine.includes('TODO')) {
      suggestions.push({
        type: 'implement',
        action: 'Implement this TODO',
        confidence: 0.85
      });
    }
    
    return suggestions.sort((a, b) => b.confidence - a.confidence);
  }
  
  // 3. INCREMENTAL EDITS
  async applyEdit(edit: Edit): Promise<void> {
    // Không replace toàn bộ file
    // Chỉ thay đổi phần cần thiết
    await editor.replaceRange(
      edit.startLine,
      edit.endLine,
      edit.newContent
    );
    
    // Auto format
    await editor.formatDocument();
    
    // Run linter
    const lintResult = await linter.check();
    if (lintResult.errors.length > 0) {
      // Show inline errors
      editor.showErrors(lintResult.errors);
    }
  }
}
