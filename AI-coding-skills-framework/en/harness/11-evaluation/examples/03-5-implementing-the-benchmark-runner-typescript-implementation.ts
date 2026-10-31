import { MinimalBashTool, MinimalEditorTool } from './minimal-tools';

export interface BenchmarkTask {
  id: string;
  problemStatement: string;
  repoPath: string;
  testCommand: string;
}

export class MinimalBenchmarkRunner {
  constructor(private llmClient: any) {}

  public async runTask(task: BenchmarkTask, maxTurns: number = 20): Promise<{ solved: boolean; turns: number; log: any[] }> {
    const bash = new MinimalBashTool(task.repoPath);
    const editor = new MinimalEditorTool(task.repoPath);

    // Minimal system prompt < 100 tokens
    const systemPrompt = `You are an expert software engineer. Solve the issue using bash and editor tools. When finished, output COMPLETE_TASK.`;

    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: task.problemStatement }
    ];

    const log: any[] = [];
    let turn = 0;

    while (turn < maxTurns) {
      turn++;
      // Call the LLM directly, without going through RAG or Memory Middleware
      const response = await this.llmClient.chat({
        messages,
        tools: [bash.definition, editor.definition]
      });

      log.push({ turn, response });

      if (response.content?.includes('COMPLETE_TASK')) {
        break;
      }

      if (response.toolCalls) {
        for (const call of response.toolCalls) {
          let toolResult: any;
          if (call.name === 'bash') {
            toolResult = await bash.execute(call.args);
          } else if (call.name === 'editor') {
            toolResult = await editor.execute(call.args);
          }

          messages.push({
            role: 'tool',
            tool_call_id: call.id,
            content: JSON.stringify(toolResult)
          });
        }
      }
    }

    // Verify the result with an objective test script
    const evalResult = await bash.execute({ command: task.testCommand });
    const solved = evalResult.exitCode === 0;

    return { solved, turns: turn, log };
  }
}
