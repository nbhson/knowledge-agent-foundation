const MCPToolPlugin = {
  name: 'mcp-tool-plugin',
  apply: (ctx: Context) => {
    ctx.provide('tools', { executeTool: async (n: string, a: any) => ({ success: true }) });
  },
};
const kernel = new Context();
kernel.plugin(MCPToolPlugin);   // ← the line people forget
