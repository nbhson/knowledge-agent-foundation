class CursorPlanner {
  async plan(codeChange: string): Promise<Plan> {
    // 1. Understand the current Context
    const context = {
      currentFile: editor.getCurrentFile(),
      selectedCode: editor.getSelection(),
      cursorLine: editor.getCursorLine(),
      recentEdits: this.getRecentEdits(5),
      relatedFiles: await this.findRelatedFiles(),
      gitContext: await git.getContext(),
    };
    
    // 2. Plan the changes
    const plan = await this.planChanges(codeChange, context);
    
    // 3. Minimize the scope (do not touch unrelated files)
    const scopedPlan = this.minimizeScope(plan, context.currentFile);
    
    return scopedPlan;
  }
  
  private minimizeScope(plan: Plan, currentFile: string): Plan {
    return {
      ...plan,
      steps: plan.steps.filter(step => 
        this.isRelated(step.file, currentFile) || step.essential
      ),
    };
  }
}
