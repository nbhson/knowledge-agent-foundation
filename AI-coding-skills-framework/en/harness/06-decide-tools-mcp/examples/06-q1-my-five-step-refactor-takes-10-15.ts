const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const content = await tools.readFile(file);
  if (content.includes('legacyFetch')) {
    await tools.writeFile(file, content.replace(/legacyFetch/g, 'modernFetch'));
  }
}
