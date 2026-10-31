import { DynamicStructuredTool } from "@langchain/core/tools";
const search = new DynamicStructuredTool({
  name: "search", description: "Search the web",
  func: async (input) => { /* ... */ },
});
