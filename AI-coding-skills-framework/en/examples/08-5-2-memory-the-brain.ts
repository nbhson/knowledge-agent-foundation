interface MemorySystem {
  // 1. Short-term Memory (Conversation)
  shortTerm: {
    maxMessages: number;
    messages: Message[];
    compress: () => void;
  };
  
  // 2. Long-term Memory (Knowledge)
  longTerm: {
    vectorStore: VectorDB;
    add: (content: string, metadata: any) => void;
    search: (query: string) => Promise<Document[]>;
  };
  
  // 3. Working Memory (Current Task)
  workingMemory: {
    currentTask: Task;
    subTasks: Task[];
    context: Map<string, any>;
  };
}
