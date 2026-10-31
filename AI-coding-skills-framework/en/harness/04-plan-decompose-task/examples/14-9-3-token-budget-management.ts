class TokenBudgetManager {
  private totalBudget: number;
  private allocated: Map<string, number>;
  private used: Map<string, number>;
  
  constructor(totalBudget: number = 100000) {
    this.totalBudget = totalBudget;
    this.allocated = new Map();
    this.used = new Map();
  }
  
  allocate(taskId: string, budget: number): boolean {
    const totalAllocated = Array.from(this.allocated.values()).reduce((a, b) => a + b, 0);
    
    if (totalAllocated + budget > this.totalBudget) {
      return false; // Not enough Token budget
    }
    
    this.allocated.set(taskId, budget);
    return true;
  }
  
  report(taskId: string, tokens: number): void {
    this.used.set(taskId, (this.used.get(taskId) || 0) + tokens);
  }
  
  canContinue(taskId: string): boolean {
    const allocated = this.allocated.get(taskId) || 0;
    const used = this.used.get(taskId) || 0;
    return used < allocated * 0.9; // Allow using up to 90%
  }
  
  getRemaining(): number {
    const totalUsed = Array.from(this.used.values()).reduce((a, b) => a + b, 0);
    return this.totalBudget - totalUsed;
  }
  
  getReport(): TokenReport {
    return {
      totalBudget: this.totalBudget,
      allocated: Object.fromEntries(this.allocated),
      used: Object.fromEntries(this.used),
      remaining: this.getRemaining(),
      efficiency: Array.from(this.used.values()).reduce((a, b) => a + b, 0) / 
                  Array.from(this.allocated.values()).reduce((a, b) => a + b, 1),
    };
  }
}
