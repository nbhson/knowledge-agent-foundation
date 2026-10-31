// ✅ Full control
const harness = new AIHarness({
  tools: {
    'file_edit': {
      validator: (path) => path.startsWith('/safe/dir'),
      maxSize: 10000,
      allowedExtensions: ['.js', '.ts', '.py']
    }
  },
  outputValidation: {
    checkSyntax: true,
    checkSecurity: true,
    runTests: true
  }
});

// You know exactly what the AI can do
// You guarantee the output is always valid
// You have detailed logs to debug with
