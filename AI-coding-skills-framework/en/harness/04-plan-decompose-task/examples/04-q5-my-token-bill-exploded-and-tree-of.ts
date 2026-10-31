canContinue(taskId: string): boolean {
  const allocated = this.allocated.get(taskId) || 0;
  const used = this.used.get(taskId) || 0;
  return used < allocated * 0.9;   // allow up to 90%
}
