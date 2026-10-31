// Plugin 1: Đăng ký Tool Service
const MCPToolPlugin = {
  name: 'mcp-tool-plugin',
  apply: (ctx: Context) => {
    ctx.provide('tools', {
      executeTool: async (name: string, args: any) => {
        console.log(`Executing MCP tool ${name}`, args);
        return { success: true };
      }
    });
  }
};

// Plugin 2: Log lại mọi lượt gọi Tool (Middleware Plugin)
const LoggerPlugin = {
  name: 'logger-plugin',
  apply: (ctx: Context) => {
    ctx.on('before-tool-call', (toolName: string) => {
      console.log(`[Event Stream] About to call tool: ${toolName}`);
    });
  }
};

// Khởi chạy Kernel
const kernel = new Context();
kernel.plugin(MCPToolPlugin);
kernel.plugin(LoggerPlugin);
