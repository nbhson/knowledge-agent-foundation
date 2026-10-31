class SmartContextManager {
  async buildOptimizedContext(query: string): Promise<string> {
    // 1. Always include system & task
    const core = this.getSystemAndTaskContext();
    
    // 2. Retrieve relevant domain knowledge
    const relevant = await this.retrieveRelevant(query);
    
    // 3. Add compressed conversation history
    const history = this.compressHistory();
    
    // 4. Include immediate context
    const immediate = this.getImmediateContext();
    
    // 5. Ensure under token limit
    return this.fitToLimit([core, relevant, history, immediate]);
  }
  
  private fitToLimit(contexts: string[]): string {
    const limit = 100000; // tokens
    let total = '';
    let tokenCount = 0;
    
    for (const ctx of contexts) {
      const tokens = this.countTokens(ctx);
      if (tokenCount + tokens < limit) {
        total += ctx;
        tokenCount += tokens;
      } else {
        // Truncate or skip
        break;
      }
    }
    
    return total;
  }
}
