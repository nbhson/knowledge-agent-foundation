class CursorPlanner {
  async plan(codeChange: string): Promise<Plan> {
    // 1. Thấu hiểu Context hiện tại
    const context = {
      currentFile: editor.getCurrentFile(),
      selectedCode: editor.getSelection(),
      cursorLine: editor.getCursorLine(),
      recentEdits: this.getRecentEdits(5),
      relatedFiles: await this.findRelatedFiles(),
      gitContext: await git.getContext(),
    };
    
    // 2. Lập kế hoạch thay đổi
    const plan = await this.planChanges(codeChange, context);
    
    // 3. Tối thiểu hóa phạm vi (không thay đổi các file không liên quan)
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
