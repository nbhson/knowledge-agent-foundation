export interface HarnessSDK {
  fs: {
    readFile(path: string): Promise<string>;
    writeFile(path: string, content: string): Promise<void>;
    searchFiles(pattern: string): Promise<string[]>;
  };
  bash: {
    exec(command: string, options?: { timeoutMs?: number }): Promise<{ stdout: string; stderr: string; exitCode: number }>;
  };
  mcp: {
    callTool(serverName: string, toolName: string, args: Record<string, any>): Promise<any>;
  };
  logger: {
    info(msg: string): void;
    warn(msg: string): void;
    error(msg: string): void;
  };
}
