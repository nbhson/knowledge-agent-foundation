const LoggerPlugin = {
  name: 'logger-plugin',
  apply: (ctx: Context) => {
    ctx.on('before-tool-call', (toolName: string) =>
      console.log(`[Event Stream] About to call tool: ${toolName}`));
  }
};
