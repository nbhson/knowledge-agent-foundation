// Fix tại 1 nơi trong harness
harness.addSecurityRule({
  name: 'no-sensitive-data',
  validate: (output) => !containsSensitiveData(output)
});

// Tất cả agents tự động có rule này
// Test 1 lần
// Deploy trong vài phút
