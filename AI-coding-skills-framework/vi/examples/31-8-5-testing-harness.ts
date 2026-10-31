// Test suite for harness
describe('Harness Tests', () => {
  test('Tool validation works', async () => {
    const result = await harness.executeTool('write_file', {
      path: '/unsafe/path'
    });
    expect(result.error).toBe('Path not allowed');
  });
  
  test('Context limits respected', async () => {
    const context = await harness.buildContext(largeQuery);
    const tokens = countTokens(context);
    expect(tokens).toBeLessThan(100000);
  });
  
  test('Guardrails catch sensitive data', async () => {
    const output = "API_KEY=sk_12345";
    const validation = await harness.validateOutput(output);
    expect(validation.valid).toBe(false);
  });
  
  test('Memory compression works', async () => {
    // Add 50 messages
    for (let i = 0; i < 50; i++) {
      await harness.addMessage({ content: `Message ${i}` });
    }
    expect(harness.memory.shortTerm.messages.length).toBeLessThan(25);
  });
});
