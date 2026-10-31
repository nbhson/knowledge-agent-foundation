interface Tool {
  name: string;
  description: string;
  parameters: JSONSchema;
  execute: (params: any) => Promise<ToolResult>;
  validation?: {
    preExecution?: (params: any) => boolean;
    postExecution?: (result: any) => boolean;
  };
}

// Example: File Editor Tool
const fileEditorTool: Tool = {
  name: "edit_file",
  description: "Edit a file with specified changes",
  parameters: {
    type: "object",
    properties: {
      path: { type: "string" },
      changes: { type: "array" }
    }
  },
  execute: async (params) => {
    // Implementation
    return { success: true, content: "..." };
  },
  validation: {
    preExecution: (params) => {
      // Check if path is safe
      return params.path.startsWith('/safe/');
    },
    postExecution: (result) => {
      // Validate syntax
      return linter.check(result.content);
    }
  }
};
