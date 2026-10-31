import { tools } from '@deepseek-ai/dsh';
const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const c = await tools.readFile(file);
  if (c.includes('legacyFetch'))
    await tools.writeFile(file, c.replace(/legacyFetch/g, 'modernFetch'));
}
