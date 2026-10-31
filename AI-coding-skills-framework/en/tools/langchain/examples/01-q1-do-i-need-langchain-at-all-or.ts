const harness = {
  llm: new ChatOpenAI({ model: "gpt-4" }),
  tools: [ new DynamicStructuredTool({
    name: "search", description: "Search the web",
    func: async (input) => { /* ... */ }
  })]
};
