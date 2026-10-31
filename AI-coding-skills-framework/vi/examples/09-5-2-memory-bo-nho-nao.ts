class HarnessMemory implements MemorySystem {
  shortTerm = {
    maxMessages: 20,
    messages: [],
    compress: () => {
      // Summarize old messages when hitting limit
      if (this.messages.length > this.maxMessages) {
        const old = this.messages.slice(0, -10);
        const summary = this.summarize(old);
        this.messages = [
          { role: 'system', content: summary },
          ...this.messages.slice(-10)
        ];
      }
    }
  };
  
  longTerm = {
    vectorStore: new ChromaDB(),
    add: async (content, metadata) => {
      await this.vectorStore.add({
        content,
        metadata,
        embedding: await this.embed(content)
      });
    },
    search: async (query) => {
      return await this.vectorStore.search(query, { limit: 5 });
    }
  };
  
  workingMemory = {
    currentTask: null,
    subTasks: [],
    context: new Map()
  };
}
