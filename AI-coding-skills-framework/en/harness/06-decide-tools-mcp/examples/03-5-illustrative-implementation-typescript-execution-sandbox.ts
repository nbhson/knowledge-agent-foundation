import * as vm from 'vm';
import { HarnessSDK } from './sdk-types';

export class CodeModeExecutor {
  constructor(private sdk: HarnessSDK) {}

  public async executeScript(code: string, timeoutMs: number = 30000): Promise<{ success: boolean; result?: any; logs: string[]; error?: string }> {
    const logs: string[] = [];

    // 1. Create a safe Context with the approved APIs
    const sandboxContext = {
      dsh: this.sdk,
      console: {
        log: (...args: any[]) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')),
        error: (...args: any[]) => logs.push(`[ERROR] ${args.join(' ')}`),
      },
      setTimeout,
      clearTimeout,
    };

    // 2. Wrap the source code in an Async IIFE
    const wrappedCode = `
      (async () => {
        ${code}
      })();
    `;

    try {
      const vmContext = vm.createContext(sandboxContext);
      const script = new vm.Script(wrappedCode);

      // 3. Execute the source code in the sandbox with a timeout
      const result = await script.runInContext(vmContext, { timeout: timeoutMs });

      return { success: true, result, logs };
    } catch (err: any) {
      return {
        success: false,
        logs,
        error: err.message || String(err)
      };
    }
  }
}
