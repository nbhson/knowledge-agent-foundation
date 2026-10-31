// ✅ Kiểm soát hoàn toàn
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

// Bạn biết chính xác AI có thể làm gì
// Bạn đảm bảo output luôn valid
// Bạn có logs chi tiết để debug
