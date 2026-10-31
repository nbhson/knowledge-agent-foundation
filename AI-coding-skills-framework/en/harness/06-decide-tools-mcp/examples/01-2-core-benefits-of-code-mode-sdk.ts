// A single round-trip only! The LLM writes code that orchestrates the SDK:
import { tools } from '@deepseek-ai/dsh';

const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const content = await tools.readFile(file);
  if (content.includes('legacyFetch')) {
    const updated = content.replace(/legacyFetch/g, 'modernFetch');
    await tools.writeFile(file, updated);
  }
}
await tools.bash('pnpm lint');
