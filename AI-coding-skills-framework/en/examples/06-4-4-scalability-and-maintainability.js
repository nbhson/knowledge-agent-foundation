// Fix it in one place inside the harness
harness.addSecurityRule({
  name: 'no-sensitive-data',
  validate: (output) => !containsSensitiveData(output)
});

// All agents automatically pick up this rule
// Test once
// Deploy in minutes
